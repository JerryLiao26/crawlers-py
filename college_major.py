#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Warning: this crawler only works on certain pages,
# if you want it to work on other pages, please change
# the needed params or methods

import requests
import json

# Set up request
url = "http://www.fengup.com/news/60593.html"

headers = {
    "User-Agent" : # Linux Chrome
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36"
}

# Send request
respond = requests.get(url=url, headers=headers)
respond.encoding = "GBK"

# Extract form
table_start_index = respond.text.index('<tr')
table_end_index = respond.text.index('</tbody')

table_data = respond.text[table_start_index : table_end_index]

# Get data
data = {}

ptr = 0
end_ptr = 0
loop = 0

# while table_data.find('<td>', end_ptr):
while table_data.find('<td>', end_ptr) != -1:
    # First slice
    ptr = table_data.index('<td>', end_ptr)
    end_ptr = table_data.index('</td>', ptr)

    data_slice_1 = table_data[ptr + 4 : end_ptr]

    ptr = end_ptr

    # Second slice
    ptr = table_data.index('<td>', end_ptr)
    end_ptr = table_data.index('</td>', ptr)

    data_slice_2 = table_data[ptr + 4 : end_ptr]

    ptr = end_ptr

    # Not title
    try:
        data_slice_1.index('strong')

    except ValueError:
        # No notes
        try:
            notes_index = data_slice_2.index('（')
            data_slice_2 = data_slice_2[ : notes_index]

        except ValueError:
            pass

        finally:
            data_slice = {
                'code' : data_slice_1,
                'name' : data_slice_2
            }

            data[loop] = data_slice

            loop += 1

# Write into file
with open('./major_data.json', 'w') as out_data_json:
    json.dump(data, out_data_json)
