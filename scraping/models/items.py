# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class scrapingItem(scrapy.Item):
    titulo = scrapy.Field()
    preco_com_taxa = scrapy.Field()
    preco_sem_taxa = scrapy.Field()
    rating = scrapy.Field()
    disponibilidade = scrapy.Field()
    categoria = scrapy.Field()
    url_imagem = scrapy.Field()


pass
