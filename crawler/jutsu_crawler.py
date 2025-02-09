import scrapy
from bs4 import BeautifulSoup

class JutsuCrawler(scrapy.Spider):
    name = 'narutospider'
    start_urls = ['https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu']

    def parse(self, response):
        for href in response.css('.smw-columnlist-container')[0].css('a::attr(href)').extract():
            extracted_data = scrapy.Request('https://naruto.fandom.com/'+href,
                           callback=self.parse_jutsu)  #the extracted data is a dict
            yield extracted_data

        for next_page in response.css('a.mw-nextlink'):
            yield response.follow(next_page, self.parse)

    def parse_jutsu(self, response):
        jutsu_name = response.css('span.mw-page-title-main::text').extract()[0]
        jutsu_name = jutsu_name.strip()

        div_selector = response.css('div.mw-parser-output')[0] #selecting the div with the jutsu description
        div_html = div_selector.extract() #extracting the html of the div

        soup = BeautifulSoup(div_html).find('div') #using BeautifulSoup to parse the html
        jutsu_type = ""

        if soup.find('aside'):
            aside = soup.find('aside')
            
            for cell in aside.find_all('div',{'class':'pi-data'}):
                if cell.find('h3'):
                    cell_name = cell.find('h3').text.strip()
                    if cell_name == 'Classification':
                        jutsu_type = cell.find('div').text.strip()

        soup.find('aside').decompose() #removing the aside tag from the html
        jutsu_description = soup.text.strip()
        jutsu_description = jutsu_description.split('Trivia')[0].strip() #removing the trivia section 
        #it will go select the trivia section we want whats before so we choose [0]

        return  dict(jutsu_name=jutsu_name, 
                     jutsu_type=jutsu_type, 
                     jutsu_description=jutsu_description)