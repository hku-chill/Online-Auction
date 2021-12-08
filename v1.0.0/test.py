# from suds.client import Client
 
# WSDL_URL="https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL"
# client=Client(WSDL_URL)
 
# args={
#     "TCKimlikNo":11111111111,
#     "Ad":"ADINIZI BÜYÜK HARFLERLE",
#     "Soyad":"SOYADINIZ BÜYÜK HARFLERLE",
#     "DogumYili":1982
# }
 
# def tcKimlikDogrula(params):
#     try:
#         return  client.service.TCKimlikNoDogrula(**params)
#     except Exception as e:
#         return False
 
# if __name__=="__main__":
#     if tcKimlikDogrula(args):
#         print("Doğru")
#     else:
#         print("Yanlış")

import requests
url="https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL"
headers = {'content-type': 'application/soap+xml'}
body = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <TCKimlikNoDogrula xmlns="http://tckimlik.nvi.gov.tr/WS">
      <TCKimlikNo>55900299672</TCKimlikNo>
      <Ad>MAHIR TEKIN</Ad>
      <Soyad>ERDENSAN</Soyad>
      <DogumYili>1998</DogumYili>
    </TCKimlikNoDogrula>
  </soap12:Body>
</soap12:Envelope>"""

response = requests.post(url,data=body.encode('utf-8'),headers=headers)

print(response.text)