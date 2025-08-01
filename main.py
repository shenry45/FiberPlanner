import random
import json
import os
import time

color_order = ["blue", "orange", "green", "brown", "slate", "white", "red", "black", "yellow", "violet", "rose", "aqua"]
nodes = dict()
links = dict()
strands = dict()

### FIBER NODE FN's ###
def showFiberLinks(nodeID):
    result = []
    for fiber in nodeID["linkedFiber"]:
        current_fiber = links.get(fiber)

        if current_fiber == None:
            continue

        result.append(f" ({current_fiber['id']}) {current_fiber['identity']} with {current_fiber['count']} fibers")

    result = ", ".join(result)

    print(result)

def showSplitters(nodeID):
    result = ""
    for splitter in nodeID["linkedSplitters"]:
        result += f" {splitter}"

    print(result)

def updateNodeComment(nodeID, comment):
    nodes[nodeID]["comment"] = comment





### FIBER LINKS FN's ###
def generateStrands(linkID, fiberCount):
        tube_pos = 0
        strand_pos = 0
        for _ in range(fiberCount):            
            createFiberStrand(
                tube=color_order[tube_pos],
                color=color_order[strand_pos],
                parentLink=linkID
            )

            if strand_pos == 11:
                strand_pos = 0
                tube_pos += 1
            else:
                strand_pos +=1

# TODO FN Need to verify strand linked count matches the actual strand count

def showAvailableStrands(linkID):
    print(links[linkID])
    count = 0
    colors = []
    for strandID in links[linkID]["linkedStrands"]:
        if strands[strandID]["feederStrand"] != 0 or strands[strandID]["nextStrand"] != 0:
            continue
        count += 1
        colors.append(f"{strands[strandID]['tube']} {strands[strandID]['color']}")

    print(f"Link {links[linkID]['identity']} has {count} available strands and the colors are {colors}.")

def linkFiberToNode(nodeID, linkID, linkType):
    print(nodeID, linkID, linkType)
    print(nodes[nodeID]["linkedFiber"])

    nodes[nodeID]["linkedFiber"].append(linkID)

    print(nodes[nodeID]["linkedFiber"])

    if linkType == "backhaul":
        links[linkID]["backhaulNode"] = nodeID
    else:
        links[linkID]["parentNode"] = nodeID

def unlinkFiberToNode(nodeID, linkID):
    nodes[nodeID]["linkedFiber"].remove(linkID)

    if nodeID == links[linkID]["backhaulNode"]:
        links[linkID]["backhaulNode"] = 0
    elif nodeID == links[linkID]["panretNode"]:
        links[linkID]["panretNode"] = 0

def updateLinkComment(linkID, comment):
    links[linkID]["comment"] = comment







### STRANDS FN's ###

def linkFiberStrands(backhaulStrandID, newStrandID):
    # If strand already spliced, reset previous
    if strands[backhaulStrandID]["nextStrand"] != 0:
        prevStrand = strands[backhaulStrandID]["nextStrand"]
        strands[prevStrand]["feederStrand"] = 0
    
    # If strand already spliced, reset previous
    if strands[newStrandID]["feederStrand"] != 0:
        prevStrand = strands[newStrandID]["feederStrand"]
        strands[prevStrand]["nextStrand"] = 0

    strands[backhaulStrandID]["nextStrand"] = newStrandID
    strands[newStrandID]["feederStrand"] = backhaulStrandID








### CREATION FN's ###

def createFiberNode(linkedFiber:list=[], linkedSplitters:list=[], identity="TBD", spliceCase:str="", container:str="", comment:str=""):
    print('create node')
        # "id": random.randint(0,99999999),
    node = {
        "id": random.randint(0,50),
        "linkedFiber": linkedFiber[:],
        "linkedSplitters": linkedSplitters[:],
        "identity": identity,
        "spliceCase": spliceCase,
        "container": container,
        "signal": 2,
        "comment": comment
    }
    nodes.update({node["id"]: node})

    return node["id"]

def createFiberLink(backhaulNode:int=0, parentNode:int=0, linkedStrands:list=[], fiberCount:int=1, identity="TBD", comment:str=""):
    print('create link')
        # "id": random.randint(0, 99999999),
    link = {
        "id": random.randint(0, 50),
        "backhaulNode": backhaulNode,
        "parentNode": parentNode,
        "linkedStrands": linkedStrands[:],
        "identity": identity,
        "count": fiberCount,
        "comment": comment
    }
    links.update({link["id"]: link})
    generateStrands(link["id"], fiberCount)

    return link["id"]

def createFiberStrand(parentLink:int=0, parentSplitter:int=0, feederStrand:int=0, nextStrand:int=0, tube:str="blue", color:str="TBD", comment:str=""):
    parentLink = int(parentLink)
    strand = {
        "id": random.randint(0, 50),
        "parentLink": parentLink,
        "parentSplitter": parentSplitter,
        "feederStrand": feederStrand,
        "nextStrand": nextStrand,
        "tube": tube,
        "color": color,
        "comment": comment,
    }
    strands.update({strand["id"]: strand})
    links[parentLink]["linkedStrands"].append(strand["id"])

def calculateFiberSignal(strandID):
    current_strand = strands[strandID]
    while current_strand["feederStrand"] != 0:
        current_strand = strands["feederStrand"]

    print(nodes[current_strand]["signal"])
 




### DATABASE ###

def readProject(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data

def updateDatabase():
    os.remove("database.json")
    all_data = {
        "nodes": nodes,
        "links": links,
        "strands": strands
    }

    with open("database.json", "w") as f:
        json.dump(all_data, f)

def wipeDatabase():
    os.remove("database.json")
    blank = {
        "nodes": {},
        "links": {},
        "strands": {}
    }
    time.sleep(1)

    with open("database.json", "w") as f:
        json.dump(blank, f)


data = readProject("database.json")
nodes = data["nodes"]
links = data["links"]
strands = data["strands"]

def main():
    node_1 = createFiberNode(identity="Number 1")
    node_2 = createFiberNode(identity="Number 2")
    node_3 = createFiberNode(identity="Number 3")

    link_2 = createFiberLink(fiberCount=2, identity="Main")
    link_3 = createFiberLink(fiberCount=2, identity="Sub")

    linkFiberToNode(node_1, link_2, "")

    linkFiberToNode(node_2, link_2, "backhaul")
    linkFiberToNode(node_2, link_3, "")
    linkFiberToNode(node_3, link_3, "backhaul")

    # linkFiberStrands(56923980, )

    # showAvailableStrands(hhh)

    # calculateFiberSignal()

    updateDatabase()


if __name__ == "__main__":
    # wipeDatabase()
    main()