
import random
import folium
import geopandas
import shapely


def read_data():
    # import dello shapefile del Comune di Verona
    city = geopandas.read_file('data/comune_verona.shp')
    build = geopandas.read_file('data/edifici_verona.shp')
    return city, build


def show_map(gdf):
    c = gdf.centroid
    mmap = folium.Map(location=[c.geometry.y, c.geometry.x], tiles='OpenStreetMap', zoom_start=12)
    folium.Marker([c.geometry.y, c.geometry.x], popup="<i>Popup di prova</i>", tooltip="Verona").add_to(mmap)
    mmap.save('map.html')  # TODO only for test purpose
    pass


def generate_random_gps(boundaries):
    return None


def mark_area_around_bomb(location, mmap):
    folium.Circle(location=location,
                  radius=1000,
                  popup="<b>Area ad alto rischio</b>",
                  tooltip="ZONA ROSSA",
                  color='red',
                  fill=True,
                  fill_color='#FF8989').add_to(mmap)


if __name__ == '__main__':
    cities, building = read_data()
    show_map(cities)


