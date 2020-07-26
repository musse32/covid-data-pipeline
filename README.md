## DEATHS FROM COVID-19 CHOROPLETH MAP

MongoDB is hosting a service with a frequently updated copy of the Johns Hopkins University COVID-19 data in MongoDB Atlas, their database in the cloud. This data is free for anyone to query using the MongoDB Query language and/or SQL.

## COVID PROJECT

This program queries the MongoDB cloud database using pymongo for the latest COVID-19 data published by Johns Hopkins University. The query extracts all records of deaths from every county in the US starting from the first recorded death until the latest day the data was updated. The database is updated daily. 

## Installation 

Clone or download this repository. Extract the contents and navigate to the project folder 'covid_project'. It is recommended to open this project in a virtual environment such as Conda. Once in the project folder run: 

```pip install -r requirements.txt```

*Please note* Windows users you may need additional steps to install the packages GeoPandas and Folium. Once all the dependencies are installed run the program:

```python main.py```


## Usage

An HMTL file will be created at the project directory level. Open the file to view in your default browser. The sliding bar on the top of the map scrolls from left to right over the timeline of the dataset. The map shows states and their running total of deaths from COVID-19 over the given time span. 

### Example running on my personal website https://hamza-musse-portfolio.herokuapp.com/projects
![](https://github.com/musse32/covid-data-pipeline/blob/master/example_map.PNG?raw=true)


## Project Tree

├───covid_project
│   └───data_pipeline
│       ├───_1_elt
│       │   └───__pycache__
│       ├───_2_metrics
│       │   ├───data
│       │   │   ├───cache
│       │   │   ├───cache_2
│       │   │   └───USA_States
│       │   └───__pycache__
│       ├───_3_publish
│       │   └───__pycache__
│       └───__pycache__


