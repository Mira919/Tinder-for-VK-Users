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

    # проверка получения людей противоположного пола (в данном случае нужно получать девушек для id 169989152)
    def test_check_sex(self):
        users = main.get_couple()
        for user in users:
            self.assertNotEqual(user['sex'], 2)
        print('Проверка получения людей противоположного пола выполнена')

    # проверка получения людей по подходящему городу (в данном случае для Перми для id 169989152)
    def test_check_city(self):
        users = main.get_couple()
        for user in users:
            self.assertNotEqual(user['city'], 'Perm')
        print('Проверка получения людей по подходящему городу выполнена')


if __name__ == '__main__':
    unittest.main()