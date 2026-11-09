#!/usr/bin/env python3
"""Insert the joint founders page into content/ru.json and content/en.json.

Replaces the earlier single-founder page (/founder/, now redirected).

Kept in the repository so the page structure is reproducible, and so the
placeholder copy is obvious at a glance rather than buried in a large JSON file.
Every `body` string below is DRAFT TEXT and must be replaced.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
CONTENT = ROOT / "content"


def gal(slug, items, cols=3):
    return {
        "cols": cols,
        "images": [
            {"src": f"founder/{slug}/{n:02d}.jpg", "alt": alt, "caption": cap}
            for n, (alt, cap) in enumerate(items, 1)
        ],
    }


def entry(year, title, role, body, slug, images, cols=3, where=None, where_note=None):
    e = {"year": year, "title": title, "role": role, "body": body}
    if where:
        e["where"] = where
        if where_note:
            e["where_note"] = where_note
    e.update(gal(slug, images, cols))
    return e


RU_ENTRIES = [
    entry("2022", "Электрический трайк с навесом", "Личный проект · рама, навес, компоновка",
          ["ЧЕРНОВИК. Личный проект вне автомобильной тематики: рама, защитный навес и компоновка "
           "посадочных мест, рассчитанные на двух пассажиров. Сделан целиком своими руками — от "
           "конструкции до сборки."],
          "scooter",
          [("Трайк с поднятым навесом в поле", "Навес в поднятом положении"),
           ("Трайк, вид сбоку", "Компоновка на двоих"),
           ("Трайк на дороге", "Рама и посадочные места")]),

    entry("2009", "Интерьеры на воде", "Яхтенные интерьеры · публикации",
          ["ЧЕРНОВИК. Работа с интерьерами катеров и яхт: та же задача, что и в автомобиле, но "
           "другие материалы, другая влажность и другие нормы. Проекты этого периода попадали в "
           "профильную прессу."],
          "princess",
          [("Моторная яхта на ходу", "Моторная яхта"),
           ("Обложка яхтенного журнала", "Публикация в профильной прессе"),
           ("Обложка яхтенного журнала", "Публикация в профильной прессе")]),

    entry("2008", "Плафон такси", "Дизайн · оснастка · серия",
          ["ЧЕРНОВИК. Светящийся плафон на крышу такси: дизайн, объёмная модель, оснастка и "
           "серийное производство. Небольшой по размеру, но полный по циклу проект — тот же путь "
           "от эскиза до тиража, что и в перегородках десятью годами позже."],
          "plafon",
          [("Такси с плафоном на крыше", "Изделие на автомобиле"),
           ("Плафон вечером с подсветкой", "Подсветка"),
           ("Плафон крупным планом", "Корпус и экран"),
           ("Визуализация плафона", "Визуализация проекта")], cols=2),

    entry("2008", "ЗиЛ-4107 — салон представительского лимузина", "Эскиз · инжиниринг · производство",
          ["ЧЕРНОВИК. Полная переделка салона представительского лимузина советского производства. "
           "Проект начинался с ручных эскизов — компоновка задней зоны, кресла, отделка — и дошёл "
           "до готового салона."],
          "zil",
          [("Эскиз салона от руки", "Эскиз компоновки"),
           ("Готовый салон, задняя зона", "Задняя зона"),
           ("Готовый салон, отделка", "Отделка и материалы")]),

    entry("2007", "Mercedes-Benz S-Class W221 — первая перегородка", "Эскиз · CAD · оснастка · изделие",
          ["ЧЕРНОВИК. Та самая первая перегородка, с которой начинается отсчёт 7pro8. Проект прошёл "
           "весь цикл, который потом стал стандартом: эскиз, объёмная модель, конструкторская "
           "разработка механизма подъёма стекла, оснастка, изделие.",
           "Всё, что компания делает сегодня в серии, выросло из этой работы."],
          "w221",
          [("Эскиз салона с перегородкой", "Эскиз"),
           ("Визуализация салона", "Визуализация"),
           ("CAD-модель каркаса перегородки", "Конструкция каркаса"),
           ("Готовая перегородка в автомобиле", "Изделие в автомобиле")], cols=2),

    entry("≈2005", "Mercedes-Benz Vito — VIP-салон", "Салон · мультимедиа · перегородка",
          ["ЧЕРНОВИК. Микроавтобус, переделанный в передвижной кабинет: индивидуальные кресла, "
           "консоли, мультимедиа и внутрисалонная перегородка. Ранний пример того типа задачи, на "
           "которой позже построилась серия."],
          "vito",
          [("Салон Vito с индивидуальными креслами", "Кресла и консоли"),
           ("Задняя зона с монитором", "Мультимедиа"),
           ("Столик в рабочем положении", "Рабочий столик"),
           ("Отделка салона", "Отделка")], cols=2),

    entry("2004", "Lamborghini Diablo VT", "Салон · аудио · отделка",
          ["ЧЕРНОВИК. Полная переделка интерьера суперкара: центральная консоль, приборная зона, "
           "аудиосистема, отделка кожей и карбоном. Работа, требующая точной посадки деталей в "
           "тесном салоне без единой прямой поверхности."],
          "diablo",
          [("Lamborghini Diablo снаружи", "Автомобиль проекта"),
           ("Центральная консоль", "Центральная консоль"),
           ("Приборная зона", "Приборная зона"),
           ("Отделка кожей и карбоном", "Материалы")], cols=2),

    entry("2003", "Chevrolet Corvette", "Салон · консоль · отделка",
          ["ЧЕРНОВИК. Салон классического Corvette: новая центральная консоль, отделка и "
           "оборудование. Проект из той серии работ, которые в начале 2000-х формировали "
           "отечественный тюнинг как отрасль."],
          "corvette",
          [("Corvette снаружи", "Автомобиль проекта"),
           ("Corvette, вид сзади", "Вид сзади"),
           ("Центральная консоль салона", "Консоль и отделка")]),

    entry("≈2003", "Hummer H1 — VIP-салон", "Салон · свет · мультимедиа",
          ["ЧЕРНОВИК. Внедорожник, превращённый в представительский салон: диван, отделка шпоном, "
           "контурный свет, мультимедиа. Заказ выполнялся для частного клиента.",
           "ИМЯ ЗАКАЗЧИКА НА СТРАНИЦЕ НЕ УКАЗАНО НАМЕРЕННО — см. примечание к странице."],
          "hummer",
          [("Hummer H1 снаружи", "Автомобиль проекта"),
           ("Задний диван и отделка", "Задняя зона"),
           ("Салон с подсветкой", "Свет и отделка"),
           ("Бар в салоне", "Оборудование салона")], cols=2),

    entry("2001", "Lincoln Reincarnation", "Кузов · салон · свет",
          ["ЧЕРНОВИК. Самый заметный проект раннего периода: автомобиль с полностью переделанным "
           "кузовом и салоном, показанный на выставках и разобранный прессой. Название проекта "
           "закрепилось за студией надолго."],
          "lincoln",
          [("Lincoln Reincarnation снаружи", "Автомобиль проекта"),
           ("Автомобиль сзади в свете фар", "Задняя оптика"),
           ("Подсветка колёсных арок", "Свет"),
           ("Салон автомобиля", "Салон")], cols=2),

    entry("≈2000", "Цех, команда, первые тиражи", "Производство · люди",
          ["ЧЕРНОВИК. Период, когда мастерская превратилась в компанию с собственным производством: "
           "дизайн, макетный участок, металл, пошив, шпон, электроника — всё под одной крышей."],
          "team",
          [("Команда студии у автомобиля", "Команда"),
           ("Команда студии, групповое фото", "Команда"),
           ("Команда у автомобиля сзади", "Команда"),
           ("Здание студии", "Цех")], cols=2),

    entry("≈1999", "До ателье: гараж, гонки, пресса", "Начало",
          ["ЧЕРНОВИК. Самое начало: работа руками в неотапливаемом гараже, самодельные проекты на "
           "том, что было под рукой, кольцевые гонки и первые знакомства в автомобильной прессе. "
           "Отсюда всё и пошло."],
          "workshop",
          [("Работа в цеху", "Гараж, начало 2000-х"),
           ("Коллаж из фотографий работы", "Из архива")], cols=2),
]

EN_ENTRIES = [
    entry("2022", "Electric trike with a canopy", "Personal project · frame, canopy, layout",
          ["DRAFT. A personal project outside cars: frame, protective canopy and seating layout for "
           "two. Built entirely by hand, from the structure to final assembly."],
          "scooter",
          [("Trike with the canopy raised, in a field", "Canopy raised"),
           ("Trike from the side", "Layout for two"),
           ("Trike on the road", "Frame and seating")]),

    entry("2009", "Interiors on the water", "Marine interiors · press",
          ["DRAFT. Work on boat and yacht interiors: the same problem as in a car, but different "
           "materials, different humidity and different rules. Projects from this period appeared "
           "in the trade press."],
          "princess",
          [("Motor yacht under way", "Motor yacht"),
           ("Yachting magazine cover", "Trade press"),
           ("Yachting magazine cover", "Trade press")]),

    entry("2008", "Taxi roof sign", "Design · tooling · series",
          ["DRAFT. An illuminated roof sign for taxis: design, 3D model, tooling and series "
           "production. Small in size but complete in cycle — the same route from sketch to volume "
           "that the partitions would take ten years later."],
          "plafon",
          [("Taxi with the roof sign fitted", "Fitted to the car"),
           ("Roof sign lit at night", "Illumination"),
           ("Roof sign in close-up", "Housing and screen"),
           ("Rendering of the roof sign", "Project rendering")], cols=2),

    entry("2008", "ZiL-4107 — state limousine interior", "Sketch · engineering · production",
          ["DRAFT. A complete rebuild of the interior of a Soviet state limousine. The project began "
           "as hand sketches — rear compartment layout, seating, trim — and ran through to a "
           "finished interior."],
          "zil",
          [("Hand sketch of the interior", "Layout sketch"),
           ("Finished interior, rear compartment", "Rear compartment"),
           ("Finished interior, trim detail", "Trim and materials")]),

    entry("2007", "Mercedes-Benz S-Class W221 — the first partition", "Sketch · CAD · tooling · product",
          ["DRAFT. The first partition, and where 7pro8 starts counting. The project ran through the "
           "full cycle that later became the standard: sketch, 3D model, engineering of the glass "
           "lift mechanism, tooling, finished product.",
           "Everything the company builds in series today grew out of this job."],
          "w221",
          [("Sketch of the interior with the partition", "Sketch"),
           ("Rendering of the interior", "Rendering"),
           ("CAD model of the partition frame", "Frame engineering"),
           ("Finished partition in the car", "Product in the car")], cols=2),

    entry("≈2005", "Mercedes-Benz Vito — VIP interior", "Interior · multimedia · partition",
          ["DRAFT. A van turned into a mobile office: individual seats, consoles, multimedia and an "
           "interior partition. An early example of exactly the kind of work the series business was "
           "later built on."],
          "vito",
          [("Vito interior with individual seats", "Seats and consoles"),
           ("Rear zone with a monitor", "Multimedia"),
           ("Table in the working position", "Work table"),
           ("Interior trim", "Trim")], cols=2),

    entry("2004", "Lamborghini Diablo VT", "Interior · audio · trim",
          ["DRAFT. A full interior rebuild of a supercar: centre console, instrument area, audio "
           "system, leather and carbon trim. Work that demands exact fit in a cramped cabin with no "
           "flat surfaces at all."],
          "diablo",
          [("Lamborghini Diablo exterior", "The project car"),
           ("Centre console", "Centre console"),
           ("Instrument area", "Instrument area"),
           ("Leather and carbon trim", "Materials")], cols=2),

    entry("2003", "Chevrolet Corvette", "Interior · console · trim",
          ["DRAFT. The interior of a classic Corvette: a new centre console, trim and equipment. One "
           "of the run of projects that, in the early 2000s, turned Russian tuning into an industry."],
          "corvette",
          [("Corvette exterior", "The project car"),
           ("Corvette from the rear", "Rear view"),
           ("Centre console", "Console and trim")]),

    entry("≈2003", "Hummer H1 — VIP interior", "Interior · lighting · multimedia",
          ["DRAFT. An off-roader turned into an executive interior: bench seat, veneer trim, ambient "
           "lighting, multimedia. Built for a private client.",
           "THE CLIENT IS DELIBERATELY NOT NAMED HERE — see the note on this page."],
          "hummer",
          [("Hummer H1 exterior", "The project car"),
           ("Rear bench and trim", "Rear compartment"),
           ("Interior with ambient lighting", "Lighting and trim"),
           ("Bar unit in the interior", "Interior equipment")], cols=2),

    entry("2001", "Lincoln Reincarnation", "Body · interior · lighting",
          ["DRAFT. The most visible project of the early period: a car with a completely rebuilt body "
           "and interior, shown at exhibitions and covered by the press. The project name stayed "
           "attached to the studio for years."],
          "lincoln",
          [("Lincoln Reincarnation exterior", "The project car"),
           ("The car from the rear, lights on", "Rear lighting"),
           ("Wheel arch lighting", "Lighting"),
           ("Interior of the car", "Interior")], cols=2),

    entry("≈2000", "Workshop, team, first volumes", "Production · people",
          ["DRAFT. The period when a workshop became a company with production of its own: design, "
           "model shop, metalwork, upholstery, veneer, electronics — all under one roof."],
          "team",
          [("The studio team by a car", "The team"),
           ("The studio team, group photograph", "The team"),
           ("The team behind a car", "The team"),
           ("The studio building", "The workshop")], cols=2),

    entry("≈1999", "Before the studio: a garage, racing, the press", "The beginning",
          ["DRAFT. The very beginning: hands-on work in an unheated garage, home-built projects out "
           "of whatever was to hand, circuit racing and the first contacts in the motoring press. "
           "This is where it all came from."],
          "workshop",
          [("Working in the workshop", "The garage, early 2000s"),
           ("Collage of working photographs", "From the archive")], cols=2),
]


# Which employer each project falls under. Derived from the career dates above
# against the photograph dates — it is a mapping, not something stated, and the
# entries on period boundaries are marked as such.
WHERE_RU = [
    ("Личный проект", None),
    ("Cardi Design / «Кар Фэйшн»", "граница периодов по датам — уточнить"),
    ("Cardi Design", "по датам снимков"),
    ("Cardi Design", "по датам снимков"),
    ("«Автоганза» / Cardi Design", "год перехода; отсюда 7pro8 ведёт отсчёт первой перегородки"),
    ("ОАО «Автоганза»", "по датам — уточнить"),
    ("A-Level", "по датам; фотографии при этом из материалов SV-ART — расхождение"),
    ("SV-ART / A-Level", "год перехода — уточнить"),
    ("SV-ART", "по датам — уточнить"),
    ("SV-ART", None),
    ("SV-ART · СКБ МАМИ", "по датам — уточнить"),
    ("До СКБ МАМИ", None),
]

WHERE_EN = [
    ("Personal project", None),
    ("Cardi Design / Car Fashion", "falls on a period boundary — to be confirmed"),
    ("Cardi Design", "from photograph dates"),
    ("Cardi Design", "from photograph dates"),
    ("Avtoganza / Cardi Design", "the year of the move; 7pro8 dates its first partition from here"),
    ("Avtoganza", "from dates — to be confirmed"),
    ("A-Level", "from dates; the photographs, however, come from SV-ART material — a discrepancy"),
    ("SV-ART / A-Level", "the year of the move — to be confirmed"),
    ("SV-ART", "from dates — to be confirmed"),
    ("SV-ART", None),
    ("SV-ART · SKB MAMI", "from dates — to be confirmed"),
    ("Before SKB MAMI", None),
]


# --------------------------------------------------------------------------
# Timeline data. Year spans are [from, to) on a shared axis.
# Iliya Bolshakov: supplied by him — real.
# Evgenii Abramov: NOT YET SUPPLIED — every segment is tentative and drawn
# dashed until the real record replaces it.
# --------------------------------------------------------------------------

AXIS_START, AXIS_END = 2000, 2027
TICKS = [2000, 2005, 2010, 2015, 2020, 2025]

ILYA_SEGMENTS = {
    "ru": [
        (2000, 2001, "2000–2001", "СКБ МАМИ", "Макетчик-конструктор"),
        (2001, 2003, "2001–2003", "SV-ART", "Конструктор, главный конструктор"),
        (2003, 2005, "2003–2005", "A-Level", "Конструктор интерьера автомобиля"),
        (2005, 2007, "2005–2007", "ОАО «Автоганза»", "Инженер-конструктор"),
        (2007, 2009, "2007–2009", "Cardi Design", "Конструктор"),
        (2009, 2015, "2009–2015", "ОАО «Кар Фэйшн»", "Конструктор интерьера автомобиля"),
        (2015, AXIS_END, "с 2015", "7pro8", "Сооснователь, совладелец"),
    ],
    "en": [
        (2000, 2001, "2000–2001", "SKB MAMI", "Model maker and design engineer"),
        (2001, 2003, "2001–2003", "SV-ART", "Design engineer, then chief design engineer"),
        (2003, 2005, "2003–2005", "A-Level", "Vehicle interior design engineer"),
        (2005, 2007, "2005–2007", "Avtoganza", "Design engineer"),
        (2007, 2009, "2007–2009", "Cardi Design", "Design engineer"),
        (2009, 2015, "2009–2015", "Car Fashion", "Vehicle interior design engineer"),
        (2015, AXIS_END, "since 2015", "7pro8", "Co-founder, co-owner"),
    ],
}

EVGENII_SEGMENTS = {
    "ru": [
        (2001, 2015, "≈2001–2015", "Места работы уточняются", "Нужна биография — как у Ильи"),
        (2015, AXIS_END, "с 2015", "7pro8", "Сооснователь"),
    ],
    "en": [
        (2001, 2015, "≈2001–2015", "Career to be supplied", "Needs the same record as Iliya's"),
        (2015, AXIS_END, "since 2015", "7pro8", "Co-founder"),
    ],
}


def segments(rows, tentative_all=False):
    out = []
    for f, t, years, org, role in rows:
        seg = {"from": f, "to": t, "years": years, "org": org, "role": role}
        if org == "7pro8":
            seg["current"] = True
        elif tentative_all:
            seg["tentative"] = True
        out.append(seg)
    return out


def with_where(entries, where, prefix):
    out = []
    for e, (w, note) in zip(entries, where):
        e = dict(e)
        e["where"] = f"{prefix}{w}"
        if note:
            e["where_note"] = note
        out.append(e)
    return out


def page(lang):
    p = "" if lang == "en" else "/ru"
    ru = lang == "ru"
    ilya = "Илья Большаков" if ru else "Iliya Bolshakov"
    evg = "Евгений Абрамов" if ru else "Evgenii Abramov"

    return {
        "slug": "founders",
        "title": "Основатели" if ru else "Founders",
        "title_tag": (f"{evg} и {ilya} — основатели 7pro8" if ru
                      else f"{evg} and {ilya} — founders of 7pro8"),
        "description": (
            "Евгений Абрамов и Илья Большаков работают вместе с начала 2000-х. Общая "
            "хронология: места работы, первая перегородка 2007 года, 7pro8 как компания с 2015 года."
            if ru else
            "Evgenii Abramov and Iliya Bolshakov have worked together since the early 2000s. A shared "
            "chronology: careers, the first partition in 2007, 7pro8 as a company since 2015."
        ),
        "blocks": [
            {
                "type": "pagehead",
                "kicker": "Основатели" if ru else "Founders",
                "title": f"{evg} и {ilya}" if ru else f"{evg} and {ilya}",
                "lead": (
                    "Вместе с начала 2000-х. Двадцать с лишним лет в одном ремесле — "
                    "конструирование автомобильного интерьера, — сначала в чужих мастерских, с "
                    "2015 года в своей. 7pro8 — это их общая работа, доведённая до серии."
                    if ru else
                    "Together since the early 2000s. More than twenty years in one craft — "
                    "vehicle interior engineering — first in other people's workshops and, since "
                    "2015, in their own. 7pro8 is their shared work, taken through to series."
                ),
                "meta": [
                    {"label": "Работают вместе" if ru else "Working together", "value": "с начала 2000-х" if ru else "since the early 2000s"},
                    {"label": "Первая перегородка" if ru else "First partition", "value": "2007"},
                    {"label": "7pro8 как компания" if ru else "7pro8 as a company", "value": "с 2015" if ru else "since 2015"},
                ],
            },
            {
                "type": "note",
                "variant": "draft",
                "title": "Черновик страницы" if ru else "Draft page",
                "body": [
                    "Настоящие данные здесь — биография и места работы Ильи Большакова. Всё, что "
                    "относится к Евгению Абрамову, — заготовка: его места работы на шкале "
                    "нарисованы пунктиром. Описания проектов помечены словом ЧЕРНОВИК. Этот блок "
                    "удаляется одной строкой в content-файле."
                    if ru else
                    "The real data here is Iliya Bolshakov's biography and career. Everything about "
                    "Evgenii Abramov is a placeholder — his segments on the timeline are drawn "
                    "dashed. The project descriptions are marked DRAFT. This block is one line to "
                    "delete in the content file."
                ],
            },
            {
                "type": "duo",
                "people": [
                    {
                        "name": evg,
                        "role": "Сооснователь 7pro8" if ru else "Co-founder, 7pro8",
                        "portrait": "founders/abramov.jpg",
                        "body": [
                            "ЧЕРНОВИК. Два-три предложения о пути Евгения: с чего начинал, где "
                            "работал, за что в компании отвечает сегодня. Нужна та же информация, "
                            "что уже есть по Илье, — годы, организации, должности."
                            if ru else
                            "DRAFT. Two or three sentences on Evgenii's route: where he started, where "
                            "he worked, what he is responsible for in the company today. The same "
                            "record already supplied for Iliya is needed — years, organisations, roles.",
                        ],
                    },
                    {
                        "name": ilya,
                        "role": "Сооснователь 7pro8" if ru else "Co-founder, 7pro8",
                        "portrait": "founders/bolshakov.jpg",
                        "body": [
                            "Начал в 2000 году макетчиком-конструктором в СКБ МАМИ — с рук и с "
                            "макета, а не с чертежа. Через год перешёл в SV-ART и за два года "
                            "вырос до главного конструктора."
                            if ru else
                            "Started in 2000 as a model maker and design engineer at SKB MAMI — with "
                            "his hands and a mock-up rather than with a drawing. A year later he moved "
                            "to SV-ART, and within two years was its chief design engineer.",
                            "Дальше — A-Level, «Автоганза», Cardi Design, «Кар Фэйшн»: пятнадцать "
                            "лет конструирования автомобильных интерьеров в компаниях, которые "
                            "создавали эту отрасль в России. С 2015 года — 7pro8."
                            if ru else
                            "Then A-Level, Avtoganza, Cardi Design and Car Fashion: fifteen years of "
                            "engineering vehicle interiors inside the companies that built that "
                            "industry in Russia. Since 2015, 7pro8.",
                        ],
                    },
                ],
            },
            {
                "type": "lanes",
                "title": "Два пути на одной шкале" if ru else "Two routes on one axis",
                "lead": (
                    "Где работал каждый из основателей, год за годом. Пунктир — даты, которые ещё "
                    "не подтверждены."
                    if ru else
                    "Where each founder worked, year by year. Dashed segments are dates not yet "
                    "confirmed."
                ),
                "start": AXIS_START,
                "end": AXIS_END,
                "ticks": TICKS,
                "together": {
                    "from": 2001,
                    "label": "Вместе — с начала 2000-х, точный год уточняется" if ru
                             else "Together from the early 2000s — exact year to be confirmed",
                },
                "lanes": [
                    {"name": evg, "segments": segments(EVGENII_SEGMENTS[lang], tentative_all=True)},
                    {"name": ilya, "segments": segments(ILYA_SEGMENTS[lang])},
                ],
                "footnote": (
                    "Проекты ниже сделаны в разные из этих периодов. Прежде чем публиковать "
                    "страницу, стоит подтвердить с бывшими работодателями, какие из работ можно "
                    "показывать и под чьим именем."
                    if ru else
                    "The projects below were done across these periods. Before this page is "
                    "published it is worth confirming with the former employers which of the work "
                    "may be shown, and under whose name."
                ),
            },
            {
                "type": "chronicle",
                "title": "Работы, от новых к старым" if ru else "The work, newest first",
                "lead": (
                    "Двенадцать проектов за двадцать пять лет, от сегодняшнего к началу. Под "
                    "названием — где в это время работал Илья; участие Евгения в каждом проекте "
                    "надо отметить отдельно."
                    if ru else
                    "Twelve projects across twenty-five years, from the present back to the "
                    "beginning. Under each title is where Iliya was working at the time; Evgenii's "
                    "part in each project still needs to be marked."
                ),
                "entries": (with_where(RU_ENTRIES, WHERE_RU, "Илья: ") if ru
                            else with_where(EN_ENTRIES, WHERE_EN, "Iliya: ")),
                "footnote": (
                    "Годы взяты из EXIF-данных снимков и названий архивов; отмеченные знаком ≈ "
                    "восстановлены по косвенным признакам. Период под каждым названием выведен "
                    "сопоставлением этих дат с местами работы — это вывод, а не факт из первых "
                    "рук. Снимки до 2007 года — сканы отпечатков и веб-графика того времени."
                    if ru else
                    "Years come from photograph EXIF data and archive names; those marked ≈ were "
                    "reconstructed indirectly. The period under each title was derived by matching "
                    "those dates against the careers — an inference, not a first-hand fact. Images "
                    "from before 2007 are scans of prints and web graphics of the period."
                ),
            },
            {
                "type": "cta",
                "title": "Эта линия продолжается" if ru else "The line continues",
                "text": (
                    "Всё, что 7pro8 выпускает сегодня в серии, выросло из работ на этой странице."
                    if ru else
                    "Everything 7pro8 builds in series today grew out of the work on this page."
                ),
                "actions": [
                    {"label": "О компании" if ru else "About the company", "href": f"{p}/company/"},
                    {"label": "Проекты" if ru else "Projects", "href": f"{p}/portfolio/"},
                ],
            },
        ],
    }


def main():
    for lang in ("en", "ru"):
        path = CONTENT / f"{lang}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["pages"] = [pg for pg in data["pages"] if pg["slug"] not in ("founder", "founders")]
        idx = next(i for i, pg in enumerate(data["pages"]) if pg["slug"] == "contact")
        data["pages"].insert(idx, page(lang))

        pre = "/ru" if lang == "ru" else ""
        company = next(pg for pg in data["pages"] if pg["slug"] == "company")
        for block in company["blocks"]:
            if block["type"] == "cta":
                block["actions"] = [a for a in block["actions"]
                                    if not a["href"].endswith(("/founder/", "/founders/"))]
                block["actions"].insert(0, {
                    "label": "Основатели" if lang == "ru" else "The founders",
                    "href": f"{pre}/founders/",
                })

        # navigation
        data["nav"] = [n for n in data["nav"] if n["slug"] not in ("founder", "founders")]
        data["nav"].append({"slug": "founders", "label": "Основатели" if lang == "ru" else "Founders"})

        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  {lang}.json: founders page in place ({len(data['pages'])} pages)")


if __name__ == "__main__":
    main()
