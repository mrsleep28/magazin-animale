from django.conf import settings
from django.utils import timezone


def date_firma(request):
    return {
        "firma": settings.FIRMA,
        "an_curent": timezone.now().year,
    }