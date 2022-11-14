import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import itertools

                                    ### csv reader
def readAndMake(counter): #when calling use for loop to increase counter by 1 each time you call to change file path 
    
    path = "C:\\Users\\tejus\\Dropbox\\csv exports\\small_csv\\SMALL_"+str(counter)+".csv"       #tejus for laptop tejush badal for pc
    #path = "C:\\Users\\tejus\\Dropbox\\csv exports\\med_csv\\MED_"+str(counter)+".csv"
    #path = "C:\\Users\\tejush badal\\Dropbox\\csv exports\\large_csv\\LARGE_"+str(counter)+"_CSV"+".csv"
    #path = "C:\\Users\\tejush badal\\Dropbox\\csv exports\\xl_csv\\XL_"+str(counter)+"_CSV"+".csv"
    df = pd.read_csv(path)
    df = df.drop([0], axis=0) #this deletes the first row since its not needed
    df = df.rename(columns ={"Unnamed: 0": "node_type"}) #gives a name to the first column for ease of access


   
                         #intializing some temp variables for iterating through column 
    listoflists = []
    numOfClass = 0
    index = 0
                                #get indices of columns to loop through by name later on since different file will export with different number of columns
    columns = df.columns
    generalName = "General"
    specificName = "Specific"
    fromName = "From"
    toName = "To"
    parentName = "Parent Name"
    generalIndex = columns.get_loc(generalName)
    specificIndex = columns.get_loc(specificName)
    fromIndex = columns.get_loc(fromName)
    toIndex = columns.get_loc(toName)
    parentIndex = columns.get_loc(parentName)
                                #### now for associations etc to connect the branches
                                #This giant for loop here references the ID associated with each node and turns it into an edgelist using the ID's

    #get the number of classes 
    for row in df["node_type"]:
       if row == "Class":
           numOfClass+=1
                                #iterate through and add attributes/operations to list, append to list of lists
    while True:
        tempList = []
        classList = []
        for row,name,number, parent in zip(df.iloc[:, 0], df.iloc[:, 2], df.iloc[:, 1], df.iloc[:, parentIndex]): #iterates through first and third row of dataframe
            if row == "Class":
                classList.append(name)
                index += 1
                if index > 1:
                    listoflists.append((list(tempList)))
                    tempList.clear()
            elif row == "Attribute" or row == "Operation":
                tempList.append(name+"_"+parent) 
        if index == numOfClass:
           listoflists.append((list(tempList)))
           break

    #print(listoflists)
    #print (classList)

                                ##### creating a dataframe to act as an edgelist 
    templist2 = []
    edgeList = []
    for l, j in zip(listoflists, classList): #NOTE: DO NOT use 'List' as variable name in for loop, will mess up the append, its a keyword not good syntax
        for element in l:
            templist2.append(element)
            templist2.append(j)

            edgeList.append(list((templist2)))
            templist2.clear()
    #print (edgeList)
                                #### now for associations etc to connect the branches
                                #This giant for loop here references the ID associated with each node and turns it into an edgelist using the ID's

    AssoIDlist = []
    tempedgelist = []
    for first,ID,name,From,to,general,specific in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2], df.iloc[:, fromIndex], df.iloc[:, toIndex], df.iloc[:, generalIndex], df.iloc[:, specificIndex]):
        if first == "Association":
            AssoIDlist.append(ID)
            AssoIDlist.append(int(From))
            tempedgelist.append(list((AssoIDlist)))
            AssoIDlist.clear()
       
            AssoIDlist.append(ID)
            AssoIDlist.append(int(to))
            tempedgelist.append(list((AssoIDlist)))
            AssoIDlist.clear()
                                        #leave constraints for now since unique name ID will be difficult e.g. two XOR's will act as one
        elif first == "Generalization":
            AssoIDlist.append(ID)
            AssoIDlist.append(int(general))
            tempedgelist.append(list((AssoIDlist)))
            AssoIDlist.clear()
        
            AssoIDlist.append(ID)
            AssoIDlist.append(int(specific))
            tempedgelist.append(list((AssoIDlist)))
            AssoIDlist.clear()
                       
    #print (tempedgelist)                                    
                               # take the temporary edgelist and put it into master edgelist with names

    #print(df.iloc[:, 2])                           
    temp4 = []
    tempName = '' 
    genspecName = ''
    counter = 0
    for s in tempedgelist:
        for g in s:
            for f,h,d,gen,fro,spec,to in zip(df.iloc[:, 2], df.iloc[:,0], df.iloc[:, 1],df.iloc[:, generalIndex],df.iloc[:, fromIndex], df.iloc[:, specificIndex], df.iloc[:, toIndex]): #f is names, d is ID list, h is node type 
               if g == d:#if the temp list ID matches the ID in that certain row
                    if pd.isna(f) == True: #check for empty names (nan)

                        if h == "Generalization":
                            for x,y in zip(df.iloc[:, 1], df.iloc[:, 2]): #x is ID, y is name 
                                if gen == x:
                                    if genspecName.endswith('_'):   # this if else is to make sure that the general class is first regardless of internal ID
                                        temphold = y+"_"
                                        temphold += genspecName
                                        genspecName = temphold
                                        counter+=1
                                        #print(genspecName)
                                    else:
                                        genspecName += y + "_"
                                        counter +=1
                                    if counter == 2:
                                        tempName = h+"_"+genspecName 
                                        #print(tempName)
                                        temp4.append(tempName)
                                        tempName = ''
                                        genspecName = ''
                                        temphold = ''
                                        counter = 0
                                        if len(temp4) == 2:#this is so that the edgelist only has 2 columns for the dataframe to reference
                                            #print(temp4)
                                            edgeList.append(list((temp4)))
                                            temp4.clear()           
                                if spec == x:
                                    genspecName += y +"_"
                                    counter +=1
                                    if counter == 2:
                                        tempName = h+"_"+genspecName 
                                        #print(tempName)
                                        temp4.append(tempName)
                                        tempName = ''
                                        genspecName = ''
                                        counter = 0
                                        if len(temp4) == 2:#this is so that the edgelist only has 2 columns for the dataframe to reference
                                            #print(temp4)
                                            edgeList.append(list((temp4)))
                                            temp4.clear()
                               

                        if h == "Association":
                            for x,y in zip(df.iloc[:, 1], df.iloc[:, 2]): #x is ID, y is name 
                                if fro == x:
                                   if genspecName.endswith('_'):   # this if else is to make sure that the from class is first regardless of internal ID
                                        temphold = y+"_"
                                        temphold += genspecName
                                        genspecName = temphold
                                        counter+=1
                                        #print(genspecName)
                                   else:
                                        genspecName += y + "_"
                                        counter +=1
                                   if counter == 2: #so that the genspec name only loops through src and target nodes once 
                                        tempName = h+"_"+genspecName
                                        #print(tempName)
                                        temp4.append(tempName)
                                        tempName = ''
                                        genspecName = ''
                                        counter = 0
                                        if len(temp4) == 2:#this is so that the edgelist only has 2 columns for the dataframe to reference
                                            #print(temp4)
                                            edgeList.append(list((temp4)))
                                            temp4.clear()
                                if to == x:
                                    genspecName += y+"_"
                                    counter +=1
                                    if counter == 2: #so that the genspec name only loops through src and target nodes once 
                                        tempName = h+"_"+genspecName
                                        #print(tempName)
                                        temp4.append(tempName)
                                        tempName = ''
                                        genspecName = ''
                                        counter = 0
                                        if len(temp4) == 2:#this is so that the edgelist only has 2 columns for the dataframe to reference
                                            #print(temp4)
                                            edgeList.append(list((temp4)))
                                            temp4.clear()

                    else:
                        temp4.append(f)
                    if len(temp4) == 2:
                        #print(temp4)
                        edgeList.append(list((temp4)))
                        temp4.clear()
    #print(edgeList)
    #makeGraph(edgeList) ##### dont call this yet when the program is going through, need to return master elist to makeGraph 
    
    return (edgeList)
                                    ### nodelist maker
def nodelist(edgeL):
    nodelist = []
    finalnodelist = []
    for y in edgeL:
        for x in y:
            nodelist.append(x)
    finalnodelist = list(dict.fromkeys(nodelist)) #this removes all duplicates from the list by turning it into a dict with unique keys and casting to list type

    return(finalnodelist)
                                    ### node label positions                   
def nudge(pos, x_shift, y_shift): ## this is a function i found that will nudge the position in the graph up so I can implement labels above nodes

    return {n:(x + x_shift, y + y_shift) for n,(x,y) in pos.items()}
                                    ### versions to range 
def ranges(i):          # function that takes the list of versions and turns them into ranges. idk how this works got it from stackoverflow
    for a, b in itertools.groupby(enumerate(i), lambda pair: pair[1] - pair[0]):   
        b = list(b)
        yield b[0][1], b[-1][1]
                                    ###drawing the graph
def makeGraph (eList, edgelabelsdict, nodelabelsdict):
    
                                #create dataframe from edgelist
    df1 = pd.DataFrame(eList,
                       columns = ['tgt_node', 'src_node'])
    #print(df1.head())
                                #####creating the graph from edgelist
    graph = nx.from_pandas_edgelist(df1,
                                    source = "src_node",
                                    target = "tgt_node")
    pos= nx.spring_layout(graph,k = 0.15, iterations = 30,  scale = 6) 
    pos_nodes = nudge(pos,0,0.25) #incr the last paramter if u want it higher x,y coords
    #pos = nx.planar_layout(graph, scale = 1)   #this is if you dont want edges to overlap at all 
    mapping = {'Class3':'Online_Play'}
    nx.relabel_nodes(graph, mapping)
    plt.figure()
    nx.draw_networkx(graph,
                     pos,
                     font_size = 7.5,
                     bbox = dict(),
                     node_size = 300)
    nx.draw_networkx_edge_labels(graph,
                                 pos,
                                 edge_labels = edgelabelsdict,
                                 font_size = 6.5)
    nx.draw_networkx_labels(graph,
                            pos = pos_nodes,
                            labels = nodelabelsdict,
                            font_size = 6.5)
    #print(graph.degree)
    #print(graph.edges)
    #print(eList)
    plt.show()

    return graph.degree
                                    ###creating stal annotations
def stal (amountOfGraphs):
    masterEdgeList = []
    duplist = []
    tempDict = {}
    tempNodeDict = {}
    nodes = []
    versionNum = 1
    for x in range(amountOfGraphs): #the range is one less than the graph number it calls since graphs start @0
        #print(versionNum)
        #print(x)
        masterEdgeList.extend(readAndMake(x))
        duplist = readAndMake(x)
        duplist2 = duplist
        for m,y in zip(duplist, duplist2):  #stal for edges
            if m == y:
                if tuple(m) in tempDict:
                    if tempDict[tuple(m)].endswith(str(versionNum)):   ### this is to stop duplicate versions from printing e.g 1,2,2,3,3,3,4,4,4,4......
                        continue
                    else:
                        tempDict[tuple(m)] += ","+str(versionNum)    ### this assigns the version number 
                else:
                    tempDict[tuple(m)] = str(versionNum)    #### this is for new edges not previously seen
        nodes = nodelist(duplist)
        dupnodes = nodes
        for f,g in zip (nodes, dupnodes): #stal for nodes  
            if f == g:
                if f in tempNodeDict:
                    if tempNodeDict[f].endswith(str(versionNum)):
                        continue
                    else:
                        tempNodeDict[f] += ","+str(versionNum)
                else:
                    tempNodeDict[f]= str(versionNum)
        versionNum += 1

    #print(tempNodeDict)
             ##### now we format the values of the dictionary so that they arent so long e.g. 1,2,3,4,6 ----> 1-4,6
    newVal = []
    temp = []
    for key, value in tempDict.items():
        x = value.split(",")                    
        temp = list(map(int,x)) #this turns list of str into int to sort 
        #print (temp)
        newVal = list(ranges(temp)) #call the ranges function
        #print(newVal)         
        tempDict[key] = newVal
        newVal = []
                                        #this is the same thing as above just now for nodes instead of edges
    newNodeVal = []
    tempNode = []
    for key, value in tempNodeDict.items():
        x = value.split(",")                    
        tempNode = list(map(int,x)) #this turns list of str into int to sort 
        #print (temp)
        newNodeVal = list(ranges(tempNode)) #call the ranges function
        tempNodeDict[key] = newNodeVal
        newNodeVal = []
                                        ### cleaning up the way the range is returned to make it prettier                                   
    string = ''
    tempvalue = []
    for key, value in tempNodeDict.items():
        if value == [(1,amountOfGraphs)]:
            tempNodeDict[key] = "ALL"
        else:
            for x in value:
                if x[0] == x[1]:
                    string = str(x[0])
                    tempvalue.append(string)
                else:
                    string = str(x[0])+"-"+str(x[1])
                    tempvalue.append(string)
            tempNodeDict[key] = tempvalue
            tempvalue = [] 
            string = ''
                                    ### same loop as above copied just for edgelist dict
    for key, value in tempDict.items():
        if value == [(1,amountOfGraphs)]:
            tempDict[key] = "ALL"
        else:
            for x in value:
                if x[0] == x[1]:
                    string = str(x[0])
                    tempvalue.append(string)
                else:
                    string = str(x[0])+"-"+str(x[1])
                    tempvalue.append(string)
            tempDict[key] = tempvalue
            tempvalue = [] 
            string = ''
           
    #print(tempNodeDict)
    #print (tempDict)
    #print(masterEdgeList)
    makeGraph(masterEdgeList, tempDict, tempNodeDict)

stal(35)
