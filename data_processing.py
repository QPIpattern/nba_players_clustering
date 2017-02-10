#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 15:16:50 2016

@author: BOB
"""
import pandas as pd
from time import time
import numpy as np
import os
import get_data
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
from sklearn import (manifold,  decomposition, lda, random_projection)
from sklearn.cluster import KMeans

def dim_reduction(year='2014',method='TSNE',filter_ratio=0.5):
      year=year
#      method_name=''.join(['manifold.',method])
      raw_file=''.join(["nba_raw_",year,".csv"])
      projected_file=''.join(["nba_projected_",year,".csv"])
      
      if(os.path.isfile(raw_file)):
            nba_data=pd.read_csv(raw_file)
            print('data loaded')

      else:
            print('file does not exist')
            nba_data=get_data.data_fetch(year)
            print('data downloaded')
            nba_data=pd.read_csv(raw_file)
            nba_data=pd.DataFrame(nba_data)
      
      nba_data=nba_data.set_index(['PLAYER_ID','TEAM_ABBREVIATION',nba_data.columns[2]])

#      print(nba_data.columns)
      # data filter. Only active players are considered
      games_min=nba_data.defense_address_GP.mean()*filter_ratio
      avg_min=nba_data.defense_address_MIN.mean()*filter_ratio
      nba_data= nba_data[nba_data.defense_address_GP >= games_min]
      nba_data = nba_data[nba_data.defense_address_MIN >= avg_min]
      
      player_names=[x[2] for x in nba_data.index]
      team_names=[x[1] for x in nba_data.index]
# NaN are replaced by mean-value of the feature(columns)
# each feature is normalized
      nba_data=nba_data.convert_objects(convert_numeric=True)
      nba_data=nba_data.fillna(nba_data.mean(skipna=True))
      scaler=StandardScaler()
      nba_data=scaler.fit_transform(nba_data)
      nba_data=pd.DataFrame(nba_data)
      

# correlation between players      
      corr = nba_data.T.corr()
      X = corr.as_matrix()
      
      X_reduced = TruncatedSVD(n_components=10, random_state=0).fit_transform(X)
      
      if(method=='TSNE'):
            tsne = manifold.TSNE(n_components=2, perplexity=40, verbose=2)
            X_tsne = tsne.fit_transform(X_reduced)
#      
      kmeans=clustering(data=X_tsne,year=year,k_clusters=7)
      df_projected = pd.DataFrame(X_tsne)
      df_projected['player'] = player_names
      df_projected['team'] = team_names
#      print(df_projected.shape,np.size(kmeans.labels_))
      df_projected['cluster']=kmeans.labels_[0:df_projected.shape[0]]
      df_projected.columns = ['x', 'y', 'player', 'team','cluters']
      df_projected.to_csv(projected_file, index=False)
                  
def clustering(data,year,k_clusters=7):
      center_file=''.join(["nba_centers_",year,".csv"])
      kmeans=KMeans(k_clusters).fit(data)
      centers=kmeans.cluster_centers_
      np.savetxt(center_file,centers)
      return(kmeans)

if __name__=="__main__":
      dim_reduction('2013')
      dim_reduction('2014')
      dim_reduction('2015') 
#      dim_reduction('2016') 
      