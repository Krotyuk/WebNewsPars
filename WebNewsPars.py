import urllib.request

import re
import sys
import chardet


class tensorParseTest:
    def __init__(self, url):
        self.url = url
        self.file = '-'.join(self.url.split('/'))[8:]
        site = urllib.request.urlopen(self.url)
        kodirovka = chardet.detect(urllib.request.urlopen(url).read())['encoding']
        html = str(site.read().decode(str(kodirovka)))

        self.article = re.findall(r'<article[^>]*>(.*?)</article>', str(html), re.DOTALL)
        if len(self.article) == 0:
            self.article = re.findall(r'<div.*itemtype="http://schema.org/NewsArticle[^>]+?>(.*)</div>', str(html),
                                      re.DOTALL)
        if 'gazeta' in url:
            self.article = re.findall(r'<p[^>]*>(.*?)</p>', str(html), re.DOTALL)
        self.reClean()
        self.saveFileTxt()

    # функция очистки контента
    def reClean(self):
        article = self.article

        # меняем ссылки на формат "[]"
        article = re.sub(r'<[aA]\s{1}href=[\'\"](.*?)[\'\"][^>]*>(.*?)</[aA]>', r'[URL="\1"] \2 [/URL]', str(article))

        # выделяем фотографии в ссылки
        article = re.sub(r'<img(.*?)alt=[\'\"](.*?)[\'\"](.*?)src=[\'\"](.*?)[\'\"](.*?)>', r'[IMG="\4"]\2[/IMG]', str(article))

        # убираем теги
        article = re.sub(r'<(section|script|aside|time).*?</\1>(?s)', '', str(article))
        article = re.sub(r'<div class="bordered-title">(.*)</div>', '', str(article))

        # убираем лишние пробелы
        article = re.sub(r'\s+', ' ', str(article))

        # убираем табуляцию
        article = re.sub(r'\t', r'\s', str(article))

        # выделяем заголовки
        article = re.sub(r'<[hH][^>]*>(.*?)</[hH][^>]*>', r'\1\r\n', str(article))

        # выделяем абзацы
        article = re.sub(r'<[pP][^>]*>(.*?)</[pP][^>]*>', r'\1\r\n\n', str(article))

        # удаляем все оставльные теги
        article = re.sub(r'<.*?>', '', str(article))

        # Выравниваем тест по формату "не больше 80 символов"
        article.strip()
        list = article.split('\r\n')
        i = 0
        j = 79
        while i < len(list):
            if len(list[i]) > j:
                shag = 1
                k = j * shag
                nachalo_stroki = 0
                while 0 < k <= len(list[i])-1:
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
    #сохранение в файл
    def saveFileTxt(self):
        fname = self.file + '.txt'
        print(fname)
        f = open(fname, 'w')
        f.write(str(self.article))
        f.close()


if len(sys.argv) > 1:
    parse = tensorParseTest(sys.argv[1])
else:
    url = input('Введите URL статьи ')
    if url is not None and len(url.strip()) > 0:
        parse = tensorParseTest(url)
