from django import template
from ..models import Song

register = template.Library()

@register.simple_tag
def is_favorite(user, id):
    song = Song.objects.filter(song_id=id, user=user).first()
    if song is not None:
        return True
    else:
        return False