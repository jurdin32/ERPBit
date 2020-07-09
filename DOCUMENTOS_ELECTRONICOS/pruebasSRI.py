import zeep

url = 'https://cel.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl'
client = zeep.Client(wsdl=url)
respuesta=client.service.autorizacionComprobante('2812201801070388669700120010010000000640000000010')
print(respuesta)