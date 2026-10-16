import os
from dotenv import load_dotenv
class LifeCoachAI:
 def __init__(self,db): self.db=db; load_dotenv()
 def context(self):
  return {'pending_tasks':self.db.list_records('tasks',"status='Pending'",order_by='due_date',limit=20),'skills':self.db.list_records('skills'),'career_goals':self.db.list_records('career_goals'),'focus_sessions':self.db.list_records('focus_sessions',order_by='session_date DESC',limit=7),'transactions':self.db.list_records('transactions',order_by='entry_date DESC',limit=30)}
 def ask(self,prompt,language='English'):
  key=os.getenv('GEMINI_API_KEY','').strip()
  if not key: return self.fallback(language)
  try:
   from google import genai
   client=genai.Client(api_key=key); model=os.getenv('GEMINI_MODEL','gemini-2.5-flash')
   response=client.models.generate_content(model=model,contents=f"You are LifeLens AI. Respond in {language}. Use supplied data, don't invent stats. Give practical concise suggestions. Do not claim medical, financial, legal or professional advice. Data: {self.context()}\nQuestion: {prompt}")
   return response.text or self.fallback(language)
  except Exception as e: return self.fallback(language,str(e))
 def roadmap(self,role,context): return self.ask(f'Create an achievable 8-week learning roadmap for {role}, using current context {context}. Include weekly outcomes and portfolio ideas.')
 def reflection(self): return self.ask('Suggest five gentle optional weekly reflection questions. Do not diagnose mental health.')
 def fallback(self,language='English',error=None):
  tasks=self.db.list_records('tasks',"status='Pending'",order_by='due_date',limit=5)
  lines='\n'.join(f"- {t['title']} — {t['priority']}, due {t['due_date']}" for t in tasks) or 'No pending tasks are recorded.'
  if language=='Hindi': intro='Gemini उपलब्ध नहीं है; यह स्थानीय रिकॉर्ड पर आधारित सुझाव है।'; action='एक छोटा अगला कदम चुनें, 25 मिनट काम करें और प्रगति दर्ज करें।'
  elif language=='Hinglish': intro='Gemini configured nahi hai; yeh local records par based fallback hai.'; action='Ek chhota next step choose karo, 25-minute focus session karo, phir progress record karo.'
  else: intro='Gemini is not configured or unavailable; this fallback uses local records.'; action='Choose one small next action, work for 25 focused minutes, then record your progress.'
  return f'**{intro}**\n\n**Pending tasks**\n{lines}\n\n**Suggested next step**\n{action}'+(f'\n\nAPI detail: {error[:180]}' if error else '\n\nSet GEMINI_API_KEY in your local .env file to enable Gemini.')
