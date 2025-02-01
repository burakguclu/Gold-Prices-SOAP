import requests
import xml.etree.ElementTree as ET

url = "http://data.altinkaynak.com/DataService.asmx"

payload = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <AuthHeader xmlns="http://data.altinkaynak.com/">
      <Username>AltinkaynakWebServis</Username>
      <Password>AltinkaynakWebServis</Password>
    </AuthHeader>
  </soap:Header>
  <soap:Body>
    <GetGold xmlns="http://data.altinkaynak.com/" />
  </soap:Body>
</soap:Envelope>"""

headers = {
    'Content-Type': 'text/xml; charset=utf-8',
    'Host': 'data.altinkaynak.com',
    'SOAPAction': "http://data.altinkaynak.com/GetGold"
}

response = requests.post(url, headers=headers, data=payload)

root = ET.fromstring(response.text)

namespace = {
    "soap": "http://schemas.xmlsoap.org/soap/envelope/",
    "altin": "http://data.altinkaynak.com/"
}

body = root.find("soap:Body", namespace)
if body is not None:
    result = body.find(".//altin:GetGoldResult", namespace)
    if result is not None:
        gold_data = ET.fromstring(result.text)

        print("\nAltın Fiyatları:\n")
        print(f"{'Kod':<10} {'Açıklama':<20} {'Alış':<12} {'Satış':<12} {'Güncellenme Zamanı'}")
        print("-" * 65)

        for kur in gold_data.findall("Kur"):
            kod = kur.find("Kod").text
            aciklama = kur.find("Aciklama").text
            alis = kur.find("Alis").text
            satis = kur.find("Satis").text
            guncellenme = kur.find("GuncellenmeZamani").text

            print(f"{kod:<10} {aciklama:<20} {alis:<12} {satis:<12} {guncellenme}")

    else:
        print("Yanıt içinde GetGoldResult bulunamadı.")
else:
    print("Yanıt içinde Body etiketi bulunamadı.")
