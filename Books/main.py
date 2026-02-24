class Book:
    def __init__(self , name , photo_url , author , year , page_number , description ):
        self.name = name
        self.photo_url = photo_url 
        self.author = author
        self.year = year
        self.page_number = page_number
        self.description = description
class BookRepository:
    def __init__(self ):
        self.books = []
    def add_book(self):
        pass
    def remove_book(self):
        pass
    def scrap_or_read(self):
        pass
        

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
        
    def scrap(self):
        pass
    def parse(self):
        pass
    
class Database:
    def __init__(self , filename):
        self.filename = filename
    def save(self):
        pass
    def read(self):
        pass