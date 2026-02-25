from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp
import json
def change_html_to_json(soup):
    result = dict()
    for index , tr in enumerate(soup):
        td = tr.select('td')
                  
        result[td[0].text] = td[1].text
    return result
    
class Book:
    def __init__(self , name , photo_url , author , year , page_number , description  ):
        self.name = name
        self.photo_url = photo_url 
        self.author = author
        self.year = year
        self.page_number = page_number
        self.description = description
    def __eq__(self, book:Book):
        if self.name == book.name:
            return True
    def to_dic(self):
        return {
            "name":self.name,
            "photo_url":self.photo_url,
            "author":self.author,
            "year":self.year,
            "page_number":self.page_number,
            "description":self.description
            
        }
    def __str__(self):
        return self.to_dic()

class BookRepository:
    def __init__(self ):
        self.books = []
    def add_book(self , book:Book):
        if book not in self.books:
            self.books.append(book)
    

        

class History_book(Book):
    
    def __init__(self, name, photo_url, author, year, page_number, description,url):
        super().__init__(name, photo_url, author, year, page_number, description)
        self.url = url

class Tech_book(Book):
    def __init__(self, name, photo_url, author, year, page_number, description , url):
        super().__init__(name, photo_url, author, year, page_number, description)
        self.url = url
        
class Scraper:
    def __init__(self , url):
        self.url = url
        self.books_url = []
        self.data = []
    #تابع اسکرپ همه و اسکرپ یک صفحه لینک صفحه کتاب هارا از سایت جمع آوری میکنه و داخل لینک کتاب ها قرار میده 
    #بعدش با استفاده از اونها اطلاعات همه کتاب هارو اسکرپ میکنیم
    def scrap_all(self):
        start_page = 1
        self.books_url.clear()
        while True:
            response = requests.get((self.url+f'/books/کتاب-تاریخی/page-{start_page}?sort=newest'))
            soup = BeautifulSoup(response.content , 'html.parser')
            a_tag_links = soup.select('h3.book-card-title a')
            print(f'page {start_page}')
            for a in a_tag_links:
              link = (self.url)+(a.get('href'))
              self.books_url.append(link)
            btn = soup.select_one('a.next-page')
            if btn:
                start_page+=1
            else:
                break
         
    def scrap_one_page(self , numberpage:int):
            response = requests.get((self.url+f'/books/کتاب-تاریخی/page-{numberpage}?sort=newest'))
            soup = BeautifulSoup(response.content , 'html.parser')
            a_tag_links = soup.select('h3.book-card-title a')
            self.books_url.clear()
            for a in a_tag_links:
              link = (self.url)+(a.get('href'))
              self.books_url.append(link)
    
    async def fetch(self , session , url):
        async with session.get(url) as response :
            html =  await response.text()
            soup = BeautifulSoup(html ,'html.parser')
            table = soup.select('div.book-details.section table tbody tr')
            description = str(soup.select_one('div#BookIntroduction p').text).strip()
            photo_link = soup.select_one('a.book-cover').get('href')
            author = soup.select_one('div.book-main-info-authors ul li a').text
            dic_info = (change_html_to_json((table)))
            print('proccessing...')
            return {
                'name':dic_info['نام کتاب'].strip(),
                'author':author,
                'year':int(dic_info['سال انتشار'].strip()),
                'page_number':int(dic_info['تعداد صفحات'].strip()),
                'description':description,
                'photo_link':photo_link
            }
    
    
    async def scrap_book_details(self):
            async with aiohttp.ClientSession() as session:
                tasks = [self.fetch(session,url) for url in self.books_url]
                result = await asyncio.gather(*tasks)
                self.data = (result)
                    
        
    sem = asyncio.Semaphore(40)
    
class Database:
    def __init__(self , filename , repo:BookRepository):
        self.filename = filename
        self.repo = repo
    def save(self):
        with open(f'{self.filename}.json' , 'w' , encoding='utf-8')as f:
            json.dump(self.repo , f , ensure_ascii=False , indent=4)
    def read(self):
        with open(f'{self.filename}.json' , 'r' , encoding='utf-8' ) as f:
          return  json.load(f)
    
    



    
