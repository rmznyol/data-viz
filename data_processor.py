import numpy as np
import pandas as pd


class DataProcessor:

    def __init__(self):
        # List the names of the individual files from the WeatherData folder
        self.file_names = ["city_attributes.csv", "temperature.csv", "wind_speed.csv", "weather_description.csv", "wind_direction.csv"]

        # List the names of the data frames to be imported
        self.df_names = ['city data', 'temp', 'ws', 'descr', 'wd']

        # put the (file_name, df_name) in a dictionary
        self.name_dct = {k: v for k, v in zip(self.file_names, self.df_names)}

        # dictionary of df's to be populated
        self.df_dct = {}

        for k in self.name_dct:
            self.df_dct[self.name_dct[k]] = pd.read_csv('https://raw.githubusercontent.com/rmznyol/data-viz/April_13/WeatherData/' + k)

        # extract only the data for US cities: Includes datetime feature!
        self.cities = self.df_dct['city data']
        self.US_cities = (
            self.cities[self.cities.Country == 'United States'].City).values
        self.feature_lst = np.append(self.US_cities, 'datetime')

        for k in self.df_dct:
            if k != 'city data':
                self.df_dct[k] = self.df_dct[k][self.feature_lst]

        # Plot the locations of the US/Canada cities
        self.locations = self.df_dct['city data']
        self.locations = self.locations[(
            self.locations.Country == 'United States')]

        # temperature
        # fills missing data with latest non-missing value
        self.tmp = self.df_dct['temp'].fillna(method='ffill')
        self.tmp = self._convert_time_zone(self.tmp)

        self.temp_in_F = self._convert_temp_to_F(self.tmp)

        self.wind_direction = self.df_dct['wd'].fillna(method='ffill')
        self.wind_direction = self._convert_time_zone(self.wind_direction)

        self.wind_speed = self.df_dct['ws'].fillna(method='ffill')
        self.wind_speed = self._convert_time_zone(self.wind_speed)

        self.weather_description = self.df_dct['descr'].fillna(method='ffill')
        self.weather_description = self._convert_time_zone(self.weather_description)

        self.latitudes = self.locations.Latitude
        self.longitudes = self.locations.Longitude
    
    @staticmethod
    def _convert_time_zone(df, initial_timezone='Israel', final_timezone='US/Eastern'):
        """
        converting timezone in dataframes
        :param df: df with datetime column in string format
        :param initial_timezone: initial timezone of the column
        :param final_timezone: timezone to be converted
        :return df: returns new df with desired timezone
        """
        df['datetime'] = pd.to_datetime(df['datetime']).dt.tz_localize(tz=initial_timezone, ambiguous='NaT', nonexistent='NaT')
        #df['datetime'].dropna(inplace=True)
        df['datetime'] = df['datetime'].dt.tz_convert(final_timezone).dt.tz_localize(None)
        return df

    # Converts Temperature from Kelvin to Farenheit
    def _convert_temp_to_F(self, df):
        datetime = df['datetime'].copy()
        df = 9 / 5 * (df.loc[:, self.US_cities].copy() - 273) + 32
        df['datetime'] = datetime
        return df
    
    def get_data(self):
        return {'locations': self.locations,
                'temp_in_F': self.temp_in_F,
                'wind_direction': self.wind_direction,
                'wind_speed': self.wind_speed,
                'weather_description': self.weather_description
                }

    @staticmethod
    def _date_data_picker(df, datetime, datatype, city_list, not_description=True):
        if datatype == 'hourly':
            return df.loc[df['datetime'] == datetime, city_list].values[0]
        else:
            df_of_the_day = df.loc[df['datetime'].dt.date ==
                                   datetime, city_list]
            if not_description:
                return df_of_the_day.mean(axis='index').values
            else:
                return df_of_the_day.mode(axis='index').iloc[0].values

    def get_organized_wind_data_in_time(self, date, datatype):

        df_wind = pd.DataFrame(
            {"lat": self.latitudes.values,
             "lon": self.longitudes.values,
             "d": self._date_data_picker(self.wind_direction, date, datatype, self.US_cities) * (np.pi / 180),
             "s": self._date_data_picker(self.wind_speed, date, datatype, self.US_cities) / 10,
             'temperature': self._date_data_picker(self.temp_in_F, date, datatype, self.US_cities)
             }
        )
        return df_wind

    def get_hover_data_in_time(self, lat, lon, datetime, datatype):
        city = self.locations[(self.latitudes == lat) | (
            self.longitudes == lon)].City.values[0]
        city_temp = self._date_data_picker(
            self.temp_in_F, datetime, datatype, [city])[0]
        city_wind_speed = self._date_data_picker(
            self.wind_speed, datetime, datatype, [city])[0]
        city_desc = self._date_data_picker(
            self.weather_description, datetime, datatype, [city], not_description=False)[0]
        return city, city_temp, city_desc, city_wind_speed


dataprocessor = DataProcessor()

if __name__ == '__main__':
    # for data in DataProcessor().get_data().values():
    #     print(data)
    from datetime import date

    # t = DataProcessor().get_data()['wind_speed'].iloc[3].datetime
    # print(t, type(t))
    # print(type(DataProcessor().get_data()['wind_direction'].datetime.iloc[0]))
    a_date = dataprocessor.wind_direction.datetime.iloc[50]

    # data = DataProcessor().get_data()
    # data_attribute = 'wind_direction'
    # print(data[data_attribute].loc[data[data_attribute]['datetime'].dt.date == a_date, 'Portland':])
    # data_of_the_day = data[data_attribute].loc[data[data_attribute]['datetime'].dt.date == a_date, 'Portland':'Boston']
    # print(data_of_the_day.mean(axis='index').values)
    # print(data[data_attribute].loc[data[data_attribute]['datetime'] == DataProcessor().get_data()['wind_direction'].datetime.iloc[50], 'Portland':].values)
    #
    # print(dataprocessor.get_organized_wind_data_in_time(a_date, 'not hourly'))
    # print(dataprocessor.get_hover_data_in_time(45.523449, -122.676208, a_date.date(), 'not hourly'))
    # test = dataprocessor.weather_description
    # print(test.loc[test['datetime'].dt.date == a_date.date(), :])
    # print(dataprocessor.get_hover_data_in_time(45.523449, -122.676208, date(2014, 9, 5), 'not hourly'))
    print(dataprocessor.get_organized_wind_data_in_time(
        date(2015, 8, 25), 'daily average'))
    # print(dataprocessor.get_organized_wind_data_in_time(a_date, 'hourly'))
