import os
import pandas as pd
import geopandas as gpd
from datetime import datetime, date, timedelta
from data_pipeline._1_elt.elt import elt_mongodb

def save_backup(tbl, dir, type=None):
	curr_dir = os.path.abspath(os.path.dirname(__file__))
	cache_dir = curr_dir + dir
	backup_loc = cache_dir +'/'+f'{type}'+datetime.now().strftime('%Y%m%d')+'.csv'

	if not os.path.exists(cache_dir):
		os.mkdir(cache_dir)
		tbl.to_csv(backup_loc)
	elif len(os.listdir(cache_dir)) < 1:
	    tbl.to_csv(backup_loc)
	else:
		last_backup = sorted(os.listdir(cache_dir))[-1]
		last_backup_dt = datetime.strptime(last_backup[7:-4], '%Y%m%d')
		print(last_backup_dt)
		if last_backup_dt + timedelta(days = 7) < datetime.now():
			tbl.to_csv(backup_loc)
	return True

def wrangle(us_deaths_tbl, cols_to_select, id_fields):
	us_deaths_df = pd.DataFrame(us_deaths_tbl)

	date_fields = [col for col in cols_to_select if col.endswith('/20')]

	us_deaths_df2 = pd.melt(us_deaths_df,
	                        id_vars = id_fields,
	                        value_vars = date_fields,
	                        var_name = 'date',
	                        value_name = 'deaths')

	## Convert new date column to standard format 
	us_deaths_df2['date'] = pd.to_datetime(us_deaths_df2['date'], format= '%m/%d/%y')

	us_deaths_df2.rename(columns= {'Combined_Key': 'county', 'Province_State': 'state'}, inplace=True)

	us_deaths_df2 = us_deaths_df2[['state', 'date', 'deaths']]

	us_deaths_df2 = us_deaths_df2[us_deaths_df2.state != '']

	us_deaths_df2['state'] = us_deaths_df2['state'].str.strip()

	return us_deaths_df2


def covid_metrics(us_deaths_df2):

	metrics_dir = (os.path.abspath(os.path.dirname(__file__)))
	shape_file = metrics_dir +'/data/USA_States/USA_States_Generalized.shp'

	states_geo = gpd.read_file(shape_file)

	states_geo = states_geo[['STATE_NAME', 'geometry']]

	states_geo.rename(columns= {'STATE_NAME': 'state'}, inplace=True)

	## Strip leading spaces from the key column
	states_geo['state'] = states_geo['state'].str.strip()

	states_geo = states_geo.sort_values('state').reset_index(drop=True)

	## Join the covid19 data with the shapefile

	joined_df = us_deaths_df2.join(states_geo.set_index('state'), how='right', on='state', lsuffix='_caller', rsuffix='_other')

	## Group by state
	joined_sum = joined_df.groupby(['state', 'date']).sum()

	joined_sum.reset_index(inplace=True)

	## Join the geometry data back onto the joined table
	joined_sum = joined_sum.join(states_geo.set_index('state'), how= 'right', on='state')

	## Convert date field to unix time in nanoseconds
	joined_sum['date_sec'] = pd.to_datetime(joined_sum['date']).astype(int) / 10**9

	joined_sum['date_sec'] = joined_sum['date_sec'].astype(int).astype(str)

	## Filter out records before first covid death (Feburary 29th)
	joined_sum = joined_sum[joined_sum.date >= '2020-02-29']

	return joined_sum, states_geo

