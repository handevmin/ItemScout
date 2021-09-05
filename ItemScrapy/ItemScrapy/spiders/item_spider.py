import json
import requests
import scrapy
from requests import request

class ItemSpider(scrapy.Spider):
    name = "item"
    page_number = 2
    keyword = "마스크"
    items = {}

    data = {
        "rankType": "rankUp",
        "pageNum": "1",
        "listNum": "60",
        "searchType": "all",
        "searchKeyword": keyword,
        "mode": "list",
        "reCaptcha": "03AGdBq26ONJYZDweXXGJ9q2-PKAqylOOuOKqfyHPH6IAbiRlSKXwxNYVWVV48K9F2wagIruG3x4X8eywpErAA3IDmyHTuNkRjFk5R3yeS65UIzAOH1P4qGS6BgYJjAx4fJOhWhjavMs8qVgI-vHs3ZXIdn0aL5lsNsazT7iSfRtTkO1BE2Z0lfg43KcKYS5Xx1FbONug_MIezniKOqUenAbHsnkNWcEk1UE5IYHJEwoY19RrhEB0Uefyjg6yoy0qaSp5uYeG9MPOoMfwj6ERi9gLMy5rdl6BONlNU19PdZ1KtIJwt8J6wfumJIgp-6TaBABuXtLg2rFFC1oq19hiszSDaTpeMI_ElZg9fMVNOqVRQsMTlOQj8tG6b83PnBE0aDKbOkvccnRbKSufGggAIuyzaR7_NWGlMor8HNGrzJrx8CUbnHqkbAYhXzy6e13txn935yJsmMRSl",
    }

    def start_requests(self):
        yield scrapy.Request(url='https://www.onch3.co.kr/idx_search_main.php?sear_txt='+self.keyword, callback=self.parse)


    def parse(self, response):
        # 온채널
        #items = ItemscrapyItem()
        items_list = response.css('ul.prd_list > li')

        for item in items_list:
            self.items['title'] = item.css('.prd_name::attr(title)').get()
            self.items['link'] = item.css('.btn_sale a::attr(href)').get()
            self.items['price'] = item.css('.prd_price::text').get()
            self.items['img'] = item.css('.prd_img .img_sale_prd::attr(src)').get()
            yield self.items
        next_page = 'https://www.onch3.co.kr/idx_search_main.php?page='+str(ItemSpider.page_number)+'&sear_txt=%EB%A7%88%EC%8A%A4%ED%81%AC&type=&catef=&cates=&catet='
        # if ItemSpider.page_number <= 53:
        #     ItemSpider.page_number +=1
        #     yield response.follow(next_page, callback= self.parse)

        # 오너클린
        base_url = 'https://ownerclan.com/V2/_ajax/getProductList.php'
        r = request('post', base_url, data=self.data)
        json_object = json.loads(r.text)
        for i in json_object['productList']:
            self.items['title'] = i['productname']
            self.items['link'] = i['selfcode']
            self.items['price'] = i['sellprice']
            self.items['img'] = i['image']
            yield self.items

        # 도매꾹
        url = 'https://domeggook.com/ssl/api/'

        # Setting Request Parameters
        param = dict()
        param['ver'] = '4.0'
        param['mode'] = 'getItemList'
        param['aid'] = '92c50b182ecd3d3ca86d14d87b554e62'
        param['market'] = 'dome'
        param['om'] = 'json'
        param['kw'] = self.keyword # 검색어

        # Getting API Response
        res = requests.get(url, params=param)

        # Parsing
        data = json.loads(res.content)
        print(data['domeggook']['list']['item'])
