# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 11:29:58 2021

@author: Hengheng Zhang

contact: hengheng.zhang@kit.edu

Function: 
"""
from urllib import request
from tqdm import tqdm
MainUrl = 'https://xfr139.larc.nasa.gov/sflops/Distribution/2021340112002_63467/'
with open('../filelist_1638807487.txt') as f:
    lines = f.readlines()
lines = lines[4:]

for line in tqdm(lines):
    Url = MainUrl+line[:-5]+'_Subset'+line[-5:-1]
    request.urlretrieve(Url, "../Data/"+line[:-5]+'_Subset'+line[-5:-1])
