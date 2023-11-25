##############################
##### Theocharis Kazakidis ###
#####        4679          ###
##############################
import sys

def readFile(input_file):#xrisimopoiw thn synartisi readFile pou ulopoihsa sto part1
    
    values = []
    input_file.readline()
    while True:
        line = input_file.readline()
        if line == '':
            break
        line = line.split(',')
        if line[13] != '':
            values.append(float(line[13]))
    
    return values
   
    
def MakeHistograms(values, histType):#xrisimopoiw thn synartisi MakeHistograms pou ulopoihsa sto part1
    if histType == "W":#opou W to equi-width hist
        length = (max(values) - min(values))/100
        
        bin = [min(values), min(values) + length, 0]
        
        histogram = [bin]
        for i in  range(1, 100):
            bin_i = [bin[0] + length, bin[1] + length, 0]
            histogram.append(bin_i)
            bin = bin_i
            
        for i in range(len(values)):
            for j in range(100):
                if values[i] >= histogram[j][0] and values[i] < histogram[j][1]:
                    histogram[j][2] = histogram[j][2] + 1
                    break
                    
        return histogram
    elif histType == "D":#opou D to equi-depth hist
        values.sort()
        count = int(len(values)/100)
        
        first = 0
        last = count
        bin = [values[first], values[last], count]
        
        histogram = [bin]
        for i in  range(1, 100):
            first = first + count
            last = last + count
            bin = [values[first], values[last], count]
            histogram.append(bin)
        
        histogram[99][2] = histogram[99][2] + len(values) - 100*count;
        return histogram

def condition(values, a, b):#sinartisi pou pernei san orisamta tis times values to a pou einai h katw timh kai b pou einai h panw timmh wste na epistrepsei mesw ths sinthikhs tis ekfwnisis twn arithmo
    
    count = 0
    
    for i in range(len(values)):#gia olo to euros twn timwn metaksi a kai b na ektelei thn sinthiki kai na leei poses timies to ikanopoioun mesw enos counter poy aksanetai
        if a <= values[i] and values[i] < b:
            count = count + 1
    return count


def methods_estimation(histogram, a, b):#pernw tis periptwsis pou mporei na isxuoun metaksi twn timwn pou mporei na parei analoga kaia ta apothikeyw se ena counter pou krataei to poses times tha exoume sto diastima
    counter = 0
    ###sxediasa sto xarti ta diastimata kai prosathisa na katalabw to ti periptwseis prokipton meta apo dokimes kateliksa stin parakatw ulopoihsh kai otan etreksa to programma emeina ikanopoihmenos apo to apotelesmata
    for i in range(100):
        if a <= histogram[i][0] and b >= histogram[i][1]:#ama h prwti timh (a) einai mikroteri/isi kai h deyteri thmi (b) einai megaliter/isi tote:
            counter = counter + histogram[i][2]#prosthetw oles tis times
        elif a > histogram[i][0] and b < histogram[i][1]:#ama h prwti timh (a) einai megaliter kai h deyteri thmi (b) einai mikroteri tote:
            counter = counter + (b - a)/(histogram[i][1] - histogram[i][0])*histogram[i][2]#prosthetw mono thn ektimhsh gia to meros tou kadou pou einai mesa sto diasthma
        elif a >= histogram[i][0] and a <= histogram[i][1] and b >= histogram[i][1]:#ama h prwti timh (a) einai megaliter/isi tou katw oriou  alla tautoxrona mikroteri/isi tou panw oriou  kai h deyteri thmi (b) einai megaliter/isi tote:
            counter = counter + (histogram[i][1] - a)/(histogram[i][1] - histogram[i][0])*histogram[i][2]
        elif a <= histogram[i][0] and b >= histogram[i][0] and  b < histogram[i][1]:#ama h prwti timh (a) einai mikroteri/isi tou katw oriou kai h deyteri thmi (b) einai megaliter/isi tou katw oriou kai tautoxrona mikroteri tou panw oriou tote:
            counter = counter + (b - histogram[i][0])/(histogram[i][1] - histogram[i][0])*histogram[i][2]
        elif b < histogram[i][0]:#am einai mikroteri ths katw oriou tote:
            return counter#epistrefw tis times pou ypologisa
    return counter



if len(sys.argv) < 4:#ama sto command line exei ligotero apo 4 orismata kathws tera theloume kai ta arguments tou a kai b gia to upologimo
    print("Error")
    exit(0)

input_file = open(sys.argv[1])#2o arg to file
a = float(sys.argv[2])#3o arg to a
b = float(sys.argv[3])#4o arg to a

values = readFile(input_file)
#print se format opws sthn ekfwnisi
print(str(len(values)) + " valid income values")
print("minimum income: " + str(min(values)) + " maximum income: " + str(max(values)))

histogramW = MakeHistograms(values, "W")
print("equiwidth:")
for i in range(100):
    print("range: [%.2f, %.2f) numtuples: %d"%(histogramW[i][0], histogramW[i][1], histogramW[i][2]))

histogramD = MakeHistograms(values, "D")
    
print("equidepth:")
for i in range(100):
    print("range: [%.2f, %.2f) numtuples: %d"%(histogramD[i][0], histogramD[i][1], histogramD[i][2]))

method_W = methods_estimation(histogramW, a, b)
print("equiwidth estimated results: %.12f "%method_W)

method_E = methods_estimation(histogramD, a, b)
print("equidepth estimated results: %.12f"%method_E)

accurate = condition(values, a, b)
print("actual results: " + str(accurate))
