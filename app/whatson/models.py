from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


# class Event(models.Model):
#     performer = models.CharField(max_length=255)
#     price = models.IntegerField()
#     starts_at = models.DateTimeField()
#     venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
