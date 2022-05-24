from flask import Flask, json,jsonify,request
from datetime import datetime
import sys
sys.path.insert(0,"..")
from appFile.UrlSchema import UrlSchema
from appFile.Urls import *

ID='id'
URL='url'
STATUS_CODE='status_code'


@app.route('/urls', methods=['GET'])
def get_all_urls():
    try:
        urls = Urls.get_all()
    except Exception as e:
        return jsonify({"message": "Couldn't find URLs"})

    serializer = UrlSchema(many=True)

    data = serializer.dump(urls)

    return jsonify(
        data
    )


@app.route('/urls',methods=['POST'])
def create_a_url():
    try:
        data = request.get_json()

        new_url=Urls(
            url=data.get(URL),
            status_code=data.get(STATUS_CODE),
            last_update=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )
    except Exception as e:
        return jsonify({"message": "No URL found"})

    new_url.add()

    serializer=UrlSchema()

    data=serializer.dump(new_url)

    return jsonify(
        data
    )


@app.route('/url/<int:id>',methods=['GET'])
def get_url(id):
    try:
        url=Urls.get_by_id(id)
    except Exception as e:
        return jsonify({"message": "URL does not exist"})

    serializer=UrlSchema()

    data=serializer.dump(url)

    return jsonify(
        data
    )


@app.route('/urltest',methods=['GET'])
def get_urls_if_test():
    try:
        urls=Urls.get_if_test()
    except Exception as e:
        return jsonify({"message": "Couldn't find Tests"})

    serializer=UrlSchema(many=True)

    data=serializer.dump(urls)

    return jsonify(
        data
    )


@app.route('/urlstatus',methods=['GET'])
def get_urls_no_status():
    try:
        urls=Urls.get_if_no_status()
    except Exception as e:
        return jsonify({"message": "Couldn't find status"})

    serializer=UrlSchema(many=True)

    data=serializer.dump(urls)

    return jsonify(
        data
    )


@app.route('/urls',methods=['PUT'])
def update_url():
    try:
        data=request.get_json()

        url_to_update = Urls.get_by_id(data.get(ID))
        url_to_update.status_code=data.get(STATUS_CODE)
        url_to_update.last_update=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    except Exception as e:
        return jsonify({"message": "Couldn't update URL"})

    db.session.commit()

    serializer=UrlSchema()

    url_data=serializer.dump(url_to_update)

    return jsonify(url_data)


@app.route('/url/<int:id>',methods=['DELETE'])
def delete_url(id):
    try:
        url_to_delete=Urls.get_by_id(id)

        url_to_delete.delete()
    except Exception as e:
        return jsonify({"message": "Couldn't delete URL"})

    return jsonify({"message":"Deleted"})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"message":"Resource not found"}), 404


@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message":"There is a problem"}), 500


if __name__ == '__main__':
    app.run(debug=True)