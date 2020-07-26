import json
import os
module_dir = os.path.dirname(__file__)  # get current directory
#importing bernhardt.json file
bn = os.path.join(module_dir,'csit.json')
op = os.path.join(module_dir, 'op.txt')
with open(bn, "r") as read_file:
    data3 = json.load(read_file)
#print(data3[0])

def csit_data():
    csit_model = []
    for i in range(8):
        csit_model.append(data3[i]['Semester'])
    #list of available faculties
    print(csit_model)


#for full info
def csit_info(usermodel):
    usermodel = usermodel.upper()
    csit_model = []
    for i in range(8):
        csit_model.append(data3[i]['Semester'])
    #print(csit_model)
                
    if usermodel in csit_model:
        #index of usermodel
        x = csit_model.index(usermodel)
        extract_model = data3[x]['Semester']
        if extract_model == usermodel:
            fp = open(op, 'a')
            fp.write("KBC Bot: BSc.CSIT "+ data3[x]['Semester']+" semester details:\n"+"Shift: "+data3[x]['Shift']+"\t\tSemester Fee: "+data3[x]['Semester_fee']+"\n")
            fp.close()
            fp = open(op, 'a')
            fp.write("Course list:\n")
            for i in range(len(data3[x]['Subjects'])):
                fp.write("*  "+data3[x]['Subjects'][i])
            if len(data3[x]['Electives'])>0:
                fp.write("\nElective Subjects: (Choose at least one from below):\n")
                for i in range(len(data3[x]['Electives'])):
                    fp.write("*  "+data3[x]['Electives'][i])
            fp.close()

#for fee only
def semester_fee(usermodel):
    usermodel = usermodel.upper()
    csit_model = []
    for i in range(8):
        csit_model.append(data3[i]['Semester'])
    if usermodel in csit_model:
        #index of usermodel
        x = csit_model.index(usermodel)
        extract_model = data3[x]['Semester']
        if extract_model == usermodel:
            fp = open(op, 'a')
            fp.write("KBC Bot: The fee for "+ data3[x]['Semester'] +" semester is "+ data3[x]['Semester_fee'])
            fp.close()


#z=input()
#csit_info(z)
#semester_fee(z)
