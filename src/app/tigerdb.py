import requests
from flask.json import jsonify
from app.model import Response, db ,RoadSegment ,Path
from app.abstractions import exists, updateFrequency
import json


def get_shortest_path(start, end, maxD):
    URL = "http://172.22.0.2:9000/query/MyGraph/ShortestPath"
    r = requests.get(url=URL, params={"S": start, "T": end, "maxDepth": maxD})
    results = json.loads(r.text)["results"]
    path = results[0]['StartSet'][0]['attributes']["StartSet.@pathResults"][0]
    return path


def get_all_resources():
    URL = "http://172.22.0.2:9000/graph/MyGraph/vertices/Resource"
    r = requests.get(url=URL)
    results = json.loads(r.text)["results"]
    print(results)
    # todo Process start and end time data (get from TG) && organize version data of sim
    for result in results:
        print(result["attributes"]["id"])
        pathNodes = getPathNodes(result["attributes"]["id"])
        createRoadSegments(pathNodes)

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



def createRoadSegments(pathNodes):
    pathIDs = []
    
#?, what if list is 2 long?
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

def getPathNodes(id):
    roadNodes = getStartAndEndNodes(id)
    source = roadNodes[0]["S"][0]['v_id']
    destination = roadNodes[0]["E"][0]['v_id']
    path = get_shortest_path(source, destination, 1000)
    pathNodes = path.split("-")
    pathNodes.pop(len(pathNodes) - 1)
    return pathNodes

def getStartAndEndNodes(resource):
    URL = "http://172.22.0.2:9000/query/MyGraph/getStartAndEndNodes"
    r = requests.get(url=URL, params={"R": resource})
    results = json.loads(r.text)["results"]
    return results
