from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from illallangi.data.aviation.models import Airline, Alliance


@require_GET
def airline_list(
    request: HttpRequest,
    alliance__slug: str | None = None,
) -> render:
    objects = Airline.objects.all()
    breadcrumbs = []

    if alliance__slug:
        alliance = Alliance.objects.get(
            Q(slug=alliance__slug),
        )
        objects = objects.filter(
            Q(alliance=alliance),
        )
        breadcrumbs.append(
            {
                "title": "Alliances",
                "url": reverse(
                    "alliance_list",
                ),
            },
        )
        breadcrumbs.append(
            {
                "title": str(alliance),
                "url": reverse(
                    "alliance_detail",
                    kwargs={
                        "slug": alliance.slug,
                    },
                ),
            },
        )
        breadcrumbs.append(
            {
                "title": "Airlines",
                "url": reverse(
                    "airline_list",
                    kwargs={
                        "alliance__slug": alliance.slug,
                    },
                ),
            },
        )

    if not alliance__slug:
        breadcrumbs.append(
            {
                "title": "Airlines",
                "url": reverse(
                    "airline_list",
                ),
            },
        )

    if objects.count() == 1:
        return redirect(
            reverse(
                "airline_detail",
                kwargs={
                    "slug": objects.first().slug,
                },
            ),
        )

    return render(
        request,
        "aviation/airline_list.html",
        {
            "base_template": ("partial.html" if request.htmx else "base.html"),
            "page": Paginator(
                object_list=objects.order_by(
                    "label",
                ),
                per_page=10,
            ).get_page(
                request.GET.get("page", 1),
            ),
            "breadcrumbs": breadcrumbs,
            "links": [
                {
                    "rel": "alternate",
                    "type": "text/html",
                    "href": request.build_absolute_uri(
                        request.get_full_path(),
                    ),
                },
            ],
        },
    )
