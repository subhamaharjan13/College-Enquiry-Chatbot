import json
import os
module_dir = os.path.dirname(__file__)  # get current directory
#importing bernhardt.json file
bn = os.path.join(module_dir,'bbs.json')
op = os.path.join(module_dir, 'op.txt')
with open(bn,"r") as read_files:
    data6=json.load(read_files)
#print(data6[0])
def bbs_data():
    bbs_model=[]
    faculty_model =[]
    for i in range(4):
         faculty_model.append(data6[i]['Year'])
    #list of availabl faculties
    print(bbs_model)

    
#for full info
def bbs_info(usermodel):
    usermodel = usermodel.upper()
    bbs_model = []
    for i in range(4):
        bbs_model.append(data6[i]['Year'])
    print(bbs_model)

    if usermodel in bbs_model:
        #index of usermodel
        x=bbs_model.index(usermodel)
        extract_model=data6[x]['Year']
        if extract_model==usermodel:
            fp = open(op, 'w')
            fp.write("KBC Bot: BBS "+ data6[x]['Year']+" year details:\n"+"Shift: "+data6[x]['Shift']+"\t\tYear Fee: "+data6[x]['Year_fee']+"\n"+"Course list:\n")
            fp.close()
            fp = open(op, 'a')
            for i in range(len(data6[x]['Subjects'])):
                fp.write("*  "+data6[x]['Subjects'][i])
            if len(data6[x]['Electives'])>0:
                fp.write("\nElective Subjects: (Choose at least one from below):\n")
                for i in range(len(data6[x]['Electives'])):
                    fp.write("*  "+data6[x]['Electives'][i])
            fp.close()
#for fee only
def year_fee(usermodel):
    usermodel = usermodel.upper()
    bbs_model = []
    for i in range(4):
        bbs_model.append(data6[i]['Year'])
    if usermodel in bbs_model:
        #index of usermodel
        x = bbs_model.index(usermodel)
        extract_model = data6[x]['Year']
        if extract_model == usermodel:
            fp = open(op, 'w')
            fp.write("\nKBC Bot: The fee for "+ data6[x]['Year'] +" year is "+ data6[x]['Year_fee'])
            fp.close()


#z=input()
#bbs_info(z)
#year_fee(z)


