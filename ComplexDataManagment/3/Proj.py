##############################
##### Theocharis Kazakidis ###
#####        4679          ###
##############################
import sys
import heapq

k = int(sys.argv[1])
myHeap = []
scores = [5, 5]
isHeapReady = False
#id:score oswn exw dei
#mono osa den exw to plhres score. otan to vrw feygoun apo edw
lowerScore = {}
#krataei to arxeio apo to opoio to exw diavasei
readFrom = {}

#posa exw hdh dei olo to score
fullScore = []
#katwfli
T = 0
R = []
def readR():
    global R#H sinarthsh diabazei to arxeio rnd.txt kai pernei ta dedomena tis kathe grammis tou ksexwrizontas ta prwta me keno kai prosthetei ta score pou phra se mia lista twn score R
    infile = open("rnd.txt")
    R = []
    
    line = infile.readline()
    while line != '':
        tokens = line.split(' ')
        R.append(float(tokens[1]))
        line = infile.readline()
        
    return R

#fileId poio arxeio diavasa 1 h 2 (0 h 1)
def process(line, fileId):#sinartisi pou pernei ws orisma tin grammi kai to fileId gia na kserei pio arxeio diabazei opou sthn arxh pernei ta dedomena ksexwrizontas tou mesw tokens kai etsi pernei to id kai to score ths kathe grammis.Meta elexei ama to objectid pou diavase einai mesa sto lexiko lowerScore kai ama einai prosthetei sto objectScore thn timi toy objectScore tou objectid pou elenxe kai otan ginei auto ta petaei eksw apo to lexika lowerScore kai readFrom.Ama to flag isHeapReady einai false h ama to katwfli T einai megalitero apo to elaxisto stoixeio ths listas swrou tote prosthetei sto objectScore thn timi toy tou score tou antikeimenou me objectId.Epeita ama to myHeap einau mikroteros apo to top k(top antikeimena me to megaliter score)prostithete mia lista me ta ta score kai id sth lista swro.Alliws ama dhladh to k einai iso me th lista swro tote elenxw an to flag isHeapReady metatrepw thn lista swro myHeap me thn bohtheia ths sinartisis heapq.heapify(myHeap) se swro kai tote kanei to flag isHeapReady true.Meta sthn lista heapIds apothikeyontai ta id ths listas swrou kai checkarei ama ama to object id brisketai mesa sta heapid,ama den einai tote elenxei ama to top stoixeio ths myHeap einai mikrotero apo to objectScore kai ama einai tote to petaei apo thn myHeap me thn heapq.heappop kai prosthetei me thn heapq.heappush thn lista [objectScore, objectId].an to objectid einai idi sto heapids briskei to pou eina sto myHeap ta petaei eksw kai to apothikeyei sto item opws kai to objectscore tou opou ta apothikeyei se mia alli lista items.Ama den einai tote pusharei ta dedomena pou phre sto swro
    global myHeap, k, scores, lowerScore, readFrom, isHeapReady, T, R
    
    
    tokens = line.split(' ')
    objectId = int(tokens[0])
    objectScore = float(tokens[1])
    
    readFrom[objectId] = fileId
    
    scores[fileId] = objectScore

    if objectId in lowerScore.keys():
        objectScore = objectScore + lowerScore[objectId]
        lowerScore.pop(objectId)
        readFrom.pop(objectId)
    else:
        if isHeapReady == False or T > myHeap[0][0]:
            objectScore = objectScore + R[objectId]
            lowerScore[objectId] = objectScore
        
    if len(myHeap) < k:
        myHeap.append([objectScore, objectId])
    else:
        if isHeapReady == False:
            heapq.heapify(myHeap)
            isHeapReady = True
        
        heapIds = [x[1] for x in myHeap]
        
        if objectId not in heapIds:
            top = myHeap[0]
            if top[0] < objectScore:
                heapq.heappop(myHeap)
                heapq.heappush(myHeap, [objectScore, objectId])
        else:
            items = []
            while True:
                item = heapq.heappop(myHeap)
                if item[1] == objectId:
                    item[0] = objectScore
                    items.append(item)
                    break
                else:
                    items.append(item)
                    
            for item in items:
                heapq.heappush(myHeap, item)
    T = sum(scores) + 5

def checkStop():#H shnarthsh sygkrinei arxika ama to katwfli einai megalitero apo to top stoixeio tou myHeap,ama einai epistreei false giati den to thelw alliws pernei ta kleidia apo to lexiko lowerScore kai blepei ama to lexiko einai 0 tote epistrefei 0 giati ola ta xrisimopoihthikan.Meta apo mia for gia kathe k antistoixei to fileid me to lexiko readfrom gia kathe kkai ama to ena arxeio einai 0 kanei to allo 1.Telos briskei to upperbound prostithwntas thn timh tou lowerscore gia kathe k kai thn timh tou score gia to allo arxeio gia na kserei pou einai to panw orio kai ama auto einai megalitero apo th top timh tou heap girnaei false giati den to thelw
    global myHeap, scores, lowerScore, readFrom, isHeapReady, T
    
    if T > myHeap[0][0]:
        return False
    
    keys = lowerScore.keys()
    
    if len(lowerScore) == 0:
        return True
    
    for k in keys:
        fileId = readFrom[k]
        if fileId == 0:
            otherFile = 1
        else:
            otherFile = 0
        upperBound = lowerScore[k] + scores[otherFile]
        if upperBound > myHeap[0][0]:
            return False
    
    return True
    
def algorithm():#H shnarthsh diavazei ta arxeia kai mesw enos counter krataw posew fores mpike mesa sthn epanalipsi dhladh poses grammes diavasa opou ton boithaene duo flag finishe kai otan enerhopoithoun ta flag auksanetai gia na termatisei alliws kalei thn procesai me to linei kai to arithmo tou arxeiou gia na kserw poio arxeio thn kalese kai otan energopoithei h shnarthsh checkStop tote stamataei kai typwnei ta apotelesmata
    global myHeap, k, scores, lowerScore, readFrom, isHeapReady, R, T
    
    infile1 = open("seq1.txt")
    infile2 = open("seq2.txt")
    counter = 0
    readR()
    
    finished1 = False
    finished2 = False
    
    while True:
        
        line = infile1.readline()
        if line == '':
            finished1 = True
        else:
            process(line, 0)
        
        counter += 1
        if finished1 == True and finished2 == True:
            break
        if checkStop() == True:
            break
        line = infile2.readline()
        if line == '':
            finished2 = True
        else:
            process(line, 1)
        counter += 1
        if finished1 == True and finished2 == True:
            break
        if checkStop() == True:
            break
        
        
        
    string = ""
    for i in range(k):
        element = heapq.heappop(myHeap)
        string = "%d: %.2f\n"%(element[1], element[0])  + string
    
    string = string.strip()
    
    print("\nNumber of sequential accesses= "  + str(counter))
    print("Top k objects:")
    print(string)
    
def readB(filename):#anoigei to arxeiο pou tou dinw (filename) kai epeita mesw ths readline to diavazei opou to splitarei se tokens mesw tou kenou kai kratei to obgectid kai to objectscore.Akomi sthn lista R enimeronei to anistoixo score sto antisotixo id kai otan einai keno to line termatizei
    global R
    infile = open(filename)
    
    line = infile.readline()
    while line != '':
        tokens = line.split(' ')
        objectId = int(tokens[0])
        objectScore = float(tokens[1])
        
        R[objectId] += objectScore
        line = infile.readline()
    return R

def bruteforce():#h shnarthsh kalei thn readR gia na diavasei opw proanefera to rnd.txt kai kai thn readB 2 fores mai gia to seq1 kai mia gia to seq2.Oso einai to plithos twn k krataei to object id kai objectscore opou ta prosthetei sthn arxika kenh lista swrou myHeap.Epeita kalietai h heapq.heapify(myHeap) gia na kanei thn lista swro kai meta sygkrinei to top stoixeio tou swrou me to objectscore kai ama einai megalitero to objectscore tote gia na to sumberilabw sta top k stoxeia petaw eksw to mikro stoixeio apo to myheap me thn heapq.heappop kai vazw to kainourgio stoixeio apo to elenxo me tin heapq.heappush kai typwnw ta apotelesmata
    global myHeap, k, scores, lowerScore, readFrom, isHeapReady, R, T
    
    readR()
    readB("seq1.txt")
    readB("seq2.txt")
    myHeap = []
    
    for i in range(k):
        objectId = i
        objectScore = R[i]
        myHeap.append([objectScore, objectId])

    heapq.heapify(myHeap)
    
    for i in range(k, len(R)):
        objectId = i
        objectScore = R[i]
        if myHeap[0][0] < objectScore:
            heapq.heappop(myHeap)
            heapq.heappush(myHeap, [objectScore, objectId])
    string = ""
    for i in range(k):
        element = heapq.heappop(myHeap)
        string = "%d: %.2f\n"%(element[1], element[0]) + string
    
    string = string.strip()
    
    print("\nBrute - Force")
    print("Number of sequential accesses= "  + str(3*len(R)))
    print("Top k objects:")
    print(string)
    
algorithm()
bruteforce()
