# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 15:21:42 2023

@author: mastelin
"""

import numpy as np
import pandas as pd
import json
from flatten_dict import flatten,unflatten
import math
import os
import itertools
from os.path import exists
import zipfile
import pickle
#%% Functions
def open_file_get_points_fcsv(subject_filename,name_fcsv):
    zip = zipfile.ZipFile(subject_filename)
    
    file = zip.read(name_fcsv)
    
    file_string = file.decode("utf-8")
    points = []
    split_ = file_string.split('\r')
    
    if len(split_) == 1:
        split_ = file_string.split('\n')
        
    for i in range(3, len(split_)-1):
            point_split = split_[i].split(',')
            points.append([float(point_split[1]),float(point_split[2]),float(point_split[3])])
    
    return points

def open_file_get_points(filename, archive):
    f = archive.open(filename)

    
    data = json.load(f)
    
    point_list = data['markups'][0]['controlPoints']
    points = []
    for item in point_list:
        points.append(item['position'])
      
    return points

def open_file_get_length(filename, archive):
    f = archive.open(filename)
    
    data = json.load(f)
    if data['markups'][0]['measurements'][0]['enabled'] == True:
        return data['markups'][0]['measurements'][0]['value']
    else:
        return 0


def open_file_get_area(filename, archive):
    f = archive.open(filename)
    
    data = json.load(f)
    if data['markups'][0]['measurements'][3]['enabled'] == True:
        return data['markups'][0]['measurements'][3]['value']
    else:
        return 0



#%% Pseudo-code

path_for_mrb = '\definePath'
mrb_filenames = os.listdir(path_for_mrb)
   
   
df_columns = ['angle', 'length']


dict_store_coordinates = flatten(dict())
df =  pd.DataFrame(columns = df_columns, index = mrb_filenames)
    
for file in mrb_filenames:
    
    archive = zipfile.ZipFile(path_for_mrb+'/'+file, 'r') 
    mrk_json_filenames = [x for x in archive.namelist() if '.mrk.json' in x] # get all files with .mrk.json

    for json_file in mrk_json_filenames:
            
        column_name = str.lower(json_file.split('/')[2].replace('.mrk.json',''))
        index_ = json_file.split('/')[0]+'.mrb'
        
        if column_name  in ['f', 'reference', 'f_1', 'ref']:
            dict_store_coordinates[(file, 'Reference')]= open_file_get_points(json_file, archive)
        
        elif 'angle' in column_name:
            df[column_name].loc[index_]  = open_file_get_angle(json_file, archive)
            
            dict_store_coordinates[(file, column_name)]= open_file_get_points(json_file, archive)
        
        else:
            dict_store_coordinates[(file, column_name)]= open_file_get_points(json_file, archive)
            df[column_name].loc[index_]  = open_file_get_length(json_file, archive)
        
slicer_raw_data[(rater,'Points')] = unflatten(dict_store_coordinates)
slicer_raw_data[(rater,'Measurments')] = df

df.to_excel(path+'_results.xlsx')
