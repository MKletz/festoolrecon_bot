import bs4 as bs
import requests, os, time

def calculate_discount(string_msrp,string_price):
    numeric_msrp = float(string_msrp.replace('$', '').replace(',', ''))
    numeric_price = float(string_price.replace('$', '').replace(',', ''))
    numeric_discount = numeric_msrp - numeric_price
    numeric_discount = '{0:.2f}'.format(round(numeric_discount,2))
    string_discount = ('$' + str(numeric_discount))
    return string_discount

def send_discord_webhook(message):
    webhook_url = os.environ['discord_webhook_url']
    data = {
        "content": message
    }

    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

url = 'https://www.festoolrecon.com/'
sleep = os.environ['interval']

while True:
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'html.parser')

    product_name = soup.find_all("h1", {"class": "product-single__title"})[0].text

    if product_name != os.environ.get('previous_product', 'none'):
        product_msrp = soup.find_all("s", {"id": "ComparePrice-product-template"})[0].text
        product_price = soup.find_all("span", {"id": "ProductPrice-product-template"})[0].text.replace('\n','').strip()
        product_discount = calculate_discount(product_msrp,product_price)

        webhook_str = f"""Festool Recon update!
        Product Name: {product_name}
        MSRP is: {product_msrp}
        Price is: {product_price}
        Discount is: {product_discount}

        {url}
        """

        send_discord_webhook(webhook_str)
        os.environ['previous_product'] = product_name
    time.sleep(sleep)
