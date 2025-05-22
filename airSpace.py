#import de las funciones gráficasy numéricas
import matplotlib.pyplot as plt
import numpy as np
#imports de todas las funciones y clases necesarias
from navAirport import *
from navPoint import *
from navSegment import *
from path import *
from graph import *


#definición de la clase AirSpace
class AirSpace:
    def __init__(AirSpace, NavPoint, NavSegment, NavAirport):
        AirSpace.NavPoint = NavPoint
        AirSpace.NavSegment = NavSegment
        AirSpace.NavAirport = NavAirport


#leer aeropuertos de Cataluña
def ReadFileCat():
    NavAirports = []
    SIDs = []
    STARs = []
    F = open('Cat_aer.txt', 'r')
    linea = F.readline().strip()
    while linea != "":
        if '.' in linea:
            if len(SIDs) == 0 or (len(STARs) == 0 and '.' not in SIDs[-1]):
                SIDs.append(linea.strip())  # Añadir a SIDs
            else:
                STARs.append(linea.strip())  # Añadir a STARs
        else:
            if SIDs or STARs:
                airport = NavAirport(name, SIDs, STARs)
                NavAirports.append(airport)
            name = linea.strip()
            SIDs = []
            STARs = []
        linea = F.readline().strip()
    F.close()
    if SIDs or STARs:
        airport = NavAirport(name, SIDs, STARs)
        NavAirports.append(airport)
    for airport in NavAirports:
        print(f"Aeropuerto: {airport.name}")
        print(f"SIDs: {airport.SIDs}")
        print(f"STARs: {airport.STARs}")
    return NavAirports

#leer puntos de navegación de cataluña
def ReadFile_2Cat():
    NavPoints = []
    F = open('Cat_nav.txt','r')
    linea = F.readline()
    while linea != "":
        elementos = linea.split(" ")
        number = int(elementos[0])
        name = elementos[1]
        latitude = float(elementos[2])
        longitude = float(elementos[3])
        np = NavPoint(number, name, latitude, longitude)
        NavPoints.append(np)
        linea = F.readline()
    F.close()
    for np in NavPoints:
        print(f"Número: {np.number}")
        print(f"Point name: {np.name}")
        print(f"Point latitude: {np.latitude}")
        print(f"Point longitude: {np.longitude}")
    return NavPoints

#leer los segmentos de Cataluña
def ReadFile_3Cat():
    NavSegments = []
    F = open('Cat_seg.txt','r')
    linea = F.readline()
    while linea != "":
        elementos = linea.split(" ")
        origin_number = int(elementos[0])
        destination_number = int(elementos[1])
        distance = float(elementos[2])
        ns = NavSegment(origin_number, destination_number, distance)
        NavSegments.append(ns)
        linea = F.readline()
    F.close()
    for ns in NavSegments:
        print(f"Origin number: {ns.origin_number}")
        print(f"Destination number: {ns.destination_number}")
        print(f"Distance: {ns.distance}")
    return NavSegments

#cargar el espacio aéreo de Cataluña llamando a las tres funciones
def LoadAirSpaceCat():
    NavAirports = ReadFileCat()
    NavPoints = ReadFile_2Cat()
    NavSegments = ReadFile_3Cat()
    airspace = AirSpace(NavPoints, NavSegments, NavAirports)
    print(f"AirSpace cargado con {len(airspace.NavPoint)} puntos, {len(airspace.NavSegment)} segmentos y con {len(airspace.NavAirport)} aeropuertos")
    return airspace


#leer aeropuertos de España
def ReadFileEsp():
    NavAirports = []
    SIDs = []
    STARs = []
    F = open('Spain_aer.txt', 'r')
    linea = F.readline().strip()
    while linea != "":
        if '.' in linea:  # Si es un SID o STAR
            if len(SIDs) == 0 or (len(STARs) == 0 and '.' not in SIDs[-1]):
                SIDs.append(linea.strip())
            else:
                STARs.append(linea.strip())
        else:
            if SIDs or STARs:
                airport = NavAirport(name, SIDs, STARs)
                NavAirports.append(airport)
            name = linea.strip()
            SIDs = []
            STARs = []
        linea = F.readline().strip()
    F.close()
    if SIDs or STARs:
        airport = NavAirport(name, SIDs, STARs)
        NavAirports.append(airport)
    for airport in NavAirports:
        print(f"Aeropuerto: {airport.name}")
        print(f"SIDs: {airport.SIDs}")
        print(f"STARs: {airport.STARs}")
    return NavAirports

#leer aeropuertos de España
def ReadFile_2Esp():
    NavPoints = []
    F = open('Spain_nav.txt','r')
    linea = F.readline()
    while linea != "":
        elementos = linea.split(" ")
        number = int(elementos[0])
        name = elementos[1]
        latitude = float(elementos[2])
        longitude = float(elementos[3])
        np = NavPoint(number, name, latitude, longitude)
        NavPoints.append(np)
        linea = F.readline()
    F.close()
    for np in NavPoints:
        print(f"Número: {np.number}")
        print(f"Point name: {np.name}")
        print(f"Point latitude: {np.latitude}")
        print(f"Point longitude: {np.longitude}")
    return NavPoints

#leer segmentos de España
def ReadFile_3Esp():
    NavSegments = []
    F = open('Spain_seg.txt','r')
    linea = F.readline()
    while linea != "":
        elementos = linea.split(" ")
        origin_number = int(elementos[0])
        destination_number = int(elementos[1])
        distance = float(elementos[2])
        ns = NavSegment(origin_number, destination_number, distance)
        NavSegments.append(ns)
        linea = F.readline()
    F.close()
    for ns in NavSegments:
        print(f"Origin number: {ns.origin_number}")
        print(f"Destination number: {ns.destination_number}")
        print(f"Distance: {ns.distance}")
    return NavSegments

#cargar espacio aéreo de España llamando a las tres funciones
def LoadAirSpaceEsp():
    NavAirports = ReadFileEsp()
    NavPoints = ReadFile_2Esp()
    NavSegments = ReadFile_3Esp()
    airspace = AirSpace(NavPoints, NavSegments, NavAirports)
    print(f"AirSpace cargado con {len(airspace.NavPoint)} puntos, {len(airspace.NavSegment)} segmentos y con {len(airspace.NavAirport)} aeropuertos")
    return airspace


#leer aeropuertos de Europa
def ReadFileEur():
    NavAirports = []
    SIDs = []
    STARs = []
    F = open('ECAC_aer.txt', 'r')
    linea = F.readline().strip()
    while linea != "":
        if '.' in linea:  # Si es un SID o STAR
            if len(SIDs) == 0 or (len(STARs) == 0 and '.' not in SIDs[-1]):
                SIDs.append(linea.strip())  # Añadir a SIDs
            else:
                STARs.append(linea.strip())  # Añadir a STARs
        else:
            if SIDs or STARs:
                airport = NavAirport(name, SIDs, STARs)
                NavAirports.append(airport)
            name = linea.strip()
            SIDs = []
            STARs = []
        linea = F.readline().strip()
    F.close()
    if SIDs or STARs:
        airport = NavAirport(name, SIDs, STARs)
        NavAirports.append(airport)
    for airport in NavAirports:
        print(f"Aeropuerto: {airport.name}")
        print(f"SIDs: {airport.SIDs}")
        print(f"STARs: {airport.STARs}")
    return NavAirports

#leer puntos de navegación de Europa
def ReadFile_2Eur():
    NavPoints = []
    F = open('ECAC_nav.txt','r')
    linea = F.readline()
    while linea != "":
        elementos = linea.split(" ")
        number = int(elementos[0])
        name = elementos[1]
        latitude = float(elementos[2])
        longitude = float(elementos[3])
        np = NavPoint(number, name, latitude, longitude)
        NavPoints.append(np)
        linea = F.readline()
    F.close()
    for np in NavPoints:
        print(f"Número: {np.number}")
        print(f"Point name: {np.name}")
        print(f"Point latitude: {np.latitude}")
        print(f"Point longitude: {np.longitude}")
    return NavPoints

#leer segmentos de Europa
def ReadFile_3Eur():
    NavSegments = []
    F = open('ECAC_seg.txt','r')
    linea = F.readline()
    while linea != "":
        elementos = linea.split(" ")
        origin_number = int(elementos[0])
        destination_number = int(elementos[1])
        distance = float(elementos[2])
        ns = NavSegment(origin_number, destination_number, distance)
        NavSegments.append(ns)
        linea = F.readline()
    F.close()
    for ns in NavSegments:
        print(f"Origin number: {ns.origin_number}")
        print(f"Destination number: {ns.destination_number}")
        print(f"Distance: {ns.distance}")
    return NavSegments

#cargar el espacio aéreo de Europa llamando a las tres funciones
def LoadAirSpaceEur():
    NavAirports = ReadFileEur()
    NavPoints = ReadFile_2Eur()
    NavSegments = ReadFile_3Eur()
    airspace = AirSpace(NavPoints, NavSegments, NavAirports)
    print(f"AirSpace cargado con {len(airspace.NavPoint)} puntos, {len(airspace.NavSegment)} segmentos y con {len(airspace.NavAirport)} aeropuertos")
    return airspace


#conversión de un espacio aéreo en grafo
def AirSpaceToGraph(airspace):
    graph = Graph()
    number_to_node = {}
    for navpoint in airspace.NavPoint:
        name = navpoint.name
        coordinate_x = navpoint.longitude
        coordinate_y = navpoint.latitude
        node = Node(name, coordinate_x, coordinate_y)
        graph.nodes.append(node)
        number_to_node[navpoint.number] = node
    for navsegment in airspace.NavSegment:
        origin_number = navsegment.origin_number
        destination_number = navsegment.destination_number
        origin_node = number_to_node.get(origin_number)
        destination_node = number_to_node.get(destination_number)
        if origin_node and destination_node:
            segment = Segment(
                name=f"{origin_node.name}-{destination_node.name}",
                origin=origin_node,
                destination=destination_node,
                cost=navsegment.distance)
            graph.segments.append(segment)
            if destination_node not in origin_node.neighbors:
                origin_node.neighbors.append(destination_node)
    return graph