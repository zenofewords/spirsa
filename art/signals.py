from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from art.models import Artwork


@receiver(pre_save, sender=Artwork)
def update_ordering(sender, instance, **kwargs):
    other_artworks = Artwork.objects.filter(ordering__gte=instance.ordering)
    order = instance.ordering

    for index, artwork in enumerate(other_artworks):
        if order + index >= artwork.ordering:
            other_artworks.filter(pk=artwork.pk).update(ordering=F('ordering') + 1)
        if order + index < artwork.ordering:
            other_artworks.filter(pk=artwork.pk).update(ordering=F('ordering') - 1)
