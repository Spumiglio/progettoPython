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


def create_map(gdf):
    c = gdf.centroid
    mmap = folium.Map(location=[c.geometry.y, c.geometry.x], tiles='OpenStreetMap', zoom_start=12)
    sim_geo = gpd.GeoSeries(gdf['geometry']).simplify(tolerance=0.0001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'orange'})
    geo_j.add_to(mmap)
    return mmap


def generate_random_point(city):
    square = city.envelope[0]
    geometry = city.geometry[0]

    while True:
        # calcolo random di latitudine e longitudini
        rand_x = random.uniform(square.bounds[0], square.bounds[2])
        rand_y = random.uniform(square.bounds[1], square.bounds[3])
        if geometry.contains(Point(rand_x, rand_y)):
            print("Una bomba è stata trovata in posizione (" + str(rand_x) + ", " + str(rand_y) + ")")
            return Point(rand_x, rand_y)


def buffer_around_point(mmap, gdf, point):
    proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=point.y, lon=point.x)),
        proj_wgs84)
    buffer = Point(0, 0).buffer(1000)  # distanza in metri
    buffer = Polygon(transform(project, buffer).exterior.coords[:])
    print("Verranno evacuati gli edifici in un area di raggio di 1 km")

    buildings_in_area = gdf[gdf.geometry.within(buffer)]
    buildings_in_area.to_csv("buildings_in_area.csv", index=False)
    mark_area_around_bomb(point, mmap) # segno l'area nella mappa

    print("Nell'area sono stati trovati " + str(len(buildings_in_area)) + " edifici da evacuare.")

    geo_j = folium.GeoJson(data=buildings_in_area, style_function=lambda x: {'fillColor': 'black', 'color': 'red'})
    geo_j.add_to(mmap)


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


def save_map(mmap, point):
    mmap.save('map.html')
    mmap.location = [point.y, point.x]
    mmap.options['zoom'] = 15
    mmap.options['zoom_control'] = False
    mmap.options['scrollWheelZoom'] = False
    mmap.options['dragging'] = False
    mmap.save("area_map.html")


if __name__ == '__main__':
    verona, building = read_data()
    verona_map = create_map(verona)
    bomb_point = generate_random_point(verona)
    buffer_around_point(verona_map, building, bomb_point)

    save_map(verona_map, bomb_point)


