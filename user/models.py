from django.db import models


class User(models.Model):
    uid = models.IntegerField(primary_key=True)
    world_level = models.SmallIntegerField()
    username = models.CharField(max_length=20)
    objects = models.Manager()

    def __str__(self):
        return self.username
