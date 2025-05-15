from airSpace import *


def test():
    ReadFile()
    print('----')
    ReadFile_2()
    print('----')
    ReadFile_3()
    print('----')
    airspace = LoadAirSpaceCat()
    Plot_(airspace)
    PlotNode_(airspace, 'GODOX')
test()