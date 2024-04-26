# load up the libraries
import panel as pn
import pandas as pd
import altair as alt
# from vega_datasets import data
import json
import numpy as np
import streamlit as st
import geopandas as gpd

pisa_df = pd.read_csv('PISA_data.csv')
country_codes = pd.read_csv('country_codes.csv')
pisa_df = pisa_df.merge(country_codes, left_on='country', right_on='code')
pisa_total = pisa_df[pisa_df['sex'] == 'TOT']
pisa_total = pisa_total.drop(columns=['country','index_code'])
pisa_total['name'] = pisa_total['country_name']
pisa_total['time'] = pisa_total['time'].astype(int)

url = "https://raw.githubusercontent.com/dallascard/si649_public/main/altair_hw4/small-airports.json"
# europe= 'https://github.com/amcharts/amcharts4/blob/master/dist/geodata/es2015/json/region/world/europeUltra.json'
from vega_datasets import data
countries = alt.topo_feature(data.world_110m.url, "countries")
# countries = alt.topo_feature(europe, "geometry")
# https://en.wikipedia.org/wiki/ISO_3166-1_numeric
country_codes_all = pd.read_csv(
    "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"
)
# world = alt.topo_feature(url, feature='continent')
# base = alt.Chart(countries).mark_geoshape(
#     fill = 'lightgray',
#     stroke = 'white'
# ).project("naturalEarth1").interactive()
st.write(data.world_110m.url)



base = alt.Chart(countries).mark_geoshape(
    fill = 'lightgray',
    stroke = 'white'
).project("mercator").interactive()

#https://stackoverflow.com/questions/66375071/geojson-file-not-plotting-correctly-in-altair
custom_world = gpd.read_file('europe.geo.json')
# change custom world geometry column to wrt


#simple polygon data, raw from github
# custom jsons https://geojson-maps.kyd.au
url_geojson = 'https://github.com/bkarduck/custom-jsons/blob/main/asia.geo.json'


# custom_world = alt.topo_feature('https://github.com/bkarduck/custom-jsons/blob/main/asia.geo.json', 'geometry')
# data_url_geojson = alt.Data(url=url_geojson, format=alt.DataFormat(property="features"))


url_geojson = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_0_countries.geojson"
data_url_geojson = alt.Data(url=url_geojson, format=alt.DataFormat(property="features"))

# eu_chart = alt.Chart(data_url_geojson).mark_geoshape().encode(color='properties.name:N').transform_filter(
#         alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Europe', ])
#     ).properties(width=600, height=500).project(
# type='mercator', reflectY=False, scale=200, translate=[50, 550])


# na_chart =alt.Chart(data_url_geojson).mark_geoshape().encode(color='properties.name:N').transform_filter(
#         alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Americas', ])
#     ).transform_filter(alt.FieldOneOfPredicate(field='properties.continent', oneOf=['North America', ])).properties(width=600, height=600)

# sa_chart = alt.Chart(data_url_geojson).mark_geoshape().encode(color='properties.name:N').transform_filter(alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Americas', ])
#     ).transform_filter(alt.FieldOneOfPredicate(field='properties.continent', oneOf=['South America', ])).properties(width=600, height=600).project(
# type='mercator', reflectY=False, scale=300, translate=[500, 100])


# aus_asia_chart = alt.Chart(data_url_geojson).mark_geoshape().encode(color='properties.name:N').transform_filter(alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Asia', 'Oceania', ])).transform_filter(alt.FieldOneOfPredicate(field='properties.region_wb', oneOf=['East Asia & Pacific', ])
#     ).properties(width=600, height=500).project(type='equalEarth',  scale=240, translate=[100, 180], rotate=[-135, -25 ,0])
# #.project(
# #type='equirectangular', reflectY=True,scale=400, translate=[100, 50])

# final_chart = alt.hconcat(
#     alt.vconcat(na_chart, sa_chart),
#     alt.vconcat(eu_chart, aus_asia_chart)

# )
# st.altair_chart(final_chart, use_container_width=True)
# europe = alt.Chart(data_url_geojson).mark_geoshape(color='lightgrey').encode(   
# # tooltip=[alt.Tooltip('name:N', title='Country')]
# ).properties(
#     width=600,
#     height=400
# ).project(
#     type='identity', reflectY=True, scale=400, translate=[100, 550]
# )
# st.altair_chart(europe, use_container_width=True)


#simple polygon data, raw from github
url_geojson = 'https://raw.githubusercontent.com/mattijn/datasets/master/two_polygons.geo.json'

# url_geojson = 'https://github.com/bkarduck/custom-jsons/blob/main/europe.geo.json'
# data_geojson_remote = alt.Data(url=url_geojson, format=alt.DataFormat(property='features',type='json'))

# #chart object for remote data
# ch_remote = alt.Chart(data_geojson_remote).mark_geoshape(
# ).encode(
#     color="properties.name:N"
# ).project(
#     type='identity', reflectY=True
# )
# st.altair_chart(ch_remote, use_container_width=True)


# Define a list of country codes for each region (ISO-3166 Alpha-3 codes)
na_countries = ['USA', 'CAN', 'MEX']  # Example North America countries
sa_countries = ['BRA', 'ARG', 'COL']  # Example South America countries
eu_countries = ['FRA', 'DEU', 'ITA'] # Example Europe countries
aus_asia_countries = ['AUS', 'CHN', 'JPN', 'IND']  # Example Australia and Asia countries

# def create_map(region_countries, title):
#     return alt.Chart(countries).mark_geoshape(
#         fill = 'lightgray',
#         stroke='white'
#     ).transform_lookup(
#         lookup="id",
#         from_=alt.LookupData(data=country_codes_all, key="country-code", fields=["country-code"])).transform_filter(
#         alt.FieldOneOfPredicate(field='country-code', oneOf=region_countries)
#     ).properties(
#         width=300,
#         height=300,
#         title=title
#     ).project('mercator')

# # Create maps for each region
# na_chart = create_map(na_countries, 'North America')
# sa_chart = create_map(sa_countries, 'South America')
# eu_chart = create_map(eu_countries, 'Europe')
# aus_asia_chart = create_map(aus_asia_countries, 'Australia & Asia')

# # Combine charts
# final_chart = alt.hconcat(
#     alt.vconcat(na_chart, sa_chart),
#     alt.vconcat(eu_chart, aus_asia_chart)
# )

# # final_chart.display()
# st.altair_chart(final_chart, use_container_width=True)


year_options=list(pisa_total["time"].unique())
year_options=list(map(lambda x:int(x),year_options))
year_options.sort()

# year_radio=alt.binding_radio(
#     options=year_options
# )
# radio_selector = alt.selection_point(
#     name="year",
#     fields=["time"],
#     bind=year_radio,
#     value=2003
#     )

yearSelector = alt.selection_interval()

selected_events = st.radio('Select Events:', options=year_options)

pisa_filtered = pisa_total[pisa_total['time'] == selected_events]



rating = alt.Chart(countries).mark_geoshape().transform_lookup(
        lookup="id",
        from_=alt.LookupData(data=country_codes_all, key="country-code", fields=["name"]),
    ).transform_lookup(
        lookup="name",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered, key="name", fields=["rating"]),
    ).encode(
        fill=alt.Color(
            "rating:Q",
            scale=alt.Scale(scheme="reds"),
        ), 
        tooltip=[
            alt.Tooltip("name:N", title="Country"),
            alt.Tooltip("rating:Q", title="Rating"),]
            ).interactive()



# .project(
#     type= 'mercator',
#     scale= 350,                          # Magnify
#     center= [20,50],                     # [lon, lat]
#     clipExtent= [[0, 0], [400, 300]],    # [[left, top], [right, bottom]]
# ).properties(
#     title='Europe (Mercator)',
#     width=400, height=300
# )

# europ = alt.topo_feature(data.world_110m.url, 'countries')

# base2= alt.Chart(europ).mark_geoshape(
#     fill='#666666',
#     stroke='white'
# ).project(
#     type= 'mercator',
#     scale= 250,                          # Magnify
#     center= [20,50],                     # [lon, lat]
#     clipExtent= [[0, 0], [400, 300]],    # [[left, top], [right, bottom]]
# ).properties(
#     title='Europe (Mercator)',
#     width=400, height=300
# )

 
chart = (
    (base + rating).properties(width=600, height=600)
    .configure_view(strokeWidth=0).interactive()
    )

st.altair_chart(chart, use_container_width=True)

# selected_events2 = st.radio('Select Events2:', options=year_options)
values = st.slider(
    'Select a year',
   min_value=2003, max_value=2018, value=2003, step=3)

# st.write('year selected:', values)

pisa_filtered2 = pisa_total[pisa_total['time'] == values]
eu_chart = alt.Chart(data_url_geojson,title='Europe').mark_geoshape(stroke='white').transform_filter(
        alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Europe', ])
    ).transform_lookup(
        lookup="properties.iso_a3",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered2, key="code", fields=["rating"]),
    ).encode(
        fill=alt.Color(
            "rating:Q",
            scale=alt.Scale(scheme="reds"),
        ), 
        tooltip=[
            alt.Tooltip("properties.name:N", title="Country"),
            alt.Tooltip("rating:Q", title="Rating"),]
            ).properties(width=400, height=250).project(
type='mercator', reflectY=False, scale=150, translate=[150, 300])

eu_base = alt.Chart(data_url_geojson).mark_geoshape( fill='#666666',
    stroke='white').encode().transform_filter(
        alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Europe', ])
    ).transform_lookup(
        lookup="properties.iso_a3",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered2, key="code", fields=["rating"]),
    ).properties(width=400, height=250).project(
type='mercator', reflectY=False, scale=150, translate=[150, 300])


na_chart =alt.Chart(data_url_geojson, title='North America').mark_geoshape(stroke='white').transform_filter(
        alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Americas', ])
    ).transform_filter(alt.FieldOneOfPredicate(field='properties.continent', oneOf=['North America', ])).transform_lookup(
        lookup="properties.iso_a3",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered2, key="code", fields=["rating"]),
    ).encode(
        fill=alt.Color(
            "rating:Q",
            scale=alt.Scale(scheme="reds"),
        ), 
        tooltip=[
            alt.Tooltip("properties.name:N", title="Country"),
            alt.Tooltip("rating:Q", title="Rating"),]
            ).properties(width=400, height=250)

na_base = alt.Chart(data_url_geojson).mark_geoshape(    fill='#666666',
    stroke='white').encode().transform_filter(alt.FieldOneOfPredicate(field='properties.continent', oneOf=['North America', ])).transform_lookup(
        lookup="properties.iso_a3",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered2, key="code", fields=["rating"])).properties(width=400, height=250)

sa_chart = alt.Chart(data_url_geojson, title='South America').mark_geoshape(stroke='white').transform_filter(alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Americas', ])
    ).transform_filter(alt.FieldOneOfPredicate(field='properties.continent', oneOf=['South America', ])).transform_lookup(
        lookup="properties.iso_a3",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered2, key="code", fields=["rating"]),
    ).encode(
        fill=alt.Color(
            "rating:Q",
            scale=alt.Scale(scheme="reds"),
        ), 
        tooltip=[
            alt.Tooltip("properties.name:N", title="Country"),
            alt.Tooltip("rating:Q", title="Rating"),]
            ).properties(width=400, height=250).project(
type='mercator', reflectY=False, scale=170, translate=[400, 50])


sa_base = alt.Chart(data_url_geojson).mark_geoshape( fill='#666666',
    stroke='white').encode(tooltip=[
            alt.Tooltip("properties.name:N", title="Country"),]).transform_filter(alt.FieldOneOfPredicate(field='properties.continent', oneOf=['South America', ])).transform_lookup(
        lookup="properties.iso_a3",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered2, key="code", fields=["rating"])).properties(width=400, height=250).project(
type='mercator', reflectY=False, scale=170, translate=[400, 50])





aus_asia_chart = alt.Chart(data_url_geojson,title='Australia and East Asia').mark_geoshape(stroke='white').transform_filter(alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Asia', 'Oceania', ])).transform_filter(alt.FieldOneOfPredicate(field='properties.region_wb', oneOf=['East Asia & Pacific', ])
    ).transform_lookup(
        lookup="properties.iso_a3",
        # can change this to other dfs
        from_=alt.LookupData(data=pisa_filtered2, key="code", fields=["rating"]),
    ).encode(
        fill=alt.Color(
            "rating:Q",
            scale=alt.Scale(scheme="reds"),
        ), 
        tooltip=[
            alt.Tooltip("properties.name:N", title="Country"),
            alt.Tooltip("rating:Q", title="Rating"),]
            ).properties(width=400, height=250).project(type='equalEarth',  scale=120, translate=[200, 90], rotate=[-135, -25 ,0])
#rotate=[-135, -25 ,0]
#.properties(width=600, height=500).project(type='equalEarth',  scale=240, translate=[100, 180], rotate=[-135, -25 ,0])
#.properties(width=300, height=270).project(type='equalEarth',  scale=160, translate=[200, 80])
# view=alt.ViewConfig(strokeWidth=1, stroke='red')
aus_asia_base = alt.Chart(data_url_geojson).mark_geoshape(    fill='#666666',
    stroke='white').encode().transform_filter(alt.FieldOneOfPredicate(field='properties.region_un', oneOf=['Asia', 'Oceania', ])).transform_filter(alt.FieldOneOfPredicate(field='properties.region_wb', oneOf=['East Asia & Pacific', ])).properties(width=400, height=250).project(type='equalEarth',  scale=120, translate=[200, 90], rotate=[-135, -25 ,0])

final_chart = alt.hconcat(
    alt.vconcat(na_base + na_chart, sa_base + sa_chart),
    alt.vconcat(eu_base + eu_chart, aus_asia_base+aus_asia_chart)

)
st.altair_chart(final_chart, use_container_width=True)





