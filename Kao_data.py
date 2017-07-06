# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 22:37:39 2017

@author: Leon
"""

import twd97
import numpy as np
import simplekml
import os
import pandas as pd
import sys,getopt

def twd97tokml(txtname):
    loadedData = np.loadtxt(txtname, dtype=np.str)
    kml = simplekml.Kml()
    data = []
    for i in range(len(loadedData)):
        QQ = loadedData[i].split(',')
        data.append(QQ)
    
    for i in range(len(data)):
        name = data[i][0]
        N = float(data[i][1])
        E = float(data[i][2])
        lat , lon = twd97.towgs84(N,E)
        kml.newpoint(name=name, coords=[(lon , lat)])

    kml.save(txtname[:-4]+".kml")

    
def rename_photo(txtname):
    test = pd.read_csv(txtname,header=None)
    os.chdir('點之記')
    pts_id = test[0].values
    img_name_all = os.listdir(".")
    img_list = [s for s in img_name_all if ".jpg" in s]
    for i,pt in enumerate(pts_id,1):
        if len(pt.split('-'))==1:
            zone = 'Control Points'
            p_id = pt
            dir_name = zone
            zone = 'C'
            
        else:
            [zone, p_id] = pt.split('-')
            dir_name = zone
        
        try:
            os.mkdir(zone)
        except:
            pass
        
        name1 = dir_name+'/'+zone+'-'+ p_id + '-1.jpg'
        os.rename(img_list[i*3-3],name1)
        name2 = dir_name+'/'+zone+'-'+ p_id + '-2.jpg'
        os.rename(img_list[i*3-2],name2)  
        name3 = dir_name+'/'+zone+'-'+ p_id + '-3.jpg'
        os.rename(img_list[i*3-1],name3)
        
def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
    except getopt.GetoptError:
        print('Kao.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Kao.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
         
    
    print('Input file is ', inputfile)
    
    txtname = inputfile
    twd97tokml(txtname)
    rename_photo(txtname)

 
if __name__ == "__main__":
    main(sys.argv[1:])