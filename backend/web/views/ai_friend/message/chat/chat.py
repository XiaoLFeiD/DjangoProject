# 语音合成前的代码
# import json
# import asyncio
# from django.http import StreamingHttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from langchain_core.messages import HumanMessage, BaseMessageChunk, BaseMessage, SystemMessage, AIMessage
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from asgiref.sync import sync_to_async
# from web.models.aifriend import AIFriend, AIFriendMessage, SystemPrompt
# from web.views.ai_friend.message.chat.graph import ChatGraph
# from web.views.ai_friend.message.memory.update import update_memory
#
#
# @sync_to_async
# def add_system_prompt(state, friend):
#     msgs = state['messages']
#     system_prompts = SystemPrompt.objects.filter(title='回复').order_by('order_number')
#     prompt = ''
#     for sp in system_prompts:
#         prompt += sp.prompt
#     prompt += f'\n【角色性格】\n{friend.character.profile}\n'
#     prompt += f'【长期记忆】\n{friend.memory}\n'
#     return {'messages': [SystemMessage(prompt)] + msgs}
#
# @sync_to_async
# def add_recent_messages(state, friend):
#     msgs = state['messages']
#     message_raw = list(AIFriendMessage.objects.filter(friend=friend).order_by('-id')[:10])
#     message_raw.reverse()
#     messages = []
#     for m in message_raw:
#         messages.append(HumanMessage(m.user_message))
#         messages.append(AIMessage(m.output))
#     return {'messages': msgs[:1] + messages + msgs[-1:]}
#
#
# @csrf_exempt
# async def ai_message_chat_view(request):
#     if request.method != 'POST':
#         return JsonResponse({'detail': 'Method not allowed'}, status=405)
#
#     @sync_to_async
#     def authenticate_and_get_data():
#         try:
#             auth = JWTAuthentication()
#             user_auth_tuple = auth.authenticate(request)
#             if not user_auth_tuple: return None, None, None
#             user, _ = user_auth_tuple
#             data = json.loads(request.body)
#             f_id, msg_text = data.get('friend_id'), data.get('message', '').strip()
#             friend = AIFriend.objects.select_related('character').filter(pk=f_id, me__user=user).first()
#             return user, friend, msg_text
#         except: return None, None, None
#
#     user, friend, message = await authenticate_and_get_data()
#     if not user: return JsonResponse({'detail': '身份认证失败'}, status=401)
#     if not friend: return JsonResponse({'result': '好友不存在'}, status=404)
#     if not message: return JsonResponse({'result': '消息不能为空'}, status=400)
#
#     app = ChatGraph.create_app()
#     inputs = {'messages': [HumanMessage(message)]}
#     inputs = await add_system_prompt(inputs, friend)
#     inputs = await add_recent_messages(inputs, friend)
#
#     async def event_stream():
#         full_output = ''
#         full_usage = {}
#         try:
#             # 使用 astream 异步流
#             async for msg, metadata in app.astream(inputs, stream_mode="messages"):
#                 # 只要是消息类型就检查元数据（统计信息通常在最后一个空内容包里）
#                 if isinstance(msg, (BaseMessage, BaseMessageChunk)):
#                     if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
#                         full_usage = msg.usage_metadata
#
#                     # 只有有内容时才 yield
#                     if msg.content:
#                         full_output += msg.content
#                         print(msg.content, end="", flush=True)
#                         yield f'data: {json.dumps({"content": msg.content}, ensure_ascii=False)}\n\n'
#                         await asyncio.sleep(0.01)
#
#             yield 'data: [DONE]\n\n'
#             # 在后端控制台强制打印统计
#             # print(f"\n统计数据: {full_usage}")
#             input_tokens = full_usage.get('input_tokens', 0)
#             output_tokens = full_usage.get('output_tokens', 0)
#             total_tokens = full_usage.get('total_tokens', 0)
#
#             await AIFriendMessage.objects.acreate(
#                 friend=friend,
#                 user_message=message[:500],
#                 input=json.dumps(
#                     [m.model_dump() for m in inputs['messages']],
#                     ensure_ascii=False,
#                 )[:10000],
#                 output=full_output[:500],
#                 input_tokens=input_tokens,
#                 output_tokens=output_tokens,
#                 total_tokens=total_tokens,
#             )
#             # print(f"\n消息已成功异步保存到数据库，Token 统计: {full_usage}")
#             msg_count = await AIFriendMessage.objects.filter(friend=friend).acount()
#             if msg_count % 1 == 0:  # 你设定的逻辑
#                 # 调用上面定义的异步更新函数
#                 await update_memory(friend)
#         except Exception as e:
#             print(f"\n流错误: {str(e)}")
#             yield f'data: {json.dumps({"error": str(e)})}\n\n'
#
#
#     response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
#     response['Cache-Control'] = 'no-cache'
#     response['X-Accel-Buffering'] = 'no'
#     return response

import json
import asyncio
import os
import uuid
import base64
import websockets
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain_core.messages import HumanMessage, BaseMessageChunk, BaseMessage, SystemMessage, AIMessage
from rest_framework_simplejwt.authentication import JWTAuthentication
from asgiref.sync import sync_to_async

from web.models.aifriend import AIFriend, AIFriendMessage, SystemPrompt
from web.views.ai_friend.message.chat.graph import ChatGraph
from web.views.ai_friend.message.memory.update import update_memory


# --- 辅助同步转异步函数 ---

@sync_to_async
def get_prompts_and_history(friend, message):
    # 1. 获取系统提示词
    system_prompts = SystemPrompt.objects.filter(title='回复').order_by('order_number')
    prompt_str = "".join([sp.prompt for sp in system_prompts])
    prompt_str += f'\n【角色性格】\n{friend.character.profile}\n'
    prompt_str += f'【长期记忆】\n{friend.memory}\n'

    # 2. 获取历史消息 (最近10条)
    message_raw = list(AIFriendMessage.objects.filter(friend=friend).order_by('-id')[:10])
    message_raw.reverse()

    history = []
    for m in message_raw:
        history.append(HumanMessage(m.user_message))
        history.append(AIMessage(m.output))

    # 3. 构造 LangChain 输入
    inputs = {
        'messages': [SystemMessage(prompt_str)] + history + [HumanMessage(message)]
    }
    return inputs


@csrf_exempt
async def ai_message_chat_tts_view(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    # 1. 身份认证与初步数据获取
    @sync_to_async
    def authenticate_and_get_data():
        try:
            auth = JWTAuthentication()
            user_auth_tuple = auth.authenticate(request)
            if not user_auth_tuple: return None, None, None
            user, _ = user_auth_tuple
            data = json.loads(request.body)
            f_id, msg_text = data.get('friend_id'), data.get('message', '').strip()
            friend = AIFriend.objects.select_related('character').filter(pk=f_id, me__user=user).first()
            return user, friend, msg_text
        except:
            return None, None, None

    user, friend, message = await authenticate_and_get_data()
    if not user: return JsonResponse({'detail': '身份认证失败'}, status=401)
    if not friend: return JsonResponse({'result': '好友不存在'}, status=404)
    if not message: return JsonResponse({'result': '消息不能为空'}, status=400)

    # 2. 准备 LangChain 输入
    inputs = await get_prompts_and_history(friend, message)
    app = ChatGraph.create_app()

    # 3. 定义异步生成器（核心逻辑）
    async def event_stream():
        # 使用 asyncio.Queue 代替线程 Queue
        mq = asyncio.Queue()
        task_id = uuid.uuid4().hex
        api_key = os.getenv('API_KEY')
        wss_url = os.getenv('WSS_URL')
        headers = {"Authorization": f"Bearer {api_key}"}

        full_output = ''
        full_usage = {}

        # 内部：TTS 发送者 (处理 LangChain 流并发送给 WebSocket)
        async def tts_sender(ws):
            nonlocal full_output, full_usage
            async for msg, metadata in app.astream(inputs, stream_mode="messages"):
                if isinstance(msg, (BaseMessage, BaseMessageChunk)) and msg.content:
                    # 发送给 TTS WebSocket
                    await ws.send(json.dumps({
                        "header": {"action": "continue-task", "task_id": task_id, "streaming": "duplex"},
                        "payload": {"input": {"text": msg.content}}
                    }))
                    # 放入队列发给前端显示文字
                    full_output += msg.content
                    await mq.put({'content': msg.content})

                    if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
                        full_usage = msg.usage_metadata

            # LLM 生成结束，告诉 TTS 结束
            await ws.send(json.dumps({
                "header": {"action": "finish-task", "task_id": task_id, "streaming": "duplex"},
                "payload": {"input": {}}
            }))

        # 内部：TTS 接收者 (从 WebSocket 接收音频)
        async def tts_receiver(ws):
            async for msg in ws:
                if isinstance(msg, bytes):
                    audio_b64 = base64.b64encode(msg).decode('utf-8')
                    await mq.put({'audio': audio_b64})
                else:
                    data = json.loads(msg)
                    if data['header']['event'] in ['task-finished', 'task-failed']:
                        break

        # 启动 WebSocket 任务
        async def run_ws_orchestrator():
            try:
                async with websockets.connect(wss_url, additional_headers=headers) as ws:
                    # 初始化 TTS
                    await ws.send(json.dumps({
                        "header": {"action": "run-task", "task_id": task_id, "streaming": "duplex"},
                        "payload": {
                            "task_group": "audio", "task": "tts", "function": "SpeechSynthesizer",
                            "model": "cosyvoice-v3-flash",
                            "parameters": {
                                "text_type": "PlainText", "voice": "longanyang", "format": "mp3",
                                "sample_rate": 22050, "volume": 50, "rate": 1.25, "pitch": 1
                            },
                            "input": {}
                        }
                    }))

                    # 等待启动
                    async for msg in ws:
                        if json.loads(msg)['header']['event'] == 'task-started':
                            break

                    # 同时运行发送和接收
                    await asyncio.gather(tts_sender(ws), tts_receiver(ws))
            except Exception as e:
                await mq.put({'error': str(e)})
            finally:
                # 放入 None 作为结束标志
                await mq.put(None)

        # 在后台启动编排任务（非阻塞）
        orchestrator_task = asyncio.create_task(run_ws_orchestrator())

        # 主循环：从 Queue 中读取内容并 yield 给 StreamingHttpResponse
        try:
            while True:
                item = await mq.get()
                if item is None:
                    break
                # print(item)
                # print("到这里了！！！")

                if 'error' in item:
                    yield f'data: {json.dumps({"error": item["error"]})}\n\n'
                    break

                yield f'data: {json.dumps(item, ensure_ascii=False)}\n\n'
                # 小额延迟防止占用过高
                await asyncio.sleep(0.001)

            yield 'data: [DONE]\n\n'

            # 4. 保存到数据库 (异步操作)
            await AIFriendMessage.objects.acreate(
                friend=friend,
                user_message=message[:500],
                input=json.dumps([m.model_dump() for m in inputs['messages']], ensure_ascii=False)[:10000],
                output=full_output[:500],
                input_tokens=full_usage.get('input_tokens', 0),
                output_tokens=full_usage.get('output_tokens', 0),
                total_tokens=full_usage.get('total_tokens', 0),
            )

            # 5. 更新记忆逻辑
            msg_count = await AIFriendMessage.objects.filter(friend=friend).acount()
            if msg_count % 1 == 0:
                await update_memory(friend)

        except Exception as e:
            print(f"Streaming Error: {e}")
            yield f'data: {json.dumps({"error": "流中断"})}\n\n'

    # 返回异步流响应
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response