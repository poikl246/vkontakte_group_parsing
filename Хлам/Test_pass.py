import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


def send(user_id, attachment):
    random_id = random.randint(-2147483648, +2147483648)
    vk.messages.send(
        peer_id=user_id,
        random_id=random_id,
        message="Новый пост в группе!",
        attachment=attachment
        )


vk_session_group = vk_api.VkApi(token='2eeb04e788c270f9ae4dd6dbae8cdd7b73e6c7969f851c4fb4d951a37eae0e05c1b9abd669c1ca1b8fe1b') # Токен группы
vk = vk_session_group.get_api()
longpoll_group = VkBotLongPoll(vk_session_group, "205773876")  # ID группы

user_id = 333482474  # Кому отправлять репост

for event in longpoll_group.listen():
    if event.type == VkBotEventType.WALL_POST_NEW:
        id_ = event.object['id']
        owner_id_ = event.group_id
        wall_id = f'wall-{owner_id_}_{id_}'
        print('Новый пост! - ', wall_id)
        attachment = wall_id
        send(user_id, attachment)