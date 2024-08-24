import pytest
from fastapi.testclient import TestClient

from self_discover.exceptions import MissingHostError
from self_discover.settings import settings

DOMAIN = "example.com"

EMAIL_ADDRESS = f"example@{DOMAIN}"

HEADERS = {"Host": f"autodiscover.{DOMAIN}"}


def test_pox_autodiscover(test_client: TestClient) -> None:
    response = test_client.post(
        "/autodiscover/autodiscover.xml",
        data=f"""<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006">
   <Request>
     <EMailAddress>{EMAIL_ADDRESS}</EMailAddress>
     <AcceptableResponseSchema>
       http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a
     </AcceptableResponseSchema>
   </Request>
 </Autodiscover>""",
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert (
        response.text
        == f"""<?xml version='1.0' encoding='utf-8'?>
<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/responseschema/2006">
    <Response xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a">
        <Account>
            <AccountType>email</AccountType>
            <Action>settings</Action>
            <Protocol>
                <Type>IMAP</Type>
                <Server>{settings.IMAP_SERVER_HOSTNAME}</Server>
                <Port>993</Port>
                <DomainRequired>off</DomainRequired>
                <LoginName>{EMAIL_ADDRESS}</LoginName>
                <SPA>off</SPA>
                <SSL>on</SSL>
                <AuthRequired>on</AuthRequired>
            </Protocol>
            <Protocol>
                <Type>POP3</Type>
                <Server>{settings.POP3_SERVER_HOSTNAME}</Server>
                <Port>995</Port>
                <DomainRequired>off</DomainRequired>
                <LoginName>{EMAIL_ADDRESS}</LoginName>
                <SPA>off</SPA>
                <SSL>on</SSL>
                <AuthRequired>on</AuthRequired>
            </Protocol>
            <Protocol>
                <Type>SMTP</Type>
                <Server>{settings.SMTP_SERVER_HOSTNAME}</Server>
                <Port>587</Port>
                <DomainRequired>off</DomainRequired>
                <LoginName>{EMAIL_ADDRESS}</LoginName>
                <SPA>off</SPA>
                <Encryption>TLS</Encryption>
                <AuthRequired>on</AuthRequired>
                <UsePOPAuth>off</UsePOPAuth>
                <SMTPLast>off</SMTPLast>
            </Protocol>
        </Account>
    </Response>
</Autodiscover>
"""
    )


def test_pox_autodiscover_xmlns_https_scheme_body(
    test_client: TestClient,
) -> None:
    response = test_client.post(
        "/autodiscover/autodiscover.xml",
        data=f"""<Autodiscover xmlns="https://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006">
   <Request>
     <EMailAddress>{EMAIL_ADDRESS}</EMailAddress>
     <AcceptableResponseSchema>
       https://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a
     </AcceptableResponseSchema>
   </Request>
 </Autodiscover>""",
        headers=HEADERS,
    )

    assert response.status_code == 200


def test_pox_autodiscover_invalid_xml(test_client: TestClient) -> None:
    response = test_client.post(
        "/autodiscover/autodiscover.xml", data="example", headers=HEADERS
    )

    assert response.status_code == 400
    assert response.text == "Payload must be valid XML"


def test_pox_autodiscover_email_address_absent(
    test_client: TestClient,
) -> None:
    response = test_client.post(
        "/autodiscover/autodiscover.xml",
        data="""<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006">
   <Request>
     <AcceptableResponseSchema>
       http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a
     </AcceptableResponseSchema>
   </Request>
 </Autodiscover>""",
        headers=HEADERS,
    )

    assert response.status_code == 400
    assert response.text == "Email address must be present in XML payload"


def test_pox_autodiscover_missing_url_prefix(test_client: TestClient) -> None:
    response = test_client.post(
        "/autodiscover/autodiscover.xml",
        data=f"""<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006">
   <Request>
     <EMailAddress>{EMAIL_ADDRESS}</EMailAddress>
     <AcceptableResponseSchema>
       http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a
     </AcceptableResponseSchema>
   </Request>
 </Autodiscover>""",
        headers={"Host": DOMAIN},
    )

    assert response.status_code == 400
    assert response.text == "URL must start with 'autodiscover'"


def test_pox_autodiscover_missing_host(test_client: TestClient) -> None:
    with pytest.raises(MissingHostError):
        test_client.post(
            "/autodiscover/autodiscover.xml",
            data=f"""<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006">
       <Request>
         <EMailAddress>{EMAIL_ADDRESS}</EMailAddress>
         <AcceptableResponseSchema>
           http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a
         </AcceptableResponseSchema>
       </Request>
     </Autodiscover>""",
            headers={"Host": ""},
        )
