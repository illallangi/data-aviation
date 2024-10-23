from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate

from illallangi.rdf.adapters import AviationAdapter as RDFAdapter


def add_model(
    **_kwargs: dict[str, object],
) -> None:
    from illallangi.django.data.models import Model, Synchronize

    Model.objects.update_or_create(
        description="Alliances of airlines working together to provide a seamless travel experience.",
        icon="aviation/alliances.jpg",
        model="illallangi.data.aviation.models.Alliance",
        plural="Alliances",
        singular="Alliance",
        url="alliances_html",
    )
    Model.objects.update_or_create(
        description="Connecting us to the world, turning dreams of distant places into reality and reminding us that the sky holds endless adventures.",
        icon="aviation/airlines.jpg",
        model="illallangi.data.aviation.models.Airline",
        plural="Airlines",
        singular="Airline",
        url="airlines_html",
    )
    Model.objects.update_or_create(
        description="Gateways to endless possibilities, where every departure is the start of a new adventure and every arrival is a homecoming.",
        icon="aviation/airports.jpg",
        model="illallangi.data.aviation.models.Airport",
        plural="Airports",
        singular="Airport",
        url="airports_html",
    )

    Synchronize.objects.update_or_create(
        callable="illallangi.data.aviation.apps.synchronize",
    )


class AviationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "illallangi.data.aviation"

    def ready(
        self,
    ) -> None:
        post_migrate.connect(
            add_model,
            sender=self,
        )


def synchronize() -> None:
    from illallangi.data.aviation.adapters import (
        AviationAdapter as DjangoAdapter,
    )
    from illallangi.data.aviation.models import Airline, Airport

    src = RDFAdapter(
        **settings.RDF,
    )
    dst = DjangoAdapter()

    src.load(
        airline_iata=[airline.iata for airline in Airline.objects.all()],
        airport_iata=[airport.iata for airport in Airport.objects.all()],
        **settings.AVIATION,
    )
    dst.load()

    src.sync_to(dst)
