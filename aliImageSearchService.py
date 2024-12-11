import aliImageSearch
from flask import Flask
from flask_cors import CORS
import aliImageSearchConfig
from flask import request


app = Flask('1688-search-service')
CORS(app)


@app.route('/health', methods=['GET'])
def health_check():
    return "OK"


@app.route('/image/cookie/update/<string:userName>', methods=['POST'])
def updateCookie(userName):
    data = request.get_json()

    aliImageSearch.updateCookie(userName, data)

    return "OK"


@app.route('/image/search', methods=['POST'])
def search():
    data = request.get_json()

    targets = aliImageSearch.aliSearch(data['imageUrl'], data['userName'])

    return targets


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=aliImageSearchConfig.aliImageSearchConfig['aliImageSearch']['port'],
            debug=False)


