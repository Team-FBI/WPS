from django.db import models

# Create your models here.
class Country(models.Model):

    name = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(
        Country, related_name="cities", on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.name

