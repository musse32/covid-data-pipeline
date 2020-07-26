import pymongo


def elt_mongodb():
	"""Connects to John Hopkins MongoDB database and extracts COVID time series data."""
	EARTH_RADIUS = 6371.0
	MDB_URL = "mongodb+srv://readonly:readonly@covid-19.hip2i.mongodb.net/covid19"
	try:
		print('Connecting to database..')
		client = pymongo.MongoClient(MDB_URL)
	except Exception as e:
		print('Could not connect to database.')
		print(e)

	covid19jhu_db = client.covid19jhu

	## Query MongoDB US Deaths table. Only select required columns, order by state name. 
	us_deaths_tbl = covid19jhu_db.time_series_covid19_deaths_US

	us_deaths_tbl_cols = list(us_deaths_tbl.find_one().keys())

	cols_to_select = {}

	id_fields = ["Combined_Key","Province_State"]

	for col in us_deaths_tbl_cols:
	    if col.endswith("/20"):
	        cols_to_select[col] = 1
	    if col in id_fields:
	        cols_to_select[col] = 1

	us_deaths_tbl = list(us_deaths_tbl.find(
	    {}, 
	    cols_to_select
	    ).sort('Province_State', pymongo.ASCENDING))
	print('Query complete.')

	return us_deaths_tbl, cols_to_select, id_fields
