from django.conf import settings


def get_tiltify(*args, **kwargs):
    """ Easy way to get a Tiltify obj """
    from tiltify2 import Tiltify3
    return Tiltify3(
        api_key=settings.TILTIFY_TOKEN,
        timeout=settings.TILTIFY_TIMEOUT,
        extra_headers={
            'Remote-App-Name': settings.HEROKU_APP_NAME,
            'Remote-App-Version': settings.HEROKU_RELEASE_VERSION,
            'Remote-App-Owner': settings.TILTIFY_APP_OWNER,
        },
        **kwargs
    )
