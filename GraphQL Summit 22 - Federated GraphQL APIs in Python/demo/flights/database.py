import mongoengine
from bson import ObjectId


def init_db():
    mongoengine.connect(host="mongodb://localhost:27017/flightsDB")

    from models import FlightBookingsModel
    FlightBookingsModel.objects.delete()

    flight = FlightBookingsModel(carrier="Emirates",
                                 flight_number="123",
                                 _departure_airport="TRV",
                                 _ordered_by=ObjectId('63131b4b629a1379dd00dcbe'))

    flight.save()

    flight = FlightBookingsModel(carrier="United Airlines",
                                 flight_number="456",
                                 _departure_airport="DXB",
                                 _ordered_by=ObjectId('63131b4b629a1379dd00dcbf'))

    flight.save()
