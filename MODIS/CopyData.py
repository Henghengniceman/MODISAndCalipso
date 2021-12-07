# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 16:46:37 2021

@author: Hengheng Zhang

contact: hengheng.zhang@kit.edu

Function: 
"""

from datetime import datetime,timedelta
import os 
import shutil
from tqdm import tqdm

MainPath = 'C:/Users/ka1319/Downloads/'
for file in tqdm(os.listdir(MainPath)):
    if file.startswith('MOD'):
        Day =  float(file[15:17])
        DataPath = (datetime(2021, 1, 1) + timedelta(Day - 1)).strftime('%Y%m%d')
        FinalPath = 'D:/MODIS Data/Data/Terra/'+DataPath
        if not os.path.exists(FinalPath):
            os.makedirs(FinalPath)
        shutil.copy(MainPath+file,FinalPath)

       