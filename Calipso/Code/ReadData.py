# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 11:50:06 2021

@author: Hengheng Zhang

contact: hengheng.zhang@kit.edu

Function: 
"""
from pyhdf.SD import SD, SDC
import os 
import matplotlib.pyplot as plt

import cartopy.crs as ccrs   #投影方式
from tqdm import tqdm
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter  #将x，y轴换成经纬度
import cartopy.feature as cfeat   #使用shp文件
from cartopy.io.shapereader import Reader  #读取自定的shp文件
import numpy as np
fontdicts={'weight': 'bold', 'size': 15}
for filename in os.listdir('../Data/SelectData'):
    
    file = SD('../Data/'+filename, SDC.READ)
    datasets_dic = file.datasets()
    sds_obj = file.select('Longitude') # select sds
    Longitude = sds_obj.get() # get sds data
    sds_obj = file.select('Latitude') # select sds
    Latitude = sds_obj.get() # get sds data
    
    # sds_obj = file.select('Total_Attenuated_Backscatter_532') # select sds
    # Total_Attenuated_Backscatter_532= sds_obj.get()
    # aa =Total_Attenuated_Backscatter_532[1,:]
    # aa = np.where(aa<0,np.nan,aa)
    # aa = aa[-100:]
    # plt.plot(aa[::-1])
    fig = plt.figure(figsize=(10,6),dpi=120)
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=0))
    ax.set_xticks([-30,-10,10,30,50,70])
    ax.set_yticks([10,30,50,70,90])
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.plot(Latitude,Longitude,color = 'green')
    ax.set_xlim(-30,70)
    ax.set_ylim(0,90)
    ax.coastlines()
    ax.set_ylabel('Latitude',fontdict = fontdicts)
    ax.set_xlabel('Longitude',fontdict = fontdicts)
    ax.scatter(8.4037,49.0069,marker = '*',s=30,color='red')
    for tick in ax.xaxis.get_major_ticks():
              tick.label.set_fontsize(20) 
    for tick in ax.yaxis.get_major_ticks():
              tick.label.set_fontsize(20) 
    ax.set_title(filename[26:45],fontdict = fontdicts)
    plt.savefig('../Figure/Track/SelectData/'+filename[26:45]+'.png')
    plt.close()


     
