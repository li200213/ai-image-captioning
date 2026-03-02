from config import conn

cur = conn.cursor()

def add_history(username, time,img_src,text_type,emotion,text):
	sql = "INSERT INTO history(username,time,img_src,text_type,emotion,text) VALUES ('%s','%s','%s','%s','%s','%s')" %(username,time,img_src,text_type,emotion,text)
	conn.ping(reconnect=True)
	cur.execute(sql)
	conn.commit()
	conn.close()

def show_history(username):
	sql = "SELECT * FROM history WHERE username ='%s'" % (username)
	conn.ping(reconnect=True)
	cur.execute(sql)
	result = cur.fetchall()
	conn.close()
	if (len(result) == 0):
		return None
	else:
		return result