from django.conf import settings


def get_tiltify(*args, **kwargs):
    """ Easy way to get a Tiltify obj """
    from tiltify2.tiltify import Tiltify2
    return Tiltify2(
        api_key=settings.TILTIFY_TOKEN,
        timeout=settings.TILTIFY_TIMEOUT,
        **kwargs
    )
