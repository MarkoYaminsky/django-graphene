import graphene
from user import queries as uq, mutations as um


class Query(uq.UserQuery):
    pass


class Mutation(um.UserMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
