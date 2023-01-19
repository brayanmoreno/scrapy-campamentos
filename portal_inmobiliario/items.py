# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArriendoItem(scrapy.Item):
    codigo = scrapy.Field()
    titulo = scrapy.Field()
    tipo_precio = scrapy.Field()
    precio = scrapy.Field()
    gastos_comunes = scrapy.Field()
    precio_m2 = scrapy.Field()
    direccion = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    superficie_total = scrapy.Field()
    superficie_util = scrapy.Field()
    ambientes = scrapy.Field()
    dormitorios = scrapy.Field()
    banos = scrapy.Field()
    habitantes_max = scrapy.Field()
    num_piso = scrapy.Field()
    requerimientos = scrapy.Field()




