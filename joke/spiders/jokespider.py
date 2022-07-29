# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector

from joke.items import JokeItem

class JokeSpider(Spider):
    name = 'joke'
    base_url = 'http://xiaohua.zol.com.cn'
    url = 'http://xiaohua.zol.com.cn/new/1.html'
    start_urls = ['http://xiaohua.zol.com.cn/new/1.html']

    meta = {
        #'dont_redirect': True,
        #'handle_httpstatus_list': [301,302,304]
    }

    def parse(self, response):
        selector = Selector(response)
        jokes = selector.xpath('//li[@class="article-summary"]')
        print("================================== page jokes length = ", len(jokes))
        nextPage = selector.xpath(
            '//div[@class="page"]/a[@class="page-next"]/@href').extract()

        print(nextPage)
        
        if len(jokes) > 0:
            for joke in jokes:
                titleList = joke.xpath('span[@class="article-title"]/a/@href').extract()
                if len(titleList) > 0:
                    yield Request(
                        str(self.base_url + str(titleList[0])), 
                        callback=self.parseContent
                    )
                else:
                    pass
        if len(nextPage) > 0:
            yield Request(str(self.base_url + str(nextPage[0])), callback=self.parse, meta=self.meta)

    def parseContent(self, response):
        selector = Selector(response)
        titles = selector.xpath('//h1[@class="article-title"]').extract()
        contents = selector.xpath('//div[@class="article-text"]').extract()

        title = ''
        
        if len(titles) > 0:
            title = str(titles[0]).replace('<h1 class="article-title">', '').replace('</h1>', '').strip()
        else:
            title = '无'
        
        if len(contents) == 0:
            return

        print(title)

        content = str(contents[0]).replace('<p>', '').replace('</p>', '').replace('<div class="article-text">', '').replace('</div>', '').replace('\t', '').replace('\n', '').replace('\r', '\n').strip()
        
        content = ''.join([s for s in content.splitlines(True) if s.strip()])

        print(content)

        item = JokeItem()
        item['title'] = title
        item['jokeInfo'] = content
        yield item

