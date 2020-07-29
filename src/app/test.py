import xml.etree.ElementTree as et
from app.postgresdb import create_response

def sort_output():
    out = et.parse("app/data/tripinfo.xml")
    root = out.getroot()
    for child in root.findall('tripinfo'):
        if "ambulance" in child.attrib['id']:
            create_response(child.attrib['depart'], child.attrib['arrival'], child.attrib['duration'], child.attrib['routeLength'])
            print(child.attrib['depart'])
