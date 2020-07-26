import json
import os
module_dir = os.path.dirname(__file__)  # get current directory
#importing bernhardt.json file
bn = os.path.join(module_dir,'mbs.json')
op = os.path.join(module_dir, 'op.txt')
#importing mbs.json file
with open(bn,"r") as read_files:
    data7=json.load(read_files)
#print(data7[0])
def mbs_data():
    mbs_model=[]
    for i in range(2):
        mbs_model.append(data7[i]['Year'])
    #list of availabl faculties
    print(mbs_model)

    
#for full info
def mbs_info(usermodel):
    usermodel = usermodel.upper()
    mbs_model = []
    for i in range(2):
        mbs_model.append(data7[i]['Year'])
    print(mbs_model)

    if usermodel in mbs_model:
        #index of usermodel
        x=mbs_model.index(usermodel)
        extract_model=data7[x]['Year']
        if extract_model==usermodel:
            fp = open(op, 'w')
            fp.write("KBC Bot: BBS "+ data7[x]['Year']+" year details:\n"+"Shift: "+data7[x]['Shift']+"\t\tYear Fee: "+data7[x]['Year_fee']+"\n")
            fp.close()
            fp = open(op, 'a')
            fp.write("Course list:\n")
            for i in range(len(data7[x]['Subjects'])):
                fp.write("*  "+data7[x]['Subjects'][i])
            if len(data7[x]['Electives'])>0:
                fp.write("\nElective Subjects: (Choose at least one from below):\n")
                for i in range(len(data7[x]['Electives'])):
                    fp.write("*  "+data7[x]['Electives'][i])
            fp.close()

#for fee only
def year_fee(usermodel):
    usermodel = usermodel.upper()
    mbs_model = []
    for i in range(2):
        mbs_model.append(data7[i]['Year'])
    if usermodel in mbs_model:
        #index of usermodel
        x = mbs_model.index(usermodel)
        extract_model = data7[x]['Year']
        if extract_model == usermodel:
            fp = open(op, 'w')
            fp.write("\nKBC Bot: The fee for "+ data7[x]['Year'] +" year is "+ data7[x]['Year_fee'])
            fp.close()


#z=input()
#mbs_info(z)
#year_fee(z)


