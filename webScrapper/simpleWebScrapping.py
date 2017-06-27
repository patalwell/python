import requests
from bs4 import BeautifulSoup

request = requests.get("https://www.amazon.com/All-New-Amazon-Echo-Dot-Add-Alexa-To-Any-Room/dp/B01DFKC2SO/ref=redir_mobile_desktop?_encoding=UTF8&ref_=ods_gw_ha_d_3pack")
content = request.content
soup = BeautifulSoup(content, "html.parser")
element = soup.find("span", {"id": "priceblock_ourprice", "class":"a-size-medium a-color-price"})
string_price = element.text.strip() #$49.99
price_without_symbol = string_price[01:] #$49.99, to remove the dollar sign we want to start on the second index of the string string_price
price = float(price_without_symbol)


def new_price():
    bid = 30.00
    if price <= bid:
        print (("The price of the Amazon Echo is now less or equal to your current {}").format(bid))
    else:
        print(("The Amazon Echo currently costs {}").format(price))
        print(("The Amazon Echo is still above your bid of {} dollars").format(bid))

new_price()

#<span id="priceblock_ourprice" class="a-size-medium a-color-price">$49.99</span>
