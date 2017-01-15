import requests
from bs4 import BeautifulSoup

# PARAMETERS FOR REFINING DEALS
MIN_DISCOUNT = 20 # 20% off minimum
MAX_DISCOUNT = 100 # 100% off maximum
MIN_PRICE = 0 # $0.00 minimum price
MAX_PRICE = 10 # $10.00 maximum price

host = "https://app.jumpsend.com"
pastDeals = []

class Deal:
    url = ""
    price = 0.0
    discount = 0.0
    shipping = ""
    retail = ""
    img_src = ""

    def __init__(self, url, price, discount, shipping, retail, img_src):
        self.url = url
        self.price = price
        self.discount = discount
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
        if link is None: # 
            continue
        else:
            link = link['href']
        link = host + link # prepend host name to url
        if link in pastDeals: # deal was already discovered in past searches
            continue

        dealLinks.append(link)
        pastDeals.append(link)

    return dealLinks

# Method for scraping individual deal pages
def scrapeDeals(dealLinks):
    if not dealLinks:
        print "Error scraping deals"
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

        shipping = soup.find('div', {'class':'product-shipment-cost-show'})
        if shipping is None: # shipping info not found
            shipping = ""
        else:
            shipping = shipping.get_text().strip()

        retail = soup.find('strong').parent
        if retail is None: # retail price not found
            retail = ""
        else:
            retail = retail.get_text().strip()
            
        img_src = soup.find('img', {'class':'img-responsive'})
        if img_src is None: # image src not found
            img_src = ""
        else:
            img_src = img_src['src']

        D = Deal(link, price, discount, shipping, retail, img_src)
        Deals.append(D)

    return Deals

dealLinks = getLinks()
NewDeals = scrapeDeals(dealLinks)
for Deal in NewDeals:
    print "price: $" + str(Deal.price)
    print "discount: " + str(Deal.discount) + "%"
