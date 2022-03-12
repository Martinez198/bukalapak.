# Process followed to extract product information from Bukalapak website


## Requirement
Need to capture the product information from the bukalapak website.
- Ref: https://www.bukalapak.com/


## Process followed
- We need to get the product information which are under handphone--> hpandsmartphones ---> search for the samsung in the search bar.
- To capture the samsung brand mobile phone products they are proving an API where all the information which is there in the UI is being provided.
	- Ref API: https://api.bukalapak.com/multistrategy-products?keywords=samsung&limit=50&offset=0&facet=true&page=1&shouldUseSeoMultistrategy=false&access_token=DSVhvXStYMoRFI5PL5vAxpV2MwjWpAO3mPT5cPRus_hsQg
- Note:  This access token may expire after few hours 
- We are making use of json API to capture the following information.
	- product_link
	- brand_name
	- product_location
	- product_price
	- product_rating
	- product_name

## Command to capture the data
```
python bukalapak.py --out-file product_info.json --csv-file product_details.csv
```
 -	`--out-file`:  Output file which stores data in the json format.
 -	`--csv-file`: Stores information in the CSV file.

### Output data links/sheets:
Round1: Extracting the information from the weblink:
-  Product details code link: https://github.com/jyothsna9797/bukalapak./blob/master/bukalapak.py
	- Product information CSV link: https://docs.google.com/spreadsheets/d/14vx0PE0nUzGKGR-vaQoeSaMrCpYizad80yqolH2PhuM/edit?usp=sharing
	- Json format product information: https://raw.githubusercontent.com/jyothsna9797/bukalapak./master/product_info.json

Round2: Providing links as an input and fixing the bugs in the file:
- Code link: https://raw.githubusercontent.com/jyothsna9797/bukalapak./master/Mainfile.py
- Output CSV link: https://docs.google.com/spreadsheets/d/17WaGLZcLePkdy6rzEM57d-eKHkQh-759jRzTP3QEG_Y/edit?usp=sharing
