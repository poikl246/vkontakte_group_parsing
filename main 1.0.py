import json
import os
import time
from threading import Thread
import requests
import config


token = config.token
import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
bot = []


# настройка
#
if os.path.exists(f"BOT"):
    print(f"Директория с именем BOT уже существует!")
else:
    os.mkdir('BOT')
    f = open('BOT/user.txt', 'w', encoding='utf-8')
    f.close()
    f = open('BOT/group.txt', 'w', encoding='utf-8')
    f.close()





# group_name = input("Введите название группы: ")
#
# url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=40&access_token={token}&v=5.52"
# req = requests.get(url)
# print(req.text)

# API-ключ созданный ранее
TOKEN = config.TOKEN
vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk_session)
# Авторизуемся как сообщество
vk = vk_session.get_api()


def sender(user_id, message):
    vk.messages.send(  # Отправляем сообщение
        user_id=user_id,
        message=message,
        random_id=random.randint(-2147483648, +2147483648))



def message_output(message_text):
    f = open('BOT/user.txt', 'r', encoding='utf-8')
    file = f.readlines()
    f.close()

    for i in file:
        i = int(i)
        sender(i, message_text)



def get_wall_posts(group_name, id_group):
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=40&access_token={token}&v=5.52"
    req = requests.get(url)
    src = req.json()

    # print(src)

    # проверяем существует ли директория с именем группы
    if os.path.exists(f"{group_name}"):
        print(f"Директория с именем {group_name} уже существует!")
    else:
        os.mkdir(group_name)

    # сохраняем данные в json файл, чтобы видеть структуру
    with open(f"{group_name}/{group_name}.json", "w", encoding="utf-8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)

    # собираем ID новых постов в список
    fresh_posts_id = []
    posts = src["response"]["items"]




    for fresh_post_id in posts:
        fresh_post_id = fresh_post_id["id"]
        fresh_posts_id.append(fresh_post_id)

    print(fresh_posts_id)
    """Проверка, если файла не существует, значит это первый
    парсинг группы(отправляем все новые посты). Иначе начинаем
    проверку и отправляем только новые посты."""
    if not os.path.exists(f"{group_name}/exist_posts_{group_name}.txt"):
        print("Файла с ID постов не существует, создаём файл!")

        with open(f"{group_name}/exist_posts_{group_name}.txt", "w") as file:
            for item in fresh_posts_id:
                file.write(str(item) + "\n")

        # извлекаем данные из постов

    else:
        print("Файл с ID постов найден, начинаем выборку свежих постов!")
        f = open(f'{group_name}/exist_posts_{group_name}.txt', 'r', encoding='utf-8')
        file = f.readlines()
        f.close()

        # for one in fresh_posts_id:
        #     caunt = 1
        #     one = str(one)
        #
        #
        #     for twe in file:
        #         twe = str(twe)
        #         if one == twe[:-1]:
        #             caunt = 0
        #             break
        #
        #         print(one, twe)
        #     if caunt == 1:
        #         message_text = f'В группе {group_name} новый пост \n https://vk.com/{group_name}?w=wall{id_group}_50'
        #         message_output(message_text)
        w = []
        for one in fresh_posts_id:
            one = f'{one}\n'
            print(f'Точно {one}')
            try:
                print(one, file.index(one), 'tru')
            except:
                print(one, 123, 'except')
                w.append(one)
                message_text = f'В группе {group_name} новый пост \nhttps://vk.com/{group_name}?w=wall{id_group}_{int(one)}'
                message_output(message_text)
        print(w)

        f = open(f'{group_name}/exist_posts_{group_name}.txt', 'w', encoding='utf-8')
        for i in fresh_posts_id:
            f.write(f'{i}\n')
        f.close()

# def main():
#     group_name = "iot_urfu"
#     id_group = -206657927
#     get_wall_posts(group_name, id_group)
#
#
# # if __name__ == '__main__':
# #     main()



def schedule_loop(bot):
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            # Слушаем longpoll, если пришло сообщение то:
            if event.text == 'Начать' or event.text == '/start' or event.text == 'начать':  # Если написали заданную фраз
                f = open('BOT/user.txt', 'a', encoding='utf-8')
                f.write(f'{event.user_id}\n')
                f.close()
                sender(event.user_id, 'Спасибо, буду присылать посты')



# schedule_loop(bot)
def schedule_loop2(bot):
    while True:
        f = open('BOT/group.txt', 'r', encoding='utf-8')
        while True:
            try:
                lin, mas = f.readline().split()
                get_wall_posts(lin, mas)
            except:
                break
        f.close()
        time.sleep(15*60)


Thread(target=schedule_loop, args=(bot,)).start()
Thread(target=schedule_loop2, args=(bot,)).start()