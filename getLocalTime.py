# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Jun 25, 2017
# @author:       Bo Zhao
# @email:        zhao2@oregonstate.edu
# @website:      http://geoviz.ceaos.oregonstate.edu
# @organization: Cartography and Geovisualization Group @ Oregon State University


import json
import pytz
from tzwhere import tzwhere
from datetime import datetime
from dateutil import tz

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('UTC')

tzwhere = tzwhere.tzwhere()

csvfile = open("pogo-localtime.csv", "w")

csvfile.write("type, species, timing, lat, lng, createdAt, local_h, local_wd\n")
file_directory = "a-400000.json"
json_data = open(file_directory).read()

data = json.loads(json_data)
features = data['features']

for feature in features:
    try:
        lng = feature['geometry']['coordinates'][0]
        lat = feature['geometry']['coordinates'][1]

        timezone_str = tzwhere.tzNameAt(latitude=lat, longitude=lng)  # Seville coordinates
        print lng, lat, timezone_str
        to_zone = tz.gettz(timezone_str)
        timezone = pytz.timezone(timezone_str)
        datetime_obj = datetime.strptime(feature['properties']['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
        utc = datetime_obj.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)

        local_h = local.hour
        local_wd = local.weekday()
        csvfile.write("%s, %s, %s, %f, %f, %s, %d, %d\n" % (feature['properties']['type'], int(feature['properties']['speciesId']), feature['properties']['timing'], lat, lng, local.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), local_h, local_wd))
    except:
        pass


csvfile.close()
