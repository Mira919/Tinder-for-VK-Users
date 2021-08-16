import unittest
import main


class TestVKAPIProgram(unittest.TestCase):

    # проверка получения имени пользователя (в данном случае 169989152 = Мирослав)
    def test_get_user(self):
        user = main.get_user()
        self.assertEqual(user['first_name'], 'Miroslav')
        print('Проверка получения имени пользователя выполнена')

    # проверка получения 10 пользователей, подходящих под критерии
    def test_get_couple(self):
        users = main.get_couple()
        self.assertEqual(len(users), 10)
        print('Проверка получения 10 пользователей, подходящих под критерии выполнена')