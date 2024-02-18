import urllib.request
import selenium.webdriver.common
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class ReplaceContainer:
    def __init__(self, old, new):
        self.oldValue = old
        self.newValue = new


def get_chapter(chapter_link):
    source_domain = 'https://www.ddyueshu.com'
    html_page_charset = 'gbk'  # из charset в meta теге начала html страницы

    src = str(urllib.request.urlopen(source_domain + chapter_link).read().decode(html_page_charset))
    start_index = 0
    ch_begin = '<div id="content">'  # начало текста главы
    ch_end = '<script>chaptererror();</script>'  # конец текста главы
    link_begin = '&rarr; <a href="'  # начало ссылки следующей главы
    link_end = '">下一章</a>'  # конец ссылки следующей главы
    text = str(src[src.find(ch_begin, start_index) + len(ch_begin):src.find(ch_end,
        src.find(ch_begin, start_index) + len(ch_begin))])
    chapter_link = str(src[src.find(link_begin, start_index) + len(link_begin):src.find(link_end, src.find(link_begin,
        start_index) + len(link_begin))])
    replaces = [
        ReplaceContainer('<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', '\n'),
        ReplaceContainer('<br /><br />', '')
    ]
    text = replace_by_templates(replaces, text)

    return text, chapter_link


def replace_by_templates(replaces, text):
    for oneReplace in replaces:
        text = text.replace(oneReplace.oldValue, oneReplace.newValue)
    return text


if __name__ == '__main__':
    src_chapter_link = '/1_1801/1956010.html'
    source_chapter_number = 1134
    result_replaces = [
        ReplaceContainer('\n', '\n\n')
    ]
    chapter_names = ['Холодный Камень Преисподней',
'Божественное вооружение возвращенное городом',
'Трое сильнейших добрались',
'Собственные правила',
'Я лично посещу глав сект!',
'Мин Есюэ готовится выйти?',
'Распоряжения',
'Сообщения области Возвышенных Земель Нижней Провинции',
'Прибытие в особняк городского лорда древнего города Цинхуа',
'Дар обучения',
'Формация Заточения Богов',
'Раздавлены',
'Ты не сможешь',
'Сердце Дао разбито, проявление истинной натуры',
'Превзошедшая все мыслимые пределы чистая сила физического тела',
'Человек, который с самого начала должен был умереть',
'Путь убийств. Сминая все, словно бамбук (1)',
'Путь убийств. Сминая все, словно бамбук (2)',
'Девять Великих Солнц, Девять Великих Лун',
'Некогда Первый',
'Бронзовый Храм Бессмертных',
'Особняк городского лорда в древнем городе Цинхуа перевернут',
'Перемены в области Возвышенных Земель Нижней Провинции',
'Секта Возвышенных Земель появляется, противостояние сильнейших',
'Вершина Горы Десяти Тысяч Мечей. Вызов на вершине горы',
'Неукротимый',
'Десять Мечей Возвращаются к Началу',
'Простое лезвие разрушает броню',
'Формация Десяти Техник Меча',
'Теперь твой черед'    ]

    driver = selenium.webdriver.Chrome()
    driver.get("https://www.deepl.com/ru/translator#zh/ru/")

    i = 0
    for ch_name in chapter_names:
        print('Глава ' + str(source_chapter_number + 69) + ' ' + ch_name + ' ' + src_chapter_link + ' ' + str(source_chapter_number))
        chapter_source, next_chapter_link = get_chapter(src_chapter_link)

        translate_number = source_chapter_number + 69  # номер главы на русском
        src_chapter_link = next_chapter_link           # ссылка на след главу
        source_chapter_number += 1                     # номер для следующей главы

        elem = driver.find_element(By.CLASS_NAME, 'relative flex-1 rounded-inherit')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'A')
        elem.send_keys(Keys.DELETE)
        elem.send_keys(chapter_source)
        time.sleep(23)
        elem = driver.find_element(By.CLASS_NAME, 'lmt__target_textarea')

        translate = elem.get_attribute("value")        # готовый перевод главы

        chapter = 'Глава ' + str(translate_number) + ' ' + ch_name + '\n' + translate + '\n'
        chapter = replace_by_templates(result_replaces, chapter)
        # запись в файл
        f = open('chapters.txt', 'a', encoding="utf-8")
        f.write(chapter)
        f.close()
        i = 1

    driver.quit()
