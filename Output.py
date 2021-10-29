# token = "b83f6ac6e3efda45e3bb4ac68ca91074be1bed8480edba29be7641be6d86b8fd1abc472b9bcdccef5e88a"
# import vk_api
# import random
# from vk_api.longpoll import VkLongPoll, VkEventType
# bot = []
#
#
#
#
#
# def sender(user_id, message):
#     vk.messages.send(  # Отправляем сообщение
#         user_id=user_id,
#         message=message,
#         random_id=random.randint(-2147483648, +2147483648))
#
#
# # API-ключ созданный ранее
# TOKEN = "2eeb04e788c270f9ae4dd6dbae8cdd7b73e6c7969f851c4fb4d951a37eae0e05c1b9abd669c1ca1b8fe1b"
# vk_session = vk_api.VkApi(token=TOKEN)
# longpoll = VkLongPoll(vk_session)
# # Авторизуемся как сообщество
# vk = vk_session.get_api()
#
#
#
#
#
#
#
# def schedule_loop(bot):
#     for event in longpoll.listen():
#         if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
#             # Слушаем longpoll, если пришло сообщение то:
#             if event.text == '/start' or event.text == 'Второй вариант фразы':  # Если написали заданную фразу
#                     sender(event.user_id, 'хз')
#
# schedule_loop(bot)


f = open('BOT/group.txt', 'r', encoding='utf-8')

lin, mas = f.readline().split()
print(lin, '\n', mas)