import re

from django.db import migrations

# Event descriptions used to carry the pretix ticket widget as embed code (stylesheet, script, <pretix-widget> or the
# older <div class="pretix-widget-compat">, and a <noscript> fallback). The event page now renders the widget from
# Event.pretix_shop, so this moves the shop link into that field and removes the embed code from the description.
# The logic is kept in this file (not imported) so the migration stays as it is when app code changes later.

HOST = r"https?://pretix\.cosmostue\.nl"
_SHOP_IN_EMBED = re.compile(r"<(?:pretix-widget|div)\b[^>]*?\bevent=\"(" + HOST + r"/[^\"]+)\"", re.I)
_SHOP_IN_NOSCRIPT = re.compile(r"<noscript>.*?href=\"(" + HOST + r"/[^\"]+)\".*?</noscript>", re.I | re.S)
_SHOP = re.compile(HOST + r"/(?:control/event/)?([\w.-]+)/([\w.-]+)", re.I)
_PIECES = [
    re.compile(r"<link\b[^>]*\bhref=\"" + HOST + r"/[^\"]*widget/v1\.css\"[^>]*>", re.I),
    re.compile(r"<script\b[^>]*\bsrc=\"" + HOST + r"/widget/v1\.[a-z-]+\.js\"[^>]*>\s*</script>", re.I),
    re.compile(r"<pretix-widget\b[^>]*>\s*</pretix-widget>", re.I),
    re.compile(r"<div\b[^>]*\bclass=\"pretix-widget-compat\"[^>]*>\s*</div>", re.I),
    re.compile(r"<noscript>(?:(?!</noscript>).)*?pretix-widget(?:(?!</noscript>).)*?</noscript>", re.I | re.S),
]
_MARK = "\x00pretix-embed\x00"
_EMPTY_WRAPPER = re.compile(r"<(p|div)\b[^>]*>(?:\s|&nbsp;|\xa0|" + _MARK + r")*</\1>\n?", re.I)


def split_embed(html):
    """Returns (shop link or "", description without the embed code); unchanged if there is no embed."""
    found = _SHOP_IN_EMBED.search(html) or _SHOP_IN_NOSCRIPT.search(html)
    shop = _SHOP.match(found.group(1)) if found else None
    if not shop:
        return "", html
    out = html
    for piece in _PIECES:
        out = piece.sub(_MARK, out)
    if _MARK not in out:
        return "", html
    # remove paragraphs/divs that only held embed code, then the remaining markers
    while True:
        cleaned = _EMPTY_WRAPPER.sub(lambda m: "" if _MARK in m.group(0) else m.group(0), out)
        if cleaned == out:
            break
        out = cleaned
    out = re.sub(r"\s*(?:" + _MARK + r"\s*)+", "\n", out)
    return f"https://pretix.cosmostue.nl/{shop.group(1)}/{shop.group(2)}/", out.strip() + "\n"


def embed_code(shop):
    return (
        f'<link rel="stylesheet" type="text/css" href="{shop}widget/v1.css">\n'
        '<script type="text/javascript" src="https://pretix.cosmostue.nl/widget/v1.en.js" async></script>\n'
        f'<pretix-widget event="{shop}" single-item-select="button"></pretix-widget>\n'
        '<noscript><div class="pretix-widget"><div class="pretix-widget-info-message">JavaScript is disabled in your '
        "browser. To access our ticket shop without JavaScript, please "
        f'<a target="_blank" rel="noopener" href="{shop}">click here</a>.</div></div></noscript>'
    )


def move_embeds_to_field(apps, schema_editor):
    event_model = apps.get_model("events", "Event")
    for event in event_model.objects.filter(pretix_shop="", description__icontains="pretix-widget"):
        shop, description = split_embed(event.description)
        if shop:
            event.pretix_shop, event.description = shop, description
            event.save(update_fields=["pretix_shop", "description"])


def put_embeds_back(apps, schema_editor):
    event_model = apps.get_model("events", "Event")
    for event in event_model.objects.exclude(pretix_shop=""):
        event.description = event.description.rstrip() + "\n" + embed_code(event.pretix_shop)
        event.pretix_shop = ""
        event.save(update_fields=["pretix_shop", "description"])


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0003_event_pretix_shop"),
    ]

    operations = [
        migrations.RunPython(move_embeds_to_field, put_embeds_back),
    ]
