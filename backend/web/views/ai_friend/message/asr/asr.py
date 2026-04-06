# import asyncio
# import json
# import os
# import uuid
#
# import websockets
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
#
#
# class ASRAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         audio = request.FILES.get('audio')
#         if not audio:
#             return Response({
#                 'result': '音频不存在'
#             })
#         pcm_data = audio.read()
#         text = asyncio.run(self.run_asr_tasks(pcm_data))
#         print(text)
#         return Response({
#             'result': 'success',
#             'text': text,
#         })
#
#     async def asr_sender(self, pcm_data, ws, task_id):
#         chunk = 3200  #pcm16 1s采样16000 16位 2byte 100ms3200字节
#
#         for i in range(0, len(pcm_data), chunk):
#             await ws.send(pcm_data[i: i+chunk])
#             await asyncio.sleep(0.01) #文档建议在传输100ms数据后 等待100ms
#
#         await ws.send(json.dumps({
#             "header": {
#                 "action": "finish-task", #告诉LLM结束语音传输
#                 "task_id": task_id,
#                 "streaming": "duplex"
#             },
#             "payload": {
#                 "input": {}
#             }
#
#         }))
#
#     async def asr_receiver(self, ws):
#         text = ''
#         async for msg in ws:
#             data = json.loads(msg)
#             event = data['header']['event']
#             if event == 'result-generated':
#                 output = data['payload']['output']
#                 if output.get('transcription', None) and output['transcription']['sentence_end']:
#                     text += output['transcription']['text']
#             elif event in ['task-finished', 'task-failed']:
#                 break
#         return text
#     async def run_asr_tasks(self, pcm_data):
#         task_id = uuid.uuid4().hex
#         api_key = os.getenv('API_KEY')
#         wss_url = os.getenv('WSS_URL')
#         headers = {
#             "Authorization": f"Bearer {api_key}"
#         }
#         async with websockets.connect(wss_url, additional_headers=headers) as ws:
#             await ws.send(json.dumps({
#                 "header": {
#                     "streaming": "duplex",
#                     "task_id": task_id,
#                     "action": "run-task"
#                 },
#                 "payload": {
#                     "model": "gummy-realtime-v1",
#                     "parameters": {
#                         "sample_rate": 16000,
#                         "format": "pcm",
#                         "transcription_enabled": True,
#                     },
#                     "input": {},
#                     "task": "asr",
#                     "task_group": "audio",
#                     "function": "recognition"
#                 }
#             }))
#             async for msg in ws:
#                 if json.loads(msg)['header']['event'] == 'task_started':
#                     break
#             _, text = await asyncio.gather(
#                 self.asr_sender(pcm_data, ws, task_id),
#                 self.asr_receiver(ws),
#             )
#             return text


import asyncio
import json
import os
import uuid
import websockets
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from asgiref.sync import sync_to_async


# ASR 发送逻辑
async def asr_sender(pcm_data, ws, task_id):
    chunk = 3200  # 100ms
    try:
        for i in range(0, len(pcm_data), chunk):
            await ws.send(pcm_data[i: i + chunk])
            await asyncio.sleep(0.01)  # 模拟真实流式发送频率

        await ws.send(json.dumps({
            "header": {
                "action": "finish-task",
                "task_id": task_id,
                "streaming": "duplex"
            },
            "payload": {"input": {}}
        }))
    except Exception as e:
        print(f"Sender Error: {e}")


# ASR 接收逻辑
async def asr_receiver(ws):
    text = ''
    try:
        async for msg in ws:
            data = json.loads(msg)
            event = data['header']['event']
            if event == 'result-generated':
                output = data['payload'].get('output')
                if output and output.get('transcription') and output['transcription']['sentence_end']:
                    text += output['transcription']['text']
            elif event in ['task-finished', 'task-failed']:
                break
    except Exception as e:
        print(f"Receiver Error: {e}")
    return text


@csrf_exempt
async def asr_process_view(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    # 1. 在同步包装器中处理认证和文件读取
    @sync_to_async
    def authenticate_and_get_audio():
        try:
            # 手动执行 JWT 认证
            auth = JWTAuthentication()
            user_auth_tuple = auth.authenticate(request)
            if not user_auth_tuple:
                return None, None

            user, _ = user_auth_tuple

            # 获取音频文件
            audio_file = request.FILES.get('audio')
            if not audio_file:
                return user, None

            # 直接在同步环境下读取二进制内容
            pcm_data = audio_file.read()
            return user, pcm_data
        except Exception as e:
            print(f"Auth/File Error: {e}")
            return None, None

    user, pcm_data = await authenticate_and_get_audio()

    # 2. 基础检查
    if not user:
        return JsonResponse({'detail': '身份认证失败'}, status=401)
    if not pcm_data:
        return JsonResponse({'result': '音频数据为空'}, status=400)

    # 3. 异步 WebSocket 通信逻辑
    task_id = uuid.uuid4().hex
    api_key = os.getenv('API_KEY')
    wss_url = os.getenv('WSS_URL')

    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        async with websockets.connect(wss_url, additional_headers=headers) as ws:
            # 发送启动指令
            await ws.send(json.dumps({
                "header": {
                    "streaming": "duplex",
                    "task_id": task_id,
                    "action": "run-task"
                },
                "payload": {
                    "model": "gummy-realtime-v1",
                    "parameters": {
                        "sample_rate": 16000,
                        "format": "pcm",
                        "transcription_enabled": True,
                    },
                    "input": {}, "task": "asr", "task_group": "audio", "function": "recognition"
                }
            }))

            # 等待确认
            async for msg in ws:
                if json.loads(msg)['header']['event'] == 'task-started':
                    break

            # 并发运行发送和接收
            # 使用 gather 拿到 receiver 返回的 text
            _, final_text = await asyncio.gather(
                asr_sender(pcm_data, ws, task_id),
                asr_receiver(ws)
            )

            return JsonResponse({
                'result': 'success',
                'text': final_text
            })

    except Exception as e:
        print(f"WebSocket 异常: {str(e)}")
        return JsonResponse({'result': 'failed', 'error': str(e)}, status=500)