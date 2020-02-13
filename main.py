import json
import time
import requests


def page(login, check_result, token, nomenclature):
    timestamp = time.time()
    refresh_time = 10
    template = """
<html>
<head>
    <meta http-equiv="refresh" content="{refresh_time}" >
</head>

<body>
status: {login} <b>{status}</b>

<br/>

token: {token}

<br/>

time: {timestamp}
<br/>
nomenclature revision : {revision} 

<br/>

server response: {response}

<br/>
</body>

</html>
"""
    return template.format(refresh_time=refresh_time, login=login, status=check_result['status'], timestamp=timestamp,
                           token=token,
                           revision=nomenclature['revision'], response=check_result['response'])


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
    print(products)

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
                    "name": "Паста с говядиной",
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
            "home": address['home']
        }
    else:
        order['order']['isSelfService'] = True

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
        'status': status,
        'status_code': status_code,
        'response': check_order_response.text

    }


def handler(event, context):
    login = ''
    if 'queryStringParameters' in event and 'login' in event['queryStringParameters']:
        login = event['queryStringParameters']['login']
    password = ''
    if 'queryStringParameters' in event and 'password' in event['queryStringParameters']:
        password = event['queryStringParameters']['password']

    org_id = ''
    if 'queryStringParameters' in event and 'org_id' in event['queryStringParameters']:
        org_id = event['queryStringParameters']['org_id']

    address = {}
    if 'queryStringParameters' in event and 'street' in event['queryStringParameters']:
        address['street'] = event['queryStringParameters']['street']

    if 'queryStringParameters' in event and 'street' in event['queryStringParameters']:
        address['home'] = event['queryStringParameters']['home']

    token = get_iikobiz_token(login, password)
    nomenclature = get_nomenclature(token, org_id)
    check_result = check_order(nomenclature, token, org_id, address)

    return {
        'statusCode': check_result['status_code'],
        'headers': {
            'Content-Type': 'text/html',
            'Content-type': 'text/html; charset=utf-8'
        },
        'isBase64Encoded': False,
        'body': page(login, check_result, token, nomenclature)
    }
