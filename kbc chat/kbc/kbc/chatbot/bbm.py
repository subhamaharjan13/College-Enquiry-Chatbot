import json
import os
module_dir = os.path.dirname(__file__)  # get current directory
#importing bernhardt.json file
bn = os.path.join(module_dir,'bbm.json')
op = os.path.join(module_dir, 'op.txt')
with open(bn, "r") as read_file:
    data5 = json.load(read_file)
#print(data5[0])

def bbm_data():
    bbm_model = []
    faculty_model = []
    for i in range(8):
        faculty_model.append(data5[i]['Semester'])
    #list of available faculties
    print(bbm_model)


#for full info
def bbm_info(usermodel):
    usermodel = usermodel.upper()
    bbm_model = []
    for i in range(8):
        bbm_model.append(data5[i]['Semester'])
    #print(bbm_model)
                
    if usermodel in bbm_model:
        #index of usermodel
        x = bbm_model.index(usermodel)
        extract_model = data5[x]['Semester']
        if extract_model == usermodel:
            fp = open(op, 'w')
            fp.write("KBC Bot: BBM "+ data5[x]['Semester']+" semester details:\n"+"Shift: "+data5[x]['Shift']+"\t\tSemester Fee: "+data5[x]['Semester_fee']+"\n"+"Course list:\n")
            fp.close()
            fp = open(op, 'a')
            for i in range(len(data5[x]['Subjects'])):
                fp.write("*  "+data5[x]['Subjects'][i])
            if len(data5[x]['Electives'])>0:
                fp.write("\nElective Subjects: (Choose at least one from below):\n")
                for i in range(len(data5[x]['Electives'])):
                    fp.write("*  "+data5[x]['Electives'][i])
            fp.close()

#for fee only
def semester_fee(usermodel):
    usermodel = usermodel.upper()
    bbm_model = []
    for i in range(8):
        bbm_model.append(data5[i]['Semester'])
    if usermodel in bbm_model:
        #index of usermodel
        x = bbm_model.index(usermodel)
        extract_model = data5[x]['Semester']
        if extract_model == usermodel:
            fp = open(op, 'w')
            fp.write("KBC Bot: The fee for "+ data5[x]['Semester'] +" semester is "+ data5[x]['Semester_fee'])
            fp.close()


#z=input()
#bbm_info(z)
#semester_fee(z)
