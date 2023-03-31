import math
import geopandas as gpd
import pandas as pd
import plotly.express as px
import shapely.geometry
import numpy as np
from shapely.affinity import affine_transform as T
from shapely.affinity import rotate as R
import data_processor

# some geometry for an arrow
a = shapely.wkt.loads(
    "POLYGON ((-0.6227064947841563 1.890841205238906, -0.3426264166591566 2.156169330238906, -0.07960493228415656 2.129731830238906, 1.952059130215843 0.022985736488906, -0.2085619635341561 -2.182924419761094, -0.6397611822841562 -1.872877544761094, -0.6636088385341563 -1.606053326011095, 0.5862935052158434 -0.400158794761094, -2.312440869784157 -0.3993228572610942, -2.526870557284156 -0.1848931697610945, -2.517313916659156 0.2315384708639062, -2.312440869784157 0.3990052677389059, 0.5862935052158434 0.399841205238906, -0.6363314947841564 1.565763080238906, -0.6227064947841563 1.890841205238906))"
)

gdf = (
    gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    .set_crs("EPSG:4326")
)

class PlotMaker():
    def __init__(self, date, data):
        """
        data_format is as follows
            lat	    lon	        d	        s
    0	45.523449	-122.676208	1.396263	0.3
    1	37.774929	-122.419418	0.000000	0.2
    2	47.606209	-122.332069	5.585054	0.5
    3	34.052231	-118.243683	0.000000	0.2
    4	32.715328	-117.157257	5.759587	0.5
        """
        self.date = date   
        self.df_wind = pd.DataFrame(
        {"lat": data['locations']['Latitude'].values,
         "lon": data['locations']['Longitude'].values,
         "d": data['wind_direction'].loc[data['wind_direction']['datetime'] == self.date, 'Portland':'Boston'].values[0]*(np.pi/180),
         "s": data['wind_speed'].loc[data['wind_speed']['datetime'] == self.date, 'Portland':'Boston'].values[0] / 10,
         'temperature': data['temp_in_F'].loc[data['temp_in_F']['datetime'] == self.date, 'Portland':'Boston'].values[0]
         }
        )


    def plot_maker(self):

        t = (
            px.scatter_mapbox(self.df_wind, lat="lat", lon="lon")
            .data
        )

        # wind direction and strength
        fig = px.choropleth_mapbox(
        self.df_wind,
        geojson=gpd.GeoSeries(
            self.df_wind.loc[:, ["lat", "lon", "d", "s"]].apply(
                lambda r: R(
                    T(a, [r["s"], 0, 0, r["s"], r["lon"], r["lat"]]),
                    r["d"],
                    origin=(r["lon"], r["lat"]),
                    use_radians=True,
                ),
                axis=1,
            )
        ).__geo_interface__,
        center = {"lat": 37.0902, "lon": -95.7129},
        locations=self.df_wind.index,
        color="temperature",
        range_color = [0,100],
        color_continuous_scale= 'icefire',
        ).add_traces(t).update_layout(mapbox={"style": "carto-darkmatter", "zoom": 3},
                                       margin={"l":0,"r":0,"t":0,"b":0})
        
        return fig

if __name__ == '__main__':
    data = data_processor.DataProcessor().get_data()
    PlotMaker('2014-04-01 00:00:00',data).plot_maker().show()



