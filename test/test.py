import unittest
import string
from VKinder import top_10
from User.user import RequiredUser
# from schema import Schema, And, Use, SchemaError


class MyTest(unittest.TestCase):
    def test_top_10(self):
        required_user = RequiredUser('43782857')
        required_user.search_data_user()
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
        self.assertIsInstance(top_10(required_user)[0], dict)

    # top10_structure = Schema({
    #     '_id': And(Use(str)),
    #     'photos': And(Use(list)),
    #     'user_id': And(Use(int)),
    #     'user_page': And(Use(str))
    # })
    # 
    # def check(top10_structure, top_10):
    #     try:
    #         top10_structure.validate(top_10)
    #         return True
    #     except SchemaError:
    #         return False
    # 
    # print(check(top10_structure, top_10))


if __name__ == '__main__':
    unittest.main()
