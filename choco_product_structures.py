from dataclasses import dataclass, field, fields, InitVar, asdict
import os
import csv
import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path
import json
import functools

from abc import ABC, abstractmethod
import abc


# def apply_product_rules(product):
#     # Implement your specific rules here
#     # For example, check product validity, format data, etc.
#     # Modify the product object directly based on the rules
#     # ...

#     # Return the modified product
#     return product

# class ProductService:
#     def __init__(self, parser, storage):
#         self.parser = parser
#         self.storage = storage

#     def process_data(self, data):
#         parsed_data = self.parser.parse(data)
#         self.storage.save(parsed_data)


# class DataProvider:
#     def __init__(self, data_adapter):
#         self.data_adapter = data_adapter

#     def read_data(self):
#         return self.data_adapter.read_data()

#     def store_data(self, data):
#         self.data_adapter.store_data(data)

# class ProductDataAdapter:
#     # Implement data handling specific to product data

# class DetailDataAdapter:
#     # ... (similar for detail data)

# class AssemblyDataAdapter:
#     # ... (similar for assembled product data)



class DataStorage(ABC):
    @abstractmethod
    def read(self, key):
        pass
    @abstractmethod
    def write(self, key, value):
        pass
    

#:TODO fetch currency & cache for each currency in use for convert_ methods
#:TODO pass from config or on init the "missing" string in a way that it could be changed
#:TODO pass base url "https://www.chocolate.co.uk" externally of the Data class
#:TODO decouple data access logic by storage type: db, file
    

# Concrete subclass for database storage
class DatabaseStorage(DataStorage):
    def __init__(self):
        # Simulate a database connection
        self.database = {}
    def read(self, key):
        if key in self.database:
            return self.database[key]
        else:
            return None
    def write(self, key, value):
        self.database[key] = value
        print(f"Writing to the database: {key} -> {value}")

STORAGES = {}
FILE_PARSERS = {}


def register_parser(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        # Do something before
        print(f, args[0], kwargs)
        # value = f(*args, **kwargs)
        FILE_PARSERS[f] = args[0]
        # # Do something after
        return args
    return decorator

def register_storage(storage_type):
    def decorator(fn):
        # print(fn, fn.__name__, storage_type)
        STORAGES[storage_type] = fn
        return fn
    return decorator

@register_parser('json_parser')
class json_parser:
    def __init__(self, filename, keys):

        self.filename = filename
        self.keys = keys
        try:
            with open(self.filename, mode="r", encoding="utf-8") as output_file:
                self.data = json.load(output_file)
        except FileNotFoundError:
            self.data= []

        print('\n\n\n\nexisting_data', len(self.data), self.data)
        


    def write(self, num, obj):
        # self.data.append(obj)
        # self.data.extend(obj)
        print()
        if not self.data.__contains__(obj): 
            
            self.data.append(obj)
            with open(self.filename, mode="w", encoding="utf-8") as output_file:
                json.dump(self.data, output_file, indent=2)


    def initialize(self):
        if len(self.data) == 0:
            with open(self.filename, mode="w", encoding="utf-8") as output_file:
                json.dump([], output_file, indent=2)

    

@register_parser('csv_parser')
class csv_parser():
    def __init__(self, filename, keys):
        

        self.filename = filename
        self.keys = keys

    def initialize(self):
        with open(self.filename, mode='w', newline='', encoding='utf-8') as output_file:
            writer = csv.DictWriter(output_file, fieldnames = self.keys )
            writer.writeheader()


    def write(self, num, obj):
        with open(self.filename, mode='a', newline='', encoding='utf-8') as output_file:
            writer = csv.DictWriter(output_file, fieldnames = self.keys)
            writer.writerow(obj)
        # print(self.filename, num, obj, self.keys)

# @register_parser('json')


@register_storage('database')
def database_storage(keys):
    un = ''
    pasw = ''
    cn_string = ''
    return DatabaseStorage()

@register_storage('file')
def file_storage(filename, extention, keys, filetype='text'):
    #config filestorage here
    return FileSystemStorage(filetype, filename, extention, keys)

def get_storage(storage_type):
    if storage_type not in STORAGES:
        raise ValueError(f"Unsupported storage type: {storage_type}")
    return STORAGES[storage_type]

def get_file_parser(file_type):
    print(FILE_PARSERS)
    if file_type not in FILE_PARSERS:
        raise ValueError(f"Unsupported file type: {file_type}")
    return FILE_PARSERS[file_type]

# Concrete subclass for file system storage
class FileSystemStorage(DataStorage):
    def __init__(self, filetype, filename, extention, keys):
        # Simulate a file system
        # self.file = {}
        self.folder_data = Path.cwd() / 'data' 
        self.file_open = False
        self.filename = str(self.folder_data) + filename  + '.' + extention
        self.filetype = filetype
        print('filename', self.filename)
        self.keys = keys

        if not (self.folder_data).exists():
            Path.mkdir(self.folder_data)

        file_exists = (
            os.path.isfile(self.filename) and os.path.getsize(self.filename)
        )

        self.file_parser = get_file_parser(extention + '_parser')(self.filename, self.keys)

        # if not file_exists:
        self.file_open = True
        self.file_parser.initialize()
        self.file_open = False
        
    def ready(self):
        return not self.file_open

    def read(self, key):
        key

    def write(self, key, value):
        self.file_open = True
        self.file_parser.write(key, value)
        print(f"Writing to the file system: {key} -> {value}")
        self.file_open = False

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
    def __init__(self, storageType, storage_queue_limit=5): #:TODO Why 5?????(?) explain -> 5 temporary cells in queue
        self.names_seen = [] #This list is used for checking duplicates.
        self.storage_queue = [] #This queue holds products temporarily until a specified storage limit is reached.
        self.storage_queue_limit = storage_queue_limit #This variable defines the maximum number of products that can reside in the storage_queue

        self.processed = 0 #row product counter

        keys = []
        keys.extend([f.name for f in fields(Product)])
        
        #setting up storage
        match storageType:
            case "database":
                self.storage = get_storage('database')()

            case "file":
                filename="product_data"
                self.storage =  get_storage('file')('/' +  filename, 'csv',  keys)
            case _:
                print('No type  {self.storage} Storage allowed')


    def initialize(self):
        print("fields")

    def write_footer(self, fields_, offset=1):
        
        self.csv_file_open = True
        
        total = [''] * len(fields(Product))
        for n, val in enumerate(fields_):
            total[n] = val

        total[-1]= self.processed
        with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as output_file:
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
            # print(self.storage_queue, len(self.storage_queue))
            self.storage_queue.append(product)
            if (
                len(self.storage_queue) >= self.storage_queue_limit
                                # and self.csv_file_open == False
                and self.storage.ready()
            ):
                self.save()

    def save(self): #buffer similar here
   
        products_to_save = []
        products_to_save.extend(self.storage_queue)
        # self.save_to_json()

        self.storage_queue.clear()
        if not products_to_save:
            return
        
        for product in products_to_save:
            self.storage.write(product.num, asdict(product))
            self.processed += 1


    def is_duplicate(self, product_data):
        if product_data.name in self.names_seen:
            print(f"Duplicate item found: {product_data.name}. Item dropped.")
            return True
        self.names_seen.append(product_data.name)
        return False
    
    def close_pipeline(self):
        if self.storage.ready():
            time.sleep(1)
        if len(self.storage_queue) > 0:
            self.save()
            # self.save_to_json()

        #:TODO implement calculate avarage on the different prices columns
        # self.write_footer(['Total', '', ''], 1)

    


list_of_urls = [
    "https://www.chocolate.co.uk/collections/all",
]

# Scraping Function


def start_scrape():

    # Loop Through List of URLs

    data_pipeline.initialize()
    counter = 1
    for url in list_of_urls:

        # Send Request

        response = requests.get(url)

        if response.status_code == 200:

            # Parse Data
            time.sleep(1)

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
                # print('prod num', n)
                # product = apply_product_rules(product)
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
    data_pipeline = ProductDataPipeline(storageType='file')
    start_scrape()
    data_pipeline.close_pipeline()
