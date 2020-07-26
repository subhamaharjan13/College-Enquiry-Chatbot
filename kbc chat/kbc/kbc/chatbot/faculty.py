import json
import os
module_dir = os.path.dirname(__file__)  # get current directory
#importing bernhardt.json file
bn = os.path.join(module_dir,'faculty.json')
op = os.path.join(module_dir, 'op.txt')

with open(bn , "r") as read_file:
    data2 = json.load(read_file)
#print(data2[0]['Co-ordinator'])

def faculty_data():
    print(data2)
    faculty_model = []
    for i in range(8):
        faculty_model.append("ok")
    #list of available faculties
    print(faculty_model)

#for full info
def faculty_info(usermodel):
    usermodel = usermodel.upper()
    faculty_model = []
    for i in range(8):
        faculty_model.append(data2[i]['Faculty'])
    #print(faculty_model)
                
    if usermodel in faculty_model:
        #index of usermodel
        x = faculty_model.index(usermodel)
        extract_model = data2[x]['Faculty']
        if extract_model == usermodel:
            fp = open(op, 'w')
            fp.write("KBC Bot: "+ data2[x]['Full'] +" (" + data2[x]['Faculty'] +") "+ "\n"+data2[x]['Affiliated']+" Afiliated "+ data2[x]['Years']+"-year "+data2[x]['Type']+" system\n\nFee: "+data2[x]['Fee']+"\nPrerequisites: "+data2[x]['Prerequisite']+"\nCo-ordinator: "+data2[x]['Co-ordinator']+"\nFor more info: "+data2[x]['Website'])
            fp.close()

#for fee only
def faculty_fee(usermodel):
    usermodel = usermodel.upper()
    faculty_model = []
    for i in range(8):
        faculty_model.append(data2[i]['Faculty'])
    if usermodel in faculty_model:
        #index of usermodel
        x = faculty_model.index(usermodel)
        extract_model = data2[x]['Faculty']
        if extract_model == usermodel:
            fp = open(op, 'w')
            fp.write("KBC Bot: The fee for "+ data2[x]['Full'] +"is "+ data2[x]['Fee'] +" for "+ data2[x]['Years'] +" years.")
            fp.close()

#for co-ordinator info only
def faculty_coordinator(usermodel):
    usermodel = usermodel.upper()
    faculty_model = []
    for i in range(7):
        faculty_model.append(data2[i]['Faculty'])
    if usermodel in faculty_model:
        #index of usermodel
        x = faculty_model.index(usermodel)
        extract_model = data2[x]['Faculty']
        if extract_model == usermodel:
            fp = open(op, 'w')
            fp.write("KBC Bot: "+ data2[x]['Co-ordinator'] +"is the co-ordinator for"+ data2[i]['Full'])
            fp.close()

#x=""
#while(x!="exit"):
#    x=input()
#    faculty_fee(x)
