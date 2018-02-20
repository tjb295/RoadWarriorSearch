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

        #list to be able to find already entered nodes
        self.searchNodesList = []

        #define the open list
        self.openList = []


        self.successorArray = []

    def loadMap(self):

        #read in file line by line and begin inserting these into
        #search nodes

        #positions list to see if the name has already been entered
        labelsList = []

        with open(self.map, "r") as nodes:
            for line in nodes:
                
                
                tuple = eval(line)
                if tuple[0] not in labelsList:

                    labelsList.append(tuple[0])
    
                    new = SearchNode(tuple[0])
                    self.searchNodesList.append(new)
                    new.coordinates = tuple[3]

                    if tuple[1] not in labelsList:

                        labelsList.append(tuple[1])

                        #create a search node for the successor if none exists
                        newSuccessor = SearchNode(tuple[1])
                        self.searchNodesList.append(newSuccessor)


                        #doubly link the two nodes, with the edge value in between
                        new.successors.append((newSuccessor, tuple[2]))
                        newSuccessor.successors.append((new, tuple[2]))

                        #now add the coordinates
                
                        newSuccessor.coordinates = tuple[4]

                    else:
                        #if we already have the 2nd value, find it and update its connections
                        for i in self.searchNodesList:
                            if i.label == tuple[1]:
                                i.successors.append((new, tuple[2]))
                else:

                    for i in self.searchNodesList:
                        if i.label == tuple[0]:
                            
                            #make cases for if the second label already exists
                            if tuple[1] not in labelsList:
                                labelsList.append(tuple[1])

                                #create new search node
                                newSuccessor = SearchNode(tuple[1])
                                self.searchNodesList.append(newSuccessor)
                                i.successors.append((newSuccessor, tuple[2]))

                                newSuccessor.successors.append((i, tuple[2]))
                                newSuccessor.coordinates = tuple[4]

                            else:
                                for j in self.searchNodesList:
                                    if j.label == tuple[1]:
                                        i.successors.append((j, tuple[2]))
                                        j.successors.append((i, tuple[2]))


        # for nodes in self.searchNodesList:
        #     print("%s is a node" % (nodes.label)) 
        #     print(" its coordinates are %d, %d " % (nodes.coordinates[0], nodes.coordinates[1]) )
        #     print("It has the sucessors ")
        #     for successors in nodes.successors:
        #         print("     %s with edge value %d" % (successors[0].label, successors[1]) )

    def performSearch(self, searchType, startNodeString, goalNodes, expansion, verbose):
    
        goalNodesArray = []
        startNode = ""
        #First state type of search and name of input file
        print("Performing %s search with map file %s \n" % (searchType, self.map))
        

        #Setting start nodes and goal nodes
        for nodes in self.searchNodesList:
            if startNodeString == nodes.label:
                startNode = nodes

            for goals in goalNodes:
                if goals == nodes.label:
                    goalNodesArray.append(nodes)

        print("The starting node is node %s " % (startNode.label) )
        print("The goal nodes are as follows: ")
        for goals in goalNodesArray:
            print("%s" % (goals.label) )

        print("\n")
        
        #append the start node to the open list
        self.openList.append(startNode)

        #Print the open list for part one 
        self.showOpenList()

        #generate successors of starting node
        self.generateSuccessors(startNode)
        print("\n")

        #insert children of starting node at front
        self.insert("front")
        
        #inser children of starting node at back
        self.insert("back")

        #insert children of starting node in order
        self.insert("order")

        #show children added
        #self.showOpenList()

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
    def hSLD(self):
        return

    #Hdir
    def hDIR(self):
        return
    
    def showOpenList(self):

        print("Open list is as follows: ")
        for open in self.openList:

            print("label: %s, Value %d" % (open.label, open.value) )
        print("\n")

    def generateSuccessors(self, currNode):

        self.successorArray = []

        for i in currNode.successors:
            i[0].value += i[1]
            self.successorArray.append(i[0])

        self.successorArray.sort(key = lambda c: c.label)

        for i in self.successorArray:
            print("Successor: %s with value %d" % (i.label, i.value) )



        # self.openList.remove(currNode)

        # for i in successorArray:
        #     self.openList.append(i)

    def insert(self,insertType):

        if insertType == "front":
            for i in self.successorArray:
                if i not in self.openList:
                    self.openList.insert(0, i)

        elif insertType == "back":  
            for i in self.successorArray:
                if i not in self.openList:
                    self.openList.append(i)
        
        elif insertType == "order":
            #sort by value of cheapest node
            for i in self.successorArray:
                if i not in self.openList:
                    self.openList.append(i)

            self.openList.sort(key = lambda c: c.value)


        else:
            print("Bad insert type")
            return

        self.showOpenList()

def main():
    mainSearch = Searcher("samplemap.txt")
    mainSearch.loadMap()
    mainSearch.performSearch("BFS", "U", ["T"], 0, 0)

if __name__ == "__main__":
    main()