## Set the range of values for the color sliderimport json
import folium
import branca.colormap as cm
import pandas as pd
import numpy as np
import geopandas as gpd
from data_pipeline._2_metrics.metrics_pandas import covid_metrics

def generate_map(joined_sum, states_geo):

    max_colour = max(joined_sum['deaths'])
    min_colour = min(joined_sum['deaths'])
    cmap = cm.linear.YlOrRd_09.scale(min_colour, max_colour)
    cmap = cmap.to_step(index=[0, 2000, 6000, 10000, 20000, 30000])
    joined_sum['colour'] = joined_sum['deaths'].map(cmap)

    ## Construct the styling dictionary to apply styles to each county for each data point

    state_list = joined_sum['state'].unique().tolist()
    state_ndx = range(len(state_list))

    style_dict = {}
    for i in state_ndx:
        state = state_list[i]
        result = joined_sum[joined_sum['state'] == state]
        inner_dict = {}
        for _, r in result.iterrows():
            inner_dict[r['date_sec']] = {'color': r['colour'], 'opacity': 0.7}
        style_dict[str(i)] = inner_dict

    ## Then create a geo-dataframe containing the features for each county.

    states_geom = states_geo[['geometry']]

    states_gdf = gpd.GeoDataFrame(states_geom)
    states_gdf = states_gdf.reset_index()

    ## Now create the final Folium map objects. 

    from folium.plugins import TimeSliderChoropleth

    slider_map = folium.Map(location=[37, -96],
                                    min_zoom= 4, 
                                    max_bounds=True,
                                    max_zoom=18,
                                    zoom_start=4,
                                    height='75%',
                                    tiles='cartodbpositron')

    slider = TimeSliderChoropleth(
        data=states_gdf.to_json(),
        styledict=style_dict,
        overlay=True
    ).add_to(slider_map)

    slider = cmap.add_to(slider_map)

    cmap.caption = "Number of confirmed COVID19 Deaths"
    slider_map.save(outfile='usa_choropleth_chart.html')
    return True
