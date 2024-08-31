from random import randint

from django.utils import timezone


def password_generator():
    """
        generate integer password with 6 digits 
        - return : integer
    """
    return randint(100000, 999999)


def five_minute_later():
    """
        returning the date time (five minute later) for OPT code expire time that sended to user
        - return : date time
    """
    return timezone.now() + timezone.timedelta(minutes=5)


def five_minute_ago():
    """
        returnin the date time (five minute ago) for saving the default value for OPT code sent time
        - return : date time
    """
    return timezone.now() - timezone.timedelta(minutes=5)