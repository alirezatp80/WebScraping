from bs4 import BeautifulSoup
import requests
import csv

class Database:
    def __init__(self , filename):
         self.name = filename
         
    def Save_data(self,data):
        with open(f'{self.name}.csv' , 'w' , encoding='utf-8' , newline='') as file:
            writer = csv.DictWriter(file , fieldnames=['rank' , 'name', 'industry', 'revenue', 'employees', 'headquarters'])
            writer.writeheader()
            writer.writerows([company.to_dict() for company in data])


class Company:
    list_companies = []
        
    def add_company(self,rank , name , industry , revenue , employees , headquarters):
        new_company = Company()
        new_company.rank = rank
        new_company.name = name 
        new_company.industry = industry
        new_company.revenue = revenue
        new_company.employees = employees
        new_company.headquarters = headquarters
        Company.list_companies.append(new_company)
    
    def __str__(self):
        return f'''
    rank = {self.rank}
    name = {self.name}
    industry = {self.industry}
    revenue = {self.revenue} millions $
    employees = {self.employees}
    headquarters = {self.headquarters}
    '''
    
    def to_dict(self):
        return  {
                    'rank':self.rank,
                    'name':self.name,
                    'industry':self.industry,
                    'revenue' :self.revenue,
                    'employees':self.employees,
                    'headquarters':self.headquarters
                }
            
        
    def get_ten_best_rank(self):
            ten_best =([(company) for company in Company.list_companies if int(company.rank)<=10])
            return ten_best
    def get_teb_best_employees(self):
        ten_best = sorted(Company.list_companies , key=lambda company:int(company.employees),reverse=True)[:10]
        return  ten_best
    def get_all_large_companies(self):
        return Company.list_companies
            
    
class Scraper:
    def __init__(self , url):
        self.url = url
        self.data = []
        
    def scrap(self):
        headers = {
            
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers)
        
        soup = BeautifulSoup(response.content , 'html.parser')
       
        table = soup.select('table.wikitable.sortable ')[1]
        tbody = table.select_one('tbody')
        self.raw_data = tbody.select('tr')[1:]
        
    def parse(self):
        for  every in (self.raw_data):
            
                company = every.select('td')
                rank  = str(company[0].text).strip()
                name = str(company[2].text).strip()
                industry = str(company[3].text).strip()
                revenue = str(company[4].text).strip()  
                employees = str(company[6].text).strip().replace(',','')
                headquarters = str(company[7].text).strip()
                self.data.append({
                    'rank':rank,
                    'name':name,
                    'industry':industry,
                    'revenue' :revenue,
                    'employees':employees,
                    'headquarters':headquarters
                })  
        
    def get_companies(self):
        return self.data
        
        
def main():
            
    scrap = Scraper('https://en.wikipedia.org/wiki/List_of_largest_German_companies')
    scrap.scrap()
    scrap.parse()
    companies = scrap.get_companies()
    my_companies = Company()
    for company in companies:
        
        rank = company.get('rank')
        name = company.get('name')
        industry = company.get('industry')
        revenue = company.get('revenue')
        employees = company.get('employees')
        headquarters = company.get('headquarters')
        
        my_companies.add_company(rank , name , industry,revenue,employees,headquarters)
        
    database = Database('best_number_employees')
    database.Save_data(my_companies.get_all_large_companies())


if __name__ == "__main__":
    main()