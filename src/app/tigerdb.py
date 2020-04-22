import requests


def get_shortest_path(start, end, maxD):
    URL = "http://172.22.0.2:9000/query/MyGraph/ShortestPath"
    r = requests.get(url=URL, params={"S": start, "T": end, "maxDepth": maxD})
    return r.json()
