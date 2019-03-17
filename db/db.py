from pymongo import MongoClient


class DataBase:
    def __init__(self, host='localhost', port=27017,
                 username=None, password=None):
        client = MongoClient(host=host, port=port,
                             username=username, password=password)
        users_db = client.vk_users
        self.db = users_db

    def add_users(self, data):
        list_users = self.db.list_users
        list_users.insert_many(data)

    def check_users(self, value):
        results = list(self.db.list_users.find({'user_id': value}))
        return  len(results) == 0