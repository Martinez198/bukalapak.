import requests
import argparse
from lxml.html import fromstring
import json

class Bukalapak():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser = self.define_args(parser)
        self.args = parser.parse_args()

    def define_args(self, parser):
        parser.add_argument('--out-file', required=True, help='output json file')
        return parser

    def get_pages(self):
        url = "https://api.bukalapak.com/multistrategy-products?keywords=samsung&limit=50&offset=0&facet=true&page=1&shouldUseSeoMultistrategy=false&access_token=bWHCCJgfTrAr1QyOUYCLdfbuZ55W032LZ6yQh5Ij5Ty-MQ"
        r = requests.get(url).json()
        return r.get("meta").get('total_pages')

    def run(self):
        out_file = open(self.args.out_file, 'w')
        pg_count = self.get_pages()
        for i in range(1,  pg_count+1):
            url = "https://api.bukalapak.com/multistrategy-products?keywords=samsung&limit=50&offset=0&facet=true&page="+str(i)+"&shouldUseSeoMultistrategy=false&access_token=bWHCCJgfTrAr1QyOUYCLdfbuZ55W032LZ6yQh5Ij5Ty-MQ"
            r = requests.get(url).json()
            for data_ in r.get('data'):
                dic = {}
                dic['product_name'] = data_.get('name')
                dic['product_link'] = data_.get('url')
                dic['product_price'] = data_.get('price')
                dic['product_rating'] = data_.get('rating').get('average_rate')
                dic['product_location'] = data_.get('store').get('address').get('city')
                dic['brand_name'] = "Samsung"
                out_file.write(json.dumps(dic)+'\n')


if __name__ == '__main__':
    Bukalapak().run()

