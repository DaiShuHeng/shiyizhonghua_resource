import scrapy

from ShiYiZhonHua.items import ShiyizhonhuaItem


class ShiyizhonhuaSpiderSpider(scrapy.Spider):
    name = 'ShiYiZhonHua_spider'
    allowed_domains = ['gushiwen.cn']
    start_urls = ['https://so.gushiwen.cn/shiwens/default.aspx?cstr=%e9%ad%8f%e6%99%8b']

    def parse(self, response):
        items = response.css('#leftZhankai .sons')
        for item in items:
            title = item.css('b::text').get()
            author = item.css('.source a:first-child::text').get()
            time = item.css('.source a:last-child::text').get()
            content = item.xpath('.//div[@class="contson"]//text()').getall()
            content = list(map(lambda s: s.replace('\n', ''), content))
            content = ''.join(list(filter(lambda s: s, content)))
            yield ShiyizhonhuaItem(
                title=title,
                author=author,
                time=time,
                content=content
            )

        next_url = response.css('.amore::attr(href)').get()
        true_url = response.urljoin(next_url)
        yield scrapy.Request(true_url, callback=self.parse)
