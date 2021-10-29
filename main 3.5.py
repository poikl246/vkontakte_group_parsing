import json
import os
import time
from threading import Thread
import requests
import config
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
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
upload = VkUpload(vk)

def sender(user_id, message):
    vk.messages.send(  # Отправляем сообщение
        user_id=user_id,
        message=message,
        random_id=random.randint(-2147483648, +2147483648))





def message_output(message_text, group_name, one, fresh_posts_id):
    f = open(f'BOT/{group_name}.txt', 'r', encoding='utf-8')
    file_id = f.readlines()
    f.close()
    print(file_id)
    for i in file_id:
        i = int(i)
        print(i)
        sender(i, message_text)
        # time.sleep(1)
        try:
            send_photo(vk, i, *upload_photo(upload, f'{group_name}/files/{int(one)}.jpg'), fresh_posts_id, group_name)
        except:
            try:
                send_photo(vk, i, *upload_photo(upload, f'{group_name}/files/{int(one)}_0.jpg'), fresh_posts_id, group_name)
            except:
                pass


def upload_photo(upload, photo):
    response = upload.photo_messages(photo)[0]

    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']

    return owner_id, photo_id, access_key




def send_photo(vk, peer_id, owner_id, photo_id, access_key, fresh_posts_id, group_name):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'

    vk.messages.send(
        random_id=get_random_id(),
        peer_id=peer_id,
        attachment=attachment
    )




def get_wall_posts_id(group_name):
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
        id_group = fresh_post_id["from_id"]
        fresh_post_id = fresh_post_id["id"]
        fresh_posts_id.append(fresh_post_id)

    print(id_group)

    text_post_list = []
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
                message_output(message_text, group_name, one, fresh_posts_id)
        print(w)

        f = open(f'{group_name}/exist_posts_{group_name}.txt', 'w', encoding='utf-8')
        for i in fresh_posts_id:
            f.write(f'{i}\n')
        f.close()

    return id_group



def get_wall_posts(group_name, id_group, smaile):
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

    text_post_list = []
    for fresh_post_id in posts:
        text_post = fresh_post_id["text"]
        text_post_list.append(text_post)
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
        with open(f"{group_name}/exist_posts_{group_name}.txt", "r") as file_list_yas:
            id_post_list = file_list_yas.readlines()
        print(id_post_list)

        def download_img(url, post_id, group_name):
            res = requests.get(url)

            # создаем папку group_name/files
            if not os.path.exists(f"{group_name}/files"):
                os.mkdir(f"{group_name}/files")

            with open(f"{group_name}/files/{post_id}.jpg", "wb") as img_file:
                img_file.write(res.content)

        for post in posts:
            print(post)
            # функция для сохранения изображений

            # функция для сохранения видео

            post_id = post["id"]
            print(f"Отправляем пост с ID {post_id}")
            if id_post_list.count(f"{post_id}\n") == 0:
                print(1)
                try:
                    if "attachments" in post:
                        post = post["attachments"]

                        photo_quality = [
                            "photo_2560",
                            "photo_1280",
                            "photo_807",
                            "photo_604",
                            "photo_130",
                            "photo_75"
                        ]

                        # проверка на 1 или несколько фото/видео в посте
                        if len(post) == 1:

                            # забираем фото
                            if post[0]["type"] == "photo":

                                for pq in photo_quality:
                                    if pq in post[0]["photo"]:
                                        post_photo = post[0]["photo"][pq]
                                        print(f"Фото с расширением {pq}")
                                        print(post_photo)
                                        download_img(post_photo, post_id, group_name)
                                        break
                            # забираем видео

                            else:
                                print("Либо линк, либо аудио, либо репост...")
                        else:
                            photo_post_count = 0
                            for post_item_photo in post:
                                if post_item_photo["type"] == "photo":
                                    for pq in photo_quality:
                                        if pq in post_item_photo["photo"]:
                                            post_photo = post_item_photo["photo"][pq]
                                            print(f"Фото с расширением {pq}")
                                            print(post_photo)
                                            post_id_counter = str(post_id) + f"_{photo_post_count}"
                                            download_img(post_photo, post_id_counter, group_name)
                                            photo_post_count += 1
                                            break
                                            # забираем видео

                                else:
                                    print("Либо линк, либо аудио, либо репост...")


                except Exception:
                    print(f"Что-то пошло не так с постом ID {post_id}!")

            else:
                print('уже парсили')



        f = open(f'{group_name}/exist_posts_{group_name}.txt', 'r', encoding='utf-8')
        file = f.readlines()
        f.close()

        w = []
        for one in fresh_posts_id:
            one1 = one
            one = f'{one}\n'
            print(f'Точно {one}')
            try:
                print(one, file.index(one), 'tru')
            except:
                print(one, 123, 'except')
                w.append(one)
                text_post_print = text_post_list[fresh_posts_id.index(one1)]
                print(text_post_print)

                if smaile == 1:
                    message_text = f'😃😃😃😃😃😃😃😃😃😃😃😃😃😃😃😃\n' \
                                   f'В ГРУППЕ {group_name} НОВЫЙ ПОСТ \nhttps://vk.com/{group_name}?w=wall{id_group}_{int(one)}\n\n\n\n\n "{text_post_print} \n\n"' \
                                   f'😃😃😃😃😃😃😃😃😃😃😃😃😃😃😃😃'
                else:
                    message_text = f'В ГРУППЕ {group_name} НОВЫЙ ПОСТ \nhttps://vk.com/{group_name}?w=wall{id_group}_{int(one)}\n\n\n\n\n "{text_post_print}"'

                message_output(message_text, group_name, one, fresh_posts_id)
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
                sender(event.user_id, 'Введите интересующие вас группы при командой\n/new_group group\n'
                                      'group - название группы (из поисковой строки). Подробности тут: https://vk.com/radio_engineering_urfu_bot?w=wall-206917464_3 \n'
                                      '\n'
                                      'Помощь - /help')
            if '/new_group' in event.text:  # Если написали заданную фраз

                if os.path.exists(f"BOT/{event.text[11:]}.txt"):
                    print(f"Файл с именем {event.text[11:]} уже существует!")
                    input_file = open(f"BOT/{event.text[11:]}.txt", 'a', encoding='utf-8')
                    input_file.write(f'{event.user_id}\n')
                    input_file.close()

                else:
                    id_grup = str(get_wall_posts_id(event.text[11:]))
                    print(id_grup[0])
                    if id_grup[0] == '-':
                        input_file = open(f"BOT/{event.text[11:]}.txt", 'w', encoding='utf-8')
                        input_file.write(f'{event.user_id}\n')
                        input_file.close()

                        input_file_2 = open(f"BOT/group.txt", 'a', encoding='utf-8')
                        input_file_2.write(f'{event.text[11:]} {id_grup} 0\n')
                        input_file_2.close()

                        get_wall_posts(event.text[11:], id_grup)

                    else:
                        sender(event.user_id, f'Проверьте название группы')
                    print(event.user_id)
                sender(event.user_id, f'{event.text[11:]} {get_wall_posts_id(event.text[11:])}\n')

            if '/del' in event.text:  # Если написали заданную фраз
                try:
                    input_file = open(f"BOT/{event.text[5:]}.txt", 'r', encoding='utf-8')
                    user_id_list = input_file.readlines()
                    input_file.close()
                    print(user_id_list)
                    user_id_list.remove(f"{event.user_id}\n")
                    print(user_id_list)

                    input_file = open(f"BOT/{event.text[5:]}.txt", 'w', encoding='utf-8')
                    input_file.writelines(user_id_list)
                    input_file.close()
                    sender(event.user_id, f'я больше не буду присылать из {event.text[5:]}')
                except Exception:
                    print("лох")


            if '/new_xax_group' in event.text:  # Если написали заданную фраз
                print('new_group_xax')

                if os.path.exists(f"BOT/{event.text[15:]}.txt"):
                    print(f"Файл с именем {event.text[15:]} уже существует!")
                    input_file = open(f"BOT/{event.text[15:]}.txt", 'a', encoding='utf-8')
                    input_file.write(f'{event.user_id}\n')
                    input_file.close()

                else:
                    id_grup = str(get_wall_posts_id(event.text[15:]))
                    print(id_grup[0])
                    if id_grup[0] == '-':
                        input_file = open(f"BOT/{event.text[15:]}.txt", 'w', encoding='utf-8')
                        input_file.write(f'{event.user_id}\n')
                        input_file.close()

                        input_file_2 = open(f"BOT/group.txt", 'a', encoding='utf-8')
                        input_file_2.write(f'{event.text[15:]} {id_grup} 1\n')
                        input_file_2.close()

                        get_wall_posts(event.text[15:], id_grup)

                    else:
                        sender(event.user_id, f'Проверьте название группы')
                    print(event.user_id)
                sender(event.user_id, f'{event.text[15:]} {get_wall_posts_id(event.text[16:])}\n'
                                      f'Сообщение с 😃')

            if event.text == '/help':
                sender(event.user_id, f'/new_group group - новая группа, вместо group пишим имя группы \n\n'
                                      f'/del group - удалить группу (больше уведомления приходить не будут)(от группы group)\n\n'
                                      f'Подробности тут: https://vk.com/radio_engineering_urfu_bot?w=wall-206917464_3')


# schedule_loop(bot)
def schedule_loop2(bot):
    while True:
        f = open('BOT/group.txt', 'r', encoding='utf-8')
        while True:
            try:
                lin, mas, smaile = f.readline().split()
                smaile = int(smaile)
                get_wall_posts(lin, mas, smaile)
            except:
                break
        f.close()
        time.sleep(30)


Thread(target=schedule_loop, args=(bot,)).start()
Thread(target=schedule_loop2, args=(bot,)).start()