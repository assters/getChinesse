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

    # замена по регуляркам для юканшу
    # (" )([А-Я])        \1- \2
    #regex = re.compile('(?P<name>(" ))(?P<name2>([А-Я]))')
    #text1 = regex.sub('\g<name>- \g<name2>', text)
    text1 = text

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
        # новое 24 02 2024
        ReplaceContainer('Боевой Секты', 'секта Войны'),
        ReplaceContainer('Сын Священного Пламени', 'Сын Священного Огня'),
        ReplaceContainer('Сынов Священного Пламени', 'Сына Священного Огня'),
        ReplaceContainer('префектуры Нижнего Цинъюня', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('префектуры Нижняя Цинъюнь', 'области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('армии Варварского Дракона', 'Армии Дикого Дракона'),
        ReplaceContainer('Облачного Дракона', 'Дракон Облака'),
        ReplaceContainer('Сыном Священного Пламени', 'Сыном Священного Огня'),
        ReplaceContainer('Сыны Священного Пламени', 'Сыном Священного Огня'),
        ReplaceContainer('Ван Ланьтянь', 'Вань Лантянь'),
        ReplaceContainer('Ван Ланьтяня', 'Вань Лантяня'),
        ReplaceContainer('миль', 'ли'),
        ReplaceContainer('боюсь', 'скорее всего'),
        ReplaceContainer('Абсолютная небесная гордость', 'Бесподобные таланты небес'),
        ReplaceContainer('Северного Небацзы', 'секта Северного Неба'),
        ReplaceContainer('Сына Священного Пламени', 'Сына Священного Огня'),
        ReplaceContainer('смотрела друг на друга', 'переглядывалась'),
        ReplaceContainer('Секты Святого Огня', 'секты Священного Огня'),
        ReplaceContainer('Сына Святого Огня', 'Сына Священного Огня'),
        ReplaceContainer('клинок Духа Крови', 'Кинжал кровавых духов'),
        ReplaceContainer('нож Духа Крови', 'Кинжал кровавых духов'),
        ReplaceContainer('ноже Духа Крови', 'Кинжале кровавых духов'),
        ReplaceContainer('духи нежити', 'духи умерших'),
        ReplaceContainer('ножу Духа Крови', 'Кинжалу кровавых духов'),
        ReplaceContainer('Ван Лангтяня', 'Вань Лантяня'),
        ReplaceContainer('Клинок Обезглавливания Души Кровавого Духа', 'Кинжал кровавых духов'),
        ReplaceContainer('Ван Лангтиана', 'Вань Лантяня'),
        ReplaceContainer('армия Варварского Дракона', 'Армия Дикого Дракона'),
        ReplaceContainer('Сыновья Священного Пламени', 'Сын Священного Огня'),
        ReplaceContainer('Ван Лантянь', 'Вань Лантянь'),
        ReplaceContainer('Ван Лантяне', 'Вань Лантяне'),
        ReplaceContainer('тела сокровища', 'драгоценного тела'),
        ReplaceContainer('тело девяти янь', 'тело Девяти Солнц'),
        ReplaceContainer('сокровенных тел', 'драгоценных тел'),
        ReplaceContainer('Серебряное Лучезарное Тело', 'Тело Серебряного Сияния'),
        ReplaceContainer('Серебряного Лучезарного Тела', 'Тела Серебряного Сияния'),
        ReplaceContainer('" - Глядя', '" - глядя'),
        ReplaceContainer('" - Эта', '" - эта'),
        ReplaceContainer('Небесный клинок Серебряной Луны', 'Небесный Клинок Серебряной Луны'),
        ReplaceContainer('Небесный Меч Серебряной Луны', 'Небесный Клинок Серебряной Луны'),
        ReplaceContainer('Небесным Боевым Мечом', 'Подпирающим Небо Мечом Войны'),
        ReplaceContainer('" - После', '" - после'),
        ReplaceContainer('небесным мечом серебряной луны', 'Небесным Клинком Серебряной Луны'),
        ReplaceContainer('Небесного Пика', 'Тяньфэн'),
        ReplaceContainer('праймовая каменная рука', 'огромная каменная рука'),
        ReplaceContainer('" - В','" - в'),
        ReplaceContainer('Первобытная Каменная Рука', 'Огромная Каменная Рука'),
        ReplaceContainer('Первобытный Каменный Кулак', 'Огромная Каменный Кулак'),
        ReplaceContainer('Кулак Небесного Прайма', 'Огромная Каменный Кулак'),
        ReplaceContainer('" - Глядя', '" - глядя'),
        ReplaceContainer('Ван Лангтиан', 'Вань Лантянь'),
        ReplaceContainer('Первобытную Каменную Руку', 'огромную каменную руку'),
        ReplaceContainer('Первобытной Каменной Руки', 'огромной каменной руки'),
        ReplaceContainer('Первобытной Каменной Руке', 'огромной каменной руке'),
        ReplaceContainer('Небесная Каменная Рука Прайма', 'Огромная каменная рука'),
        ReplaceContainer('каменная рука Премьер-неба', 'огромная каменная рука'),
        ReplaceContainer('" - Все', '" - все'),
        ReplaceContainer('Юньлун', 'Дракон Облака'),
        ReplaceContainer('" - Увидев','" - увидев'),
        ReplaceContainer('Торговой палаты','торговой компании'),
        ReplaceContainer('"Облачный дракон"','Дракон Облака'),
        ReplaceContainer('" - Из','" - из'),
        ReplaceContainer('низшего состояния Цин Юня','области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Оптимистичной Каменной Руке','огромной каменной руке'),
        ReplaceContainer('Оптимистичную Каменную Руку','огромную каменную руку'),
        ReplaceContainer('Сыну Святого Огня','Сына Священного Огня'),
        ReplaceContainer('Премьер Небесных Каменных Рук','огромных каменных рук'),
        ReplaceContainer('Небесный Пик','Тяньфэн'),
        ReplaceContainer('Небесных Каменных Рук','огромных каменных рук'),
        ReplaceContainer('Главные Каменные Руки','огромные каменные руки'),
        ReplaceContainer('Главных Каменных Рук','огромных каменных рук'),
        ReplaceContainer('первобытных каменных рук','огромных каменных рук'),
        ReplaceContainer('Огромная Каменная Рука','огромная каменная рука'),
        ReplaceContainer('Первородные Небесные Каменные Руки','огромные каменные руки'),
        ReplaceContainer('Первородных огромных каменных рук','огромных каменных рук'),
        ReplaceContainer('секты Священного Пламени','секты Священного Огня'),
        ReplaceContainer('Сын Святого Пламени','Сын Священного Огня'),
        ReplaceContainer('Секты Святого Пламени','секты Священного Огня'),
        ReplaceContainer('сферу Шести Трансформаций Перевоплощения','сферу Шести Оборотов Колеса Сансары'),
        ReplaceContainer('Секту Священного Огня','секту Священного Огня'),
        ReplaceContainer('Секте Священного Огня','секте Священного Огня'),
        ReplaceContainer('Секте Священного Пламени','секте Священного Огня'),
        ReplaceContainer('Шестую Сферу Перевоплощения','Шестой Оборот Колеса Сансары'),
        ReplaceContainer('Секта Священного Пламени','секта Священного Огня'),
        ReplaceContainer('Сектой Священного Пламени','сектой Священного Огня'),
        ReplaceContainer('Сыновей Священного Пламени','Сына Священного Огня'),
        ReplaceContainer('Тел Сокровищ','драгоценных тел'),
        ReplaceContainer('Телом Сокровищ','драгоценным телом'),
        ReplaceContainer('Тело Земли','Тело Великой Земли'),
        ReplaceContainer('тело-сокровище','драгоценное тело'),
        ReplaceContainer('тел-сокровищ','драгоценных тел'),
        ReplaceContainer('" - Выражение','" - выражение'),
        ReplaceContainer('тело сокровища','драгоценное тело'),
        ReplaceContainer('земным телом','Телом Великой Земли'),
        ReplaceContainer('земное тело','Тело Великой Земли'),
        ReplaceContainer('" - Услышав','" - услышав'),
        ReplaceContainer('" - Посмотрев','" - посмотрев'),
        ReplaceContainer('" - На лицах','" - на лицах'),
        ReplaceContainer('" - У тех','" - у тех'),
        ReplaceContainer('" - У','" - у'),
        ReplaceContainer('" - Сразу','" - сразу'),
        ReplaceContainer('" - Внезапно','" - внезапно'),
        ReplaceContainer('" - Старик','" - старик'),
        ReplaceContainer('Бессмертным телом','Телом Святого'),
        ReplaceContainer('Земного тела','Великого Тела Земли'),
        ReplaceContainer('Небесными Каменными Руками','огромными каменными руками'),
        ReplaceContainer('Ван Лантяня','Вань Лантяня'),
        ReplaceContainer('Ван Лан Тянь','Вань Лантянь'),
        ReplaceContainer('Рейтинга Небес','Небесного Рейтинга'),
        ReplaceContainer('Рейтинг Небес','Небесный Рейтинг'),
        ReplaceContainer('армии варваров-драконов','Армии Дикого Дракона'),
        ReplaceContainer('Оптимусов Каменных Рук','огромных каменных рук'),
        ReplaceContainer('Окончательный Демонический Клинок','Последний Дьявольский Клинок'),
        ReplaceContainer('Окончательным Демоническим Клинком','Последнего Дьявольского Клинка'),
        ReplaceContainer('Последнего Демонического Лезвия','Последнего Дьявольского Клинка'),
        ReplaceContainer('армии варварских драконов','Армии Дикого Дракона'),
        ReplaceContainer('Окончательный Клинок Демона','Последний Дьявольский Клинок'),
        ReplaceContainer('запрещенным божественным оружием','божественным вооружением запретного ранга'),
        ReplaceContainer('Центральном Имперском Царстве','Мире Срединного Императора'),
        ReplaceContainer('Последнего Лезвия Демона','Последнего Дьявольского Клинка'),
        ReplaceContainer('Шестую Трансформацию Реинкарнации','Шестой Оборот Колеса Сансары'),
        ReplaceContainer('Армию Варварских Драконов','Армию Дикого Дракона'),
        ReplaceContainer('армии драконов-варваров','Армии Дикого Дракона'),
        ReplaceContainer('государстве Нижний Цинъюнь','области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Торговой Палатой','торговой компанией'),
        ReplaceContainer('последний дьявольский клинок','Последний Дьявольский Клинок'),
        ReplaceContainer('Варварского Дракона','Дикого Дракона'),
        ReplaceContainer('Варварского Леопарда','Дикого Леопарда'),
        ReplaceContainer('Армия Драконов-Варваров','Армия Дикого Дракона'),
        ReplaceContainer('Армия Варварских Драконов','Армия Дикого Дракона'),
        ReplaceContainer('Священная Земля Гуаньган','Святая Земля Распростертого Холода'),
        ReplaceContainer('" - Медленно','" - медленно'),
        ReplaceContainer('Бог Убийства','Богоубийца'),
        ReplaceContainer('убийство бога','Богоубийца'),
        ReplaceContainer('убить бога','Богоубийца'),
        ReplaceContainer('"Бум!" ,','"Бум!",'),
        ReplaceContainer('"Ка-чау"','"Щелк"'),
        ReplaceContainer('"Ка-чау!."','"Щелк"'),
        ReplaceContainer('"Щелк!" ,','"Щелк!",'),
        ReplaceContainer('футов','чжанов'),
        ReplaceContainer('Секты Священного Огня','секты Священного Огня'),
        ReplaceContainer('техника гигантского духа','Техника Духа Гиганта'),
        ReplaceContainer('техники гигантского духа','Техники Духа Гиганта'),
        ReplaceContainer('Священная Земля Гуанхань','Святая Земля Распростертого Холода'),
        ReplaceContainer('Небесной Секты Сюань','секты Северного Неба'),
        ReplaceContainer('Святой Девой Минъюй','Святая Дочь Мин Юй'),
        ReplaceContainer('Божественной Девы Тысячи Дождей','Богини Тысячи Дождей'),
        ReplaceContainer('Молчанияе','Молчания'),
        ReplaceContainer('Святой Девы Яркого Нефрита','Святой Дочери Мин Юй'),
        ReplaceContainer('префектуры Нижний Цинъюнь','области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Безмолвную гору','Хребет Молчания'),
        ReplaceContainer('государство Цинъюнь Нижнее','область Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Святая Земля Великого Рассеивания','Святая Земля Распростертого Холода'),
        ReplaceContainer('три свирепых и четыре свирепых','третий и четвертый свирепый'),
        ReplaceContainer('Молчаливой Горы','Хребта Молчания'),
        ReplaceContainer('Трех Свирепых и Четырех Свирепых','третьего и четвертого свирепого'),
        ReplaceContainer('трое и четверо','третий и четвертый'),
        ReplaceContainer('" - Вдруг','" - вдруг'),
        ReplaceContainer('" - Кто-то вдруг','" - кто-то вдруг'),
        ReplaceContainer('Безмолвного Холма','Хребта Молчания'),
        ReplaceContainer('" - Кто-то','" - кто-то'),
        ReplaceContainer('Молчаливого Хребта','Хребта Молчания'),
        ReplaceContainer('Божественной Леди Тысячи Дождей','Богини Тысячи Дождей'),
        ReplaceContainer('" - Довольно','" - довольно'),
        ReplaceContainer('" - Один','" - один'),
        ReplaceContainer('" - Несколько','" - несколько'),
        ReplaceContainer('государства Нижняя Цин Юнь','области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('"Ка-чау!"','"Щелк!"'),
        ReplaceContainer('"Щелк!" ,','"Щелк!",'),
        ReplaceContainer('Barbarian Dragon Army','Армию Дикого Дракона'),
        ReplaceContainer('Yunlong Торговая палата','торговую компанию Дракон Облака'),
        ReplaceContainer('Ван Руюн','Ван Жуюнь'),
        ReplaceContainer('Ван Руолю','Ван Жолю'),
        ReplaceContainer('Три Фола и Четыре Фола','третий и четвертый свирепый'),
        ReplaceContainer('" - Древнее','" - древнее'),
        ReplaceContainer('Безмолвный холм','Хребет Молчания'),
        ReplaceContainer('Нин Шуана','Нин Шуан'),
        ReplaceContainer('Убийственный Бог','Богоубийца'),
        ReplaceContainer('Великого Убийцы','великий свирепый'),
        ReplaceContainer('Древний Существовал','Древнее существо'),
        ReplaceContainer('Варварской Драконьей Армии','Армии Дикого Дракона'),
        ReplaceContainer('Святой Земли Гуаньган','Святой Земли Распростертого Холода'),
        ReplaceContainer('" - Горбатый','" - горбатый'),
        ReplaceContainer('Святая Земля Гуаньган','Святая Земля Распростертого Холода'),
        ReplaceContainer('" - Равнодушный','" - равнодушный'),
        ReplaceContainer('клана Байсе','семьи Байсе'),
        ReplaceContainer('Се Вуджи','Се Уцзи'),
        ReplaceContainer('Неистинный Владыка','У Чжэнь'),
        ReplaceContainer('Се Вуцзи','Се Уцзи'),
        ReplaceContainer('" - Высокий','" - высокий'),
        ReplaceContainer('Тихий Хребет','Хребет Молчания'),
        ReplaceContainer('Святой Земли Гуаньхань','Святой Земли Распростертого Холода'),
        ReplaceContainer('" - Ответ','" - ответ'),
        ReplaceContainer('старика-горбуна','горбатого старика'),
        ReplaceContainer('Деревом Великого Дракона Луо','Великим Драконьем Деревом Ло'),
        ReplaceContainer('верховными министрами-гостями','внешними верховным министрами'),
        ReplaceContainer('" - На лице','" - на лице'),
        ReplaceContainer('Ганодерма Чистого Ян','Духовный Корень Чистого Ян'),
        ReplaceContainer('Чистый Ян Линчжи','Духовный Корень Чистого Ян'),
        ReplaceContainer('Меч Духа Крови','Меч Кровавой Души'),
        ReplaceContainer('Старым Зомби','старым трупом'),
        ReplaceContainer('Святая Дева Яркого Нефрита','Святая Дочь Мин Юй'),
        ReplaceContainer('Священная Дева Яркого Нефрита','Святая Дочь Мин Юй'),
        ReplaceContainer('" - Слова','" - слова'),
        ReplaceContainer('Святую Деву Минъюй','Святая Дочь Мин Юй'),
        ReplaceContainer('" - Видя','" - видя'),
        ReplaceContainer('светлых орлов','Световых Орлов'),
        ReplaceContainer('" - И','" - И - с пробелом'),
        ReplaceContainer('" - Над','" - над'),
        ReplaceContainer('" - Лицо','" - лицо'),
        ReplaceContainer('Старый зомби','Старый труп'),
        ReplaceContainer('"Жужжание!"','"Б-о-о-м!"'),
        ReplaceContainer('Торговую палату','торговую компанию'),
        ReplaceContainer('армию Драконов-варваров','Армию Дикого Дракона'),
        ReplaceContainer('" - Глаза','" - глаза'),
        ReplaceContainer('Сотня семьи Се','Семья Байсе'),
        ReplaceContainer('" - Холодный','" - холодный'),
        ReplaceContainer('Безмолвной Горе','Хребте Молчания'),
        ReplaceContainer('Безмолвной Горы','Хребта Молчания'),
        ReplaceContainer('Фазы Дхармы Подавления Тюрьмы','магической техники Подавления Тюрьмы'),
        ReplaceContainer('Богу Убийства','Богоубийце'),
        ReplaceContainer('Бога Убийства','Богоубийцы'),
        ReplaceContainer('Богом Убийства','Богоубийцей'),
        ReplaceContainer('Боевая диаграмма пяти юаней','Боевая Диаграмма Пяти Основ'),
        ReplaceContainer('" - При','" - при'),
        ReplaceContainer('боевые карты пяти стихий','Боевую Диаграмму Пяти Основ'),
        ReplaceContainer('Меч Ветра Грома','Меч Ветра и Грома'),
        ReplaceContainer('Боевого Меча Наклонившегося Неба','Подпирающего Небо Меча Войны'),
        ReplaceContainer('Пятиэлементная Боевая Диаграмма','Боевая Диаграмма Пяти Основ'),
        ReplaceContainer('Диаграмму Пятиэлементной Битвы','Боевую Диаграмму Пяти Основ'),
        ReplaceContainer('Бессмертную Технику Трансформации','Технику Бессмертного Аватара'),
        ReplaceContainer('Диаграмму Пяти Элементарных Формаций','Боевую Диаграмму Пяти Основ'),
        ReplaceContainer('"Ни один не останется позади!"','"Убить всех!"'),
        ReplaceContainer('Бога Истребления','Богоубийцы'),
        ReplaceContainer('Фазой Дхармы Подавления Тюрьмы','магической техникой Подавления Тюрьмы'),
        ReplaceContainer('фаз Дхармы','магических техник'),
        ReplaceContainer('фазы Дхармы','магические техники'),
        ReplaceContainer('Фаза Дхармы','Магическая техника'),
        ReplaceContainer('фазе Дхармы','магической технике'),
        ReplaceContainer('Фазу Дхармы','магическую технику'),
        ReplaceContainer('черепашкарк','черепашка'),
        ReplaceContainer('Фазой Дхармы Бога','магической техникой божественного ранга'),
        ReplaceContainer('Мо Сяо Сяо','Мо Сяо'),
        ReplaceContainer('Мо Синь','Мо Сяо'),
        ReplaceContainer('тела-сокровища','драгоценных тела'),
        ReplaceContainer('Магическая техника Чжэнь Тюрьмы','магическая техника Подавления Тюрьмы'),
        ReplaceContainer('Святая Дева Минъюй','Святая Дочь Мин Юй'),
        ReplaceContainer('Бог Истребления','Богоубийца'),
        ReplaceContainer('"Щелк" ,','"Щелк!",'),
        ReplaceContainer('Бог-убийца','Богоубийца'),
        ReplaceContainer('Бог Убийц','Богоубийца'),
        ReplaceContainer('Бог Убийств','Богоубийца'),
        ReplaceContainer('Эфирного Пика','Туманного Пика'),
        ReplaceContainer('Небесный Остаточный Меч','Раскалывающий Небеса Меч'),
        ReplaceContainer('Меч Небесного Остатка','Раскалывающий Небеса Меч'),
        ReplaceContainer('Меч Остатка Неба','Раскалывающий Небеса Меч'),
        ReplaceContainer('Божественное Оружие','божественное вооружение'),
        ReplaceContainer('Чжэньтай','отделения порядка'),
        ReplaceContainer('Мисти Пик','Туманного Пика'),
        ReplaceContainer('Нижнее Цинъюнь','Возвышенные Земли Нижней Провинции'),
        ReplaceContainer('Небесный Боевой Меч','Подпирающий Небо Меч Войны'),
        ReplaceContainer('Нин Юаньюаньву','Нин Юаньву'),
        ReplaceContainer('бога-убийцу','Богоубийцу'),
        ReplaceContainer('Меча Небесного Остатка','Раскалывающего Небеса Меча'),
        ReplaceContainer('Меч Небесных Руин','Раскалывающий Небеса Меч'),
        ReplaceContainer('Небесный Расчленяющий Меч','Раскалывающий Небеса Меч'),
        ReplaceContainer('Бога Убийц','Богоубийцы'),
        ReplaceContainer('"Рев!"','"Р-о-а-а-а-г-р-х!"'),
        ReplaceContainer('Истребительного Бога','Богоубийцы'),
        ReplaceContainer('Боевым Копьем Разрыва Крови','Боевым Копьем Разрыва Крови'),
        ReplaceContainer('Боевые Доспехи Призрачного Змея','Боевые Доспехи Мрачной Змеи'),
        ReplaceContainer('Сонг Враг','Сун Ди'),
        ReplaceContainer('Широкой Холодной Святой Земли','Святая Земля Распростертого Холода'),
        ReplaceContainer('Лунный Обрушивающийся Небесный Лук','Небесный Лук Разорванной Луны'),
        ReplaceContainer('Сун Врага','Сун Ди'),
        ReplaceContainer('ветровым магическим цинем','Древней Цитрой Демона Ветра'),
        ReplaceContainer('ветровой магический цинь','Древняя Цитра Демона Ветра'),
        ReplaceContainer('боевой клан','Секта Войны'),
        ReplaceContainer('префектуре Нижний Цинъюнь','области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('"Рор!!!"','"Р-о-а-а-а-г-р-х!"'),
        ReplaceContainer('Божественных Оружий','божественных вооружений'),
        ReplaceContainer('Убийственном Боге','Богоубийце'),
        ReplaceContainer('бога-убийцы','Богоубийцы'),
        ReplaceContainer('"Huffing--!"','"Хуф!"'),
        ReplaceContainer('"Хаффинг!!!"','"Хуф!"'),
        ReplaceContainer('четыре убийцы','четверо свирепых'),
        ReplaceContainer('Небесный Лук Баттеринг Мун','Небесный Лук Разорванной Луны'),
        ReplaceContainer('Сун Враг','Сун Ди'),
        ReplaceContainer('"Рев!!!"','"Р-о-а-а-а-г-р-х!"'),
        ReplaceContainer('враг Сун','Сун Ди'),
        ReplaceContainer('Божественных Оружия','божественных вооружения'),
        ReplaceContainer('Бог Истребителей','Богоубийца'),
        ReplaceContainer('Врага Сун','Сун Ди'),
        ReplaceContainer('Боевая диаграмма Пять Юань','Боевая Диаграмма Пяти Основ'),
        ReplaceContainer('Пяти Элементов','Пяти Основ'),
        ReplaceContainer('Пяти Основ','Пяти Основ'),
        ReplaceContainer('Нижнем Государстве Зелёного Облака','Возвышенные Земли Нижней Провинции'),
        ReplaceContainer('Магическая техника Подавляющей Тюрьмы','Магическая техника Подавления Тюрьмы'),
        ReplaceContainer('Клинок Высшего Демона','Последний Дьявольский Клинок'),
        ReplaceContainer('Клинок Последнего Демона','Последний Дьявольский Клинок'),
        ReplaceContainer('Нин Фрост','Нин Шуан'),
        ReplaceContainer('Огненного Духа','Духа Огня'),
        ReplaceContainer('Огненных Духов','Духа Огня'),
        ReplaceContainer('Центрального Имперского Царства','Мира Срединного Императора'),
        ReplaceContainer('Небесный Лук Лавинной Луны','Небесный Лук Разорванной Луны'),
        ReplaceContainer('"Убить!" ,','"Убить!",'),
        ReplaceContainer('Яркого Нефрита','Мин Юй'),
        ReplaceContainer('Божественная дева','Богиня'),
        ReplaceContainer('Три стиля Махабхараты','Три Формы Мохэ'),
        ReplaceContainer('Мин Ночной Снег','Мин Есюэ'),
        ReplaceContainer('Святой Девы','Святой Дочери'),
        ReplaceContainer('Мин Нефрит','Мин Юй'),
        ReplaceContainer('Нангун Ци','Наньгун Вэнь'),
        ReplaceContainer('Наньгун Ци','Наньгун Вэнь'),
        ReplaceContainer('Городе Сунь Лун','городе Солнца и Луны'),
        ReplaceContainer('ваше превосходительство','старший'),
        ReplaceContainer('Сюань Луо','Сюань Ло'),
        ReplaceContainer('жидкости Тысячи Душ','Сока Тысячи Душ'),
        ReplaceContainer('Центральном Имперском Королевстве','Мире Срединного Императора'),
        ReplaceContainer('Священное Королевство','Святая страна'),
        ReplaceContainer('Священное царство','Святая страна'),
        ReplaceContainer('Свободное Королевство','Свободная страна'),
        ReplaceContainer('Свободное царство','Свободная страна'),
        ReplaceContainer('Светлое Королевство','страна Света'),
        ReplaceContainer('Светлого царства','страны Света'),
        ReplaceContainer('Центральную Императорскую империю','Мир Срединного Императора'),
        ReplaceContainer('Светлого Королевства','страны Света'),
        ReplaceContainer('Кровавое Бешенство','Кровавый Безумец'),
        ReplaceContainer('Гигантский Дух Бог Ци Дун','Гигант Великого Духа Ци Дун'),
        ReplaceContainer('Наньгун Цяня','Наньгун Вэня'),
        ReplaceContainer('Наньгун Цянем','Наньгун Вэнем'),
        ReplaceContainer('задиристый','неряшливый'),
        ReplaceContainer('просил Наньгун','Наньгун Вэнь'),
        ReplaceContainer('Nangong попросить','Наньгун Вэнь'),
        ReplaceContainer('Камнем Долголетия Небесного Воробья','Камнем Долголетия Небесной Птицы'),
        ReplaceContainer('Небесного Воробья','Небесной Птицы'),
        ReplaceContainer('ваша светлость','старший'),
        ReplaceContainer('Королевство Демонов','Дьявольская страна'),
        ReplaceContainer('Вашим Превосходительством','старшим'),
        ReplaceContainer('Вашему Превосходительству','старшему'),
        ReplaceContainer('камень долголетия Небесной Птицы','Камень Долголетия Небесной Птицы'),
        ReplaceContainer('фрукт дракона Великого Луо','Великий Драконий Фрукт Ло'),
        ReplaceContainer('Нижнее Государство Цинъюнь','область Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Небесный Лук Разрушающейся Луны','Небесный Лук Разорванной Луны'),
        ReplaceContainer('Доспехи Призрачного Змея','Боевые Доспехи Мрачной Змеи'),
        ReplaceContainer('Боевое Копье Кровавого Разрыва','Боевое Копье Разрыва Крови'),
        ReplaceContainer('префектура Нижнего Цинъюня','область Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('префектуре Нижняя Цинъюнь','области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Тихой Гряды','Хребта Молчания'),
        ReplaceContainer('Безмолвного Хребта','Хребта Молчания'),
        ReplaceContainer('прайдов','гордостей'),
        ReplaceContainer('Шести Трансформаций','Шести Оборотов'),
        ReplaceContainer('Небесный Принц Сюань','Сын секты Северного Неба'),
        ReplaceContainer('Колеса Реинкарнации','Колеса Сансары'),
        ReplaceContainer('Реинкарнация шести изменений','Колесо Сансары Шести Оборотов'),
        ReplaceContainer('Нижнего государства Цинъюнь','области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Нижняя Префектура Цинъюнь','область Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('фрукт Великого Дракона Луо','Великий Драконий Фрукт Ло'),
        ReplaceContainer('Священная Земля Широкого Холода','Святая Земля Распростертого Холода'),
        ReplaceContainer('Циньмэнь','Секта Цинь'),
        ReplaceContainer('Небесный Лунный Лук Лавины','Небесный Лук Разорванной Луны'),
        ReplaceContainer('государства Нижний Цинъюнь','области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('государством Цин Юнь','областью Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Божественный Солдат Секты Чжэнь','основопологающее божественное вооружение'),
        ReplaceContainer('небесный лук Лунного Обрушения','Небесный Лук Разорванной Луны'),
        ReplaceContainer('Маленький Ублюдок','маленькая черепашка'),
        ReplaceContainer('Жидкость Тысячи Душ','Сок Тысячи Душ'),
        ReplaceContainer('Царства Света','страны Света'),
        ReplaceContainer('рафинировать','очищать'),
        ReplaceContainer('Верхнее государство','верхнию область'),
        ReplaceContainer('Маленький Ван Бастард','маленькая черепашка'),
        ReplaceContainer('Королевство Света','страна Света'),
        ReplaceContainer('Маленького Ублюдка','маленькую черепашку'),
        ReplaceContainer('Царство Света','страна Света'),
        ReplaceContainer('маленького Ван Бастарда','маленькую черепашку'),
        ReplaceContainer('Святую Землю Гуаньган','Святую Землю Распростертого Холода'),
        ReplaceContainer('боевое копье Кровавого Разлома','Боевое Копье Разрыва Крови'),
        ReplaceContainer('лунный лук','Небесный Лук Разорванной Луны'),
        ReplaceContainer('"Шаша-шаша!"','"Шу-шу-шу!"'),
        ReplaceContainer('Великое Драконье Дерево Луо','Великое Драконье Дерево Ло'),
        ReplaceContainer('драконьего дерева Луо','Великого Драконьего Дерева Ло'),
        ReplaceContainer('драконий фрукт Луо','Великий Драконий Фрукт Ло'),
        ReplaceContainer('Драконий фрукт Великого Луо','Великий Драконий Фрукт Ло'),
        ReplaceContainer('маленького Ван Барка','маленькой черепашки'),
        ReplaceContainer('армию варваров-драконов','Армию Дикого Дракона'),
        ReplaceContainer('принц','Молодой господин'),
        ReplaceContainer('Царства Дьявола','Дьявольской страны'),
        ReplaceContainer('Царства Демона','Дьявольской страны'),
        ReplaceContainer('Драконьего Дерева Великого Ло','Великого Драконьего Дерева Ло'),
        ReplaceContainer('Драконьего Дерева Великого Ло','Великого Драконьего Дерева Ло'),
        ReplaceContainer('Страны Дьявола','Дьявольской страны'),
        ReplaceContainer('Нижней Префектуры Цинъюнь','области Возвышенных Земель Нижней Провинции'),
        ReplaceContainer('Последний Демонический Клинок','Последний Дьявольский Клинок'),
        ReplaceContainer('Золотом Драконьем Посохе','Золотой Трости Дракона'),
        ReplaceContainer('Шести Оборотов в Единстве','Единства Шести Оборотов'),
        ReplaceContainer('Посох Золотого Дракона','Золотая Трость Дракона'),
        ReplaceContainer('Окончательный Демонический Меч','Последний Дьявольский Клинок')
    ]

    text3 = replace_by_templates(replaces, text1)
    # запись в файл результата
    f2 = open('result.txt', 'a', encoding="utf-8")
    f2.write(text3)
    f2.close()

if __name__ == '__main__':
    i = 1
    # getTranslate_uukanshu_net()
    # getTranslate_ddyueshu_com()

    # Перед заменой Замемнить
    #\r\n   на \r\nReplaceContainer('
    #\r\n   на '),\r\n
    # и вставить между переводами ', '  ---- через альт сначала ,' в правой части
    # потом вырезать правую и вставить '    -----   \r\n   на '\r\n
    replaceByDictionary()

    # Регулярки (ручные):
    # (" )([А-Я])        \1- \2          ----для дефисов
    # ("[.] )([А-Я])     " - \2
    # Обычные:
    # ". -               " -
    # !".                !"
    # ?".                ?"
    # \r\n               \r\n\r\n
    # \r\n\r\n\r\n\r\n   \r\n\r\n
    #
    # (" - )([А-Я])     ----ф3 потом заменить ф2 на изменный макрос контрол шифт ф2
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
