## The EDGE class is just a utility class for the GraphViz and GraphMaker classes.  It simply represents an edge in
# a graph being constructed, capturing the endpoints of the edge as well as its label.  Its biggest active
# contribution is that it is able to compute the edge label based on some distortion percentage (between 0-1) that is
# passed into the constructor as the "label".

__author__ = "Eck Doerry"
__copyright__ = "Copyright 2018, Northern Arizona University, Flagstaff AZ"


import numpy as np
import scipy.spatial as graph
import matplotlib.pyplot as plt

class Edge:

    # Makes a new edge.  You pass in two points (x,y tuples) plus a label.  Label is used flexibly to determine
    #  how the edge is labeled.   If label=0, then edge is just labeled with exact straightline distance between
    #  the points.  If label is a value between 0-1, this is viewed as a percentage to distort the distance by.
    #  If label > 1, then is taken as an actual value that you want placed on that edge.
    def __init__(self, p1,p2, label=0):
        self.p1=p1
        self.p2=p2
        self.x1=p1[0]
        self.y1=p1[1]
        self.x2=p2[0]
        self.y2=p2[1]
        self.dist= int(graph.distance.euclidean(p1,p2))
        self.midx = abs(p1[0] - p2[0]) / 2 + min(p1[0], p2[0])
        self.midy = abs(p1[1] - p2[1]) / 2 + min(p1[1], p2[1])
        self.endlabel1=""
        self.endlabel2=""
        # if a distortion was passed in, randomly distort edge length appropriately.
        if label==0: self.label=self.dist  # default.  Edge label is its length
        elif label<1: # label was a distortion percentage. randomly calc length based on it.
            adjust=self.dist*label
            distortion= np.random.randn()*adjust
            # randomly adjust the labeled distance to be longer/shorter than using the distortion
            #if (np.random.random() < 0.5): self.label=int(self.dist - distortion) # randomly add/subtract the adjustment
            #else: self.label=int(self.dist + distortion)
            # # Commented out above. For graphs of road networks, the labeled dist is ALWAYS longer, never shorter than SLD
            self.label = int(self.dist + distortion)
        else: self.label=label # label was an actual number you want on the edge

    def get(self):
        return ([self.x1,self.y1],[self.x2,self.y2],self.label,[self.midx,self.midy])

    def midpt(self):
        return([self.midx,self.midy])

    # Returns true if the edge connects the two labels. Have to check both directions!
    def connects(self,label1,label2):
        if (label1 == self.endlabel1 and label2 == self.endlabel2) or (label1 == self.endlabel2 and label2 == self.endlabel1):
            return True
        return False

    def setLabels(self,l1,l2):
        self.endlabel1=l1
        self.endlabel2=l2

# Unit test main fn
# x= Edge((23,56),(34,45))
# print("created an edge: "+ str(x.get()))
