# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 13:45:59 2021

@author: Hengheng Zhang

contact: hengheng.zhang@kit.edu

Function: 
"""
from pyhdf.SD import SD, SDC
import os 
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs   #投影方式
from tqdm import tqdm
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter  #将x，y轴换成经纬度
import cartopy.feature as cfeat   #使用shp文件
from cartopy.io.shapereader import Reader  #读取自定的shp文件

fontdicts={'weight': 'bold', 'size': 15}
for Day in tqdm(os.listdir('../Data/Terra/')[1:2]):
    fig = plt.figure(figsize=(16,9),dpi=120)
    ax = fig.add_subplot(121, projection=ccrs.PlateCarree(central_longitude=0))
    ax.set_xticks([-30,-10,10,30,50,70])
    ax.set_yticks([10,30,50,70,90])
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    for filename in tqdm(os.listdir('../Data/Terra/'+Day)):
        
    
        file = SD('../Data/Terra/'+Day+'/'+filename, SDC.READ)
        # f = h5py.File('../Data/'+FileNames[5], 'r')
        # print(f.keys())    
        # print(file.info())
        datasets_dic = file.datasets()
        # file.close()
        # for idx,sds in enumerate(datasets_dic.keys()):
        #     print (idx,sds)
        sds_obj = file.select('Longitude') # select sds
        Longitude = sds_obj.get() # get sds data
        
        sds_obj = file.select('Latitude') # select sds
        Latitude = sds_obj.get() # get sds data
        
        
        sds_obj = file.select('AOD_550_Dark_Target_Deep_Blue_Combined') # select sds
        AOD = sds_obj.get() # get sds data
    
        add_offset = sds_obj.attributes()['add_offset']
        scale_factor = sds_obj.attributes()['scale_factor']
        AOD = (AOD - add_offset) * scale_factor
        AOD = np.array(AOD)    
        AOD = np.where(AOD<0,np.nan,AOD)
        AOD[-1,-1] = 0.65
        AOD[0,0] = 0
        # AOD [:,0]=np.nan
        proj = ccrs.PlateCarree()
        
        ac = ax.contourf(Longitude,Latitude, AOD,vim=0,vmax=0.65)
        
        ax.set_xlim(-30,70)
        ax.set_ylim(0,90)
        AOD  = list(AOD)
    ax.coastlines()
    ax.set_title('MODIS AOD @ 550 nm',fontdict = fontdicts)
    ax.set_ylabel('Latitude',fontdict = fontdicts)
    ax.set_xlabel('Longitude',fontdict = fontdicts)
    
    for tick in ax.xaxis.get_major_ticks():
              tick.label.set_fontsize(20) 
    for tick in ax.yaxis.get_major_ticks():
              tick.label.set_fontsize(20) 
    
    Germany_shp1 = Reader('../gadm36_DEU_shp/gadm36_DEU_0.shp')
    fea_pro = cfeat.ShapelyFeature(Germany_shp1.geometries(), proj,
                                  edgecolor='darkolivegreen', facecolor='none')
    ax.add_feature(fea_pro, linewidth=0.3, alpha=0.5)
    ax.scatter(8.4037,49.0069,marker = '*',s=30,color='red')
    
    # l = 0.47
    # b = 0.15
    # w = 0.01
    # h = 0.7
    # #对应 l,b,w,h；设置colorbar位置；
    # rect = [l,b,w,h] 
    # cbar_ax = fig.add_axes(rect) 
    # cb = plt.colorbar(ac, cax=cbar_ax)
    cb=fig.colorbar(ac, ax=ax,orientation='horizontal',fraction=0.04,pad=0.16)
    cb.set_label('AOD' ,fontdict=fontdicts) #设置colorbar的标签字体及其大小
    cb.ax.tick_params(labelsize=20)
    
    ax = fig.add_subplot(122, projection=ccrs.PlateCarree(central_longitude=0))
    ax.set_xticks([-30,-10,10,30,50,70])
    ax.set_yticks([10,30,50,70,90])
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    fontdicts={'weight': 'bold', 'size': 15}
    for filename in tqdm(os.listdir('../Data/Terra/'+Day)):
        
    
        file = SD('../Data/Terra/'+Day+'/'+filename, SDC.READ)
        # f = h5py.File('../Data/'+FileNames[5], 'r')
        # print(f.keys())    
        # print(file.info())
        datasets_dic = file.datasets()
        # file.close()
        # for idx,sds in enumerate(datasets_dic.keys()):
        #     print (idx,sds)
        sds_obj = file.select('Longitude') # select sds
        Longitude = sds_obj.get() # get sds data
        
        sds_obj = file.select('Latitude') # select sds
        Latitude = sds_obj.get() # get sds data
        
        
        sds_obj = file.select('Deep_Blue_Angstrom_Exponent_Land') # select sds
        AOD = sds_obj.get() # get sds data
    
        add_offset = sds_obj.attributes()['add_offset']
        scale_factor = sds_obj.attributes()['scale_factor']
        AOD = (AOD - add_offset) * scale_factor
        AOD = np.array(AOD)    
        AOD = np.where(AOD<0,np.nan,AOD)
        AOD[-1,-1] = 4
        AOD[0,0] = 0
        # AOD [:,0]=np.nan
        proj = ccrs.PlateCarree()
        
        ac = ax.contourf(Longitude,Latitude, AOD,vim=0,vmax=4)
        
        ax.set_xlim(-30,70)
        ax.set_ylim(0,90)
        # AOD  = list(AOD)
    ax.coastlines()
    ax.set_title('Angstrom Exponent (660nm/470nm)',fontdict = fontdicts)
    ax.set_ylabel('Latitude',fontdict = fontdicts)
    ax.set_xlabel('Longitude',fontdict = fontdicts)
    
    for tick in ax.xaxis.get_major_ticks():
              tick.label.set_fontsize(20) 
    for tick in ax.yaxis.get_major_ticks():
              tick.label.set_fontsize(20) 
    
    Germany_shp1 = Reader('../gadm36_DEU_shp/gadm36_DEU_0.shp')
    fea_pro = cfeat.ShapelyFeature(Germany_shp1.geometries(), proj,
                                  edgecolor='darkolivegreen', facecolor='none')
    ax.add_feature(fea_pro, linewidth=0.3, alpha=0.5)
    ax.scatter(8.4037,49.0069,marker = '*',s=30,color='red')
    
    # l = 0.92
    # b = 0.15
    # w = 0.01
    # h = 0.7
    # #对应 l,b,w,h；设置colorbar位置；
    # rect = [l,b,w,h] 
    # cbar_ax = fig.add_axes(rect) 
    cb=fig.colorbar(ac, ax=ax,orientation='horizontal',fraction=0.04,pad=0.16)
    cb.set_label('AE' ,fontdict=fontdicts) #设置colorbar的标签字体及其大小    # cb.set_label('[%]' ,fontdict=fontdicts) #设置colorbar的标签字体及其大小
    cb.ax.tick_params(labelsize=20)
    plt.subplots_adjust(wspace=0.3, hspace=0)
# plt.suptitle('2021-'+Day[4:6]+'-'+Day[6:8],fontsize=25)
    ax.text(-65,101,'2021-'+Day[4:6]+'-'+Day[6:8],fontdict={'weight': 'bold', 'size': 20})
    plt.savefig('../Figure/Terra/AOD_AE'+Day+'.png')

    plt.close()
    # plt.clabel(ac, inline=True, fontsize=8, fmt='%.0f')
    
    
    
    
