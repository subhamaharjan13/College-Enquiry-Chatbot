import json
import os
module_dir = os.path.dirname(__file__)  # get current directory
#importing bernhardt.json file
bn = os.path.join(module_dir,'bsw.json')
op = os.path.join(module_dir, 'op.txt')
#importing bsw.json file
with open(bn,"r") as read_files:
    data8=json.load(read_files)
#print(data8[0])
def bsw_data():
    bsw_model=[]
    for i in range(3):
        bsw_model.append(data8[i]['Year'])
    #list of availabl faculties
    print(bsw_model)

    
#for full info
def bsw_info(usermodel):
    usermodel = usermodel.upper()
    bsw_model = []
    for i in range(3):
        bsw_model.append(data8[i]['Year'])
    #print(bsw_model)

    if usermodel in bsw_model:
        #index of usermodel
        x=bsw_model.index(usermodel)
        extract_model=data8[x]['Year']
        if extract_model==usermodel:
            fp = open(op, 'w')
            fp.write("KBC Bot: BSW "+ data8[x]['Year']+" year details:\n"+"Shift: "+data8[x]['Shift']+"\t\tYear Fee: "+data8[x]['Year_fee']+"\n")
            fp.close()
            fp = open(op, 'a')
            print("Course list:\n")
            for i in range(len(data8[x]['Subjects'])):
                fp.write("*  "+data8[x]['Subjects'][i])
            if len(data8[x]['Electives'])>0:
                fp.write("\nElective Subjects: (Choose at least one from below):\n")
                for i in range(len(data8[x]['Electives'])):
                    fp.write("*  "+data8[x]['Electives'][i])
            fp.close()

#for fee only
def year_fee(usermodel):
    usermodel = usermodel.upper()
    bsw_model = []
    for i in range(3):
        bsw_model.append(data8[i]['Year'])
    if usermodel in bsw_model:
        #index of usermodel
        x = bsw_model.index(usermodel)
        extract_model = data8[x]['Year']
        if extract_model == usermodel:
            fp = open(op, 'w')
            fp.write("\nKBC Bot: The fee for "+ data8[x]['Year'] +" year is "+ data8[x]['Year_fee'])
            fp.close()


#z=input()
#bsw_info(z)
#year_fee(z)


