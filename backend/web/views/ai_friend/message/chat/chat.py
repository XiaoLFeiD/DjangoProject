import json
import asyncio
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain_core.messages import HumanMessage, BaseMessageChunk, BaseMessage, SystemMessage, AIMessage
from rest_framework_simplejwt.authentication import JWTAuthentication
from asgiref.sync import sync_to_async
from web.models.aifriend import AIFriend, AIFriendMessage, SystemPrompt
from web.views.ai_friend.message.chat.graph import ChatGraph

@sync_to_async
def add_system_prompt(state, friend):
    msgs = state['messages']
    system_prompts = SystemPrompt.objects.filter(title='回复').order_by('order_number')
    prompt = ''
    for sp in system_prompts:
        prompt += sp.prompt
    prompt += f'\n【角色性格】\n{friend.character.profile}\n'
    return {'messages': [SystemMessage(prompt)] + msgs}

@sync_to_async
def add_recent_messages(state, friend):
    msgs = state['messages']
    message_raw = list(AIFriendMessage.objects.filter(friend=friend).order_by('-id')[:10])
    message_raw.reverse()
    messages = []
    for m in message_raw:
        messages.append(HumanMessage(m.user_message))
        messages.append(AIMessage(m.output))
    return {'messages': msgs[:1] + messages + msgs[-1:]}


@csrf_exempt
async def ai_message_chat_view(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    @sync_to_async
    def authenticate_and_get_data():
        try:
            auth = JWTAuthentication()
            user_auth_tuple = auth.authenticate(request)
            if not user_auth_tuple: return None, None, None
            user, _ = user_auth_tuple
            data = json.loads(request.body)
            f_id, msg_text = data.get('friend_id'), data.get('message', '').strip()
            friend = AIFriend.objects.filter(pk=f_id, me__user=user).first()
            return user, friend, msg_text
        except: return None, None, None

    user, friend, message = await authenticate_and_get_data()
    if not user: return JsonResponse({'detail': '身份认证失败'}, status=401)
    if not friend: return JsonResponse({'result': '好友不存在'}, status=404)
    if not message: return JsonResponse({'result': '消息不能为空'}, status=400)

    app = ChatGraph.create_app()
    inputs = {'messages': [HumanMessage(message)]}
    inputs = await add_system_prompt(inputs, friend)
    inputs = await add_recent_messages(inputs, friend)

    async def event_stream():
        full_output = ''
        full_usage = {}
        try:
            # 使用 astream 异步流
            async for msg, metadata in app.astream(inputs, stream_mode="messages"):
                # 只要是消息类型就检查元数据（统计信息通常在最后一个空内容包里）
                if isinstance(msg, (BaseMessage, BaseMessageChunk)):
                    if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
                        full_usage = msg.usage_metadata

                    # 只有有内容时才 yield
                    if msg.content:
                        full_output += msg.content
                        print(msg.content, end="", flush=True)
                        yield f'data: {json.dumps({"content": msg.content}, ensure_ascii=False)}\n\n'
                        await asyncio.sleep(0.01)

            yield 'data: [DONE]\n\n'
            # 在后端控制台强制打印统计
            # print(f"\n统计数据: {full_usage}")
            input_tokens = full_usage.get('input_tokens', 0)
            output_tokens = full_usage.get('output_tokens', 0)
            total_tokens = full_usage.get('total_tokens', 0)

            await AIFriendMessage.objects.acreate(
                friend=friend,
                user_message=message[:500],
                input=json.dumps(
                    [m.model_dump() for m in inputs['messages']],
                    ensure_ascii=False,
                )[:10000],
                output=full_output[:500],
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
            )
            # print(f"\n消息已成功异步保存到数据库，Token 统计: {full_usage}")
        except Exception as e:
            print(f"\n流错误: {str(e)}")
            yield f'data: {json.dumps({"error": str(e)})}\n\n'

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response