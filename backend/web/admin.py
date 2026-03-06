from django.contrib import admin

from web.models.aifriend import AIFriend, AIFriendMessage, SystemPrompt
from web.models.character import Character
from web.models.conversation import Conversation
from web.models.conversion_member import ConversationMember
from web.models.friend import Friend
from web.models.message import Message
from web.models.user import UserProfile
# Register your models here.

#admin.site.register(UserProfile) 写法等价下边
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    #自定义后台显示行为 通过user筛选结果
    raw_id_fields = ("user",)

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    raw_id_fields = ("author",)

@admin.register(AIFriend)
class AIFriendAdmin(admin.ModelAdmin):
    raw_id_fields = ("me","character",)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    raw_id_fields = ()

@admin.register(ConversationMember)
class ConversationMemberAdmin(admin.ModelAdmin):
    raw_id_fields = ("conversation", "user", "last_read_message",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    raw_id_fields = ("conversation", "sender")

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", "friend",)

@admin.register(AIFriendMessage)
class AIMessageAdmin(admin.ModelAdmin):
    raw_id_fields = ('friend',)

admin.site.register(SystemPrompt)
