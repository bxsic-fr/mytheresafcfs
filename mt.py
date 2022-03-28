import requests

from py_adyen_encrypt import encryptor

from selenium import webdriver

from requests.utils import dict_from_cookiejar

link = str(input("LINK of the product : "))

size = "DT 32 / XXS"

pid = link.split("/")[-1].split("-")[-1].split(".")[0]

# requests session
session = requests.Session()

session.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}

# request with session


first = session.get(link)

print("Session created")
# cookies = first.cookies
# headers = first.headers

category_id = first.text.split('"subCategoryID":"')[1].split('"')[0]

atc = "https://www.mytheresa.com/fr-fr/ajaxcart/cart/add/category_id/" # + category_id

formkey = first.text.split('<input name="form_key" type="hidden" value="')[1].split('"')[0]

z = first.text.split('<ul class="sizes">')[1].split("</ul>")[0]

a = z.split("<li>")
a.pop(0)

slist = {}

for i in a:
    slist[i.split("<a class=\"addtocart-trigger\" href=\"javascript:void(0);\" data-option=\"")[1].split("\"")[0]] =  i.split(">")[1].split("<")[0].replace("\n", "")

size_id = list(slist.keys())[list(slist.values()).index(size)]

"""form_key: eB6b2cIijyyDUylu
product: 2182805
related_product: 
super_attribute[142]: 2569"""

body = {
    "form_key": formkey,
    "product": pid,
    "related_product": "",
    "super_attribute[142]": size_id
}

session.post(atc + category_id + "/", data=body)

print("ATC")

onepagecheckout = session.get("https://www.mytheresa.com/fr-fr/checkout/onepage/")

print("Fpage checkout")

loginmethod = session.post("https://www.mytheresa.com/fr-fr/checkout/onepage/saveMethod/", data={"method": "guest"})

print("Saved method")

onepagecheckout2 = session.get("https://www.mytheresa.com/fr-fr/checkout/onepage/progress/?prevStep=login")

print("progress in checkout")

# fname, lname, email, houseno, street, postcode, city, country, phone

fname = "John"
lname = "Smith"
email = "John@mytheresa.com"
houseno = "2"
street = "Rue de la Paix"
postcode = "75155"
city = "Paris"
country = "France"
phone = "0466513245"

body = {
    "shipping[address_id]": "590372667",
    "shipping[same_as_billing]": "1",
    "shipping[prefix]": "M.",
    "shipping[suffix]": "",
    "shipping[firstname]": fname,
    "shipping[lastname]": lname,
    "shipping[company]": "",
    "billing[email]": email,
    "shipping[house_number]": houseno,
    "shipping[street][]": street,
    "shipping[street][]": "",
    "shipping[postcode]": postcode,
    "shipping[city]": city,
    "shipping[country_id]": country,
    "shipping[telephone]": phone,
    "shipping[save_in_address_book]": "1",
    "billing[use_for_shipping]": "1",
    "billing[address_id]": "",
    "billing[prefix]": "Mlle.",
    "billing[suffix]": "",
    "billing[firstname]": "",
    "billing[lastname]": "",
    "billing[company]": "",
    "billing[house_number]": "",
    "billing[street][]": "",
    "billing[street][]": "",
    "billing[postcode]": "",
    "billing[city]": "",
    "billing[country_id]": "FR",
    "billing[telephone]": "",
    "billing[save_in_address_book]": "1",
    "shipping_method": "mzups_standard",
    "is_eco_package": "1",
    "giftoptions[292997314][type]": "quote",
    "giftmessage[292997314][type]": "quote",
    "giftmessage[292997314][to]": "To",
    "giftmessage[292997314][from]": "From",
    "giftmessage[292997314][message]": "",
}

save_adrs = session.post("https://www.mytheresa.com/fr-fr/checkout/onepage/saveDelivery/", data=body)

print("Adress saved")


onepagecheckout3 = session.get("https://www.mytheresa.com/fr-fr/checkout/onepage/progress/?prevStep=delivery")

print(onepagecheckout3.status_code)

# adyen key :
"""
10001|BDDBC3D5D295D76130434778B66DC95CF149DDBEEA8FB8FAC22415FAE7EB02C9530DA04859786CB5D07278D3F9DFE46463A21F94B4DBBDF1C42AEC2F69BB60FC7409177ECC80ADB2117C075C408CFFB102C4DB22D6D96FC3D85ECF337A63355761B3A33B2B2AB00BC8E3BA02C498322132D1C88331FFA26CF9AF1509D1150DE3B1A4F551BF7E0E6799B23204CEE3050A4DE9FDEF3E7C1A613CD5A7A306EEA1EF77213CFEF181006D0A7D4BF2C738734FE272523DC77C288B47D16E4DC39519017199DFEDEB94FC9343864AC6A07B5F9EFBCA22D1BCA01DFC7019B3100E2D216A12A9F09FEDEB2AEAFA7D0C1E8F201D9DBF6E162160623EF502BC8151585C44BD
"""
ADYEN_KEY = "10001|BDDBC3D5D295D76130434778B66DC95CF149DDBEEA8FB8FAC22415FAE7EB02C9530DA04859786CB5D07278D3F9DFE46463A21F94B4DBBDF1C42AEC2F69BB60FC7409177ECC80ADB2117C075C408CFFB102C4DB22D6D96FC3D85ECF337A63355761B3A33B2B2AB00BC8E3BA02C498322132D1C88331FFA26CF9AF1509D1150DE3B1A4F551BF7E0E6799B23204CEE3050A4DE9FDEF3E7C1A613CD5A7A306EEA1EF77213CFEF181006D0A7D4BF2C738734FE272523DC77C288B47D16E4DC39519017199DFEDEB94FC9343864AC6A07B5F9EFBCA22D1BCA01DFC7019B3100E2D216A12A9F09FEDEB2AEAFA7D0C1E8F201D9DBF6E162160623EF502BC8151585C44BD"

cnum = "4143140003850207"
cvv = "561"
month = "08"
year = "2022"

enc = encryptor(ADYEN_KEY)

enc.adyen_version = '_0_1_25'

card = enc.encrypt_card(card=cnum, cvv=cvv, month=month, year=year)

b = {
    "payment[method]": "adyen_cc",
    "payment[cc_owner]": fname + ' ' + lname,
    "payment[encrypted_number]": card['card'],
    "payment[encrypted_expiry_month]": card['month'],
    "payment[encrypted_expiry_year]": card['year'],
    "payment[encrypted_cvc]": card['cvv'],
    "allValidcard": "true",
    "payment[screen_width]": "2560",
    "payment[screen_height]": "1440",
    "payment[color_depth]": "24",
    "payment[time_zone_offset]": "-60",
    "payment[language]": "fr-FR",
    "payment[java_enabled]": "false",
    "form_key": formkey,
}

savecard = session.post("https://www.mytheresa.com/fr-fr/checkout/onepage/savePayment/", data=b)

finalbeforepaiement = session.post("https://www.mytheresa.com/fr-fr/braintree/checkout/quoteTotal/")

ou = {
    "payment[method]": "adyen_cc",
    "payment[cc_owner]": fname + ' ' + lname,
    "payment[encrypted_number]": card['card'],
    "payment[encrypted_expiry_month]": card['month'],
    "payment[encrypted_expiry_year]": card['year'],
    "payment[encrypted_cvc]": card['cvv'],
    "allValidcard": "true",
    "payment[screen_width]": "2560",
    "payment[screen_height]": "1440",
    "payment[color_depth]": "24",
    "payment[time_zone_offset]": "-60",
    "payment[language]": "fr-FR",
    "payment[java_enabled]": "false",
    "form_key": formkey,
    "agreement[4]": "1",
    "order_comment": ""
}

payement = session.post("https://www.mytheresa.com/fr-fr/checkout/onepage/saveOrder/form_key/" + formkey, data=ou)

cookies = dict_from_cookiejar(session.cookies)

driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')

driver.get("https://www.mytheresa.com/fr-fr/adyen/process/validate3ds2/")

for key, value in cookies.items():
    driver.add_cookie({'name': key, 'value': value, 'domain': 'www.mytheresa.com'})
    
driver.get("https://www.mytheresa.com/fr-fr/adyen/process/validate3ds2/")

print("\n\n\n")
print("SUCCESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
print("\n\n\n")