from datetime import date
import pandas as pd
class FinanceManager:
 def __init__(self,db): self.db=db
 def add(self,day,kind,amount,category,note=''):
  if kind not in {'Income','Expense'} or amount<0 or not category.strip(): raise ValueError('Enter a valid transaction.')
  with self.db.connect() as c: c.execute('INSERT INTO transactions(entry_date,kind,amount,category,note) VALUES(?,?,?,?,?)',(day.isoformat(),kind,float(amount),category,note))
 def budget(self,month,amount):
  if len(month)!=7 or month[4]!='-' or amount<0: raise ValueError('Use YYYY-MM and a non-negative amount.')
  with self.db.connect() as c: c.execute('INSERT INTO budgets(month,amount) VALUES(?,?) ON CONFLICT(month) DO UPDATE SET amount=excluded.amount',(month,float(amount)))
 def get_budget(self,m):
  r=self.db.list_records('budgets','month=?',(m,)); return float(r[0]['amount']) if r else None
 def spent(self,m):
  with self.db.connect() as c: return float(c.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE kind='Expense' AND substr(entry_date,1,7)=?",(m,)).fetchone()[0])
 def monthly(self):
  with self.db.connect() as c: return pd.DataFrame([dict(r) for r in c.execute("SELECT substr(entry_date,1,7) month,SUM(CASE WHEN kind='Income' THEN amount ELSE 0 END) income,SUM(CASE WHEN kind='Expense' THEN amount ELSE 0 END) expenses FROM transactions GROUP BY month ORDER BY month")])
 def insights(self,day):
  m=day.strftime('%Y-%m'); spent=self.spent(m); b=self.get_budget(m); out=[f'Recorded spending this month: ₹{spent:,.0f}.']
  out.append('Set a monthly budget to compare spending.' if b is None else (f'₹{b-spent:,.0f} remains in your recorded budget.' if b>=spent else f'Spending is ₹{spent-b:,.0f} above budget.'))
  return out
 def import_csv(self,file):
  df=pd.read_csv(file); required={'entry_date','kind','amount','category'}
  if not required.issubset(df.columns): raise ValueError('Required CSV columns: entry_date, kind, amount, category')
  for _,r in df.iterrows(): self.add(date.fromisoformat(str(r.entry_date)[:10]),str(r.kind),float(r.amount),str(r.category),str(r.get('note','')))
  return len(df)
