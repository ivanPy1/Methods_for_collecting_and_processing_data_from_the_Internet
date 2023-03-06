import scrapy
from itemloaders.processors import Compose, TakeFirst

import datetime

# очистка имени автора
def clean_author(value):
    try:
        value = value[0].replace('\n    ', '')
    except:
        return value
    return value

# преобразование даты рождения
def clean_date_born(value):
    try:
        list_months = ['January',
                       'February',
                       'March',
                       'April',
                       'May',
                       'June',
                       'July',
                       'August',
                       'September',
                       'October',
                       'November',
                       'December']

        for month in list_months:
            if month in value:
                value = value[0].replce(month, list_months.index(month) + 1)
        value = datetime.date(value)

    except:
        return value
    return value


# очистка описания
def clean_description(value):
    try:
        value = value[0].replace('\n', '').replace('        ', '')
        value = value[0].replace('    \n', '').replace('    ', '')
    except:
        return value
    return value


class QuotesToscrapeComItem(scrapy.Item):
    _id = scrapy.Field()
    author = scrapy.Field(input_processor=Compose(clean_author), output_processor=TakeFirst())
    date_born = scrapy.Field(input_processor=Compose(clean_date_born), output_processor=TakeFirst())
    description = scrapy.Field(input_processor=Compose(clean_description), output_processor=TakeFirst())
    author_page = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
