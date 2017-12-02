import pandas as pd
raw = pd.read_csv("mysite/raw.csv")
import os

raw = raw.fillna("...") #96180
msgID = raw['msg_id'].unique()

centerRound = raw[raw["round_center_bool"]==1] #28050
# raw.loc[(raw["msg_id"] ==108679) & (raw["round"] == 3),"round_center_bool"]

for idx, row in centerRound.iterrows():
	raw.loc[(raw["msg_id"] ==row["msg_id"]) & (raw["round"] == row["round"]+1),"round_center_bool"]=2

directory = "qa/static/data/batch"
n=0
for i in msgID:
	fID = str(n//800+1)
	newDir = directory+fID+"/"
	if not os.path.exists(newDir):
		os.makedirs(newDir)
	newDF = raw[raw['msg_id']==i]
	newDF.to_csv(newDir+"msg"+str(n)+".csv", index=False,encoding='utf-8')
	n += 1

%timeit df.set_value('C', 'x', 10)

%timeit df['x']['C'] = 10

%timeit df.at['C', 'x'] = 10


# df = raw[['round', 'speaker','text','msg_id']]
# df.columns = ['roundid', 'speaker', 'Conversation_txt', 'question_id']
import sqlite3

conn = sqlite3.connect('db.sqlite3')
lRaw = raw.drop_duplicates(subset=['msg_id', 'round'], keep="last")
lDF = pd.DataFrame()
n=1
for idx, row in lRaw.iterrows():
	try:
		sql = "insert into polls_label values ({},{},{}, 'NA',{}".format(idx, row[1], row[2], row[0]) + ");"
		c = conn.cursor()
		c.execute(sql)
		conn.commit()
		n += 1
	except:
		lDF = lDF.append(row)

conn.close()


c = conn.cursor()
c.execute("PRAGMA table_info(qa_conversation);")
c.fetchall()
tmpDF = pd.DataFrame()
for idx, row in raw.iterrows():
	try:
		sql = "insert into polls_conversation values ({}, {}, \'{}\', {},\'{}\', {}".format(idx, row[1], row[3], row[2],row[4], row[0]) + ");"
		c = conn.cursor()
		c.execute(sql)
		conn.commit()
	except:
		tmpDF = tmpDF.append(row)

errorDF = pd.DataFrame()	
for idx, row in tmpDF.iterrows():
	try:
		sql = "insert into polls_conversation values ({}, {}, \"{}\", {},\"{}\", {}".format(idx, row[1], row[3], row[2],row[4], row[0]) + ");"
		c = conn.cursor()
		c.execute(sql)
		conn.commit()
	except:
		errorDF = errorDF.append(row)
## labels
labelDF = pd.DataFrame()
for idx, row in raw.iterrows():
	try:
		sql = "insert into qa_answer values ({}, 'label{}', datetime('now'), {}, 0, datetime('now'), 0, 0, 0".format(idx, row[2], row[0]) + ");"
		c = conn.cursor()
		c.execute(sql)
		conn.commit()
	except:
		labelDF = labelDF.append(row)

qRaw = raw.drop_duplicates(subset='msg_id', keep="last")

qDF = pd.DataFrame()
n=1
for idx, row in qRaw.iterrows():
	try:
		sql = "insert into polls_question values ({}, 'description{}', datetime('now'), 0".format(row[0], row[0]) + ");"
		c = conn.cursor()
		c.execute(sql)
		conn.commit()
		n += 1
	except:
		qDF = qDF.append(row)

conn.close()