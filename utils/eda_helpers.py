import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

class EDA:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.trips_df = None
        self.requests_df = None

    def load_data(self):
        trips_file = os.path.join(self.data_dir, 'nb.csv')
        self.trips_df = pd.read_csv(trips_file)

        requests_file = os.path.join(self.data_dir, 'driver_locations_during_request.csv')
        self.requests_df = pd.read_csv(requests_file)

    def summary_stats(self):
        print("Trips Data Summary:")
        print(self.trips_df.describe())
        print("\nDelivery Requests Data Summary:")
        print(self.requests_df.describe())

    def plot_trip_distribution(self):
        sns.distplot(self.trips_df['Trip Duration'])
        plt.title('Trip Duration Distribution')
        plt.xlabel('Duration (minutes)')
        plt.ylabel('Frequency')
        plt.show()