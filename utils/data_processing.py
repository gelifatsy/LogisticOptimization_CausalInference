import pandas as pd
from datetime import datetime
import holidays
from geopy import distance
from datetime import date, timedelta

class DataProcessor:

    def __init__(self) -> None:
        self.ng_holidays = holidays.country_holidays('NG')

    def isWeekend(self, df_date_str):
        # 2024-06-12 07:28:04
        datetime_object = datetime.strptime(df_date_str, '%Y-%m-%d %H:%M:%S')
        # print(datetime_object.weekday())
        if datetime_object.weekday() < 5:
            return 0
        else:  # 5 Sat, 6 Sun
            return 1

    def isHoliday(self, df_date_str):
        try:
            dt = datetime.strptime(df_date_str, '%Y-%m-%d %H:%M:%S').date()
            if dt in self.ng_holidays:
                return 1
            else: return 0
        except Exception as e:
            return 0
    def print_holidays_in_year(self, year):
        holiday_count = 0
        day = date(year, 1, 1)
        for n in range(365):
            if day in self.ng_holidays:
                print(f"Date: {day.strftime('%Y-%m-%d')}, Holiday: {self.ng_holidays.get(day)}")
                holiday_count += 1
            day += timedelta(days=1)
        print(f"Total number of holidays in {year}: {holiday_count}")


    def calculate_distances(self, starting_coordinates, ending_coordinates):
        calculated_distances = []
        for i in range(len(starting_coordinates)):
            val = str(starting_coordinates[i]).split(',')
            starting_tuple = (val[0], val[1])
            val_end = str(ending_coordinates[i]).split(',')
            ending_tuple = (val_end[0], val_end[1])
            if val_end[0] == "0.0" or val_end[1] == "0.0":
                calculated_distances.append(-1)
            elif val_end[0] == "0.5" or val_end[1] == "0.5":
                calculated_distances.append(-2)
            else:
                calculated_distances.append(distance.distance(starting_tuple, ending_tuple).km)
        return calculated_distances

    def check_distances_based_on_time(self, df, start_date_col='Trip Start Time', end_date_col='Trip End Time', distance_col='distance'):
        start_datetime_object = datetime.strptime(df[start_date_col], '%Y-%m-%d %H:%M:%S')
        end_datetime_object = datetime.strptime(df[end_date_col], '%Y-%m-%d %H:%M:%S')
        time_taken = end_datetime_object-start_datetime_object
        hrs = time_taken.total_seconds()/3600

    def calculate_speeds(self, starting_time_list, ending_time_list, distance_list):
        speed_list = []
        for i in range(len(starting_time_list)):
            try:
                start_datetime_object = datetime.strptime(starting_time_list[i], '%Y-%m-%d %H:%M:%S')
                end_datetime_object = datetime.strptime(ending_time_list[i], '%Y-%m-%d %H:%M:%S')
                time_taken = end_datetime_object-start_datetime_object
                hrs = time_taken.total_seconds()/3600
                speed_list.append(distance_list[i]/hrs)
            except Exception as e:
                speed_list.append(0.0)
        return speed_list

    def generateLatAndLng(self, df):
        lat, lng = df['Trip Origin'].apply(lambda x: str(x).split(','))
        return lat, lng

    def load_data(self, path):
        try:
            df = pd.read_csv(path)
            return df
        except Exception as e:
            return None

    def load_clean_data(self, path):
        try:
            df = pd.read_csv(path)
            # Perform additional cleaning steps here, if needed
            return df
        except Exception as e:
            return None
        
    def detect_outliers(self, df, column_name):
        Q1 = df[column_name].quantile(0.25)
        Q3 = df[column_name].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = (df[column_name] < lower_bound) | (df[column_name] > upper_bound)
        return outliers, lower_bound, upper_bound

    def count_outliers(self, df, column_name):
        outliers, lower_bound, upper_bound = self.detect_outliers(df, column_name)
        above_upper_bound = (df[column_name] > upper_bound).sum()
        below_lower_bound = (df[column_name] < lower_bound).sum()
        print(f"Lower bound for outliers: {lower_bound:.2f}")
        print(f"Upper bound for outliers: {upper_bound:.2f}")
        print(f"Data points above upper bound ({upper_bound:.2f}): {above_upper_bound}")
        print(f"Data points below lower bound ({lower_bound:.2f}): {below_lower_bound}")
    
    def remove_outliers(self, df, column_name):
        outliers, _, _ = self.detect_outliers(df, column_name)
        df_clean = df[~outliers]
        return df_clean
    
    