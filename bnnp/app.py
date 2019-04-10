from flask import Flask,request
from .utils import TradeCreate
import qrcode

app = Flask(__name__)

my_view_url = '/bnnppayment'

print(__name__)

app_id = '2153135e8a1c572a'
original_url = 'https://openauth.bananapay.cn/ToAuthPage?app_id=' + app_id + \
    '&scope=auth_base&redirect_uri=' + my_view_url + '&state=123456'

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

    return '<h1>Hello, World!</h1>'