import pytest
from fastapi.testclient import TestClient

from self_discover.exceptions import MissingHostError
from self_discover.settings import settings

DOMAIN = "example.com"

EMAIL_ADDRESS = f"example@{DOMAIN}"

HEADERS = {"Host": f"autoconfig.{DOMAIN}"}


def test_thunderbird_autoconfig(test_client: TestClient) -> None:
    response = test_client.get(
        "/mail/config-v1.1.xml",
        params={"emailaddress": EMAIL_ADDRESS},
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert (
        response.text
        == f"""<?xml version='1.0' encoding='utf-8'?>
<clientConfig version="1.1">
    <emailProvider id="{DOMAIN}">
        <domain>{DOMAIN}</domain>
        <displayName>%EMAILADDRESS%</displayName>
        <incomingServer type="imap">
            <hostname>{settings.IMAP_SERVER_HOSTNAME}</hostname>
            <port>993</port>
            <socketType>SSL</socketType>
            <username>%EMAILADDRESS%</username>
            <authentication>password-cleartext</authentication>
        </incomingServer>
        <outgoingServer type="smtp">
            <hostname>{settings.SMTP_SERVER_HOSTNAME}</hostname>
            <port>587</port>
            <socketType>STARTTLS</socketType>
            <username>%EMAILADDRESS%</username>
            <authentication>password-cleartext</authentication>
        </outgoingServer>
    </emailProvider>
</clientConfig>
"""
    )


def test_thunderbird_missing_url_prefix(test_client: TestClient) -> None:
    response = test_client.get(
        "/mail/config-v1.1.xml",
        params={"emailaddress": EMAIL_ADDRESS},
        headers={"Host": DOMAIN},
    )

    assert response.status_code == 400
    assert response.text == "URL must start with 'autoconfig'"


def test_thunderbird_missing_host(test_client: TestClient) -> None:
    with pytest.raises(MissingHostError):
        test_client.get(
            "/mail/config-v1.1.xml",
            params={"emailaddress": EMAIL_ADDRESS},
            headers={"Host": ""},
        )
