import scrapy
from portal_inmobiliario.items import ArriendoItem
from urllib.parse import urlparse
from urllib.parse import parse_qs

arriendo_keys = {
    'Superficie total': 'superficie_total',
    'Superficie útil': 'superficie_util',
    'Ambientes': 'ambientes',
    'Dormitorios': 'dormitorios',
    'Baños': 'banos',
    'Cantidad máxima de habitantes': 'habitantes_max',
    'Número de piso de la unidad': 'num_piso'
}

class PortalinmobiliarioSpider(scrapy.Spider):
    name = 'portalinmobiliario'

    def start_requests(self):
            urls = [
                'https://www.portalinmobiliario.com/arriendo/departamento',
            ]

            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        arriendo_link = response.xpath('//ol/li/div/div/a')
        yield from response.follow_all(arriendo_link, self.parse_arriendo)

        next_page_link = response.xpath('//div[@class="ui-search-pagination shops__pagination-content"]//a')
        yield from response.follow_all(next_page_link, self.parse)

    def get_contenedor_derecho(self, response, arriendo):
        arriendo['titulo'] = response.xpath('//h1/text()').get()
        arriendo['tipo_precio'] = response.xpath('div[2]/div/div/span/span[2]/text()').get()
        arriendo['precio'] = response.xpath('div[2]/div/div/span/span[3]/text()').get()
        arriendo['gastos_comunes'] = response.xpath('div[3]/p/text()').get()
        arriendo['precio_m2'] = response.xpath('//div[@id="price_comparison"]/div/div[last()]/div/p[last()]/text()').get()
        arriendo['codigo'] = response.xpath('//div[@id="seller_profile"]//p/text()').get()

    def get_lat_lon_url(self, url):
        parsed_url = urlparse(url)
        lat, lon = parse_qs(parsed_url.query)['center'][0].split(',')
        return lat, lon

    def get_contenedor_izquierdo(self,response , arriendo):
        arriendo['direccion'] = response.xpath('//div[@id="location"]//p/text()').get()
        arriendo['lat'], arriendo['lon'] = self.get_lat_lon_url(response.xpath('//div[@id="location"]//img/@src').get())

        info_especifica = response.xpath('//div[@id="technical_specifications"]//tr')
        for datos in info_especifica:
            key = datos.xpath('th/text()').get()
            if key in arriendo_keys:
                arriendo[arriendo_keys[key]] = datos.xpath('td/span/text()').get()
        
        arriendo['requerimientos'] = response.xpath('//div[@id="long_term_rental_requirements"]/div/div/div/div/div/div/span/text()').getall()

    def parse_arriendo(self, response):
        arriendo = ArriendoItem()
        self.get_contenedor_derecho(
            response.xpath('//div[@class="ui-pdp-container__row ui-pdp-component-list"]/div'), 
            arriendo
        )

        self.get_contenedor_izquierdo(
            response.xpath('//div[@class="ui-pdp-container__col col-2 ui-pdp-container--column-left pb-40"]'),
            arriendo
        )
        
        yield arriendo

        