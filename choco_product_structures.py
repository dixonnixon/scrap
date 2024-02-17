from dataclasses import dataclass, field, fields, InitVar, asdict
import os
import csv
import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path



#:TODO fetch currency & cache for each currency in use for convert_ methods
#:TODO pass from config or on init the "missing" string in a way that it could be changed
#:TODO pass base url "https://www.chocolate.co.uk" externally of the Data class


@dataclass
class Product:
    num: str = ""
    name: str = ""
    price_string: InitVar[str] = ""
    price_gb: float = field(init=False)
    price_usd: float = field(init=False)
    price_ua: float = field(init=False)
    url: str = ""

    def __post_init__(self, price_string):
        self.name = self.clean_name()
        self.price_gb = self.clean_price(price_string)
        self.price_ua = self.convert_price_to_ua()
        self.price_usd = self.convert_price_to_usd()
        self.url = self.create_absolute_url()


    def clean_price(self, price_string):
        price_string = price_string.strip()
        price_string = price_string.replace("Sale price£", "")
        price_string = price_string.replace("Sale priceFrom £", "")
        if price_string == "":
            return 0.0
        return float(price_string)
    
    def convert_price_to_usd(self):
        return self.price_gb * 1.21
    
    def convert_price_to_ua(self):
        return self.price_gb * 0.4 
    
    def clean_name(self):
        if self.name == "":
            return "missing"
        return self.name.strip()
    
    def create_absolute_url(self):
        if self.url == "":
            return "missing"
        
    def create_absolute_url(self):
        if self.url == "":
            return "missing"
        return "https://www.chocolate.co.uk" + self.url
    

class ProductDataPipeline:
    def __init__(self, csv_filename="", storage_queue_limit=5): #:TODO Why 5?????(?) explain
        self.names_seen = [] #This list is used for checking duplicates.
        self.storage_queue = [] #This queue holds products temporarily until a specified storage limit is reached.
        self.storage_queue_limit = storage_queue_limit #This variable defines the maximum number of products that can reside in the storage_queue
        self.csv_filename = csv_filename #This variable stores the name of the CSV file used for product data storage.
        self.csv_file_open = False #This boolean variable tracks whether the CSV file is currently open or closed.
        # self.check_file()
        self.processed = 0
        
        self.folder_data = Path.cwd() / 'data' 
        self.filename = str(self.folder_data) + '/' +  self.csv_filename 


    def check_file(self):
        print("fields")
        if not (self.folder_data).exists():
            Path.mkdir(self.folder_data)


        self.csv_file_open = True

        file_exists = (
            os.path.isfile(self.filename) and os.path.getsize(self.filename)
        )
        print(file_exists)
        keys = []
        keys.extend([f.name for f in fields(Product)])
        with open(self.filename, mode='w', newline='', encoding='utf-8') as output_file:
            writer = csv.DictWriter(output_file, fieldnames = keys)

            writer.writeheader()

        self.csv_file_open = False

    def write_footer(self, fields_, offset=1):
        
        self.csv_file_open = True
        
        total = [''] * len(fields(Product))
        for n, val in enumerate(fields_):
            print(n, val)
            total[n] = val


        total.extend([self.processed])
        # print(total)
        with open(self.filename, mode='a', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)
            #insert empty offset row
            n = 0
            while n < offset:
                writer.writerow([''] * len(fields(Product)))
                n+=1
            writer.writerow(total)

        self.csv_file_open = False



    def clean_raw_product(self, scraped_data):
        
        return Product(
            num=scraped_data.get("num",""),
            name=scraped_data.get("name", ""),
            price_string=scraped_data.get("price", ""),
            url=scraped_data.get("url", ""),
        )

    # check
    def add_product(self, num, scraped_data): #queue based approach here
        scraped_data["num"] = num 
        product = self.clean_raw_product(scraped_data)
        if self.is_duplicate(product) == False:
            print(self.storage_queue, len(self.storage_queue))
            self.storage_queue.append(product)
            if (
                len(self.storage_queue) >= self.storage_queue_limit
                and self.csv_file_open == False
            ):
                self.save_to_csv()

    def save_to_csv(self): #buffer similar here
        folder_data = Path.cwd() / 'data' 
        # if not (folder_data).exists():
        #     Path.mkdir(folder_data )

        filename = str(folder_data) + '/' +  self.csv_filename 

        self.csv_file_open = True
        products_to_save = []
        products_to_save.extend(self.storage_queue)
        self.storage_queue.clear()
        if not products_to_save:
            return
        keys = [field.name for field in fields(products_to_save[0])]
        print('keys ', keys)
        # file_exists = (
        #     os.path.isfile(filename) and os.path.getsize(filename)
        # )
        # print('\n',file_exists,'\n')

        # with open(filename, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as output_file:
        with open(filename, mode='a', newline='', encoding='utf-8') as output_file:
            writer = csv.DictWriter(output_file, fieldnames = keys)

            # if not file_exists:
            #     writer.writeheader()
            for product in products_to_save:
                # product['num'] = self.processed
                
                writer.writerow(asdict(product))
                self.processed += 1
        self.csv_file_open = False

    def is_duplicate(self, product_data):
        if product_data.name in self.names_seen:
            print(f"Duplicate item found: {product_data.name}. Item dropped.")
            return True
        self.names_seen.append(product_data.name)
        return False
    
    def close_pipeline(self):

        if self.csv_file_open:
            time.sleep(1)
        if len(self.storage_queue) > 0:
            self.save_to_csv()

        self.write_footer(['Total', '', 'total_price_gb'], 1)

    


list_of_urls = [
    "https://www.chocolate.co.uk/collections/all",
]

# Scraping Function


def start_scrape():

    # Loop Through List of URLs

    data_pipeline.check_file()
    counter = 1
    for url in list_of_urls:

        # Send Request

        response = requests.get(url)

        if response.status_code == 200:

            # Parse Data
            time.sleep(2)

            soup = BeautifulSoup(response.content, "html.parser")
            products = soup.select("product-item")

            for n, product in enumerate(products):
                name = product.select("a.product-item-meta__title")[0].get_text()
                price = (
                    product.select("span.price")[0]
                    .get_text()
                    .replace("\nSale price£", "")
                )
                url = product.select("div.product-item-meta a")[0]["href"]

                # Add To Data Pipeline
                print('prod num', n)
                data_pipeline.add_product(counter, {"name": name, "price": price, "url": url})
                counter += 1
            # Next Page

            next_page = soup.select('a[rel="next"]')
            print('\n\n\nnext page = ', next_page)
            if len(next_page) > 0:
                list_of_urls.append(
                    "https://www.chocolate.co.uk" + next_page[0]["href"]
                )
    print(data_pipeline.processed)


if __name__ == "__main__":
    data_pipeline = ProductDataPipeline(csv_filename="product_data.csv")
    start_scrape()
    data_pipeline.close_pipeline()
