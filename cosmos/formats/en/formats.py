# Date and time formats for the site's language (LANGUAGE_CODE = "en").
# Formats not set here are Django's English defaults.

# Reference: https://docs.djangoproject.com/en/3.2/ref/templates/builtins/#date
# https://docs.djangoproject.com/en/3.2/ref/settings/#date-format
DATE_FORMAT = "d M Y"
# https://docs.djangoproject.com/en/3.2/ref/settings/#time-format
TIME_FORMAT = "H:i"
# https://docs.djangoproject.com/en/3.2/ref/settings/#datetime-format
DATETIME_FORMAT = "d M Y H:i"

DATETIME_INPUT_FORMATS = [
    "%d-%m-%Y %H:%M",  # 25-10-2006 14:30
    "%d-%m-%y %H:%M",  # 25-10-06 14:30
    "%d/%m/%Y %H:%M",  # 25/10/06 14:30
    "%d/%m/%y %H:%M",  # 25/10/06 14:30
    "%Y-%m-%d %H:%M:%S",  # '2006-10-25 14:30:59'
    "%Y-%m-%d %H:%M:%S.%f",  # '2006-10-25 14:30:59.000200'
    "%Y-%m-%d %H:%M",  # '2006-10-25 14:30'
    "%m/%d/%Y %H:%M:%S",  # '10/25/2006 14:30:59'
    "%m/%d/%Y %H:%M:%S.%f",  # '10/25/2006 14:30:59.000200'
    "%m/%d/%Y %H:%M",  # '10/25/2006 14:30'
    "%m/%d/%y %H:%M:%S",  # '10/25/06 14:30:59'
    "%m/%d/%y %H:%M:%S.%f",  # '10/25/06 14:30:59.000200'
    "%m/%d/%y %H:%M",  # '10/25/06 14:30'
]
