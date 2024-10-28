from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET

from illallangi.data.aviation.models import Alliance


@require_GET
def alliance_detail(
    request: HttpRequest,
    slug: str,
) -> render:
    objects = Alliance.objects.filter(
        slug=slug,
    )

    if objects.count() > 1:
        return HttpResponse(
            status=500,
            content="Multiple alliances found",
        )

    if objects.count() == 1:
        obj = objects.first()
        return render(
            request,
            "aviation/alliance_detail.html",
            {
                "base_template": ("partial.html" if request.htmx else "base.html"),
                "obj": obj,
                "breadcrumbs": [
                    {
                        "title": "Alliances",
                        "url": reverse(
                            "alliance_list",
                        ),
                    },
                    {
                        "title": str(obj),
                        "url": reverse(
                            "alliance_detail",
                            kwargs={
                                "slug": slug,
                            },
                        ),
                    },
                ],
                "links": [
                    {
                        "rel": "alternate",
                        "type": "text/html",
                        "href": request.build_absolute_uri(
                            request.get_full_path(),
                        ),
                    },
                ],
                "related_objects": {
                    related_object.related_model._meta.verbose_name.title(): {  # noqa: SLF001
                        "href": reverse(
                            f"{related_object.related_model._meta.verbose_name.lower()}_list",  # noqa: SLF001
                            kwargs={
                                "alliance__slug": slug,
                            },
                        ),
                        "title": related_object.related_model._meta.verbose_name_plural.title(),  # noqa: SLF001
                        "count": related_object.related_model.objects.filter(
                            models.Q(alliance=obj)
                        ).count(),
                    }
                    for related_object in obj._meta.related_objects  # noqa: SLF001
                }.values(),
            },
        )

    return HttpResponse(
        status=400,
        content="Alliance not found",
    )
