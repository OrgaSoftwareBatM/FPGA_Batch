# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 10:26:44 2016

@author: shintaro
"""

from gdsii import types
from gdsii.record import Record
import numpy as np
import re
import pylab as plt

class structurefromGDS(object):
    """
    Interface to convert the polygons from GDS files into point lists that 
    can be used to calculate the potential landscapes.
    Reads gds file
    outputs pointlist when called
    """
    def __init__(self, fname):
        self.fname = fname        
        self.units = []
        self.pointlists = []
        self.string_infos = {}

    def show_data(self, rec):
        """Shows data in a human-readable format."""
        if rec.tag_type == types.ASCII:
            return '"%s"' % rec.data.decode() # TODO escape
        elif rec.tag_type == types.BITARRAY:
            return str(rec.data)
        return ', '.join('{0}'.format(i) for i in rec.data)
    
    def main(self):
        """
        open filename (if exists)
        read units
        get list of polygons
        """
#        test = []
        no_of_Structures = 0
        string_position = []
        strings = []
        
        with open(self.fname, 'rb') as a_file:
            for rec in Record.iterate(a_file):
#                test.append([rec.tag_name, rec.data, rec.tag_type])
                if rec.tag_type == types.NODATA:
                    pass
                else:
#                    print('%s: %s' % (rec.tag_name, show_data(rec)))
#                    print('%s:' % (rec.tag_name))
                    if rec.tag_name == 'UNITS':
                        """
                        get units
                        """
                        unitstring = self.show_data(rec)
                        self.units = np.array(re.split(',', unitstring)).astype(float)
                        
                    elif rec.tag_name == 'XY':
                        no_of_Structures += 1
                        """
                        get pointlist
                        """
                        # get data
                        datastring = self.show_data(rec)
                        # split string at , and convert to float
                        data = np.array(re.split(',', datastring)).astype(float)
                        # reshape into [[x1,y1],[x2,y2],...]
                        if len(data)>2:
                            data = np.reshape(data,(len(data)/2, 2))[:-1]
                        else:
                            data = np.reshape(data,(len(data)/2, 2))
                        self.pointlists.append(data)
                    elif rec.tag_name == 'STRING':
                        string_position.append(no_of_Structures-1)
                        strings.append(rec.data)
        self.string_infos = dict(zip(string_position, strings))
                        


    def __call__(self):
        """
        execute main
        return list of polygons with correct SI-units (scaled by units)
        """
        print("\n\n LoadGDS have been disabled \n\n")
        # self.main()
#        return np.array(self.pointlists) * self.units[1]
#        return np.multiply(np.array(self.pointlists), self.units[1])
        return np.array(self.pointlists)
        
if __name__ == '__main__':
    """
    This is how to use the software.
    Change the argument of convertGDStopts to your gds file
    """
    getStuff = structurefromGDS('GDS\HBT6.GDS')
    fig10 = plt.figure(10)
    fig10.clf()
    ax = fig10.add_subplot(1,1,1)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    for i, array in enumerate(getStuff()):
            xpos = array[:,0]
            ypos = array[:,1]
            """Show gates with enumeration if wanted"""
            if not i in getStuff.string_infos.keys():
                ax.fill(xpos, ypos, facecolor='b',alpha=0.5, edgecolor='black')
            else:
                ax.text(xpos[0], ypos[0], getStuff.string_infos[i])

    #for clarity: shape=(l,m,n):(l polygons, m points, n coordinates each)
#    print np.shape(getStuff())