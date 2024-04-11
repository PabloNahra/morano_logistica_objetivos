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

def vtex_sku_by_ref_id(sku=''):
    try:
        # Busco datos del SKU a partir del SKU que le llega
        # https://developers.vtex.com/docs/api-reference/catalog-api#get-/api/catalog/pvt/stockkeepingunit?endpoint=get-/api/catalog/pvt/stockkeepingunit
        sku_by_ref_id = vtex_requests(vtex_url=f"https://stylewatch.vtexcommercestable.com.br/api/catalog/pvt/"
                                               f"stockkeepingunit?RefId={sku}",
                                      vtex_appkey="vtexappkey-stylewatch-GQVYIK",
                                      vtex_apptoken="VXWQRLVWNMJGBWIHBYOSCPHZSTTXYJYSQOOEBMIPXXRTYZHJCFZQGFPFPXXXSXYDORQNHEFPQZUEXNATMKVSKILKYJODOKWZZOFHJTBYZJZHKKHBXEKICFSGFFOXPBBF")

        # Tomamos mas datos del SKU
        sku_by_id = vtex_requests(vtex_url=f"https://stylewatch.vtexcommercestable.com.br/api/catalog_system/pvt/sku/stockkeepingunitbyid/{sku_by_ref_id['Id']}",
                                      vtex_appkey="vtexappkey-stylewatch-GQVYIK",
                                      vtex_apptoken="VXWQRLVWNMJGBWIHBYOSCPHZSTTXYJYSQOOEBMIPXXRTYZHJCFZQGFPFPXXXSXYDORQNHEFPQZUEXNATMKVSKILKYJODOKWZZOFHJTBYZJZHKKHBXEKICFSGFFOXPBBF")

        '''
        # Datos de la imagen principal
        # https://developers.vtex.com/docs/api-reference/catalog-api#get-/api/catalog/pvt/stockkeepingunit/-skuId-/file?endpoint=get-/api/catalog/pvt/stockkeepingunit/-skuId-/file
        # https://stylewatch.vteximg.com.br/arquivos/ids/244058-100-100/kit-gm00002.jpg
        sku_image = vtex_requests(vtex_url=f"https://stylewatch.vtexcommercestable.com.br/api/catalog/pvt/stockkeepingunit/"
                                           f"{sku_by_ref_id['Id']}/file",
                                      vtex_appkey="vtexappkey-stylewatch-GQVYIK",
                                      vtex_apptoken="VXWQRLVWNMJGBWIHBYOSCPHZSTTXYJYSQOOEBMIPXXRTYZHJCFZQGFPFPXXXSXYDORQNHEFPQZUEXNATMKVSKILKYJODOKWZZOFHJTBYZJZHKKHBXEKICFSGFFOXPBBF")
        # Filtro solo la primera principal
        # main_image = next((img for img in sku_image if img.get('IsMain', False)), None)
        '''

        # combino datos
        # sku_info_vtex = [{sku_by_ref_id['id'], sku_by_id['NameComplete']}]
        # sku_info_vtex = []
        sku_info_vtex = {'RefId': sku_by_ref_id['RefId'],
                         'URL': f"https://www.stylestore.com.ar{sku_by_id['DetailUrl']}",
                         'NAME': sku_by_id['NameComplete'],
                         'URL_IMAGE': sku_by_id['ImageUrl'],
                             # f"https://stylewatch.vteximg.com.br/arquivos/ids/{main_image['ArchiveId']}-100-100/"
                             # f"{main_image['Name']}.jpg",
                         'CATEGORY': sku_by_id['ProductCategories'],
                         'TAG': sku_by_id['KeyWords'],
                         }

        return sku_info_vtex

    except Exception as e:
        # Si ocurre un error, lanza una nueva excepción con un mensaje personalizado
        raise Exception(f"Error en búsqueda del SKU en VTEX: {e}")
