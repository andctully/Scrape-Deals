import requests
from bs4 import BeautifulSoup

# PARAMETERS FOR REFINING DEALS
lowDiscount = 20 # 20% off minimum
highDiscount = 100 # 100% off maximum
lowPrice = 0 # $0.00 minimum price
highPrice = 10 # $10.00 maximum price

host = "https://app.jumpsend.com"
Deals = []

class Deal:
    url = ""
    price = "" 
    shipping = ""
    discount = ""
    retail = ""
    img_src = ""

    def __init__(self, url, price, shipping, discount, retail, img_src):
        self.url = url
        self.price = price
        self.shipping = shipping
        self.discount = discount
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
    deal_links = []
    for deal in deals: 
        link = deal.find('a', href=True)['href']
        deal_links.append(host + link)

    return deal_links

# Method for scraping individual deal pages
def scrapeDeals(deal_links):
    if not deal_links:
        print "Error scraping deals"
        return False

    for link in deal_links:
        r = requests.get(link)
        if r.status_code != 200:
            print "Error loading deal link"
            continue

        soup = BeautifulSoup(r.content, "html.parser")

        price = soup.find('span', {'class':'first-price'}).get_text().strip()
        price += soup.find('span', {'class':'second-price'}).get_text().strip()
        shipping = soup.find('div', {'class':'product-shipment-cost-show'}).get_text().strip()
        discount = soup.find('span', {'class':'discount'}).get_text().strip()
        retail = soup.find('strong').parent.get_text().strip()
        img_src = soup.find('img', {'class':'img-responsive'})['src']
        D = Deal(link, price, shipping, discount, retail, img_src)
        Deals.append(D)

deal_links = getLinks()
scrapeDeals(deal_links)
for D in Deals:
    print D.url
    print
