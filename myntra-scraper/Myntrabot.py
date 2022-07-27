import requests
import math
import json
from multiprocessing import Pool
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float

engine = create_engine('sqlite:///myntra.db', echo=False)
meta = MetaData()

products_table = Table(
    'products', meta,
    Column('id', Integer, primary_key=True),
    Column('website', String),
    Column('link', String, unique=True),
    Column('name', String),
    Column('brand', String),
    Column('category', String),
    Column('sizes', String),
    Column('price', Float),
    Column('mrp', Float),
    Column('gender', String),
    Column('primary_image', String),
    Column('secondary_images', String),
    Column('section', String),
)
meta.create_all(engine)
conn = engine.connect()

class MyntraScrapper:
    rows = 100
    domain = "https://www.myntra.com/"
    base_url = domain + "gateway/v2/search/"
    
    def __init__(self, no_of_items ):
        with open("headers.txt") as f:
            header_string = f.read()
        headers = dict(i.strip().split(": ")
                       for i in header_string.splitlines())
        s = requests.Session()
        s.headers.update(headers)
        s.get("https://myntra.com")
        s.get("https://www.myntra.com/myntra-fashion-store?f=Brand%3AU.S.%20Polo%20Assn.%2CU.S.%20Polo%20Assn.%20Denim%20Co.%2CU.S.%20Polo%20Assn.%20Kids%2CU.S.%20Polo%20Assn.%20Tailored%2CU.S.%20Polo%20Assn.%20Women%3A%3AGender%3Amen%2Cmen%20women&rf=Discount%20Range%3A30.0_100.0_30.0%20TO%20100.0")
        #Increase no_of_items because there might be same item in multiple categories
        self.no_of_items  = no_of_items * 1.2
        self.s = s

    def get_product_info(self, category, product):
        same_keys = ["brand", "category", "mrp", "price", "gender"]
        info = {i: product[i] for i in same_keys}
        more_info = {
            "website": "https://www.myntra.com/",
            "link": self.domain+product["landingPageUrl"],
            "name": product["productName"],
            "primary_image": product["searchImage"]
        }
        info["sizes"] = product["sizes"]
        info["secondary_images"] = ",".join(i["src"] for i in product["images"] if i["src"])
        info["section"] = self.categories[category]
        info.update(more_info)
        return info

    def get_products(self, category, page_no):
        data = self.get_category(category, page_no)
        products = data["products"]
        products = [self.get_product_info(category, product) for product in products]
        return products

    def save_products(self, params):
        category, page_no = params
        products = self.get_products(category, page_no)
        conn.execute(products_table.insert(
        ).prefix_with('OR IGNORE'), products)
        print("Category:", category, "| Page No:", page_no, "completed")

    def get_no_of_pages(self, category):
        data = self.get_category(category)
        total_count = data["totalCount"]
        no_of_pages = math.ceil(total_count/self.rows)
        return no_of_pages
    
    def get_no_of_products(self, category):
        data = self.get_category(category)
        total_count = data["totalCount"]
        return total_count

    def get_category(self, category, page_no=1):
        skip = self.rows*(page_no-1)
        params = {"p": page_no, "plaEnabled": False,
                  "rows": self.rows, "o": skip}
        res = self.s.get(self.base_url+f"{category}", params=params)
        return res.json()

    def scrap_category_products(self, category, percentage):
        actual_pages = self.get_no_of_pages(category)
        pages = math.ceil(actual_pages * percentage/100)
        print("Scraping", pages, "pages, out of", actual_pages)
        # for parallel processing
        no_of_threads = 4
        pool = Pool(no_of_threads)
        pool.map(self.save_products, ((category, i)
                 for i in range(1, pages+1)))
        pool.close()

    def scrap_all_categories(self):
        with open("categories.json") as f:
            categories = f.read()
            categories = json.loads(categories)
        self.categories = categories
        
        counts = {}
        print("Getting number of products in each category")
        for category in categories:
            products = self.get_no_of_products(category)
            counts[category] = products
            print(categories[category], products)

        total_products = sum(counts.values())
        # percentage of items to scrap per category
        percentage = min(self.no_of_items, total_products)*100//total_products
        print("There are total", total_products, "products")
        print("Scraping a total of aleast", total_products*percentage//100, "products")

        for category in categories:
            print("Now scraping", categories[category])
            self.scrap_category_products(category, percentage)


if __name__ == "__main__":
    no_of_items = 400000
    myntra_bot = MyntraScrapper(no_of_items)
    myntra_bot.scrap_all_categories()
