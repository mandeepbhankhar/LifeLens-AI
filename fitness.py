class WellnessManager:
 def __init__(self,db): self.db=db
 def workout(self,day,exercise,mins,note=''):
  if not exercise.strip() or int(mins)<0: raise ValueError('Enter an exercise and non-negative duration.')
  with self.db.connect() as c: c.execute('INSERT INTO workouts(workout_date,exercise_name,duration_minutes) VALUES(?,?,?)',(day.isoformat(),exercise,int(mins)))
 def daily(self,day,sleep,water,activity,note=''):
  if not 0<=sleep<=24 or not 0<=water<=20 or not 0<=activity<=1440: raise ValueError('Check wellness values.')
  with self.db.connect() as c: c.execute('INSERT INTO wellness_records(record_date,sleep_hours,water_litres,activity_minutes,note) VALUES(?,?,?,?,?) ON CONFLICT(record_date) DO UPDATE SET sleep_hours=excluded.sleep_hours,water_litres=excluded.water_litres,activity_minutes=excluded.activity_minutes,note=excluded.note',(day.isoformat(),sleep,water,activity,note))
