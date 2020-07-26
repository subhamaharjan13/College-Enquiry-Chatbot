# use natural language toolkit
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
import os
import sys
import random
import json
import numpy as np
import time
import datetime
from . import trainingset as t
#importing methods for json
from .bernhardt import bernhardt_data
from .faculty import faculty_data, faculty_info, faculty_fee, faculty_coordinator
from .csit import csit_data, csit_info, semester_fee
from .bca import bca_data, bca_info, semester_fee
from .bbm import bbm_data, bbm_info, semester_fee
from .bbs import bbs_data, bbs_info, year_fee
from .mbs import mbs_data, mbs_info, year_fee
from .bsw import bsw_data, bsw_info, year_fee
from .writelogs import writeToJSONFile
stemmer = LancasterStemmer()
import os
module_dir = os.path.dirname(__file__)  # get current directory
bn = os.path.join(module_dir, 'bernhardt.json')
op = os.path.join(module_dir, 'op.txt')

#reading json files
with open(bn, "r") as read_file:
    data1 = json.load(read_file)
fc = os.path.join(module_dir, 'faculty.json')
with open(fc, "r") as read_file:
    data2 = json.load(read_file)
cs = os.path.join(module_dir, 'csit.json')
with open(cs, "r") as read_file:
    data3 = json.load(read_file)
bca = os.path.join(module_dir, 'bca.json')
with open(bca, "r") as read_file:
    data4 = json.load(read_file)
bbm = os.path.join(module_dir, 'bca.json')
with open(bbm, "r") as read_file:
    data5 = json.load(read_file)
bbs = os.path.join(module_dir, 'bbs.json')
with open(bbs, "r") as read_file:
    data6 = json.load(read_file)
mbs = os.path.join(module_dir, 'mbs.json')
with open(mbs, "r") as read_file:
    data7 = json.load(read_file)
bsw = os.path.join(module_dir, 'bsw.json')
with open(bsw, "r") as read_file:
    data8 = json.load(read_file)

#-------------testing only------------#
#use to print functions form json readers    
#csit_info("first")
#bernhardt_data()
#faculty_info("bbs")
#--------------------------------------#

#neural network algorithm implementation//
words = []
classes = []
documents = []
ignore_words = ['?']
# loop through each sentence in our t.training data
for pattern in t.training_data:
    # tokenize each word in the sentence
    w = nltk.word_tokenize(pattern['sentence'])
    # add to our words list
    words.extend(w)
    # add to documents in our corpus
    documents.append((w, pattern['class']))
    # add to our classes list
    if pattern['class'] not in classes:
        classes.append(pattern['class'])

# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = list(set(words))

# remove duplicates
classes = list(set(classes))

print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "unique stemmed words", words)


# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    training.append(bag)
    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    output.append(output_row)

# sample training/output
i = 0
w = documents[i][0]
#print ([stemmer.stem(word.lower()) for word in w])
#print (training[i])
#print (output[i])



# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output*(1-output)

def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

def think(sentence, show_details=True):
    x = bow(sentence.lower(), words, show_details)
    if show_details:
        print ("sentence:", sentence, "\n bow:", x)
    # input layer is our bag of words
    l0 = x
    # matrix multiplication of input and hidden layer
    l1 = sigmoid(np.dot(l0, synapse_0))
    # output layer
    l2 = sigmoid(np.dot(l1, synapse_1))
    return l2



def train(X, y, hidden_neurons=10, alpha=1, epochs=50000, dropout=False, dropout_percent=0.5):

    print ("Training with %s neurons, alpha:%s, dropout:%s %s" % (hidden_neurons, str(alpha), dropout, dropout_percent if dropout else '') )
    print ("Input matrix: %sx%s    Output matrix: %sx%s " % (len(X),len(X[0]),1, len(classes)) )
    np.random.seed(1)

    last_mean_error = 1
    # randomly initialize our weights with mean 0
    synapse_0 = 2*np.random.random((len(X[0]), hidden_neurons)) - 1
    synapse_1 = 2*np.random.random((hidden_neurons, len(classes))) - 1

    prev_synapse_0_weight_update = np.zeros_like(synapse_0)
    prev_synapse_1_weight_update = np.zeros_like(synapse_1)

    synapse_0_direction_count = np.zeros_like(synapse_0)
    synapse_1_direction_count = np.zeros_like(synapse_1)

    for j in iter(range(epochs+1)):

        # Feed forward through layers 0, 1, and 2
        layer_0 = X
        layer_1 = sigmoid(np.dot(layer_0, synapse_0))

        if(dropout):
            layer_1 *= np.random.binomial([np.ones((len(X),hidden_neurons))],1-dropout_percent)[0] * (1.0/(1-dropout_percent))

        layer_2 = sigmoid(np.dot(layer_1, synapse_1))

        # how much did we miss the target value?
        layer_2_error = y - layer_2

        if (j% 10000) == 0 and j > 5000:
            # if this 10k iteration's error is greater than the last iteration, break out
            if np.mean(np.abs(layer_2_error)) < last_mean_error:
                #print ("delta after "+str(j)+" iterations:" + str(np.mean(np.abs(layer_2_error))) +"   Loading.. please wait")
                #print("Loading.. please wait")
                last_mean_error = np.mean(np.abs(layer_2_error))
            else:
                #print ("break:", np.mean(np.abs(layer_2_error)), ">", last_mean_error  +"   Loading.. please wait")
                #print("Loading.. please wait")
                break

        # in what direction is the target value?
        # were we really sure? if so, don't change too much.
        layer_2_delta = layer_2_error * sigmoid_output_to_derivative(layer_2)

        # how much did each l1 value contribute to the l2 error (according to the weights)?
        layer_1_error = layer_2_delta.dot(synapse_1.T)

        # in what direction is the target l1?
        # were we really sure? if so, don't change too much.
        layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)

        synapse_1_weight_update = (layer_1.T.dot(layer_2_delta))
        synapse_0_weight_update = (layer_0.T.dot(layer_1_delta))

        if(j > 0):
            synapse_0_direction_count += np.abs(((synapse_0_weight_update > 0)+0) - ((prev_synapse_0_weight_update > 0) + 0))
            synapse_1_direction_count += np.abs(((synapse_1_weight_update > 0)+0) - ((prev_synapse_1_weight_update > 0) + 0))

        synapse_1 += alpha * synapse_1_weight_update
        synapse_0 += alpha * synapse_0_weight_update

        prev_synapse_0_weight_update = synapse_0_weight_update
        prev_synapse_1_weight_update = synapse_1_weight_update

    now = datetime.datetime.now()

    # persist synapses
    synapse = {'synapse0': synapse_0.tolist(), 'synapse1': synapse_1.tolist(),
               'datetime': now.strftime("%Y-%m-%d %H:%M"),
               'words': words,
               'classes': classes
              }
    synapse_file = "synapses.json"

    with open(synapse_file, 'w') as outfile:
        json.dump(synapse, outfile, indent=4, sort_keys=True)
    #print ("saved synapses to:", synapse_file)




X = np.array(training)
y = np.array(output)

start_time = time.time()

train(X, y, hidden_neurons=20, alpha=0.1, epochs=100000, dropout=False, dropout_percent=0.2)

elapsed_time = time.time() - start_time
#print ("processing time:", elapsed_time, "seconds")


# probability threshold
ERROR_THRESHOLD = 0.2
# load our calculated synapse values
synapse_file = 'synapses.json'
with open(synapse_file) as data_file:
    synapse = json.load(data_file)
    synapse_0 = np.asarray(synapse['synapse0'])
    synapse_1 = np.asarray(synapse['synapse1'])


def classify(sentence,usermodel, capital_usermodel, show_details=False):
    results = think(sentence, show_details)
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD ]
    results.sort(key=lambda x: x[1], reverse=True)
    return_results =[[classes[r[0]],r[1]] for r in results]
    #print ("%s \n classification: %s" % (sentence, return_results))
    #capital_usermodel = usermodel.upper()


    #Response set
    response_greeting = ["Hmm.. What can i help you with?",
                         "Hmmm... Which faculty would u like to get information about?",
                         "Um, which faculty do you prefer?",
                         "Ahh.. which faculty would you like to search for?",
                         "Hello! Sir/Madam, how can I help you with?",
                         "Hi! How can I assist you with?",
                         "What can i help you with,please provide the details for the faculty that intrest you ?"]

    random_greeting = random.choice(response_greeting)




    response_health = ["So nice of you to ask, I'm good.",
                       "I'm fit and fine.",
                       "I am good. Thank You!",
                       "I am fine. Thank You!",
                       "I'm great and having fun."]

    random_health = random.choice(response_health)



    
    response_work = ["I can help you go through more options on college details and faculty provided. \nKBC Bot: Which faculty do you like?",
                     "I am here to provide you best information about the Kathmandu BernHardt College. \nKBC Bot: Which faculty shall i search for?",
                     "I am assigned to help you provide the information on college. \nKBC Bot: Which faculty do you want me to search for?",
                     "Helping you get the details about the college. \nKBC Bot: Which faculty do you like?",
                     "I can assist you by provideing the college information. \nKBC Bot: Which faculty do you want to look for?"]

    random_work = random.choice(response_work)



    response_faculty = ["Which faculty do you want?",
                        "Which faculty do you wish to study?",
                        "Could you please mention the faculty?",
                        "Which faculty shall I look for?"]
    randon_faculty= random.choice(response_faculty)
    

    response_semester = ["Which semester do you want?",
                        "Which semester do you wish to study?",
                        "Could you please mention the semester?",
                        "Which semester shall I look for?"]
    randon_semester=random.choice(response_semester)

    response_year = ["Which  do you want?",
                        "Which year do you wish to study?",
                        "Could you please mention the year?",
                        "Which year shall I look for?"]
    randon_year= random.choice(response_year)
    
    
    response_negative = ["What shall I do for you?",
                      "Do you want to hear a joke?",
                      "What do you want me to do?",
                      "Ok you can talk to me casually.",
                      "You can ask me anything you want to..."]
    random_negative = random.choice(response_negative) 


    response_utter = ['um', 'umm', 'hm', 'hmmm', 'ok','hrm','ummm','hmmmmumm']
    random_utter = random.choice(response_utter)


    response_jokes = ["Why did the physics teacher break up with the biology teacher? There was no chemistry.",
                      "Just changed my Facebook name to 'No one' so when I see stupid posts I can click like and it will say 'No one likes this'.",
                      "What do you call a fat psychic? A four chin teller.",
                      "If con is the opposite of pro, it must mean Congress is the opposite of progress?",
                      "If 4 out of 5 people SUFFER from diarrhea; does that mean that one enjoys it?",
                      "I used to like my neighbors, until they put a password on their Wi-Fi.",
                      "Stalking is when two people go for a long romantic walk together but only one of them knows about it.",
                      "Light travels faster than sound. This is why some people appear bright until they speak.",
                      "The only dates I get these days are software updates."]

    random_jokes = random.choice(response_jokes)


    response_laugh = ['hehe', 'haha', 'glad that i made you laugh ^__^']
    random_laugh = random.choice(response_laugh)


    response_love = ['i love you too',
                     'but i dont',
                     'You can love me. I am just a bot',
                     'Thanks for loving me']
    random_love = random.choice(response_love)


    response_thanks = ["You're welcome!","Anytime :)", "My pleasure", "Mention not, I'm happy to help",
                       "You're most welcome, do text if something comes up", "so glad i could be of any help :)",
                       "You're most welcome",
                       "Please do visit if you have anymore query"]
    random_thanks = random.choice(response_thanks)

   
    response_goodbye = ["Bye!","Bye Bye :)","Bye! Take care.", "Okay bye! See you later", "sayonara!", "TaTa",
                        "That was nice talking to you.", "That was nice talking to you. Bye!!"]

    random_goodbye = random.choice(response_goodbye)


    response_whelse = ['I can tell you jokes',
                         'I can make you laugh.',
                         'You can tell me to make you laugh.',
                         'I can crack jokes..']
    random_whelse = random.choice(response_whelse)




    response_recommend = ['No',
                         'I am not trained for that.',
                         'I can only suggest you by providing college information. \nKBC Bot: Which faculty do you prefer?',
                         'I can only find and provide college information. \nKBC Bot: Which brand phones do you like?']
    random_recommend = random.choice(response_recommend)
    



    response_fallback = ['Sorry?',
                         'I am sorry, I didnt understand it.',
                         'Excuse me, I didnt understand.',
                         'I cannot understand what you are trying to say.',
                         'Can you say that again?',
                         'Sorry, I cannot understand what you are trying to say...']
    random_fallback = random.choice(response_fallback)



    try:
        if return_results[0][0] == "":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: Say something??")
            fp.close()
        
        if return_results[0][0] == "greeting":
            time.sleep(1)
            fp = open(op,'w')
            fp.write("KBC Bot: "+ random_greeting)
            fp.close()

        elif return_results[0][0] == "health":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: "+ random_health)
            fp.close()
                
                
        elif return_results[0][0] == "work":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: " + random_work)
            fp.close()
    
        #----- clz info
        elif return_results[0][0] == "bernhardt":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: " + bernhardt_data())
            fp.close()
        #----faculty details
        elif return_results[0][0] == "faculty":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: Faculties currently available in KBC are:"+"*************************************************"+"\n(1)\tBSc CSIT\n(2)\tBCA\n(3)\tBBM\n(4)\tBBS\n(5)\tMBS\n(6)\tBASW")
            fp.close()
        #------ fee details
        elif return_results[0][0] == "csitfee":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: " + faculty_fee('csit'))
            fp.close()
        elif return_results[0][0] == "bcafee":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: " + faculty_fee('bca'))
            fp.close()
        elif return_results[0][0] == "bbmfee":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: " + faculty_fee('bbm'))
            fp.close()
        elif return_results[0][0] == "bbsfee":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: " + faculty_fee('bbs'))
            fp.close()
        elif return_results[0][0] == "mbsfee":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: " + faculty_fee('mbs'))
            fp.close()
        elif return_results[0][0] == "bswfee":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: " + faculty_fee('bsw'))
            fp.close()

        
        #csitdetails
        elif return_results[0][0] == "csitdetails":
            faculty_info("csit")
            fp = open(op, 'w')
            fp.write("KBC Bot: Do you want more details? Which semester or year you want to know about?"+"\nKBC Bot: Or ask about another faculty that interests you.")
            fp.close()
            if (capital_usermodel=="CSIT" or usermodel=="BSCCSIT"):
                sentence = input("You: ")
                if(sentence.upper()=="FIRST" or sentence.upper()=="SECOND" or sentence.upper()=="THIRD" or sentence.upper()=="FOURTH" or sentence.upper()=="FIFTH" or sentence.upper()=="SIXTH" or sentence.upper()=="SEVENTH" or sentence.upper()=="EIGHT"):
                    csit_info(sentence.upper())
                else:
                    app_flow(sentence)
        #bcadetails
        elif return_results[0][0] == "bcadetails":
            time.sleep(1)
            faculty_info("bca")
            fp = open(op, 'w')
            fp.write("KBC Bot: Do you want more details? Which semester or year you want to know about?"+"\nKBC Bot: Or ask about another faculty that interests you.")
            fp.close()
            if (capital_usermodel=="BCA"):
                if(sentence.upper()=="FIRST" or sentence.upper()=="SECOND" or sentence.upper()=="THIRD" or sentence.upper()=="FOURTH" or sentence.upper()=="FIFTH" or sentence.upper()=="SIXTH" or sentence.upper()=="SEVENTH" or sentence.upper()=="EIGHT"):
                    fp = open(op, 'a')
                    fp.write(bca_info(sentence.upper()))
                    fp.close()
                else:
                    app_flow(sentence)
        #bbmdetails
        elif return_results[0][0] == "bbmdetails":
            time.sleep(1)
            faculty_info("bbm")
            fp = open(op, 'w')
            fp.write("KBC Bot: Do you want more details? Which semester or year you want to know about?"+"\nKBC Bot: Or ask about another faculty that interests you.")
            fp.close()
            if (capital_usermodel=="BBM"):
                if(sentence.upper()=="FIRST" or sentence.upper()=="SECOND" or sentence.upper()=="THIRD" or sentence.upper()=="FOURTH" or sentence.upper()=="FIFTH" or sentence.upper()=="SIXTH" or sentence.upper()=="SEVENTH" or sentence.upper()=="EIGHT"):
                    fp = open(op, 'a')
                    fp.write(bbm_info(sentence.upper()))
                    fp.close()
                else:
                    app_flow(sentence)

        #bbsdetails
        elif return_results[0][0] == "bbsdetails":
            time.sleep(1)
            faculty_info("bbs")
            fp = open(op, 'w')
            fp.write("KBC Bot: Do you want more details? Which semester or year you want to know about?"+"\nKBC Bot: Or ask about another faculty that interests you.")
            fp.close()
            if (capital_usermodel=="BBS"):
                if(sentence.upper()=="FIRST" or sentence.upper()=="SECOND" or sentence.upper()=="THIRD" or sentence.upper()=="FOURTH"):
                    fp = open(op, 'a')
                    fp.write(bbs_info(sentence.upper()))
                    fp.close()
                else:
                    app_flow(sentence)

        #mbsdetails
        elif return_results[0][0] == "mbsdetails":
            time.sleep(1)
            faculty_info("mbs")
            fp = open(op, 'w')
            fp.write("KBC Bot: Do you want more details? Which semester or year you want to know about?"+"\nKBC Bot: Or ask about another faculty that interests you.")
            fp.close()
            if (capital_usermodel=="MBS"):
                if(sentence.upper()=="FIRST" or sentence.upper()=="SECOND"):
                    fp = open(op, 'a')
                    fp.write(mbs_info(sentence.upper()))
                    fp.close()
                else:
                    app_flow(sentence)
        #bswdetails
        elif return_results[0][0] == "bswdetails":
            time.sleep(1)
            faculty_info("bsw")
            fp = open(op, 'w')
            fp.write("KBC Bot: Do you want more details? Which semester or year you want to know about?"+"\nKBC Bot: Or ask about another faculty that interests you.")
            fp.close()
            if (capital_usermodel=="BSW" or usermodel=="BASW"):
                if(sentence.upper()=="FIRST" or sentence.upper()=="SECOND" or sentence.upper()=="THIRD" or sentence.upper()=="FOURTH"):
                    fp = open(op, 'a')
                    fp.write(bsw_info(sentence.upper()))
                    fp.close()
                else:
                    app_flow(sentence)        
        
        
                          
        elif return_results[0][0] == "negative":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: "+ random_negative)
            fp.close()
        elif return_results[0][0] == "utter":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: "+ random_utter)
            fp.close()

        elif return_results[0][0] == "jokes":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: "+ random_jokes)
            fp.close()

        elif return_results[0][0] == "laugh":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: "+ random_laugh)
            fp.close()


        elif return_results[0][0] == "love":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: "+ random_love)
            fp.close()

        elif return_results[0][0] == "thanks":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: "+ random_thanks)
            fp.close()

        elif return_results[0][0] == "whelse":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: "+ random_whelse)
            fp.close()

        elif return_results[0][0] == "recommend":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: "+ random_recommend)
            fp.close()

        elif return_results[0][0] == "exit":
            time.sleep(1)
            fp = open(op, 'w')
            fp.write("KBC Bot: "+ random_goodbye)
            fp.close()
            time.sleep(1.5)
            print("**************************************************************************")
            sys.exit()


        else:
            fp = open(op, 'w')
            fp.write("KBC Bot: "+ random_fallback)
            fp.close()


    except IndexError:
        #print(sentence)
        response_fallback = ['Sorry?',
                             'I am sorry, I didnt understand it.',
                             'Excuse me, I didnt understand.',
                             'I cannot understand what you are trying to say.',
                             'Can you say that again?',
                             'Sorry, I cannot understand what you are trying to say...']
        random_fallback = random.choice(response_fallback)

        fp = open(op, 'w')
        fp.write("KBC Bot: "+ random_fallback)
        fp.close()
        pass

    except TypeError:
        #print("KBC Bot:error")
        pass

    except ValueError:
        #print("KBC Bot: value error")
        pass
    
    return return_results
        



#KBC Bot conversation
#x=0
#while(x<=100):
#    print( )
#    x = x + 1
    
fp = open(op,'w')
fp.write("\n\n----------------KBC Bot: Kathmandu BernHardt College Inforamtion Bot------------------\n"+"KBC Bot: Hello I am KBC Bot."+"KBC Bot: I am here to provide you details about Kathmandu BernHardt College.")
fp.close()
time.sleep(0.8)

def app_flow(sentence):
    #model detection
    word_tokens = nltk.word_tokenize(sentence)
    #print(word_tokens)
    stop_words = list(set(stopwords.words('english')))
    stop_words.extend(['guys', 'please', 'want', 'hi', 'KBC Bot', 'KBC Bot', 'whats', 'what\'s', 'hm', 'so',
                       'hmm', 'um','ok', 'check', 'need', '?', 'available', 'u', 'nepal', 'know',
                       'provide', 'me', 'look', "'s", 'specify', 'search', 'find', 'mention', 'pls', 'plz', 'current', 'tell', 'hello', 'KBC Bot', 'how', 'are', 'you',
                       'best', 'different', 'various', 'website', 'websites', 'give', 'show','can','you','is','location','website','college','provide', ])

    filtered_model = [w for w in word_tokens if not w in stop_words]

    usermodel = ' '.join(map(str, filtered_model))
    #print (usermodel)
    capital_usermodel = usermodel.upper()
    #print(capital_usermodel)

    faculty_list =["csit", "bsccsit", "bsc.csit", "bca", "bbm", "bbs", "mbs", "bsw", "basw"]
    lower_faculty_list = []
    for faculty in faculty_list:
        lower_faculty_list.append(faculty.lower())
    if usermodel in faculty_list or usermodel in lower_faculty_list:
        #use model ma use gareko code haru
        #print("found.")

        response_model = ["Okay, I will search for it. Can you please wait for a second?",
                          "Okay, just hold on for a second!","Ok just wait a sec",
                          "Searching..could you please wait for some time?",
                          "Sure!I will search for it",
                          "Ok, I will search for it..."]
        random_model = random.choice(response_model)
        
       
       
            
        faculty_model = []
        for i in range(8):
            faculty_model.append(data2[i]['Faculty'])

        
        
        if usermodel in faculty_model or capital_usermodel in faculty_model:
            time.sleep(1.5)
            faculty_info(usermodel)
            return 0

        else:

            response_sorry = ["Sorry, this faculty is not available.",
                              "Can you please search for other faculties?",
                              "Sorry this faculty is unvailable.",
                              "Sorry this faculty is not available."]
            random_sorry = random.choice(response_sorry)    
            time.sleep(2)
            fp = open(op, 'w')
            fp.write("KBC Bot: "+ random_sorry)
            fp.close()
            

    else:
        #save user logs to user log file
        #print("chaina")
        path = './'
        fileName = 'usertextlogs'

        now = datetime.datetime.now()

        data = {}
        data['sentence'] = sentence
        data['datetime'] = now.strftime("%Y-%m-%d %H:%M")

        writeToJSONFile(path, fileName, data)
        #print("Log recored to "+ fileName)

        sentence = classify(sentence, usermodel, capital_usermodel)


def getMessage(sentence):
    app_flow(sentence)
    return 0


    

                





