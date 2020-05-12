from django.db import models


# Create your models here.
class Maps(models.Model):
    id = models.AutoField(primary_key=True)
    graph = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'map'
