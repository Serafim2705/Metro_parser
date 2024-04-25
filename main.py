import requests
import csv

fields = ['name', 'id', 'url', 'promo_price', 'regular_price', 'manufacturer']
url = 'https://api.metro-cc.ru/products-api/graph'

# GraphQL-запрос
with open('query.txt', 'r', encoding='utf-8') as file:
    query = file.read()
    file.close()

# Параметры
size_per_req = 1000
variables = {
    "storeId": 10,
    "sort": "default",
    "size": size_per_req,
    "from": 0,
    "filters": [
        {
            "field": "main_article",
            "value": "0"
        }
    ],
    "attributes": [],
    "in_stock": True,
    "eshop_order": False,
    "allStocks": False,
    "slug": "pityevaya-voda-kulery"
}

# Заголовки
headers = {
    'Content-Type': 'application/json',
}
len_prod = size_per_req
csv_file = 'data.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fields, delimiter=";")
    writer.writeheader()
    while len_prod == size_per_req:

        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

        if response.status_code == 200:
            # print(response.json())
            product_data = response.json()['data']['category']['products']

            for product in product_data:

                if product.get('stocks')[0].get('prices').get('is_promo') is False:
                    regular_price = product.get('stocks')[0].get('prices').get('price')
                    promo_price = regular_price
                else:
                    regular_price = product.get('stocks')[0].get('prices').get('old_price')
                    promo_price = product.get('stocks')[0].get('prices').get('price')

                writer.writerow({"name": product.get('name'), 'id': product.get('id'),
                                 'url': product.get('url'), 'promo_price': promo_price,
                                 'regular_price': regular_price, 'manufacturer': product.get('manufacturer').get('name')})

                print(F"name: {product['name']}, id: {product['id']}, url: {product['url']}, "
                      F"promo_price: {promo_price}, regular_price: {regular_price},"
                      F" manufacturer: {product['manufacturer']['name']}")

            len_prod = len(response.json()['data']['category']['products'])
            variables['from'] += len_prod
            print("Нашлось записей: ", len_prod)
        else:
            print('Ошибка при выполнении запроса:', response.text)
