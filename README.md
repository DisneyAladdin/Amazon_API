# Amazon_API
From JAN code, obtain ASIN code, price, review, category and ranking on Amazon market by using Amazon API.

# Important portion
Can get information of Amazon from only JAN code.

This is a big merit for users selling merchandise on Amazon

# Usage
0. Import modules here
```python
from amazon.api import AmazonAPI
from amazon.api import LookupException, AsinNotFound
```

1. Edit here<br>
```python
ACCESS_KEY = "ここにアクセスキーを入力"
SECRET_ACCESS_KEY = "ここにシークレットアクセスキーを入力"
ASSOCIATE_TAG = "ここにアソシエイトタグを入力"
```
2. Here, get informations by using API (The most important code)
```python
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
```



# Licence

# Author
Shuto Kawabata
