from tinydb import TinyDB, Query
import json
import os
import requests
from datetime import datetime
import argparse



def edr_meta_to_oar(edr_api_url):
   #variables to fulfill
   edr_rq=requests.get(edr_api_url)
   edr_meta_dict=edr_rq.json()
   identifier=edr_meta_dict['id']
   first_param_iter=next(iter(edr_meta_dict['parameters']))
   bbox=edr_meta_dict['parameters'][first_param_iter]['extent']['horizontal']['geographic']
   bbox_crs=edr_meta_dict['crs']
   minx=bbox.split(',')[0].replace('BBOX[','')
   miny=bbox.split(',')[1]
   maxx=bbox.split(',')[2]
   maxy=bbox.split(',')[3].replace(']','')
   issued=datetime.now().isoformat()
   type_='dataset'
   title=edr_meta_dict['title']
   description=edr_meta_dict['description']
   contact='Shane Mill'
   links=''
   themes=''
   te_begin=edr_meta_dict['extent']['temporal']['range'][0]
   te_end=edr_meta_dict['extent']['temporal']['range'][-1]

   OAP_REC_JSON={
        'id': identifier,
        'type': 'Feature',
        'geometry': {
            'type': 'Polygon',
            'coordinates': [[
                [minx, miny],
                [minx, maxy],
                [maxx, maxy],
                [maxx, miny],
                [minx, miny]
            ]]
        },
        'properties': {
            'recordCreated': issued,
            'recordUpdated': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'type': type_,
            'title': title,
            'description': description,
            'contactPoint': contact,
            'associations': links,
            'externalId': [{
                'scheme': 'default',
                'value': identifier
            }],
            'themes': themes,
            'extent': {
                'spatial': {
                    'bbox': [bbox],
                    'crs': bbox_crs
                },
                'temporal': {
                    'interval': [te_begin, te_end],
                    'trs': 'http://www.opengis.net/def/uom/ISO-8601/0/Gregorian'  # noqa
                }
            },
            '_metadata-anytext': ''
        }
    }

   anytext = ' '.join(OAP_REC_JSON)
   OAP_REC_JSON['_metadata-anytext']=anytext
   return OAP_REC_JSON


def export_to_tinydb(oap_rec):
   try:
      os.remove('db.json')
   except:
      pass
   db = TinyDB('db.json')
   db.insert(oap_rec)
   return


if __name__ == "__main__":

   edr_api_url='http://data-api-c.mdl.nws.noaa.gov/OGC-EDR-API/collections/metar/instances/latest?f=application%2Fjson'
   oap_rec=edr_meta_to_oar(edr_api_url)
   export_to_tinydb(oap_rec)

