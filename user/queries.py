import graphene

from user.models import User
from user.schema import UserType


class UserQuery(graphene.ObjectType):
    get_users = graphene.List(UserType, username=graphene.String(), adventure_rank=graphene.Int())
    get_user = graphene.Field(UserType, uid=graphene.Int())

    @staticmethod
    def resolve_get_users(parent, info, username=None, adventure_rank=None):
        queryset = User.objects.all()

        if username is not None:
            queryset = queryset.filter(username=username)

        if adventure_rank is not None:
            queryset = queryset.filter(adventure_rank=adventure_rank)

        return queryset

    @staticmethod
    def resolve_get_user(parent, info, uid):
        return User.objects.filter(uid=uid).first()
