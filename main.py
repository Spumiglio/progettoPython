import csv
import random
import folium
import geopandas as gpd
import pyproj

from functools import partial
from shapely.geometry import Point, Polygon
from shapely.ops import transform


def read_data():
    # import dello shapefile del Comune di Verona
    city = gpd.read_file('data/comune_verona.shp')
    build = gpd.read_file('data/edifici_verona.shp')
    return city, build


def show_map(gdf):
    # build_j = gpd.GeoSeries(building['geometry']).simplify(tolerance=0.001)
    # b_j = build_j.to_json()
    # map2 = folium.GeoJson(b_j)
    # map2.add_to(mmap)

    c = gdf.centroid
    mmap = folium.Map(location=[c.geometry.y, c.geometry.x], tiles='OpenStreetMap', zoom_start=12)
    # folium.Marker([c.geometry.y, c.geometry.x], popup="<i>Popup di prova</i>", tooltip="Verona").add_to(mmap)
    # map2.add_to(mmap)
    sim_geo = gpd.GeoSeries(gdf['geometry']).simplify(tolerance=0.0001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'orange'})
    geo_j.add_to(mmap)
    mmap.save('map.html')  # TODO only for test purpose
    return mmap


def generate_random_gps(city):
    square = city.envelope[0]
    geometry = city.geometry[0]
    while True:
        rand_x = random.uniform(square.bounds[0], square.bounds[2])
        rand_y = random.uniform(square.bounds[1], square.bounds[3])
        if geometry.contains(Point(rand_x, rand_y)):
            print("La bomba è stata trovata in posizione (" + str(rand_x) + ", " + str(rand_y) + ")")
            return Point(rand_x, rand_y)


def buffer_around_point(mmap, gdf, point):
    proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=point.y, lon=point.x)),
        proj_wgs84)
    buffer = Point(0, 0).buffer(1000)  # distance in metres
    buffer = Polygon(transform(project, buffer).exterior.coords[:])

    buildings_in_area = gdf[gdf.geometry.within(buffer)]
    buildings_in_area.to_csv("buildings_in_area.csv", index=False)
    mark_area_around_bomb(point, mmap)
    print("Nell'area sono stati trovati " + str(len(buildings_in_area)) + " edifici da evacuare.")
    geo_j = folium.GeoJson(data=buildings_in_area, style_function=lambda x: {'fillColor': 'black', 'color': 'red'})
    geo_j.add_to(mmap)
    mmap.save('map.html')


def mark_area_around_bomb(location, mmap):
    folium.Marker(location=(location.y, location.x),
                  popup="Qui è stato trovato un ordigno!",
                  tooltip='BOMBA',
                  icon=folium.Icon(color='red')).add_to(mmap)
    folium.Circle(location=(location.y, location.x),
                  radius=1000,
                  popup="<b>Area ad alto rischio</b>",
                  tooltip="ZONA ROSSA",
                  color='red',
                  fill=True,
                  fill_color='#FF8989').add_to(mmap)
    mmap.save('map.html')


def save_map(mmap, point):
    mmap.save('map.html')
    mmap.location = [point.y, point.x]
    # map_larger = folium.Map(location=[point.y, point.x], zoom_start=18).add_to(figure)
    mmap.save("area_map.html")


if __name__ == '__main__':
    cities, building = read_data()
    mmap = show_map(cities)
    point = generate_random_gps(cities)
    buffer_around_point(mmap, building, point)

    save_map(mmap, point)


