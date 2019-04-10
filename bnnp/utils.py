import base64
import json
import requests
import rsa
import time,datetime,collections

import urllib

api_url = 'http://openapi.bananapay.cn/gateway'
app_id = '2153135e8a1c572a'
public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0c+XGUXqHTgY2+c8+Jh8Ify3F+KWdocxMcYFzvnOEtyLuDcDHE2ZuH38ifpuFYmN+G9b+gveBnUiY2fRsxiNYjQNsi3EeQwJ5ACBeX6yLzLJm9hE+QMTZVbukpIpOyEfSorUlmAbLkP1mhUSxWoO0AwrVZ32aC0vrCrUEbHQ2N1xm8lfvE+hF7QGxXcVJxtunAKprCjDk2WMSNCiVVaeQ+ljI/oxe0bJ0nUTylgMYd3arCkqJv6PKseJuwyLV8U84nXblsGzLFF/M57PdKuigxEm2Hvx3bWEloQPK6vhn6js6+JaY25rVdhPd6ulMd1d4bS3cHSqgaVHrQoxSxgfVQIDAQAB
-----END PUBLIC KEY-----"""

private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAmYAlQNxLBgRQH8PqVLyj3KWH/qNRwF2kIS9iDT/ZFnd1QpCO
BR9pp/9iYQJ86l6qN4bVa7eLcSPnnVVJzJ97RBm0e17trXOK7/COQUtzhMI82XBh
9zcqWCN8cE/li/uQK6vRBccqg0BBEbJ0TDJ5KkINXQf1MTc5ZAF8kEHIy/N/IxQV
FJkE+CflFPY1ua06s6p6pzZ6bPxChl72vb2qsBcf41+NkyMNRqcyD20rjf/eObW2
TRj519c/ScWcEBKwFhf4sFuAkG5KWPtpI+22ABiVNc0HFJOzXqhgPCqwSsmBWYoC
p/DaiA9yveaYhb66LA/oG9IjmyPDDE3ZPujAfwIDAQABAoIBACjSeJXQQC+AdCKO
gsI4TMfASfOBUZt8C8s7g7MMWNptuISUVwCrwviHpY0xETFvLYuI0zdLX80eBFnG
NdMyUqDgySvKKiFnyfpXmi1pOHaFBZO6HIOXay53eX+Q7/YTV9sVXYhQ2FCBhQyE
zgL5pVmEqXMlS6LkEeIztwHSTOlYFN8TecxxAZg0srJdNXTHoW2qHyA52bAjnM2a
088kl5fpOQDSAm74SLy70QLmMWqQN+i09vJW/oIrq7QFJaBWwv8KkpFf/7EkTrGN
J0kirNgQW8DGtFcuHejJFj6Km6O/skOF+J2qTghNRVfnrBw3pkiQZujMIZC3k8UX
RCJdQAECgYEA5OIAL3Dqckf8mywlbdPo1E1N7oB0xq3D89p5kJt6GpHrvYRTHK3p
M2E9ke8dv+pLiUnJ47+By47btcKpTkv0o50KM+pBpGNVGnlMZYXutsMry5FHWW1W
hntnjZtgrlmaYDinoCq55h5JZY+EjWMxGxQyo+fVC0zFAfCWpc72IH8CgYEAq6/O
gxF+Vie2NfZFc5oyAAEboP0heGCnNCu7i9p93TkrRJzIYxL71496jMz++ADNqXQ4
JbLEZKiDAgx3cvMKVRCNyB+d9uRRjEOu01j93cg9PMf8xKvb6LTpgE5vSnPNDm1c
tKj4zILfCpBpW6R1d32kqn0PyaN4pHTfS9q9YAECgYAbduL+zlXTkL/G/u0e2Ka/
kucfD1rz3DX/NOARchacyZW4EADJGDU7bReuQzsWpE6cErafFYPFoUbL8KfQNV0N
pPJseFeYGjNEEfoQ1JloZNMEglJFcNFJIdWzMEnRof7cPPAgUAAulMPJ5AbL0HM8
BJhvAoqV6IhbSztIeiUekQKBgQCmM3v0L/QgTTM8C9rx7RxoGqp3b3R+Rvq2K3vU
CEB97wDu2+O03UTFSVU2hqBwzr5JQ4OzItqyItsoGY9szNB8xpiqWcken6o94auV
V3nywAxgEa2lakVpgfDlT4i3B2FDjSUIkua/fBWU8XW8zHkWop/Ml2K4LTL16Vnc
4bUgAQKBgF3pWniz1Ro/bZKDKOemt0abbvj8QvozHDV8H4w/80pXpowHgf9HXRYX
Hv/JYg5aKTIbcIWVT21FyiueFwZDCbdewlZyWjRUtLmJ3wTXMHuOkewlUU4OAFcM
yILcT26Jrpo31cDhd53ddy3TPjdysIOl+ZnL5ZX2XkDXfxO9A9Ws
-----END RSA PRIVATE KEY-----"""


def sign_with_rsa(private_key, sign_content, charset):

    sign_content = sign_content.encode(charset)
    
    signature = rsa.sign(sign_content, rsa.PrivateKey.load_pkcs1(private_key, format='PEM'), 'SHA-256')
    sign = base64.b64encode(signature)
    sign = str(sign, encoding=charset)

    return sign

def get_sign_content(all_params):
    sign_content = ""
    for (k, v) in sorted(all_params.items()):
        value = v
        if not isinstance(value, str):
            value = json.dumps(value, ensure_ascii=False)
        sign_content += ("&" + k + "=" + value)
    sign_content = sign_content[1:]
    return sign_content

def TradeCreate(auth_code, app_id):

    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json'}
    ts = int(time.time())
    ts = datetime.datetime.fromtimestamp(ts)
    # print(ts)

    data = collections.OrderedDict()
    data['app_id'] = app_id

    biz_content = {}
    biz_content['out_trade_no'] = "20150320010101001"
    # biz_content['seller_id'] = 'SP00000169'
    biz_content['total_amount'] = 100
    biz_content['subject'] = "test"
    biz_content['buyer_id'] = GetBuyerID(auth_code)

    data['biz_content'] = biz_content

    data['charset'] = 'utf-8'
    data['format'] = 'JSON'
    data['method'] = 'bananapay.trade.create'
    data['notify_url'] = 'www.baidu.com'
    data['sign_type'] = 'RSA2'
    data['timestamp'] = str(ts)
    
    data['version'] = '1.0'
    sign_content = get_sign_content(data)
    # print(sign_content)

    sign = sign_with_rsa(private_key,sign_content,'utf-8')

    data['sign'] = sign

    url = api_url + '?' + urllib.parse.urlencode(data).replace('%27','%22')
    print(url)
    url = url.replace('%27','%22')
    # print(url)
    # print('\n')
    result = requests.post(url)
    r = result.content.decode("utf-8")
    print(r)
    return(r)

def verify_with_rsa(public_key, message, sign):
    public_key = public_key
    sign = base64.b64decode(sign)
    pk = rsa.PublicKey.load_pkcs1_openssl_pem(public_key)
    print(pk)
    return bool(rsa.verify(message, sign, pk))

def GetBuyerID(code):
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json'}
    ts = int(time.time())
    ts = datetime.datetime.fromtimestamp(ts)

    data = collections.OrderedDict()
    data['app_id'] = app_id

    biz_content = {}
    biz_content['grant_type'] = "authorization_code"
    biz_content['code'] = code

    data['biz_content'] = biz_content

    data['charset'] = 'utf-8'
    data['format'] = 'JSON'
    data['method'] = 'bananapay.system.oauth.token'
    data['sign_type'] = 'RSA2'
    data['timestamp'] = str(ts)
    data['version'] = '1.0'
    sign_content = get_sign_content(data)
    # print(sign_content)

    sign = sign_with_rsa(private_key,sign_content,'utf-8')

    data['sign'] = sign

    url = api_url + '?' + urllib.parse.urlencode(data).replace('%27','%22')
    
    url = url.replace('%27','%22')
    
    result = requests.post(url)
    r = result.content.decode("utf-8")
    print(r)
    try:
        openid = json.loads(r)['bananapay_system_oauth_token_response']['openid']
    
        return(openid)
    except:
        return ''