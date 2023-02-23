import graphene
import user.schema as us


class Query(us.UserQuery):
    pass


class Mutation(us.UserMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
