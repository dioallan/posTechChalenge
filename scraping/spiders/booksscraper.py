import scrapy
import requests
from scrapy.http import Request
from scraping.models.items import scrapingItem
import re


class BooksscraperSpider(scrapy.Spider):
    name = "booksscraper"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        BASE_URL = "https://books.toscrape.com/"
        book_urls = response.xpath(
            '//article[@class="product_pod"]/h3/a/@href').extract()
        for book_url in book_urls:
            full_url = response.urljoin(book_url)
            print(full_url)
            yield Request(full_url, callback=self.parse_book)
        try:
            next_page = response.xpath(
                '//li[@class="next"]/a/@href').extract_first()
            if next_page:
                yield response.follow(next_page, self.parse)
        except Exception as e:
            self.logger.error(f"Error while parsing next page: {e}")
        pass

    def parse_book(self, response):
        # Extraindo a url da imagem
        image_url = response.xpath(
            '//div[@class="item active"]/img/@src').extract_first()
        if image_url:
            image_url = response.urljoin(image_url)
        else:
            image_url = ""

        # Extraindo o Titulo do livro e convertendo para string
        title = str(response.xpath(
            '//h1/text()').get() or "")

        # Extraindo o preço sem taxa e convertendo para float
        price_without_tax = response.xpath(
            '//th[contains(text(), "Price (excl. tax)")]/following-sibling::td/text()').extract_first()
        if price_without_tax:
            price_without_tax = float(
                price_without_tax.replace('£', '').strip())
        else:
            price_without_tax = 0.0

        # Extraindo o preço com taxa e convertendo para float
        price_with_tax = response.xpath(
            '//th[contains(text(), "Price (incl. tax)") ]/following-sibling::td/text()').extract_first()
        if price_with_tax:
            price_with_tax = float(price_with_tax.replace('£', '').strip())
        else:
            price_with_tax = 0.0

        # Extraindo a disponibilidade pegando da String somente o valor e convertendo para inteiro
        availability = response.xpath(
            '//th[contains(text(), "Availability")]/following-sibling::td/text()').extract_first()
        if availability:
            match = re.search(r'\((\d+)\s+available\)', availability)
            if match:
                availability = int(match.group(1))
            else:
                availability = 0  # ou None, se preferir
        else:
            availability = 0  # ou None

        # Extraindo a categoria do livro e convertendo para string
        category = (response.xpath(
            '//ul[@class="breadcrumb"]/li[3]/a/text()').get() or "").strip()

        # Extraindo a classificação em Estrelas do livro e salvando como número
        rating_class = response.xpath(
            '//p[contains(@class, "star-rating")]/@class').get()
        rating_number = 0
        if rating_class:
            match = re.search(r'star-rating (\w+)', rating_class)
            if match:
                rating = match.group(1)
                rating_map = {
                    'One': 1,
                    'Two': 2,
                    'Three': 3,
                    'Four': 4,
                    'Five': 5
                }
                rating_number = int(rating_map.get(rating, 0))

        item = scrapingItem(
            titulo=title,
            preco_sem_taxa=price_without_tax,
            preco_com_taxa=price_with_tax,
            rating=rating_number,
            disponibilidade=availability,
            categoria=category,
            url_imagem=image_url,
        )

        yield item
