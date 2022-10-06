import datetime as dt


class Record:
    # При такой реализации комментарий является обязательным, но обязательно ли?
    def __init__(self, amount, comment, date=''):
        self.amount = amount  # Здесь можно передать кол-во, но какого типа? USD? EUR?
        # При таком подходе возможно использовать кол-во для любого наследника.
        # Наверное стоит - либо конструировать класс на основе необходимого поля, либо использовать setter...
        # Либо применить применить паттерн композиция...
        self.date = (
            dt.datetime.now().date() if  # Вместо if else блока можно указать параметр по умолчанию в конструкторе.
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        # Надо известить пользователя о формате ввода, иначе возникнет TypeError.
        # Либо написать метод / функцию, для конвертации из всех возможных типов дат
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    # Будет логично добавить метод get_record.
    # И сделать оба метода приватными (https://docs.python.org/3/howto/descriptor.html).
    def add_record(self, record):
        self.records.append(record)  # Здесь вызывается встроенный метод списка (list) append...

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        # Может попробуем переопределить метод и вернуть строку ?
        # Взяв как пример метод get_today_cash_remained, например
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()  # Можно использовать само выражение, а не переменную
        for record in self.records:
            # В if блоке попробуйте упростить условие,
            # 7 в таком случае ведь < (today - record.date).days, а ноль меньше
            # оператор and кажется лишний. Получиться без него?
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        # Просто возвращаем объект?
        # Может попробуем переопределить метод и вернуть строку ?
        # Взяв как пример метод get_today_cash_remained, например
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()  # Переменную можно не объявлять, а пользоваться выражением
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')  # Скобки действительно нужны? Мы ведь возвращаем строку, а не tuple


class CashCalculator(Calculator):
    # Так же USD_RATE и EURO_RATE передаются в метод get_today_cash_remained,
    # их можно не объявлять, если их объявить в конструкторе (прим. self.USD_RATE)
    # Но каждый день курс валют может быть разным...
    # Надо либо использовать фиксированный курс, либо просто передавать в метод
    # Какой еще может быть вариант решения проблемы?
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # В этот метод передается валюта (currency),
    # Можно передавать каждый раз разную строку, и это вызовет неточности в расчетах.
    # К тому же не предусмотрен вариант, когда пользователь передает произвольную строку.
    # При таком варианте расчет можно вести и в бананах, но стоит ли?
    # Для финансовых вычислений рекомендуется использовать модуль decimal
    # Возможно, целесообразней будет использовать Enum (https://docs.python.org/3/library/enum.html)
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Стоит ли создавать еще одну переменную?
        # Ведь она указывает на тот же объект (currency)
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Что будет с кодом, если добавятся еще 5 валют?
        # Количество ветвлений в if ... elif увеличит код, он станет намного менее читабельным.
        # Вышеупомянутый, встроенный класс Enum может помочь решить и эту проблему
        # и сделать код компактней.
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00  # Строка никак не влияет на код...
            # Либо нужен отдельный курс для рубля и других валют СНГ
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # В одном месте используется format(), в другом f строки.
            # f строки быстрее, могут принимать выражения и даже объекты классов
            # (при наличии у последних метода __str__() ).
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        # Действительно необходимо вызывать метод родителя через super() ?
        # Названия методов ведь одинаковы...
        super().get_week_stats()
