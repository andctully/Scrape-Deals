import requests
import os
from time import sleep
from bs4 import BeautifulSoup

# PARAMETERS FOR SENDING EMAIL
SENDER = "" # sender's email
PASS = ""   # sender's email password
RCVR = ""   # receiver's email

# PARAMETERS FOR REFINING DEALS
MIN_DISCOUNT = 20 # 20% off minimum
MAX_DISCOUNT = 100 # 100% off maximum
MIN_PRICE = 0 # $0.00 minimum price
MAX_PRICE = 10 # $10.00 maximum price

host = "https://app.jumpsend.com"
pastDeals = []

WAIT_TIME = 300 # Interval between searches in seconds

class Deal:
    url = ""
    price = 0.0
    discount = 0.0
    title = ""
    shipping = ""
    retail = ""
    img_src = ""

    def __init__(self, url, price, discount, title, shipping, retail, img_src):
        self.url = url
        self.price = price
        self.discount = discount
        self.title = title
        self.shipping = shipping
        self.retail = retail
        self.img_src = img_src

# Method for collecting the links to deals from the main deal page
def getLinks():
    deals_url = host + "/deals"
    r = requests.get(deals_url)
    if r.status_code != 200:
        print "Error getting links"
        return False

    soup = BeautifulSoup(r.content, "html.parser")

    deals = soup.find_all('div', {'class':'deal'})
    dealLinks = []
    for deal in deals: 
        link = deal.find('a', href=True)
        if link is None: # unable to link to individual deal
            continue
        else:
            link = link['href'] # get url from href
        link = host + link # prepend host name to url
        if link in pastDeals: # deal is not new 
            continue

        dealLinks.append(link)
        pastDeals.append(link)

    return dealLinks

# Method for scraping individual deal pages
def scrapeDeals(dealLinks):
    if not dealLinks: # dealLinks is empty or an error occurred
        print "No new deals or an error occurred"
        return False

    Deals = []

    for link in dealLinks:
        r = requests.get(link)
        if r.status_code != 200:
            print "Error loading deal link"
            continue

        soup = BeautifulSoup(r.content, "html.parser")

        price1 = soup.find('span', {'class':'first-price'})
        if price1 is None: # first half of price not found
            continue
        price1 = price1.get_text().strip()

        price2 = soup.find('span', {'class':'second-price'})
        if price2 is None: # second half of price not found
            continue
        price2 = price2.get_text().strip()

        price = price1 + price2
        price = float(price[1:]) # remove $ and convert to float

        if price < MIN_PRICE or price > MAX_PRICE:
            continue # deal did not meet price requirements

        discount = soup.find('span', {'class':'discount'})
        if discount is None: # discount not found 
            continue
        discount = discount.get_text().strip()
        discount = float(discount[:2]) # remove % and convert to float

        if discount < MIN_DISCOUNT or discount > MAX_DISCOUNT:
            continue # deal did not meet discount requirements

        title = soup.find('h2')
        if title is None: 
            title = "Title not found"
        else:
            title = title.get_text()

        shipping = soup.find('div', {'class':'product-shipment-cost-show'})
        if shipping is None: # shipping info not found
            shipping = "Shipping information not found"
        else:
            shipping = shipping.get_text().strip()

        retail = soup.find('strong').parent
        if retail is None: # retail price not found
            retail = "Retail price not found"
        else:
            retail = retail.get_text().strip()
            
        img_src = soup.find('img', {'class':'img-responsive'})
        if img_src is None: # image src not found
            img_src = "Image src not found"
        else:
            img_src = img_src['src']

        D = Deal(link, price, discount, title, shipping, retail, img_src)
        Deals.append(D)

    return Deals

def emailDeals(Deals):
    if not Deals:
        print "No new deals to send"
        return False

    BODY = ""
    for Deal in Deals:
        title = Deal.title
        price = "${}".format(str(Deal.price))
        disc = "{}% OFF".format(str(Deal.discount))
        retail = Deal.retail
        ship = Deal.shipping
        url = Deal.url
        BODY += "{} \n {} \n {} \n {} \n {} \n {} \n \n".format(
                title, price, disc, retail, ship, url)

    SUBJECT = "You have {} new deals to check out on Jump Send!".format(len(Deals))

    os.system("python send_email.py '{}' '{}' '{}' '{}' '{}'".format(
        SENDER, PASS, RCVR, SUBJECT, BODY))
    
# MAIN FUNCTION
while True:
    print "Checking for deals..."
    dealLinks = getLinks()
    NewDeals = scrapeDeals(dealLinks)
    emailDeals(NewDeals)
    if NewDeals:
        print "{} new deals were found!".format(len(NewDeals))
    print "Waiting {} minutes to search again...".format(WAIT_TIME / 60.0)
    sleep(WAIT_TIME) 
