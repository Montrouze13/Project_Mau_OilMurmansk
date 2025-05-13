import requests
from secret import *

def createResourceGroup(url,parentID,display_name,description):
    r= requests.post(
        url=url,
        json={
            "resource": {
                "cls":"resource_group",
                "parent":{"id":parentID},
                "display_name": display_name,
                "description": description,}
        },
        auth=AUTH
    )
    return r

def createVectorLayer(url:str,parentID:int,display_name:str,geometry_type:str,fields:list,srs:int=3857,description:str=''):
    r= requests.post(
        url=url,
        json={
            "resource": {
                "cls":"vector_layer",
                "parent":{"id":parentID},
                "display_name": display_name,
                "description": description,},
            "vector_layer":{
                "srs":{ "id": srs },
                "geometry_type": geometry_type,
                "fields": fields,
            }
        },
        auth=AUTH
    )
    return r


def addFeature(resId: int, feature: dict):
    return requests.post(
        url=f'https://geo.mauniver.ru/api/resource/{resId}/feature/?src=3857',
        json=feature,
        auth=AUTH

    )
