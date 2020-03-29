import xarray as xr
from collections import OrderedDict
import os

eulrdir = "/home/HPCS/bipink/Avizo_test/0.5m/New_Data/Eulerian/"
destdir = "/home/HPCS/bipink/Avizo_test/0.5m/New_Data/Eulerian/eul_data_for_avizo/"

files = sorted([x for x in os.listdir(eulrdir) if x.endswith('.nc')])

start = 0
stop = len(files)
stride = 1

for i in range(start,stop):

  eulrfile = os.path.join(eulrdir,files[i])
  destfile = os.path.join(destdir,files[i])
  
  data = xr.open_dataset(eulrfile)
  
  zindices, yindices, xindices = [data[dim].astype(int)[::stride] for dim in ('z', 'y', 'x')]
  
  coords = OrderedDict([('z', zindices),('y', yindices),('x', xindices)])
  
  newdata = xr.Dataset(coords=coords)
      
  dims = ['z', 'y', 'x']
  
  variables = [v for v in data.variables if v in ('mixing_ratio')]
  
  for variable in variables:
      tempdata = data[variable][::stride,::stride,::stride]
      newdataarray = xr.DataArray(tempdata.astype('float64'),
              dims=dims, coords=coords)
  
      newdata.update({variable: newdataarray})
      newdata[variable].encoding['_FillValue'] = False
  
      print(variable,newdata[variable].shape, newdata[variable].dtype) ##info
  
  newdata.x.encoding['_FillValue'] = False
  newdata.y.encoding['_FillValue'] = False
  newdata.z.encoding['_FillValue'] = False
  
  print(newdata, '\n\n')
  
  # write netcdf file
  newdata.to_netcdf(path=destfile,format='NETCDF4_CLASSIC')