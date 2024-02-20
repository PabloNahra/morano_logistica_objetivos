import requests


def vtex_requests(vtex_url='', vtex_appkey='', vtex_apptoken=''):

    # url = "https://stylewatch.vtexcommercestable.com.br/api/logistics/pvt/inventory/skus/4520"
    url = vtex_url

    headers = {
        "Content-Type": "charset=utf-8",
        "Accept": "application/json",
        "X-VTEX-API-AppKey": vtex_appkey,
        "X-VTEX-API-AppToken": vtex_apptoken
    }

    response = requests.get(url, headers=headers)

    response_json = response.json()

    return response_json

'''
# prueba
print(vtex_requests(vtex_url="https://stylewatch.vtexcommercestable.com.br/api/logistics/pvt/inventory/skus/4520",
                    vtex_appkey="vtexappkey-stylewatch-GQVYIK",
                    vtex_apptoken="VXWQRLVWNMJGBWIHBYOSCPHZSTTXYJYSQOOEBMIPXXRTYZHJCFZQGFPFPXXXSXYDORQNHEFPQZUEXNATMKVSKILKYJODOKWZZOFHJTBYZJZHKKHBXEKICFSGFFOXPBBF"))
'''

def vtex_sku_by_ref_id(sku=''):

    # https://developers.vtex.com/docs/api-reference/catalog-api#get-/api/catalog/pvt/stockkeepingunit?endpoint=get-/api/catalog/pvt/stockkeepingunit
    sku_by_ref_id = vtex_requests(vtex_url=f"https://stylewatch.vtexcommercestable.com.br/api/catalog/pvt/"
                                           f"stockkeepingunit?RefId={sku}",
                                  vtex_appkey="vtexappkey-stylewatch-GQVYIK",
                                  vtex_apptoken="VXWQRLVWNMJGBWIHBYOSCPHZSTTXYJYSQOOEBMIPXXRTYZHJCFZQGFPFPXXXSXYDORQNHEFPQZUEXNATMKVSKILKYJODOKWZZOFHJTBYZJZHKKHBXEKICFSGFFOXPBBF")
    print("sku_by_ref_id")
    print(sku_by_ref_id)

    # https://developers.vtex.com/docs/api-reference/catalog-api#get-/api/catalog/pvt/stockkeepingunit/-skuId-/file?endpoint=get-/api/catalog/pvt/stockkeepingunit/-skuId-/file
    # https://stylewatch.vteximg.com.br/arquivos/ids/244058-100-100/kit-gm00002.jpg
    sku_image = vtex_requests(vtex_url=f"https://stylewatch.vtexcommercestable.com.br/api/catalog/pvt/stockkeepingunit/"
                                       f"{sku_by_ref_id['Id']}/file",
                                  vtex_appkey="vtexappkey-stylewatch-GQVYIK",
                                  vtex_apptoken="VXWQRLVWNMJGBWIHBYOSCPHZSTTXYJYSQOOEBMIPXXRTYZHJCFZQGFPFPXXXSXYDORQNHEFPQZUEXNATMKVSKILKYJODOKWZZOFHJTBYZJZHKKHBXEKICFSGFFOXPBBF")

    print("sku_image")
    print(sku_image)

    # Categoria

    return



# SkuId=22714 ProductId = 1782312 ref_id = 'kit-gm00002'
vtex_sku_by_ref_id(sku='kit-gm00002')