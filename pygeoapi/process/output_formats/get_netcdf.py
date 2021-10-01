import io
import numpy as np
import requests
import xarray as xr

def computation_subtraction_netcdf(request_url_1,request_url_2,parameter_name):
        mimetype = 'application/x-netcdf4'
        rq1_bytes=requests.get(request_url_1).content
        rq2_bytes=requests.get(request_url_2).content
        rq1_ds=xr.open_dataset(io.BytesIO(rq1_bytes))
        rq2_ds=xr.open_dataset(io.BytesIO(rq2_bytes)) 
        output_base=rq2_ds

        #something in this block is causing invalid netcdf
        rq1_step=rq1_ds.step.values
        rq2_step=rq2_ds.step.values
        valid_time_rq1=rq1_ds.valid_time.values
        valid_time_rq2=rq2_ds.valid_time.values
        rq1_ds=rq1_ds.drop('valid_time')
        rq2_ds=rq2_ds.drop('valid_time')
        rq1_ds=rq1_ds.rename({'step':'valid_time'})
        rq2_ds=rq2_ds.rename({'step':'valid_time'})       
        rq1_ds=rq1_ds.assign_coords({'valid_time':valid_time_rq1.astype(str)})
        rq2_ds=rq2_ds.assign_coords({'valid_time':valid_time_rq2.astype(str)})
        valid_time_intersect=np.intersect1d(valid_time_rq1,valid_time_rq2)
        valid_time_min=str(valid_time_intersect.min())
        valid_time_max=str(valid_time_intersect.max())
        rq1_ds=rq1_ds.sel({'valid_time':slice(valid_time_min,valid_time_max)})
        rq2_ds=rq2_ds.sel({'valid_time':slice(valid_time_min,valid_time_max)})
        output=rq2_ds

        output_base=output_base.isel({'step':slice(0,len(output_base['step'].values)-2)})
        for data_vars in rq1_ds.data_vars:
            output_base[data_vars].values=(rq1_ds[data_vars].values-rq2_ds[data_vars].values).astype(np.float32)
        import pdb; pdb.set_trace()
        outputs='/tmp/output.netcdf'
        output_base.attrs['_FillValue']=np.nan
        output_base.to_netcdf(outputs)
        return mimetype, outputs

