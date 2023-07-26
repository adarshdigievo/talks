import graphene
import graphene_federation
from graphene.relay import Node
from graphene_federation import key
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from graphql import GraphQLResolveInfo

from models import UserModel


@key(fields='id')
class UserType(MongoengineObjectType):
    class Meta:
        model = UserModel
        interfaces = (Node,)

    @staticmethod
    def __resolve_reference(reference, info: GraphQLResolveInfo):
        return UserModel.objects.get(pk=reference.id)


class Query(graphene.ObjectType):
    users_query = MongoengineConnectionField(UserType)


schema = graphene_federation.build_schema(query=Query)
