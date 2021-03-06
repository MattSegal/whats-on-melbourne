from django.db import models
from django.utils.text import slugify


class Source(models.Model):
    name = models.CharField(max_length=255)
    scraper = models.CharField(max_length=255)
    scraped_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):
    EVENT_TYPES = (
        ("TRIVIA", "Trivia"),
        ("JAZZ", "Jazz"),
        ("ARTS", "Arts and Theatre"),
        ("HIPHOP", "Hip-Hop"),
        ("EDM", "Electronic Dance Music"),
        ("ROCK", "Rock"),
        ("FOLK", "Folk"),
        ("COMEDY", "Comedy"),
        ("POKER", "Poker"),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    starts_at = models.DateTimeField()
    artist = models.CharField(max_length=255)
    price = models.IntegerField(null=True, blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(
        max_length=15, choices=EVENT_TYPES, null=True, blank=True
    )
    details_url = models.URLField(max_length=255, blank=True, null=True)
    show_search = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
