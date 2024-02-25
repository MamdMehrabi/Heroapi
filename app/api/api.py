import re
import html
import requests
import json
import faker
import urllib.parse
import langdetect

from os.path import abspath
from random import randint
from jalali.Jalalian import jdate
from bs4 import BeautifulSoup


class HeroAPI():

    def __init__(
            self,
            url: str = 't.me/Heroapi',
            developer: str = 'amirali irvany',
            github: str = 'https://github.com/metect/Heroapi'
    ) -> dict:
        self.url: str = url
        self.github: str = github
        self.developer: str = developer

    async def execute(
            self,
            status: bool = True,
            developer: str = None,
            err_message: str = None,
            note: str = None,
            data: dict = None,
    ) -> dict:
        developer = self.developer if developer == None else self.developer
        __dict: dict = {
            'status': status,
            'dev': developer,
            'url': self.url,
            'github': self.github,
            'result': {
                'out': data,
                'note': note,
                'err_message': err_message,
            }
        }
        return __dict

    async def main_app(self):
        return await self.execute(
            status=True,
            developer='amirali irvany',
        )


    async def rubino(self, auth: str, url: str, timeout: float = 10) -> dict:
        payload: dict = {
            'api_version': '0',
            'auth': auth,
            'client': {
                'app_name': 'Main',
                'app_version': '3.0.1',
                'package': 'app.rubino.main',
                'lang_code': 'en',
                'platform': 'PWA'
            },
            'data': {
                'share_link': url.split('/')[-1],
                'profile_id': None
            },
            'method': 'getPostByShareLink'
        }
        session = requests.session()
        base_url: str = f'https://rubino{randint(1, 20)}.iranlms.ir/'
        responce = session.request(
            method='get', url=base_url, json=payload
        )
        return await self.execute(data=responce.json())


    async def font_generate(self, text: str = 'Heroapi') -> dict:
        prefix = re.sub(pattern='api.py', repl='f.json', string=abspath(__file__))
        with open(prefix, 'r') as f:
            fonts = json.load(f)

        converted_text = ''
        for count in range(0, len(fonts)):
            for char in text:
                if char.isalpha():
                    char_index = ord(char.lower()) - 97
                    converted_text += fonts[str(count)][char_index]
                else:
                    converted_text += char

            converted_text += '\n'
            result = converted_text.split('\n')[0:-1]

        return await self.execute(
            data=result, note='Currently only English language is supported'
        )


    async def lang(self, text: str) -> dict:
        try:
            return await self.execute(data=langdetect.detect(text))
        except langdetect.LangDetectException:
            return await self.execute(
                status=False,
                err_message='The value of the `text` parameter is not invalid'
            )


    async def translator(self, text: str, to_lang: str = 'auto', from_lang: str = 'auto') -> dict:
        session = requests.session()
        base_url: str = 'https://translate.google.com'
        url: str = f'{base_url}/m?tl={to_lang}&sl={from_lang}&q={urllib.parse.quote(text)}'
        r = session.request(
            method='get', url=url, headers={
                'User-Agent':
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
            }
        )

        if r.status_code == 200:
            result = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', r.text)
            return await self.execute(
                data=html.unescape(result[0])
            )
        else:
            return await self.execute(
                status=False,
                data='A problem has occurred on our end'
            )


    async def _faketext(self, count: int = 100, lang: str = 'en_US') -> dict:
        if count >= 999:
            return await self.execute(
                status=False,
                err_message='The amount is too big. Send a smaller number `count`'
            )
        else:
            return await self.execute(
                data=faker.Faker([lang]).text(count)
            )


    async def date_time(self) -> dict:
        return await self.execute(
            data=jdate(result_format='H:i:s ,Y/n/j')
        )


    async def usd(self):
        r = requests.get(
            'https://www.tgju.org/currency'
        )
        soup = BeautifulSoup(r.text, 'html.parser')
        html = soup.find_all(
            'span', {
                'class': 'info-price'
            }
        )
        __make = lambda index, x: re.findall(r'.*\">(.*)<\/', string=str(html[index]))[x]
        return await self.execute(
            data={
                'exchange': __make(0, 0),
                'shekel_gold': __make(2, 0),
                'gold18': __make(3, 0),
                'dollar': __make(5, 0),
                'euro': __make(6, 0),
                'Brent_oil': __make(7, 0),
                'bitcoin': __make(8, 0)
            }
        )
