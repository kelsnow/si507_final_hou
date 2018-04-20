#--------This file is used to build up the database from the data scraped from MIT the Media Lab and provide---------
#-------- interactivity to end users---------


# building up data base 
import pandas as pd
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from flask import Flask
import sqlite3
import json 
import nltk 
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
stop_words = set(stopwords.words('english'))


DBNAME = 'media.db'
MEDIA_JSON = 'media.json'


f_json = open(MEDIA_JSON,'r')
f_data = f_json.read()
media_data = json.loads(f_data)

f_json_1 = open('hashtag.json','r')
f_data_1 = f_json_1.read()
hashtag_data = json.loads(f_data_1)


try:
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
except Exception as e:
    print (e)


statement= '''
    DROP TABLE IF EXISTS 'Labs'; 
'''
cur.execute(statement)

statement='''
    DROP TABLE IF EXISTS 'Projects';
'''
cur.execute(statement)


statement='''
    DROP TABLE IF EXISTS 'Hashtags';
'''
cur.execute(statement)


statement='''
    CREATE TABLE 'Labs'(
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name Text NOT NULL,
        LabBrief Text NOT NULL,
        PrimaryInstructor Text,
        PeopleNumber Integer,
        HashtagNumber Integer
    );
'''

cur.execute(statement)
conn.commit()


statement = '''
    CREATE TABLE 'Projects'(
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name Text NOT NULL,
        ProjectBrief Text,
        LabName Text NOT NULL
    );
'''
cur.execute(statement)
conn.commit()



statement = '''
    CREATE TABLE 'Hashtags'(
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name Text NOT NULL     
    );
'''
cur.execute(statement)
conn.commit()


#-----------POPULATE TABLE----------------

# Table Labs
for i in media_data.keys():
	insertion = (None,i,media_data[i]['brief'],media_data[i]['director'],media_data[i]['peoplenum'],media_data[i]['hashnum'])
	statement = "INSERT INTO 'Labs'"
	statement+="VALUES (?,?,?,?,?,?)"
	cur.execute(statement,insertion)

conn.commit()

# Table Hashtags 
for i in hashtag_data:
	insertion = (None,i)
	statement = "INSERT INTO 'Hashtags'"
	statement+="VALUES (?,?)"
	cur.execute(statement,insertion)

conn.commit()

# Table Projects 

for i in media_data.keys():
	for j in media_data[i]['projects'].keys():	
		# print(media_data[i]['projects'][j]['brief'])
		insertion = (None,j,media_data[i]['projects'][j]['brief'],i)
		statement = "INSERT INTO 'Projects'"
		statement+="VALUES (?,?,?,?)"
		cur.execute(statement,insertion)

conn.commit()

# Adding foreign key
statement = '''
    ALTER TABLE Projects
    ADD COLUMN LabId INTEGER;
'''

cur.execute(statement)
conn.commit()


statement='''
        UPDATE  Projects
        SET LabId = (
			SELECT Labs.Id 
			FROM Labs
			WHERE Labs.Name = Projects.LabName   
        )               
        '''
cur.execute(statement)
conn.commit()


statement = "SELECT LabBrief FROM Labs"
cur.execute(statement)
conn.commit()
lab_brief_lst = []
for row in cur:
    lab_brief_lst.append(' '.join([str(x) for x in row]))

# print(brief_lst)

statement = "SELECT ProjectBrief FROM Projects"
cur.execute(statement)
conn.commit()
project_brief_lst = []
for row in cur:
    project_brief_lst.append(' '.join([str(x) for x in row]))




#Part2---------------Data Analysis and ploting  -----------

# function to get the top 10 words of lab brief 
def get_top_ten_Brief(lst):
    

    tokens = []
    for i in lst:
        tokens.append(nltk.word_tokenize(i.lower()))

    # frequency distribution of tokenized list with stop words taken out 
    alphabet = list(string.ascii_lowercase)
    fre_dis = {}
    # print(tokens[1])
    for i in tokens:
        for j in i:
            if j[0] in alphabet:
                if j not in stop_words:
                    if j in fre_dis:
                        fre_dis[j] +=1
                    else:
                        fre_dis[j] =1


    sorted_fre_lst = sorted(fre_dis.items(),key = lambda x:x[1],reverse = True)

    top_five=[]
    for i in range(10):
        top_five.append(sorted_fre_lst[i])  
        
        ("{},({})".format(sorted_fre_lst[i][0],sorted_fre_lst[i][1]))
    return top_five
    


# five = get_top_five_Brief(lab_brief_lst)
# print(five)

project_five = get_top_ten_Brief(project_brief_lst)
# print(project_five)


#-------------------Graphs-----------------------
lab_name =[]
lab_peoplenum = []
lab_hashnum=[]

for i in media_data.keys():
    lab_name.append(i)
    lab_peoplenum.append(media_data[i]['peoplenum'])
    lab_hashnum.append(media_data[i]['hashnum'])

def plot_lab_size():

    trace1 = go.Bar(
    x=lab_name,
    y=lab_peoplenum,
    name='lab size',
    marker=dict(
        color='#FFD7E9',
    ),
    opacity=0.75
    )


    data = [trace1]
    layout = go.Layout(
    title='Lab size distribution',
    xaxis=dict(
        title='labs'
    ),
    yaxis=dict(
        title='lab people number'
    ),
    bargap=0.02,
    bargroupgap=0.01
    )

    fig = go.Figure(data=data, layout=layout) 
    py.plot(fig, filename='styled histogram')

# plot_lab_size(lab_name,lab_peoplenum)


def plot_lab_hashnum():
    trace1 = go.Bar(
    x=lab_name,
    y=lab_hashnum,
    name='lab size',
    marker=dict(
        color='#0DA35E',
    ),
    opacity=0.75
    )


    data = [trace1]
    layout = go.Layout(
    title='Lab hashtag distribution',
    xaxis=dict(
        title='labs'
    ),
    yaxis=dict(
        title='hashtag numbers'
    ),
    bargap=0.02,
    bargroupgap=0.01
    )

    fig = go.Figure(data=data, layout=layout) 
    py.plot(fig, filename='styled histogram')

# plot_lab_hashnum(lab_name,lab_hashnum)

def get_index_sameLabId(LabIds,myLabId):
    outIndx = []
    for cindx in range(0,len(LabIds)):
        if LabIds[cindx] == myLabId:
           outIndx.append(cindx)
    return outIndx

def getString_forwdcloud_fromSameLabID(DF,LabIds,myLabId,indxBrief):
    indxs_inputLabId = get_index_sameLabId(LabIds,myLabId)
    cID_wordstring = ""
    for cline in indxs_inputLabId:
        cID_wordstring = cID_wordstring + str(DF.iloc[cline, indxBrief])
    return cID_wordstring   

def plot_cloud(lab_id):
    app = Flask(__name__)
    # read file as dataframe
    MYDF = pd.DataFrame(pd.read_csv("Projects.csv"))
    # check file column names
    # print(MYDF.columns.values)

    Nlabid = len(set(MYDF ["LabId"]))
    INDX_BRIEF = MYDF .columns.get_loc("ProjectBrief") #global var, the column of brief


    # for c_labid in set(MYDF ["LabId"]):
    cbreif_string = getString_forwdcloud_fromSameLabID(MYDF ,MYDF["LabId"],lab_id, INDX_BRIEF )
    wordcloud = WordCloud(background_color="white",width=1000, height=860, margin=2).generate(cbreif_string)
    cfile = "labid" + str(lab_id) + ".wordcloud.png"
    # wordcloud.to_file(cfile)
    @app.route('/')
    def cloud():
        im_src = "/static/"+cfile
        tag = '<img src='+ im_src+ ' />'
        return tag
    if __name__ == '__main__':
        app.run(debug = True)

    # return cfile

# plot_cloud(1)


# -----------------------interactivity---------------
def interactive_prompt():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    print("Hey there, we finally meet.Here is a list of all the lab groups in MIT the Media lab")
    c = 1
    for i in media_data.keys():
        print(c, i)
        c+=1

    answer=input("Choose a lab Id for more information (or 'help' for options or 'quit'): ")

    while answer.lower() != "quit":
        
        if answer.lower() == "help":
            lst_command = "info <labId> \n available anytime\n lists all the labs in Media lab \n valid inputs: an integer\n"
            lst_command+= "top brief \n available anytime \n we would give you the top 10 most used words in the lab groups'brief\n"
            lst_command+= "plot size \n available anytime \n we would provide you with the graphs of the size of each lab\n"
            lst_command+= "plot hashtag \n available anytime \n we would provide you with the graphs of the number of hashtags(research topics) each lab has\n"
            lst_command+= "plot cloud <labId> \n available anytime \n We would generate a wordcloud for the specific lab for you\n"
            lst_command+= "quit \n quit the program\n"
            lst_command+="help \n   lists availabe commands"

            print(lst_command)
            answer = input("Choose a lab Id for more information (or 'help' for options or 'quit'): ")
        elif answer.lower().startswith('plot'):
            if answer.lower().split()[1].lower() == 'size':
                plot_lab_size()
            elif answer.lower().split()[1].lower() == 'hashtag':
                plot_lab_hashnum()
            elif answer.lower().split()[1].lower() == 'cloud':
                try: 
                    plot_cloud(answer.lower().split()[2])
                except:
                    print("command not recognized")
                    answer = input("Choose a lab Id for more information (or 'help' for options or 'quit'): ")
            else:
                print("command not recognized")
                answer = input("Enter some commands (or 'help' for options or 'quit'): ")
        elif answer.lower().startswith('top'):
            get_top_ten_Brief(lab_brief_lst)
        elif answer.lower().startswith('info'):
            try: 
                print(answer.lower().split()[1])
                statement = '''
                    SELECT Name, LabBrief,PrimaryInstructor
                    FROM Labs WHERE Id = ?
                '''
                params = (answer.lower().split()[1],)
                cur.execute(statement,params)
                for row in cur:
                    print("Lab Name: " +row[0] + "Lab Brief: " + row[1] + "Primary Instructor: " + row[2])
                answer = input("Enter some commands (or 'help' for options or 'quit'):")
            except:
                print("command not recognized")
                answer = input("Choose a lab Id for more information (or 'help' for options or 'quit'): ")
        else:
            print("command not recognized")
            answer = input("Enter some commands (or 'help' for options or 'quit'):")
            



    

interactive_prompt()






























