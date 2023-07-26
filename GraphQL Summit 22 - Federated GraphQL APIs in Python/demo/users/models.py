from mongoengine import Document, StringField, DateField


class UserModel(Document):
    meta = {'collection': 'users'}
    email = StringField(required=True)
    name = StringField(required=True)
    dob = DateField(required=True)
