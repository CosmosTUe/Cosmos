import re

from django.core.exceptions import ValidationError

PRETIX_HOST = "pretix.cosmostue.nl"

# A shop link (https://pretix.cosmostue.nl/<organizer>/<event>/...) or a back-office link
# (https://pretix.cosmostue.nl/control/event/<organizer>/<event>/...), with or without https://
_LINK = re.compile(
    r"^(?:https?://)?"
    + re.escape(PRETIX_HOST)
    + r"/(?:control/event/)?(?P<organizer>[\w.-]+)/(?P<event>[\w.-]+)(?:[/?#].*)?$"
)


def shop_url(link):
    """Returns the canonical shop address for a pretix link, or raises ValidationError."""
    value = (link or "").strip().replace(" ", "")
    match = _LINK.match(value)
    if not match or match["organizer"] == "control":
        raise ValidationError(
            "This doesn't look like a pretix shop link. Copy the address of the event's shop on %(host)s, "
            "for example https://%(host)s/cosmos/myevent/.",
            params={"host": PRETIX_HOST},
        )
    return f"https://{PRETIX_HOST}/{match['organizer']}/{match['event']}/"
