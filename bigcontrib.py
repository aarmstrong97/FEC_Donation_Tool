###
#FEC election donation tool
#Calculates the contribution of employees that donated in a election cycle
#Sums Democratic donations, Republican donations,
#and Other donations and maps donations from employees to their employer
#
#Austin Armstrong, January 2018
###

fileName = input("Type the name of the individual input file,\n"\
                 "assuming format follows FEC standard as of 2016...\n"\
                 "and file is in local directory...\n")


cont = open(fileName, 'r')
sortedDonors=[]

sum=0
index=0

def getKey(item):
    return item[1]

#Returns a record in a line according to | delimiter index
def rec(line, index):
    return line.split('|')[index]

def getDonors(cont):
    donors={}
    bigDonors=[]
    for line in cont:
        name = rec(line,7)

        if name in donors:
            donors[name]+= int(rec(line, 14))
        else:
            donors[name]= int(rec(line, 14))

        if donors[name]>150000 and name not in bigDonors:
            bigDonors.append(name)
    return bigDonors,donors

bigDonors,donors = getDonors(cont)

#Sort big donors in descending order, >$150,000
sortedDonors = [(i, donors[i]) for i in bigDonors]
sortedDonors = sorted(sortedDonors, key=getKey, reverse=True)

#print big donors
prompt = input("Print donors over $150k? (y/n)")
if prompt == "y":
    for index in range(len(sortedDonors)):
        print(sortedDonors[index])

#Now time to map the fund ID codes from individual donations to respective
#committees and candidates.

candidateDict={}
committeeDict={}
cninput = input("type directory of candidate file..\n")
cminput = input("type directory of committee file..\n")
cn = open(cninput,'r')
cm = open(cminput,'r')

#map codes to party affilitaions
for line in cn:
    candidateDict[rec(line,9)]= rec(line, 2)

for line in cm:
    committeeDict[rec(line,0)]=rec(line,10)

#now time to map employers to contributions of their employes
employerDict = {}

cont = open(fileName,'r')

#Some 'employers' are filtered out in order for the result to best
#reflect 'true' employers. Filter can be modified directly from its file
filterFile=open('filter.txt','r')
filter = [i.rstrip() for i in (filterFile)]
filter.append('')
for line in cont:

    #if employer is in the employer dict
    if employerDict.get(rec(line, 11), False):

        #if the identification # is in the candidate dict
        if candidateDict.get(rec(line, 0), False):

            #add the tuple of party and amount onder the employer dict
            employerDict[rec(line, 11)].append((candidateDict[rec(line, 0)], rec(line, 14)))

        #if the # is in the committee dict
        if committeeDict.get(rec(line, 0), False):
            employerDict[rec(line, 11)].append((committeeDict[rec(line, 0)], rec(line, 14)))

    #employer is not in the employerdict
    #make sure person is working in a "true" company, see filter above.
    elif rec(line, 11).upper() not in filter:

        #instantiate the empty list
        employerDict[rec(line, 11)] = []
        if candidateDict.get(rec(line, 0), False):
            #add the tuple of party and amount to the employer dict
            employerDict[rec(line, 11)].append((candidateDict[rec(line, 0)], rec(line, 14)))
        #if the # is in the committee dict
        if committeeDict.get(rec(line, 0), False):
            employerDict[rec(line, 11)].append((committeeDict[rec(line, 0)], rec(line, 14)))

#condense all donations into DEM, REP, or other for each employer key
for key in employerDict.keys():
    demDonation = 0
    repDonation = 0
    otherDonation = 0
    for employer in employerDict[key]:
        if employer[0]=="DEM":
            demDonation += int(employer[1])
        elif employer[0]=="REP":
            repDonation += int(employer[1])
        else:
            otherDonation += int(employer[1])

    employerDict[key] = [("DEM", demDonation), ("REP", repDonation), ("OTHER", otherDonation)]

#Special case, 'blackstone' and 'the blackstone group' are both in the top 30 list in 2014.
#Merge the two together.
employerDict['THE BLACKSTONE GROUP'] = \
                                        [("DEM", employerDict['BLACKSTONE'][0][1]+ \
                                            employerDict['THE BLACKSTONE GROUP'][0][1]),
                                        ("REP", employerDict['BLACKSTONE'][1][1]+ \
                                            employerDict['THE BLACKSTONE GROUP'][1][1]),
                                        ("OTHER", employerDict['BLACKSTONE'][2][1]+ \
                                            employerDict['THE BLACKSTONE GROUP'][2][1])\
                                        ]

employerDict.pop('BLACKSTONE')

#sort the companies by total sum of donations
sortedDonors = sorted(employerDict.items(), key=lambda x: x[1][0][1]+x[1][1][1]+x[1][2][1], reverse=True)

#make a list with the 30 largest donors of the election cycle
topDonors = []
for z,key in enumerate(sortedDonors):
    topDonors.append(key)
    if z==30:
        break


outputName = input("Type the name for the output data file (30 largest donating employers)\n")
donorFile = open(outputName, "w+")

#output data in | delimiter format,
#0:employer, 1: DEM donation sum, 2: REP donation sum, 3: OTHER donation sum
for i in topDonors:
    donorFile.write(i[0]+"|"+str(i[1][0][1])+"|"+str(i[1][1][1])+"|"+str(i[1][2][1])+"|"+"\n")

print("~~~~")

prompt = input("Compare values from another year? (y/n)\n" \
           "(values from another 30 top companies compared to current employer dict)\n")

if prompt == 'y':
    findfile = input("type the name of file to check\n")
    inputFile = open(findfile, 'r')
    outputFile = open(findfile+"_out", 'w+')
    temp =''

    inputNames =[]

    for read in inputFile.readlines():
        print(read)
        temp = rec(read,0)
        if employerDict.get(temp,False):
            print(employerDict[temp])

            outputFile.write(read.rstrip()+'|'+str(employerDict[temp][0][1])+\
                            '|'+str(employerDict[temp][1][1])+\
                            '|'+str(employerDict[temp][2][1])+'\n')
        else:
            print(temp, "not a donor in this year")
            outputFile.write(read.rstrip()+'|'+str(0)+'|'+str(0)+'|'+str(0)+'\n')
 



