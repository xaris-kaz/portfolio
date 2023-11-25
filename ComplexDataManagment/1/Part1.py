##############################
##### Theocharis Kazakidis ###
#####        4679          ###
##############################
import sys

def readFile(input_file):#sinartisi pou diavazei to arxeio kai krataei tin stili income pou xreiazomaste
    
    values = []#lista pou kratai to plithos twn  timwn pou diavazei apo to input
    input_file.readline()#kalei tin sinartisi kai readline h opoia diavazei kathe fora mia grammi kai epanaliptika(while true) oso tha altheyei tote na elexei gia tis kenes grammes kai na tis prospernaei alliws ama uparxei timh na to kanei slpit (stin stili 13 pou einai to income) wste na to diaxwrizei  tin kathe timi apo tis alles kai na tis prosthetei stin lista values
    while True:
        line = input_file.readline()
        if line == '':
            break
        line = line.split(',')
        if line[13] != '':
            values.append(float(line[13]))
    
    return values
   
    
def MakeHistograms(values, histType):
    if histType == "W":#dhmiourghsa mia synarhsh makehistogram pou exeis ws orismata thn lista values kai to tupo tou histogram .Edw exoume histType=W giati anaferomai se equi-Width histogram
        length = (max(values) - min(values))/100#mia metavliti lenght pou mas dinei to plithos twn values pou exoume se kathe bin
        
        bin = [min(values), min(values) + length, 0]#dhmioygw mia lista bin h opoia exei tin katw timh, thn panw timh kai to numtable
        
        histogram = [bin]
        for i in  range(1, 100):#100 bins ara gia 100 fores epanaliptika ananewnaetai o i me tis nees times
            bin_i = [bin[0] + length, bin[1] + length, 0]#auksanw kathe fore oso htan h proigoumi katw kai panw timi sin to lenht kathe bin
            histogram.append(bin_i)#vazw stin lista tin nees times twn bins
            bin = bin_i
            
        for i in range(len(values)):
            for j in range(100):
                if values[i] >= histogram[j][0] and values[i] < histogram[j][1]:#gia oses fores kanei thn epanalipsi kai gia oso eimai mesa se kapoio bin apo ayta tote oses times values mpoun mesa se auto to bin auksise to counter kai dwse to numtuples
                    histogram[j][2] = histogram[j][2] + 1
                    break
                    
        return histogram
        
    elif histType == "D":
        values.sort()#gia to equi-depth xreiazomaste prwta n taksinomizoume tis times
        count = int(len(values)/100)#to pose times tha exoume se kathe bin
        
        first = 0
        last = count
        bin = [values[first], values[last], count]#idia ulopoihsh me panw mesw mias lista bin sthn arxh exoyme tin katw timh sthn mesi thn panw timi kai to count pou enai ousiastika to numtuple apla edw exoume stathero artithmo timwn pou mapiounon se kthe bin
        
        histogram = [bin]
        for i in  range(1, 100):
            first = first + count
            last = last + count
            bin = [values[first], values[last], count]#auksanw epanaliptika mecri na ftasw ta 100 bin to first kai to last me to stahero count ananewnntas oso auksanetai to i tis times tous kai epeita ta vazw sthn lista histgram
            histogram.append(bin)
        
        histogram[99][2] = histogram[99][2] + len(values) - 100*count;#porsthetoume sto teyetaio numtple thn mia kai monadiki timh pou menei .To len(values) epistreei oles tis times ths stilis kai to 100*count epistrefeo to megethos kathe bin epi ta posa bin mas zitaei h askisi.Oti menei prostithtetai sto histogram[99][2] opou krataei ta hdh posa numtuples exou ta bins kai to teleytaio stoixeio poi menei mpainei sto teleytaio kado
        return histogram
    

if len(sys.argv) < 2:
    print("Error")#tupikos elexos ama dwsei den eparkoun tastoixea sto command line
    exit(0)

input_file = open(sys.argv[1])#to arxeio to dinoume san deutero osima apo sto command line afou theloume na douleyoume anaksartita to arxeio dhladh oxi me ena mono sugkekrimeno arxeio

values = readFile(input_file)#pou tha kratiountai oi times pou diavazei
histogramW = MakeHistograms(values, "W")#mia metavliti pou dieykolynei tin ektypwsi kai exei oti epistrefoun ta histogramata
histogramD = MakeHistograms(values, "D")

print(str(len(values)) + " valid income values")#print gai na ektpwnei opws to format print pou zitisate sthn ekfwnisi
print("minimum income: " + str(min(values)) + " maximum income: " + str(max(values)))
print("equiwidth:")
for i in range(100):
    print("range: [%.2f, %.2f) numtuples: %d"%(histogramW[i][0], histogramW[i][1], histogramW[i][2]))
    
print("equidepth:")
for i in range(100):
    print("range: [%.2f, %.2f) numtuples: %d"%(histogramD[i][0], histogramD[i][1], histogramD[i][2]))

