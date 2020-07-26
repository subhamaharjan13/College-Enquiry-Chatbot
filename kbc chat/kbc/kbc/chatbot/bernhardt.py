import json
import os
module_dir = os.path.dirname(__file__)  # get current directory
#importing bernhardt.json file
bn = os.path.join(module_dir,'bernhardt.json')
op = os.path.join(module_dir, 'op.txt')
with open(bn, "r") as read_file:
    data1 = json.load(read_file)
#print(data1[0]['Name'])

def bernhardt_data():
    fp = open(op, 'w')
    fp.write("KBC Bot: "+data1[0]['Name']+"\n"+data1[0]['Address']+"\tPhone: "+data1[0]['Contact']+"Website: "+data1[0]['Website']+"\tEmail: "+data1[0]['Email']+"\n\n"+data1[0]['Intro']+"\n--------------------------------------------------- Vision ----------------------------------------------------\n"+data1[0]['Vision']+"\n--------------------------------------------------- Mission ---------------------------------------\n"+data1[0]['Mission'])
    fp.close()



   



    
#bernhardt_data()
