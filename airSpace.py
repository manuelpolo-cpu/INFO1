import numpy as np
from navAirport import *
from navPoint import *
from navSegment import *
import matplotlib.pyplot as plt
from path import *


class AirSpace:
    def __init__(AirSpace, NavPoints, NavSegments, NavAirports):
        AirSpace.NavPoint = NavPoints
        AirSpace.NavSegment = NavSegments
        AirSpace.NavAirport = NavAirports


def ReadFile():
    NavAirports = []
    SIDs = []
    STARs = []
    F = open('Cat_aer.txt', 'r')
    linea = F.readline().strip()
    while linea != "":
        # Si la línea no es un nombre de aeropuerto
        if not linea.startswith("LE"):
            # Si es un SID o un STAR
            if '.' in linea:  # Si es un SID o STAR
                if len(SIDs) == 0 or (len(STARs) == 0 and '.' not in SIDs[-1]):
                    SIDs.append(linea.strip())  # Añadir a SIDs
                else:
                    STARs.append(linea.strip())  # Añadir a STARs
        else:
            # Si ya hay un aeropuerto previamente, lo añadimos a la lista
            if SIDs or STARs:
                airport = NavAirport(name, SIDs, STARs)
                NavAirports.append(airport)
            # Definir el nombre del aeropuerto y reiniciar las listas de SIDs y STARs
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


def ReadFile_2():
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


def ReadFile_3():
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


def LoadAirSpaceCat():
    NavAirports = ReadFile()
    NavPoints = ReadFile_2()
    NavSegments = ReadFile_3()
    airspace = AirSpace(NavPoints, NavSegments, NavAirports)
    print(f"AirSpace cargado con {len(airspace.NavPoint)} puntos, {len(airspace.NavSegment)} segmentos y con {len(airspace.NavAirport)} aeropuertos")
    return airspace


def Plot_(airspace):
    plt.figure(figsize=(18, 9))
    x_navpoint = []
    y_navpoint = []
    for navpoint in airspace.NavPoint:
        x_navpoint.append(navpoint.longitude)
        y_navpoint.append(navpoint.latitude)
        plt.text(navpoint.longitude,navpoint.latitude,navpoint.name, fontsize=10, color = 'lightgreen',fontweight = 'bold')
    plt.scatter(x_navpoint,y_navpoint, color = 'lightgrey',s = 100)

    for navsegment in airspace.NavSegment:

        origin = next(np for np in airspace.NavPoint if np.number == navsegment.origin_number)
        destination = next(np for np in airspace.NavPoint if np.number == navsegment.destination_number)

        origin_x, origin_y = origin.longitude, origin.latitude
        destination_x, destination_y = destination.longitude, destination.latitude

        plt.annotate("",xy=(destination_x, destination_y),xytext=(origin_x, origin_y),arrowprops=dict(facecolor="lightblue", edgecolor="lightblue", arrowstyle="->", lw=2))

        mid_x = (origin_x + destination_x) / 2
        mid_y = (origin_y + destination_y) / 2
        plt.text(mid_x, mid_y, f"{navsegment.distance:.2f}", color="black", fontsize=10, fontweight='bold')

    plt.xticks(np.arange(-1, 4.5, 0.5))
    plt.yticks(np.arange(38, 42, 0.5))
    plt.grid(color = 'lightpink')
    plt.show()



def PlotNode_(airspace, nameOrigin):
    plt.figure(figsize=(18, 9))

    node_origin = None
    for node in airspace.NavPoint:
        if node.name == nameOrigin:
            node_origin = node
            break

    if not node_origin:
        print("No se encontró el nodo de origen.")
        return

    plt.text(node_origin.longitude + 0.05, node_origin.latitude + 0.05, node_origin.name,
             fontsize=10, color='lightgreen', fontweight='bold')
    plt.scatter(node_origin.longitude, node_origin.latitude, color='grey', s=100)

    for node in airspace.NavPoint:
        if node.name != nameOrigin:
            plt.scatter(node.longitude, node.latitude, color='lightgrey', s=100)
            plt.text(node.longitude + 0.05, node.latitude + 0.05, node.name,
                     fontsize=10, color='lightgreen', fontweight='bold')

    navpoint_by_number = {n.number: n for n in airspace.NavPoint}

    for segment in airspace.NavSegment:
        if segment.origin_number == node_origin.number:
            destino = navpoint_by_number.get(segment.destination_number)
            if destino:
                ox, oy = node_origin.longitude, node_origin.latitude
                dx, dy = destino.longitude, destino.latitude
                plt.annotate("",
                             xy=(dx, dy), xytext=(ox, oy),
                             arrowprops=dict(facecolor="lightblue", edgecolor="lightblue", arrowstyle="->", lw=2))
                mx, my = (ox + dx) / 2, (oy + dy) / 2
                plt.text(mx, my, f"{segment.distance:.2f}", color="black", fontsize=9, fontweight='bold')

    plt.xticks(np.arange(-1, 4.5, 0.5))
    plt.yticks(np.arange(38, 42, 0.5))
    plt.grid(color='lightpink')
    plt.show()


