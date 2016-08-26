#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import zipfile
import re
import numpy as np
import os.path


# import csvs, do some light preprocessing, save as h5 store

# assumes get_data.py has already been runß

# import zipped csvs, preprocess, and build into single table
regex_csv=re.compile(".*(csv)") # for searching csv name in zipped file
# following will be extracted from csv files
# because the above url doesn't allow column subsetting, it's done in the following loop instead
cols_to_get = ['FlightDate', 'AirlineID', 'TailNum', 'FlightNum', 'OriginAirportID', 'OriginCityMarketID',
               'DestAirportID', 'DestCityMarketID', 'CRSDepTime', 'DepTime', 'DepDelay', 'TaxiOut', 'WheelsOff',
               'WheelsOn', 'TaxiIn', 'CRSArrTime', 'ArrTime', 'ArrDelay', 'Cancelled',
               'CancellationCode', 'Diverted', 'CRSElapsedTime', 'ActualElapsedTime', 'AirTime', 'Flights',
               'Distance', 'CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay',
               'FirstDepTime', 'TotalAddGTime', 'LongestAddGTime', 'DivAirportLandings', 'DivReachedDest',
               'DivActualElapsedTime', 'DivArrDelay', 'DivDistance', 'Div1AirportID', 'Div1AirportSeqID',
               'Div1WheelsOn', 'Div1TotalGTime', 'Div1LongestGTime', 'Div1WheelsOff', 'Div1TailNum', 'Div2AirportID',
               'Div2AirportSeqID', 'Div2WheelsOn', 'Div2TotalGTime', 'Div2LongestGTime', 'Div2WheelsOff',
               'Div2TailNum', 'Div3AirportID', 'Div3AirportSeqID', 'Div3WheelsOn', 'Div3TotalGTime',
               'Div3LongestGTime', 'Div3WheelsOff', 'Div3TailNum', 'Div4AirportID', 'Div4AirportSeqID',
               'Div4WheelsOn', 'Div4TotalGTime', 'Div4LongestGTime', 'Div4WheelsOff', 'Div4TailNum',
               'Div5AirportID', 'Div5AirportSeqID', 'Div5WheelsOn', 'Div5TotalGTime', 'Div5LongestGTime',
               'Div5WheelsOff', 'Div5TailNum']
# following columns will be converted to int. this helps with saving space later.
#   will convert all cols except for 'FlightDate', 'TailNum' and 'CancellationCode' (these need to remain strings)
keep_as_strings = ['FlightDate', 'TailNum', 'CancellationCode', 'Div1TailNum', 'Div2TailNum', 'Div3TailNum',
                   'Div4TailNum', 'Div5TailNum']
int_updates_col_names = list(set(cols_to_get) - set(keep_as_strings))
# experimenting with reassigning data types to save space
# going from int 64 (default on my system) to int 16 is a 4x savings in memory/space
# all but two variables fit within int 16 range, and two remaining are positive only, which fit within uint 16 range
# but this is a lazy solution. some columns could be set even more efficiently, though benefit not as great
as_uint16 = ['OriginCityMarketID','DestCityMarketID']
as_int16 = list(set(int_updates_col_names) - set(as_uint16))

dtypes = {'Div1TailNum': str, 'Div2TailNum': str, 'Div3TailNum': str,
          'Div4TailNum': str, 'Div5TailNum': str}  # need to specify these since they are sparse, but are strings


all_data = pd.DataFrame([]) # will collect each month as loop progresses
for year_ii in range(2011, 2016 + 1): # restricting to just last 5 years, for now
    for month_ii in range(1, 12 + 1):
        load_name = 'data/airport_data_%i_%i.zip' % (year_ii, month_ii)
        if not os.path.isfile(load_name):
            print('No file - skipping: ' + load_name)
            continue
        print('parsing file: ' + load_name)
        zf = zipfile.ZipFile(load_name, 'r')
        if zf.namelist().__len__() < 1:
            print "error on file: " + load_name
        # get csv file name from zip (there are multiple files in there)
        csv_name = [m.group(0) for l in zf.namelist() for m in [regex_csv.search(l)] if m]
        # get zipfile object for file
        data = zf.open(csv_name[0])
        # read csv into data frame, from zipfile. restrict to subset of columns (rest are redundant information)
        this_file_data = pd.read_csv(data, usecols=cols_to_get, dtype=dtypes)
        # replace nans with 0's
        # will in turn allows conversion to int
        this_file_data.fillna(0, inplace=True)
        this_file_data[int_updates_col_names] = this_file_data[int_updates_col_names].astype(int)
        # collect data final data frame
        all_data = pd.concat([all_data, this_file_data], ignore_index=True)

# do reassignments
all_data[as_uint16] = all_data[as_uint16].astype(np.uint16)
all_data[as_int16] = all_data[as_int16].astype(np.int16)

# enforce str for these columns (possible mixed types) to prevent h5 complaints
all_data.loc[:, keep_as_strings] = all_data[keep_as_strings].applymap(str)


# save out
# currently works out roughly to 1 gig per year
store = pd.HDFStore('2011_2016_int16test.h5')
store.put('all_data', all_data)
store.close()
