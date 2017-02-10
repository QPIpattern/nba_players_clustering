library(data.table) 
library(scatterD3) 
library(d3heatmap)
library(ggplot2) 
library(ggrepel) 
library(htmlwidgets)

setwd('/home/kris/projects/basketball')

similarity<- function(year){
    file_path=paste('nba_norm_',year,'.csv',sep='')
    print(file_path)
    dt <- fread(file_path, header=TRUE) # an error arise if read_csv is useddt
    dt=dt[team!='total']
    
#    cl <- kmeans(dt[, list(x, y)], centers=7) 
#    positions <- c('Shooting Guard', 'Dynamic C/PF', 'Slow C/PF', 'Dynamic SF/PF', 'Slow SF/PF', 'Point Guard', 'Stretch C/PF') 
#    dt=dt[, 'cluster' := cl$cluster]
#    dt[, 'position' := positions[dt$cluster]]
    
    
    tooltips <- paste("<strong>", dt$player,"</strong><br /><strong>", dt$team, "</strong><br />") 
    p <- scatterD3(x = dt$x, y = dt$y, lab = dt$player, col_var=dt$team, symbol_var=dt$cluters, point_opacity = 0.7, tooltip_text = tooltips, col_lab = "Team", symbol_lab = "Cluster", width=1000, height=1000) 
    saveWidget(p, paste('nba_player_similarity',year,'.html'))
    print(paste(year,"_saved"))
}

#years=c('2013','2014','2015')
year='2015'
for(year in years){
  print(year)
  similarity(year)
}