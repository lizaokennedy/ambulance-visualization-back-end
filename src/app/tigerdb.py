import requests
from math import floor
from flask.json import jsonify
from app.model import Response, db ,RoadSegment ,Path
from app.postgresdb import exists, updateFrequency
import json


def get_shortest_path(start, end, maxD):
    URL = "http://172.22.0.2:9000/query/MyGraph/ShortestPath"
    r = requests.get(url=URL, params={"S": start, "T": end, "maxDepth": maxD})
    results = json.loads(r.text)["results"]
    if len(results[0]['StartSet']) > 0:
        path = results[0]['StartSet'][0]['attributes']["StartSet.@pathResults"][0]
        return path
    else:
        return start + "-" + end


def get_all_resources():
    count = 0
    URL = "http://172.22.0.2:9000/graph/MyGraph/vertices/Resource"
    r = requests.get(url=URL)
    results = json.loads(r.text)["results"]
    # todo Process start and end time data (get from TG) && organize version data of sim
    for result in results:
        print("Progress: " + str(round(count/len(results)*100)) + "%")
        pathNodes = get_path_nodes(result["attributes"]["id"])
        create_road_segments(pathNodes)

        path = Path(pathNodes)
        db.session.add(path)
        db.session.commit()

        start = result["attributes"]["ResponseCallTime"]
        end = start + result["attributes"]["AmbulanceStartTime"] + result["attributes"]["OnSceneDuration"] + result["attributes"]["TimeAtHospital"] + \
            result["attributes"]["TravelTimePatient"] + \
            result["attributes"]["TravelTimeHospital"] + \
            result["attributes"]["TravelTimeStation"]

        response = Response(path.id, start, end, 1)
        db.session.add(response)
        db.session.commit()
        count = count + 1



def create_road_segments(pathNodes):
    pathIDs = []
    
    for i in range(len(pathNodes) - 2):
        segment = RoadSegment(0,0,0)
        if (pathNodes[i] < pathNodes[i + 1]):

            if (not (exists(pathNodes[i], pathNodes[i + 1]))):
                segment = RoadSegment(pathNodes[i], pathNodes[i+1], 1)
                db.session.add(segment)
                db.session.commit()
            else:
                segment = updateFrequency(pathNodes[i], pathNodes[i + 1])
                db.session.commit()
            
        elif (pathNodes[i + 1] < pathNodes[i]):

            if (not (exists(pathNodes[i+1], pathNodes[i]))):

                segment = RoadSegment(pathNodes[i+1], pathNodes[i], 1)
                db.session.add(segment)
                db.session.commit()
            else:
                segment = updateFrequency(pathNodes[i+1], pathNodes[i])
                db.session.commit()
        
        db.session.commit()
        pathIDs.append(segment.id)
    return pathIDs

def get_path_nodes(id):
    roadNodes = get_start_and_end_nodes(id)
    source = roadNodes[0]["source"][0]['v_id']
    destination = roadNodes[1]["dest"][0]['v_id']
    path = get_shortest_path(source, destination, 1000)
    pathNodes = path.split("-")
    pathNodes.pop(len(pathNodes) - 1)

    return pathNodes

def get_start_and_end_nodes(resource):
    results = ""
    URL = "http://172.22.0.2:9000/query/MyGraph/StartAndEndNodes"
    r = requests.get(url=URL, params={"R": resource})
    results = json.loads(r.text)["results"]
    # print(json.loads(r.text)["results"])
    return results


def get_all_response_call_times():
    results = ""
    URL = "http://172.22.0.2:9000/graph/MyGraph/vertices/Resource?select=ResponseCallTime"
    r = requests.get(url=URL)
    results = json.loads(r.text)["results"]
    responseTimes = []
    for i in range(len(results)):
        responseTimes.append(results[i]['attributes']['ResponseCallTime'])
    return responseTimes

def get_num_responses():
    URL = "http://172.22.0.2:9000/graph/MyGraph/vertices/Resource"
    r = requests.get(url=URL, params={"count_only": "true"})
    results = json.loads(r.text)["results"][0]["count"]
    return str(results)

def get_num_transfers():
    URL = "http://172.22.0.2:9000/graph/MyGraph/vertices/Resource"
    r = requests.get(url=URL, params={"filter": "Transfer=1", "count_only": "true"})
    results = json.loads(r.text)["results"][0]["count"]
    return str(results)

def get_avg_response_time():
    URL = "http://172.22.0.2:9000/graph/MyGraph/vertices/Resource"
    r = requests.get(url=URL, params={"select": "AmbulanceStartTime"})
    results = json.loads(r.text)["results"]
    accum = 0
    for i in range(len(results)):
        accum += results[i]["attributes"]["AmbulanceStartTime"]
    
    time = (accum/len(results))/60 #8.1234533
    mins = floor(time) #8
    seconds = round((time - mins) * 60)
    if seconds < 10:
        seconds = "0" + str(seconds)
    returnTime = str(mins) + ":" + str(seconds)
    return returnTime