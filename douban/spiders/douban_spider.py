# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名 不能和项目名称重复
    name = "douban_spider"
    # 允许的域名
    allowed_domains = ["movie.douban.com"]
    # 入口url 扔到调度器里面去
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in movie_list:
            douban_item = DoubanItem()
            # 进一步解析xpath，获取到具体的内容
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()  # . 在当前xpath解析规则下进一步细分
            douban_item['movie_name'] = i_item.xpath(".//div[@class='info']//div[@class='hd']/a/span[1]/text()").extract_first()
            content = i_item.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            # 遇到多行，需要对数据进行处理
            for i_content in content:
                content_s = "".join(i_content.split())
            douban_item['introduce'] = content_s
            print(content_s)
            douban_item['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()
            # 将数据yield到pipelines里面去，进行存储及清洗相关的操作
            yield douban_item
        # 解析下一页规则，取后一页的xpath
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link,callback=self.parse)