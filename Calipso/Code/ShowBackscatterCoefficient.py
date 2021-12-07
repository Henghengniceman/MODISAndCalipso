# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 14:22:30 2021

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
ProductName = 'Perpendicular_Attenuated_Backscatter_532'
for filename in tqdm(os.listdir('../Data')[0:2]):
    
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
    Product= sds_obj.get()
    Product = np.where(Product<0,np.nan,Product)
    # Product = Product*1e9
    
    # plt.plot(Product[1,:])
    Attitude = list(np.arange(1,5)*300)+list(np.arange(5,296)*30)+list(np.arange(296,496)*60)+list(np.arange(496,551)*180)+list(np.arange(551,584)*300)
    Attitude = np.array(Attitude)
    Attitude = Attitude[::-1]
    Longitude = Longitude[:,0]
    X,Y = np.meshgrid(Longitude, lidar_altitudes[289:])
    Product = Product.T
    # Productds = xr.Dataset(
    #       {
    #         "Product":(("Attitude",'Longitude'),Product[:,289:].T),
    #       },
    #         coords={
    #         "Attitude":lidar_altitudes[289:],
        
    #         "Longitude": Longitude,
    #               }, 
    #     )        
    
    # Productda = Productds.Product
    # ProfileSingle = Product[:,26266]
    # fig, axes = plt.subplots(1, 1,figsize=(5, 6),dpi=120)  
    # axes.plot(ProfileSingle,lidar_altitudes)
    # axes.set_ylim([0,8])
    
    with plt.style.context(['science','no-latex']):
        fig, axes = plt.subplots(1, 1,figsize=(16, 6),dpi=120)  
        cs = axes.contourf(X, Y, Product[289:,:], locator=ticker.LogLocator())
    
        # cs = Productda.plot.contourf(
        #         ax=axes,
        #         # vmin = 0,
        #         # vmax = 6,
        #         # y="Range",
        #         levels=13,
        #         robust=True,
        #         cmap = 'jet',
        #         add_colorbar=False,
        #         locator=ticker.LogLocator(),
                
        #               )
        cbar=fig.colorbar(cs, ax=axes,orientation='vertical',fraction=0.04,pad=0.1)
        cbar.set_label('K$\mathregular{m^-}$$\mathregular{^1}$$\mathregular{Sr^-}$$\mathregular{^1}$',fontdict=fontdicts)
        cbar.ax.tick_params(labelsize=20)
        axes.axvline(8.4037,color='r',ls='--',lw=2)
        axes.set_title(ProductName+'@'+filename[26:45],fontdict=fontdicts)
        axes.set_ylabel('Attitude [km]',fontdict=fontdicts)
        axes.set_xlabel('Longitude',fontdict=fontdicts,labelpad = 12.5)
    axes.xaxis.set_major_formatter(LongitudeFormatter())
    # axes.yaxis.set_major_formatter(LatitudeFormatter())
    plt.savefig('../Figure/'+ProductName+'@'+filename[26:45]+'.png')
    plt.close()
        
    #color bar
       