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

def createVectorLayer(url:str,parentID:int,display_name:str,geometry_type:str,fields:list,srs:int=4326,description:str=''):
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

def addPointToVectorLayer(url: str, layer_id: int, geometry: dict, attributes: dict):
    r = requests.post(
        url=url,
        json={
            "geometry": geometry,
            "properties": attributes
        },
        auth=AUTH
    )
    return r
