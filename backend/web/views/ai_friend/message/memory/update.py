

from asgiref.sync import sync_to_async
from django.utils.timezone import now
from langchain_core.messages import SystemMessage, HumanMessage

from web.models.aifriend  import SystemPrompt, AIFriendMessage
from web.views.ai_friend.message.memory.graph import MemoryGraph


# def create_system_message():
#     system_prompts = SystemPrompt.objects.filter(title='记忆管理').order_by('order_number')
#     prompt = ''
#     for sp in system_prompts:
#         prompt += sp.prompt
#     return SystemMessage(prompt)
#
#
# def create_human_message(friend):
#     prompt = f'【原始记忆】\n{friend.memory}\n'
#     prompt += f'【最近对话】\n'
#     messages = list(AIFriendMessage.objects.filter(friend=friend).order_by('-id')[:10])
#     messages.reverse()
#     for m in messages:
#         prompt += f'user: {m.user_message}\n'
#         prompt += f'ai: {m.output}\n'
#     return HumanMessage(prompt)


@sync_to_async
def get_memory_prompt_data(friend):
    """同步查询记忆所需的各种数据"""
    # 1. 系统词
    system_prompts = SystemPrompt.objects.filter(title='记忆管理').order_by('order_number')
    sys_prompt_str = "".join([sp.prompt for sp in system_prompts])

    # 2. 最近对话
    messages = list(AIFriendMessage.objects.filter(friend=friend).order_by('-id')[:10])
    messages.reverse()
    history_str = f'【原始记忆】\n{friend.memory}\n【最近对话】\n'
    for m in messages:
        history_str += f'user: {m.user_message}\nai: {m.output}\n'

    return sys_prompt_str, history_str


async def update_memory(friend):
    """异步执行记忆更新流程"""
    sys_str, human_str = await get_memory_prompt_data(friend)

    app = MemoryGraph.create_app()

    inputs = {
        'messages': [
            SystemMessage(sys_str),
            HumanMessage(human_str),
        ]
    }

    res = await app.ainvoke(inputs)
    friend.memory = res['messages'][-1].content

    friend.update_time = now()
    await friend.asave()
