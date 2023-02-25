from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
from tqdm import tqdm
import logging


# import requests_html
# from requests_html import HTMLSession
# import bs4
# import typing
# # import requests

# import json
# import requests
# from tqdm.notebook import trange


class Scrapper:
    img_links = []

    def __init__(self):
        self.session = HTMLSession()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (windows NT 10.0; Win64; x64; rv: 87.0)'
        self.response = None

    def scrap_olx(self, url):
        response = self.session.get(url)
        logging.debug(f"status code {response.status_code}")
        self.response = response

        title_l = self.get_text_data('//h1[@class="css-1soizd2 er34gjf0"]')
        price_l = self.get_text_data('//h3[@class="css-ddweki er34gjf0"]')
        house_prop_l = self.get_text_data('//li[@class="css-1r0si1e"]/p[@class="css-b5m1rv er34gjf0"]')
        description__intro_word_l = self.get_text_data('//h3[@class="css-dirtch er34gjf0"]')
        description_l = self.get_text_data('//div[@class="css-bgzo2k er34gjf0"]')
        title = title_l[0]
        price = price_l[0]
        house_prop = house_prop_l
        description_intro_word = description__intro_word_l[0]
        description = description_l[0]
        self.get_images()
        content = {'title': title,
                   'price': price,
                   'address': " \"назва вулиці\"",  # TODO use actual address
                   'properties': house_prop,
                   'description_intro_word': description_intro_word,
                   'description': description,
                   'img_links': self.img_links
                   }
        return content

    def get_text_data(self, path):
        values = self.response.html.xpath(path)
        texts = []
        for v in values:
            texts.append(v.text)
        return texts

    def get_images(self):
        # todo dont save but use only list of links
        soup = BeautifulSoup(self.response.content, 'html.parser')
        imgs = soup.find_all('img')
        img_links = []
        for i in tqdm(range(len(imgs))):
            image_link = imgs[i].attrs.get('src')
            if image_link is None:
                image_link = imgs[i].attrs.get('data-src')
            # filter only pictures taht contains pictures of house
            if not 'http' in image_link or 'resizer' in image_link:
                continue
            img_links.append(image_link)
        self.img_links = img_links

    def download_images(self):
        for link in self.img_links:
            image = self.session.get(link).content
            m = re.search('files/(.+?)/image;', link)
            if m:
                file_name = m.group(1)
                with open(f'pictures/{file_name}.jpg', 'wb') as file:
                    file.write(image)
        logging.debug('Downloaded images to pictures')

