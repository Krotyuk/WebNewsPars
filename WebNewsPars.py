import urllib.request
import re
import sys

class ParseMyClass:
    def __init__(self, url):
        self.url = url
        self.file = '-'.join(self.url.split('/'))[8:]
        site = urllib.request.urlopen(self.url)
        html = str(site.read().decode('utf-8'))
        self.article = re.findall(r'<article[^>]*>(.*?)</article>', str(html), re.DOTALL)
        if len(self.article) == 0:
            self.article = re.findall(r'<div.*itemtype="http://schema.org/NewsArticle[^>]+?>(.*)</div>', str(html),
                                      re.DOTALL)
        self.razbor()
        self.save()

    def razbor(self):
        article = self.article

        # меняем ссылки
        article = re.sub(r'<[aA]\s{1}href=[\'\"](.*?)[\'\"][^>]*>(.*?)</[aA]>', r'[URL="\1"] \2 [/URL]', str(article))

        #		#Тут надо будет подумать, как получше это сделать
        #		#выбираем фотки
        #		article = re.sub(r'<img(.*?)alt=[\'\"](.*?)[\'\"](.*?)src=[\'\"](.*?)[\'\"](.*?)>', r'[IMG="\4"]\2[/IMG]', str(article))

        # удаляем различные теги для чистоты
        article = re.sub(r'<(section|script|aside|time).*?</\1>(?s)', '', str(article))
        article = re.sub(r'<div class="bordered-title">(.*)</div>', '', str(article))

        # удаляем лишние пробелы
        article = re.sub(r'\s+', ' ', str(article))

        # удаляем табуляцию
        article = re.sub(r'\t', r'\s', str(article))

        # выделяем заголовки
        article = re.sub(r'<[hH][^>]*>(.*?)</[hH][^>]*>', r'\1\r\n', str(article))

        # выделяем абзацы
        article = re.sub(r'<[pP][^>]*>(.*?)</[pP][^>]*>', r'\1\r\n', str(article))

        # удаляем все оставльные теги
        article = re.sub(r'<.*?>', '', str(article))

        # Выравниваем по 80 символов
        article.strip()
        list = article.split('\r\n')
        i = 0
        j = 79
        while i < len(list):
            if len(list[i]) > j:
                shag = 1
                k = j * shag
                nachalo_stroki = 0
                while 0 < k <= len(list[i]):
                    if ord(list[i][k]) != 32:
                        while list[i][k] is not None and list[i][k] != ' ' and list[i][
                            k] != '\n' and k > nachalo_stroki:
                            k = k - 1
                    if k == nachalo_stroki:
                        list[i] = list[i][:j + nachalo_stroki] + '\n' + list[i][j + nachalo_stroki:]
                    else:
                        list[i] = list[i][:k] + '\n' + list[i][k + 1:]
                    k = (j * shag) - k
                    shag = shag + 1
                    k = (j * shag) - k
                    nachalo_stroki = k - j
            i = i + 1
        article = str('\r\n'.join(list))
        self.article = article

    def save(self):
        fname = self.file + '.txt'
        print(fname)
        f = open(fname, 'w')
        f.write(str(self.article))
        f.close()


if len(sys.argv) > 1:
    parse = ParseMyClass(sys.argv[1])
else:
    url = input('Введите URL статьи ')
    if url is not None and len(url.strip()) > 0:
        parse = ParseMyClass(url)
