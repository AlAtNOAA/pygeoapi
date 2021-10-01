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

import io
import logging
import numpy as np
from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError
from pygeoapi.process.output_formats import get_covjson, get_netcdf 
import requests
import xarray as xr
import flask

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
           'sampling_geometry': 'cube',
           'collection_name': 'automated_gfs_100_forecast_time0_lat_0_lon_0_ground_or_water_surface',
           'instance1': '2021-09-02T00:00:00',
           'instance2': '2021-09-02T06:00:00',
           'coords': 'POLYGON((-134.315336 27.319254,-134.315336 55.952663,-66.484018 55.952663,-66.484018 27.319254,-134.315336 27.319254))',
           'parameter-name': 'TMP_P0_L1_GLL0',
           'datetime': '',
           'f':'CoverageJSON'
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

        collection_name=data.get('collection_name',None)
        f=data.get('f',None)
        coords = data.get('coords', None)
        parameter_name = data.get('parameter-name', None)
        datetime = data.get('datetime', None)
        instance1= data.get('instance1', None)
        instance2= data.get('instance2', None)
        sampling_geometry= data.get('sampling_geometry', None)

        request_url_1='http://data-api-c.mdl.nws.noaa.gov/OGC-EDR-API/collections/'+collection_name+'/instances/'+instance1+'/'+sampling_geometry+'?coords='+coords+'&parameter-name='+parameter_name+'&datetime='+datetime+'&f='+f

        request_url_2='http://data-api-c.mdl.nws.noaa.gov/OGC-EDR-API/collections/'+collection_name+'/instances/'+instance2+'/'+sampling_geometry+'?coords='+coords+'&parameter-name='+parameter_name+'&datetime='+datetime+'&f='+f
        
        if f=='CoverageJSON':
           mimetype, outputs=get_covjson.computation_subtraction_covjson(request_url_1,request_url_2,parameter_name)
           return mimetype, outputs
        if f=='NetCDF':
           mimetype, output_loc=get_netcdf.computation_subtraction_netcdf(request_url_1,request_url_2,parameter_name)
           return mimetype, output_loc                    


    def __repr__(self):
        return '<ComputationSubtractionProcessor> {}'.format(self.name)
