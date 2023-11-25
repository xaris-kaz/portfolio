##############################
##### Theocharis Kazakidis ###
#####        4679          ###
##############################
import sys



def gridCells():###Diavazei ta arxeia pou dhmiourgountai apo peros 1 .Me to leksiko apothikeuei dedomena apo kathe keli tou grid kai diavazei tis ypoloipes grammes sto "grid.dir"  Kathe grammi antistoixei se ena cell tou grid kai periexei ena key kai ta mbr.Ean o N !=0, diavazei ton antistoixo arithmo grammwn apo to "grid.grd", kathemia apo tis opoies perigrafei ena mono mbr. Aftes oi grammes periexoun ena id, ena mbr kai mia lista simeiwn .Kataskevazei mia lista mbr gia to trexon cell kai tin apothikeyei sto leksiko me kleidi tis syntetagmenes tou keliou
    
    infileDir = open("grid.dir", "r")
    infileGrd = open("grid.grd", "r")
    
    lineDir = infileDir.readline()
    tokens = lineDir.split(" ")
    minX = float(tokens[0])
    maxX = float(tokens[1])
    minY = float(tokens[2])
    maxY = float(tokens[3])
    
    
    gridX = [[[0,0] for j in range(10)] for i in range(10)]
    gridY = [[[0,0] for j in range(10)] for i in range(10)]
    
    grid = {}
    
    for i in range(0, 10):
        for j in range(0, 10):
            gridX[i][j][0] = minX + i*(maxX - minX)/10
            gridX[i][j][1] = minX + (i+1)*(maxX - minX)/10
            
            gridY[i][j][0] = minY + j*(maxY - minY)/10
            gridY[i][j][1] = minY + (j+1)*(maxY - minY)/10
                        
    
    lineDir = infileDir.readline()
    while lineDir != '':#
        tokens = lineDir.split(" ")
        N = int(tokens[2])
        key = "(" + tokens[0] + "," + tokens[1] + ")"
        if N != 0:
            cellMbrs = []
            
            for i in range(N):
                lineGrd = infileGrd.readline()
                tokens = lineGrd.split(",")
                mbrId = int(tokens[0])
                
                xyMin = tokens[1].split(" ")
                xyMax = tokens[2].split(" ")
                
                minX = float(xyMin[0])
                minY = float(xyMin[1])
                maxX = float(xyMax[0])
                maxY = float(xyMax[1])
                
                points = []
                for j in range(3, len(tokens)):
                    p = tokens[j].split(" ")
                    x = float(p[0])
                    y = float(p[1])
                    
                    points.append([x, y])
                
                mbr = [mbrId, [[minX, minY], [maxX, maxY]], points]
                cellMbrs.append(mbr)
            
            grid[key] = cellMbrs
                
        lineDir = infileDir.readline()
        
    
                
    return gridX, gridY, grid

    

def readQueries():
    infile = open(sys.argv[1], "r")
    
    queries = []###Diavazei mesw orismatos to arxeio query.txt tis ekfwnisis ,splitarei ta dedomena kathe grammis prwta sto komma gia na diaxwrisei to id me ta upoloipa kai meta sto keno kai pairnei to minX...maxY kai ta prosthetei me sygkekrimeni morfi stin lista queries
    allLines = infile.readlines()
    
    for i in range(len(allLines)):
        line = allLines[i]
        tokens = line.split(",")
        id = int(tokens[0])
        tokens1 = tokens[1].split(" ")
        minX = float(tokens1[0])
        maxX = float(tokens1[1])
        minY = float(tokens1[2])
        maxY = float(tokens1[3])
        queries.append([id, [[minX, minY], [maxX, maxY]]])
    return queries

def findResults(query, gridX, gridY, grid):
    minX = query[1][0][0]
    minY = query[1][0][1]###Ksexwrizei ta min,max twn query gia na mporei na eleksei epita an uparxei tomi me ta cells kai auksanei to counter cells kai mpainei sto leksiko.An isxyei tsekarei an uparxei tomi kai me ta mbr kai na isxyei tote kratame to id tou se mia lista. Gia na mhn exoume dyo fores to idio id, elgxoume me to reference point opws leei sthn ekfwnisi
    maxX = query[1][1][0]
    maxY = query[1][1][1]
    cells = 0
    mbrs = []
    
    for i in  range(10):
        for j in range(10):
            
            if minX > gridX[i][j][1]:
                continue
            if maxX < gridX[i][j][0]:
                continue
            
            if minY > gridY[i][j][1]:
                continue
            if maxY < gridY[i][j][0]:
                continue
            key = "(" + str(i) + "," + str(j) + ")"
            
            if key not in grid.keys():
                continue
            
            cells += 1
            cellMbrs = grid[key]
            
            for k in range(len(cellMbrs)):
                mbrMinX = cellMbrs[k][1][0][0]
                mbrMinY = cellMbrs[k][1][0][1]
                mbrMaxX = cellMbrs[k][1][1][0]
                mbrMaxY = cellMbrs[k][1][1][1]
                
                if minX > mbrMaxX:
                    continue
                if maxX < mbrMinX:
                    continue
                
                if minY > mbrMaxY:
                    continue
                if maxY < mbrMinY:
                    continue
                
                refPx = max(minX, mbrMinX)
                refPy = max(minY, mbrMinY)
                
                if gridX[i][j][0] <= refPx and refPx <= gridX[i][j][1] and gridY[i][j][0] <= refPy and refPy <= gridY[i][j][1]:
                    if check(minX, minY, maxX, maxY, mbrMinX, mbrMinY, mbrMaxX, mbrMaxY, cellMbrs[k][2]) == True:
                        mbrs.append(cellMbrs[k][0])
    return cells, mbrs
    
def check(minX, minY, maxX, maxY, mbrMinX, mbrMinY, mbrMaxX, mbrMaxY, points):
    if minX <= mbrMinX and mbrMaxX <= maxX:###Elegxei prwta ama h pleyra X tou mbr periexetai sto parathiro tote uparxei tomh tou parathirou me to linestring(sxima A tou 3.1),antoistixa kai oli h pleyra y(sxima B tou 3.1) enw se opiadipote alli periptwsi prepei na upologisti apo ton tupo tou arthtou to an uparxei tomh i oxi epomenws pernoume ta euthigramma tmimata pou sximatizontai apo ta simeia kai efarmozoume to tipo kai elegxoume ean yparxei tomh me kapoia akmh tou parathirou kai an 0<=t<=1 and 0<=u<=1 tote exoume tomh
        return True
    elif minY <= mbrMinY and mbrMaxY <= maxY:
        return True
    else:
        for i in range(len(points) - 1):
            x1 = points[i][0]
            y1 = points[i][1]
            x2 = points[i+1][0]
            y2 = points[i+1][1]
            
            X = [minX, minX, maxX, maxX]
            Y = [minY, maxY, maxY, minY]
            
           
            for j in range(len(X)):
                x3 = X[j]
                y3 = Y[j]
                x4 = X[(j+1)%4]
                y4 = Y[(j+1)%4]
                
                    
                w = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
                if w == 0:
                    continue
                
                t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4))/((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
                u = ((x1-x3)*(y1-y2) - (y1-y3)*(x1-x2))/((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
                
                if 0 <= t and t <= 1 and 0 <= u and u <= 1:
                    return True

    return False


gridX, gridY, grid = gridCells()
queries = readQueries()
for i in range(len(queries)):
    cells, mbrs = findResults(queries[i], gridX, gridY, grid)
    ####Tupwnei me tin morfi opws eida sthn ekfwnisi
    print("Query " + str(queries[i][0]) +" results")
    strMbr = ""
    for i in range(len(mbrs)):
        strMbr = strMbr + str(mbrs[i]) + " "
    print(strMbr)
    print("Cells: " + str(cells))
    print("Results: " + str(len(mbrs)))
    
    print("----------")
