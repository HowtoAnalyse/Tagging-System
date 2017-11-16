import pandas as pd
raw = pd.read_csv("qa/static/data/raw.csv")
import os

raw = raw.fillna("...")
msgID = raw['msg_id'].unique()

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




# df = raw[['round', 'speaker','text','msg_id']]
# df.columns = ['roundid', 'speaker', 'Conversation_txt', 'question_id']
import sqlite3

conn = sqlite3.connect('db.sqlite3')
tmpDF = pd.DataFrame()
for idx, row in raw.iterrows():
	try:
		sql = "insert into qa_conversation values ({}, {}, \'{}\', \'{}\', {}".format(idx, row[1], row[2], row[3],row[0]) + ");"
		c = conn.cursor()
		c.execute(sql)
		conn.commit()
	except:
		tmpDF = tmpDF.append(row)

errorDF = pd.DataFrame()	
for idx, row in tmpDF.iterrows():
	try:
		sql = "insert into qa_conversation values ({}, {}, \"{}\", \"{}\", {}".format(idx, row[0], row[2], row[3],row[1]) + ");"
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
		sql = "insert into qa_question values ({}, 'title{}','description{}', datetime('now'), 1, 0, 0, 0, 0, 'slug{}', {}".format(row[0], row[0], row[0], row[0], n) + ");"
		c = conn.cursor()
		c.execute(sql)
		conn.commit()
		n += 1
	except:
		qDF = qDF.append(row)

conn.close()
