##############################
##### Theocharis Kazakidis ###
#####        4679          ###
##############################
import sys


def readFile(filename):###Anoigei to arxeio gia diabasma pou to pernei apo orisma sto command line kai epieta dibazei kathe grammi kai gia oso einai to sinolo to grammwn splitarei tis grammes sto komma kai ta apotelesmata autwn ta splitarei sto keno opou ,meta apothikeyei ta dedomena analoga me to einai se metavlites kai ta prosthetoi stis listes,akomi orizei tin tripleta mbr kai telos epistrefei allMbrs, min(allX), min(allY), max(allX), max(allY)
    infile = open(sys.argv[1], "r")
    
    line = infile.readline()
    N = int(line)
    allMbrs = []
    allX = []
    allY = []
    for i in range(N):
        line = infile.readline()
        tokens = line.split(",")
        
        X = []
        Y = []
        points = []
        print(len(tokens))
        for j in range(len(tokens)):
            t = tokens[j].split(" ")
            print(t)
            x = float(t[0])
            y = float(t[1])
            X.append(x)
            Y.append(y)
            points.append([x, y])
        mbr = [i+1, [[min(X), min(Y)], [max(X), max(Y)]], points]
        
        allX.extend(X)
        allY.extend(Y)
        allMbrs.append(mbr)
    return allMbrs, min(allX), min(allY), max(allX), max(allY)

def gridCells(allMbrs, minX, minY, maxX, maxY):###Orizei to grid 10X10 me gridX gia axonaX kai gridY gia axonaY kai thetei ta oria pou pernei to x kai y gia range apo 0 ws 10 me basi tin sel 2 tou pdf.Gia ola ta mbr afou ta anathetei analoga se minX...maxY epeita, elexei poia mbr temnontai me to grid kai ftiaxnei lexiko pou an tementai me mbr tote to prostheti se mia lista kai telos epistrefei ta gridX, gridY, grid
    gridX = [[[0,0] for j in range(10)] for i in range(10)]
    gridY = [[[0,0] for j in range(10)] for i in range(10)]
    
    grid = {}
    for i in range(0, 10):
        for j in range(0, 10):
            gridX[i][j][0] = minX + i*(maxX - minX)/10
            gridX[i][j][1] = minX + (i+1)*(maxX - minX)/10
            
            gridY[i][j][0] = minY + j*(maxY - minY)/10
            gridY[i][j][1] = minY + (j+1)*(maxY - minY)/10
            
            print(i, j, gridX[i][j], gridY[i][j])
            
    
    for mbr in allMbrs:
        minX = mbr[1][0][0]
        minY = mbr[1][0][1]
        
        maxX = mbr[1][1][0]
        maxY = mbr[1][1][1]
       
        for i in range(10):
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
                if key in grid.keys():
                    grid[key].append(mbr)
                else:
                    grid[key] = [mbr]
                
    return gridX, gridY, grid

def gridFiles(grid, minX, minY, maxX, maxY):
    outfile = open("grid.dir", "w")

    outfile.write(str(minX) + " " + str(maxX) + " " + str(minY) + " " + str(maxY) + "\n")
    for i in range(10):
        for j in range(10):
            key = "(" + str(i) + "," + str(j) + ")"
            if key in grid.keys():
                outfile.write(str(i) + " " + str(j) + " " + str(len(grid[key])) + "\n")
            else:
                outfile.write(str(i) + " " + str(j) + " 0\n")
    outfile.close()
    ###Dhmioyrgei prwta to grid.dir opou sthn prwti grammi exei tis min kai max times kai stis upoloipes xrisimopoiwntas to lexiko apo tin gridCells grafei tis sintentagmenes kai ta mbr.Meta dhmiourgei to grid.grd opou kai pali me basi to lexiko apo gridCells , taksinomoiei ta periexomena twn keliwn kai ta grafei stin morfi pou ztitai apo tin ekfwnisi dhladh prwta id meta min max kai telos ta simeia twn x,y
    outfile = open("grid.grd", "w")
   
    for i in range(10):
        for j in range(10):
            
            key = "(" + str(i) + "," + str(j) + ")"
            if key in grid.keys():
                cellMbrs = grid[key]
                
                for mbr in cellMbrs:
                    minX = mbr[1][0][0]
                    minY = mbr[1][0][1]
                    
                    maxX = mbr[1][1][0]
                    maxY = mbr[1][1][1]
                    
                    outfile.write(str(mbr[0]) +"," + str(minX) + " " + str(minY) + "," + str(maxX) + " " + str(maxY))###grafw sto arxeio ta dedomena opws zitetai na ta grapsoume apo tin ekfwnisi kai katw opou mbr[2] ta simeia x,y ta grafw taksinomimena mesw tou prwta  str[0] kai meta to str[1]
                    
                    points = mbr[2]
                    for p in points:
                        outfile.write("," + str(p[0]) + " " + str(p[1]))
                    outfile.write("\n")
    outfile.close()
    
    

allMbrs, minX, minY, maxX, maxY = readFile(sys.argv[1])
gridX, gridY, grid = gridCells(allMbrs, minX, minY, maxX, maxY)
gridFiles(grid, minX, minY, maxX, maxY)
 
