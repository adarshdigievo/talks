from mongoengine import Document, StringField, ObjectIdField


class FlightBookingsModel(Document):
    meta = {'collection': 'flight_bookings'}

    carrier = StringField(required=True)
    flight_number = StringField(required=True)
    _departure_airport = StringField(required=True)
    _ordered_by = ObjectIdField(required=True)
