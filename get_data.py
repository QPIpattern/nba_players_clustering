#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 13:09:15 2016

@author: BOB
"""
import urllib
import json
import pandas as pd
from time import time
import numpy as np
import os


url="http://stats.nba.com/js/data/sportvu"

# dict of urls by year
def url_list(year='2014'):
     addresslist = {
    "pullup_address": os.path.join(url,year,"pullUpShootData.json"),
    "drives_address": os.path.join(url,year,"drivesData.json"),
    "defense_address":os.path.join(url,year,"defenseData.json"),
    "passing_address":os.path.join(url,year,"passingData.json"),
    "touches_address": os.path.join(url,year,"touchesData.json"),
    "speed_address": os.path.join(url,year,"speedData.json"),
    "rebounding_address": os.path.join(url,year,"reboundingData.json"),
    "catchshoot_address": os.path.join(url,year,"catchShootData.json"),
    "shooting_address": os.path.join(url,year,"shootingData.json")
    }
     return(addresslist)
    
def data_fetch(year='2014'):
      urls=url_list(year)
      sportsvu_data = {}
      for key, url in urls.items():
          print(key,url)
          response = urllib.request.urlopen(url)
          raw = response.read().decode('utf-8')
          data = json.loads(raw)
          headers = data['resultSets'][0]['headers']
          table = data['resultSets'][0]['rowSet']
          df = pd.DataFrame(table)
#          print(df.size)
          df.columns = headers
          df = df.set_index(['PLAYER_ID', 'TEAM_ABBREVIATION'])
          # to avoid same colnames in different keys
          df.columns = ['{}_{}'.format(key, x) for x in df.columns] 
          sportsvu_data[key] = df
#-------------------------------------------------------------

          #turn sportsvu in pandas dataframe
      sportvu = None
      for suffix, input_df in sportsvu_data.items():
            print(suffix)
            if sportvu is None:
                  sportvu = input_df
            else:
                  sportvu = pd.merge(sportvu,
                           input_df,
                           how='inner',
                           left_index=True,
                           right_index=True)
       
            print("total_size:", sportvu.size)
            
      # remove reducant columns
      sportvu = sportvu.T.drop_duplicates().T.reset_index()
      # the third index should be the first column other than two existing indexes, otherwise it reports error.
      sportvu = sportvu.set_index(['PLAYER_ID','TEAM_ABBREVIATION',sportvu.columns[2]]) 
      sportvu=sportvu.convert_objects(convert_numeric=True)
      sportvu = sportvu._get_numeric_data()
      sportvu= sportvu.astype(float)
      sportvu.to_csv(''.join(["nba_raw_",year,".csv"]),index=True)
      
  
if __name__=="__main__":
      data_fetch()  

  


      

    


