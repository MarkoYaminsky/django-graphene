import graphene
from django.db import IntegrityError
from graphene_django.types import DjangoObjectType

from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User

    player_status = graphene.String()

    def resolve_player_status(self, info):
        wl = self.world_level
        if wl <= 4:
            return "Novice"
        elif wl < 7:
            return "Medium"
        else:
            return "Veteran"


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


class UserMutable(graphene.Mutation):
    class Arguments:
        uid = graphene.Int(required=True)
        world_level = graphene.Int(required=True)
        username = graphene.String(required=True)

    user = graphene.Field(UserType)
    status = graphene.String()

    @staticmethod
    def mutate(_, info, uid, world_level, username):
        ...


class UserCreateMutation(UserMutable):
    @staticmethod
    def mutate(_, info, uid, world_level, username):
        try:
            user = User.objects.create(uid=uid, world_level=world_level, username=username)
        except IntegrityError:
            return UserCreateMutation(user=None, status="error")
        return UserCreateMutation(user=user, status="success")


class UserUpdateMutation(UserMutable):
    @staticmethod
    def mutate(_, info, uid, **kwargs):
        user = User.objects.filter(uid=uid).first()
        if not user:
            return UserUpdateMutation(user=None, status="error")

        for key, value in kwargs.items():
            setattr(user, key, value)

        user.save()
        return UserUpdateMutation(user=user, status="success")


class UserDeleteMutation(graphene.Mutation):
    class Arguments:
        uid = graphene.Int(required=True)

    status = graphene.String()

    @staticmethod
    def mutate(_, info, uid):
        user = User.objects.filter(uid=uid).first()
        if not user:
            return UserDeleteMutation(status="error")
        user.delete()
        return UserDeleteMutation(status="success")


class UserMutation:
    create_user = UserCreateMutation.Field()
    update_user = UserUpdateMutation.Field()
    delete_user = UserDeleteMutation.Field()
