import datetime
import json
import csv

#Creates a list from placeVisit data.
def placeVisit(placeVisit_dict):
    place_id = placeVisit_dict["location"]["placeId"]
    lat = placeVisit_dict["location"]["latitudeE7"]
    lon = placeVisit_dict["location"]["longitudeE7"]
    address = placeVisit_dict["location"]["address"].replace("\n",", ")
    start_time = placeVisit_dict["duration"]["startTimestampMs"]
    end_time = placeVisit_dict["duration"]["endTimestampMs"]
    confidence = placeVisit_dict["visitConfidence"]
    #Formatting variables
    lat = int(lat)/1e7
    lon = int(lon)/1e7
    start_time = timeStampToDate(int(start_time))
    end_time = timeStampToDate(int(end_time))
    place_visit = [place_id,lat, lon, address, start_time, end_time, confidence]
    return place_visit

#Returns a list of all the waypoints of a activity.
def activitySegment(activitySegment_dict):
    start_point = activityStartPoint(activitySegment_dict)
    end_point = activityEndPoint(activitySegment_dict)
    activity_points = activityRawPoints(activitySegment_dict, start_point)
    activity_points.insert(0, start_point)
    end_point.insert(1, (len(activity_points)) + 1)
    activity_points.append(end_point)
    return activity_points

#Set start point of activity as a list.
def activityStartPoint(activitySegment_dict):
    trip_id = activitySegment_dict["duration"]["startTimestampMs"]
    order = 1
    lat = activitySegment_dict["startLocation"]["latitudeE7"]
    lon = activitySegment_dict["startLocation"]["longitudeE7"]
    time_stamp = timeStampToDate(int(trip_id))
    distance = activitySegment_dict.get("distance", 0)
    ac_type = activitySegment_dict["activityType"]
    confidence = activitySegment_dict["confidence"]
    time_convention = timeStampToAMPM(int(trip_id))
    #Formatting variables
    lat = int(lat)/1e7
    lon = int(lon)/1e7
    start_point = [trip_id, order, lat, lon, time_stamp, distance, ac_type, confidence, time_convention]
    return start_point

#Creates a list of list with each waypoint of activity.
def activityRawPoints(activitySegment_dict, start_point):
    points = []
    order = 1
    if "waypointPath" in activitySegment_dict.keys():
      way_points = activitySegment_dict["waypointPath"]["waypoints"]
      for point in way_points:
        trip_id = start_point[0]
        order += 1
        lat = int(point["latE7"])/1e7
        lon = int(point["lngE7"])/1e7
        time_stamp = start_point[4]
        distance = start_point[5]
        ac_type = start_point[6]
        confidence = start_point[7]
        time_convention = timeStampToAMPM(int(trip_id))
        #Formatting variables
        list_point = [trip_id, order, lat, lon, time_stamp, distance, ac_type, confidence, time_convention]
        points.append(list_point)
    elif "simplifiedRawPath" in activitySegment_dict.keys():
      raw_points = activitySegment_dict["simplifiedRawPath"]["points"]
      for point in raw_points:
        trip_id = start_point[0]
        order += 1
        lat = int(point["latE7"])/1e7
        lon = int(point["lngE7"])/1e7
        time_stamp = timeStampToDate(int(point["timestampMs"]))
        distance = start_point[5]
        ac_type = start_point[6]
        confidence = start_point[7]
        time_convention = timeStampToAMPM(int(trip_id))
        #Formatting variables
        list_point = [trip_id, order, lat, lon, time_stamp, distance, ac_type, confidence, time_convention]
        points.append(list_point)
    return points

#Set end point of activity as a list.
def activityEndPoint(activitySegment_dict):
    trip_id = activitySegment_dict["duration"]["startTimestampMs"]
    lat = activitySegment_dict["endLocation"]["latitudeE7"]
    lon = activitySegment_dict["endLocation"]["longitudeE7"]
    time_stamp = activitySegment_dict["duration"]["endTimestampMs"]
    distance = activitySegment_dict.get("distance", 0)
    ac_type = activitySegment_dict["activityType"]
    confidence = activitySegment_dict["confidence"]
    time_convention = timeStampToAMPM(int(trip_id))
    #Formatting variables
    lat = int(lat)/1e7
    lon = int(lon)/1e7
    time_stamp = timeStampToDate(int(time_stamp))
    end_point = [trip_id, lat, lon, time_stamp, distance, ac_type, confidence, time_convention]
    return end_point

#Convert milliseconds timestamp into a readable date.
def timeStampToDate(milliseconds):
    date = datetime.datetime.fromtimestamp(milliseconds/1000.0)
    date = date.strftime('%Y-%m-%d %H:%M:%S')
    return date

#Check time convention.
def timeStampToAMPM(milliseconds):
    date = datetime.datetime.fromtimestamp(milliseconds/1000.0)
    if date.hour < 12:
      time_convention = "AM"
    else:
      time_convention = "PM"
    return time_convention

#Method to run all the scripts.data_unit['activitySegment'].keys()
>>> dict_keys(['startLocation', 'endLocation', 'duration', 'distance', 'activityType', 'confidence', 'activities', 'waypointPath', 'simplifiedRawPath']){
  "timelineObjects" : [ {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 448980113,
        "longitudeE7" : -932234573
      },
      "endLocation" : {
        "latitudeE7" : 449775115,
        "longitudeE7" : -932736596
      },
      "duration" : {
        "startTimestampMs" : "15830311539.99", Saturday, February 29, 2020 8:52:33.999 PM
        "endTimestampMs" : "1583031975707"
      },
      "distance" : 10810,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "HIGH",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 83.60238671302795
      }, {
        "activityType" : "STILL",
        "probability" : 13.840694725513458
      }, {
        "activityType" : "WALKING",
        "probability" : 1.4871674589812756
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 448981208,
        -932234573
        }, {
      : 448980979,
        -932746963
        }, {
      : 449775047,
        -932736663
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583031975707",
        "location" : {
          "latitudeE7" : 449775115,
          "longitudeE7" : -932736596,
          "accuracyMetres" : 125
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 449770542,
        "longitudeE7" : -932753880,
        "placeId" : "ChIJ2cz51agts1IRSazGgsGXcZ8",
        "address" : "731 Hennepin Ave #1\nMinneapolis, MN 55403\nUSA",
        "name" : "Union Rooftop",
        "sourceInfo" : {
          "deviceTag" : -2093848546
        },
        "locationConfidence" : 78.55645
      },
      "duration" : {
        "startTimestampMs" : "1583031975707",
        "endTimestampMs" : "1583052820861"
      },
      "placeConfidence" : "MEDIUM_CONFIDENCE",
      "childVisits" : [ {
        "location" : {
          "latitudeE7" : 449772959,
          "longitudeE7" : -932750231,
          "placeId" : "ChIJtR-HT5Eys1IR0XIKobtXPdk",
          "address" : "731 Hennepin Ave\nMinneapolis, MN 55403\nUSA",
          "name" : "REV Ultra Lounge",
          "sourceInfo" : {
            "deviceTag" : -2093848546
          },
          "locationConfidence" : 46.46219
        },
        "duration" : {
          "startTimestampMs" : "1583031975707",
          "endTimestampMs" : "1583052820861"
        },
        "placeConfidence" : "MEDIUM_CONFIDENCE",
        "centerLatE7" : 449770850,
        "centerLngE7" : -932743450,
        "visitConfidence" : 97,
        "otherCandidateLocations" : [ {
          "latitudeE7" : 449773046,
          "longitudeE7" : -932754335,
          "placeId" : "ChIJBbVhRpEys1IRQw9PjnqyJWI",
          "locationConfidence" : 29.703474
        }, {
          "latitudeE7" : 449771351,
          "longitudeE7" : -932730977,
          "placeId" : "ChIJjSOn2pAys1IRKpXwH3Ehj98",
          "locationConfidence" : 0.8191539.6
        }, {
          "latitudeE7" : 449774610,
          "longitudeE7" : -932750370,
          "placeId" : "ChIJ08HdQJEys1IRsj-S-bkBnf0",
          "locationConfidence" : 0.6103774
        }, {
          "latitudeE7" : 449781309,
          "longitudeE7" : -932727939.,
          "placeId" : "ChIJmda725Ays1IRO_M_AAKOtDc",
          "locationConfidence" : 0.29531738
        } ],
        "editConfirmationStatus" : "NOT_CONFIRMED"
      } ],
      "centerLatE7" : 449770850,
      "centerLngE7" : -932743450,
      "visitConfidence" : 97,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 449773046,
        "longitudeE7" : -932754335,
        "placeId" : "ChIJBbVhRpEys1IRQw9PjnqyJWI",
        "locationConfidence" : 19.822271
      }, {
        "latitudeE7" : 449771351,
        "longitudeE7" : -932730977,
        "placeId" : "ChIJjSOn2pAys1IRKpXwH3Ehj98",
        "locationConfidence" : 0.546653
      }, {
        "latitudeE7" : 449774610,
        "longitudeE7" : -932750370,
        "placeId" : "ChIJ08HdQJEys1IRsj-S-bkBnf0",
        "locationConfidence" : 0.4073283
      }, {
        "latitudeE7" : 449781309,
        "longitudeE7" : -932727939.,
        "placeId" : "ChIJmda725Ays1IRO_M_AAKOtDc",
        "locationConfidence" : 0.19707665
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 449766663,
        "longitudeE7" : -932750419
      },
      "endLocation" : {
        "latitudeE7" : 449029726,
        "longitudeE7" : -932173268
      },
      "duration" : {
        "startTimestampMs" : "1583052820861",
        "endTimestampMs" : "1583053883353"
      },
      "distance" : 9796,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "HIGH",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 90.63105583190918
      }, {
        "activityType" : "STILL",
        "probability" : 7.52694234251976
      }, {
        "activityType" : "WALKING",
        "probability" : 0.914988573640585
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 449767341,
        -932749786
        }, {
      : 449758644,
        -932729415
        }, {
      : 449758644,
        -932729415
        }, {
      : 449074554,
        -93275039.6
        }, {
      : 449029769,
        -932178039.
        } ]
      },
      "simplifiedRawPath" : {
        "points" : [ {
      : 449758530,
        -932730637,
          "timestampMs" : "1583052994489",
          "accuracyMeters" : 65
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583054098844",
        "location" : {
          "latitudeE7" : 449026438,
          "longitudeE7" : -932177830,
          "accuracyMetres" : 84
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 449026654,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJn40NGh4p9ocRomjhS3xb_MM",
        "address" : "5529 38th Ave S\nMinneapolis, MN 55417\nUSA",
        "name" : "5529 38th Ave S",
        "sourceInfo" : {
          "deviceTag" : -2093848546
        },
        "locationConfidence" : 99.22263
      },
      "duration" : {
        "startTimestampMs" : "1583053883353",
        "endTimestampMs" : "1583092066954"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 449027733,
      "centerLngE7" : -932175967,
      "visitConfidence" : 91,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 449027748,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJpQyEGh4p9ocRfZ8hfqyGpeI",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.25698608
      }, {
        "latitudeE7" : 449021465,
        "longitudeE7" : -932171866,
        "placeId" : "ChIJ7wdfPh4p9ocRlQhY9AwpFwk",
        "locationConfidence" : 0.239.85007
      }, {
        "latitudeE7" : 449026796,
        "longitudeE7" : -932200715,
        "placeId" : "ChIJjXZ9muEo9ocRGAXdqygVk2s",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.056481782
      }, {
        "latitudeE7" : 449055365,
        "longitudeE7" : -932174700,
        "placeId" : "ChIJpS6cnB0p9ocRo6jVi3DIi2I",
        "locationConfidence" : 0.050405554
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 449017945,
        "longitudeE7" : -932178311
      },
      "endLocation" : {
        "latitudeE7" : 452221204,
        "longitudeE7" : -933346797
      },
      "duration" : {
        "startTimestampMs" : "1583092066954",
        "endTimestampMs" : "1583094236005"
      },
      "distance" : 42987,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "HIGH",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 96.01058959960938
      }, {
        "activityType" : "STILL",
        "probability" : 2.69849244505167
      }, {
        "activityType" : "WALKING",
        "probability" : 0.5223383661359549
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 449017944,
        -932178268
        }, {
      : 450987892,
        -931881408
        }, {
      : 452221069,
        -933346405
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583094601008",
        "location" : {
          "latitudeE7" : 452223879,
          "longitudeE7" : -933349052,
          "accuracyMetres" : 70
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 452223368,
        "longitudeE7" : -933348614,
        "placeId" : "ChIJQXOWrKg9s1IRBEmWSrQzk3I",
        "address" : "13808 Northwood Dr NW\nAndover, MN 55304\nUSA",
        "name" : "13808 Northwood Dr NW",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 99.46694
      },
      "duration" : {
        "startTimestampMs" : "1583094236005",
        "endTimestampMs" : "1583099894000"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 452222500,
      "centerLngE7" : -933347850,
      "visitConfidence" : 85,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 452202111,
        "longitudeE7" : -933342250,
        "placeId" : "ChIJDX__KKk9s1IRdOeV0Z0wZMg",
        "locationConfidence" : 0.18566135
      }, {
        "latitudeE7" : 452200020,
        "longitudeE7" : -933333874,
        "placeId" : "ChIJLZitwM09s1IRuZHWf0_P3eA",
        "locationConfidence" : 0.105918124
      }, {
        "latitudeE7" : 452209060,
        "longitudeE7" : -933346000,
        "placeId" : "ChIJs4p60qg9s1IRPib1FjJRoX8",
        "locationConfidence" : 0.09103308
      }, {
        "latitudeE7" : 452201639.,
        "longitudeE7" : -933333536,
        "placeId" : "ChIJKd2uMak9s1IRrLUInOo-tB4",
        "locationConfidence" : 0.055628754
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 452213038,
        "longitudeE7" : -933330950
      },
      "endLocation" : {
        "latitudeE7" : 449010020,
        "longitudeE7" : -932178356
      },
      "duration" : {
        "startTimestampMs" : "1583099894000",
        "endTimestampMs" : "1583102169014"
      },
      "distance" : 47707,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "HIGH",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 83.09993147850037
      }, {
        "activityType" : "STILL",
        "probability" : 8.84978100657463
      }, {
        "activityType" : "WALKING",
        "probability" : 6.278771162033081
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 452213249,
        -933330764
        }, {
      : 452196197,
        -933375701
        }, {
      : 452102050,
        -933372879
        }, {
      : 451041564,
        -931884613
        }, {
      : 450387763,
        -931900634
        }, {
      : 449764022,
        -932464904
        }, {
      : 449010009,
        -932178344
        } ]
      },
      "simplifiedRawPath" : {
        "points" : [ {
      : 452102051,
        -933373184,
          "timestampMs" : "1583100034000",
          "accuracyMeters" : 5
        }, {
      : 450387764,
        -931900787,
          "timestampMs" : "1583101134011",
          "accuracyMeters" : 5
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583102169014",
        "location" : {
          "latitudeE7" : 449010020,
          "longitudeE7" : -932178356,
          "accuracyMetres" : 65
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 449026654,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJn40NGh4p9ocRomjhS3xb_MM",
        "address" : "5529 38th Ave S\nMinneapolis, MN 55417\nUSA",
        "name" : "5529 38th Ave S",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 78.7839.3
      },
      "duration" : {
        "startTimestampMs" : "1583102169014",
        "endTimestampMs" : "1583112318000"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 449010020,
      "centerLngE7" : -932178356,
      "visitConfidence" : 86,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 449008044,
        "longitudeE7" : -932175785,
        "placeId" : "ChIJD5ro0R8p9ocRFoWZX94ufys",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 15.464292
      }, {
        "latitudeE7" : 449021465,
        "longitudeE7" : -932171866,
        "placeId" : "ChIJ7wdfPh4p9ocRlQhY9AwpFwk",
        "locationConfidence" : 1.9902947
      }, {
        "latitudeE7" : 449027748,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJpQyEGh4p9ocRfZ8hfqyGpeI",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.739.47275
      }, {
        "latitudeE7" : 449026796,
        "longitudeE7" : -932200715,
        "placeId" : "ChIJjXZ9muEo9ocRGAXdqygVk2s",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.6720774
      }, {
        "latitudeE7" : 449009138,
        "longitudeE7" : -932175785,
        "placeId" : "ChIJ1TztzR8p9ocRQgY7ndm8I04",
        "locationConfidence" : 0.6550781
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 449034863,
        "longitudeE7" : -932150360
      },
      "endLocation" : {
        "latitudeE7" : 449023741,
        "longitudeE7" : -932177187
      },
      "duration" : {
        "startTimestampMs" : "1583112318000",
        "endTimestampMs" : "1583115100000"
      },
      "distance" : 2865,
      "activityType" : "WALKING",
      "confidence" : "HIGH",
      "activities" : [ {
        "activityType" : "WALKING",
        "probability" : 77.83254981040955
      }, {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 10.756460577249527
      }, {
        "activityType" : "STILL",
        "probability" : 7.434827834367752
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 449035568,
        -932150344
        }, {
      : 449044837,
        -932114257
        }, {
      : 449067955,
        -9321139.52
        }, {
      : 449071998,
        -932133102
        }, {
      : 449071998,
        -932152175
        }, {
      : 449053382,
        -932167510
        }, {
      : 449053382,
        -932169876
        }, {
      : 449053421,
        -932222518
        }, {
      : 448990173,
        -932229080
        }, {
      : 448981170,
        -932223434
        }, {
      : 448999824,
        -932196578
        }, {
      : 449020652,
        -932178192
        }, {
      : 449023742,
        -932178192
        } ]
      },
      "simplifiedRawPath" : {
        "points" : [ {
      : 449067955,
        -932114792,
          "timestampMs" : "1583112807000",
          "accuracyMeters" : 10
        }, {
      : 449072037,
        -932151337,
          "timestampMs" : "1583113133001",
          "accuracyMeters" : 10
        }, {
      : 449053764,
        -932169876,
          "timestampMs" : "1583113413001",
          "accuracyMeters" : 10
        }, {
      : 448990173,
        -932229996,
          "timestampMs" : "1583114348001",
          "accuracyMeters" : 10
        }, {
      : 448999100,
        -932196579,
          "timestampMs" : "1583114758002",
          "accuracyMeters" : 10
        } ]
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 449026654,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJn40NGh4p9ocRomjhS3xb_MM",
        "address" : "5529 38th Ave S\nMinneapolis, MN 55417\nUSA",
        "name" : "5529 38th Ave S",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 98.312256
      },
      "duration" : {
        "startTimestampMs" : "1583115100000",
        "endTimestampMs" : "1583122960873"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 449024650,
      "centerLngE7" : -932177300,
      "visitConfidence" : 94,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 449021465,
        "longitudeE7" : -932171866,
        "placeId" : "ChIJ7wdfPh4p9ocRlQhY9AwpFwk",
        "locationConfidence" : 0.9751099
      }, {
        "latitudeE7" : 449027748,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJpQyEGh4p9ocRfZ8hfqyGpeI",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.1941698
      }, {
        "latitudeE7" : 449026796,
        "longitudeE7" : -932200715,
        "placeId" : "ChIJjXZ9muEo9ocRGAXdqygVk2s",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.10691104
      }, {
        "latitudeE7" : 449027737,
        "longitudeE7" : -932159438,
        "placeId" : "ChIJ3ZDiYx4p9ocR-z5up0-vsRk",
        "locationConfidence" : 0.10576681
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 449025617,
        "longitudeE7" : -932177542
      },
      "endLocation" : {
        "latitudeE7" : 449039.778,
        "longitudeE7" : -932177928
      },
      "duration" : {
        "startTimestampMs" : "1583122960873",
        "endTimestampMs" : "1583124930000"
      },
      "distance" : 157,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "LOW",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 52.76137590408325
      }, {
        "activityType" : "WALKING",
        "probability" : 22.949881851673126
      }, {
        "activityType" : "STILL",
        "probability" : 21.34062498807907
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 449025611,
        -932178115
        }, {
      : 449037704,
        -932177963
        }, {
      : 449039.764,
        -932177963
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583124930000",
        "location" : {
          "latitudeE7" : 449039.778,
          "longitudeE7" : -932177928,
          "accuracyMetres" : 70
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 449026654,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJn40NGh4p9ocRomjhS3xb_MM",
        "address" : "5529 38th Ave S\nMinneapolis, MN 55417\nUSA",
        "name" : "5529 38th Ave S",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 98.884315
      },
      "duration" : {
        "startTimestampMs" : "1583124930000",
        "endTimestampMs" : "15831618039.99"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 449030933,
      "centerLngE7" : -932177700,
      "visitConfidence" : 72,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 449027748,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJpQyEGh4p9ocRfZ8hfqyGpeI",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.31995088
      }, {
        "latitudeE7" : 449021465,
        "longitudeE7" : -932171866,
        "placeId" : "ChIJ7wdfPh4p9ocRlQhY9AwpFwk",
        "locationConfidence" : 0.24381062
      }, {
        "latitudeE7" : 449026796,
        "longitudeE7" : -932200715,
        "placeId" : "ChIJjXZ9muEo9ocRGAXdqygVk2s",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.12477461
      }, {
        "latitudeE7" : 449008044,
        "longitudeE7" : -932175785,
        "placeId" : "ChIJD5ro0R8p9ocRFoWZX94ufys",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.098958194
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 449027534,
        "longitudeE7" : -932177741
      },
      "endLocation" : {
        "latitudeE7" : 448899646,
        "longitudeE7" : -930332334
      },
      "duration" : {
        "startTimestampMs" : "15831618039.99",
        "endTimestampMs" : "1583163809201"
      },
      "distance" : 16497,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "HIGH",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 82.33104944229126
      }, {
        "activityType" : "STILL",
        "probability" : 14.837242662906647
      }, {
        "activityType" : "WALKING",
        "probability" : 1.4634612947702408
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 449015922,
        -932178268
        }, {
      : 448912963,
        -931847686
        }, {
      : 448899726,
        -930331573
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583164174001",
        "location" : {
          "latitudeE7" : 448888412,
          "longitudeE7" : -930337618,
          "accuracyMetres" : 65
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 448908979,
        "longitudeE7" : -930346973,
        "placeId" : "ChIJs0zWB7Mss1IRrfmCKCjytuk",
        "address" : "103 Concord Exchange N\nSouth St Paul, MN 55075\nUSA",
        "name" : "Vandalia Glassworks",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 46.010746
      },
      "duration" : {
        "startTimestampMs" : "1583163809201",
        "endTimestampMs" : "1583164333002"
      },
      "placeConfidence" : "LOW_CONFIDENCE",
      "centerLatE7" : 448894000,
      "centerLngE7" : -930334950,
      "visitConfidence" : 74,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 448894061,
        "longitudeE7" : -930337005,
        "placeId" : "ChIJ2T8C8gvU94cRl6myTmODCzc",
        "locationConfidence" : 37.43891
      }, {
        "latitudeE7" : 448901150,
        "longitudeE7" : -930344150,
        "placeId" : "ChIJM_4HcAzU94cRx2AzQ0Effeg",
        "locationConfidence" : 7.7434435
      }, {
        "latitudeE7" : 448875317,
        "longitudeE7" : -930331362,
        "placeId" : "ChIJvzPCwAvU94cRZnVKvX6ihu0",
        "locationConfidence" : 3.0113845
      }, {
        "latitudeE7" : 448895339.,
        "longitudeE7" : -930310995,
        "placeId" : "ChIJp_xyRTgs9ocR6rdNlvqMTVM",
        "locationConfidence" : 1.6788082
      }, {
        "latitudeE7" : 448895339.,
        "longitudeE7" : -930310995,
        "placeId" : "ChIJKVFTMQnU94cR04PpaW6yMg8",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 1.2181762
      }, {
        "latitudeE7" : 448896296,
        "longitudeE7" : -930313369,
        "placeId" : "ChIJC3KDNgnU94cR2Y88udvvXx4",
        "locationConfidence" : 0.7476246
      }, {
        "latitudeE7" : 44888439.8,
        "longitudeE7" : -930321841,
        "placeId" : "ChIJNVaW7LEus1IRDCdQMTW7FU0",
        "locationConfidence" : 0.5510031
      }, {
        "latitudeE7" : 448891230,
        "longitudeE7" : -930339.270,
        "placeId" : "ChIJMWzGkgvU94cRJ9sd6GCsYyU",
        "locationConfidence" : 0.52911
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 448788487,
        "longitudeE7" : -930309002,
        "placeId" : "ChIJJbo4a_HT94cRdUPhXvYFxJs",
        "address" : "701 Concord St S\nSouth St Paul, MN 55075\nUSA",
        "name" : "Envision Hotel St. Paul South, Ascend Hotel Collection",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 77.49198
      },
      "duration" : {
        "startTimestampMs" : "1583164333002",
        "endTimestampMs" : "1583168331999"
      },
      "placeConfidence" : "MEDIUM_CONFIDENCE",
      "centerLatE7" : 448777400,
      "centerLngE7" : -930311250,
      "visitConfidence" : 95,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 448803817,
        "longitudeE7" : -930312518,
        "placeId" : "ChIJbzqju_bT94cRQHlaGOT-RIk",
        "locationConfidence" : 8.81086
      }, {
        "latitudeE7" : 448777099,
        "longitudeE7" : -930325464,
        "placeId" : "ChIJrzK4ZzXT94cRaCktWcqkZ48",
        "locationConfidence" : 8.635769
      }, {
        "latitudeE7" : 449425340,
        "longitudeE7" : -930988190,
        "placeId" : "ChIJHdyLsZwq9ocRBXrrMHRemq8",
        "locationConfidence" : 1.5602307
      }, {
        "latitudeE7" : 448798833,
        "longitudeE7" : -930331961,
        "placeId" : "ChIJA-tu9vPT94cRspMsDTCbFm8",
        "locationConfidence" : 1.2346979
      }, {
        "latitudeE7" : 448750360,
        "longitudeE7" : -930293711,
        "placeId" : "ChIJc59Uz-_T94cRqrXy3qRfZ8E",
        "locationConfidence" : 1.1740266
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 448770783,
        "longitudeE7" : -930314019
      },
      "endLocation" : {
        "latitudeE7" : 449177675,
        "longitudeE7" : -932623113
      },
      "duration" : {
        "startTimestampMs" : "1583168331999",
        "endTimestampMs" : "158317439.5000"
      },
      "distance" : 21496,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "HIGH",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 79.39.133048057556
      }, {
        "activityType" : "STILL",
        "probability" : 19.46731060743332
      }, {
        "activityType" : "WALKING",
        "probability" : 0.44584739.953279495
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 448770523,
        -9303139.49
        }, {
      : 448906707,
        -9318339.53
        }, {
      : 449099006,
        -932228622
        }, {
      : 449058303,
        -932228851
        }, {
      : 449035720,
        -932216339.
        }, {
      : 449012832,
        -932475204
        }, {
      : 4490139.77,
        -932504272
        }, {
      : 449108123,
        -932626495
        }, {
      : 449179077,
        -932623138
        } ]
      },
      "simplifiedRawPath" : {
        "points" : [ {
      : 449099808,
        -932229080,
          "timestampMs" : "1583170680000",
          "accuracyMeters" : 10
        }, {
      : 449035797,
        -932216949,
          "timestampMs" : "15831738239.98",
          "accuracyMeters" : 5
        }, {
      : 449014320,
        -9325039.67,
          "timestampMs" : "1583174078000",
          "accuracyMeters" : 5
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583174809012",
        "location" : {
          "latitudeE7" : 449187802,
          "longitudeE7" : -932625964,
          "accuracyMetres" : 70
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 449177622,
        "longitudeE7" : -932622469,
        "placeId" : "ChIJ7cgUk9Qn9ocRSn1wMJWdi9U",
        "address" : "4701 Chicago Ave\nMinneapolis, MN 55407\nUSA",
        "name" : "Wings Financial Credit Union",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 91.68037
      },
      "duration" : {
        "startTimestampMs" : "158317439.5000",
        "endTimestampMs" : "1583174809012"
      },
      "placeConfidence" : "MEDIUM_CONFIDENCE",
      "centerLatE7" : 449182700,
      "centerLngE7" : -932624500,
      "visitConfidence" : 92,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 449173847,
        "longitudeE7" : -932630629,
        "placeId" : "ChIJaVkHl9Qn9ocRxrF0IViuH1c",
        "locationConfidence" : 3.366558
      }, {
        "latitudeE7" : 449184030,
        "longitudeE7" : -932623310,
        "placeId" : "ChIJZ_SkZdQn9ocR51RZBPYUnPI",
        "locationConfidence" : 2.2931292
      }, {
        "latitudeE7" : 449180859,
        "longitudeE7" : -932620952,
        "placeId" : "ChIJAQDQ8tQn9ocRzc4brrytvnU",
        "locationConfidence" : 1.9436249
      }, {
        "latitudeE7" : 449159667,
        "longitudeE7" : -932620738,
        "placeId" : "ChIJXXueNSsm9ocRC4dtUK5E5PE",
        "locationConfidence" : 0.20904137
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 449187802,
        "longitudeE7" : -932625964
      },
      "endLocation" : {
        "latitudeE7" : 448985315,
        "longitudeE7" : -932180880
      },
      "duration" : {
        "startTimestampMs" : "1583174809012",
        "endTimestampMs" : "1583175598038"
      },
      "distance" : 6144,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "HIGH",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 91.49948358535767
      }, {
        "activityType" : "STILL",
        "probability" : 7.157854735851288
      }, {
        "activityType" : "WALKING",
        "probability" : 0.8552023209631443
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 449187812,
        -932626037
        }, {
      : 449197120,
        -932680053
        }, {
      : 449197120,
        -932683105
        }, {
      : 448906364,
        -932646484
        }, {
      : 448985328,
        -932180862
        } ]
      },
      "simplifiedRawPath" : {
        "points" : [ {
      : 449197807,
        -932683105,
          "timestampMs" : "1583174933016",
          "accuracyMeters" : 10
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583175598038",
        "location" : {
          "latitudeE7" : 448985315,
          "longitudeE7" : -932180880,
          "accuracyMetres" : 65
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 449008044,
        "longitudeE7" : -932175785,
        "placeId" : "ChIJD5ro0R8p9ocRFoWZX94ufys",
        "address" : "5629 38th Ave S\nMinneapolis, MN 55417\nUSA",
        "name" : "5629 38th Ave S",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 66.09524
      },
      "duration" : {
        "startTimestampMs" : "1583175598038",
        "endTimestampMs" : "1583180836999"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 448987250,
      "centerLngE7" : -932178550,
      "visitConfidence" : 94,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 448847554,
        "longitudeE7" : -932222846,
        "placeId" : "ChIJB2rAhSov9ocRkTV4eHzT0ys",
        "locationConfidence" : 33.858852
      }, {
        "latitudeE7" : 449009310,
        "longitudeE7" : -932174729,
        "placeId" : "ChIJKSPtzR8p9ocR71FIbVCYChc",
        "locationConfidence" : 0.014420289
      }, {
        "latitudeE7" : 448992361,
        "longitudeE7" : -932162831,
        "placeId" : "ChIJHf97OZ0p9ocRb0q3f2LNFwA",
        "locationConfidence" : 0.007727661
      }, {
        "latitudeE7" : 448985954,
        "longitudeE7" : -932154552,
        "placeId" : "ChIJ52OMSwsp9ocRCwZHwYxxob0",
        "locationConfidence" : 0.0070685735
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 448989296,
        "longitudeE7" : -932176304
      },
      "endLocation" : {
        "latitudeE7" : 448824157,
        "longitudeE7" : -932114294
      },
      "duration" : {
        "startTimestampMs" : "1583180836999",
        "endTimestampMs" : "1583181470001"
      },
      "distance" : 2109,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "HIGH",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 88.48262429237366
      }, {
        "activityType" : "STILL",
        "probability" : 5.2993454039.09683
      }, {
        "activityType" : "WALKING",
        "probability" : 4.256321489810944
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 448989295,
        -932178497
        }, {
      : 448984642,
        -932064819
        }, {
      : 448824043,
        -932114181
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583181645218",
        "location" : {
          "latitudeE7" : 448824578,
          "longitudeE7" : -932122809,
          "accuracyMetres" : 63
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 448847554,
        "longitudeE7" : -932222846,
        "placeId" : "ChIJB2rAhSov9ocRkTV4eHzT0ys",
        "address" : "Minnesota\nUSA",
        "name" : "Minneapolis−Saint Paul International Airport",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 82.77725
      },
      "duration" : {
        "startTimestampMs" : "1583181470001",
        "endTimestampMs" : "1583189259721"
      },
      "placeConfidence" : "MEDIUM_CONFIDENCE",
      "centerLatE7" : 4488539.14,
      "centerLngE7" : -932119429,
      "visitConfidence" : 84,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 448834433,
        "longitudeE7" : -932114135,
        "placeId" : "ChIJqa-Cpi0p9ocRLu72YYTorlc",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 17.199734
      }, {
        "latitudeE7" : 448810818,
        "longitudeE7" : -932059269,
        "placeId" : "ChIJ2WzpLTMp9ocRwSQE35a_PVw",
        "locationConfidence" : 0.021075832
      }, {
        "latitudeE7" : 448820322,
        "longitudeE7" : -932056052,
        "placeId" : "ChIJYWUkmJYp9ocRDrbUXaieGCk",
        "locationConfidence" : 0.0017149381
      }, {
        "latitudeE7" : 447214681,
        "longitudeE7" : -948056498,
        "placeId" : "ChIJN1RR688D9YcRrfJtVYoNYPg",
        "locationConfidence" : 2.2149908E-4
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED",
      "simplifiedRawPath" : {
        "points" : [ {
      : 448823039.,
        -932118492,
          "timestampMs" : "1583181789000",
          "accuracyMeters" : 25
        }, {
      : 448845254,
        -932112283,
          "timestampMs" : "1583182119116",
          "accuracyMeters" : 6
        }, {
      : 448836053,
        -932119338,
          "timestampMs" : "1583182308110",
          "accuracyMeters" : 6
        }, {
      : 448855411,
        -932120703,
          "timestampMs" : "1583188331444",
          "accuracyMeters" : 65
        }, {
      : 448855411,
        -932120703,
          "timestampMs" : "1583188646576",
          "accuracyMeters" : 65
        }, {
      : 448853522,
        -932113580,
          "timestampMs" : "1583188944589",
          "accuracyMeters" : 65
        }, {
      : 448855411,
        -932120703,
          "timestampMs" : "1583189130313",
          "accuracyMeters" : 65
        } ]
      }
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 448853522,
        "longitudeE7" : -932113580
      },
      "endLocation" : {
        "latitudeE7" : 39.8488837,
        "longitudeE7" : -10.467539.81
      },
      "duration" : {
        "startTimestampMs" : "1583189259721",
        "endTimestampMs" : "1583197438001"
      },
      "distance" : 1096077,
      "activityType" : "FLYING",
      "confidence" : "MEDIUM",
      "activities" : [ {
        "activityType" : "FLYING",
        "probability" : 70.72411775588989
      }, {
        "activityType" : "WALKING",
        "probability" : 11.94992139.9354935
      }, {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 7.532184571027756
      } ],
      "simplifiedRawPath" : {
        "points" : [ {
      : 448857849,
        -932222978,
          "timestampMs" : "1583189378000",
          "accuracyMeters" : 5
        }, {
      : 448853522,
        -932113580,
          "timestampMs" : "1583189743458",
          "accuracyMeters" : 65
        }, {
      : 448857849,
        -932222978,
          "timestampMs" : "1583190176869",
          "accuracyMeters" : 5
        } ]
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 39.8560963,
        "longitudeE7" : -10.46737376,
        "placeId" : "ChIJ_0T_mCp_bIcRapy1NbQ7WEk",
        "address" : "8500 Peña Blvd\nDenver, CO 80249\nUSA",
        "name" : "Denver International Airport",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 92.007904
      },
      "duration" : {
        "startTimestampMs" : "1583197438001",
        "endTimestampMs" : "1583199312000"
      },
      "placeConfidence" : "MEDIUM_CONFIDENCE",
      "centerLatE7" : 39.8493750,
      "centerLngE7" : -10.46753200,
      "visitConfidence" : 93,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 39.8487935,
        "longitudeE7" : -10.46728573,
        "placeId" : "ChIJn9i5m-9nbIcRvEmOgDbYD0A",
        "locationConfidence" : 6.235767
      }, {
        "latitudeE7" : 39.8474721,
        "longitudeE7" : -10.46738532,
        "placeId" : "ChIJ5cqyBe9nbIcRh31xfGKPJFA",
        "locationConfidence" : 1.4114263
      }, {
        "latitudeE7" : 39.8497980,
        "longitudeE7" : -10.46751910,
        "placeId" : "ChIJcX9-8eVnbIcR_ciaLYyo3KE",
        "locationConfidence" : 0.3215075
      }, {
        "latitudeE7" : 39.8471757,
        "longitudeE7" : -10.46738596,
        "placeId" : "ChIJ_f-tA-9nbIcROYKpymOf8DE",
        "locationConfidence" : 0.0064228186
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 39.8498765,
        "longitudeE7" : -10.46752587
      },
      "endLocation" : {
        "latitudeE7" : 39.7718936,
        "longitudeE7" : -10.48004070
      },
      "duration" : {
        "startTimestampMs" : "1583199312000",
        "endTimestampMs" : "1583200085000"
      },
      "distance" : 13769,
      "activityType" : "FLYING",
      "confidence" : "MEDIUM",
      "activities" : [ {
        "activityType" : "FLYING",
        "probability" : 67.7230954170227
      }, {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 17.558684945106506
      }, {
        "activityType" : "IN_BUS",
        "probability" : 5.878940597176552
      } ],
      "simplifiedRawPath" : {
        "points" : [ {
      : 39.7763749,
        -10.47915624,
          "timestampMs" : "1583199954000",
          "accuracyMeters" : 10
        } ]
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 39.7722020,
        "longitudeE7" : -10.48008530,
        "placeId" : "ChIJWbyE1YdkbIcRAKlXVOuKkKY",
        "address" : "16001 E 40th Cir\nAurora, CO 80011\nUSA",
        "name" : "Cambria Hotel Denver International Airport",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 96.9513
      },
      "duration" : {
        "startTimestampMs" : "1583200085000",
        "endTimestampMs" : "1583201198452"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 39.7721667,
      "centerLngE7" : -10.48007767,
      "visitConfidence" : 95,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 39.7723897,
        "longitudeE7" : -10.47994137,
        "placeId" : "ChIJ310Z5YdkbIcRTjE5zjk-3Z0",
        "locationConfidence" : 1.3868722
      }, {
        "latitudeE7" : 39.7721563,
        "longitudeE7" : -10.48010191,
        "placeId" : "ChIJg_uiL4ZkbIcRvver4atQ4L4",
        "locationConfidence" : 0.23244601
      }, {
        "latitudeE7" : 39.7723700,
        "longitudeE7" : -10.47969630,
        "placeId" : "ChIJ8XTFOX1kbIcRd6GJGtBm_5w",
        "locationConfidence" : 0.22222297
      }, {
        "latitudeE7" : 39.7719690,
        "longitudeE7" : -10.48023530,
        "placeId" : "ChIJp37GMYZkbIcRcTNTNX23Mss",
        "locationConfidence" : 0.21479933
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 39.7723604,
        "longitudeE7" : -10.48010704
      },
      "endLocation" : {
        "latitudeE7" : 449031208,
        "longitudeE7" : -932171792
      },
      "duration" : {
        "startTimestampMs" : "1583201198452",
        "endTimestampMs" : "1583204200999"
      },
      "distance" : 1111199,
      "activityType" : "FLYING",
      "confidence" : "LOW",
      "activities" : [ {
        "activityType" : "FLYING",
        "probability" : 35.561615228652954
      }, {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 32.285323739.05182
      }, {
        "activityType" : "STILL",
        "probability" : 14.403729140758514
      } ],
      "simplifiedRawPath" : {
        "points" : [ {
      : 449120512,
        -932230725,
          "timestampMs" : "1583203447117",
          "accuracyMeters" : 12
        }, {
      : 449140688,
        -932228297,
          "timestampMs" : "1583203508999",
          "accuracyMeters" : 4
        }, {
      : 449162656,
        -932162200,
          "timestampMs" : "1583203578999",
          "accuracyMeters" : 4
        }, {
      : 449176126,
        -932160777,
          "timestampMs" : "1583203658999",
          "accuracyMeters" : 6
        }, {
      : 449166999,
        -932133188,
          "timestampMs" : "15832039.44999",
          "accuracyMeters" : 4
        }, {
      : 449099875,
        -932177492,
          "timestampMs" : "1583204075999",
          "accuracyMeters" : 4
        } ]
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 449026654,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJn40NGh4p9ocRomjhS3xb_MM",
        "address" : "5529 38th Ave S\nMinneapolis, MN 55417\nUSA",
        "name" : "5529 38th Ave S",
        "sourceInfo" : {
          "deviceTag" : -2093848546
        },
        "locationConfidence" : 97.957375
      },
      "duration" : {
        "startTimestampMs" : "1583204200999",
        "endTimestampMs" : "1583205074427"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 449029100,
      "centerLngE7" : -932173700,
      "visitConfidence" : 87,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 449021465,
        "longitudeE7" : -932171866,
        "placeId" : "ChIJ7wdfPh4p9ocRlQhY9AwpFwk",
        "locationConfidence" : 0.7400563
      }, {
        "latitudeE7" : 449027748,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJpQyEGh4p9ocRfZ8hfqyGpeI",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.47161132
      }, {
        "latitudeE7" : 449055365,
        "longitudeE7" : -932174700,
        "placeId" : "ChIJpS6cnB0p9ocRo6jVi3DIi2I",
        "locationConfidence" : 0.18063708
      }, {
        "latitudeE7" : 449027737,
        "longitudeE7" : -932159438,
        "placeId" : "ChIJ3ZDiYx4p9ocR-z5up0-vsRk",
        "locationConfidence" : 0.16962099
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 39.7722020,
        "longitudeE7" : -10.48008530,
        "placeId" : "ChIJWbyE1YdkbIcRAKlXVOuKkKY",
        "address" : "16001 E 40th Cir\nAurora, CO 80011\nUSA",
        "name" : "Cambria Hotel Denver International Airport",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 58.484913
      },
      "duration" : {
        "startTimestampMs" : "1583205074427", Monday, March 2, 2020 10:11:14.427 PM 
        "endTimestampMs" : "1583249978583"
      },
      "placeConfidence" : "MEDIUM_CONFIDENCE",
      "centerLatE7" : 39.7723650,
      "centerLngE7" : -10.48000450,
      "visitConfidence" : 61,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 39.7732721,
        "longitudeE7" : -10.47987375,
        "placeId" : "ChIJLz7CAYhkbIcRbVr62MsyHuk",
        "locationConfidence" : 19.53162
      }, {
        "latitudeE7" : 39.7734441,
        "longitudeE7" : -10.47988206,
        "placeId" : "ChIJLz7CAYhkbIcR-BgaKWwUb4k",
        "locationConfidence" : 13.232319
      }, {
        "latitudeE7" : 39.7723897,
        "longitudeE7" : -10.47994137,
        "placeId" : "ChIJ310Z5YdkbIcRTjE5zjk-3Z0",
        "locationConfidence" : 5.06939.84
      }, {
        "latitudeE7" : 39.7723565,
        "longitudeE7" : -10.47996458,
        "placeId" : "ChIJ310Z5YdkbIcR7Kts-0x0kqQ",
        "locationConfidence" : 1.7922282
      }, {
        "latitudeE7" : 39.7723700,
        "longitudeE7" : -10.47969630,
        "placeId" : "ChIJ8XTFOX1kbIcRd6GJGtBm_5w",
        "locationConfidence" : 0.6683299
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 39.7708590,
        "longitudeE7" : -10.48225860,
        "placeId" : "ChIJP0dGXL1kbIcRS4A4spcPa58",
        "address" : "13800 E 39.th Ave\nAurora, CO 80011\nUSA",
        "name" : "Staples Fulfillment Center",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 94.89853
      },
      "duration" : {
        "startTimestampMs" : "1583249978583",
        "endTimestampMs" : "1583270635847"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 39.7714500,
      "centerLngE7" : -10.48227850,
      "visitConfidence" : 92,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 39.7702353,
        "longitudeE7" : -10.48235359,
        "placeId" : "ChIJt7UhtJhkbIcRC4F8U6nb74I",
        "locationConfidence" : 1.9754865
      }, {
        "latitudeE7" : 39.7707287,
        "longitudeE7" : -10.48196966,
        "placeId" : "ChIJy162jpdkbIcRsDEUfnR7l2U",
        "locationConfidence" : 0.48900402
      }, {
        "latitudeE7" : 39.7708590,
        "longitudeE7" : -10.48225860,
        "placeId" : "ChIJP0dGXL1kbIcRE0yQjg-enZ8",
        "locationConfidence" : 0.4172884
      }, {
        "latitudeE7" : 39.7646780,
        "longitudeE7" : -10.48121400,
        "placeId" : "ChIJY8yl65xkbIcRXvlD_NdUY1k",
        "locationConfidence" : 0.38986465
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 39.7715107,
        "longitudeE7" : -10.48228641
      },
      "endLocation" : {
        "latitudeE7" : 448493507,
        "longitudeE7" : -932885508
      },
      "duration" : {
        "startTimestampMs" : "1583270635847",
        "endTimestampMs" : "1583277077999"
      },
      "distance" : 1102251,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "MEDIUM",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 74.30844902992249
      }, {
        "activityType" : "STILL",
        "probability" : 12.486502528190613
      }, {
        "activityType" : "FLYING",
        "probability" : 8.06034430861473
      } ],
      "simplifiedRawPath" : {
        "points" : [ {
      : 449036123,
        -932176985,
          "timestampMs" : "1583276187999",
          "accuracyMeters" : 4
        }, {
      : 449008727,
        -932179002,
          "timestampMs" : "1583276337998",
          "accuracyMeters" : 6
        }, {
      : 448981653,
        -932223445,
          "timestampMs" : "1583276407998",
          "accuracyMeters" : 4
        }, {
      : 448976461,
        -932348595,
          "timestampMs" : "1583276487997",
          "accuracyMeters" : 8
        }, {
      : 448967163,
        -932420560,
          "timestampMs" : "1583276557999",
          "accuracyMeters" : 8
        }, {
      : 448551566,
        -932954011,
          "timestampMs" : "1583276978000",
          "accuracyMeters" : 6
        }, {
      : 448551699,
        -932906454,
          "timestampMs" : "15832770039.99",
          "accuracyMeters" : 8
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583277107999",
        "location" : {
          "latitudeE7" : 448491430,
          "longitudeE7" : -932880137,
          "accuracyMetres" : 66
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 448493602,
        "longitudeE7" : -932878283,
        "placeId" : "ChIJXWCOYaUl9ocRg4_DxxaCvcM",
        "address" : "8563 Lyndale Ave S\nBloomington, MN 55420\nUSA",
        "name" : "Smokeless - Vape and CBD",
        "sourceInfo" : {
          "deviceTag" : -2093848546
        },
        "locationConfidence" : 96.52365
      },
      "duration" : {
        "startTimestampMs" : "1583277077999",
        "endTimestampMs" : "1583277478999"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 448499200,
      "centerLngE7" : -932884500,
      "visitConfidence" : 90,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 448513400,
        "longitudeE7" : -932868490,
        "placeId" : "ChIJma30nrol9ocR1PgWo61tJ4U",
        "locationConfidence" : 1.1082052
      }, {
        "latitudeE7" : 448506606,
        "longitudeE7" : -932851141,
        "placeId" : "ChIJGbbRMLsl9ocRZTZQyjs-WTk",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.70742744
      }, {
        "latitudeE7" : 448505191,
        "longitudeE7" : -932854418,
        "placeId" : "ChIJuWj1Orsl9ocR71nZbhMfMDA",
        "locationConfidence" : 0.66639.61
      }, {
        "latitudeE7" : 448495200,
        "longitudeE7" : -932878120,
        "placeId" : "ChIJn0ALn7ol9ocR1Kzf3WMM7DM",
        "locationConfidence" : 0.30837256
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 448504949,
        "longitudeE7" : -932883568
      },
      "endLocation" : {
        "latitudeE7" : 39.7723388,
        "longitudeE7" : -10.48007857
      },
      "duration" : {
        "startTimestampMs" : "1583277478999",
        "endTimestampMs" : "1583279445000"
      },
      "distance" : 1100717,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "MEDIUM",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 76.92668437957764
      }, {
        "activityType" : "STILL",
        "probability" : 10.110724717378616
      }, {
        "activityType" : "WALKING",
        "probability" : 5.620976164937019
      } ],
      "simplifiedRawPath" : {
        "points" : [ {
      : 448617061,
        -932853419,
          "timestampMs" : "1583277610999",
          "accuracyMeters" : 6
        }, {
      : 448619976,
        -932692301,
          "timestampMs" : "1583277879000",
          "accuracyMeters" : 6
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583280008002",
        "location" : {
          "latitudeE7" : 39.7723497,
          "longitudeE7" : -10.48010485,
          "accuracyMetres" : 70
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 39.7722020,
        "longitudeE7" : -10.48008530,
        "placeId" : "ChIJWbyE1YdkbIcRAKlXVOuKkKY",
        "address" : "16001 E 40th Cir\nAurora, CO 80011\nUSA",
        "name" : "Cambria Hotel Denver International Airport",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 94.921646
      },
      "duration" : {
        "startTimestampMs" : "1583279445000",
        "endTimestampMs" : "1583285903000"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 39.7723740,
      "centerLngE7" : -10.48008800,
      "visitConfidence" : 76,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 39.7735233,
        "longitudeE7" : -10.47989177,
        "placeId" : "ChIJLz7CAYhkbIcRCvaIzoTKHB0",
        "locationConfidence" : 1.9213562
      }, {
        "latitudeE7" : 39.7732721,
        "longitudeE7" : -10.47987375,
        "placeId" : "ChIJLz7CAYhkbIcRbVr62MsyHuk",
        "locationConfidence" : 1.6807711
      }, {
        "latitudeE7" : 39.7734441,
        "longitudeE7" : -10.47988206,
        "placeId" : "ChIJLz7CAYhkbIcR-BgaKWwUb4k",
        "locationConfidence" : 0.44695833
      }, {
        "latitudeE7" : 39.7723897,
        "longitudeE7" : -10.47994137,
        "placeId" : "ChIJ310Z5YdkbIcRTjE5zjk-3Z0",
        "locationConfidence" : 0.34040952
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 39.7732721,
        "longitudeE7" : -10.47987375,
        "placeId" : "ChIJLz7CAYhkbIcRbVr62MsyHuk",
        "address" : "16221 E 40th Ave\nDenver, CO 80239.\nUSA",
        "name" : "Urban Sombrero",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 43.11191
      },
      "duration" : {
        "startTimestampMs" : "1583285903000",Tuesday, March 3, 2020 6:38:23 PM
        "endTimestampMs" : "1583291826409"
      },
      "placeConfidence" : "MEDIUM_CONFIDENCE",
      "centerLatE7" : 39.7729033,
      "centerLngE7" : -10.47979683,
      "visitConfidence" : 76,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 39.7732875,
        "longitudeE7" : -10.47975856,
        "placeId" : "ChIJ3e65tGJkbIcRFnJG3lvyCww",
        "locationConfidence" : 30.679424
      }, {
        "latitudeE7" : 39.7735233,
        "longitudeE7" : -10.47989177,
        "placeId" : "ChIJLz7CAYhkbIcRCvaIzoTKHB0",
        "locationConfidence" : 6.555493
      }, {
        "latitudeE7" : 39.7722020,
        "longitudeE7" : -10.48008530,
        "placeId" : "ChIJWbyE1YdkbIcRAKlXVOuKkKY",
        "locationConfidence" : 5.9069777
      }, {
        "latitudeE7" : 39.7723700,
        "longitudeE7" : -10.47969630,
        "placeId" : "ChIJ8XTFOX1kbIcRd6GJGtBm_5w",
        "locationConfidence" : 5.1866827
      }, {
        "latitudeE7" : 39.7734441,
        "longitudeE7" : -10.47988206,
        "placeId" : "ChIJLz7CAYhkbIcR-BgaKWwUb4k",
        "locationConfidence" : 5.1376877
      }, {
        "latitudeE7" : 39.7722425,
        "longitudeE7" : -10.47982508,
        "placeId" : "ChIJVwCcU31kbIcRzGVWlv7znfs",
        "locationConfidence" : 1.7842844
      }, {
        "latitudeE7" : 39.7733432,
        "longitudeE7" : -10.47988140,
        "placeId" : "ChIJLz7CAYhkbIcR2g9lIEY1jEw",
        "locationConfidence" : 0.4742211
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 39.7728011,
        "longitudeE7" : -10.48010240
      },
      "endLocation" : {
        "latitudeE7" : 449041013,
        "longitudeE7" : -932169474
      },
      "duration" : {
        "startTimestampMs" : "1583291826409",
        "endTimestampMs" : "1583303665999"
      },
      "distance" : 1108418,
      "activityType" : "FLYING",
      "confidence" : "LOW",
      "activities" : [ {
        "activityType" : "FLYING",
        "probability" : 48.843276500701904
      }, {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 32.866719365119934
      }, {
        "activityType" : "WALKING",
        "probability" : 7.178911566734314
      } ]
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 39.7722020,
        "longitudeE7" : -10.48008530,
        "placeId" : "ChIJWbyE1YdkbIcRAKlXVOuKkKY",
        "address" : "16001 E 40th Cir\nAurora, CO 80011\nUSA",
        "name" : "Cambria Hotel Denver International Airport",
        "sourceInfo" : {
          "deviceTag" : -2093848546
        },
        "locationConfidence" : 95.66597
      },
      "duration" : {
        "startTimestampMs" : "1583303665999", Wednesday, March 4, 2020 11:34:25.999 PM
        "endTimestampMs" : "1583333293000"Wednesday, March 4, 2020 7:48:13 AM
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 39.7716090,
      "centerLngE7" : -10.48011338,
      "visitConfidence" : 70,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 39.7719690,
        "longitudeE7" : -10.48023530,
        "placeId" : "ChIJp37GMYZkbIcRcTNTNX23Mss",
        "locationConfidence" : 1.4409783
      }, {
        "latitudeE7" : 39.7732721,
        "longitudeE7" : -10.47987375,
        "placeId" : "ChIJLz7CAYhkbIcRbVr62MsyHuk",
        "locationConfidence" : 0.83844745
      }, {
        "latitudeE7" : 39.7735233,
        "longitudeE7" : -10.47989177,
        "placeId" : "ChIJLz7CAYhkbIcRCvaIzoTKHB0",
        "locationConfidence" : 0.73320425
      }, {
        "latitudeE7" : 39.7734441,
        "longitudeE7" : -10.47988206,
        "placeId" : "ChIJLz7CAYhkbIcR-BgaKWwUb4k",
        "locationConfidence" : 0.43236542
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 39.7716090,
        "longitudeE7" : -10.48011338
      },
      "endLocation" : {
        "latitudeE7" : 39.7712613,
        "longitudeE7" : -10.48224925
      },
      "duration" : {
        "startTimestampMs" : "1583333293000",Wednesday, March 4, 2020 7:48:13 AM
        "endTimestampMs" : "1583333590002" Wednesday, March 4, 2020 7:53:10.002 AM 
      },
      "distance" : 1883,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "MEDIUM",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 71.24656438827515
      }, {
        "activityType" : "STILL",
        "probability" : 14.401443302631378
      }, {
        "activityType" : "IN_FERRY",
        "probability" : 5.359182506799698
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 39.7729225,
        -10.48043365
        }, {
      : 39.7697792,
        -10.48099822
        }, {
      : 39.7713584,
        -10.48225708
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583333590002",Wednesday, March 4, 2020 7:53:10.002 AM
        "location" : {
          "latitudeE7" : 39.7712613,
          "longitudeE7" : -10.48224925,
          "accuracyMetres" : 65
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 39.7708590,
        "longitudeE7" : -10.48225860,
        "placeId" : "ChIJP0dGXL1kbIcRS4A4spcPa58",
        "address" : "13800 E 39.th Ave\nAurora, CO 80011\nUSA",
        "name" : "Staples Fulfillment Center",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 95.90224
      },
      "duration" : {
        "startTimestampMs" : "1583333590002",Wednesday, March 4, 2020 7:53:10.002 AM 
        "endTimestampMs" : "1583345736004" Wednesday, March 4, 2020 11:15:36.004 PM
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 39.7713067,
      "centerLngE7" : -10.48225533,
      "visitConfidence" : 93,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 39.7702353,
        "longitudeE7" : -10.48235359,
        "placeId" : "ChIJt7UhtJhkbIcRC4F8U6nb74I",
        "locationConfidence" : 1.239.3012
      }, {
        "latitudeE7" : 39.7708590,
        "longitudeE7" : -10.48225860,
        "placeId" : "ChIJP0dGXL1kbIcRE0yQjg-enZ8",
        "locationConfidence" : 0.8657144
      }, {
        "latitudeE7" : 39.7707287,
        "longitudeE7" : -10.48196966,
        "placeId" : "ChIJy162jpdkbIcRsDEUfnR7l2U",
        "locationConfidence" : 0.5177197
      }, {
        "latitudeE7" : 39.7694669,
        "longitudeE7" : -10.48213655,
        "placeId" : "ChIJgWmbF5hkbIcRDblfuvFpQ2k",
        "locationConfidence" : 0.3438853
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 39.7712748,
        "longitudeE7" : -10.48224970
      },
      "endLocation" : {
        "latitudeE7" : 39.7721295,
        "longitudeE7" : -10.48006900
      },
      "duration" : {
        "startTimestampMs" : "1583345736004",Wednesday, March 4, 2020 11:15:36.004 PM 
        "endTimestampMs" : "1583365081000"Wednesday, March 4, 2020 4:38:01 PM
      },
      "distance" : 1109917,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "LOW",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 45.94147205352783
      }, {
        "activityType" : "FLYING",
        "probability" : 36.89465820789337
      }, {
        "activityType" : "IN_FERRY",
        "probability" : 8.59573781490326
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 39.7713584,
        -10.48225631
        }, {
      : 39.7694587,
        -10.48097839.
        }, {
      : 39.7719421,
        -10.48006210
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583365523431", Wednesday, March 4, 2020 4:45:23.431 PM
        "location" : {
          "latitudeE7" : 39.7722993,
          "longitudeE7" : -10.4800839.6,
          "accuracyMetres" : 125
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 39.7722020,
        "longitudeE7" : -10.48008530,
        "placeId" : "ChIJWbyE1YdkbIcRAKlXVOuKkKY",
        "address" : "16001 E 40th Cir\nAurora, CO 80011\nUSA",
        "name" : "Cambria Hotel Denver International Airport",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 92.77188
      },
      "duration" : {
        "startTimestampMs" : "1583365081000",Wednesday, March 4, 2020 4:38:01 PM
        "endTimestampMs" : "1583367012695"Wednesday, March 4, 2020 6:10:12.695 PM
      },
      "placeConfidence" : "MEDIUM_CONFIDENCE",
      "centerLatE7" : 39.7722680,
      "centerLngE7" : -10.48007720,
      "visitConfidence" : 81,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 39.7735233,
        "longitudeE7" : -10.47989177,
        "placeId" : "ChIJLz7CAYhkbIcRCvaIzoTKHB0",
        "locationConfidence" : 2.2704048
      }, {
        "latitudeE7" : 39.7732721,
        "longitudeE7" : -10.47987375,
        "placeId" : "ChIJLz7CAYhkbIcRbVr62MsyHuk",
        "locationConfidence" : 1.9450321
      }, {
        "latitudeE7" : 39.7734441,
        "longitudeE7" : -10.47988206,
        "placeId" : "ChIJLz7CAYhkbIcR-BgaKWwUb4k",
        "locationConfidence" : 1.5529244
      }, {
        "latitudeE7" : 39.7723897,
        "longitudeE7" : -10.47994137,
        "placeId" : "ChIJ310Z5YdkbIcRTjE5zjk-3Z0",
        "locationConfidence" : 0.59983885
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 39.7722720,
        "longitudeE7" : -10.48007817
      },
      "endLocation" : {
        "latitudeE7" : 39.7725518,
        "longitudeE7" : -10.48008913
      },
      "duration" : {
        "startTimestampMs" : "1583367012695",Wednesday, March 4, 2020 5:10:12.695 PM
        "endTimestampMs" : "1583403470002"Thursday, March 5, 2020 3:17:50.002 AM
      },
      "distance" : 263,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "LOW",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 53.969788551330566
      }, {
        "activityType" : "STILL",
        "probability" : 29.342785477638245
      }, {
        "activityType" : "WALKING",
        "probability" : 11.575020849704742
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 39.7724609,-10..48007812
      : 39.7724609,-10.48008346
        }, {
      : 39.7724609, -10.48008880
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583403470002",
        "location" : {
          "latitudeE7" : 39.7725518,
          "longitudeE7" : -10.48008913,
          "accuracyMetres" : 90
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 39.7722333,
        "longitudeE7" : -10.48074056,
        "placeId" : "ChIJLS0fioVkbIcRr6S_FbfHRtQ",
        "address" : "15500 E 40th Ave\nDenver, CO 80239.\nUSA",
        "name" : "Crowne Plaza Denver Airport Convention Ctr, an IHG Hotel",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 74.259796
      },
      "duration" : {
        "startTimestampMs" : "1583403470002",
        "endTimestampMs" : "1583419668007"Thursday, March 5, 2020 7:47:48.007 AM
      },
      "placeConfidence" : "MEDIUM_CONFIDENCE",
      "centerLatE7" : 39.7731387,
      "centerLngE7" : -10.48058892,
      "visitConfidence" : 68,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 39.7734878,
        "longitudeE7" : -10.480639.20,
        "placeId" : "ChIJx34z0o1kbIcRpijDHYesdTI",
        "locationConfidence" : 14.552051
      }, {
        "latitudeE7" : 39.7736759,
        "longitudeE7" : -10.48090044,
        "placeId" : "ChIJu-QHt49kbIcRKWcz3aYSiMQ",
        "locationConfidence" : 3.4485993
      }, {
        "latitudeE7" : 39.77439.30,
        "longitudeE7" : -10.48041078,
        "placeId" : "ChIJRQpH0IhkbIcRtaSG4om8kbk",
        "locationConfidence" : 2.4740083
      }, {
        "latitudeE7" : 39.7745207,
        "longitudeE7" : -10.48091532,
        "placeId" : "ChIJFVlSNo5kbIcRrJNeQeTaxoY",
        "locationConfidence" : 1.4569502
      }, {
        "latitudeE7" : 39.7719690,
        "longitudeE7" : -10.48023530,
        "placeId" : "ChIJp37GMYZkbIcRcTNTNX23Mss",
        "locationConfidence" : 1.4220718
      }, {
        "latitudeE7" : 39.7730320,
        "longitudeE7" : -10.48083180,
        "placeId" : "ChIJd0Y7vY9kbIcRb-AH1Y4QLPA",
        "locationConfidence" : 0.7729813
      }, {
        "latitudeE7" : 39.7732949,
        "longitudeE7" : -10.48076162,
        "placeId" : "ChIJZVihoI9kbIcRrj1BMMEkKq8",
        "locationConfidence" : 0.45634872
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 39.7731387,
        "longitudeE7" : -10.48058892
      },
      "endLocation" : {
        "latitudeE7" : 39.7714144,
        "longitudeE7" : -10.48216494
      },
      "duration" : {
        "startTimestampMs" : "1583419668007",
        "endTimestampMs" : "1583419963000"
      },
      "distance" : 1473,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "HIGH",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 91.87384843826294
      }, {
        "activityType" : "STILL",
        "probability" : 3.2795168459415436
      }, {
        "activityType" : "WALKING",
        "probability" : 2.4239.884689450264
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 39.7730827,
        -10.48059005
        }, {
      : 39.7697792,
        -10.48099822
        }, {
      : 39.7714729,
        -10.48216400
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583420177001",
        "location" : {
          "latitudeE7" : 39.7712429,
          "longitudeE7" : -10.48224182,
          "accuracyMetres" : 92
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 39.7708590,
        "longitudeE7" : -10.48225860,
        "placeId" : "ChIJP0dGXL1kbIcRS4A4spcPa58",
        "address" : "13800 E 39.th Ave\nAurora, CO 80011\nUSA",
        "name" : "Staples Fulfillment Center",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 95.91718
      },
      "duration" : {
        "startTimestampMs" : "1583419963000",
        "endTimestampMs" : "1583437049709"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 39.7712750,
      "centerLngE7" : -10.48222650,
      "visitConfidence" : 81,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 39.7702353,
        "longitudeE7" : -10.48235359,
        "placeId" : "ChIJt7UhtJhkbIcRC4F8U6nb74I",
        "locationConfidence" : 1.0630225
      }, {
        "latitudeE7" : 39.7708590,
        "longitudeE7" : -10.48225860,
        "placeId" : "ChIJP0dGXL1kbIcRE0yQjg-enZ8",
        "locationConfidence" : 0.9303632
      }, {
        "latitudeE7" : 39.7707287,
        "longitudeE7" : -10.48196966,
        "placeId" : "ChIJy162jpdkbIcRsDEUfnR7l2U",
        "locationConfidence" : 0.62380224
      }, {
        "latitudeE7" : 39.7694669,
        "longitudeE7" : -10.48213655,
        "placeId" : "ChIJgWmbF5hkbIcRDblfuvFpQ2k",
        "locationConfidence" : 0.36909378
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 39.7713857,
        "longitudeE7" : -10.48224210
      },
      "endLocation" : {
        "latitudeE7" : 39.8487755,
        "longitudeE7" : -10.46750814
      },
      "duration" : {
        "startTimestampMs" : "1583437049709",
        "endTimestampMs" : "1583438091000"
      },
      "distance" : 15686,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "LOW",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 59.09876823425293
      }, {
        "activityType" : "STILL",
        "probability" : 30.440962314605713
      }, {
        "activityType" : "WALKING",
        "probability" : 6.368710845708847
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 39.7699127,
        -10.48185119
        }, {
      : 39.8337707,
        -10.47356948
        }, {
      : 39.8487739.,
        -10.46750869
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583438476645",
        "location" : {
          "latitudeE7" : 39.8488131,
          "longitudeE7" : -10.46739.39.0,
          "accuracyMetres" : 74
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 39.8560963,
        "longitudeE7" : -10.46737376,
        "placeId" : "ChIJ_0T_mCp_bIcRapy1NbQ7WEk",
        "address" : "8500 Peña Blvd\nDenver, CO 80249\nUSA",
        "name" : "Denver International Airport",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 100.0
      },
      "duration" : {
        "startTimestampMs" : "1583438091000",
        "endTimestampMs" : "1583450708000"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 39.8538386,
      "centerLngE7" : -10.46763443,
      "visitConfidence" : 73,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 39.8495895,
        "longitudeE7" : -10.46730582,
        "placeId" : "ChIJu5u4zFBnbIcRfKZ-shjAAP0",
        "locationConfidence" : 2.2377242E-6
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED",
      "simplifiedRawPath" : {
        "points" : [ {
      : 39.8487755,
        -10.46750814,
          "timestampMs" : "1583438091000",
          "accuracyMeters" : 73
        }, {
      : 39.8488131,
        -10.46739.39.0,
          "timestampMs" : "1583438476645",
          "accuracyMeters" : 14
        }, {
      : 39.8537508,
        -10.46743127,
          "timestampMs" : "1583440475069",
          "accuracyMeters" : 5
        }, {
      : 39.8537701,
        -10.46761974,
          "timestampMs" : "1583442164236",
          "accuracyMeters" : 3
        }, {
      : 39.8539.092,
        -10.46767998,
          "timestampMs" : "1583443001959",
          "accuracyMeters" : 65
        }, {
      : 39.8539.477,
        -10.46735280,
          "timestampMs" : "158344639.1211",
          "accuracyMeters" : 6
        } ]
      }
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 39.8546779,
        "longitudeE7" : -10.46771239.
      },
      "endLocation" : {
        "latitudeE7" : 449319777,
        "longitudeE7" : -932223722
      },
      "duration" : {
        "startTimestampMs" : "1583450708000",
        "endTimestampMs" : "1583470927577"
      },
      "distance" : 1100230,
      "activityType" : "FLYING",
      "confidence" : "HIGH",
      "activities" : [ {
        "activityType" : "FLYING",
        "probability" : 95.70473432540894
      }, {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 1.6932535916566849
      }, {
        "activityType" : "WALKING",
        "probability" : 1.2719160877168179
      } ],
      "simplifiedRawPath" : {
        "points" : [ {
      : 39.8738185,
        -10.46631882,
          "timestampMs" : "1583452490000",
          "accuracyMeters" : 30
        }, {
      : 449029031,
        -932179241,
          "timestampMs" : "1583457497536",
          "accuracyMeters" : 65
        }, {
      : 448979612,
        -932198477,
          "timestampMs" : "1583460301002",
          "accuracyMeters" : 4
        }, {
      : 448828105,
        -932064829,
          "timestampMs" : "1583460615000",
          "accuracyMeters" : 8
        }, {
      : 448808517,
        -932079706,
          "timestampMs" : "1583460858002",
          "accuracyMeters" : 32
        }, {
      : 449021531,
        -932178220,
          "timestampMs" : "1583461261003",
          "accuracyMeters" : 8
        }, {
      : 449350351,
        -932245051,
          "timestampMs" : "1583467369358",
          "accuracyMeters" : 8
        } ]
      }
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 449319777,
        "longitudeE7" : -932223722
      },
      "endLocation" : {
        "latitudeE7" : 449018023,
        "longitudeE7" : -932175309
      },
      "duration" : {
        "startTimestampMs" : "1583470927577",
        "endTimestampMs" : "1583471662935"
      },
      "distance" : 39.94,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "HIGH",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 79.17906045913696
      }, {
        "activityType" : "STILL",
        "probability" : 10.791461169719696
      }, {
        "activityType" : "FLYING",
        "probability" : 4.571788758039.4745
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 449319953,
        -932223205
        }, {
      : 449166412,
        -932133636
        }, {
      : 449035720,
        -932216339.
        }, {
      : 449017524,
        -932176742
        }, {
      : 449017524,
        -932175292
        } ]
      },
      "simplifiedRawPath" : {
        "points" : [ {
      : 449035759,
        -932213821,
          "timestampMs" : "1583471371104",
          "accuracyMeters" : 12
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583471662935",
        "location" : {
          "latitudeE7" : 449018023,
          "longitudeE7" : -932175309,
          "accuracyMetres" : 76
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 449026654,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJn40NGh4p9ocRomjhS3xb_MM",
        "address" : "5529 38th Ave S\nMinneapolis, MN 55417\nUSA",
        "name" : "5529 38th Ave S",
        "sourceInfo" : {
          "deviceTag" : -2093848546
        },
        "locationConfidence" : 95.284996
      },
      "duration" : {
        "startTimestampMs" : "1583471662935",
        "endTimestampMs" : "1583512121413"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 449024067,
      "centerLngE7" : -932175067,
      "visitConfidence" : 90,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 449021465,
        "longitudeE7" : -932171866,
        "placeId" : "ChIJ7wdfPh4p9ocRlQhY9AwpFwk",
        "locationConfidence" : 4.1507974
      }, {
        "latitudeE7" : 449027748,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJpQyEGh4p9ocRfZ8hfqyGpeI",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.15447062
      }, {
        "latitudeE7" : 449026796,
        "longitudeE7" : -932200715,
        "placeId" : "ChIJjXZ9muEo9ocRGAXdqygVk2s",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.08070591
      }, {
        "latitudeE7" : 449008044,
        "longitudeE7" : -932175785,
        "placeId" : "ChIJD5ro0R8p9ocRFoWZX94ufys",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.07771963
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 44902739.8,
        "longitudeE7" : -932173789
      },
      "endLocation" : {
        "latitudeE7" : 449027102,
        "longitudeE7" : -932174036
      },
      "duration" : {
        "startTimestampMs" : "1583512121413", friday, March 6, 2020 10:28:41.413 AM 
        "endTimestampMs" : "1583513478000"
      },
      "distance" : 3821,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "LOW",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 53.07573080062866
      }, {
        "activityType" : "STILL",
        "probability" : 40.00042974948883
      }, {
        "activityType" : "CYCLING",
        "probability" : 2.453714795410633
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 449027442,
        -932178115
        }, {
      : 449128227,
        -932104568
        }, {
      : 449190330,
        -932165603
        }, {
      : 449166412,
        -932133636
        }, {
      : 449027137,
        -932178115
        } ]
      },
      "simplifiedRawPath" : {
        "points" : [ {
      : 449190292,
        -932160492,
          "timestampMs" : "1583512570572",
          "accuracyMeters" : 65
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583513478000",
        "location" : {
          "latitudeE7" : 449027102,
          "longitudeE7" : -932174036,
          "accuracyMetres" : 65
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 449026654,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJn40NGh4p9ocRomjhS3xb_MM",
        "address" : "5529 38th Ave S\nMinneapolis, MN 55417\nUSA",
        "name" : "5529 38th Ave S",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 96.09381
      },
      "duration" : {
        "startTimestampMs" : "1583513478000",
        "endTimestampMs" : "1583523173003"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 449026433,
      "centerLngE7" : -932174267,
      "visitConfidence" : 86,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 449021465,
        "longitudeE7" : -932171866,
        "placeId" : "ChIJ7wdfPh4p9ocRlQhY9AwpFwk",
        "locationConfidence" : 3.1100168
      }, {
        "latitudeE7" : 449027748,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJpQyEGh4p9ocRfZ8hfqyGpeI",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.2557915
      }, {
        "latitudeE7" : 449027737,
        "longitudeE7" : -932159438,
        "placeId" : "ChIJ3ZDiYx4p9ocR-z5up0-vsRk",
        "locationConfidence" : 0.12352443
      }, {
        "latitudeE7" : 449055365,
        "longitudeE7" : -932174700,
        "placeId" : "ChIJpS6cnB0p9ocRo6jVi3DIi2I",
        "locationConfidence" : 0.09910777
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 449032901,
        "longitudeE7" : -932177673
      },
      "endLocation" : {
        "latitudeE7" : 449035729,
        "longitudeE7" : -932176307
      },
      "duration" : {
        "startTimestampMs" : "1583523173003",
        "endTimestampMs" : "1583523812000"
      },
      "distance" : 2002,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "MEDIUM",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 72.22542762756348
      }, {
        "activityType" : "STILL",
        "probability" : 20.18226832151413
      }, {
        "activityType" : "WALKING",
        "probability" : 2.956038899719715
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 449032897,
        -932178039.
        }, {
      : 449062805,
        -932177810
        }, {
      : 449113502,
        -932228469
        }, {
      : 449058303,
        -932228851
        }, {
      : 449035644,
        -932176284
        } ]
      },
      "simplifiedRawPath" : {
        "points" : [ {
      : 449115562,
        -932228546,
          "timestampMs" : "1583523319515",
          "accuracyMeters" : 5
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "15835240239.98",
        "location" : {
          "latitudeE7" : 449026999,
          "longitudeE7" : -932175586,
          "accuracyMetres" : 70
        }
      }
    }
  }, {
    "placeVisit" : {
      "location" : {
        "latitudeE7" : 449026654,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJn40NGh4p9ocRomjhS3xb_MM",
        "address" : "5529 38th Ave S\nMinneapolis, MN 55417\nUSA",
        "name" : "5529 38th Ave S",
        "sourceInfo" : {
          "deviceTag" : -820903608
        },
        "locationConfidence" : 98.26221
      },
      "duration" : {
        "startTimestampMs" : "1583523812000",
        "endTimestampMs" : "1583538302998"
      },
      "placeConfidence" : "HIGH_CONFIDENCE",
      "centerLatE7" : 449029467,
      "centerLngE7" : -932175867,
      "visitConfidence" : 81,
      "otherCandidateLocations" : [ {
        "latitudeE7" : 449021465,
        "longitudeE7" : -932171866,
        "placeId" : "ChIJ7wdfPh4p9ocRlQhY9AwpFwk",
        "locationConfidence" : 0.79678625
      }, {
        "latitudeE7" : 449027748,
        "longitudeE7" : -93217539.2,
        "placeId" : "ChIJpQyEGh4p9ocRfZ8hfqyGpeI",
        "semanticType" : "TYPE_SEARCHED_ADDRESS",
        "locationConfidence" : 0.33829513
      }, {
        "latitudeE7" : 449027737,
        "longitudeE7" : -932159438,
        "placeId" : "ChIJ3ZDiYx4p9ocR-z5up0-vsRk",
        "locationConfidence" : 0.12405429
      }, {
        "latitudeE7" : 449055365,
        "longitudeE7" : -932174700,
        "placeId" : "ChIJpS6cnB0p9ocRo6jVi3DIi2I",
        "locationConfidence" : 0.118941955
      } ],
      "editConfirmationStatus" : "NOT_CONFIRMED"
    }
  }, {
    "activitySegment" : {
      "startLocation" : {
        "latitudeE7" : 449033584,
        "longitudeE7" : -932165042
      },
      "endLocation" : {
        "latitudeE7" : 449026960,
        "longitudeE7" : -93217539.8
      },
      "duration" : {
        "startTimestampMs" : "1583538302998",Friday, March 6, 2020 5:45:02.998 PM
        "endTimestampMs" : "1583542341999"
      },
      "distance" : 6243,
      "activityType" : "IN_PASSENGER_VEHICLE",
      "confidence" : "LOW",
      "activities" : [ {
        "activityType" : "IN_PASSENGER_VEHICLE",
        "probability" : 43.05156767368317
      }, {
        "activityType" : "WALKING",
        "probability" : 34.63541269302368
      }, {
        "activityType" : "STILL",
        "probability" : 17.35800802707672
      } ],
      "waypointPath" : {
        "waypoints" : [ {
      : 449033584,
        -932165298
        }, {
      : 449164199,
        -932132644
        }, {
      : 449060020,
        -931980972
        }, {
      : 449053878,
        -932082290
        }, {
      : 449026985,
        -932178115
        } ]
      },
      "simplifiedRawPath" : {
        "points" : [ {
      : 449060173,
        -931981049,
          "timestampMs" : "1583541103078",
          "accuracyMeters" : 10
        } ]
      },
      "parkingEvent" : {
        "timestampMs" : "1583542341999", Saturday, March 7, 2020 12:52:21.999 AM
        "location" : {
          "latitudeE7" : 449026960,
          "longitudeE7" : -93217539.8,
          "accuracyMetres" : 69
        }
      }
    }
  }, {
    
def parse_data(data):data_unit['placeVisit'].keys()
>>> dict_keys(['location', 'duration', 'placeConfidence', 'centerLatE7', 'centerLngE7', 'visitConfidence', 'otherCandidateLocations', 'editConfirmationStatus'])
    for data_unit in data["timelineObjects"]:
      if "activitySegment" in data_unit.keys():
        write_activity_points_csv(activitySegment(data_unit["activitySegment"]))
      elif "placeVisit" in data_unit.keys():
        write_places_csv(placeVisit(data_unit["placeVisit"]))
      else:
        print("Error")

#CSV writers.
def write_places_csv(place_data_list):
  with open('FULL_places.csv', 'a', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(place_data_list)

def write_activity_points_csv(point_data_list):
  with open('FULL_activity_points.csv', 'a', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerows(point_data_list)


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

files = ["04-2019_APRIL.json", "05-2019_MAY.json", "06-2019_JUNE.json", "07-2019_JULY.json", "08-2019_AUGUST.json", "09-2019_SEPTEMBER.json"]

for file in files:
  # import pdb; pdb.set_trace()

  with open(f"data/{file}") as f:
    data = json.load(f)
  parse_data(data)
