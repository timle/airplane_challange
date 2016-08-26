#!/usr/bin/env python
# -*- coding: utf-8 -*-

# automate data download

# take advantage of the naming scheme of the prezip files to automate download of all years/months data
# url pattern: http://tsdata.bts.gov/PREZIP/On_Time_On_Time_Performance_[year]_[month].zip
#   note - non-empty data files start at year: 1987, month: 10

# then join data with airport and carrier codes

# save this preprocessed data out as sqllite for ease of access throughout rest of codebase

import urllib2
import os.path

#from StringIO import StringIO

# download to zip

for year_ii in range(1987, 2016 + 1):
    for month_ii in range(1, 12 + 1):
        url_txt = 'http://tsdata.bts.gov/PREZIP/On_Time_On_Time_Performance_%i_%i.zip' % (year_ii, month_ii)
        sav_name = 'data/airport_data_%i_%i.zip' % (year_ii, month_ii)

        if os.path.isfile(sav_name):
            print('Already exists: ' + url_txt)
            continue

        print('Downloading url: ' + url_txt)
        # download file
        request = urllib2.urlopen(url_txt)

        # save
        output = open(sav_name, "w")
        output.write(request.read())
        output.close()




test = store.get('all_data')
# join airport codes
#   load airport codes
#   note, save extra data to new table for later joins


# join airplane codes
#   load airplain codes
#   note, save extra data to new table for later joins



