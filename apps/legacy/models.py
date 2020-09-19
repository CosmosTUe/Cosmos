# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = True
        db_table = "auth_group"


# class AuthGroupPermissions(models.Model):
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

#     class Meta:
#         managed = True
#         db_table = "auth_group_permissions"
#         unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = True
        db_table = "auth_user"


# class AuthUserGroups(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = True
#         db_table = "auth_user_groups"
#         unique_together = (("user", "group"),)


# class AuthUserUserPermissions(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = True
#         db_table = "auth_user_user_permissions"
#         unique_together = (("user", "permission"),)


class CmsAliaspluginmodel(models.Model):
    cmsplugin_ptr = models.OneToOneField("CmsCmsplugin", models.DO_NOTHING, primary_key=True)
    plugin = models.ForeignKey("CmsCmsplugin", models.DO_NOTHING, blank=True, null=True, related_name="+")
    alias_placeholder = models.ForeignKey("CmsPlaceholder", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "cms_aliaspluginmodel"


class CmsCmsplugin(models.Model):
    position = models.PositiveSmallIntegerField()
    language = models.CharField(max_length=15)
    plugin_type = models.CharField(max_length=50)
    creation_date = models.DateTimeField()
    changed_date = models.DateTimeField()
    parent = models.ForeignKey("self", models.DO_NOTHING, blank=True, null=True)
    placeholder = models.ForeignKey("CmsPlaceholder", models.DO_NOTHING, blank=True, null=True)
    depth = models.PositiveIntegerField()
    numchild = models.PositiveIntegerField()
    path = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = True
        db_table = "cms_cmsplugin"


class CmsGlobalpagepermission(models.Model):
    can_change = models.IntegerField()
    can_add = models.IntegerField()
    can_delete = models.IntegerField()
    can_change_advanced_settings = models.IntegerField()
    can_publish = models.IntegerField()
    can_change_permissions = models.IntegerField()
    can_move_page = models.IntegerField()
    can_view = models.IntegerField()
    can_recover_page = models.IntegerField()
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "cms_globalpagepermission"


# class CmsGlobalpagepermissionSites(models.Model):
#     globalpagepermission = models.ForeignKey(CmsGlobalpagepermission, models.DO_NOTHING)
#     site = models.ForeignKey("DjangoSite", models.DO_NOTHING)

#     class Meta:
#         managed = True
#         db_table = "cms_globalpagepermission_sites"
#         unique_together = (("globalpagepermission", "site"),)


class CmsPage(models.Model):
    created_by = models.CharField(max_length=255)
    changed_by = models.CharField(max_length=255)
    creation_date = models.DateTimeField()
    changed_date = models.DateTimeField()
    publication_date = models.DateTimeField(blank=True, null=True)
    publication_end_date = models.DateTimeField(blank=True, null=True)
    in_navigation = models.IntegerField()
    soft_root = models.IntegerField()
    reverse_id = models.CharField(max_length=40, blank=True, null=True)
    navigation_extenders = models.CharField(max_length=80, blank=True, null=True)
    template = models.CharField(max_length=100)
    login_required = models.IntegerField()
    limit_visibility_in_menu = models.SmallIntegerField(blank=True, null=True)
    is_home = models.IntegerField()
    application_urls = models.CharField(max_length=200, blank=True, null=True)
    application_namespace = models.CharField(max_length=200, blank=True, null=True)
    publisher_is_draft = models.IntegerField()
    languages = models.CharField(max_length=255, blank=True, null=True)
    xframe_options = models.IntegerField()
    publisher_public = models.OneToOneField("self", models.DO_NOTHING, blank=True, null=True)
    is_page_type = models.IntegerField()
    node = models.ForeignKey("CmsTreenode", models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "cms_page"
        unique_together = (("node", "publisher_is_draft"),)


# class CmsPagePlaceholders(models.Model):
#     page = models.ForeignKey(CmsPage, models.DO_NOTHING)
#     placeholder = models.ForeignKey("CmsPlaceholder", models.DO_NOTHING)

#     class Meta:
#         managed = True
#         db_table = "cms_page_placeholders"
#         unique_together = (("page", "placeholder"),)


class CmsPagepermission(models.Model):
    can_change = models.IntegerField()
    can_add = models.IntegerField()
    can_delete = models.IntegerField()
    can_change_advanced_settings = models.IntegerField()
    can_publish = models.IntegerField()
    can_change_permissions = models.IntegerField()
    can_move_page = models.IntegerField()
    can_view = models.IntegerField()
    grant_on = models.IntegerField()
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, blank=True, null=True)
    page = models.ForeignKey(CmsPage, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "cms_pagepermission"


class CmsPageuser(models.Model):
    user_ptr = models.OneToOneField(AuthUser, models.DO_NOTHING, primary_key=True)
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name="+")

    class Meta:
        managed = True
        db_table = "cms_pageuser"


class CmsPageusergroup(models.Model):
    group_ptr = models.OneToOneField(AuthGroup, models.DO_NOTHING, primary_key=True)
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "cms_pageusergroup"


class CmsPlaceholder(models.Model):
    slot = models.CharField(max_length=255)
    default_width = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "cms_placeholder"


class CmsPlaceholderreference(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)
    name = models.CharField(max_length=255)
    placeholder_ref = models.ForeignKey(CmsPlaceholder, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "cms_placeholderreference"


class CmsStaticplaceholder(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    dirty = models.IntegerField()
    creation_method = models.CharField(max_length=20)
    draft = models.ForeignKey(CmsPlaceholder, models.DO_NOTHING, blank=True, null=True, related_name="+")
    public = models.ForeignKey(CmsPlaceholder, models.DO_NOTHING, blank=True, null=True, related_name="+")
    site = models.ForeignKey("DjangoSite", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "cms_staticplaceholder"
        unique_together = (("code", "site"),)


class CmsTitle(models.Model):
    language = models.CharField(max_length=15)
    title = models.CharField(max_length=255)
    page_title = models.CharField(max_length=255, blank=True, null=True)
    menu_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    slug = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    has_url_overwrite = models.IntegerField()
    redirect = models.CharField(max_length=2048, blank=True, null=True)
    creation_date = models.DateTimeField()
    published = models.IntegerField()
    publisher_is_draft = models.IntegerField()
    publisher_state = models.SmallIntegerField()
    page = models.ForeignKey(CmsPage, models.DO_NOTHING)
    publisher_public = models.OneToOneField("self", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "cms_title"
        unique_together = (("language", "page"),)


class CmsTreenode(models.Model):
    path = models.CharField(unique=True, max_length=255)
    depth = models.PositiveIntegerField()
    numchild = models.PositiveIntegerField()
    parent = models.ForeignKey("self", models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey("DjangoSite", models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "cms_treenode"


class CmsUrlconfrevision(models.Model):
    revision = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "cms_urlconfrevision"


class CmsUsersettings(models.Model):
    language = models.CharField(max_length=10)
    clipboard = models.ForeignKey(CmsPlaceholder, models.DO_NOTHING, blank=True, null=True)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "cms_usersettings"


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = True
#         db_table = "django_migrations"


class DjangoRedirect(models.Model):
    site = models.ForeignKey("DjangoSite", models.DO_NOTHING)
    old_path = models.CharField(max_length=200)
    new_path = models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = "django_redirect"
        unique_together = (("site", "old_path"),)


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = "django_session"


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = "django_site"


class DjangocmsGooglemapGooglemap(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)
    title = models.CharField(max_length=255)
    zoom = models.PositiveSmallIntegerField()
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    width = models.CharField(max_length=6)
    height = models.CharField(max_length=6)
    scrollwheel = models.IntegerField()
    double_click_zoom = models.IntegerField()
    draggable = models.IntegerField()
    keyboard_shortcuts = models.IntegerField()
    pan_control = models.IntegerField()
    zoom_control = models.IntegerField()
    street_view_control = models.IntegerField()
    style = models.TextField()
    fullscreen_control = models.IntegerField()
    map_type_control = models.CharField(max_length=255)
    rotate_control = models.IntegerField()
    scale_control = models.IntegerField()
    template = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "djangocms_googlemap_googlemap"


class DjangocmsGooglemapGooglemapmarker(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    show_content = models.IntegerField()
    info_content = models.TextField()
    icon = models.ForeignKey("FilerImage", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "djangocms_googlemap_googlemapmarker"


class DjangocmsGooglemapGooglemaproute(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)
    title = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    travel_mode = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "djangocms_googlemap_googlemaproute"


class DjangocmsSnippetSnippet(models.Model):
    name = models.CharField(unique=True, max_length=255)
    html = models.TextField()
    template = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = True
        db_table = "djangocms_snippet_snippet"


class DjangocmsSnippetSnippetptr(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)
    snippet = models.ForeignKey(DjangocmsSnippetSnippet, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "djangocms_snippet_snippetptr"


class DjangocmsTextCkeditorText(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)
    body = models.TextField()

    class Meta:
        managed = True
        db_table = "djangocms_text_ckeditor_text"


class DjangocmsVideoVideoplayer(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)
    embed_link = models.CharField(max_length=255)
    poster = models.ForeignKey("FilerImage", models.DO_NOTHING, blank=True, null=True)
    attributes = models.TextField()
    label = models.CharField(max_length=255)
    template = models.CharField(max_length=255)
    parameters = models.TextField()

    class Meta:
        managed = True
        db_table = "djangocms_video_videoplayer"


class DjangocmsVideoVideosource(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)
    text_title = models.CharField(max_length=255)
    text_description = models.TextField()
    attributes = models.TextField()
    source_file = models.ForeignKey("FilerFile", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "djangocms_video_videosource"


class DjangocmsVideoVideotrack(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)
    kind = models.CharField(max_length=255)
    srclang = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    attributes = models.TextField()
    src = models.ForeignKey("FilerFile", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "djangocms_video_videotrack"


class EasyThumbnailsSource(models.Model):
    storage_hash = models.CharField(max_length=40)
    name = models.CharField(max_length=255)
    modified = models.DateTimeField()

    class Meta:
        managed = True
        db_table = "easy_thumbnails_source"
        unique_together = (("storage_hash", "name"),)


class EasyThumbnailsThumbnail(models.Model):
    storage_hash = models.CharField(max_length=40)
    name = models.CharField(max_length=255)
    modified = models.DateTimeField()
    source = models.ForeignKey(EasyThumbnailsSource, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "easy_thumbnails_thumbnail"
        unique_together = (("storage_hash", "name", "source"),)


class EasyThumbnailsThumbnaildimensions(models.Model):
    thumbnail = models.OneToOneField(EasyThumbnailsThumbnail, models.DO_NOTHING)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "easy_thumbnails_thumbnaildimensions"


class FilerClipboard(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "filer_clipboard"


# class FilerClipboarditem(models.Model):
#     clipboard = models.ForeignKey(FilerClipboard, models.DO_NOTHING)
#     file = models.ForeignKey("FilerFile", models.DO_NOTHING)

#     class Meta:
#         managed = True
#         db_table = "filer_clipboarditem"


class FilerFile(models.Model):
    file = models.CharField(max_length=255, blank=True, null=True)
    field_file_size = models.BigIntegerField(db_column="_file_size", blank=True, null=True)
    # Field renamed because it started with '_'.
    sha1 = models.CharField(max_length=40)
    has_all_mandatory_data = models.IntegerField()
    original_filename = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    is_public = models.IntegerField()
    folder = models.ForeignKey("FilerFolder", models.DO_NOTHING, blank=True, null=True)
    owner = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    polymorphic_ctype = models.ForeignKey(DjangoContentType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "filer_file"


class FilerFolder(models.Model):
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    lft = models.PositiveIntegerField()
    rght = models.PositiveIntegerField()
    tree_id = models.PositiveIntegerField()
    level = models.PositiveIntegerField()
    owner = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    parent = models.ForeignKey("self", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "filer_folder"
        unique_together = (("parent", "name"),)


class FilerFolderpermission(models.Model):
    type = models.SmallIntegerField()
    everybody = models.IntegerField()
    can_edit = models.SmallIntegerField(blank=True, null=True)
    can_read = models.SmallIntegerField(blank=True, null=True)
    can_add_children = models.SmallIntegerField(blank=True, null=True)
    folder = models.ForeignKey(FilerFolder, models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "filer_folderpermission"


class FilerImage(models.Model):
    file_ptr = models.OneToOneField(FilerFile, models.DO_NOTHING, primary_key=True)
    field_height = models.IntegerField(db_column="_height", blank=True, null=True)
    # Field renamed because it started with '_'.
    field_width = models.IntegerField(db_column="_width", blank=True, null=True)
    # Field renamed because it started with '_'.
    date_taken = models.DateTimeField(blank=True, null=True)
    default_alt_text = models.CharField(max_length=255, blank=True, null=True)
    default_caption = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    must_always_publish_author_credit = models.IntegerField()
    must_always_publish_copyright = models.IntegerField()
    subject_location = models.CharField(max_length=64)

    class Meta:
        managed = True
        db_table = "filer_image"


class FilerThumbnailoption(models.Model):
    name = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    crop = models.IntegerField()
    upscale = models.IntegerField()

    class Meta:
        managed = True
        db_table = "filer_thumbnailoption"


class LetsencryptAcmechallenge(models.Model):
    challenge = models.CharField(unique=True, max_length=255)
    response = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "letsencrypt_acmechallenge"


class MenusCachekey(models.Model):
    language = models.CharField(max_length=255)
    site = models.PositiveIntegerField()
    key = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "menus_cachekey"


class MysiteCard(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)
    title_text = models.CharField(max_length=50)
    content = models.TextField()
    color_class = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = "mysite_card"


class MysiteCardimage(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)
    title_text = models.CharField(max_length=50)
    content = models.TextField()
    image_url = models.CharField(max_length=100)
    image_title = models.CharField(max_length=100)
    color_class = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = "mysite_cardimage"


class MysiteCardimagelink(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)
    title_text = models.CharField(max_length=50)
    content = models.TextField()
    image_url = models.CharField(max_length=100)
    image_title = models.CharField(max_length=100)
    color_class = models.CharField(max_length=50)
    link_text = models.CharField(max_length=100)
    link_destination = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = "mysite_cardimagelink"


class MysiteCardlink(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)
    title_text = models.CharField(max_length=50)
    content = models.TextField()
    color_class = models.CharField(max_length=50)
    link_text = models.CharField(max_length=100)
    link_destination = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = "mysite_cardlink"


class MysiteColumnplugin(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = True
        db_table = "mysite_columnplugin"


class MysiteDoor(models.Model):
    is_open = models.IntegerField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = True
        db_table = "mysite_door"


class MysiteFacebookeventsmodel(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = True
        db_table = "mysite_facebookeventsmodel"


class MysiteFacebookgallerymodel(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = True
        db_table = "mysite_facebookgallerymodel"


class MysiteParentplugin(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = True
        db_table = "mysite_parentplugin"


class MysitePi(models.Model):
    ip = models.CharField(max_length=50)
    updated_at = models.DateTimeField()

    class Meta:
        managed = True
        db_table = "mysite_pi"


class MysiteProfile(models.Model):
    department = models.CharField(max_length=100)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)
    nationality = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    card_number = models.CharField(max_length=25)
    gender = models.CharField(max_length=10)
    key_access = models.CharField(max_length=3)
    member_type = models.CharField(max_length=50)
    phone_nr = models.CharField(max_length=15)
    tue_id = models.CharField(max_length=25)

    class Meta:
        managed = True
        db_table = "mysite_profile"


class MysiteSlidermodel(models.Model):
    cmsplugin_ptr = models.OneToOneField(CmsCmsplugin, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = True
        db_table = "mysite_slidermodel"


class MysiteToken(models.Model):
    token = models.CharField(max_length=100)
    device = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = "mysite_token"
