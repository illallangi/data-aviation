from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from illallangi.data.aviation.models import Alliance


@require_GET
def alliance_list(
    request: HttpRequest,
) -> render:
    objects = Alliance.objects.all()
    breadcrumbs = []

    if not False:
        breadcrumbs.append(
            {
                "title": "Alliances",
                "url": reverse(
                    "alliance_list",
                ),
            },
        )

    if objects.count() == 1:
        return redirect(
            reverse(
                "alliance_detail",
                kwargs={
                    "slug": objects.first().slug,
                },
            ),
        )

    return render(
        request,
        "aviation/alliance_list.html",
        {
            "base_template": ("partial.html" if request.htmx else "base.html"),
            "page": Paginator(
                object_list=objects.order_by(
                    "name",
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
