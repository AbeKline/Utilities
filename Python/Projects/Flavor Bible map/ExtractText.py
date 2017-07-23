import sys
import io
import networkx as nx
import matplotlib.pyplot as plt


speedFactor = 1000
strengths = [60,20,5,1]
ingredients = []
topIngredient = '<p class="h">'
basic = '<p class="bl1">'
bold = '<strong class="calibre1">'
strong = '</strong>'
sp = '</p>'
#length = 0
filelist = open("Filelists\\Chapter3.txt")

class TopLevelIngredient:
    graph = nx.Graph()
    def __init__(self, name):
        self.name = name
        self.pairings = []
        self.strengths = []
        self.attributes = {}
        self.combinations = []
        self.random = []
    def addAttribute(self,type,attribute):
        if (len(type)>0 and len(attribute)>0):
            if '–' in attribute:
                #if there is an m-dash in the line, it is between seasons. This splits that range and adds both per StackOverflow 10973766
                [(self.addAttribute(type, a) for a in snipOut(attribute,'–'))]
            elif type in self.attributes:
                if attribute not in self.attributes[type]:
                    self.attributes[type] += attribute
            else:
                self.attributes[type] = attribute
    def addPairing(self, name, strength):
        if '+' in name:
            self.combinations.append(name) #strengths will always be 1
        else:
            self.pairings.append(name)
            self.strengths.append(strength)
            self.graph.add_edge(self.name.lower(), name.lower(), weight = strength)
    def print(self):
        print(self.name)
    def printPairings(self):
        tp = 'Pairings: '
        for i in range(len(self.pairings)):
            tp += '[' + self.pairings[i] + ':' + str(self.strengths[i]) + '], '
        print(tp)

def printIngredientList():
    for i in ingredients:
        i.print()
def printList(l):
    for i in l:
        print(i)

def classify(line):
    retval = 'unknown'
    if line.find(topIngredient) > -1:
        return 'toplevelingredient'
    if basic in line:
        if bold in line:
            if ':' in line:
                return 'attribute'
        return 'subItem'
    return retval

def parseP(line, start):
    li = line.find(start)
    ri = line.find(sp)
    line = line[li + len(start):ri]
    return line

def snipOut(line, crap):
    l = len(crap)
    i = line.find(crap)
    if i > -1:
        return line[0: i].strip(), line[i + l:].strip()
    return line,''

def parseTopLevelIngredient(line):
    line = parseP(line, topIngredient)
    if '<' in line:
        line = line[0:line.find('<')]
    return line

def strengthCheck(suba):
    if bold in suba:
        if '*' in suba: #0, strongest recommendation
            #PP is stripping out the identifying tag, then we strip out the /strong and send bag an arglist of the attribute and it's strength.
            return ''.join(snipOut(parseP(suba+sp,bold),strong))[1:], strengths[0] #I'm proud of this line
        elif suba[len(bold)+1].isupper():
            return ''.join(snipOut(parseP(suba+sp,bold),strong)), strengths[1]
        else:
            return ''.join(snipOut(parseP(suba + sp, bold), strong)), strengths[2]
    else:
        return suba,strengths[3]

def parseSubIngredient(line): #strips the p tag, then runs it through the strcheck engine, stripping out formatting as it goes
    return strengthCheck(parseP(line, basic))

def parseAttribute(line): #remove the p tag and the boldness, then split on : to get the type of attribute, value
    return snipOut(parseP(line,basic+bold), ':'+strong)


if __name__ == '__main__':
    #loop through all the letters of the alphabet
    for filename in filelist:
        #open file
        file = open(filename.strip('\n'),"rb")
        #prepare some variables
        currentIngredient = TopLevelIngredient('')
        tliCounter = 0
        #loop through each line of the book
        for line in file:
            line = line.decode('utf-8')
            #length += len(line)
            lineType = classify(line)
            if lineType == 'toplevelingredient':
                tliCounter += 1
                if tliCounter%speedFactor == 0:
                    print('Name: ',currentIngredient.name)
                    currentIngredient.printPairings()
                    print('Attributes: ', str(currentIngredient.attributes))
                    if currentIngredient.combinations:
                        print('combos: ', currentIngredient.combinations)
                currentIngredient = TopLevelIngredient(parseTopLevelIngredient(line))
                ingredients.append(currentIngredient)
            elif lineType == 'subItem':
                currentIngredient.addPairing(*parseSubIngredient(line))
            elif lineType == 'attribute':
                currentIngredient.addAttribute(*parseAttribute(line))
            elif lineType == 'unknown':
                currentIngredient.random.append(line)
            #print (line)

    # nx.draw(TopLevelIngredient.graph)
    # plt.draw()

    #print(len(TopLevelIngredient.graph.nodes()))
    #printIngredientList()
    #print (len(ingredients))
    # for i in ingredients:
    #     print(i.name)

        nx.write_graphml(currentIngredient.graph, "Output\\flavorBibleGraph.xml")

# graph = currentIngredient.graph
# nx2tikz --input ExtractText.py --output out --format pdf
#print(length)
