# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 17:24:05 2021

@author: Hengheng Zhang

contact: hengheng.zhang@kit.edu

Function: 
"""

from pyhdf.SD import SD, SDC
import os 
import matplotlib.pyplot as plt
import xarray as xr
from pyhdf.HDF import *
from pyhdf.VS import *
from matplotlib import ticker, cm

# import cartopy.crs as ccrs   #投影方式
# from tqdm import tqdm
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter  #将x，y轴换成经纬度
# import cartopy.feature as cfeat   #使用shp文件
# from cartopy.io.shapereader import Reader  #读取自定的shp文件
import numpy as np
from tqdm import tqdm

fontdicts={'weight': 'bold', 'size': 15}
ProductName = 'Feature_Classification_Flags'
for filename in tqdm(os.listdir('../Data')[175:176]):
    if filename.startswith('CAL_LID_L2_VFM'):
    
    #%% Get Attitude
        hdf_interface = HDF('../Data/'+filename)
        vs_interface = hdf_interface.vstart()
        meta = vs_interface.attach("metadata")
        field_infos = meta.fieldinfo()
        all_data = meta.read(meta._nrecs)[0]
        meta.detach()
        data_dictionary = {}
        field_name_index = 0
        for field_info, data in zip(field_infos, all_data):
            data_dictionary[field_info[field_name_index]] = data
        lidar_altitudes = np.array(data_dictionary["Lidar_Data_Altitudes"])
        
        file = SD('../Data/'+filename, SDC.READ)
        datasets_dic = file.datasets()
        sds_obj = file.select('Longitude') # select sds
        Longitude = sds_obj.get() # get sds data
        sds_obj = file.select('Latitude') # select sds
        Latitude = sds_obj.get() # get sds data
        sds_obj = file.select(ProductName) # select sds
        data= sds_obj.get()
        
        