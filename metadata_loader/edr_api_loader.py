from tinydb import TinyDB, Query
import json
import os
import requests
from datetime import datetime

def edr_meta_to_oar():
   #variables to fulfill
   identifier=''
   minx=''
   miny=''
   maxx=''
   maxy=''
   issued=''
   type_=''
   title=''
   description=''
   contact=''
   links=''
   themes=''
   bbox=''
   bbox_crs=''
   te_begin=''
   te_end=''
   _anytext=''

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
            '_metadata-anytext': _anytext
        }
    }
   return OAP_REC_JSON


def export_to_tinydb(oap_rec):
   try:
      os.remove('db.json')
   except:
      pass
   db = TinyDB('db.json')
   import pdb; pdb.set_trace()
   print('test')
   db.insert(oap_rec)
   return



if __name__ == "__main__":
   oap_rec=edr_meta_to_oar()
   export_to_tinydb(oap_rec)

