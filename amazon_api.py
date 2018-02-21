#coding:utf-8
PURPLE  = '\033[35m'
RED     = '\033[31m'
CYAN    = '\033[36m'
OKBLUE  = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL    = '\033[91m'
ENDC    = '\033[0m'
from amazon.api import AmazonAPI
from amazon.api import LookupException, AsinNotFound
from time import sleep
import codecs
import re
import requests
import shutil
import csv
ACCESS_KEY = "ここにアクセスキーを入力"
SECRET_ACCESS_KEY = "ここにシークレットアクセスキーを入力"
ASSOCIATE_TAG = "ここにアソシエイトタグを入力"
error = 0

amazon = AmazonAPI(ACCESS_KEY, SECRET_ACCESS_KEY, ASSOCIATE_TAG, region="JP")

#def save(JAN,name,price,asin,title,amazon_price,review):
	
def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open('image/'+ file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)








def amazon_api(JAN,name,price,url,counter):
	try:
		product = amazon.lookup(ItemId=JAN, IdType="EAN", SearchIndex="All")
		if isinstance(product, list):
			print 'NO amazon'
		else:
			asin = product.asin
			title= product.title
			amazon_price= product.price_and_currency[0]
			group = product.product_group
			rank  = product.sales_rank
			if amazon_price is None:
				amazon_price = 0
			reviews = product.reviews[1]
			print 'ASIN: '+ OKBLUE +str(asin) + ENDC
			print title
			print 'price: '+str(amazon_price)
			print 'group: '+str(group)
			print 'ranking: '+str(rank)
			#if int(rank) < 100000:
			#	image_url = 'http://images-jp.amazon.com/images/P/'+asin+'.09.THUMBZZZ.jpg'
			#	image_name = asin + '.jpg'
			#	download_img(image_url, image_name)
		
			#print 'review: '+str(reviews)
			r = requests.get(reviews)
			sleep(0.01)
			content = r.text
			content = content.encode('utf_8')
			n = 0
			if '<div style="display:block; text-align:center; padding-bottom: 5px;" class="tiny">' in content:
				n = content.split('<div style="display:block; text-align:center; padding-bottom: 5px;" class="tiny">')[1]
				n = n.split('レビュー')[0]
				n = n.replace('\n','')
				n = n.replace('<b>','')	
				n = n.replace('\t','')
				n = n.replace(' ','')
				print 'review: '+str(n)
			else:
				
				print 'review: '+str(n)
			review = n

			if int(rank) < 300000 or int(review) > 1:
                                image_url = 'http://images-jp.amazon.com/images/P/'+asin+'.09.THUMBZZZ.jpg'
                                image_name = asin + '.jpg'
				download_img(image_url, image_name)



			mono_url = 'http://mnrate.com/item/aid/'+ asin			
			dif = int(price) - int(amazon_price)
			r_dif = int(amazon_price)*0.1 + int(dif)
			br = - r_dif/int(price)*100
			print 'BR: '+PURPLE+ str(int(br)) +ENDC
			amazon_url = 'https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=カタカナ&url=search-alias%3Daps&field-keywords=' + JAN

			strings = str(JAN)+','+str(asin)+','+str(mono_url)+','+str(name)+','+str(price)+','+str(amazon_price)+','+str(dif)+','+str(int(r_dif))+','+str(br)+','+str(review)+','+str(url)+','+str(amazon_url)+','+str(group)+','+str(rank)+'\n'
			#print strings
			b.write(strings)
			
			#save(JAN,name,price,asin,title,amazon_price,review)


	except Exception as e:
		#print e
		if 'ASIN(s) not found:' in e:
			counter = 7
		counter = counter +1
		if counter > 4:
			print 'Not found'	
		else:
			sleep(1)
			amazon_api(JAN,name,price,url,counter)














JAN = 0
count = -1
a = open('/output/output.csv','r')
b = open('/output/output2.csv','w')
b.write('JAN,ASIN,MONO,NAME,PRICE,amazon_PRICE,DIF,R_DIF,BR,REV,URL,amazonURL\n')
for line in a:
	count = count + 1
	LINE = line.rstrip().split(',')
	JAN   = LINE[0]
	name  = LINE[1]
	price = LINE[2]
	url   = LINE[3] 
	counter = 0
	print '\n\n'
	if count >= 1:
		print OKGREEN + str(count) + ENDC
		print 'JAN: '+str(JAN)
		#print name
		#print price
		#print url
		amazon_api(JAN,name,price,url,counter)
		sleep(0.5)

a.close()
b.close()
