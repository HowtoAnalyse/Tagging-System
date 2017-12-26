import pandas as pd
raw = pd.read_csv("mysite/raw.csv", nrows=238)
import os
di = {'i': "客服", 'he': "客户"}
raw = raw.replace({"speaker": di})
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

conn = MySQLdb.connect("127.0.0.1","sara302","skip200Gram","polls" )
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

# mysql
import MySQLdb

conn = MySQLdb.connect("127.0.0.1","sara302","skip200Gram","polls",charset='utf8',use_unicode=True)
c = conn.cursor()
c.execute("delete from polls_conversation;")
conn.commit()
c.execute("delete from polls_label;")
conn.commit()

c.execute("delete from polls_question;")
conn.commit()


c.execute("describe polls_question;")
conn.commit()

c.execute("alter table polls_conversation DEFAULT CHARACTER SET utf8;")
conn.commit()
c.execute("alter table polls_label DEFAULT CHARACTER SET utf8;")
conn.commit()

# c.execute("delete from polls_conversation")
# conn.commit()


# c.fetchall()
# alter table TableName DEFAULT CHARACTER SET utf8;
# id, question_text, labeled, pub_date
qRaw = raw.drop_duplicates(subset='msg_id', keep="last")
gDF = pd.DataFrame()
n=1
for idx, row in qRaw.iterrows():
	sql = "update polls_question set groupid = " + str(n%8+1) + " where id=" + str(row['msg_id'])
	try:
		c.execute(sql)
		conn.commit()
	except:
		gDF = gDF.append(row)
	n += 1



qDF = pd.DataFrame()
n=1
for idx, row in qRaw.iterrows():
	try:
		sql = "insert into polls_question values ({}, 'question_{}',0,now()".format(row[0], row[0]) + ");"
		c = conn.cursor()
		c.execute(sql)
		conn.commit()
		n += 1
	except:
		qDF = qDF.append(row)

# id, roundid, center_bool, label_text, question_id
lRaw = raw.drop_duplicates(subset=['msg_id','round','speaker'], keep="first")
lDF = pd.DataFrame()
n=1
for idx, row in lRaw.iterrows():
	try:
		# id, roundid, center_bool, text, qid, speaker
		sql = "insert into polls_label values ({},{},{}, 'NA',{},\'{}\'".format(idx, row[1], row[2], row[0], row[3]) + ");"
		c = conn.cursor()
		c.execute(sql)
		conn.commit()
		n += 1
	except:
		lDF = lDF.append(row)

# id, roundid, speaker, center_bool, conversation_txt, question_id
c.execute("select * from polls_conversation where id = 228;")
c.fetchall()

tmpDF = pd.DataFrame()
for idx, row in raw.iterrows():
	sql = "insert into polls_conversation values ({}, {}, \'{}\', {},\'{}\', {}".format(idx, row[1], row[3], row[2],row[4], row[0]) + ");"
	try:
		c.execute(sql)
		conn.commit()
	except:
		tmpDF = tmpDF.append(row)

errorDF = pd.DataFrame()	
for idx, row in tmpDF.head().iterrows():
	sql = "insert into polls_conversation values ({}, {}, \"{}\", {},\"{}\", {}".format(idx, row[1], row[3], row[2],row[4], row[0]) + ");"
	try:
		c.execute(sql)
		conn.commit()
	except:
		errorDF = errorDF.append(row)
## labels

conn.close()