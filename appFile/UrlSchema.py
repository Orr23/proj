from marshmallow import Schema,fields

class UrlSchema(Schema):
    id=fields.Integer()
    url=fields.String()
    status_code=fields.Integer()
    last_update=fields.DateTime()