import pg8000
conn = pg8000.connect(user="postgres", password="smith620695", database="form")
cursor = conn.cursor()
cursor.execute("select question from answer as a, question as q where a.id_question = q.id_question AND a.id_owner = 1 AND q.id_meeting = 1")
print (cursor.fetchone())
cursor.close()
conn.close()

