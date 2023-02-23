import graphene
from django.db import IntegrityError

from user.models import User
from user.schema import UserType


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
