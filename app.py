from datetime import date,datetime,timedelta
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from database.db_manager import DatabaseManager
from modules.productivity import TaskManager,ProductivityAnalyzer
from modules.finance import FinanceManager
from modules.career import CareerManager
from modules.fitness import WellnessManager
from modules.mental_growth import MentalGrowthManager
from modules.analytics import AnalyticsManager
from ai.life_coach import LifeCoachAI
from utils.report_generator import ReportGenerator
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
BASE=Path(__file__).parent; (BASE/'data').mkdir(exist_ok=True)
st.set_page_config(page_title='LifeLens AI',page_icon='🌱',layout='wide')

st.markdown("""
<style>
/* =====================================================
   LIFELENS AI — PROFESSIONAL UI THEME
   ===================================================== */

:root {
    color-scheme: light;
    --page: #f4f7fc;
    --surface: #ffffff;
    --text: #172033;
    --muted: #68758c;
    --border: #d9e2ef;
    --primary: #5145e5;
    --primary-hover: #4338ca;
    --navy: #0b1220;
    --navy-border: #1e2b40;
    --radius: 14px;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: var(--page) !important;
    color: var(--text) !important;
}

[data-testid="stHeader"] {
    background: rgba(244, 247, 252, 0.94) !important;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1500px;
    padding: 2rem 2rem 3rem;
}

/* ---------------- TEXT & TYPOGRAPHY ---------------- */

.stApp,
.stApp p,
.stApp li,
.stApp label,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] strong,
.stApp [data-testid="stWidgetLabel"],
.stApp [data-testid="stWidgetLabel"] p {
    color: var(--text);
}

.stApp [data-testid="stCaptionContainer"],
.stApp small {
    color: var(--muted) !important;
}

.pt {
    color: var(--text) !important;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.045em;
    line-height: 1.2;
}

.sub {
    color: var(--muted) !important;
    margin-top: 7px;
    font-size: 0.97rem;
}

/* ---------------- TEXT INPUTS ---------------- */

/* Keep fields white with readable text and a clean border. */
.stApp [data-baseweb="input"] > div,
.stApp [data-baseweb="textarea"] > div {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 9px !important;
    box-shadow: none !important;
    transition: border-color 0.18s ease,
                box-shadow 0.18s ease;
}

.stApp input,
.stApp textarea,
.stApp [data-baseweb="input"] input,
.stApp [data-baseweb="textarea"] textarea {
    background: transparent !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    caret-color: var(--primary) !important;
    font-size: 0.94rem;
}

/* Change only the border when the user focuses a field. */
.stApp [data-baseweb="input"] > div:focus-within,
.stApp [data-baseweb="textarea"] > div:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(81, 69, 229, 0.10) !important;
}

/* Text-area specific styling. */
.stApp textarea {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    border-radius: 8px !important;
    min-height: 100px;
    resize: vertical;
}

.stApp textarea:focus {
    outline: none !important;
    box-shadow: none !important;
}

/* Standalone inputs, including compatible Streamlit versions. */
.stApp input {
    border-color: transparent !important;
    outline: none !important;
    box-shadow: none !important;
}

.stApp input::placeholder,
.stApp textarea::placeholder {
    color: #8995a8 !important;
    -webkit-text-fill-color: #8995a8 !important;
    opacity: 1 !important;
}

/* ---------------- DROPDOWNS & DATE FIELDS ---------------- */

.stApp [data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 9px !important;
    box-shadow: none !important;
}

.stApp [data-baseweb="select"] > div:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(81, 69, 229, 0.10) !important;
}

.stApp [data-baseweb="select"] *,
.stApp [data-baseweb="popover"] *,
.stApp [role="listbox"] *,
.stApp [role="option"] {
    color: var(--text) !important;
}

.stApp [data-baseweb="popover"] {
    background: #ffffff !important;
}

/* ---------------- BUTTONS ---------------- */

.stApp button[kind="primary"],
.stApp [data-testid="stFormSubmitButton"] button {
    background: var(--primary) !important;
    color: #ffffff !important;
    border: 1px solid var(--primary) !important;
    border-radius: 9px !important;
    font-weight: 650 !important;
    transition: background 0.18s ease,
                transform 0.18s ease,
                box-shadow 0.18s ease;
}

.stApp button[kind="primary"] *,
.stApp [data-testid="stFormSubmitButton"] button * {
    color: #ffffff !important;
}

.stApp button[kind="primary"]:hover,
.stApp [data-testid="stFormSubmitButton"] button:hover {
    background: var(--primary-hover) !important;
    border-color: var(--primary-hover) !important;
    box-shadow: 0 4px 12px rgba(81, 69, 229, 0.18);
}

.stApp button[kind="secondary"] {
    background: #ffffff !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 9px !important;
}

/* ---------------- TABS ---------------- */

.stApp [data-testid="stTabs"] button[role="tab"] {
    color: #66738a !important;
    font-weight: 600 !important;
}

.stApp [data-testid="stTabs"] button[role="tab"] * {
    color: inherit !important;
}

.stApp [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: var(--primary) !important;
}

.stApp [data-testid="stTabs"] button[role="tab"][aria-selected="true"] * {
    color: var(--primary) !important;
}

/* ---------------- EXPANDERS & CONTAINERS ---------------- */

.stApp [data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e0e7f1 !important;
    border-radius: 12px !important;
    overflow: hidden;
}

.stApp [data-testid="stExpander"] summary,
.stApp [data-testid="stExpander"] summary * {
    color: var(--text) !important;
}

.stApp [data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border: 1px solid #e3e9f3 !important;
    border-radius: 15px !important;
    padding: 15px !important;
    box-shadow: 0 4px 16px rgba(26, 42, 72, 0.035);
}

/* ---------------- METRIC CARDS ---------------- */

.stApp [data-testid="stMetric"] {
    background: linear-gradient(145deg, #ffffff, #fbfcff) !important;
    border: 1px solid #e2e8f2 !important;
    border-radius: 15px !important;
    padding: 17px 18px !important;
    min-height: 108px;
    box-shadow: 0 5px 18px rgba(26, 42, 72, 0.045);
    transition: transform 0.18s ease,
                box-shadow 0.18s ease;
}

.stApp [data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(26, 42, 72, 0.075);
}

.stApp [data-testid="stMetricLabel"] {
    color: #66738a !important;
    font-size: 0.84rem !important;
}

.stApp [data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-size: 1.75rem !important;
    font-weight: 780 !important;
    letter-spacing: -0.04em;
}

.stApp [data-testid="stMetricDelta"] {
    font-size: 0.82rem !important;
}

/* ---------------- TABLES ---------------- */

.stApp [data-testid="stDataFrame"] {
    border: 1px solid #e0e7f1 !important;
    border-radius: 12px !important;
    overflow: hidden;
    background: #ffffff !important;
}

/* ---------------- SIDEBAR ---------------- */

[data-testid="stSidebar"] {
    background: var(--navy) !important;
    border-right: 1px solid var(--navy-border) !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #e8eef9 !important;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #9eacc2 !important;
}

/* Sidebar navigation labels. */
[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 7px 10px;
    border-radius: 9px;
    transition: background 0.15s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #172338 !important;
}

/* Keep sidebar inputs readable if any are added later. */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea {
    background: #ffffff !important;
    color: var(--text) !important;
}

/* Branding classes already used by app.py. */
.brand {
    font-size: 1.55rem;
    font-weight: 850;
    letter-spacing: -0.035em;
    color: #ffffff !important;
}

.tagline {
    font-size: 0.78rem;
    color: #aab8cf !important;
    margin-top: 4px;
}

/* ---------------- AI INSIGHTS ---------------- */

.insight {
    background: #f6f5ff;
    border-left: 3px solid #7463f0;
    padding: 12px 13px;
    border-radius: 8px;
    margin: 9px 0;
    color: #28334a !important;
    line-height: 1.55;
}

/* ---------------- RESPONSIVE LAYOUT ---------------- */

@media (max-width: 850px) {
    [data-testid="stMainBlockContainer"] {
        padding: 1rem 0.8rem 2rem;
    }

    .pt {
        font-size: 1.65rem;
    }

    .stApp [data-testid="stMetric"] {
        padding: 12px !important;
        min-height: 95px;
    }

    .stApp [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
    }
}


/* ===== LIFELENS AI: INPUT BORDER FIX ===== */

/* Text input: Task title, Tags, and other text fields */
.stApp div[data-testid="stTextInput"] input {
    border: 1.5px solid #B8C5D9 !important;
    border-radius: 9px !important;
    background: #FFFFFF !important;
    color: #172033 !important;
    box-shadow: none !important;
    box-sizing: border-box !important;
}

/* Description: visible border on the textarea itself */
.stApp div[data-testid="stTextArea"] textarea {
    border: 1.5px solid #B8C5D9 !important;
    border-radius: 9px !important;
    background: #FFFFFF !important;
    color: #172033 !important;
    box-shadow: none !important;
    outline: none !important;
    box-sizing: border-box !important;
}

/* Focus: purple border for text input */
.stApp div[data-testid="stTextInput"] input:focus {
    border-color: #5145E5 !important;
    box-shadow: 0 0 0 2px rgba(81, 69, 229, 0.12) !important;
}

/* Focus: purple border for Description */
.stApp div[data-testid="stTextArea"] textarea:focus {
    border-color: #5145E5 !important;
    box-shadow: 0 0 0 2px rgba(81, 69, 229, 0.12) !important;
}

/* Keep text readable */
.stApp div[data-testid="stTextInput"] input,
.stApp div[data-testid="stTextArea"] textarea {
    -webkit-text-fill-color: #172033 !important;
    caret-color: #5145E5 !important;
}

</style>
""", unsafe_allow_html=True)

db=DatabaseManager(BASE/'data'/'lifelens.db'); db.initialize(); db.seed_demo_data_if_empty()
tasks=TaskManager(db); prod=ProductivityAnalyzer(db); finance=FinanceManager(db); career=CareerManager(db); wellness=WellnessManager(db); growth=MentalGrowthManager(db); analytics=AnalyticsManager(db); coach=LifeCoachAI(db); reports=ReportGenerator(db); today=date.today()
def heading(t,s=''):
 st.markdown(f'<div class="pt">{t}</div>',unsafe_allow_html=True)
 if s: st.markdown(f'<div class="sub">{s}</div>',unsafe_allow_html=True)
def table(rows,empty='Nothing recorded yet.'):
 if rows: st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
 else: st.info(empty)
def csv(rows,name):
 if rows: st.download_button('Download CSV',pd.DataFrame(rows).to_csv(index=False).encode('utf-8-sig'),file_name=name,mime='text/csv')
def bar(df,x,y,title,color='#536dfe'):
 if df.empty: st.info('Add records to see this chart.'); return
 fig,ax=plt.subplots(figsize=(8,3)); ax.bar(df[x].astype(str),df[y],color=color); ax.set_title(title,loc='left'); ax.grid(axis='y',alpha=.2); ax.set_axisbelow(True); ax.spines[['top','right','left']].set_visible(False); fig.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close(fig)
pages=['Dashboard','Productivity','Career','Finance','Fitness','Mental Growth','AI Life Coach','Analytics','Settings']
with st.sidebar:
 st.markdown('<div class="brand">🌱 LifeLens AI</div><div class="tagline">Your Life. Your Goals. Your Growth.</div>',unsafe_allow_html=True); st.divider(); page=st.radio('NAVIGATION',pages); st.divider(); st.caption('Local-first · SQLite storage')
name=db.get_setting('user_name','Alex')
if page=='Dashboard':
 greeting='Good morning' if datetime.now().hour<12 else ('Good afternoon' if datetime.now().hour<17 else 'Good evening'); a,b=st.columns([4,1])
 with a: heading(f'{greeting}, {name}! 👋',"Here's your personal growth overview for today.")
 with b: st.markdown(f'<div style="text-align:right;padding-top:12px;color:#697386">{today:%A, %d %b %Y}</div>',unsafe_allow_html=True)
 s=analytics.snapshot(today); cols=st.columns(5)
 for c,(lab,val) in zip(cols,[('☑ Tasks Completed',f"{s['done']}/{s['total']}"),('◷ Focus Time',f"{s['focus']} min"),('₹ Money Spent',f"₹{s['spent']:,.0f}"),('♧ Workout Status','Done' if s['workout'] else 'Not yet'),('✦ Growth Score',f"{s['score']}%")]): c.metric(lab,val)
 left,right=st.columns([1.7,1])
 with left:
  with st.container(border=True):
   st.markdown('**Weekly Progress**'); w=prod.week(today); fig,ax=plt.subplots(figsize=(8,3)); x=range(len(w)); ax.bar([i-.18 for i in x],w.tasks,.36,label='Tasks',color='#536dfe'); ax.bar([i+.18 for i in x],w.focus,.36,label='Focus minutes',color='#8b5cf6'); ax.set_xticks(list(x),w.day); ax.grid(axis='y',alpha=.2); ax.set_axisbelow(True); ax.spines[['top','right','left']].set_visible(False); ax.legend(frameon=False,ncols=2); fig.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close(fig)
 with right:
  with st.container(border=True):
   st.markdown('**💡 AI Life Insights**')
   for i in analytics.insights(today): st.markdown(f'<div class="insight">{i}</div>',unsafe_allow_html=True)
   st.caption('Data-based observations, not AI-generated recommendations.')
 a,b=st.columns(2)
 with a:
  with st.container(border=True):
   st.markdown("**Today's Schedule**")
   for r in db.list_records('schedule_items','schedule_date=?',(today.isoformat(),),'schedule_time'): st.write(f"**{r['schedule_time']}** · {r['title']} — {r['category']}")
   with st.expander('Add schedule item'):
    with st.form('qs'):
     title=st.text_input('Activity'); tm=st.time_input('Time'); cat=st.selectbox('Category',['Work','Learning','Break','Personal'])
     if st.form_submit_button('Save'):
      if title.strip(): db.insert_record('schedule_items',{'schedule_date':today.isoformat(),'schedule_time':tm.strftime('%H:%M'),'title':title.strip(),'category':cat}); st.rerun()
      else: st.error('Activity required.')
 with b:
  with st.container(border=True):
   st.markdown('**Priority Tasks**')
   for r in tasks.list(status='Pending',limit=5):
    if st.checkbox(f"{r['title']} · {r['priority']} · {r['due_date']}",key=f"dash{r['id']}"): tasks.complete(r['id']); st.rerun()
elif page=='Productivity':
 heading('Productivity','Tasks, focus sessions, deadlines, schedule and daily goals.'); tabs=st.tabs(['Tasks','Focus sessions','Schedule','Goals'])
 with tabs[0]:
  with st.expander('＋ Add task',expanded=True):
   with st.form('taskadd',clear_on_submit=True):
    title=st.text_input('Task title *'); desc=st.text_area('Description'); a,b,c=st.columns(3); priority=a.selectbox('Priority',['Low','Medium','High','Urgent'],index=1); due=b.date_input('Due date',today); cat=c.selectbox('Category',['Work','Learning','Personal','Health','Finance','General']); tags=st.text_input('Tags')
    if st.form_submit_button('Create task'):
     try: tasks.create(title,desc,priority,due,cat,tags); st.success('Created.'); st.rerun()
     except Exception as e: st.error(str(e))
  a,b,c=st.columns(3); sf=a.selectbox('Status',['All','Pending','Completed']); pf=b.selectbox('Priority',['All','Low','Medium','High','Urgent']); filt=c.selectbox('Due date',['All','Today','Overdue','Next 7 days']); rows=tasks.list(None if sf=='All' else sf,None if pf=='All' else pf)
  if filt=='Today': rows=[r for r in rows if r['due_date']==today.isoformat()]
  elif filt=='Overdue': rows=[r for r in rows if r['due_date']<today.isoformat() and r['status']=='Pending']
  elif filt=='Next 7 days': rows=[r for r in rows if today.isoformat()<=r['due_date']<=(today+timedelta(days=7)).isoformat()]
  table(rows,'No tasks match these filters.'); csv(rows,'tasks.csv')
  if rows:
   with st.expander('Edit / complete / delete task'):
    chosen=st.selectbox('Select task',rows,format_func=lambda r:f"{r['id']} · {r['title']}")
    with st.form('edit_task'):
     title=st.text_input('Title',chosen['title']); desc=st.text_area('Description',chosen.get('description','') or ''); pri=st.selectbox('Priority',['Low','Medium','High','Urgent'],index=['Low','Medium','High','Urgent'].index(chosen['priority'])); due=st.date_input('Due date',date.fromisoformat(chosen['due_date'])); cat=st.text_input('Category',chosen['category']); tags=st.text_input('Tags',chosen.get('tags','') or ''); status=st.selectbox('Status',['Pending','Completed'],index=0 if chosen['status']=='Pending' else 1)
     if st.form_submit_button('Save changes'): tasks.update(chosen['id'],title,desc,pri,due,cat,tags,status); st.rerun()
    if st.button('Delete task'): tasks.delete(chosen['id']); st.rerun()
  overdue=tasks.overdue()
  if overdue: st.warning(f"{len(overdue)} overdue task(s): "+', '.join(r['title'] for r in overdue[:5]))
 with tabs[1]:
  with st.form('focus'):
   day=st.date_input('Session date',today); mins=st.number_input('Focus minutes',1,240,25); note=st.text_input('Note','Pomodoro')
   if st.form_submit_button('Save session'):
    try: prod.add(day,mins,note); st.rerun()
    except Exception as e: st.error(str(e))
  table(db.list_records('focus_sessions',order_by='session_date DESC,id DESC',limit=100)); st.caption('Records completed focus sessions; use any timer separately.')
 with tabs[2]:
  with st.form('schedule'):
   day=st.date_input('Date',today,key='sd'); tm=st.time_input('Time'); title=st.text_input('Activity'); cat=st.selectbox('Category',['Work','Learning','Break','Personal'])
   if st.form_submit_button('Add schedule'):
    if title.strip(): db.insert_record('schedule_items',{'schedule_date':day.isoformat(),'schedule_time':tm.strftime('%H:%M'),'title':title.strip(),'category':cat}); st.rerun()
    else: st.error('Activity required.')
  table(db.list_records('schedule_items',order_by='schedule_date DESC,schedule_time'))
 with tabs[3]:
  with st.form('goals'):
   day=st.date_input('Goal date',today,key='gd'); target=st.number_input('Tasks target',1,50,3); focus=st.number_input('Focus target minutes',15,600,120)
   if st.form_submit_button('Save goal'): db.upsert_record('daily_goals',{'goal_date':day.isoformat(),'tasks_target':int(target),'focus_target_minutes':int(focus)},['goal_date']); st.success('Saved.')
  table(db.list_records('daily_goals',order_by='goal_date DESC'))
elif page=='Career':
 heading('Career Development','Career goals, skill inventory, courses, portfolio and applications.'); tabs=st.tabs(['Goals','Skills','Courses','Portfolio','Applications','AI Roadmap'])
 with tabs[0]:
  with st.form('cg'):
   title=st.text_input('Career goal'); due=st.date_input('Target date',today+timedelta(days=90)); details=st.text_area('Milestones')
   if st.form_submit_button('Add goal'):
    try: career.add_goal(title,due,details); st.rerun()
    except Exception as e: st.error(str(e))
  rows=db.list_records('career_goals',order_by='target_date'); table(rows)
  if rows:
   r=st.selectbox('Goal progress',rows,format_func=lambda x:f"{x['id']} · {x['title']}"); p=st.slider('Progress %',0,100,int(r['progress_percent']))
   if st.button('Save progress'): career.progress(r['id'],p); st.rerun()
 with tabs[1]:
  with st.form('skill'):
   n=st.text_input('Skill'); cur=st.slider('Current proficiency',0,100,20); target=st.slider('Target proficiency',0,100,80)
   if st.form_submit_button('Save skill'):
    try: career.skill(n,cur,target); st.rerun()
    except Exception as e: st.error(str(e))
  rows=db.list_records('skills',order_by='name'); table(rows)
  if rows:
   fig,ax=plt.subplots(figsize=(7,3)); ax.bar([r['name'] for r in rows],[r['current_level'] for r in rows],color='#8b5cf6'); ax.set_ylabel('Level (%)'); ax.set_ylim(0,100); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
 with tabs[2]:
  with st.form('course'):
   n=st.text_input('Course / certification'); provider=st.text_input('Provider'); status=st.selectbox('Status',['Planned','In progress','Completed']); hours=st.number_input('Learning hours',0.0,10000.0,0.0)
   if st.form_submit_button('Save course'):
    if n.strip(): db.insert_record('courses',{'name':n,'provider':provider,'status':status,'learning_hours':hours}); st.rerun()
    else: st.error('Name required.')
  table(db.list_records('courses'))
 with tabs[3]:
  with st.form('portfolio'):
   n=st.text_input('Project name'); url=st.text_input('Project URL'); desc=st.text_area('Description')
   if st.form_submit_button('Save project'):
    if n.strip(): db.insert_record('portfolio_projects',{'name':n,'url':url,'description':desc}); st.rerun()
    else: st.error('Name required.')
  table(db.list_records('portfolio_projects'))
 with tabs[4]:
  with st.form('job'):
   company=st.text_input('Company'); role=st.text_input('Role'); day=st.date_input('Applied date',today); status=st.selectbox('Status',['Saved','Applied','Interview','Offer','Rejected']); note=st.text_input('Notes')
   if st.form_submit_button('Save application'):
    if company.strip() and role.strip(): db.insert_record('job_applications',{'company':company,'role':role,'applied_date':day.isoformat(),'status':status,'notes':note}); st.rerun()
    else: st.error('Company and role required.')
  table(db.list_records('job_applications',order_by='applied_date DESC'))
 with tabs[5]:
  role=st.text_input('Target role','Python backend developer')
  if st.button('Generate learning roadmap'): st.session_state['roadmap']=coach.roadmap(role,career.context())
  if st.session_state.get('roadmap'): st.markdown(st.session_state['roadmap'])
elif page=='Finance':
 heading('Personal Finance','Income, expenses, budgets and savings in Indian rupees.'); tabs=st.tabs(['Transactions','Budget','Savings','Insights'])
 with tabs[0]:
  with st.form('transaction'):
   a,b,c=st.columns(3); kind=a.selectbox('Type',['Expense','Income']); amount=b.number_input('Amount ₹',0.0,100000000.0,100.0,step=50.0); day=c.date_input('Date',today); cat=st.selectbox('Category',['Food','Transport','Housing','Bills','Education','Health','Shopping','Salary','Freelance','Savings','Other']); note=st.text_input('Note')
   if st.form_submit_button('Add transaction'):
    try: finance.add(day,kind,amount,cat,note); st.rerun()
    except Exception as e: st.error(str(e))
  rows=db.list_records('transactions',order_by='entry_date DESC,id DESC'); table(rows); csv(rows,'transactions.csv')
  if rows:
   df=pd.DataFrame(rows); exp=df[df.kind=='Expense'].groupby('category',as_index=False).amount.sum(); bar(exp,'category','amount','Expenses by category','#f59e0b'); monthly=finance.monthly()
   if not monthly.empty:
    fig,ax=plt.subplots(figsize=(8,3)); x=range(len(monthly)); ax.bar([i-.18 for i in x],monthly.income,.36,label='Income',color='#22a06b'); ax.bar([i+.18 for i in x],monthly.expenses,.36,label='Expenses',color='#f59e0b'); ax.set_xticks(list(x),monthly.month); ax.legend(frameon=False); ax.set_title('Monthly income vs expenses'); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
  with st.expander('Import transactions from CSV'):
   up=st.file_uploader('CSV columns: entry_date, kind, amount, category, optional note',type=['csv'])
   if up and st.button('Import CSV'):
    try: st.success(f'Imported {finance.import_csv(up)} rows.'); st.rerun()
    except Exception as e: st.error(f'Import failed: {e}')
 with tabs[1]:
  with st.form('budget'):
   month=st.text_input('Month YYYY-MM',today.strftime('%Y-%m')); limit=st.number_input('Monthly budget ₹',0.0,100000000.0,10000.0)
   if st.form_submit_button('Save budget'):
    try: finance.budget(month,limit); st.rerun()
    except Exception as e: st.error(str(e))
  table(db.list_records('budgets',order_by='month DESC')); b=finance.get_budget(today.strftime('%Y-%m')); spent=finance.spent(today.strftime('%Y-%m'))
  if b is not None: st.metric('Budget remaining',f'₹{b-spent:,.0f}',f'Spent ₹{spent:,.0f} / ₹{b:,.0f}'); st.progress(min(1,spent/b) if b else 0)
 with tabs[2]:
  with st.form('savings'):
   n=st.text_input('Savings goal'); target=st.number_input('Target ₹',1.0,100000000.0,5000.0); saved=st.number_input('Saved so far ₹',0.0,100000000.0,0.0)
   if st.form_submit_button('Save goal'):
    if n.strip(): db.insert_record('savings_goals',{'name':n,'target_amount':target,'saved_amount':saved}); st.rerun()
    else: st.error('Name required.')
  rows=db.list_records('savings_goals'); table(rows)
  for r in rows: st.write(f"{r['name']}: ₹{r['saved_amount']:,.0f} / ₹{r['target_amount']:,.0f}"); st.progress(min(1,r['saved_amount']/r['target_amount']))
 with tabs[3]:
  for x in finance.insights(today): st.info(x)
  st.caption('Educational tracking only, not professional financial advice.')
elif page=='Fitness':
 heading('Fitness & Wellness','Track workouts, sleep, water and activity.'); tabs=st.tabs(['Workout log','Daily wellness','Goals'])
 with tabs[0]:
  with st.form('workout'):
   day=st.date_input('Workout date',today); exercise=st.text_input('Exercise'); mins=st.number_input('Duration minutes',0,1440,30); note=st.text_input('Notes')
   if st.form_submit_button('Save workout'):
    try: wellness.workout(day,exercise,mins,note); st.rerun()
    except Exception as e: st.error(str(e))
  rows=db.list_records('workouts',order_by='workout_date DESC,id DESC'); table(rows); csv(rows,'workouts.csv')
  if rows: bar(pd.DataFrame(rows).groupby('workout_date',as_index=False).duration_minutes.sum(),'workout_date','duration_minutes','Workout minutes by day','#22a06b')
 with tabs[1]:
  with st.form('wellness'):
   day=st.date_input('Date',today,key='wellnessday'); sleep=st.number_input('Sleep hours',0.0,24.0,7.0,.25); water=st.number_input('Water litres',0.0,20.0,2.0,.25); activity=st.number_input('Activity minutes',0,1440,20); note=st.text_area('Private wellness note')
   if st.form_submit_button('Save wellness record'):
    try: wellness.daily(day,sleep,water,activity,note); st.rerun()
    except Exception as e: st.error(str(e))
  table(db.list_records('wellness_records',order_by='record_date DESC')); st.caption('Personal tracking only; no diagnosis or medical advice.')
 with tabs[2]:
  with st.form('wellgoals'):
   workouts=st.number_input('Weekly workout target',0,21,3); water=st.number_input('Daily water goal litres',0.0,20.0,2.0); sleep=st.number_input('Sleep target hours',0.0,24.0,8.0)
   if st.form_submit_button('Save goals'): db.set_setting('weekly_workout_target',workouts); db.set_setting('daily_water_target',water); db.set_setting('sleep_target',sleep); st.success('Saved.')
elif page=='Mental Growth':
 heading('Mental Growth','Journal, gratitude, mood check-ins, and habits.'); tabs=st.tabs(['Journal','Mood & gratitude','Habits','Reflection'])
 with tabs[0]:
  with st.form('journal'):
   day=st.date_input('Date',today); kind=st.selectbox('Entry type',['Reflection','Gratitude','Win','Challenge','Other']); content=st.text_area('Journal entry')
   if st.form_submit_button('Save journal'):
    try: growth.journal(day,kind,content); st.rerun()
    except Exception as e: st.error(str(e))
  rows=db.list_records('journal_entries',order_by='entry_date DESC,id DESC')
  for r in rows:
   with st.expander(f"{r['entry_date']} · {r['entry_type']}"):
    st.write(r['content'])
    if st.button('Delete entry',key=f"del{r['id']}"): growth.delete(r['id']); st.rerun()
  csv(rows,'journal.csv')
 with tabs[1]:
  with st.form('mood'):
   day=st.date_input('Check-in date',today,key='moodday'); mood=st.select_slider('Mood',['Very low','Low','Okay','Good','Great'],value='Okay'); gratitude=st.text_area('One thing you are grateful for')
   if st.form_submit_button('Save check-in'): growth.mood(day,mood,gratitude); st.rerun()
  table(db.list_records('mood_checkins',order_by='checkin_date DESC'))
 with tabs[2]:
  with st.form('habit'):
   n=st.text_input('Habit name'); day=st.date_input('Date',today,key='habitday'); done=st.checkbox('Completed')
   if st.form_submit_button('Record habit'):
    if n.strip(): growth.habit(n,day,done); st.rerun()
    else: st.error('Habit name required.')
  rows=db.list_records('habit_logs',order_by='habit_date DESC'); table(rows); csv(rows,'habits.csv')
 with tabs[3]:
  st.markdown('- What went well this week, and why?\n- What drained your energy?\n- What did you learn?\n- What is one small adjustment for next week?')
  if st.button('Generate AI reflection prompts'): st.session_state['reflection']=coach.reflection()
  if st.session_state.get('reflection'): st.markdown(st.session_state['reflection'])
elif page=='AI Life Coach':
 heading('AI Life Coach','Personalized help based on your recorded data.'); language=st.selectbox('Response language',['English','Hindi','Hinglish']); prompt=st.text_area('Ask a question',placeholder='Help me prioritize today’s work.')
 if st.button('Ask LifeLens AI',type='primary'):
  if prompt.strip():
   with st.spinner('Preparing response...'): st.session_state['answer']=coach.ask(prompt,language)
  else: st.warning('Enter a question.')
 a,b=st.columns(2)
 with a:
  if st.button('Analyze productivity'): st.session_state['answer']=coach.ask('Analyze productivity and suggest three practical improvements.',language)
 with b:
  if st.button('Plan my day'): st.session_state['answer']=coach.ask('Create a realistic schedule using pending tasks.',language)
 if st.session_state.get('answer'): st.markdown(st.session_state['answer'])
 st.caption('Informational only; not medical, financial, legal, or professional advice.')
elif page=='Analytics':
 heading('Analytics','Choose a period and export your report.'); period=st.selectbox('Period',['7 days','30 days','90 days']); start=today-timedelta(days=int(period.split()[0])-1); df,s=analytics.period(start,today); cols=st.columns(4)
 for c,(l,v) in zip(cols,[('Tasks completed',s['tasks']),('Focus minutes',s['focus']),('Expenses',f"₹{s['expenses']:,.0f}"),('Workout minutes',s['workouts'])]): c.metric(l,v)
 bar(df,'day','tasks','Tasks completed by day'); bar(df,'day','focus','Focus time by day','#8b5cf6'); bar(df,'day','workouts','Workout minutes by day','#22a06b')
 st.markdown('**Growth score formula:** 50% task completion rate + 30% focus target attainment (target 120 minutes, capped at 100%) + 20% if a workout is recorded. This is a personal indicator, not a scientifically validated score.')
 st.download_button('Download analytics CSV',reports.summary(start,today).to_csv(index=False).encode('utf-8-sig'),file_name='lifelens_analytics.csv',mime='text/csv')
else:
 heading('Settings','Profile, local backup and API setup.')
 with st.form('profile'):
  new=st.text_input('Display name',name)
  if st.form_submit_button('Save profile'):
   if new.strip(): db.set_setting('user_name',new.strip()); st.rerun()
   else: st.error('Name cannot be empty.')
 st.write('Copy `.env.example` to `.env`, then set `GEMINI_API_KEY` and optionally `GEMINI_MODEL`. Never commit `.env`.')
 st.download_button('Download SQLite backup',db.export_database_bytes(),file_name='lifelens_backup.sqlite',mime='application/octet-stream')
 st.warning('College/portfolio project; not production-security reviewed. Protect your local account and backup files.')
