import pandas as pd
import statsmodels
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt

store = pd.HDFStore('2014_2016.h5') # generated with pre_process_data.py
all_data = store.get('all_data')

#convert datetime
all_data.FlightDate = pd.to_datetime(all_data.FlightDate)



#plt.subplot(2, 1, 1)
#plt.hist(np.log(del_CarrierDelay), bins='auto')  # plt.hist passes it's arguments to np.histogram
#plt.title("del_car")

#plt.subplot(2, 1, 2)
#plt.hist(np.log(del_WeatherDelay), bins='auto')  # plt.hist passes it's arguments to np.histogram
#plt.title("del_weath")

#plt.show()


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




# biased towards when delays occur
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

stacked['delay_by_dist'] = stacked.delayAmnt / stacked.Distance

agg_fun_1 = {'delayAmnt': {'delay': [np.sum, np.mean, np.median, np.std]},
           'Distance': {'dist': [np.sum, np.mean, np.median, np.std, len]}}

agg_fun_2 = {'delayAmnt': {'delay': [np.sum, np.mean, np.median, np.std]},
           'delay_by_dist': {'D_by_D': [np.mean, np.median, np.std, len]}}

stacked.groupby('delayType', axis=0).agg(agg_fun_2)
# given trip of n kilometers, what kind of delay is likely to happen
# this excludes all trips with no delays.
# what is happening, carrier delays are more common, but less severe.
# this means more trips have carrier delays,
# but there is issue with bias in here? only picking trips with a delay?




# non-biased
cols = list(sub_dat.columns.values)
delay_cols = ['CarrierDelay',  'WeatherDelay',  'NASDelay',  'SecurityDelay',  'LateAircraftDelay']
base_cols = list(set(cols) - set(delay_cols))
stacked2 = pd.DataFrame([])
for cur_col in delay_cols:
    # clean up variable names
    # make purpose of loop explicit
    df_subset = sub_dat[base_cols].loc
    delay_subset = sub_dat[cur_col].loc
    df_subset['delayType'] = cur_col
    df_subset['delayAmnt'] = delay_subset
    stacked = pd.concat([stacked, df_subset], ignore_index=True)

stacked['delay_by_dist'] = stacked.delayAmnt / stacked.Distance

agg_fun_1 = {'delayAmnt': {'delay': [np.sum, np.mean, np.median, np.std]},
           'Distance': {'dist': [np.sum, np.mean, np.median, np.std, len]}}

agg_fun_2 = {'delayAmnt': {'delay': [np.sum, np.mean, np.median, np.std]},
           'delay_by_dist': {'D_by_D': [np.sum, np.mean, np.median, np.std, len]}}

stacked.groupby('delayType', axis=0).agg(agg_fun_2)





# stacked will make some statistics easier, but keep in mind that flights are repeated.

# stats models basic regression?

# need multivariate plot? pandas does this no?
# explicitly declare some vars as factors.