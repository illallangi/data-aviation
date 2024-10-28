from autoslug import AutoSlugField
from django.db import models
from django.templatetags.static import static


class Alliance(
    models.Model,
):
    # Surrogate Keys

    id = models.AutoField(
        primary_key=True,
    )

    slug = AutoSlugField(
        populate_from="get_slug",
        unique=True,
    )

    # Natural Keys

    name = models.CharField(
        blank=False,
        max_length=255,
        null=False,
        unique=True,
    )

    # Methods

    def __str__(
        self,
    ) -> str:
        return self.name

    def get_logo_url(
        self,
    ) -> str:
        return static(f"aviation/alliance_logos/{self.slug}.png")

    def get_slug(
        self,
    ) -> str:
        return self.name
