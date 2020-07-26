import os
from datetime import datetime, date, timedelta
from data_pipeline._1_elt.elt import elt_mongodb
from data_pipeline._2_metrics.metrics_pandas import covid_metrics
from data_pipeline._2_metrics.metrics_pandas import wrangle
from data_pipeline._2_metrics.metrics_pandas import save_backup
from data_pipeline._3_publish.maps import generate_map

## Load required files ##
tbl1, cols_to_select, id_fields = elt_mongodb()

# transform loaded data
# save to backup folder if backup data is over a week old

tbl2 = wrangle(tbl1, cols_to_select, id_fields)

try:
	save_backup(tbl2, '/data/cache', type='metrics')
except Exception as e:
	print('Backup file not saved')
	print(e)


## generate final aggregation table, backup, and publish to dashboard

tbl3, tbl4 = covid_metrics(tbl2)

try:
	save_backup(tbl3, '/data/cache_2', type='publish')
except Exception as e:
	print('Backup file not saved')
	print(e)

## create choropleth map 
try:
	generate_map(tbl3, tbl4)
except Exception as e:
	print('Map not saved properly.')
	print(e)







