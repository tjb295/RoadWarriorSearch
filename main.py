### Author: Thomas Back ####
import numpy 
from scipy.spatial import distance
import matplotlib
from graphviz import GraphViz

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

        self.goalNodesArray = []

        self.history = []

        self.prevNode = ""

        self.expansions = 0

        self.path = []

        self.verbose = False

        self.numGoals = 0

        self.finishedGoals = []

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

    def performSearch(self, searchType, startNodeString, goalNodes, expansion, verbose, grapher):
    
        
        startNode = ""
        #First state type of search and name of input file
        print("Performing %s search with map file %s \n" % (searchType, self.map))
        self.verbose = verbose

        stats = SearchStats()

        #Setting start nodes and goal nodes
        for nodes in self.searchNodesList:
            if startNodeString == nodes.label:
                startNode = nodes

            for goals in goalNodes:
                if goals == nodes.label:
                    self.goalNodesArray.append(nodes)

        print("The starting node is node %s " % (startNode.label) )
        print("The goal nodes are as follows: ")
        for goals in self.goalNodesArray:
            print("%s" % (goals.label) )

        print("\n")

        #Grapher functionality
        grapher.loadGraphFromFile("30node.txt")
        grapher.plot()
        grapher.markStart(startNode.label)
        grapher.markGoal(self.goalNodesArray[0].label)
        

        #append the start node to the open list
        self.openList.append(startNode)

        #Print the open list for part one 
        self.showOpenList()

        if   searchType == "BFS": 
            #conduct bfs search
            self.bfs(grapher, stats)  
            

        elif searchType == "DFS":
            self.dfs(grapher, stats)

        elif searchType == "BEST":
            self.best(grapher, stats)

        elif searchType == "A*":
            self.aStar(grapher, stats)

        else:
            print("Error searchType is invalid \n")
            return 

        ##output
        print("The total number of expansions were %d" % (self.expansions))
        print("The length of the path to goal is %d " % (self.calcPathCost()))
        print("The path is as follows: ", end="")
        for i in self.path:
            print("%s, " % (i.label), end ="")
        print("\n")

        print("The average openlist size was %f " % (stats.calculcateAvgOpenlist()) )
        print("The maximum openlist size was %d"  % (stats.maxOpenListSize) )
        print("\n")

        print("The average node branching factor is %f" % (stats.calculateAvgBranch()) )
    
    def calcPathCost(self):
        num = 0
        for i in self.path:
         num += i.value

        return num
    #Straight Line Distance
    def hSLD(self, node):

        #calculate sldistance between two points
        for i in self.searchNodesList:
            if i.label == node.label:
                pointA = i.coordinates
                pointA =(pointA[0], pointA[1])

        for i in self.goalNodesArray:
            pointB = i.coordinates
            goalPoint = (pointB[0],pointB[1])

        dist = distance.euclidean(pointA, goalPoint)

        return dist

        print("Distance between points is %d" % (dist) )
        print("\n")

    #Hdir
    def hDIR(self):
        return
    
    def showOpenList(self):

        print("Open list is as follows: ")
        for open in self.openList:

            print("label: %s, Value %d" % (open.label, open.value) )
        print("\n")

    def generateSuccessors(self, currNode, isBest, stats):

        self.successorArray = []

        if isBest:
            currNode.successors.sort(key = lambda c: c[1])

        for i in currNode.successors:
            i[0].value += i[1]
            self.successorArray.append(i[0])

        if not isBest:
            self.successorArray.sort(key = lambda c: c.label)

        # for i in self.successorArray:
        #     print("Successor: %s with value %d" % (i.label, i.value) )
        # print("\n")


        # self.openList.remove(currNode)

        # for i in successorArray:
        #     self.openList.append(i)

        stats.avgBranchFactor(self.successorArray)

    def insert(self,insertType, stats):

        #handle duplicate nodes being inserted
        for i in self.openList:
            for j in self.successorArray:
                if i.label == j.label:
                    self.successorArray.remove(j)

        for i in self.successorArray:
            if i.label in self.history:
                self.successorArray.remove(i)

        if insertType == "front":
            for i in self.successorArray:
                self.openList.insert(0, i)

        elif insertType == "back":  
            for i in self.successorArray:
                self.openList.append(i)
        
        elif insertType == "order":
            count = 0
            #sort by value of cheapest node
            for i in self.successorArray:
                self.openList.insert(count, i)
                count += 1

        else:
            print("Bad insert type")
            return

        stats.openListSize(self.openList)
    

    def bfs(self, grapher, stats):
        #run bfs search to be recursively called
        ##edge array will keep track of next to be explored edges
        edgeArray = []

        #generate successor array first
        #self.showOpenList()
        nodeToOpen = self.openList.pop(0)
        self.path.append(nodeToOpen)

        self.expansions += 1

        self.history.append(nodeToOpen.label)
        grapher.exploreNode(nodeToOpen.label, [self.prevNode, nodeToOpen.label])

        #check if we reached goal node
        if nodeToOpen in self.goalNodesArray:
            for i in self.goalNodesArray:
                if nodeToOpen == i:
                    self.finishedGoals.append(i)
                    self.goalNodesArray.remove(i)
            print("GoalHit")
            if len(self.goalNodesArray) == 0:
                print("Success in finding node in BFS")
                print("The search ended at node: %s" % (nodeToOpen.label))
                return

        self.prevNode = nodeToOpen.label
        self.generateSuccessors(nodeToOpen, False, stats)

        #grapher.exploreEdges(nodeToOpen.label, edgeArray)
        #insert successors to front of open list
        self.insert("back", stats)

        #now the currently explored node is at the front of the list
        self.bfs(grapher, stats)


    def dfs(self, grapher, stats):
        #Run the dfs search to be called recursively
        edgeArray = []

        #first explore the node on the top of open list
        nodeToOpen = self.openList.pop(0)
        self.path.append(nodeToOpen)
        self.expansions += 1


        self.history.append(nodeToOpen.label)

        grapher.exploreNode(nodeToOpen.label, [self.prevNode, nodeToOpen.label])
        
        #check if we reached goal node
        if nodeToOpen in self.goalNodesArray:
            for i in self.goalNodesArray:
                if nodeToOpen == i:
                    self.finishedGoals.append(i)
                    self.goalNodesArray.remove(i)
            print("GoalHit")
            if len(self.goalNodesArray) == 0:
                print("Success in finding node in DFS")
                print("The search ended at node: %s" % (nodeToOpen.label))
                return

        self.prevNode = nodeToOpen.label
        self.generateSuccessors(nodeToOpen, False, stats)

        for i in self.successorArray:
            edgeArray.append(i.label)

        #grapher.exploreEdges(nodeToOpen.label, edgeArray)

        #insert into front since dfs iwll explore the first child of every new node opened
        self.insert("front", stats)

        self.dfs(grapher, stats)

    def best(self, grapher, stats):
        #Best first search implementation

        nodeToOpen = self.openList.pop(0)
        self.path.append(nodeToOpen)

        self.history.append(nodeToOpen.label)
        self.expansions += 1

        grapher.exploreNode(nodeToOpen.label, [self.prevNode, nodeToOpen.label])

        #check if we reached goal node
        if nodeToOpen in self.goalNodesArray:
            for i in self.goalNodesArray:
                if nodeToOpen == i:
                    self.finishedGoals.append(i)
                    self.goalNodesArray.remove(i)
            print("GoalHit")
            if len(self.goalNodesArray) == 0:
                print("Success in finding node in Best First")
                print("The search ended at node: %s" % (nodeToOpen.label))
                return

        self.prevNode = nodeToOpen.label

        self.generateSuccessors(nodeToOpen, True, stats)

        self.insert("order", stats)

        self.best(grapher, stats)

    def aStar(self, grapher, stats):
        #A* implementation

        nodeToOpen = self.openList.pop(0)
        self.path.append(nodeToOpen)
        self.expansions += 1

        self.history.append(nodeToOpen.label)

        grapher.exploreNode(nodeToOpen.label, [self.prevNode, nodeToOpen.label])

        #check if we reached goal node
        if nodeToOpen in self.goalNodesArray:
            for i in self.goalNodesArray:
                if nodeToOpen == i:
                    self.finishedGoals.append(i)
                    self.goalNodesArray.remove(i)
            print("GoalHit")
            if len(self.goalNodesArray) == 0:
                print("Success in finding node in A*")
                print("The search ended at node: %s" % (nodeToOpen.label))
                return

        self.prevNode = nodeToOpen.label

        self.generateSuccessors(nodeToOpen, False, stats)

        #find the lowest SLD 
        mini = 0
        minNode = nodeToOpen
        for i in self.successorArray:
            if mini == 0:
                mini = self.hSLD(i)
            if self.hSLD(i) < mini:
                minNode = i
                mini = self.hSLD(i)

        self.successorArray.insert(0, minNode)

        self.insert("order", stats)

        self.aStar(grapher, stats)


class SearchStats:

    def __init__(self):
        self.avgOpenListSize = 0
        self.maxOpenListSize = 0
        self.listTimesChecked = 0

        self.avgDepth = 0
        self.maxDepth = 0

        self.avgBranchingFactor = 0
        self.listBranchFChecked = 0

    def openListSize(self, list):

        #calculaate the open list size
        self.listTimesChecked += 1
        self.avgOpenListSize += len(list)

        if self.maxOpenListSize == 0:
            self.maxOpenListSize = len(list)
        if len(list) > self.maxOpenListSize:
            self.maxOpenListSize = len(list)

    def calculcateAvgOpenlist(self):
        return self.avgOpenListSize / self.listTimesChecked

    def avgBranchFactor(self, list):
        self.listBranchFChecked += 1
        self.avgBranchingFactor += len(list)
        
    def calculateAvgBranch(self):
        return self.avgBranchingFactor / self.listBranchFChecked


def main():
    grapher = GraphViz()
    mainSearch = Searcher("30node.txt")
    mainSearch.loadMap()
    mainSearch.performSearch("A*", "U", ["E", "T"], 0, False, grapher)
    wait = input("wait")

if __name__ == "__main__":
    main()
