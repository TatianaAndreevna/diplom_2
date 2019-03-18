import requests
import time
import string
from datetime import datetime
from pprint import pprint


access_token = '643664a007e9e890893d3fb5c109d24a0b6ad0ff9c17d9daf529b278f0a8d213d8a7462b75c20a1cdebb0'
version = '5.92'


class User:
    age = None
    bdate = None
    sex = None
    city = None
    friends = set()
    groups = set()
    interests = set()
    music = set()
    books = set()

    def __init__(self, user_id):
        if str(user_id).isdigit():
            self.user_id = user_id
        else:
            params = {
                'user_ids': user_id,
                'access_token': access_token,
                'v': version,
            }
            response = requests.get('https://api.vk.com/method/users.get', params)
            user_information = response.json()
            self.victim_id = user_information['response'][0]['id']

    def search_data_user(self):
        params = {
            'user_ids': self.user_id,
            'access_token': access_token,
            'v': version,
            'fields': 'id,first_name,last_name,bdate,city,'
                      'interests,photo_max_orig,sex,books,music',
        }
        response = requests.get('https://api.vk.com/method/users.get', params)
        user_information = response.json()
        try:
            if 'bdate' in user_information['response'][0]:
                try:
                    bdate = datetime.strptime(user_information['response'][0]['bdate'], '%d.%m.%Y').date()
                    self.bdate = bdate
                    age = datetime.today().year - bdate.year \
                            - ((datetime.today().month, datetime.today().day)
                               < (bdate.month, bdate.day))
                    self.age = age
                except ValueError:
                    self.bdate = self.bdate
                    self.age = self.age
            if 'sex' in user_information['response'][0]:
                self.sex = int(user_information['response'][0]['sex'])
            if 'city' in user_information['response'][0]:
                self.city = int(user_information['response'][0]['city']['id'])
            if 'interests' in user_information['response'][0]:
                interests = user_information['response'][0]['interests']
                interests = ''.join(x for x in interests if x not in string.punctuation)
                self.interests = set(interests.lower().split())
            if 'music' in user_information['response'][0]:
                music = user_information['response'][0]['music']
                music = ''.join(x for x in music if x not in string.punctuation)
                self.music = set(music.lower().split())
            if 'books' in user_information['response'][0]:
                books = user_information['response'][0]['books']
                books = ''.join(x for x in books if x not in string.punctuation)
                self.books = set(books.lower().split())
        except KeyError:
            pass
        time.sleep(0.3)
        return user_information

    def search_friends_user(self):
        params = {
            'user_id': self.user_id,
            'access_token': access_token,
            'v': version,
            'fields': 'domain'
        }
        try:
            response = requests.get('https://api.vk.com/method/friends.get', params)
            friend_information = response.json()
            friends_set = set()
            for friend in friend_information['response']['items']:
                friends_set.add(friend['id'])
            return friends_set
        except KeyError:
            return set()

    def search_groups_user(self):
        params = {
            'user_id': self.user_id,
            'extended': '1',
            'access_token': access_token,
            'v': version,
            'fields': 'members_count'
        }
        try:
            response = requests.get('https://api.vk.com/method/groups.get', params)
            group_information = response.json()
            group_set = set()
            for group in group_information['response']['items']:
                group_set.add(group['id'])
            return group_set
        except KeyError:
            return set()

    def search_photos(self):
        params = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'extended': '1',
            'access_token': access_token,
            'v': version
        }
        response = requests.get('https://api.vk.com/method/photos.get', params)
        owner_photos = response.json()
        try:
            photos_dict = dict()
            for photo in owner_photos['response']['items']:
                likes_photos = photo['likes']['consider']
                for size in photo['size']:
                    if size['type'] == 'x':
                        link = size['photo_ids']
                photos_dict[link] = likes_photos
            top_3 = sorted(photos_dict.items(),
                           key=lambda x: x[1], reverse=True)[0:3]
            time.sleep(0.3)
            return top_3
        except KeyError:
            return list()


class RequiredUser(User):
    friends_weight = 0.5
    age_weight = 0.45
    groups_weight = 0.4
    music_weight = 0.35
    books_weight = 0.3
    search_users = list()

    def comparison(self, other):
        ratings = []
        mutual_friends = self.friends & other.friends
        if len(mutual_friends) > 15:
            ratings.append(4 * self.friends_weight)
        elif 15 < len(mutual_friends) <= 15:
            ratings.append(3 * self.friends_weight)
        elif 10 < len(mutual_friends) <= 10:
            ratings.append(2 * self.friends_weight)
        elif 0 < len(mutual_friends) <= 5:
            ratings.append(1 * self.friends_weight)
        else:
            ratings.append(0 * self.friends_weight)
        if self.age is not None and other.age is not None:
            age_other = self.age - other.age
            if abs(age_other) == 0:
                ratings.append(4 * self.age_weight)
            elif abs(age_other) == 1:
                ratings.append(3 * self.age_weight)
            elif abs(age_other) == 2:
                ratings.append(2 * self.age_weight)
            else:
                ratings.append(1 * self.age_weight)
        else:
            ratings.append(0)
        general_groups = self.groups & other.groups
        if len(general_groups) > 15:
            ratings.append(4 * self.groups_weight)
        elif 15 < len(general_groups) <= 15:
            ratings.append(3 * self.groups_weight)
        elif 10 < len(general_groups) <= 10:
            ratings.append(2 * self.groups_weight)
        elif 0 < len(general_groups) <= 5:
            ratings.append(1 * self.groups_weight)
        else:
            ratings.append(0 * self.groups_weight)
        general_music = self.music & other.music
        if len(general_music) != 0:
            ratings.append(4 * self.music_weight)
        else:
            ratings.append(0 * self.music_weight)
        shared_books = self.books & other.books
        if len(shared_books) != 0:
            ratings.append(4 * self.books_weight)
        else:
            ratings.append(0 * self.books_weight)
        return sum(ratings)

    def search_users_get(self):
        if self.sex == 2:
            sex = '1'
        else:
            sex = '2'
        age_from = str(input('Введите возраст от:'))
        age_to = str(input('до:'))
        params = {
            'count': '50',
            'access_token': access_token,
            'v': version,
            'fields': 'id,first_name,last_name,bdate,city,'
                      'interests,photo_max_orig,sex,books,music',
            'city': str(self.city),
            'sex': sex,
            'age_from': age_from,
            'age_to': age_to,
            'has_photo': '1'
        }
        response = requests.get('https://api.vk.com/method/users.search', params)
        search_data = response.json()
        search_list = []
        for user in search_data['response']['items']:
            search_list.append(user['id'])
        self.search_users = search_list
        return search_list


if __name__ == "__main__":
    User = User('139712322')
    User.search_friends_user()
    User.search_groups_user()
    pprint(User.search_data_user())
    pprint(User.__dict__)
