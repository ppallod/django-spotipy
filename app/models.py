from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Song(models.Model):

    class Meta:
            unique_together = ('song_id', 'user')        

    id = models.AutoField(primary_key=True)
    song_id = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete= models.CASCADE ,related_name="songs")
    name = models.CharField(max_length=64)
    artist = models.CharField(max_length=64)
    preview_url = models.URLField()
    image_url = models.URLField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"