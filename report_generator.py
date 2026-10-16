from datetime import timedelta
import pandas as pd
class ReportGenerator:
 def __init__(self,db): self.db=db
 def summary(self,start,end):
  rows=[]; d=start
  while d<=end:
   rows.append({'date':d.isoformat(),'tasks_completed':sum(t['status']=='Completed' for t in self.db.get_tasks_for_date(d)),'focus_minutes':self.db.get_focus_minutes(d),'expenses_inr':self.db.get_expense_total(d)}); d+=timedelta(days=1)
  return pd.DataFrame(rows)
