import datetime
import vk
import time
import json

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

# ищем пару по критериям
def get_couple():
    user = get_user()
    couple = []

    if user['sex'] == 1:  # определить какой у пользователя пол
        sex = 2
    else:
        sex = 1

    try:  # проверка в правильном ли формате указана дата рождения и определение сколько пользователю лет
        age_user = str((datetime.datetime.today() - datetime.datetime.strptime(user['bdate'], '%d.%m.%Y')) / 365)[:2]  # сколько пользователю лет
    except:
        bdate = input('У вас в профиле не верно указана или вообще не указана дата рождения, пожалуйста введите ее в формате ДД.ММ.ГГ: ')
        user['bdate'] = bdate
        age_user = str((datetime.datetime.today() - datetime.datetime.strptime(user['bdate'], '%d.%m.%Y')) / 365)[:2]  # сколько пользователю лет

    users = api.users.search(count=600, sex=sex, city=user['city']['id'],fields='bdate,sex,city,domain,relation')  # ищем подходящих людей count(кол-во), sex(пол), сity(город), bdate(день рождение), domain(короткие адрес)
    for people in users['items']:
        if not people['is_closed']:  # проверка что страница не закрыта
            try:
                age_people = str((datetime.datetime.today() - datetime.datetime.strptime(people['bdate'], '%d.%m.%Y')) / 365)[:2]  # сколько лет искомому человеку
                if 6 > int(age_user) - int(age_people) > -6:  # проверка по возрасту (+- 6 лет)
                    if people['relation'] != 4 and people['relation'] != 8 and people['relation'] != 3:  # проверка на семейное положение (не женат/замужем, не помолвлен/помолвлена, не в гражданском браке)
                        couple.append(people)
            except:
                pass
    return couple[:10]


# Получаем ссылку на пользователя и топ 3 фотографии
def get_url_photo():
    users = get_couple()
    unsorted_like = [] # список из 10 людей, где у каждого: кол-во лайков, ссылка, топ 3 фотографии
    sorted_like = []  # конечный, отсортированный результат
    sum_like_list = [] # список из суммых лайков 3ех фотографий

    for user in users:
        top3_like = []  # лайки фоток по убыванию
        user_photo = api.photos.get(owner_id=user['id'], album_id='profile',extended=1)  # получаем фотки со страницы пользователя
        time.sleep(1.5)
        for photo in user_photo['items']:
            top3_like.append(photo['likes']['count'])  # добавляем лайки фоток
        top3_like.sort(reverse=True)  # сортировка лайков по убыванию
        top3_like = top3_like[:3]
        sum_like_list.append(sum(top3_like)) # список из суммых лайков 3ех фотографий

        top_dict = {}  # id: ссылка на пользователя, photos: [ссылки на топ 3 фотографии]
        url_list = []  # список для хранения ссылок на фотки

        for photo in user_photo['items']:
            if photo['likes']['count'] in top3_like:  # если фото в топ 3 лайков, то добавляем ссылку на фото
                url_list.append(photo['sizes'][0]['url'])
        top_dict['sum_like'] = sum(top3_like) # добавляем суммарное кол-во лайков на трех фотографиях
        top_dict['id'] = 'https://vk.com/' + user['domain']  # добавляем ссылку на пользователя
        top_dict['photos'] = url_list[:3]  # добавляем 3 ссылки на фотографии
        unsorted_like.append(top_dict) # список из 10 людей, где у каждого: кол-во лайков, ссылка, топ 3 фотографии

    sum_like_list.sort(reverse=True)  # сортируем по убыванию
    while sum_like_list:  # цикл который сортирует список пар чтобы сначала шли с самым большим количеством лайков
        for account in unsorted_like:
            if len(sum_like_list) == 0:  # если поля лайков нет то завершить цикл
                break
            if account['sum_like'] == sum_like_list[0]:  # если поле лайков у человека в списке топ лайков
                sorted_like.append(account)  # то добавляем в список
                del (sum_like_list[0])  # удаляем поле лайков у человека
    # for user in sorted_like:
    #     del user['sum_like'] # удалить поле лайков при выводе
    return sorted_like


# сохранить данные в файл JSON
def save_to_file(file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(func, file, ensure_ascii=False, indent=2)


# сохранить данные в БД MongoDB
def save_to_mongodb():
    client = MongoClient()
    my_db = client['vk_api']  # создать/обратится к бд
    couple = my_db['couple']  # создать/обратится к коллекции
    # my_db.couple.drop()
    for people in func:
        couple.insert_one(people)
    print(list(couple.find()))  # проверка


finish_time = datetime.datetime.now()
run_time = finish_time - start_time
print('Программа закончила работу')
print(f'Программа выполнялась {str(run_time)[:9]} секунды')


if __name__ == '__main__':
    save_to_file('couple.json')
    # save_to_mongodb()