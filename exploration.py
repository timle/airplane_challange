import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt

store = pd.HDFStore('2014_2016.h5') # generated with pre_process_data.py

all_data = store.get('all_data')

#convert datetime
all_data.FlightDate = pd.to_datetime(all_data.FlightDate)

# simple t-test

is2015 = (all_data.FlightDate >= '2015-01-01') & (all_data.FlightDate < '2016-01-01')
del_CarrierDelay = all_data.CarrierDelay.loc[(all_data.CarrierDelay>0) & is2015]
del_WeatherDelay = all_data.WeatherDelay.loc[(all_data.WeatherDelay>0) & is2015]
del_NASDelay = all_data.NASDelay.loc[(all_data.NASDelay>0) & is2015]
del_SecurityDelay = all_data.SecurityDelay.loc[(all_data.SecurityDelay>0) & is2015]
del_LateAircraftDelay = all_data.LateAircraftDelay.loc[(all_data.LateAircraftDelay>0) & is2015]


np.average(del_CarrierDelay)
np.average(del_WeatherDelay)
np.average(del_NASDelay)
np.average(del_SecurityDelay)
np.average(del_LateAircraftDelay)
#label delay type, stack dataframes
# then can use apply...

np.max(del_CarrierDelay)
np.max(del_WeatherDelay)
np.max(del_NASDelay)
np.max(del_SecurityDelay)
np.max(del_LateAircraftDelay)

np.sum(del_CarrierDelay)/60/24
np.sum(del_WeatherDelay)/60/24
np.sum(del_NASDelay)/60/24
np.sum(del_SecurityDelay)/60/24
np.sum(del_LateAircraftDelay)/60/24


len(del_CarrierDelay) - (np.sum(del_CarrierDelay <= 30))
len(del_WeatherDelay) - (np.sum(del_WeatherDelay <= 30))


sum(del_CarrierDelay)
sum(del_WeatherDelay)

len(del_CarrierDelay) # 570022 incidents
len(del_WeatherDelay) # 64716 incidents


plt.subplot(2, 1, 1)
plt.hist(np.log(del_CarrierDelay), bins='auto')  # plt.hist passes it's arguments to np.histogram
plt.title("del_car")

plt.subplot(2, 1, 2)
plt.hist(np.log(del_WeatherDelay), bins='auto')  # plt.hist passes it's arguments to np.histogram
plt.title("del_weath")

plt.show()


# subset 2015 only, has delay, and following columns:
cols = list(all_data.columns.values)

sub_cols = ['FlightDate', 'AirlineID', 'TailNum', 'OriginAirportID', 'OriginCityMarketID', 'DestAirportID',
            'DestCityMarketID', 'CRSDepTime', 'DepDelay',  'CRSArrTime', 'ArrTime', 'ArrDelay', 'Cancelled',
            'CancellationCode', 'Diverted', 'Distance', 'CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay',
            'LateAircraftDelay']

is2015 = (all_data.FlightDate >= '2015-01-01') & (all_data.FlightDate < '2016-01-01')
has_net_delay = (all_data.DepDelay + all_data.ArrDelay) > 0

sub_dat = all_data[sub_cols].loc[is2015 & has_net_delay]

# set departure information
sub_dat['is_morning_dep'] = sub_dat.CRSDepTime < 1200
sub_dat['is_weekday_dep'] = sub_dat.FlightDate.dt.dayofweek < 5  #Saturday=5, Sunday=6
sub_dat['month'] = sub_dat.FlightDate.dt.month


cols = list(sub_dat.columns.values)
delay_cols = ['CarrierDelay',  'WeatherDelay',  'NASDelay',  'SecurityDelay',  'LateAircraftDelay']
base_cols = list(set(cols) - set(delay_cols))
stacked = pd.DataFrame([])
for cur_col in delay_cols:
    # clean up variable names
    # make purpose of loop explicit
    rows_with_delays = sub_dat[cur_col] > 0
    df_subset = sub_dat[base_cols].loc[rows_with_delays]
    delay_subset = sub_dat[cur_col].loc[rows_with_delays]
    df_subset['delayType'] = cur_col
    df_subset['delayAmnt'] = delay_subset
    stacked = pd.concat([stacked, df_subset], ignore_index=True)

# stacked will make some statistics easier, but keep in mind that flights are repeated.

# stats models basic regression?

# need multivariate plot? pandas does this no?
# explicitly declare some vars as factors.