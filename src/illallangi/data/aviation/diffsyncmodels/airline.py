import diffsync

from illallangi.data.aviation.models import Airline as ModelAirline
from illallangi.data.aviation.models import Alliance


class Airline(
    diffsync.DiffSyncModel,
):
    _modelname = "Airline"
    _identifiers = ("iata",)
    _attributes = (
        "alliance__name",
        "dominant_color",
        "icao",
        "label",
    )

    pk: int

    iata: str

    alliance__name: str | None
    dominant_color: str | None
    icao: str | None
    label: str | None

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Airline":
        alliance = (
            Alliance.objects.get_or_create(name=attrs["alliance__name"])[0]
            if "alliance__name" in attrs and attrs["alliance__name"] is not None
            else None
        )

        obj = ModelAirline.objects.update_or_create(
            iata=ids["iata"],
            defaults={
                "label": attrs["label"],
                "icao": attrs["icao"],
                "alliance": alliance,
                "dominant_color": attrs["dominant_color"],
            },
        )[0]

        return super().create(
            adapter,
            {
                "pk": obj.pk,
                **ids,
            },
            attrs,
        )

    def update(
        self,
        attrs: dict,
    ) -> "Airline":
        alliance = (
            Alliance.objects.get_or_create(name=attrs["alliance__name"])[0]
            if "alliance__name" in attrs and attrs["alliance__name"] is not None
            else None
        )

        ModelAirline.objects.filter(
            pk=self.pk,
        ).update(
            **{
                **{k: v for k, v in attrs.items() if k not in ["alliance__name"]},
                "alliance": alliance,
            },
        )

        return super().update(attrs)

    def delete(
        self,
    ) -> "Airline":
        ModelAirline.objects.get(
            pk=self.pk,
        ).delete()

        return super().delete()
