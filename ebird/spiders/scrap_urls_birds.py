import scrapy
import re
import bird_dictionary as bd

bird_list=bd.fill_birds('name')


class ScrapeBirdsSpider(scrapy.Spider):
    name= "birdscraper"
    allowed_domains=['ebird.org']
    def __init__(self):
        self.start_urls=[i.url() for i in bird_list]

    def start_requests(self):
        for i,url in enumerate(self.start_urls):
            print('---------------------------')
            print(i,'----',url)
            print('---------------------------')
            yield scrapy.Request(url=url,callback=self.parse,dont_filter=True,meta={"cookiejar":i})
    
    def get_audio(self,parsing_script_json):
        start=parsing_script_json.find('audioAssetsJson') 
        parsing_script_json=parsing_script_json[start:]
        parsing_script_json=parsing_script_json[parsing_script_json.find('assetId'):]
        parsing_script_json=parsing_script_json[:parsing_script_json.find(',')]
        parsing_script_json=parsing_script_json.replace('\n','').replace('\t','').replace(' ','') #parsing string
        return parsing_script_json

    def parse(self,response):
        image = response.css('img').xpath('@src').get()
        code = response.url[26:]
        common_name=response.xpath('//span[@class="Heading-main Media--hero-title"]//text()').get()
        scientific_name=response.xpath('//span[@class="Heading-sub Heading-sub--sci Heading-sub--custom u-text-4-loose"]//text()').get()
        description=response.xpath('//p[@class="u-stack-sm"]/text()').get()
        if description:
            description=description.split('\n',1)[0]
        #The data is in a Json var in a script and i cant use regex because structure vary from url
        parsing_script_json=response.xpath('//script[contains(.,"audioAssetsJson")]/text()').get()

        audio=self.get_audio(parsing_script_json)
        try:
            audio= re.findall('[0-9]+',audio)
            audio=int(audio[0])
            if (audio==0):
                audio=None
        except:
            audio=None

        yield {
            'code':code,
            'scientific_name':scientific_name,
            'common_name':common_name,
            'description':description,
            'image':image,
            'audio':audio,
            'url':response.url
        }
