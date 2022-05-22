from flask import Flask, json,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema,fields
from datetime import datetime

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://postgres:potterdursley@127.0.0.1/URL_DATABASE'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


db=SQLAlchemy(app)


class Urls(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    status_code = db.Column(db.Integer(), nullable=True)
    last_update = db.Column(db.DateTime(), nullable=True)

    def __int__(self, id, url, status_code, last_update):
        self.id = id
        self.url = url
        self.status_code = status_code
        self.last_update = last_update

    def __repr__(self):
        return self.id

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_if_test(cls):
        lst = cls.query.all()
        return list(filter(lambda k: 'test' in k.url, lst))

    @classmethod
    def get_if_no_status(cls):
        lst = cls.query.all()
        return list(filter(lambda k: k.status_code is None, lst))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UrlSchema(Schema):
    id=fields.Integer()
    url=fields.String()
    status_code=fields.Integer()
    last_update=fields.DateTime()


@app.route('/urls', methods=['GET'])
def get_all_urls():
    urls = Urls.get_all()

    serializer = UrlSchema(many=True)

    data = serializer.dump(urls)

    return jsonify(
        data
    )


@app.route('/urls',methods=['POST'])
def create_a_url():
    data=request.get_json()

    new_url=Urls(
        url=data.get('url'),
        status_code=data.get('status_code'),
        last_update=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )

    new_url.save()

    serializer=UrlSchema()

    data=serializer.dump(new_url)

    return jsonify(
        data
    ), 201


@app.route('/url/<int:id>',methods=['GET'])
def get_url(id):
    url=Urls.get_by_id(id)

    serializer=UrlSchema()

    data=serializer.dump(url)

    return jsonify(
        data
    ), 200


@app.route('/urltest',methods=['GET'])
def get_urls_if_test():
    urls=Urls.get_if_test()

    serializer=UrlSchema(many=True)

    data=serializer.dump(urls)

    return jsonify(
        data
    )


@app.route('/urlstatus',methods=['GET'])
def get_urls_no_status():
    urls=Urls.get_if_no_status()

    serializer=UrlSchema(many=True)

    data=serializer.dump(urls)

    return jsonify(
        data
    )


@app.route('/url/<int:id>',methods=['PUT'])
def update_url(id):
    url_to_update=Urls.get_by_id(id)

    data=request.get_json()

    url_to_update.status_code=data.get('status_code')
    url_to_update.last_update=datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    db.session.commit()

    serializer=UrlSchema()

    url_data=serializer.dump(url_to_update)

    return jsonify(url_data), 200


@app.route('/url/<int:id>',methods=['DELETE'])
def delete_url(id):
    url_to_delete=Urls.get_by_id(id)

    url_to_delete.delete()

    return jsonify({"message":"Deleted"}), 204


@app.errorhandler(404)
def not_found(error):
    return jsonify({"message":"Resource not found"}), 404

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message":"There is a problem"}), 500

if __name__ == '__main__':
    app.run(debug=True)