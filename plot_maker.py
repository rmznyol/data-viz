import geopandas as gpd

import plotly.express as px
import shapely.geometry

from shapely.affinity import affine_transform as T
from shapely.affinity import rotate as R
from data_processor import dataprocessor

# some geometry for an arrow
a = shapely.wkt.loads(
    "POLYGON ((-0.6227064947841563 1.890841205238906, -0.3426264166591566 2.156169330238906, -0.07960493228415656 2.129731830238906, 1.952059130215843 0.022985736488906, -0.2085619635341561 -2.182924419761094, -0.6397611822841562 -1.872877544761094, -0.6636088385341563 -1.606053326011095, 0.5862935052158434 -0.400158794761094, -2.312440869784157 -0.3993228572610942, -2.526870557284156 -0.1848931697610945, -2.517313916659156 0.2315384708639062, -2.312440869784157 0.3990052677389059, 0.5862935052158434 0.399841205238906, -0.6363314947841564 1.565763080238906, -0.6227064947841563 1.890841205238906))"
)

gdf = (
    gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    .set_crs("EPSG:4326")
)


class PlotMaker():
    def __init__(self, data):

        self.df_wind = data
        self.geojson = gpd.GeoSeries(
            self.df_wind.loc[:, ["lat", "lon", "d", "s"]].apply(
                lambda r: R(
                    T(a, [r["s"], 0, 0, r["s"], r["lon"], r["lat"]]),
                    r["d"],
                    origin=(r["lon"], r["lat"]),
                    use_radians=True,
                ),
                axis=1,
            )
        ).__geo_interface__

    def plot_maker(self):
        """
        needed data_format is as follows
       lat         lon         d         s  temperature
0   45.523449 -122.676208  3.985168  0.262500    61.879625
1   37.774929 -122.419418  1.941679  0.237500    75.072500
2   47.606209 -122.332069  1.705332  0.158333    58.413125
3   34.052231 -118.243683  1.106102  0.054167    78.815375
4   32.715328 -117.157257  2.490730  0.108333    76.781750
5   36.174969 -115.137222  2.756166  0.125000    81.845375
6   33.448380 -112.074043  2.231113  0.125000    85.760750
        """
        t = (
            px.scatter_mapbox(self.df_wind, lat="lat", lon="lon")
            .data
        )

        # wind direction and strength
        fig = px.choropleth_mapbox(
            self.df_wind,
            geojson=self.geojson,
            center={"lat": 37.0902, "lon": -95.7129},
            locations=self.df_wind.index,
            color="temperature",
            range_color=[0, 100],
            color_continuous_scale='icefire',
        ).add_traces(t).update_layout(mapbox={"style": "carto-darkmatter", "zoom": 3},
                                      margin={"l": 0, "r": 0, "t": 0, "b": 0})

        return fig


if __name__ == '__main__':
    from datetime import date

    PlotMaker(dataprocessor.get_organized_wind_data_in_time(date(2014, 9, 5), 'not hourly')).plot_maker().show()
