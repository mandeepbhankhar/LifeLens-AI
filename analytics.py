from datetime import timedelta
import pandas as pd
class AnalyticsManager:
 def __init__(self,db): self.db=db
 def snapshot(self,day):
  tasks=self.db.get_tasks_for_date(day); done=sum(t['status']=='Completed' for t in tasks); focus=self.db.get_focus_minutes(day); spent=self.db.get_expense_total(day); workout=self.db.has_workout(day)
  score=round((done/len(tasks)*50 if tasks else 0)+min(focus/120,1)*30+(20 if workout else 0))
  return {'done':done,'total':len(tasks),'focus':focus,'spent':spent,'workout':workout,'score':score}
 def week(self,day):
  rows=[]
  for n in range(6,-1,-1):
   d=day-timedelta(days=n); tasks=self.db.get_tasks_for_date(d)
   rows.append({'day':d.strftime('%a'),'tasks':sum(t['status']=='Completed' for t in tasks),'focus':self.db.get_focus_minutes(d)})
  return pd.DataFrame(rows)
 def insights(self,day):
  pending=self.db.list_records('tasks',"status='Pending' AND priority IN ('High','Urgent')")
  out=[f'{len(pending)} high-priority task(s) remain pending.' if pending else 'No pending high-priority tasks recorded.',f"Today's recorded focus time: {self.db.get_focus_minutes(day)} minutes."]
  budget=self.db.list_records('budgets','month=?',(day.strftime('%Y-%m'),)); spent=self.db.get_expense_total(day)
  out.append('Set a monthly budget and record transactions to see spending comparisons.' if not budget else f"Today's spending is ₹{spent:,.0f}; monthly spending is ₹{self.db.monthly_expense_total(day):,.0f}.")
  return out
 def period(self,start,end):
  rows=[]; d=start
  while d<=end:
   tasks=self.db.get_tasks_for_date(d); rows.append({'day':d.isoformat(),'tasks':sum(t['status']=='Completed' for t in tasks),'focus':self.db.get_focus_minutes(d),'workouts':sum(int(w['duration_minutes']) for w in self.db.list_records('workouts','workout_date=?',(d.isoformat(),))) }); d+=timedelta(days=1)
  df=pd.DataFrame(rows); expenses=self.db.execute("SELECT COALESCE(SUM(amount),0) n FROM transactions WHERE kind='Expense' AND entry_date BETWEEN ? AND ?",(start.isoformat(),end.isoformat()),True)[0]['n']
  return df,{'tasks':int(df.tasks.sum()),'focus':int(df.focus.sum()),'workouts':int(df.workouts.sum()),'expenses':float(expenses)}
