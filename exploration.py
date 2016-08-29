import pandas as pd
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt
import math

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


# adding meta info
all_data['is_morning_dep'] = all_data.CRSDepTime < 1200
all_data['is_weekday_dep'] = all_data.FlightDate.dt.dayofweek < 5  #Saturday=5, Sunday=6
all_data['month'] = all_data.FlightDate.dt.month
all_data['quarter'] = np.divide(np.array(all_data['month']), 4) + 1


# subset 2015 only, has delay, and following columns:
cols = list(all_data.columns.values)



sub_cols = ['FlightDate', 'AirlineID', 'TailNum', 'OriginAirportID', 'OriginCityMarketID', 'DestAirportID',
            'DestCityMarketID', 'CRSDepTime', 'DepDelay',  'CRSArrTime', 'ArrTime', 'ArrDelay', 'Cancelled',
            'CancellationCode', 'Diverted', 'Distance', 'CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay',
            'LateAircraftDelay', 'is_morning_dep', 'is_weekday_dep', 'month', 'quarter' ]

is2015 = (all_data.FlightDate >= '2015-01-01') & (all_data.FlightDate < '2016-01-01')
has_net_delay = (all_data.DepDelay + all_data.ArrDelay) > 0
has_no_delay = (all_data.DepDelay + all_data.ArrDelay) <= 0

sub_dat_delay = all_data.loc[is2015 & has_net_delay, sub_cols]
sub_dat_no_delay = all_data.loc[is2015 & has_no_delay, sub_cols]


# lf for regression
# when a delay happens, what causes it
cols = list(sub_dat_delay.columns.values)
delay_cols = ['CarrierDelay',  'WeatherDelay',  'NASDelay',  'SecurityDelay',  'LateAircraftDelay']
base_cols = list(set(cols) - set(delay_cols))
stacked = pd.DataFrame([])
for cur_col in delay_cols:
    # clean up variable names
    # make purpose of loop explicit
    rows_with_delays = sub_dat_delay[cur_col] > 0
    df_subset = sub_dat_delay[base_cols].loc[rows_with_delays]
    delay_subset = sub_dat_delay[cur_col].loc[rows_with_delays]
    df_subset['delayType'] = cur_col
    df_subset['delayAmnt'] = delay_subset
    stacked = pd.concat([stacked, df_subset], ignore_index=True)
# add in flights without delays
df_subset = sub_dat_no_delay.loc[:, base_cols]
df_subset['delayType'] = 'AAnoDelay'
df_subset['delayAmnt'] = 0
stacked = pd.concat([df_subset, stacked], ignore_index=True)


# stacked['delay_by_dist'] = stacked.delayAmnt / stacked.Distance

agg_fun_1 = {'delayAmnt': {'delay': [np.sum, np.mean, np.median, np.std]},
           'Distance': {'dist': [np.sum, np.mean, np.median, np.std, len]}}

agg_fun_2 = {'delayAmnt': {'delay': [np.sum, np.mean, np.median, np.std]},
           'delay_by_dist': {'D_by_D': [np.mean, np.median, np.std, len]}}

stacked.groupby('delayType', axis=0).agg(agg_fun_1)
# given trip of n kilometers, what kind of delay is likely to happen
# this excludes all trips with no delays.
# what is happening, carrier delays are more common, but less severe.
# this means more trips have carrier delays,
# but there is issue with bias in here? only picking trips with a delay?
# it does cause a skew, but does it matter?
# is there a different way to cut up the data, given one trip can have multiple delay types.


# basic fit
#mod = smf.ols(formula='delayAmnt ~ delayType * C(quarter)', data=stacked)
#res = mod.fit()
#print res.summary()

# basic fit + log normalize delay amount
#mod = smf.ols(formula='np.log(delayAmnt) ~ delayType * C(quarter)', data=stacked)
#res = mod.fit()
#print res.summary()


# basic fit

# basic fit + log normalize delay amount
mod_wd = smf.ols(formula='np.log(delayAmnt+1) ~ delayType * C(quarter)', data=stacked)
res_wd = mod_wd.fit()
print res_wd.summary()

# morning and weekday factors
mod_2_wd = smf.ols(formula='np.log(delayAmnt+1) ~ delayType * C(quarter) + is_morning_dep + is_weekday_dep', data=stacked)
res_2_wd = mod_2_wd.fit()
print res_2_wd.summary()

# add airline
mod_3_wd = smf.ols(formula='np.log(delayAmnt+1) ~ delayType * C(quarter) * is_morning_dep + is_weekday_dep + C(AirlineID)', data=stacked)
res_3_wd = mod_3_wd.fit()
print res_3_wd.summary()


# add airline interaction
mod_3_wd = smf.ols(formula='np.log(delayAmnt+1) ~ delayType * C(quarter) * C(AirlineID) + is_morning_dep + is_weekday_dep', data=stacked)
res_3_wd = mod_3_wd.fit()
print res_3_wd.summary()

# viz
from pandas.tools.plotting import scatter_matrix

cols_to_plot = ['delayAmnt', 'delayType', 'quarter', 'is_morning_dep', 'is_weekday_dep']
scatter_matrix(stacked[cols_to_plot], alpha=0.2, figsize=(6, 6), diagonal='kde')


#mod_2 = smf.ols(formula='delayAmnt ~ delayType ', data=stacked2)
#res_2 = mod_2.fit()
#print res_2.summary()

# non-biased by number of trips...







# stacked will make some statistics easier, but keep in mind that flights are repeated.

# stats models basic regression?

# need multivariate plot? pandas does this no?
# explicitly declare some vars as factors.