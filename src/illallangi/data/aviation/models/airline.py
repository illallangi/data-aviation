from autoslug import AutoSlugField
from colorfield.fields import ColorField
from django.db import models
from django.templatetags.static import static


class Airline(
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

    # ip:airlineIataCode: Airline IATA Code
    # P229: IATA airline designator
    iata = models.CharField(
        blank=False,
        help_text="two-character identifier for an airline",
        max_length=2,
        null=False,
        unique=True,
        verbose_name="IATA airline designator",
    )

    # Fields

    # P114: airline alliance
    # ip:memberOfAirlineAlliance: Member Of Airline Alliance
    alliance = models.ForeignKey(
        blank=True,
        help_text="alliance the airline belongs to",
        null=True,
        on_delete=models.SET_NULL,
        to="Alliance",
        verbose_name="airline alliance",
    )

    # ip:dominantColor: Dominant Color
    dominant_color = ColorField(
        blank=True,
        help_text="Dominant Color",
        null=True,
        verbose_name="Dominant Color",
    )

    # ip:airlineIcaoCode: Airline ICAO Code
    # P230: ICAO airline designator
    icao = models.CharField(  # noqa: DJ001
        blank=True,
        help_text="three letter identifier for an airline",
        max_length=3,
        null=True,
        verbose_name="ICAO airline designator",
    )

    # rdfs:label: A human-readable name for the subject
    label = models.CharField(  # noqa: DJ001
        blank=True,
        help_text="A human-readable name for the subject",
        max_length=255,
        null=True,
        verbose_name="Label",
    )

    # Methods

    def __str__(
        self,
    ) -> str:
        if self.label:
            return self.label
        return self.iata

    def get_logo_url(
        self,
    ) -> str:
        return static(f"aviation/airline_logos/{self.slug}.png")

    def get_slug(
        self,
    ) -> str:
        if self.label:
            return self.label
        return self.iata
