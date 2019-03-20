import string
from User.user import User, RequiredUser
from db.db import DataBase
from pprint import pprint


def top_10(required_user):
    db = DataBase()
    search_users = required_user.search_users_get()
    search_users_dict = dict()
    search_photo_users = dict()
    for user in search_users:
        if db.check_users(user):
            following_user = User(str(user))
            following_user.search_data_user()
            following_user.search_friends_user()
            following_user.search_groups_user()
            search_users_dict[user] = required_user.comparison(following_user)
            search_photo_users[user] = following_user.search_photos()
            print('-')
        else:
            continue
    search_users_dict = sorted(search_users_dict.items(),
                               key=lambda x: x[1], reverse=True)

    data_base = list()
    for user in search_users_dict[0:10]:
        dict_top_10 = dict()
        user_photos = search_photo_users[user[0]]
        list_photos = list()
        for photo in user_photos:
            list_photos.append(photo[0])
        dict_top_10['user_id'] = user[0]
        dict_top_10['user_page'] = 'https:/vk.com/id' + str(user[0])
        dict_top_10['user_photos'] = list_photos
        data_base.append(dict_top_10)
    db.add_users(data_base)
    return data_base


# Поиск людей, подходящих под условия, на основании информации о конкретном пользователе из ВК.
# Вывод популярных фото с аватара подошедших людей.
if __name__ == "__main__":
    required_user = RequiredUser('43782857')
    required_user.search_data_user()
# Если у пользователя не заполнены любимые книги, музыка и интересы, то можно ввести их вручную
    if len(required_user.books) == 0:
        books = input('Введите ваши любимые книги:')
        books = ''.join(x for x in books if x not in string.punctuation)
        required_user.books = set(books.lower().split())
    if len(required_user.music) == 0:
        music = input('Введите вашу любимую музыку:')
        music = ''.join(x for x in music if x not in string.punctuation)
        required_user.interests = set(music.lower().split())
    if len(required_user.interests) == 0:
        interests = input('Введите ваши интересы:')
        interests = ''.join(x for x in interests if x not in string.punctuation)
        required_user.interests = set(interests.lower().split())
    required_user.search_friends_user()
    required_user.search_groups_user()
    top_10_users = top_10(required_user)
    pprint(top_10_users)
