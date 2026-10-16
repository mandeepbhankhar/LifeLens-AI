class CareerManager:
 def __init__(self,db): self.db=db
 def add_goal(self,title,day,details=''):
  if not title.strip(): raise ValueError('Goal title required.')
  with self.db.connect() as c: c.execute('INSERT INTO career_goals(title,target_date,details,progress_percent) VALUES(?,?,?,0)',(title,day.isoformat(),details))
 def progress(self,i,p):
  if not 0<=int(p)<=100: raise ValueError('Progress must be 0–100.')
  with self.db.connect() as c: c.execute('UPDATE career_goals SET progress_percent=? WHERE id=?',(int(p),int(i)))
 def skill(self,name,current,target):
  if not name.strip() or not 0<=current<=100 or not 0<=target<=100: raise ValueError('Skill name and levels 0–100 required.')
  with self.db.connect() as c: c.execute('INSERT INTO skills(name,current_level,target_level) VALUES(?,?,?) ON CONFLICT(name) DO UPDATE SET current_level=excluded.current_level,target_level=excluded.target_level',(name,int(current),int(target)))
 def context(self): return {'goals':self.db.list_records('career_goals'),'skills':self.db.list_records('skills'),'courses':self.db.list_records('courses')}
