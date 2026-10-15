import datetime
import importlib

from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import make_aware

from apps.events.models import Event
from apps.events.pretix import shop_url
from tests.cosmos.helpers import get_image_file
from tests.events.views.events import EventFormTest

move_embeds = importlib.import_module("apps.events.migrations.0004_move_pretix_embeds")

SHOP = "https://pretix.cosmostue.nl/cosmos/TEST1/"


class ShopLinkTest(TestCase):
    def test_accepts_shop_and_back_office_links(self):
        for link in (
            "https://pretix.cosmostue.nl/cosmos/TEST1/",
            "https://pretix.cosmostue.nl/cosmos/TEST1",
            "pretix.cosmostue.nl/cosmos/TEST1/",
            "http://pretix.cosmostue.nl/cosmos/TEST1/redeem?voucher=X",
            "  https://pretix.cosmostue.nl/control/event/cosmos/TEST1/live/ ",
        ):
            self.assertEqual(SHOP, shop_url(link), link)

    def test_rejects_other_links(self):
        for link in (
            "https://pretix.eu/cosmostickets/thanksgiving/",
            "https://pretix.cosmostue.nl/cosmos/",
            "https://pretix.cosmostue.nl/control/",
            "https://cosmostue.nl/events/1/",
            "tickets please",
        ):
            with self.assertRaises(ValidationError, msg=link):
                shop_url(link)


class EventFormShopLinkTest(TestCase):
    def test_back_office_link_is_saved_as_shop_link(self):
        form = EventFormTest.generate_form()
        form.data["pretix_shop"] = "https://pretix.cosmostue.nl/control/event/cosmos/TEST1/live/"
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(SHOP, form.cleaned_data["pretix_shop"])

    def test_link_to_another_site_is_refused(self):
        form = EventFormTest.generate_form()
        form.data["pretix_shop"] = "https://pretix.eu/someone/event/"
        self.assertFalse(form.is_valid())
        self.assertIn("pretix_shop", form.errors)

    def test_shop_link_is_optional(self):
        form = EventFormTest.generate_form()
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual("", form.cleaned_data["pretix_shop"])


class EventPageWidgetTest(TestCase):
    def make_event(self, pretix_shop=""):
        return Event.objects.create(
            name="Event",
            image=get_image_file(),
            description="<p>Description</p>",
            lead="Lead",
            start_date_time=make_aware(datetime.datetime(2200, 1, 1, 18)),
            end_date_time=make_aware(datetime.datetime(2200, 1, 1, 21)),
            member_only=False,
            location="Common Room",
            organizer=Group.objects.create(name="organizer"),
            price=0,
            pretix_shop=pretix_shop,
        )

    def test_widget_shown_for_event_with_shop(self):
        response = self.client.get("/events/%d/" % self.make_event(SHOP).pk)
        self.assertContains(response, '<pretix-widget event="%s" single-item-select="button"></pretix-widget>' % SHOP)
        self.assertContains(response, 'href="%swidget/v1.css"' % SHOP)
        self.assertContains(response, 'src="https://pretix.cosmostue.nl/widget/v1.en.js"')

    def test_no_widget_without_shop(self):
        response = self.client.get("/events/%d/" % self.make_event().pk)
        self.assertNotContains(response, "pretix-widget")


class MoveEmbedsMigrationTest(TestCase):
    EMBED = (
        '<p><link rel="stylesheet" type="text/css" href="https://pretix.cosmostue.nl/cosmos/TEST1/widget/v1.css"></p>\n'
        '<p><script type="text/javascript" src="https://pretix.cosmostue.nl/widget/v1.en.js" async></script></p>\n'
        '<pretix-widget event="https://pretix.cosmostue.nl/cosmos/TEST1/" single-item-select="button"></pretix-widget>'
        '<noscript><div class="pretix-widget"><div class="pretix-widget-info-message">JavaScript is disabled. Please '
        '<a target="_blank" rel="noopener" href="https://pretix.cosmostue.nl/cosmos/TEST1/">click here</a>.</div></div>'
        "</noscript>"
    )

    def test_embed_moves_to_field_and_text_stays(self):
        shop, description = move_embeds.split_embed("<p>Come along!</p>\n" + self.EMBED + "\n<p>See you there.</p>")
        self.assertEqual(SHOP, shop)
        self.assertEqual("<p>Come along!</p>\n<p>See you there.</p>\n", description)

    def test_older_compat_embed(self):
        html = (
            '<p>Text</p><div class="pretix-widget-compat" event="https://pretix.cosmostue.nl/cosmos/old/"></div>'
            '<noscript><div class="pretix-widget">Please <a href="https://pretix.cosmostue.nl/cosmos/old/">'
            "click here</a></div></noscript>"
        )
        self.assertEqual(("https://pretix.cosmostue.nl/cosmos/old/", "<p>Text</p>\n"), move_embeds.split_embed(html))

    def test_shops_on_other_pretix_sites_are_left_alone(self):
        html = (
            '<link rel="stylesheet" href="https://pretix.eu/tint/love/widget/v1.css">'
            '<pretix-widget event="https://pretix.eu/tint/love/"></pretix-widget>'
        )
        self.assertEqual(("", html), move_embeds.split_embed(html))

    def test_description_without_embed_is_unchanged(self):
        html = '<p>Tickets: <a href="https://pretix.cosmostue.nl/cosmos/TEST1/">buy here</a></p>'
        self.assertEqual(("", html), move_embeds.split_embed(html))

    def test_put_back_code_contains_the_widget(self):
        code = move_embeds.embed_code(SHOP)
        self.assertIn('<pretix-widget event="%s"' % SHOP, code)
        self.assertEqual(SHOP, move_embeds.split_embed("<p>x</p>\n" + code)[0])
