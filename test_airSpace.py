from airSpace import *
from graph import *
import matplotlib.pyplot as plt
import numpy as np
from path import *


def test():
    print('Cargando espacio aéreo...')
    airspace_cat = LoadAirSpaceCat()
    print('Convirtiendo a grafo...')
    graph_cat = AirSpaceToGraph(airspace_cat)
    figsize = (15,7)
    xticks = range(-1,5,1)
    yticks = np.arange(38, 42.5, 0.5)
    Plot(graph_cat, figsize, xticks, yticks)
    plt.show()
    PlotNode(graph_cat, 'GODOX', figsize, xticks, yticks)
    plt.show()
test()