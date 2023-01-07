# Utilized resources
# https://github.com/YogurtTheHorse/ulauncher-translator
# https://github.com/mouuff/mtranslate
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
import textwrap
import sys
import re

if (sys.version_info[0] < 3):
    import urllib2
    import urllib
    import HTMLParser
else:
    import html
    import urllib.request
    import urllib.parse

agent = {'User-Agent': "Mozilla/5.0 (Android 9; Mobile; rv:67.0.3) Gecko/67.0.3 Firefox/67.0.3"}


def unescape(text):
    if (sys.version_info[0] < 3):
        parser = HTMLParser.HTMLParser()
    else:
        parser = html
    return (parser.unescape(text))


def translate(to_translate, to_language="auto", from_language="auto", wrap_len="80"):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    data = {'i': to_translate,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTIME',
            'typoResult': 'false'}
    # 将需要post的内容，以字典的形式记录在data内。
    r = requests.post(url, data=data)
    # post需要输入两个参数，一个url，一个是data，返回的是一个Response对象
    answer = r.json()
    result = answer['translateResult'][0][0]['tgt']
    return result;



class TranslateExtension(Extension):
    def __init__(self):
        super(TranslateExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or str()
        
        if len(query.strip()) == 0:
            return RenderResultListAction([
                ExtensionResultItem(icon='images/icon.png',
                                    name='No input',
                                    on_enter=HideWindowAction())
            ])
        
        if len(query)>3 and ":" in query[0]:
            from_language = "auto"
            to_language = query[1:3]
            query = query[3:]
        elif len(query)>5 and ":" in query[2]:
            from_language = query[:2]
            to_language = query[3:5]
            query = query[5:]
        else:
            from_language = extension.preferences["otherlang"]
            to_language = extension.preferences["mainlang"]
        ceviri = translate(query, to_language, from_language, extension.preferences["wrap"])
        
        items = [
            ExtensionResultItem(icon='images/icon.png',
                                name=query.replace("\n",""),
                                description=translate(query, to_language, from_language, extension.preferences["wrap"]),
                                on_enter=CopyToClipboardAction(ceviri))
        ]

        return RenderResultListAction(items)


if __name__ == '__main__':
    TranslateExtension().run()
