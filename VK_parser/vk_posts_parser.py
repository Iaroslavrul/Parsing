import ftplib
import json
import logging
import os
import re
import time
from datetime import datetime
import autotitle
import requests

LOG_FOLDER = "logs\\"
logging.basicConfig(filename=LOG_FOLDER + str(datetime.now()).replace(':', '_') + '.txt',
                    level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s\t:  %(message)s',
                    datefmt='%d.%m.%Y-%H:%M:%S')

cities = {
    "Russia": ['Москва', 'СПБ', "Новосибирск", "Екатеринбург", "Нижний Новгород", "Казань", "Челябинск", "Омск",
               "Самара", "Ростов-на-Дону", "Уфа", "Красноярск", "Воронеж", "Пермь", "Волгоград", "Краснодар",
               "Саратов",
               "Тюмень", "Тольятти", "Ижевск", "Барнаул", "Ульяновск", "Иркутск", "Хабаровск", "Ярославль",
               "Владивосток", "Махачкала", "Томск", "Оренбург", "Кемерово", "Новокузнецк", "Рязань", "Астрахань",
               "Набережные Челны", "Пенза", "Киров", "Липецк", "Чебоксары", "Балашиха", "Калининград", "Тула",
               "Курск",
               "Сочи", "Ставрополь", "Тверь", "Магнитогорск", "Брянск", "Иваново", "Белгород", "Сургут", "Чита",
               "Нижний Тагил", "Архангельск", "Калуга", "Смоленск", "Волжский", "Якутск", "Саранск", "Череповец",
               "Курган", "Вологда", "Орёл", "Владикавказ", "Подольск", "Тамбов", "Мурманск", "Петрозаводск",
               "Нижневартовск", "Стерлитамак", "Кострома", "Новороссийск", "Химки", "Таганрог", "Сыктывкар",
               "Нижнекамск", "Нальчик", "Дзержинск", "Братск", "Орск", "Благовещенск", "Энгельс", "Ангарск",
               "Великий Новгород", "Мытищи", "Псков", "Люберцы", "Бийск", "Прокопьевск", "Армавир"],
    "Belarus": ["Минск", "Гомель", "Могилев", "Витебск", "Гродно", "Брест", "Бобруйск", "Барановичи", "Борисов",
                "Пинск"],
    "Kazakhstan": ["Алма-Ата", "Нур-Султан", "Шымкент", "Актобе", "Караганда", "Тараз", "Павлодар",
                   "Усть-Каменогорск", "Атырау", "Костанай", "Петропавловск", "Туркестан"],
    "Ukraine": ["Киев", 'Харьков', 'Одесса', 'Днепр', 'Запорожье', 'Львов', 'Кривой Рог', 'Николаев', 'Мариуполь',
                'Винница', 'Херсон', 'Полтава', 'Чернигов', 'Черкассы', 'Хмельницкий', 'Черновцы', 'Житомир', 'Сумы',
                'Ровно', 'Ивано-Франковск', 'Каменское', 'Кропивницкий', 'Тернополь', 'Кременчуг', 'Луцк',
                'Белая Церковь', 'Краматорск', 'Мелитополь', 'Ужгород', 'Славянск', 'Никополь', 'Бердянск', 'Бровары',
                'Павлоград', "Северодонецк"]
}

current_date = datetime.today()


def take_groups(reg_request):
    token = 'ee35da8bcba75879183337b8faghtghgtnfhykf13781cb16d32c6f08f0e633d93295e294924'
    version = 5.103
    count = 20
    all_groups = []
    answer = requests.get('https://api.vk.com/method/groups.search',
                          params={
                              'access_token': token,
                              'v': version,
                              'q': reg_request,
                              'count': count,
                          })
    groups_list = answer.json()['response']['items']
    for group in groups_list:
        try:
            short_name = group['screen_name']
            all_groups.append(short_name)
        except IndexError:
            print("")
    time.sleep(2)
    return all_groups


def take_posts(domain):
    token = '4229372442293724422937246b4244e4f544229422937241fe203c832d569a0e82d6100'
    version = 5.103
    count = 50
    all_posts = []
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': token,
                                'v': version,
                                'domain': domain,
                                'count': count,
                            })
    data = ''
    try:
        data = response.json()['response']['items']
    except KeyError:
        print("")
    all_posts.extend(data)
    time.sleep(2)
    return all_posts


def get_data(groups, city, country):
    arr = []
    for group in groups:
        all_posts = take_posts(group)
        for post in all_posts:
            all_text = post['text']
            url = 'https://vk.com/wall{0}_{1}'.format(post['from_id'], post['id'])
            url_to_list = list(url)
            date = datetime.utcfromtimestamp(post['date'])
            diff_day = current_date - date
            day1 = re.sub(r'^\d{1,2}:.*', '0', str(diff_day))
            day2 = re.sub(r'\s+.*', '', str(day1))
            if int(day2) < 15 and "-" in url_to_list:
                date_to_json = datetime.utcfromtimestamp(post['date']).strftime('%Y-%m-%d %H:%M:%S')
                autoTitleFromDesc = ''
                try:
                    autoTitleFromDesc = get_auto_title.autotitle(all_text)
                except UnicodeEncodeError:
                    print("UnicodeEncodeError")
                vac = {
                    "url": url,
                    "AutoTitleFromDesc": autoTitleFromDesc,
                    "date": date_to_json,
                    "desc": all_text,
                    "region": city,
                    "country": country,
                    "group": group,
                }
            else:
                break
    return arr


def json_writer(*arr_vacancies):
    for arr in arr_vacancies:
        with open(os.path.join('json', arr[0]["name"] + ".json"), 'w', encoding='utf-8') as f:
            json.dump({"data": arr}, f, indent=2, ensure_ascii=False)


def dump_to_ftp():
    ftp_connection = ftplib.FTP("silarc.jest.com", "cont", "jvdfkdv")
    for folder, _, files in os.walk('json'):
        for file in files:
            file_dir = os.path.join(folder, file)
            with open(file_dir, 'rb') as file:
                send = ftp_connection.storbinary("STOR " + os.path.basename(file_dir), file)


def clean_folder(path='json'):
    for folder, _, files in list(os.walk(path)):
        for file in files:
            file_dir = os.path.join(folder, file)
            os.remove(file_dir)


def main():
    arr_multi = [{"name": "Multi_VK"}]
    arr_ukraine = [{"name": "Ukraine_VK"}]
    for country in cities.keys():
        for city in cities[country]:
            groups = take_groups("Работа " + city)
            if country != "Ukraine":
                multi = get_data(groups, city, country)
                arr_multi.extend(multi)
            else:
                ukr = get_data(groups, city, country)
                arr_ukraine.extend(ukr)
    json_writer(arr_multi, arr_ukraine)


if __name__ == '__main__':
    logging.info('Start')
    clean_folder()
    main()
    dump_to_ftp()
    logging.info('Finish')
