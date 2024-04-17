from datetime import datetime
import scrapy
import json

class AreaSpider(scrapy.Spider):
    name = "area"
    allowed_domains = ["www.daftarperusahaan.com"]
    
    # ========================================================= add the desired link located at www.daftarperusahaan.com
    start_urls = [
        "https://www.daftarperusahaan.com/area/papua-barat"
    ]
    # =========================================================

    def parse(self, response):
        links = response.css('.node > h2 > a::attr(href)').getall()
        for link in links:
            yield response.follow(link, self.parse_company)
        
        next_page = response.css('#squeeze > div > div > div.clear-block > div.item-list > ul > li.pager-next > a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            
    def parse_company(self, response):
        url = response.url
        source = "daftarperusahaancom"
        domain = url.split('/')[2]
        company = response.css('.node > div.content.clear-block > strong::text').get()
        alamat = response.css('.node > div.content.clear-block > p::text').get()
        telp = response.css('.node > div.content.clear-block > div.field.field-type-text.field-field-telepon > div.field-items > div::text').get()
        
        if telp is not None:
            telp = telp.strip()
        
        fax = response.css('.node > div.content.clear-block > div.field.field-type-text.field-field-fax > div.field-items > div::text').get()
        
        if fax is not None:
            fax = fax.strip()
        
        keterangan = response.css('.node > div.content.clear-block > div.field.field-type-text.field-field-keterangan > div.field-items > div::text').get()
        
        if keterangan is not None:
            keterangan = keterangan.strip()
        
        bidang = response.css('.node > div:nth-child(2) > div > div.category > ul > li > a::text').get()
        area = response.css('.node > div:nth-child(2) > div > div.tags > ul > li > a::text').getall()
        crawling_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        crawling_epoch = int(datetime.now().timestamp())
        
        data = {
            'url': url,
            'source': source,
            'domain': domain,
            'crawling_time': crawling_time,
            'crawling_epoch': crawling_epoch,
            'company': company,
            'alamat': alamat,
            'telp': telp,
            'fax': fax,
            'keterangan': keterangan,
            'bidang': bidang,
            'area': area
        }
        
        folder = 'daftarperusahaan/json'
        file_name = f'{company.lower().replace(" ", "_")}_{crawling_epoch}.json'
        
        with open(f'{folder}/{file_name}', 'w') as outfile:
            json.dump(data, outfile)
