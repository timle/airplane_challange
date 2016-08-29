import pandas as pd
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.stats.multitest as smm
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import seaborn as sns
sns.set(font_scale=1.5)

# h5 dataset
store = pd.HDFStore('2014_2016.h5') # generated with pre_process_data.py
all_data = store.get('all_data')

# airplane carrier ids
airplane_ids = pd.read_csv('airplane_challange/data/L_AIRLINE_ID.csv')

all_data = pd.merge(all_data, airplane_ids, how='left', left_on='AirlineID', right_on='Code')


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



sub_cols = ['FlightDate', 'AirlineID', 'Description', 'TailNum', 'OriginAirportID', 'OriginCityMarketID', 'DestAirportID',
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

# first round descriptive statistics

agg_fun_1 = {'delayAmnt': {'delay': [np.sum, np.mean, np.median, np.std, len]},
           'Distance': {'dist': [np.sum, np.mean, np.median, np.std, len]}}

agg_fun_2 = {'delayAmnt': {'delay': [np.sum, np.mean, np.median, np.std]},
           'delay_by_dist': {'D_by_D': [np.mean, np.median, np.std, len]}}

# by delay type
stacked.groupby('delayType', axis=0).agg(agg_fun_1)

# by airline
stacked.groupby('Description', axis=0).agg(agg_fun_1)



# exploring models
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
mod_3_wd_v = smf.ols(formula='np.log(delayAmnt+1) ~ delayType * C(quarter) * is_morning_dep + is_weekday_dep + C(Description)', data=stacked)
res_3_wd_v = mod_3_wd_v.fit()
# p value correction
pVals = res_3_wd_v.pvalues
pVals_corr = smm.multipletests(pVals, method='fdr_bh')
res_3_wd_v.pvalues = pVals_corr
# translate coef back into normal values - makes interpretation easier
log_params = res_3_wd_v.params
res_3_wd_v['params'] = np.power(np.e, res_3_wd_v.params)



# logistic... assumption free version?




# viz - hist 1
plt.figure();
sns.set(font_scale=1.5)
p1 = sns.distplot((stacked['delayAmnt']));
p1.set_title('Delay Amount, all flights')
p1.set_xlim([0, 2000])
p1.set_xlabel('Delay (in minutes)')

# viz - hist 2
plt.figure();
sns.set(font_scale=1.5)
p1 = sns.distplot(stacked['delayAmnt'].loc[stacked['delayAmnt'] > 0]);
p1.set_title('Delay Amount, delayed flights')
p1.set_xlim([0, 2000])
p1.set_xlabel('Delay (in minutes)')


# viz - hist 3
plt.figure();
p1 = sns.distplot(np.log(stacked['delayAmnt'].loc[stacked['delayAmnt'] > 0]),kde=False)
p1.set_title('Delay Amount, log transformed, delayed flights')
#p1.set_xlim([0, 2000])
p1.set_xlabel('Delay (in minutes) log')


# plot subset - help speed up plotting
cols_to_subset_for_plot = ['delayAmnt','delay_log', 'delayType', 'quarter', 'is_morning_dep', 'is_weekday_dep']
rows = random.sample(stacked.index, 50000)
plot_subset = stacked.loc[rows, cols_to_subset_for_plot]


# scatter matrix (depreciated)
from pandas.tools.plotting import scatter_matrix
jitter = (np.random.rand(1, len(rows))-1)*.8
plot_subset['delayType_j'] = np.transpose(pd.factorize(plot_subset['delayType'])[0] + jitter)
plot_subset['quarter_j'] = np.transpose(np.array(plot_subset['quarter']) + jitter)
plot_subset['is_morning_dep_j'] = np.transpose(np.array(plot_subset['is_morning_dep']) + jitter)
plot_subset['is_weekday_dep_j'] = np.transpose(np.array(plot_subset['is_weekday_dep']) + jitter)
plot_subset['delay_log'] = np.log(plot_subset.delayAmnt+1)
stacked['delay_log'] = np.log(stacked.delayAmnt+1)
cols_to_plot = ['delay_log', 'delayType', 'quarter_j', 'is_morning_dep_j', 'is_weekday_dep_j']
scatter_matrix(plot_subset[cols_to_plot], alpha=0.2, figsize=(6, 6), diagonal='kde')

# box plot
plt.figure();
bp = stacked.boxplot(column=['delay_log'], by=['delayType'])

# multivariate interactions?
#yo = stacked['delay_log'].hist(by=stacked['delayType'], figsize=(6, 4), bins=100)
#[x[0].set_xlim([0,8]) for x in yo]
#[x[1].set_xlim([0,8]) for x in yo]

#q_dt_mi = [stacked['delayType'], stacked['quarter']]
#pd.MultiIndex.from_arrays(q_dt_mi)

#yo = stacked['delay_log'].hist(by=stacked['quarter'], figsize=(6, 4), bins=100)
#[x[0].set_xlim([0,8]) for x in yo]
#[x[1].set_xlim([0,8]) for x in yo]

#yo = stacked['delay_log'].hist(by=stacked['is_morning_dep'], figsize=(6, 4), bins=100)
#[x[0].set_xlim([0,8]) for x in yo]
#[x[1].set_xlim([0,8]) for x in yo]

#yo = stacked['delay_log'].hist(by=stacked['is_weekday_dep'], figsize=(6, 4), bins=100)
#[x[0].set_xlim([0,8]) for x in yo]
#[x[1].set_xlim([0,8]) for x in yo]



# delay amount, across delay type
plt.figure()
p2 = sns.stripplot(x="delayType", y="delay_log", data=plot_subset, jitter=.4, size=2, alpha = .75)
p2.set_title('Delay amount, 50k Random subset, across delay type')
p2.set_ylim([0,8])
p2.set_xlim([.5,5.5])

# delay amount, across delay type, colored by factor
# takes too long to plot!
sns.stripplot(x="delayType", y="delay_log", data=plot_subset, hue="is_morning_dep_j", jitter=.4)


