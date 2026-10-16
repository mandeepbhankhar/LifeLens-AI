from datetime import date,timedelta
import pandas as pd
class TaskManager:
 def __init__(self,db): self.db=db
 def create(self,title,desc,priority,due,category,tags=''):
  if not title.strip(): raise ValueError('Task title is required.')
  if priority not in {'Low','Medium','High','Urgent'}: raise ValueError('Invalid priority.')
  self.db.add_task(title,desc,priority,due,category)
  if tags:
   with self.db.connect() as c: c.execute('UPDATE tasks SET tags=? WHERE id=(SELECT MAX(id) FROM tasks)',(tags,))
 def list(self,status=None,priority=None,limit=None):
  rows=self.db.get_all_tasks()
  if status: rows=[r for r in rows if r['status']==status]
  if priority: rows=[r for r in rows if r['priority']==priority]
  return rows[:limit] if limit else rows
 def complete(self,i): self.db.set_task_status(i,'Completed')
 def delete(self,i): self.db.delete_task(i)
 def update(self,i,title,desc,priority,due,category,tags,status):
  if not title.strip(): raise ValueError('Title required.')
  with self.db.connect() as c: c.execute('UPDATE tasks SET title=?,description=?,priority=?,due_date=?,category=?,status=?,tags=?,completed_at=CASE WHEN ?="Completed" THEN CURRENT_TIMESTAMP ELSE NULL END WHERE id=?',(title,desc,priority,due.isoformat(),category,status,tags,status,int(i)))
 def overdue(self): return self.db.list_records('tasks',"status='Pending' AND due_date < ?",(date.today().isoformat(),),'due_date')
class ProductivityAnalyzer:
 def __init__(self,db): self.db=db
 def add(self,day,mins,note=''):
  if int(mins)<=0: raise ValueError('Minutes must be positive.')
  self.db.add_focus_session(day,int(mins),note)
 def week(self,day):
  out=[]
  for n in range(6,-1,-1):
   d=day-timedelta(days=n); ds=d.isoformat(); rows=self.db.get_tasks_for_date(d)
   out.append({'day':d.strftime('%a'),'tasks':sum(x['status']=='Completed' for x in rows),'focus':self.db.get_focus_minutes(d)})
  return pd.DataFrame(out)
