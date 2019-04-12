from flask import Flask,request
from .utils import TradeCreate
import qrcode
import urllib
import requests

app = Flask(__name__)

my_view_url = 'https://bnnp.herokuapp.com/bnnppayment'

print(__name__)

app_id = '2153135e8a1c572a'
original_url = 'https://openauth.bananapay.cn/ToAuthPage?app_id=' + app_id + \
    '&scope=auth_base&redirect_uri=' + 'https%3a%2f%2fbnnp.herokuapp.com%2fbnnppayment'
print(original_url)



qr_code = qrcode.make(original_url)
qr_code.save("bnnp store.png")


@app.route('/bnnppayment',methods=['GET','POST'])
def index():

    app_id = request.args.get('app_id')
    app_id = '2153135e8a1c572a'
    auth_code = request.args.get('auth_code')
    scope = request.args.get('scope')
    print(app_id)
    print(auth_code)
    print(scope)
    TradeCreate(auth_code,app_id)

    return '<h1>11111</h1>'


@app.route('/notify',methods=['GET',"POST"])
def notify():
    print(request.args)
    return '<h1>notify</h1>'