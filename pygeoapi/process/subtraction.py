# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2019 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import logging
import numpy as np
from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError
import requests

LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '0.2.0',
    'id': 'computation-subtraction',
    'title': {
        'en': 'computation-subtraction',
    },
    'description': {
        'en': 'Computation process that subtracts two inputs',
    },
    'keywords': ['trends','subtraction'],
    'links': [{
        'type': 'text/html',
        'rel': 'canonical',
        'title': 'information',
        'href': 'https://example.org/process',
        'hreflang': 'en-US'
    }],
    'outputs': {
        'result': {
            'title': 'Result',
            'description': 'The result of the subtraction',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
           'instance1': '2021-09-02T00:00:00',
           'instance2': '2021-09-02T06:00:00',
           'coords': 'POINT(-77.725999 36.047816)',
           'parameter-name': 'TMP_P0_L1_GLL0',
           'datetime': ''
        }
    }
}


class ComputationSubtractionProcessor(BaseProcessor):

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.process.hello_world.ComputationSubtractionProcessor
        """

        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data):

        mimetype = 'application/json'
        coords = data.get('coords', None)
        parameter_name = data.get('parameter-name', None)
        datetime = data.get('datetime', None)
        instance1= data.get('instance1', None)
        instance2= data.get('instance2', None)

        request_url_1='http://data-api-c.mdl.nws.noaa.gov/OGC-EDR-API/collections/automated_gfs_100_forecast_time0_lat_0_lon_0_ground_or_water_surface/instances/'+instance1+'/position?coords='+coords+'&parameter-name='+parameter_name+'&datetime='+datetime+'&f=CoverageJSON'

        request_url_2='http://data-api-c.mdl.nws.noaa.gov/OGC-EDR-API/collections/automated_gfs_100_forecast_time0_lat_0_lon_0_ground_or_water_surface/instances/'+instance2+'/position?coords='+coords+'&parameter-name='+parameter_name+'&datetime='+datetime+'&f=CoverageJSON'
        rq1_json=requests.get(request_url_1).json()
        rq2_json=requests.get(request_url_2).json()
        
        rq1_time_array=rq1_json['domain']['axes']['t']['values']
        rq2_time_array=rq2_json['domain']['axes']['t']['values']
        rq1_data_array=rq1_json['ranges'][parameter_name]['values']
        rq2_data_array=rq2_json['ranges'][parameter_name]['values']
        
        outputs=rq2_json
        outputs['ranges'][parameter_name]['values']=(np.array(rq1_data_array)-np.array(rq2_data_array)).tolist()
        #outputs eventually will be the coveragejson response
        return mimetype, outputs

    def __repr__(self):
        return '<ComputationSubtractionProcessor> {}'.format(self.name)
