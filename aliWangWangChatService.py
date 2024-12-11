from flask import Flask
from flask import request
from flask_cors import CORS
import aliWangWangTxRx
import json
import aliCookieService
import aliWangWangConfig


app = Flask('1688-chat-service')
CORS(app)


@app.route('/health', methods=['GET'])
def health_check():
    return "OK"


@app.route('/aliWangWang/getDetail', methods=['POST'])
def get_detail():
    data = json.loads(json.dumps(request.get_json()))

    return json.dumps(aliWangWangTxRx.getProductDetail(data['offerId'], data['userName']), default=lambda o: o.__dict__)


@app.route('/aliWangWang/tx', methods=['POST'])
def send_chat():
    data = request.get_json()

    aliWangWangTxRx.chatWithCustomer(data['offerId'], data['chatList'], data['userName'])

    return "SUCCESS"


@app.route('/aliWangWang/rx', methods=['POST'])
def recv_chat():
    data = json.loads(json.dumps(request.get_json()))

    return json.dumps(aliWangWangTxRx.getChatHistory(data['offerId'], data['userName']), default=lambda o: o.__dict__)


@app.route('/aliWangWang/cookie/update/<string:userName>', methods=['POST'])
def update_ali_cookie(userName):
    data = request.get_json()

    aliCookieService.updateCookie(userName, data)

    aliWangWangTxRx.reloadChromePool()

    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=aliWangWangConfig.aliWangWangConfig['aliWangWang']['port'], debug=False)


