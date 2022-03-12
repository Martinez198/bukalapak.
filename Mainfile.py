import requests
from lxml import html
from bs4 import BeautifulSoup
import pandas as pd
import json
import datetime
import time
import time
import csv
import random
from time import sleep
import os
import threading

#Proxy (Harsh Khare)
from scraper_api import ScraperAPIClient
import random


def sleep_random():
    pcnt = random.randint(1,10)
    # pcnt = random.randint(10,40)
    return pcnt


def clean_rubish(cleantext):
    SiteSKUCode_1 = cleantext
    SiteSKUCode_1 = SiteSKUCode_1.replace('\\t', '')
    SiteSKUCode_1 = SiteSKUCode_1.replace('\\n', '')
    SiteSKUCode_1 = SiteSKUCode_1.replace("\\", '')
    SiteSKUCode_1 = SiteSKUCode_1.replace("[", '')
    SiteSKUCode_1 = SiteSKUCode_1.replace("]", '')
    return SiteSKUCode_1

def clean_data(abc):
    SKU_code = abc
    try:
        SKU_code = SKU_code[0]
        SKU_code = clean_rubish(SKU_code)
    except:
        SKU_code = ""
    return SKU_code

def posSubSt(target,key,key_1,res):
    import string
    index = target.index(key)
    index_1 = target.index(key_1)
    try:
        while index!=-1:
            index = target.index(key)
            index_1 = target.index(key_1)
            if(target[target.index(key):target.index(key_1)]!=''):
                res.append(target[target.index(key):target.index(key_1)])
            target = target[index_1+key_1.__len__():]
    except:
        pass
    return res


#get header
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}


def ProductCrawl( index,url_product ):
    sleep(sleep_random())
    pcnt = random.randint(1, 400)
    #pcnt = random.randint(405, 1500)
#    proxies = prx.proxy_deliver(pcnt)
    #res1 = requests.get(url_product, proxies=proxies, headers=headers)

    client = ScraperAPIClient('3ee62317f55e96b41a47f4de5569242f')
    print(url_product)
    try:
        res1 = client.get(url=url_product,  headers=headers).text
#        print(page);
        lxmlElem1 = html.fromstring(res1)
        # print(res.text)
        lxm1 = str(lxmlElem1)


        p1 = str(lxmlElem1.xpath('//div/h1/text()'))

        ProductName = product_name = str(clean_rubish( p1 )).replace("'","")

        pnf = clean_rubish(str(lxmlElem1.xpath('//h1[contains(@class, "title")]/text()')))
        if '404' in pnf and product_name == '':
            product_name = 'Product not available'
        #JSON IN HTML (HARSH KHARE)
        soup= BeautifulSoup(res1,features='html.parser')
        ctr=0
        for json_soup in soup.findAll('script',{'type':'application/ld+json'}):
            ctr+=1
            obj=''
            if ctr==4:
                zz=json_soup.text
                obj=json.loads(zz)
            print(str(obj))

        SKU_code = str(lxmlElem1.xpath('//div[@class="dy"]/*//div[@class="u-hm"]/form[1]/input[@name="item[product_sku_id]"]/@value'))
        SKU_code = clean_rubish(SKU_code)
        SKU_code = SKU_code.replace("'","")
        SKU_code = SKU_code.replace('"',"")
        product_id = str(lxmlElem1.xpath('//div[@class="c-panel__body"]/*//div[@class="u-clearfix"]/form[1]/input[@name="item[product_id]"]/@value'))
        product_id = clean_rubish(product_id)
        product_id = product_id.replace("'","")
        product_id = product_id.replace('"',"")

        brand = lxmlElem1.xpath('//div[@class="brand-view"]/p/a/text()')

        stock = lxmlElem1.xpath('//*[@id="section-main-product"]/div[2]/div[4]/text()')
        try:
            stock = clean_data(stock)
            stock = clean_rubish(stock)
        except:
            stock = str( stock )
        stock = str(stock).replace('\n','').replace('>','').replace('stok','')
        availability = ''
        outofstock = str(lxmlElem1.xpath('//span[@class="c-label--large c-labe u-mrgn-bottom--3--sold-out"]/text()'))
        if 'Stok Habis' in outofstock:
            stock = 'Out of stock'
            availability = 'No'
        item_del = str(lxmlElem1.xpath('//span[@class="c-label--large ge c-label u-mrgn-bottom--3--removed"]/text()'))
        if 'Barang Telah Dihapus' in item_del:
            stock = 'Out of stock'
            availability = 'No'
        if stock == '':
            stock = 'NA'
        if availability != 'No':
            availability = 'Yes'

        Listing_size = str(lxmlElem1.xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div[1]/table/tbody/tr[8]/td[2]/text()'))
        if Listing_size == '':
            Listing_size='NA'
        Listing_size_data_ = clean_rubish(str(lxmlElem1.xpath('//option[@data-label="Kapasitas" and @selected ]/@data-id')).replace("'",""))
        Listing_color_id = clean_rubish(str(lxmlElem1.xpath('//tr[td[contains(text(),"Warna")]]/td[2]/select/option[@selected]/@data-id')).replace("'",""))

        if Listing_color_id != '':
            Listing_size_data_id = Listing_color_id+"-"+Listing_size_data_
        else:
            Listing_size_data_id = Listing_size_data_




        try:
            promo_price = str(lxmlElem1.xpath('//*[@id="section-main-product"]/div[2]/div[2]/div/div[1]/div/span/text()'))
            promo_price = promo_price.replace("$","")
            promo_price = promo_price.replace("S","")
            promo_price = promo_price.replace(".","")
            promo_price = promo_price.replace("['", "").replace("']", "").replace("'", "")
        except:
            promo_price = ''

        try:
            listing_price = str(lxmlElem1.xpath('//*[@id="section-main-product"]/div[2]/div[2]/div/div[1]/div[1]/span/text()'))
            listing_price = listing_price.replace("$", "")
            listing_price = listing_price.replace("S", "")
            listing_price = listing_price.replace(".", "")
            listing_price = listing_price.replace("['", "").replace("']", "").replace("'", "")
        except:
            listing_price = ''

        #if promo_price == '[]' or promo_price == '':
         #   xp ='//div[@class="js-product-detail-price js-variant-detail-element js-variant-price-'+str(Listing_size_data_id)+' qa-pd-price u-mrgn-bottom--3 u-position-relative"]//div[@class="c-product-detail-price"]/span/span[@class="amount positive"]/text()'
          #  promo_price1 = clean_rubish(str( lxmlElem1.xpath(xp) ))
        if promo_price == '[]' or promo_price == '' :
            try:
                promo_price = lxmlElem1.xpath('//div[@class="c-rice"]/span/span[@class="amount positive"]/text()')[0]
            except:
                promo_price = lxmlElem1.xpath('//div[@class="c-product-detail-price"]/span/span[@class="amount positive"]/text()')
            promo_price = str(promo_price).replace("$","")
            promo_price = str(promo_price).replace("S","")
            promo_price = str(promo_price).replace(".","")
            promo_price = str(promo_price).replace("['", "").replace("']", "").replace("'", "")



        if listing_price == '[]' or listing_price == '':
            listing_price = promo_price

        desc = lxmlElem1.xpath('//*[@id="section-informasi-barang"]/div[2]/div[3]/div/div[1]/div/text()')
        #desc = str(clean_rubish(desc)).replace("'","")
        if desc == '':
            desc = 'NA'

        spec = str(lxmlElem1.xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div[1]/text()'))
        spec = str(clean_rubish(spec)).replace("'","")
        if spec == '':
            spec = 'NA'

        # desc = clean_rubish(desc)
        #sku = lxmlElem1.xpath('//div[@class="infoContainer"]/ul/li[2][@title="Manufacturer Part Number"]/span[2][@name="mpn"]/text()')
        url = url_product
        #product_rating = lxmlElem1.xpath('//span[@itemprop="ratingCount"]/a/text()')
        try:
            war = posSubSt( res1.text, 'Garansi' , '</dd>',[] )
            war1 = str(war).split('<dd')
            war2 = war1[len(war1) - 1  ].split('>')
            warranty = str(clean_rubish( str( war2[len(war2) - 1] ) )).replace("'","")
        except:
            warranty = ''

        try:
            reb = posSubSt( res1.text, 'class="c-icon c-icon--label qa-pd-condition-icon"' , '</dd>',[] )
            reb1 = str(reb).split('<dd')
            reb2 = posSubSt(str(reb1), '"c-label">', '</span>', [])
            refurb = str(reb2).replace('"c-label">', '')
            refurb = clean_rubish(refurb)
            # print(refurb)

            # refur = clean_rubish(str(war2[len(war2) - 1]))
        except:
            refurb = ''

        refurbish = ''
        if any(val.lower() in product_name.lower() for val in ['referbish','refer','refurbish','refurb','second hand','second-hand','second','2 nd','2nd','bekas','welfare goods','welfare products']):
            refurbish = 'Yes'
        else:
            refurbish = 'No'

        if 'Bekas'.lower() in refurb.lower():
            refurbish = 'Yes'

        if 'Bekasi'.lower() in refurb.lower():
            refurbish = 'No'

        if 'Import'.lower() in ProductName.lower():
            imp_exp = 'Import'
        elif 'Export'.lower() in ProductName.lower():
            imp_exp = 'Export'
        else:
            imp_exp = 'NA'


        pro1 = pro2 = pro3 = pro4 = pro5 = pro6 = pro7 = pro8 = pro9 = pro10 = pro11 = ''
        if 'with'.lower() in ProductName.lower():
            pro1 = 'with - keyword in ListingTitle '
        if '&' in ProductName.lower():
            pro2 = '& - keyword in ListingTitle '
        if 'bundle'.lower() in ProductName.lower():
            pro3 = 'bundle - keyword in ListingTitle '
        if 'free'.lower() in ProductName.lower():
            pro4 = 'free - keyword in ListingTitle '
        if 'insurance'.lower() in ProductName.lower():
            pro5 = 'insurance - keyword in ListingTitle '
        if 'Extended Warranty'.lower() in ProductName.lower():
            pro6 = 'extended warranty - keyword in ListingTitle '
        if 'International Ver'.lower() in ProductName.lower():
            pro7 = 'International Ver - keyword in ListingTitle '
        if 'Warranty'.lower() in ProductName.lower():
            pro8 = 'warranty - keyword in ListingTitle '
        if 'GARANSI RESMI'.lower() in ProductName.lower():
            pro9 = 'GARANSI RESMI(OFFICIAL GUARANTEE) - keyword in ListingTitle '
        if 'bebas'.lower() in ProductName.lower():
            pro10 = 'bebas - free - keyword in ListingTitle '
        if 'bonus'.lower() in ProductName.lower():
            pro11 = 'bonus - keyword in ListingTitle '

        pro = clean_rubish(str([pro1 + pro2 + pro3 + pro4 + pro5 + pro6 + pro7 + pro8 + pro9 + pro10 + pro11]))




#SEL    LER INFO (HARSH KHARE)
        seller_name = str(lxmlElem1.xpath('//*[@id="section-informasi-pelapak"]/div[2]/div/div[1]/div[1]/h3/a/text()'))
        if seller_name == '[]':
            seller_name = str(lxmlElem1.xpath('//div[@class="c-brand-user__avatar"]/*//h2/a/text()[0]') )

        seller_name = str(clean_rubish(seller_name)).replace("'",'')
        seller_rating = str(lxmlElem1.xpath('//*[@id="section-informasi-pelapak"]/div[2]/div/div[2]/div[1]/div[1]/div/span/text()'))
        if seller_rating=='':
            seller_rating='NA'


        product_rating = str( lxmlElem1.xpath('//*[@id="section-ulasan-barang"]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/span/text()') )
        if product_rating == '':
            product_rating = 'NA'
        product_review = clean_rubish(str( lxmlElem1.xpath('//a[@id="product-detail-seller-feedback"]/text()') ))
        if product_review == '':
            product_review = 'NA'

        warranty = lxmlElem1.xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div[1]/table/tbody/tr[10]/td[2]/text()')
        #type_init = list1['lob'][index] (Harsh Khare)





        try:
            if '_' in type_init:
                some = type_init.split('_')
                Cat = some[0]
                Type = some[1]
                try:
                    if '(' in Type:
                        Type = Type.split('(')
                        Type = Type[0]
                    else:
                        Type = Type
                except:
                    pass
        except:
            Cat = ''
            Type = ''

        recrawl_flag = 0  # should be 0 else cache page will not be generated
#        import time
        # import date
        from datetime import date
        import datetime
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
        #path = 'E:/AdvanceCrawler/SavePage/Bukalapa_sein/cache/' (Harsh Khare)
        #cache_page_link = cache.create_cache(SKU_code, url_product , st, recrawl_flag, res1.text,path) (Harsh Khare)
        #cache_page_link = cache_page_link.replace('E:/AdvanceCrawler/', 'https://ecxus098.eclerx.com/') (Harsh Khare)

        weekNumber = date.today().isocalendar()[1]
        weekNumber = 'W'+str(weekNumber)
        ts = time.time()
        today = datetime.date.today()
        st = datetime.datetime.fromtimestamp(ts).strftime('%m/%d/%Y %H:%M:%S')
        st_1 = datetime.datetime.fromtimestamp(ts).strftime('%m/%d/%Y')
        print(st)
        url_page = clean_rubish( str(lxmlElem1.xpath('//link[@rel="canonical"]/@href')) ).replace("'","")



        myData = {
            'Include/ Exclude': '',
            'Week': weekNumber,
            'Sub': 'SEIN',
            'Site': 'Bukalapak',
            'Cat': Cat,
            'Type': Type,
            'Series Name': '',
            'SS SKU Code': '',
            'D/B Name': '',
            'SS SKU Size': '',
            'SS SKU Colour': pro,
            'Listing Title': product_name,
            'Listing Size': Listing_size,
            'Listing Color': 'NA',
            'CCY': 'IDR',
            'RRP (LC)': '',
            'LP (LC)': listing_price,
            'SP (LC)': promo_price,
            'Off/Bund/Promo': 'NA',
            'Seller Name': seller_name,
            'Seller Rating': seller_rating,
            'Seller Rep': 'NA',
            'Seller type': 'Unauthorized',
            'Availability': availability,
            'Stocks': stock,
            'Import/Export': imp_exp,
            'Refurbished': refurbish ,
            'Prod Rating': product_rating,
            '# of Prod Review': product_review,
            'Specification': spec,
            'Description': desc,
            'URL': url_page,
            'Site Prod ID': product_id,
            'Brand': 'Samsung',
            'Site SKU Code': SKU_code,
            'FX': '' ,
            'RRP (USD)': url_product,
            'LP (USD)': '',
            'SP (USD)': '',
            'Warranty Type': warranty ,
            'Timestamp': st,
            'Seller size': 'NA',
            'Seller Time': 'NA',
            'Report Date': st_1,
        }

        outfinal = []
        for k, v in myData.items():
            outfinal.append(v)

        color = lxmlElem1.xpath('//tr[td[contains(text(),"Warna")]]/td[2]/select/option/text()')
        if color == []:
            #with open('Dataout.csv','a', newline="",  encoding='utf-8') as f:
            with open('Dataout.csv', 'a', newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(outfinal)

            #with open('Dataout/PD_Output'+str(index)+'.csv', 'a', newline='', encoding="utf-8") as f:
            #    writer = csv.writer(f)
            #    writer.writerow(outfinal)
        else:
            for ac in range(len(color)):
                myData['Listing Color'] = str(color[ac]).strip(' ')
                outfinal = list(myData.values())
                with open('Dataout.csv', 'a', newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(outfinal)
            with open('Dataout/PD_Output'+str(index)+'.csv', 'a', newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(outfinal)

            sleep(1)
    except:
        pass



def multithred_logic(url_list):
    if url_list.__len__() > 20 :
        for i in range(0,url_list.__len__()-1,20) :    # j = j + 1
            url = url_list[i]
            url2 = str(url).split("^")

            try:

                try:
                    t1 = threading.Thread(target=ProductCrawl, args=(i,url))
                except:
                    print(url)
                    pass
                t1.start()

                try:
                    t2 = threading.Thread(target=ProductCrawl, args=(i + 1, url_list[i+1]))
                except:
                    print(url_list[i+1])
                    pass
                t2.start()

                try:
                    t3 = threading.Thread(target=ProductCrawl, args=(i + 2, url_list[i + 2]))
                except:
                    print(url_list[i+2])
                    pass
                t3.start()

                sleep(sleep_random())

                try:
                    t4 = threading.Thread(target=ProductCrawl, args=(i + 3, url_list[i + 3]))
                except:
                    print(url_list[i+3])
                    pass
                t4.start()


                try:
                    t5 = threading.Thread(target=ProductCrawl, args=(i + 4, url_list[i + 4]))
                except:
                    print(url_list[i+4])
                    pass
                t5.start()

                sleep(10)

                try:
                    t6 = threading.Thread(target=ProductCrawl, args=(i + 5, url_list[i + 5]))
                except:
                    print(url_list[i+5])
                    pass
                t6.start()


                try:
                    t7 = threading.Thread(target=ProductCrawl, args=(i + 6, url_list[i + 6]))
                except:
                    print(url_list[i+6])
                    pass
                t7.start()

                sleep(sleep_random())

                try:
                    t8 = threading.Thread(target=ProductCrawl, args=(i + 7, url_list[i + 7]))
                except:
                    print(url_list[i+7])
                    pass
                t8.start()


                try:
                    t9 = threading.Thread(target=ProductCrawl, args=(i + 8, url_list[i + 8]))
                except:
                    print(url_list[i+8])
                    pass
                t9.start()



                try:
                    t10 = threading.Thread(target=ProductCrawl, args=(i + 9, url_list[i + 9]))
                except:
                    print(url_list[i+9])
                    pass
                t10.start()

                try:
                    t11 = threading.Thread(target=ProductCrawl, args=(i + 10,url_list[i+10]))
                except:
                    print(url)
                    pass
                t11.start()

                try:
                    t12 = threading.Thread(target=ProductCrawl, args=(i + 11, url_list[i+11]))

                except:
                    print(url_list[i+1])
                    pass
                t12.start()

                try:
                    t13 = threading.Thread(target=ProductCrawl, args=(i + 12, url_list[i+12]))

                except:
                    print(url_list[i+2])
                    pass
                t13.start()

                sleep(sleep_random())

                try:
                    t14 = threading.Thread(target=ProductCrawl, args=(i + 13, url_list[i+13]))

                except:
                    print(url_list[i+3])
                    pass
                t14.start()


                try:
                    t15 = threading.Thread(target=ProductCrawl, args=(i + 14, url_list[i+14]))

                except:
                    print(url_list[i+4])
                    pass
                t15.start()

                sleep(sleep_random())

                try:
                    t16 = threading.Thread(target=ProductCrawl, args=(i + 15, url_list[i+15]))

                except:
                    print(url_list[i+5])
                    pass
                t16.start()


                try:
                    t17 = threading.Thread(target=ProductCrawl, args=(i + 16, url_list[i+16]))

                except:
                    print(url_list[i+6])
                    pass
                t17.start()

                sleep(sleep_random())

                try:
                    t18 = threading.Thread(target=ProductCrawl, args=(i + 17, url_list[i+17]))

                except:
                    print(url_list[i+7])
                    pass
                t18.start()


                try:
                    t19 = threading.Thread(target=ProductCrawl, args=(i + 18, url_list[i+18]))

                except:
                    print(url_list[i+8])
                    pass
                t19.start()



                try:
                    t20 = threading.Thread(target=ProductCrawl, args=(i + 19,url_list[i+19]))
                except:
                    print(url_list[i+9])
                    pass
                t20.start()


                t21.start()
                t21.join()

                # t11.start()
                # t11.join()

                sleep(sleep_random())

            except:
                pass
            print(i)

    for ih in range(int(url_list.__len__() / 20) * 20, url_list.__len__() ):
        try:
            ProductCrawl(ih, url_list[ih])
        except:
            print(url_list[ih])
            pass


myData = {
'Include/ Exclude': '',
'Week': '' ,
'Sub': 'SENZ',
'Site': 'PBTech',
'Cat': '',
'Type': '',
'Series Name': '',
'SS SKU Code': '',
'D/B Name': '',
'SS SKU Size': '',
'SS SKU Colour': '',
'Listing Title': '',
'Listing Size': '',
'Listing Color': '',
'CCY': '',
'RRP (LC)': '',
'LP (LC)': '',
'SP (LC)': '',
'Off/Bund/Promo': '',
'Seller Name': '',
'Seller Rating': '',
'Seller Rep': '',
'Seller type': '',
'Availability': '',
'Stocks': '',
'Import/Export': '',
'Refurbished': '',
'Prod Rating': '',
'# of Prod Review': '',
'Specification': '',
'Description': '',
'URL': '',
'Site Prod ID': '',
'Brand': '',
'Site SKU Code': '',
'FX': '',
'RRP (USD)': '',
'LP (USD)': '',
'SP (USD)': '',
'Warranty Type': '',
'Timestamp': '',
'Seller size': '',
'Seller Time': '',
'Report Date': ''
}

outfinal = []


#OUTPUT (HARSH)


for k,v in myData.items():
    outfinal.append(k)

with open('Dataout.csv', 'a', newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(outfinal)

df1 = pd.read_csv('Product_details.csv')
list1 = df1.to_dict()
url_list = list_url1 = list1['Product_URL']


#ProductCrawl(0,'https://www.bukalapak.com/p/handphone/hp-smartphone/fhho1l-jual-promo-samsung-galaxy-s8-sm-g950-garansi-resmi-samsung')
for idd in range(0,200):
    ProductCrawl(idd,url_list[idd])

multi_log = multithred_logic(url_list)


