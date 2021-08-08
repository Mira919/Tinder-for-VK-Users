import datetime
import vk
import time

start_time = datetime.datetime.now()
print(f'Программа начала свою работу')

access_token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
v = '5.103'

session = vk.Session(access_token)
api = vk.API(session, v=v)

user_id = input('Введите ваш ID вконтакте (например 169989152): ')

# получаем страницу пользователя, которому надо найти пару
def get_user():
    try:  # проверка что профиль не закрыт, если закрыт то программа завершается
        user = api.users.get(user_ids=user_id, fields='bdate,sex,city,interests') # получаем информацию пользователя
        groups = api.users.getSubscriptions(user_id=user_id, extended=1) # получаем группы пользователя
        time.sleep(1.5)
        for i in user:
            i['groups'] = groups
    except:
        print('Извините, ваш профиль закрыт!')
        exit(0)

    if 'city' not in user[0]:  # проверка указан ли на странице город, если не указан то программа завершается
        print('У вас на странице не задан город! Пожалуйста укажите его в своих настройках ВКонтакте.')
        exit(0)

    return user[0]

finish_time = datetime.datetime.now()
run_time = finish_time - start_time
print('Программа закончила работу')
print(f'Программа выполнялась {str(run_time)[:9]} секунды')