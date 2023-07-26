import datetime

import mongoengine
from bson import ObjectId


def init_db():
    mongoengine.connect(host="mongodb://localhost:27017/usersDB")

    from models import UserModel
    UserModel.objects.delete()

    user = UserModel(name="John Doe",
                     email="john@example.com",
                     dob=datetime.date(1990, 12, 30),
                     pk=ObjectId('63131b4b629a1379dd00dcbe'))
    user.save()

    user = UserModel(name="Steve",
                     email="steve@example.com",
                     dob=datetime.date(1985, 5, 9),
                     pk=ObjectId('63131b4b629a1379dd00dcbf'))
    user.save()
