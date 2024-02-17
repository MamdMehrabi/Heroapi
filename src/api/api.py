from myrino.client import Client
import langdetect
import faker
import json


def rubino(url: str, timeout: float = 10) -> dict:
    '''This method is used to get the download link
    and other information of the post(s) in Rubino Messenger
    :param url:
        The link of the desired post
    :param timeout:
        Optional To manage slow timeout when the server is slow
    :return:
        Full post information

    Powered by the myrino library. github > github.com/metect/myrino
    '''
    cliant = Client('rnd', timeout=timeout)
    return cliant.get_post_by_share_link(share_link=url)


def font(text: str = 'ohmyapi') -> dict:
    '''This function is for generating fonts. Currently only English language is supported
    :param text:
        The text you want the font to be applied to
    '''

    # opening `f.json` to read the source fonts from it
    with open('.f.json', 'r') as f:
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

    return result


def lang(text: str) -> str:
    '''This function is to identify the language of a text
    :param text:
        Your desired text
    :return:
        example: `en` or `fa`
    '''
    return langdetect.detect(text)


def faker_data(content: str = 'text', count: int = 10, lang: str = 'en_US') -> list:
    '''This api is used to generate fake content.
    :param content:
        Type of content. example > `text` or `name`
    :param count:
        Number of contents. example > 10 or 50
    :param lang:
        desired language. example > `en_US` or `fa_IR`
        !NOTE: Uppercase and lowercase letters are sensitive
    :return:
        Fake data as a list
    '''
    data: list = []
    fake: classmethod = faker.Faker(lang.split())
    if content == 'text': return fake.text()
    elif content == 'name':
        for _ in range(0, len(count)):
            data.append(fake.name())

        return data


    elif content == 'data':
        for _ in range(0, len(count)):
            data.append(fake.data())

        return data


    elif content == 'emoji':
        for _ in range(0, len(count)):
            data.append(fake.emoji())

        return data


    elif content == 'ip':
        for _ in range(0, len(count)):
            data.append(fake.ipv4())

        return data