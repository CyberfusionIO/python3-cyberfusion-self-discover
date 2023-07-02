"""App."""

import defusedxml.ElementTree as SafeET
from fastapi import FastAPI, Query, Request, Response, status

from self_discover.settings import settings
from self_discover.utilities import (
    get_host_from_request,
    get_pox_autodiscover_response,
    get_thunderbird_autoconfig_response,
)

app = FastAPI()

PREFIX_AUTODISCOVER = "autodiscover"
PREFIX_AUTOCONFIG = "autoconfig"


@app.post("/autodiscover/autodiscover.xml")
async def pox_autodiscover(request: Request) -> Response:
    """Get POX ('plain old XML') autodiscover response."""
    if get_host_from_request(request).split(".")[0] != PREFIX_AUTODISCOVER:
        return Response(
            content=f"URL must start with '{PREFIX_AUTODISCOVER}'",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    body = await request.body()

    try:
        email_address = SafeET.fromstring(body).find(
            ".//{https://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006}EMailAddress"
        )
    except SafeET.ParseError:
        return Response(
            content="Payload must be valid XML",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if email_address is None:
        return Response(
            content="Email address must be present in XML payload",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    data = get_pox_autodiscover_response(
        settings.IMAP_SERVER_HOSTNAME,
        settings.POP3_SERVER_HOSTNAME,
        settings.SMTP_SERVER_HOSTNAME,
        email_address.text,
    )

    return Response(content=data, media_type="application/xml")


@app.get("/mail/config-v1.1.xml")
async def thunderbird_autoconfig(
    request: Request,
    email_address: str = Query(alias="emailaddress"),  # noqa: B008
) -> Response:
    """Get Thunderbird autoconfig response."""
    if get_host_from_request(request).split(".")[0] != PREFIX_AUTOCONFIG:
        return Response(
            content=f"URL must start with '{PREFIX_AUTOCONFIG}'",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    hostname_without_autoconfig = get_host_from_request(request).split(".")
    hostname_without_autoconfig.remove(
        PREFIX_AUTOCONFIG
    )  # Due to the check above, we know that this is the first element

    data = get_thunderbird_autoconfig_response(
        settings.IMAP_SERVER_HOSTNAME,
        settings.POP3_SERVER_HOSTNAME,
        settings.SMTP_SERVER_HOSTNAME,
        email_address,
        ".".join(hostname_without_autoconfig),
    )

    return Response(content=data, media_type="application/xml")
