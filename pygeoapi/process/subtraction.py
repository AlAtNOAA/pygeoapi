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
    'inputs': {
        'input1': {
            'title': 'Input1',
            'description': 'first entry in subtraction',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['input1']
        },
        'input1': {
            'title': 'Input2',
            'description': 'second entry request in subtraction',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['input2']
        },
    },
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
            'input1': 'float, integer, array, or list',
            'input2': 'float, integer, array, or list',
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
        input1 = data.get('input1', None)
        input2 = data.get('input2', None)
        if input1 is None or input2 is None:
            raise ProcessorExecuteError('Cannot process with the given inputs. Check that the inputs are of type integer, float, or list')

        if isinstance(input1,list) and isinstance(input2,list):
           input1_np=np.array(input1)
           input2_np=np.array(input2)
           value=np.subtract(input1_np,input2_np).tolist()
        else:
           value=input1-input2
        outputs = {
            'id': 'result',
            'value': value
        }

        return mimetype, outputs

    def __repr__(self):
        return '<ComputationSubtractionProcessor> {}'.format(self.name)
