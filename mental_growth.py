class MentalGrowthManager:
 def __init__(self,db): self.db=db
 def journal(self,day,kind,content):
  if not content.strip(): raise ValueError('Journal entry required.')
  with self.db.connect() as c: c.execute('INSERT INTO journal_entries(entry_date,entry_type,content) VALUES(?,?,?)',(day.isoformat(),kind,content.strip()))
 def delete(self,i):
  with self.db.connect() as c: c.execute('DELETE FROM journal_entries WHERE id=?',(int(i),))
 def mood(self,day,mood,gratitude):
  with self.db.connect() as c: c.execute('INSERT INTO mood_checkins(checkin_date,mood,gratitude) VALUES(?,?,?)',(day.isoformat(),mood,gratitude))
 def habit(self,name,day,done):
  with self.db.connect() as c: c.execute('INSERT INTO habit_logs(habit_date,habit_name,completed) VALUES(?,?,?)',(day.isoformat(),name,int(done)))
