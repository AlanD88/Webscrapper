
import urllib2
from bs4 import BeautifulSoup
import urllib
import csv
import os
import random
import time


def download_image(url, name):
    path = "C:/Users/aland/Desktop/webscrapper"
    fullfilename = os.path.join(path, name)
    #urllib.urlretrieve(url, fullfilename)
    #name = path + name
    image = urllib.URLopener()
    image.retrieve(url, fullfilename)


def get_image_url(soup):
    image = soup.findAll('img', {"src": True})
    prImage = ''

    for i in image:
        s = str(i['src'])
        if s[1] == "/":
            prImage = s

    prImage = list(prImage)
    prImage = prImage[2:]
    prImage = ''.join(prImage)
    prImage = 'http://' + prImage
    imagetitle = title
    imagetitle += ".jpg"  # Add image extension

    download_image(prImage, imagetitle)

def product_sku(soup):
    sku = ' '
    checksku = soup.find("span", class_="item-number")
    try:
        for sk in checksku.find('span'):
            sku = str(sk)
    except:
        sku = random.randint(11111, 88888)
    return sku


def product_price():
    price = random.uniform(50.0, 2000.00)
    price = float("{0:.2f}".format(price))  # Round to 2 decimal places

    return price


def product_specs(soup):
    productSpecs = soup.findAll("div", class_="product-info-specs")
    specs=''
    for ps in productSpecs:
        specs = str(ps.text)
    return specs.strip().lower().split()


def product_features(soup, brand, sku):
    ls = soup.findAll("ul", class_="pdp-features")

    feature_ls = []
    for line in ls:
        new_line = ''
        for letter in line.text:
            #print letter
            l = ''
            try:
                l = str(letter)
            except:
                print "Letter in description not convertible"
                l = ''
                pass
            new_line += l
        #print new_line
        if new_line[0] == '\n':
            if new_line[-2] == '\n':
                new_line = new_line[1:-2]
            else:
                new_line = new_line[1:]
        #print "line: {}".format(new_line)
        feature_ls.append(new_line)
        #print "feature_list: {}".format(feature_ls)
    features = ".  ".join(feature_ls)

    p_i.append(product_id)  # ID
    p_i.append(title)
    p_i.append(features)
    p_i.append(brand)
    p_i.append(random.choice(['brian.jones', 'alan.duncan', 'amir.shahinpour', 'victor.shahbazian', 'bereket.haile']))
    p_i.append(sku)
    product_info.append(p_i)

def consolidate_product_data(specs):
    size = ''
    length = ''
    width = ''
    height = ''
    brand = ''
    weight = ''
    model = ''
    color = ''
    unit = ''
    for detail in range(len(specs)):
        if specs[detail] == "brand:":
            brand = specs[detail + 1]  # Product brand
        if specs[detail] == "dimensions:":
            count = 0
            dim = detail + 1
            while True:
                test = specs[dim]
                if test[0].isdigit():  # sometimes dimensions contain float values
                    if count == 0:
                        length = test
                    elif count == 1:
                        width = test
                    elif count == 2:
                        height = test
                    count += 1
                dim += 1
                if count == 3:  # Only need to grab 3 dimensions.  No 4D products
                    False
                    break
                    # size = specs[detail+1: detail+9]
                    # size = ''.join(size)
        if specs[detail] == "weight:":
            weight = specs[detail + 1]
            unit = specs[detail + 2]  # Product weight
        if specs[detail] == "lb.":
            if weight.isalpha() or weight == '':  # Checks if weight was word and not an actual weight value
                weight = specs[detail - 1]
                unit = specs[detail]
        if specs[detail] == "model:":
            model = specs[detail + 1]  # product model
        if specs[detail] == "color:":
            color = specs[detail + 1]
        if specs[detail] == "height:":
            height = specs[detail + 1]
        if specs[detail] == "width:":
            width = specs[detail + 1]
        if specs[detail] == "depth:":
            length = specs[detail + 1]

    # Build list in proper order
    data.append(product_id)  # ID
    data.append(title)  # Product title
    data.append(price)  # Product Price
    data.append(color)  # product Color
    color_code = gen_hex_color_code()
    data.append(color_code)  # Color Code,
    data.append(color)  # Color group, same because not supplied by site
    data.append('')  # Size name not supplied by costco
    data.append('')  # Size order not supplied by costco....what even is it?
    data.append(length)
    data.append(width)
    data.append(height)
    data.append(unit)  # Weight unit
    data.append(weight)  # Weight
    all_data.append(data)
    return brand

def gen_hex_color_code(): # Generate a random hex code since costco doesnt give me one.
    return ''.join([random.choice('0123456789ABCDEF') for x in range(6)])


################################################### Costco WebScraper #################################################


file_data = 'websites.txt'
websites = open(file_data, 'r')
all_data = []
product_info = []

data_titles = ['product_info_id', 'title', 'price', 'color', 'color_code', 'color_group', 'size_name', 'size_order',
               'length', 'width', 'height', 'unit', 'weight']
product_titles = ['product_info_id', 'title', 'description', 'manufacturer', 'created_by', 'UPC']
all_data.append(data_titles)
product_info.append(product_titles)
run = 1

# Single test site
#websites = ["http://www.costco.com/Bighorn-Ultimate-Access-Gun-Safe-Model-UAB7144EX-.product.100285126.html"]
total = 0
product_id = 10
for site in websites:  # Read through each website
    total += 1
    print "Total runs: {}".format(total)
    try:
        page = urllib2.urlopen(site)
    except:
        print "URL broken: {}".format(site)
        continue
    productTrue = True
    soup = BeautifulSoup(page, 'html.parser')
    data = []
    p_i = []
    #  Product title
    title = ' '

    memberOnly = soup.find('p', class_="member-only")
    not_member = True
    if memberOnly is not None:
        for m in memberOnly:
            m = str(m)
            m = m.lower().strip()
            if m == "member only item":
                not_member = False
                sleepy = random.randint(5,9)
                print "member only item"
                time.sleep(sleepy)

    if not_member:
        product_id += 1
        for div in soup.findAll('h1'):
            #title = u' '.join(div.text).encode('utf-16').strip()
            for letter in div.text:
                let = ''
                try:
                    let = str(letter)
                except:
                    print "letter in title not convertible"
                    let = ''
                    pass
                title += let
            if title is None:
                productTrue = False
                break
            # try:
            #     title = str(div.text)
            # except:  # If title breaks don't even bother processing rest of page
            #     productTrue = False
            #     print "Not convertable title"
            #     break
            title = title.strip()
            title = title.translate(None, '></\\":?*|')
            break
        if productTrue:
            ##########################################################
            # Product sku
            sku = product_sku(soup)
            ############################################################
            # Product Price  //// Costco price element wont fetch, returns empty '--'
            price = product_price()
            ###########################################################
            # Get initial product image from page then use google image scrapper using product model
            # try:
            #     get_image_url(soup)
            # except:
            #     print "Failed to get image"
            #     continue
            ##########################################################
            # Get product specs
            specs = product_specs(soup)
            #print specs
            # print specs # Printing specs gives you the product specifications as a complete list.  Use to see how to iterate through data
            brand = consolidate_product_data(specs)
            #################################################################
            # Get product features/description
            product_features(soup, brand, sku)

            sleepy = random.randint(5, 10)
            print "Sleep for: {} seconds".format(sleepy)
            time.sleep(sleepy)
            run +=1
            print "Continue, processed runs: {}".format(run)

with open("product.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(all_data)
f.close()
with open("product_info.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(product_info)
f.close()

websites.close()
