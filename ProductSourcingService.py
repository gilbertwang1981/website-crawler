from flask import Flask
from flask_cors import CORS
import SourcingProduct
from flask import request
import json

app = Flask('1688-sourcing-service')
CORS(app)


@app.route('/health', methods=['GET'])
def health_check():
    return "OK"


@app.route('/sourcing/create', methods=['POST'])
def create_sourcing():
    data = request.get_json()

    SourcingProduct.publishSourcing(data['userName'], data['subject'], data['amount'],
                                    data['price'], data['desc'], data['cone'],
                                    data['ctwo'], data['cthree'], data['aone'],
                                    data['atwo'], data['athree'])

    return "SUCCESS"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10016, debug=False)


