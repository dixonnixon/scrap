import requests
import json
import csv
import re
from pathlib import Path

from bs4 import BeautifulSoup

site_url='https://www.chocolate.co.uk'
list_of_urls = [
    site_url + '/collections/all'
]

folder = "data"

scraped_data = []

def save_to_csv(data_list, filename):
    keys = data_list[0].keys()
    #---check & create dir if not exists
    folder_data = Path.cwd() / folder 
    print(type(folder_data), folder_data)
    if not (folder_data).exists():
        Path.mkdir(folder_data )
    # folder + '/' + 
    filename = str(folder_data) + '/' +  filename + '.csv'
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data_list)

def start_scrape():
    for url in list_of_urls:
        ##
        # print(url)
        response = requests.get(url)

        if response.status_code == 200:
            # print(response.text)
            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.select('product-item')
            for product in products:
                url_prod = product.select('div.product-item-meta a')[0]['href']
                nm = product.select('a.product-item-meta__title')[0].get_text()
                text = product.select('span.price')[0].get_text()
                prev_price = ''
                prev_price_field = product.select('span.price--compare')
                if(len(prev_price_field) > 0):
                    prev_price = re.findall('\£\d+\.\d+', prev_price_field[0].text)[0]

                pr = re.findall('\£\d+\.\d+', text)
                # print(pr[0])
                scraped_data.append({
                    'name': nm,
                    'price': pr[0],
                    'prev_price': prev_price,
                    'url': url + url_prod 
                })
            
            ## Next Page
            next_page = soup.select('a[rel="next"]')
            if len(next_page) > 0:
                next_page_url = next_page[0]['href']
                # print(( len(next_page) > 0), next_page_url)
                list_of_urls.append(site_url + next_page_url)
                # print(list_of_urls)
            # print(products, len(products), first_product_nm, first_product_pr, url)
        pass


if __name__ == "__main__":
    start_scrape()
    # print(json.dumps(scraped_data))
    print( 'total_products:', len(scraped_data))
    save_to_csv(scraped_data, 'chocolates')