import djp
from django.urls import URLPattern, re_path

from illallangi.data.aviation import checks  # noqa: F401


@djp.hookimpl
def installed_apps() -> list[str]:
    return [
        "illallangi.data.aviation",
        "colorfield",
    ]


@djp.hookimpl
def urlpatterns() -> list[URLPattern]:
    from illallangi.data.aviation import views

    return [
        re_path(
            r"^alliances/(?P<alliance__slug>[\w\d-]+)/airlines/$",
            views.airline_list,
            name="airline_list",
        ),
        re_path(
            r"^airlines/$",
            views.airline_list,
            name="airline_list",
        ),
        re_path(
            r"^airlines/(?P<slug>[\w\d-]+)/$",
            views.airline_detail,
            name="airline_detail",
        ),
        re_path(
            r"^airports/$",
            views.airport_list,
            name="airport_list",
        ),
        re_path(
            r"^airports/(?P<slug>[\w\d-]+)/$",
            views.airport_detail,
            name="airport_detail",
        ),
        re_path(
            r"^alliances/$",
            views.alliance_list,
            name="alliance_list",
        ),
        re_path(
            r"^alliances/(?P<slug>[\w\d-]+)/$",
            views.alliance_detail,
            name="alliance_detail",
        ),
    ]
