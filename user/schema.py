import graphene
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
