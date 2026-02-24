class Book:
    def __init__(self , name , photo_url , author , year , page_number , description ):
        self.name = name
        self.photo_url = photo_url 
        self.author = author
        self.year = year
        self.page_number = page_number
        self.description = description

class History_book(Book):
    
    def __init__(self, name, photo_url, author, year, page_number, description,url):
        super().__init__(name, photo_url, author, year, page_number, description)
        self.url = url

class Tech_book(Book):
    def __init__(self, name, photo_url, author, year, page_number, description , url):
        super().__init__(name, photo_url, author, year, page_number, description)
        self.url = url
        
