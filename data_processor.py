import numpy as np
import pandas as pd

class DataProcessor:

    def __init__(self):
        #List the names of the individual files from the WeatherData folder
        self.file_names = ["city_attributes.csv","temperature.csv","wind_speed.csv","humidity.csv"
                ,"weather_description.csv","pressure.csv","wind_direction.csv"]

        #List the names of the data frames to be imported
        self.df_names = ['city data','temp','ws','humid','descr', 'press','wd']

        #put the (file_name, df_name) in a dictionary
        self.name_dct = {k:v for k,v in zip(self.file_names, self.df_names)}

        #dictionary of df's to be populated
        self.df_dct = {}

        for k in self.name_dct:
            self.df_dct[self.name_dct[k]] = pd.read_csv("WeatherData/" + k)
            
        # extract only the data for US cities: Includes datetime feature!
        self.cities =self.df_dct['city data']
        self.US_cities = (self.cities[self.cities.Country == 'United States'].City).values
        self.feature_lst = np.append(self.US_cities, 'datetime')

        for k in self.df_dct:
            if k != 'city data':
                self.df_dct[k] = self.df_dct[k][self.feature_lst]
        
        # Plot the locations of the US/Canada cities
        self.locations = self.df_dct['city data']
        self.locations = self.locations[(self.locations.Country == 'United States')]


        #temperature 
        self.tmp = self.df_dct['temp']
        self.tmp = self.tmp.fillna(method = 'ffill') #fills missing data with latest non-missing value
        self.tmp.loc[:,'datetime'] = pd.to_datetime(self.tmp.loc[:,'datetime'])

        self.wind_direction = self.df_dct['wd']
        self.wind_direction = self.wind_direction.fillna(method = 'ffill')
        self.wind_direction.loc[:,'datetime'] = pd.to_datetime(self.wind_direction.loc[:,'datetime'])

        self.wind_speed = self.df_dct['ws']
        self.wind_speed = self.wind_speed.fillna(method = 'ffill')
        self.wind_speed.loc[:,'datetime'] = pd.to_datetime(self.wind_speed.loc[:,'datetime'])

        self.weather_description = self.df_dct['descr']
        self.weather_description = self.weather_description.fillna(method='ffill')
        self.weather_description.loc[:, 'datetime'] = pd.to_datetime(self.weather_description.loc[:, 'datetime'])

    # Converts Temperature from Kelvin to Farenheit
    def _convert_temp_to_F(self,df):
        datetime = df['datetime'].copy()
        df = 9/5 * (df.loc[:, self.US_cities].copy() - 273) + 32
        df['datetime'] = datetime
        return df

    def get_data(self):
        return {'locations': self.locations,
                'temp_in_F': self._convert_temp_to_F(self.tmp),
                'wind_direction': self.wind_direction,
                'wind_speed': self.wind_speed,
                'weather_description': self.weather_description
        }


if __name__ == '__main__':
    # for data in DataProcessor().get_data().values():
    #     print(data)
    from datetime import date
    from datetime import timedelta
    t = DataProcessor().get_data()['wind_speed'].iloc[3].datetime
    print(t, type(t))



