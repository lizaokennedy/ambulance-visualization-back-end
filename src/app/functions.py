import requests
from flask.json import jsonify
from app.model import Response, db ,RoadSegment ,Path
from app.tigerdb import getAllResponseCallTimes
import json

def get_reposnses_per_week():
    responses = getAllResponseCallTimes()
    offset = get_offset(responses)
    weekCounts = [0] * 52
    for time in responses:
        time -= offset
        time = round((((time/60)/60)/24)/7)
        weekCounts[time-1] += 1
    return json.dumps(weekCounts)



def get_offset(responses):
    minval = 10000000000
    for time in responses:
        if time < minval:
            minval = time
    return minval