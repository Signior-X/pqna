from flask import Flask, render_template, jsonify, request
import random
import json

# ----------------- app configurations -----------------
app = Flask(__name__)

# ----------------- Summary ----------------------------
'''
Variables:
    last_question_number - Integer
    qdics - Questions dictionary
    players - Players dictionary

Functions:
    generate_ques() - Generate random and questions
    read_sample_data_file() - Read the database sample.json

Routes:
    / - index

APIs:
    /api/generate - Generate a new question
    /api/increase - Update the score
    /api/create - Create database (Private)
    /api/getdata - Get the current database (Private)

'''

# ----------------- Variables --------------------------
'''
After changing the variables don't forget to create a new sample.json
'''

last_question_number = 19

qdics = {
    0: 'Has ***** ever dated his friend\'s ex?',
    1: 'Kya ***** ka byah hogya?',
    2: 'Has ***** ever kissed a stranger?',
    3: '***** has ever fantasised about a teacher?',
    4: 'Can ***** murder someone?',
    5: 'Kya ***** fantasised about having sex with a dog?',
    6: 'Has ***** ever kissed a person of same gender?',
    7: 'Does ***** ever had sexted with the person of same sex',
    8: 'The best friend of Rachita is *****.',
    9: 'Has ***** ever got laid with opposite gender?',
    10: 'Has ***** ever broke someone\'s heart?',
    11: '***** had a friend with benefits scene?',
    12: '***** had been in a secret relationship.',
    13: '***** likes bdsm?',
    14: 'Does ***** likes his cream?',
    15: '***** likes to smoke weed',
    16: 'Has ***** ever smoked a cigarette?',
    17: 'Has ***** ever made out with someone?',
    18: 'Kya ***** ne kabhi saste nashe kiye hai?',
    19: '***** has ever peed in a pool.'
}

# qdics = {
#     0: 'Has ***** ever pissed on the bed?',
#     1: 'Does ***** likes to play pubg?',
#     2: 'Kya ***** aagyakari bacha hai?',
#     3: 'Kya ***** din bhar phone ma laga rehta hai?',
#     4: 'Kya ***** ko sab pareshaan karte hai?',
#     5: 'Kya ***** ko sab maarte hai',
#     6: 'Kya ***** ne kabhi mummy ko pareshaan kiya hai?',
#     7: 'Kya ***** abhi chatting ma laga rehta hai?',
#     8: 'Kya ***** kabhi mummy se maar khaya hai?',
#     9: 'Kya ***** ne kabhi muh se makhi khayi hai?'
# }

last_player = 9
players = {
    0: 'Aryan',
    1: 'Sarthak',
    2: 'Khubi',
    3: 'Dhruv',
    4: 'Devansh',
    5: 'Parshva',
    6: 'Priyam',
    7: 'Anshika',
    8: 'Deepali',
    9: 'Atul'
}


# ----------------- Functions ---------------------
'''
Function to generate a random question
'''
def generate_ques():
    '''
    params: none

    return:
        qr: random question
        pr: random person
        qname: Complete question
    '''
    qr = random.randint(0, last_question_number)
    pr = random.randint(0, last_player)
    # print(qr,pr)
    qname = qdics[qr].replace("*****", players[pr])

    return qr,pr,qname

'''
Function to read the sample data file where data is stored
'''
def read_sample_data_file():
    '''
    params: none

    return:
        json_object (dictionary) - The data present in the sample.json
    '''
    # Opening JSON file
    with open('sample.json', 'r') as openfile:

        # Reading from json file
        json_object = json.load(openfile)

    return json_object
    # print(type(json_object)) # dictionary

'''
Function to write the sample data file where data is stored
'''
def write_sample_data_file(dic):
    '''
    params: dic (dictionary) - The data to update

    return: none
    '''

    # Serializing json
    json_object = json.dumps(dic, indent = 4)

    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

    # Done

# ----------------- Routes --------------------
# Most of the work is done in the frontend in the javascript
@app.route('/')
def index():
    qr, pr, qname = generate_ques()
    return render_template('index.html', qno=qr, pno=pr, ques=qname )

@app.route('/agreed')
def agree():
    data  = read_sample_data_file()
    # print(data)

    new_dic = {}

    for i in data:
        for j in data[i]:
            key_to_set = qdics[int(j)].replace('*****', players[int(i)])
            data_to_set = data[i][j]['yes']
            if(data_to_set != 0):
                new_dic[key_to_set] = data_to_set

    sorted_dic = {k: v for k, v in sorted(new_dic.items(), key=lambda item: item[1])}

    print(sorted_dic)
    return render_template('popular.html', data=sorted_dic)

@app.route('/disagreed')
def disagree():
    data  = read_sample_data_file()
    # print(data)

    new_dic = {}

    for i in data:
        for j in data[i]:
            key_to_set = qdics[int(j)].replace('*****', players[int(i)])
            data_to_set = data[i][j]['no']
            if(data_to_set != 0):
                new_dic[key_to_set] = data_to_set

    sorted_dic = {k: v for k, v in sorted(new_dic.items(), key=lambda item: item[1])}

    print(sorted_dic)
    return render_template('popular.html', data=sorted_dic)

@app.route('/ranks')
def ranklist():
    data = read_sample_data_file()

    new_dic = {}

    # Loop to create a new dictionary
    for i in data:
        for j in data[i]:
            key_to_set = qdics[int(j)].replace('*****', players[int(i)])
            data_to_set = {'no': data[i][j]['no'], 'yes': data[i][j]['yes']}

            # check for so that not both are false at the same time
            if((data_to_set['no'] != 0) or (data_to_set['yes'] != 0)):
                new_dic[key_to_set] = data_to_set

    return render_template('popular.html', data=new_dic)
# End of ranks page

# ----------------- APIs ----------------------

'''
API to generate a new random variable

return:
    qr - question number
    pr - person number
    qname - question name
'''
@app.route('/api/generate', methods=['POST'])
def generate():
    qr, pr, qname = generate_ques()
    return jsonify(qr=qr,pr=pr,qname=qname)
# End of generate API

'''
API To increase the points

params:
    pno: person numner
    qno: question number
    option: yes or no

return:
    success: 1 or 0
'''
@app.route('/api/increase', methods=['POST'])
def add_score():
    current_data = read_sample_data_file()

    pno = str(request.json['pno'])
    qno = str(request.json['qno'])
    option = str(request.json['option']) # option is yes or no
    print(pno,qno,option)

    # print(current_data)

    current_data[pno][qno][option] += 1

    # print(current_data)
    write_sample_data_file(current_data)

    return jsonify(success=1)
# End of increase score API

'''
To create a new file
It creates a new sample.json
Thus, it is resetting the score

return:
    json_data of sample.json (Empty)
'''
@app.route('/api/create')
def create_database():
    dic = dict()
    # Data to be written
    for i in players:
        dic[i] = {}
        for j in qdics:
            dic[i][j] = {'yes': 0, 'no': 0}

    # Serializing json
    json_object = json.dumps(dic, indent = 4)

    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

    # Return what dictionary it has created
    return dic
# End of create database API

'''
API to check the data stored in the sample.json file
different from ranklist
'''
@app.route('/api/getdata')
def get_data():
    json_object = read_sample_data_file()

    return json_object
# End of get current data


if __name__ == "__main__":
    app.run(debug = True)
