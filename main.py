# import numpy as np
# import scipy
# import matplotlib

##thes search node class with two attributes, the label, 
#and value as the path cost from start to this node

class SearchNode:

    def __init__(self,label):
        self.label = label

        self.coordinates = ()

        self.successors = []
        #value is the path cost
        self.value = 0
    
##class to load map
class Searcher:

    def __init__(self, map):
        self.map = map

    def loadMap(self):

        #read in file line by line and begin inserting these into
        #search nodes

        #positions list to see if the name has already been entered
        labelsList = []

        #list to be able to find already entered nodes
        searchNodesList = []

        with open(self.map, "r") as nodes:
            for line in nodes:

                tuple = eval(line)
                if tuple[0] not in labelsList:

                    labelsList.append(tuple[0])
    
                    new = SearchNode(tuple[0])
                    searchNodesList.append(new)

                    if tuple[1] not in labelsList:

                        labelsList.append(tuple[1])

                        #create a search node for the successor if none exists
                        newSuccessor = SearchNode(tuple[1])
                        searchNodesList.append(newSuccessor)


                        #doubly link the two nodes, with the edge value in between
                        new.successors.append((newSuccessor, tuple[2]))
                        newSuccessor.successors.append((new, tuple[2]))

                        #now add the coordinates
                        new.coordinates = tuple[3]
                        newSuccessor.coordinates = tuple[4]

                    else:
                        #if we already have the 2nd value, find it and update its connections
                        for i in searchNodesList:
                            if i.label == tuple[1]:
                                i.successors.append((new, tuple[2]))
                else:

                    for i in searchNodesList:
                        if i.label == tuple[0]:
                            
                            #make cases for if the second label already exists
                            if tuple[1] not in labelsList:
                                labelsList.append(tuple[1])

                                #create new search node
                                newSuccessor = SearchNode(tuple[1])
                                i.successors.append((newSuccessor, tuple[2]))

                                newSuccessor.successors.append((i, tuple[2]))
                                newSuccessor.coordinates = tuple[4]

                            else:
                                for j in searchNodesList:
                                    if j.label == tuple[1]:
                                        i.successors.append((j, tuple[2]))
                                        j.successors.append((i, tuple[2]))
        for nodes in searchNodesList:
            print("%s is a node" % (nodes.label)) 
            print("It has the sucessors ")
            for successors in nodes.successors:
                print("     %s with edge value %d" % (successors[0].label, successors[1]) )
                        
                        



                    






    def performSearch(searchType, startNode, goalNodes, expansion, verbose):
        #First state type of search and name of input file
        print("Performing %s search with map file %s \n" % (searchType, self.map))
        print("The start node is %s \n" % (startNode.value))
        print("while the goal nodes are " + goalNodes.value)

        if   searchType == "BFS":   
            return

        elif searchType == "DFS":
            return

        elif searchType == "BEST":
            return

        elif searchType == "A*":
            return

        else:
            print("Error searchType is invalid \n")
            return 
    
    #Straight Line Distance
    def HeuristicFunction1():
        return

    #Hdir
    def HeuristicFunction2():
        return

def main():
    mainSearch = Searcher("samplemap.txt")
    mainSearch.loadMap()

if __name__ == "__main__":
    main()