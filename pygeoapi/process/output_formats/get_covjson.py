import numpy as np
import requests


def computation_subtraction_covjson(request_url_1,request_url_2,parameter_name):
        mimetype = 'application/json'
        rq1_json=requests.get(request_url_1).json()
        rq2_json=requests.get(request_url_2).json()

        rq1_time_array=rq1_json['domain']['axes']['t']['values']
        rq2_time_array=rq2_json['domain']['axes']['t']['values']
        rq1_data_array=rq1_json['ranges'][parameter_name]['values']
        rq2_data_array=rq2_json['ranges'][parameter_name]['values']

        outputs=rq2_json
        outputs['ranges'][parameter_name]['values']=(np.array(rq1_data_array)-np.array(rq2_data_array)).tolist()
        return mimetype, outputs

