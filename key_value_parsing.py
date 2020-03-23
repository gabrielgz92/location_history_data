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

#Method to run all the scripts.
def parse_data(data):
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
