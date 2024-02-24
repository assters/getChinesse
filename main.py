import re
import urllib.request
import selenium.webdriver.common
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time



class ReplaceContainer:
    def __init__(self, old, new):
        self.oldValue = old
        self.newValue = new

def replace_by_templates(replaces, text):
        for oneReplace in replaces:
            if oneReplace.oldValue == 'Маленький Бастард':
                i2 = 0
            text = text.replace(oneReplace.oldValue, oneReplace.newValue)
        return text

def multiple_replace(string, rep_dict):
    pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict,key=len,reverse=True)]), flags=re.DOTALL)
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)


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

def getTranslate_ddyueshu_com():
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
        #####
        #chapter_source='萧凡杀了金樽太君，以及属于金樽太君的一众广寒圣地就算了，毕竟无力阻止，再者，他们心头其实也早都希望金樽太君去死了，但结果现在萧凡连原本属于广寒圣地的魔国后裔都要抢走，那这个就没法忍了。'
        #next_chapter_link='sss'
        #####
        translate_number = source_chapter_number + 69  # номер главы на русском
        src_chapter_link = next_chapter_link           # ссылка на след главу
        source_chapter_number += 1                     # номер для следующей главы

        elem = driver.find_element(By.CLASS_NAME, 'focus-visible-disabled-container')
        #elem.find_element(By.CLASS_NAME, 'rounded-bl-inherit')
        elem.click()
        # clear field
        elem.send_keys('1')
        elem.send_keys(Keys.CONTROL + 'A')
        elem.send_keys(Keys.DELETE)

        elem.send_keys(chapter_source)
        time.sleep(17)

        # GET TRANSLATED TEXT
        elem = driver.find_elements(By.CLASS_NAME, 'focus-visible-disabled-container')
        translate = elem[1].text
        #elem = driver.find_element(By.CLASS_NAME, 'sentence_highlight')
        #translate = elem.get_attribute("innerHTML")

        chapter = 'Глава ' + str(translate_number) + ' ' + ch_name + '\n' + translate + '\n'
        chapter = replace_by_templates(result_replaces, chapter)
        # запись в файл
        f = open('chapters.txt', 'a', encoding="utf-8")
        f.write(chapter)
        f.close()
        i = 1

    driver.quit()



def replaceByDictionary():
    # открыть файл
    f = open('chapters.txt', 'r', encoding="utf-8")
    text = f.read()
    f.close()

    # замена по регуляркам
    # (" )([А-Я])        \1- \2
    regex = re.compile('(?P<name>(" ))(?P<name2>([А-Я]))')
    text1 = regex.sub('\g<name>- \g<name2>', text)

    # замена текста
    replaces = [
        ReplaceContainer('\nмаленькая черепашка', '\nМаленькая черепашка'),
        ReplaceContainer('Сяо Фаном', 'Сяо Фанем'),
        ReplaceContainer('Сэр', 'Господин'),
        ReplaceContainer('Красном особняке', 'Красном Доме'),
        ReplaceContainer('Ленг Цюян', 'Лэн Цюянь'),
        ReplaceContainer('Лэн Цюянья', 'Лэн Цюянь'),
        ReplaceContainer('Лэн Цюяньем', 'Лэн Цюянь'),
        ReplaceContainer('Лэн Цюяне', 'Лэн Цюянь'),
        ReplaceContainer('сэр', 'господин'),
        ReplaceContainer('Государь', 'Глава секты'),
        ReplaceContainer('герцог', 'господин'),
        ReplaceContainer('Дворцом Божественной Девы', 'Дворцом Богини'),
        ReplaceContainer('Дворца Богинь', 'Дворца Богини'),
        ReplaceContainer('Божественный Женский Дворец', 'Дворец Богини'),
        ReplaceContainer('Сайлент Хилла', 'Хребта Молчания'),
        ReplaceContainer('Сайлент Хилл', 'Хребет Молчания'),
        ReplaceContainer('Ка-чинг', 'Щелк'),
        ReplaceContainer('Императором Демонов', 'Дьявольским Императором'),
        ReplaceContainer('Император Дьяволов', 'Дьявольский Император'),
        ReplaceContainer('Королевство Дьяволов', 'Дьявольская страна'),
        ReplaceContainer('Ниншань', 'Нин Шуан'),
        ReplaceContainer('ниншен', 'Нин Шуан'),
        ReplaceContainer('Ниншаня', 'Нин Шуан'),
        ReplaceContainer('император демонов', 'Дьявольский Император'),
        ReplaceContainer('императором дьявола', 'Дьявольским Императором'),
        ReplaceContainer('Нижнему Государству Цин Юнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Центральное Имперское царство', 'Мир Срединного Императора'),
        ReplaceContainer('старик в штатском', 'старик в белом'),
        ReplaceContainer('"Ваше превосходительство ', '"Старший'),
        ReplaceContainer('Ди Нану', 'Ди Наню'),
        ReplaceContainer('Ван Руо Лю', 'Ван Жолю'),
        ReplaceContainer('Ван Рулю', 'Ван Жолю'),
        ReplaceContainer('Ван Жуйюнь', 'Ван Жуюнь'),
        ReplaceContainer('лорд', 'господин'),
        ReplaceContainer('Ниншанг', 'Нин Шуан'),
        ReplaceContainer('Ниншана', 'Нин Шуан'),
        ReplaceContainer('Лэн Цю Янем', 'Лэн Цюянь'),
        ReplaceContainer('Императора Демонов', 'Дьявольский Император'),
        ReplaceContainer('Герцог', 'Господин'),
        ReplaceContainer('Торговой Палаты', 'торговой компании'),
        ReplaceContainer('Клан Сюаньтянь', 'Секта Северного Неба'),
        ReplaceContainer('клан Сюаньтянь', 'секта Северного Неба'),
        ReplaceContainer('Минг Ю', 'Мин Юй'),
        ReplaceContainer('слова упали', 'слова прозвучали'),
        ReplaceContainer('минутного молчания', 'недолгого молчания'),
        ReplaceContainer('Неплохо', 'Да'),
        ReplaceContainer('Пика Нездешнего Мира', 'Туманного Пика'),
        ReplaceContainer('Лэн Цюяня', 'Лэн Цюянь'),
        ReplaceContainer('Ти Юй', 'Те Юй'),
        ReplaceContainer('Ти Юя', 'Те Юя'),
        ReplaceContainer('Галстука Юй', 'Те Юя'),
        ReplaceContainer('Тие Ю', 'Те Юй'),
        ReplaceContainer('маленький Вангэ', 'маленькая черепашка'),
        ReplaceContainer('Маленький Кинг Бастер', 'маленькая черепашка'),
        ReplaceContainer('Маленький Королевский Бустер', 'маленькая черепашка'),
        ReplaceContainer('Маленький Король Бастер', 'маленькая черепашка'),
        ReplaceContainer('Маленький Король-Бустер', 'маленькая черепашка'),
        ReplaceContainer('Маленький Король Баба', 'маленькая черепашка'),
        ReplaceContainer('Маленький Королевский Ублюдок', 'маленькая черепашка'),
        ReplaceContainer('меч Северного Неба', 'Меч Северного Неба'),
        ReplaceContainer('Маленького Ван Ба', 'маленькую черепашку'),
        ReplaceContainer('маленького ублюдка', 'маленькую черепашку'),
        ReplaceContainer('Маленького Короля', 'маленькой черепашки'),
        ReplaceContainer('Маленьком Королевском Ублюдке', 'маленькой черепашке'),
        ReplaceContainer('Маленькая черепашка', 'маленькая черепашка'),
        ReplaceContainer('........', '...'),
        ReplaceContainer('......', '...'),
        ReplaceContainer('.....', '...'),
        ReplaceContainer('Маленькой черепашки Ублюдка', 'маленькую черепашку'),
        ReplaceContainer('Маленькой черепашки Бастера', 'маленькой черепашки'),
        ReplaceContainer('Маленький Король VIII', 'маленькая черепашка'),
        ReplaceContainer('Маленькой черепашки', 'маленькой черепашки'),
        ReplaceContainer('Маленьким Королем', 'маленькой черепашкой'),
        ReplaceContainer('Маленький Король', 'маленькая черепашка'),
        ReplaceContainer('Сотни Благодарностей', 'Байсе'),
        ReplaceContainer('Пик Нетерпеливого Мира', 'Туманный Пик'),
        ReplaceContainer('Сто Се Ши', 'Байсе'),
        ReplaceContainer('Бай Се', 'Байсе'),
        ReplaceContainer('Мо Синя', 'Мо Сяо'),
        ReplaceContainer('Ленг Цю Янь', 'Лэн Цюянь'),
        ReplaceContainer('Северного Неба Цзянь', 'Меч Северного Неба'),
        ReplaceContainer('"Клик!"', '"Щелк"'),
        ReplaceContainer('Сто Се', 'Байсе'),
        ReplaceContainer('фея Цзыруо', 'Фея Цзы Жо'),
        ReplaceContainer('Небесного Ранга', 'Рейтинга Небес'),
        ReplaceContainer('Последний Клинок Демона', 'Последний Дьявольский Клинок'),
        ReplaceContainer('злодеев Рейтинга Небес', 'свирепых Рейтинга Небес'),
        ReplaceContainer('Королевством Дьявола', 'Дьявольской страной'),
        ReplaceContainer('Королевству Дьявола', 'Дьявольской стране'),
        ReplaceContainer('Лэн Цю Янь', 'Лэн Цюянь'),
        ReplaceContainer('маленький Ван Ба', 'маленькая черепашка'),
        ReplaceContainer('Незримый Пик', 'Туманный Пик'),
        ReplaceContainer('Красный особняк', 'Красный Дом'),
        ReplaceContainer('Великим Драконьим Деревом Луо', 'Великим Драконьим Деревом Ло'),
        ReplaceContainer('Центральном Императорском царстве', 'Мире Срединного Императора'),
        ReplaceContainer('Драконье Дерево Да Ло', 'Великое Драконье Дерево Ло'),
        ReplaceContainer('Драконье Дерево Да Луо', 'Великое Драконье Дерево Ло'),
        ReplaceContainer('Верховного Мастера Ву Чжэня', 'Верховного Мастера У Чжэня'),
        ReplaceContainer('Центрального Императорского царства', 'Мира Срединного Императора'),
        ReplaceContainer('".', '."'),
        ReplaceContainer('Сотни Се', 'Байсе'),
        ReplaceContainer('Королевства Демонов', 'Дьявольской страны'),
        ReplaceContainer('Пик Нездешнего Мира', 'Туманный Пик'),
        ReplaceContainer('Торговая Палата', 'торговая компания'),
        ReplaceContainer('Боевая Секта', 'секта Войны'),
        ReplaceContainer('! "', '!"'),
        ReplaceContainer('машина для убийства', 'намерение убийства'),
        ReplaceContainer('Последний Клинок Дьявола', 'Последний Дьявольский Клинок'),
        ReplaceContainer('Клинок Окончательного Дьявола', 'Последний Дьявольский Клинок'),
        ReplaceContainer('Пфф', 'Пуф'),
        ReplaceContainer('Сюань Тянь', 'Северного Неба'),
        ReplaceContainer('нижнего уровня префектуры Цин Юнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('префектуре Нижний Цин Юнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('нижней префектуры Цин Юнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('префектуру Нижний Цин Юнь', 'область Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('государство Нижний Цин Юнь', 'область Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('государстве Нижний Цин Юнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('префектурой Нижний Цин Юнь', 'областью Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('префектуры Нижний Цин Юнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Нижней Префектуре Цин Юнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('нижнем регионе Цин Юнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Линь Бацзюнь', 'Линь Поцзюнь'),
        ReplaceContainer('регионе Нижний Цин Юнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Нижней префектуре Цин Юнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Королевства Дьявола', 'Дьявольской страны'),
        ReplaceContainer('Царства Демонов', 'Дьявольской страны'),
        ReplaceContainer('царство демонов', 'Дьявольская страна'),
        ReplaceContainer('царства демонов', 'Дьявольской страны'),
        ReplaceContainer('государству Нижний Цин Юнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('государства Нижний Цин Юнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('префектуры Нижнего Цин Юня', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Цин Юнь Ха Чжоу', 'области Возвышенных Земель Нижней Провинции '),
        ReplaceContainer('потомков дьявола', 'потомков Дьявольской страны'),
        ReplaceContainer('Святой Земли Даян', 'Превозносимой Святой Земли'),
        ReplaceContainer('префектуру Нижнего Цин Юня', 'область Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Мин Исюэ', 'Мин Есюэ'),
        ReplaceContainer('святая госпожа Минг Ю', 'Святая Дочь Мин Юй'),
        ReplaceContainer('Великий Метод Сердца Самореализации', 'Великая Техника Невозмутимости Сердца'),
        ReplaceContainer('Мудрец Минг Ю', 'Святая Дочь Мин Юй'),
        ReplaceContainer('Туо Тре', 'Тоба'),
        ReplaceContainer('Секта Сюаньтянь', 'секта Северного Неба'),
        ReplaceContainer('префектуре Нижнего Цин Юня', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('префектуре Нижняя Цин Юнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Дворец Божественной Девы', 'Дворец Богини'),
        ReplaceContainer('Нижнюю Префектуру Цин Юнь', 'область Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Сяо Фану', 'Сяо Фаню'),
        ReplaceContainer('Усовершенствования Крови', 'Очищения Крови'),
        ReplaceContainer('Янь Цзы Пин', 'Янь Цзыпин'),
        ReplaceContainer('Сяо Фана', 'Сяо Фаня'),
        ReplaceContainer('префектура Нижний Цин Юнь', 'область Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('нижний штат Цин Юнь', 'область Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('нижнем регионе Цинъюнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('весь область', 'всю область'),
        ReplaceContainer('Туоба', 'Тоба'),
        ReplaceContainer('Тоба Лююнем', 'Тоба Лю Юнем'),
        ReplaceContainer('Тоба Лююнь', 'Тоба Лю Юнь'),
        ReplaceContainer('Центральном Имперском царстве', 'Мире Срединного Императора'),
        ReplaceContainer('Ван Ланьтянем', 'Вань Лантянем'),
        ReplaceContainer('Окончательный Клинок Дьявола', 'Последний Дьявольский Клинок'),
        ReplaceContainer('последнего дьявольского клинка', 'Последнего Дьявольского Клинка'),
        ReplaceContainer('держав', 'сил'),
        ReplaceContainer('низким голосом', 'тихим голосом'),
        ReplaceContainer('Священная земля', 'Святая Земля'),
        ReplaceContainer('Гуан Хань', 'Распростертого Холода'),
        ReplaceContainer('Сун Синьшэн', 'Сун Синьшуан'),
        ReplaceContainer('Боевой сектой', 'сектой Войны'),
        ReplaceContainer('Священной Земле', 'Святой Земле'),
        ReplaceContainer('Священной Земли', 'Святой Земли'),
        ReplaceContainer('Жадный Волк', 'Жадные Волки'),
        ReplaceContainer('хрипловатым', 'сдавленным'),
        ReplaceContainer('Вожделенный Волк', 'Жадные Волки'),
        ReplaceContainer('Оставшийся Теневой Камень', 'камень памяти'),
        ReplaceContainer('Нин Шуана', 'Нин Шуан'),
        ReplaceContainer('Оставшихся Теневых Камня', 'камня памяти'),
        ReplaceContainer('Камень Долголетия Небесного Воробья', 'Камень Долголетия Небесной Птицы'),
        ReplaceContainer('Тоба Лююня', 'Тоба Лю Юня'),
        ReplaceContainer('Нин Шуаном', 'Нин Шуан'),
        ReplaceContainer('Wu Zong', 'Клан Сражения'),
        ReplaceContainer('War Zong', 'Клан ВОйны'),
        ReplaceContainer('префектуру Нижний Цин Юнь', 'область Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('легкомысленная девушка', 'простая девушка'),
        ReplaceContainer('ветреная дева', 'простая девушка'),
        ReplaceContainer('светлая дева', 'простая девушка'),
        ReplaceContainer('Сяо Фаном', 'Сяо Фанем'),
        ReplaceContainer('Маленький Бастард', 'маленькая черепашка'),
    ]

    text3 = replace_by_templates(replaces, text1)
    # запись в файл результата
    f = open('result.txt', 'a', encoding="utf-8")
    f.write(text3)
    f.close()

if __name__ == '__main__':
    i = 1
    # getTranslate_uukanshu_net()
    # getTranslate_ddyueshu_com()
    replaceByDictionary()

    print('Finished')

###  ожидает ссылку '/b/31560/161569.html'
def get_chapter_uukanshu_net(chapter_link):
    source_domain = 'https://www.uukanshu.com'
    html_page_charset = 'gbk'  # из charset в meta теге начала html страницы

    src = str(urllib.request.urlopen(source_domain + chapter_link).read().decode(html_page_charset))
    start_index = 0
    ch_begin = '<p><br/>'  # начало текста главы
    ch_end = '<div style="margin:0px;">'  # конец текста главы
    link_begin = '</span>\r\n                 \r\n                <a href="'  # начало ссылки следующей главы
    link_end = '" id="next" title'  # конец ссылки следующей главы
    # не работает на всех главах
    # text = str(src[src.find(ch_begin, start_index) + len(ch_begin):src.find(ch_end,
    #     src.find(ch_begin, start_index) + len(ch_begin))])
    chapter_link = str(
        src[src.find(link_begin, start_index) + len(link_begin):src.find(link_end, src.find(link_begin,
                                                                                            start_index) + len(
            link_begin))])

    # text = "\n".join(text.splitlines())
    text = src.splitlines()
    text = text[122] + text[131]

    replaces = [
        ReplaceContainer('<p>', ''),
        ReplaceContainer('<br/>', '\n'),
        ReplaceContainer('<br />', 'Перевод строки'),
        ReplaceContainer('\n\n\n\n', ''),
        ReplaceContainer('<div class="ad_content"><!-- 桌面内容中间2 -->', ''),
        ReplaceContainer('<ins class="adsbygoogle"', ''),
        ReplaceContainer('style="display:inline-block;width:336px;height:280px"', ''),
        ReplaceContainer('data-ad-client="ca-pub-7553981642580305"', ''),
        ReplaceContainer('data-ad-region="cont_mid"', ''),
        ReplaceContainer('data-ad-slot="4557028097"></ins>', ''),
        ReplaceContainer('<script>', ''),
        ReplaceContainer('(adsbygoogle = window.adsbygoogle || []).push({});', ''),
        ReplaceContainer('</script>', ''),
        ReplaceContainer('</div>', ''),
        ReplaceContainer('\r\n\r\n', ''),
    ]
    text = replace_by_templates(replaces, text)

    # удалить пустые строки
    text = "\n".join(text.splitlines())
    replaces = [
        ReplaceContainer('\n\n', ''),
        ReplaceContainer('\n\n\n\n', ''),
        ReplaceContainer('#UU', ''),
        ReplaceContainer('&#119;', ''),
        ReplaceContainer('&#46;', ''),
        ReplaceContainer('&#107;', ''),
        ReplaceContainer('&#32;', ''),
        ReplaceContainer('&#117;;', ''),
        ReplaceContainer('&#85;', ''),
        ReplaceContainer('&#97;', ''),
        ReplaceContainer('&#110;', ''),
        ReplaceContainer('&#85;', ''),
        ReplaceContainer('&#99;', ''),
        ReplaceContainer('&#109;', ''),
        ReplaceContainer('w', ''),
        ReplaceContainer('u', ''),
        ReplaceContainer('k', ''),
        ReplaceContainer('a', ''),
        ReplaceContainer('h', ''),
        ReplaceContainer('s', ''),
        ReplaceContainer('n', ''),
        ReplaceContainer('u', ''),
        ReplaceContainer('U', ''),
        ReplaceContainer('c', ''),
        ReplaceContainer('o', ''),
        ReplaceContainer('m', ''),
        ReplaceContainer('ｍ', ''),
        ReplaceContainer('ａ', ''),
        ReplaceContainer('ｗ', ''),
        ReplaceContainer('Ｕ', ''),
        ReplaceContainer('ｕ', ''),
        ReplaceContainer('ｋ', ''),
        ReplaceContainer('ｎ', ''),
        ReplaceContainer('ｈ', ''),
        ReplaceContainer('ｃ', ''),
        ReplaceContainer('ｏ', ''),
        ReplaceContainer('.', ''),
        ReplaceContainer('ｓ', ''),
        ReplaceContainer('&nbsp;', ''),
        ReplaceContainer('&#117;', ''),
        ReplaceContainer('&#115;', ''),
        ReplaceContainer('&#111;', ''),
        ReplaceContainer('&#104;', ''),
        ReplaceContainer('</div>', ''),
        ReplaceContainer('       ', ' '),
        ReplaceContainer('  ', ' '),
        ReplaceContainer('                ', ' '),
        ReplaceContainer('           ', ' '),
        ReplaceContainer('   ', ' '),
        ReplaceContainer('  ', ' '),
        ReplaceContainer('\n\n', '\n'),
        ReplaceContainer(' \n', ''),
        ReplaceContainer(' ?&bp;&bp;&bp;&bp;', ''),
        ReplaceContainer('　　&bp;&bp;&bp;&bp;', ''),
        ReplaceContainer('&bp;&bp;&bp;&bp;', ''),
        ReplaceContainer('  ', ''),
        ReplaceContainer('<!--flge-->', ''),
        ReplaceContainer('<!--flgpb--> ', ''),
        ReplaceContainer('　　', ''),
        ReplaceContainer('\r\n\r\n', '\n'),
    ]
    text = replace_by_templates(replaces, text)

    # удалить пустые строки
    text = "\n".join(text.splitlines())

    replaces = [
        ReplaceContainer('\n\n', '\n'),
        ReplaceContainer('Перевод строки', '\n'),
        ReplaceContainer('\n\n', '\n'),
    ]
    text = replace_by_templates(replaces, text)

    return text, chapter_link

def getTranslate_uukanshu_net():
    src_chapter_link = '/b/31560/161569.html'
    source_chapter_number = 1104
    result_replaces = [
        ReplaceContainer('\n', '\n\n')
    ]
    chapter_names = ['Ставки на публике',
                     'Избиение талантов небес',
                     'Тело серебряного сияния',
                     'Доведенный до отчаяния',
                     'Отчаяние - это только начало (1)',
                     'Отчаяние - это только начало (2)',
                     'Появление второго свирепого, безграничного в своей свирепости',
                     'Не можешь отступить, так оставайся',
                     'Выбыли из списка!',
                     'Общая просьба',
                     'Лев, широко раскрывший пасть',
                     'И подумать не могли, что они такие с...',
                     'Появление Богоубийцы',
                     'Истинная сила магической техники Подавления Тюрьмы',
                     'Божественное вооружение здесь, объединение с Богоубийцей',
                     'Падение Богоубийцы (1)',
                     'Падение Богоубийцы (2)',
                     'Здесь темно, пожалуйста закрой глаза',
                     'Клан Духа Огня',
                     'Земля движется, все переворачивается с ног на голову (1)',
                     'Земля движется, все переворачивается с ног на голову (2)',
                     'Смерть Богини Тысячи Дождей',
                     'Тело трех жизней',
                     'Контракт продажи',
                     'Мир в ужасе, спор продолжается',
                     'Новый великий глава, родившийся под несчастливой звездой',
                     'Выбор каждого',
                     'Обман до смерти',
                     'Поднимаются один за другим',
                     'Убил ее']

    driver = selenium.webdriver.Chrome()
    driver.get("https://www.deepl.com/ru/translator#zh/ru/")

    i = 0
    for ch_name in chapter_names:
        print('Глава ' + str(source_chapter_number + 69) + ' ' + ch_name + ' ' + src_chapter_link + ' ' + str(
            source_chapter_number))
        chapter_source, next_chapter_link = get_chapter_uukanshu_net(src_chapter_link)

        translate_number = source_chapter_number + 69  # номер главы на русском
        src_chapter_link = next_chapter_link  # ссылка на след главу
        source_chapter_number += 1  # номер для следующей главы

        elem = driver.find_element(By.CLASS_NAME, 'lmt__source_textarea')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'A')
        elem.send_keys(Keys.DELETE)
        elem.send_keys(chapter_source)
        time.sleep(16)
        elem = driver.find_element(By.CLASS_NAME, 'lmt__target_textarea')

        translate = elem.get_attribute("value")  # готовый перевод главы
        # translate = chapter_source ##############
        chapter = 'Глава ' + str(translate_number) + ' ' + ch_name + '\n' + translate + '\n'
        chapter = replace_by_templates(result_replaces, chapter)
        # запись в файл
        f = open('chapters.txt', 'a', encoding="utf-8")
        f.write(chapter)
        f.close()
        i = 1

    driver.quit()

