import os
import json
import time

import requests

REFRESH_TIME = 10


def get_iikobiz_token(login, password):
    url = "https://iiko.biz:9900/api/0/auth/access_token?user_id=%s&user_secret=%s" % (login, password)
    token_response = requests.get(url)
    token = json.loads(token_response.text)
    return token


def get_nomenclature(token, orgId):
    url = "https://iiko.biz:9900/api/0/nomenclature/%s?access_token=%s" % (orgId, token)
    nomenclature_response = requests.get(url)
    nomenclature = json.loads(nomenclature_response.text)
    return nomenclature


def demo_order(nomenclature, org_id, address):
    products = nomenclature['products']

    product = next(product for product in products if (not product['modifiers'] and not product['groupModifiers']))
    if not product:
        raise NameError('No product without modifiers')

    order = {
        "organization": org_id,
        "customer": {
            "name": "Иван",
            "phone": "71235678901"
        },
        "order": {
            "phone": "71235678901",
            "isSelfService": "true",
            "items": [
                {
                    "id": product['id'],
                    "name": product['name'],
                    "amount": 10,
                    "code": product['code'],
                    "sum": product['price'],
                }
            ]
        }
    }
    if 'street' in address:
        order['order']['isSelfService'] = False
        order['order']["address"] = {
            "street": address['street'],
            "home": address['home'],
        }

        if 'city' in address:
            order['order']["address"]['city'] = address['city']

    else:
        order['order']['isSelfService'] = True

    if 'delivery_terminal_id' in address:
        order['deliveryTerminalId'] = address['delivery_terminal_id']

    return order


def check_status(check_order_response):
    try:
        json_response = json.loads(check_order_response.text)
        if not json_response['problem']:
            return "success"
        return "fail"
    except Exception as err:
        return "fail"


def check_order(nomenclature, token, orgId, address):
    url = "https://iiko.biz:9900/api/0/orders/checkCreate?access_token=%s" % (token)

    order = demo_order(nomenclature, orgId, address)

    check_order_response = requests.post(url, json=order)

    status = check_status(check_order_response)
    status_code = 200 if 'success' == status else 500
    return {
        'order': order,
        'status': status,
        'status_code': status_code,
        'response': check_order_response.text

    }


def html_response(template, args, status=200):
    path = os.path.dirname(__file__)
    with open(path + '/' + template, 'r') as file:
        html = file.read().replace('\n', '')

    if args:
        args['refresh_time'] = REFRESH_TIME
        args['timestamp'] = time.time()
        html = html.format(**args)

    return {
        'statusCode': status,
        'headers': {
            'Content-type': 'text/html; charset=utf-8'
        },
        'isBase64Encoded': False,
        'body': html
    }


def handler(event, context):
    if 'login' not in event['queryStringParameters']:
        return html_response('home.html', {}, status=200)

    login = ''
    if 'login' in event['queryStringParameters']:
        login = event['queryStringParameters']['login']
    password = ''
    if 'password' in event['queryStringParameters']:
        password = event['queryStringParameters']['password']

    org_id = ''
    if 'org_id' in event['queryStringParameters']:
        org_id = event['queryStringParameters']['org_id']

    address = {}
    if 'street' in event['queryStringParameters']:
        address['street'] = event['queryStringParameters']['street']

    if 'home' in event['queryStringParameters']:
        address['home'] = event['queryStringParameters']['home']

    if 'city' in event['queryStringParameters']:
        address['city'] = event['queryStringParameters']['city']

    if 'delivery_terminal_id' in event['queryStringParameters']:
        address['delivery_terminal_id'] = event['queryStringParameters']['delivery_terminal_id']

    token = get_iikobiz_token(login, password)
    nomenclature = get_nomenclature(token, org_id)
    check_result = check_order(nomenclature, token, org_id, address)

    args = {'login': login,
            'token': token,
            'nomenclature': nomenclature,
            'check_result': check_result
            }
    return html_response('status.html', args, status=check_result['status'])
