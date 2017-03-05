import sys,getopt

class HeapEntry():
    def __init__(self):
        self.hDegree = 0
        self.hLeftSib = None
        self.hRightSib = None
        self.hParent = None
        self.hChild = None
        self.hChildCut = False
        self.hElem = None
        self.hHashTag = None

class FibonacciHeap:

    def HeapInit(self,elem,hHashTag):
        node = HeapEntry()
        node.hRightSib = node
        node.hLeftSib = node
        node.hHashTag = hHashTag
        node.hElem = int(elem)
        return node
    
    # pointer to the max element
    hMax = None
    root_list = None
    degreeMap = {}
            
    # insert new node into un ordered root list in O(1) time
    def insertNode(self,newNode):
            if self.hMax == None:
                self.hMax = newNode
                self.hMax.hParent = None
                self.hMax.hLeftSib = self.hMax
                self.hMax.hRightSib = self.hMax
                self.hMax.hChildCut = False
                #print "hMax: " + str(self.hMax.hElem)
                
            else:
                #print "hMax and newNode: " + str(self.hMax.hElem) + " "+ str(newNode.hElem)
                self.hMax = self.InsertIntoRootList(self.hMax,newNode)
                #print "hMax in else: " + str(self.hMax.hElem)

            print self.hMax.hElem 
            maxNodeTemp = self.hMax.hLeftSib
            currNode = self.hMax
            while currNode is not maxNodeTemp:
                if currNode.hRightSib.hElem > self.hMax.hElem:
                    self.hMax = currNode.hRightSib
                currNode = currNode.hRightSib
            print "FInal hMax: " + str(self.hMax.hElem)      

    # function to iterate through a doubly linked list
    def iterate_(self,head):
        print "---------------entered in iterate---------------"
        start = head
        next_start = start.hLeftSib
        print "Doubly Circular Linked list: "
        while start is not next_start:
            print (start.hElem)
            start = start.hRightSib
        print start.hElem
        print "----------------exit iteration------------------"
            
    def InsertIntoRootList(self,oldNode,newNode):
        if oldNode == None and newNode == None:
            return None

        elif oldNode != None and newNode == None:
            return oldNode

        elif oldNode == None and newNode != None:
            newNode.hParent = None
            newNode.hChildCut = False
            if newNode.hDegree == 0:
                newNode.hChild = None
            return newNode

        else:
            valNext = oldNode.hRightSib
            oldNode.hRightSib = newNode
            oldNode.hRightSib.hLeftSib = oldNode
            newNode.hRightSib = valNext
            newNode.hRightSib.hLeftSib = newNode
            newNode.hParent = None
            newNode.hCHildCut = False
            if newNode.hDegree == 0:
                newNode.hChild = None
            if oldNode.hElem > newNode.hElem:
                return oldNode
            else:
                return newNode
        
        
    def increase_key(self,node,newVal):
        print "Entered in increase key"
        node.hElem = node.hElem + int(newVal)    # change the value at node to new larger value
        cacheParent = node.hParent          # the parent of the nofe is stored
        # check to see if the child node's count value is grater than its parent
        
        if cacheParent is not None and node.hElem > cacheParent.hElem:
            # cut() and cascading_cut(): cut the node from its parent node and cascade into root node
            self.cut(node,cacheParent)
            self.cascading_cut(cacheParent)
        # new node with larger count becomes hMax    
        if node.hElem > self.hMax.hElem:
            self.hMax = node
            print "Final hMax: " + str(self.hMax.hElem)
        return None

    # if a child node becomes greater than its parent node we
    # cut this chold node off and bring it up to the root list
    
    def cut(self,childNode,parentNode):

        print "Entered in cut"
        #set the parent of the node to removed to null
        childNode.hParent = None
            
        # when the childnode has siblings,set the right sibling as new child
        if parentNode.hChild == childNode and childNode.hRightSib != childNode:
            parentNode.hChild = childNode.hRightSib
            childNode.hLeftSib.hRightSib = childNode.hRightSib
            childNode.hRightSib.hLeftSib = childNode.hLeftSib

        elif parentNode.hChild != childNode and childNode.hRightSib != childNode:
            childNode.hLeftSib.hRightSib = childNode.hRightSib
            childNode.hRightSib.hLeftSib = childNode.hLeftSib

        else:
            parentNode.hChild = None

        childNode.hRightSib = childNode.hLeftSib = childNode
        childNode.hChildCut = False     #childcut is set to false
        parentNode.hDegree = parentNode.hDegree - 1 #decrease the degree of parent node
        self.insertNode(childNode)
    
        
    def cascading_cut(self,parentNode):
        grandParentNode = parentNode.hParent
        if grandParentNode != None:
            if parentNode.hChildCut == False:
                parentNode.hChildCut = True
            else:
                self.cut(parentNode,grandParentNode)
                self.cascading_cut(grandParentNode)
        return None

    # remove the max node from the heap
    def RemoveMax(self):
        cacheMaxNode = self.hMax        # need to return this to calling function
        if self.hMax.hRightSib == self.hMax:    # for a single node at root
            self.hMax = None                    # set the max pointer to null and heap becomes empty
            self.AddChildren2Root(cacheMaxNode) # add the children of max node to root
        else:
            self.hMax.hRightSib.hLeftSib = self.hMax.hLeftSib
            self.hMax.hLeftSib.hRightSib = self.hMax.hRightSib
            rightChild = cacheMaxNode.hRightSib
            self.hMax = None
            self.hMax = rightChild
            self.AddChildren2Root(cacheMaxNode)
            currPointer = self.hMax
            while True:
                if currPointer.hRightSib.hElem > self.hMax.hElem:
                    self.hMax = currPointer.hRightSib
                currPointer = currPointer.hRightSib
                if currPointer == rightChild:
                    break

            self.RecursiveMerge(self.hMax)
            self.degreeMap = {}
            cacheMaxNode.hLeftSib = cacheMaxNode
            cacheMaxNode.hRightSib = cacheMaxNode
            cacheMaxNode.hParent = None
            cacheMaxNode.hChild = None
            cacheMaxNode.hDegree = 0
            return cacheMaxNode

    # this method recursively combines modes until two nodes have the same degree
    def RecursiveMerge(self,pairNode1):
        while True:
            degree = pairNode1.hDegree
            if degree in self.degreeMap:
                if pairNode1 != self.degreeMap[degree]:
                    pairNode2 = self.degreeMap[degree]
                    del self.degreeMap[degree]
                    parentNode = self.CombineThePairs(pairNode1,pairNode2)
                    pairNode1 = parentNode
                    self.RecursiveMerge(pairNode1)
                    return
            else:
                self.degreeMap[degree] = pairNode1       #update table with this node and degree

            pairNode1 = pairNode1.hRightSib
            if pairNode1 == self.hMax:
                break

    def CombineThePairs(self,pairNode1,pairNode2):
        if pairNode1 == self.hMax or pairNode2 == self.hMax:
            if pairNode1 == self.hMax:
                pairNode2.hLeftSib.hRightSib = pairNode2.hRightSib
                pairNode2.hRightSib.hLeftSib = pairNode2.hLeftSib
                parentNode = pairNode1
                childNode = pairNode2
            else:
                pairNode1.hLeftSib.hRightSib = pairNode1.hRightSib
                pairNode1.hRightSib.hLeftSib = pairNode1.hLeftSib
                parentNode = pairNode2
                childNode = pairNode1
        elif pairNode1.hElem > pairNode2.hElem:
            pairNode2.hLeftSib.hRightSib = pairNode2.hRightSib
            pairNode2.hRightSib.hLeftSib = pairNode2.hLeftSib
            parentNode = pairNode1
            childNode = pairNode2
        else:
            pairNode1.hLeftSib.hRightSib = pairNode1.hRightSib
            pairNode1.hRightSib.hLeftSib = pairNode1.hLeftSib
            parentNode = pairNode2
            childNode = pairNode1

        if parentNode.hDegree == 0:
            parentNode.hChild = childNode
            childNode.hParent = parentNode
            childNode.hRightSib = childNode
            childNode.hLeftSib = childNode
        else:
            childNode.hRightSib = childNode
            childNode.hLeftSib = childNode

            defaultChild = parentNode.hChild
            valNext = defaultChild.hRightSib
            defaultChild.hRightSib = childNode
            defaultChild.hRightSib.hLeftSib = defaultChild
            childNode.hRightSib = valNext
            childNode.hRightSib.hLeftSib = childNode
            childNode.hParent = parentNode
        parentNode.hDegree = parentNode.hDegree + 1
        return parentNode
        
    # this method adds the children of a removed node to root node list    
    def AddChildren2Root(self,removedChild):
        tempNode = removedChild.hChild
        if removedChild.hDegree == 0:       # max node has no child
            return
        elif removedChild.hDegree == 1:     # max node has only one child
            self.insertNode(tempNode)

        else:
            # max node has more than one child
            for i in range(removedChild.hDegree):
                currChild = removedChild.hChild
                removedChild.hChild = currChild.hRightSib
                currChild.hRightSib = currChild
                currChild.hLeftSib = currChild
                self.insertNode(currChild)
        removedChild.hChild = None
        return
    
def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts,args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'fib.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print 'fib.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i","--ifile"):
            inputfile = arg
        elif opt in ("-o","--ofile"):
            outputfile = arg

    F_input = open(inputfile,'r')
    F_output = open(outputfile,'w')
    hm = {}                      # keep track of node,value
    heap = FibonacciHeap()
    
    for line in F_input:
        readHashTag = line
        first = readHashTag[0]
        if first == "#":
            hashTag = readHashTag[1:].split()[0]
            hashTagCount = readHashTag[1:].split()[1]
            if hashTag in hm:
                print "Implement increasekey"
                heap.increase_key(hm[hashTag],hashTagCount)
            else:
                node = heap.HeapInit(hashTagCount,hashTag)
                hm[hashTag] = node
                heap.insertNode(node)
                
        elif (first == 's' or first == 'S'):
            print "stop"
            heap.iterate_(hm[hashTag])
            F_input.close()
            sys.exit()

        else:
            query = int(readHashTag)
            node = HeapEntry()
            key = {}
            value = {}
            for i in range(query):
                #node = HeapEntry()
                #print node.hHashTag
                node = heap.RemoveMax();
                print node.hHashTag
                key[i] = node.hHashTag
                value[i] = node.hElem
                F_output.write(key[i])
                if(i < query-1):
                    F_output.write(",")

            for j in range(query):
                node = heap.HeapInit(value[j],key[j])
                hm[key[j]] = node
                heap.insertNode(node)
            F_output.write("\n")
            print "query encounterd: " + str(query)
            

    
    F_input.close()
    F_output.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
