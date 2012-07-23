from mezzanine.conf import register_setting

register_setting(
    name="RICHTEXT_ALLOWED_TAGS",
    append=True,
    default=("iframe", "embed"), #etc
)