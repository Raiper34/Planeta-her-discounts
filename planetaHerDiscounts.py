from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

from discountColors import DiscountColors

class PlanetaHerDiscounts:

    BASE_URL = 'https://www.planetaher.cz'
    BASE_URL_DISCOUNTS = '{baseUrl}/tag/action-discount'.format(baseUrl=BASE_URL)

    def __init__(self):
        self.pages = self.getPages()

    def getPages(self):
        response = urlopen(self.BASE_URL_DISCOUNTS)
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find('section', {'class': 'products__pages'}).findAll('a', {'class': 'paging__numbers__link'})
        return list(map(lambda link: link.get('href'), links))

    def getProducts(self):
        self.products = []
        for page in self.pages:
            response = urlopen('{baseUrl}/{page}'.format(baseUrl=self.BASE_URL, page=page))
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            productItems = soup.find_all("li", {"class": "products__item"})

            for item in productItems:
                priceOriginal = int(re.sub('[^0-9]', '', item.find('div', {'class': 'product-box__price product-box__price--old'}).find('span').contents[0]))
                priceDiscounted = int(re.sub('[^0-9]', '', item.find('div', {'class': 'product-box__price'}).find('strong').contents[0]))
                percentage = 100 - (priceDiscounted * 100 / priceOriginal)
                self.products.append({
                    'title': item.find('a').get('title'),
                    'priceOriginal': priceOriginal,
                    'priceDiscounted': priceDiscounted,
                    'percentage': percentage,
                    'url': '{baseUrl}{productUrl}'.format(baseUrl=self.BASE_URL, productUrl=item.find('a').get('href'))
                })
        self.products = sorted(self.products, key=lambda item: item['percentage'])
        return self.products

    def printProducts(self, threshold=50, highOnly=False):
        for product in self.products:
            productInfoString = '{title}: {priceDiscounted}({priceOriginal})CZK {percentage:.2f}% {url}'.format(
                title=product['title'],
                priceDiscounted=product['priceDiscounted'],
                priceOriginal=product['priceOriginal'],
                percentage=product['percentage'],
                url=product['url']
            )
            if product['percentage'] > threshold:
                print('{colorStart}{productInfoString}{colorEnd}'.format(colorStart=DiscountColors.START_HIGH, productInfoString=productInfoString, colorEnd=DiscountColors.END))
            else:
                if not highOnly:
                    print(productInfoString)
