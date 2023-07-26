import logging

import graphene
from graphene.relay import Node
from graphene_federation import build_schema, external, extend
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from graphql import GraphQLResolveInfo

from models import FlightBookingsModel
import airportsdata

airports = airportsdata.load('IATA')


@extend(fields='id')
class UserType(graphene.ObjectType):
    id = external(graphene.ID(required=True))


class AirportType(graphene.ObjectType):
    name = graphene.String(required=True)
    code = graphene.String(required=True)


class FlightBookingType(MongoengineObjectType):
    class Meta:
        model = FlightBookingsModel
        interfaces = (Node,)
        exclude_fields = ('_departure_airport', '_ordered_by')
        required_fields = ('_departure_airport', '_ordered_by')

    departure_airport = graphene.Field(AirportType, required=True)
    ordered_by = graphene.Field(UserType, required=True)

    @staticmethod
    def resolve_departure_airport(root: FlightBookingsModel, info: GraphQLResolveInfo):
        airport_code = root._departure_airport
        return AirportType(code=airport_code, name=airports[airport_code]['name'])

    @staticmethod
    def resolve_ordered_by(root: FlightBookingsModel, info: GraphQLResolveInfo):

        return UserType(id=root._ordered_by)


class Query(graphene.ObjectType):
    flights_query = MongoengineConnectionField(FlightBookingType)


schema = build_schema(query=Query)
