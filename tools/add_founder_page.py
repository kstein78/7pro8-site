#!/usr/bin/env python3
"""One-off: insert the founder page into content/ru.json and content/en.json.

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


def entry(year, title, role, body, slug, images, cols=3):
    e = {"year": year, "title": title, "role": role, "body": body}
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


def page(lang):
    p = "" if lang == "en" else "/ru"
    ru = lang == "ru"
    return {
        "slug": "founder",
        "title": "Илья Большаков" if ru else "Iliya Bolshakov",
        "title_tag": ("Илья Большаков — основатель 7pro8" if ru
                      else "Iliya Bolshakov — founder of 7pro8"),
        "description": (
            "Хронология работ Ильи Большакова, основателя 7pro8: от гаражных проектов конца "
            "1990-х и салонов суперкаров до первой перегородки на Mercedes-Benz W221 в 2007 году."
            if ru else
            "A chronology of the work of Iliya Bolshakov, founder of 7pro8: from garage projects in "
            "the late 1990s and supercar interiors to the first Mercedes-Benz W221 partition in 2007."
        ),
        "blocks": [
            {
                "type": "pagehead",
                "kicker": "Основатель" if ru else "Founder",
                "title": "Илья Большаков" if ru else "Iliya Bolshakov",
                "lead": (
                    "ЧЕРНОВИК ВВОДНОГО АБЗАЦА. Двадцать пять лет работы руками и головой в одном и "
                    "том же ремесле: интерьер автомобиля как инженерная задача, а не как украшение."
                    if ru else
                    "DRAFT INTRODUCTION. Twenty-five years of hands-on work in one craft: the interior "
                    "of a car as an engineering problem rather than as decoration."
                ),
                "meta": [
                    {"label": "В профессии с" if ru else "In the trade since", "value": "≈1999"},
                    {"label": "Первая перегородка" if ru else "First partition", "value": "2007"},
                    {"label": "Проектов ниже" if ru else "Projects below", "value": "12"},
                ],
            },
            {
                "type": "note",
                "title": "Черновик страницы" if ru else "Draft page",
                "body": [
                    "Все тексты на этой странице — заготовки. Фотографии и порядок расставлены по "
                    "датам файлов и по названиям архивов; годы со знаком ≈ подтверждения требуют. "
                    "Этот блок удаляется одной строкой в content-файле."
                    if ru else
                    "Every text on this page is a placeholder. The photographs and their order come "
                    "from file dates and archive names; years marked ≈ still need confirming. This "
                    "block is one line to delete in the content file."
                ],
            },
            {
                "type": "split",
                "tone": "paper",
                "title": "Как это началось" if ru else "How it started",
                "body": [
                    "ЧЕРНОВИК. Здесь — короткая биография: откуда пришёл, чему учился, как гараж "
                    "превратился в производство и почему в итоге всё сошлось на перегородках."
                    if ru else
                    "DRAFT. A short biography goes here: where he came from, what he trained in, how "
                    "a garage became a production shop, and why it all ended up converging on "
                    "partitions.",
                    "ЧЕРНОВИК. Второй абзац — про подход к работе. Один-два конкретных примера "
                    "лучше любых определений."
                    if ru else
                    "DRAFT. A second paragraph on how he works. One or two concrete examples beat any "
                    "amount of description.",
                ],
                "image": {
                    "src": "founder/portrait.jpg",
                    "alt": "Портрет Ильи Большакова" if ru else "Portrait of Iliya Bolshakov",
                    "caption": "МЕСТО ПОД ПОРТРЕТ — нужна фотография" if ru else "PORTRAIT SLOT — photograph needed",
                },
            },
            {
                "type": "chronicle",
                "title": "Работы, от новых к старым" if ru else "The work, newest first",
                "lead": (
                    "Двенадцать проектов за двадцать с лишним лет. Порядок обратный: сегодняшнее "
                    "сверху, начало внизу."
                    if ru else
                    "Twelve projects across more than twenty years, in reverse order: the present at "
                    "the top, the beginning at the bottom."
                ),
                "entries": RU_ENTRIES if ru else EN_ENTRIES,
                "footnote": (
                    "Годы взяты из EXIF-данных снимков и названий архивов. Отмеченные знаком ≈ "
                    "восстановлены по косвенным признакам и требуют подтверждения. Снимки до "
                    "2007 года — сканы плёночных отпечатков и веб-графика того времени, отсюда их "
                    "разрешение."
                    if ru else
                    "Years come from photograph EXIF data and archive names. Those marked ≈ were "
                    "reconstructed indirectly and need confirming. Images from before 2007 are scans "
                    "of film prints and web graphics of the period, hence their resolution."
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
        data["pages"] = [p for p in data["pages"] if p["slug"] != "founder"]
        idx = next(i for i, p in enumerate(data["pages"]) if p["slug"] == "contact")
        data["pages"].insert(idx, page(lang))

        # and a way in, from the company page
        company = next(p for p in data["pages"] if p["slug"] == "company")
        for block in company["blocks"]:
            if block["type"] == "cta":
                label = "Основатель компании" if lang == "ru" else "The founder"
                href = ("/ru" if lang == "ru" else "") + "/founder/"
                block["actions"] = [a for a in block["actions"] if a["href"] != href]
                block["actions"].insert(0, {"label": label, "href": href})

        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  {lang}.json: founder page inserted ({len(data['pages'])} pages)")


if __name__ == "__main__":
    main()
