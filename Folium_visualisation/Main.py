__author__ = 'Khash'
import folium

map_osm = folium.Map(location=[45.523, -122.675], tiles='OpenStreetMap')
map_osm.create_map(path='osm.html')