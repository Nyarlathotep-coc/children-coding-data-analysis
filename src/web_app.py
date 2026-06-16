import sys, os, json, io, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, render_template, jsonify, session
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'coding_data_analysis_2026'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# ==================== 缓存 ====================
_cache = {'data': {}, 'cleaned': {}, 'features': {}, 'analysis': {}}

# ==================== 1. 获取数据 ====================
def generate_all_data():
    np.random.seed(42); random.seed(42)
    first = ['子涵','梓涵','一诺','浩宇','欣怡','子轩','思远','雨桐','明哲','嘉琪','天佑','诗涵','俊杰','雅琪','致远','思琪','宇航','艺涵','博文','雨萱','昊然','若曦','鹏飞','子墨','宇轩','悦然','文博','梓萱','皓轩']
    last = ['王','李','张','刘','陈','杨','赵','黄','周','吴','徐','孙','马','朱','胡','郭','何','高','林','罗','郑','梁','谢','宋','唐','韩','冯','董','程','曹']
    students = []
    for i in range(1, 201):
        s = {'student_id': f'S{str(i).zfill(4)}', 'name': random.choice(last)+random.choice(first), 'age': random.choice([7,8,9,10,11,12,13,14,15,16]), 'gender': random.choice(['男','女'])}
        s['grade'] = max(1, s['age']-5)
        if i % 50 == 0: s['grade'] = f"{s['grade']}年级"
        if i % 100 == 0: s['age'] = 3
        d = datetime(2025,9,1)+timedelta(days=random.randint(0,180))
        s['enrollment_date'] = d.strftime('%Y/%m/%d') if i%80==0 else d.strftime('%Y-%m-%d')
        s['course_level'] = random.choice(['入门','初级','中级','高级','竞赛'])
        if s['age'] <= 8 and random.random() < 0.05: s['course_level'] = '高级'
        s['parent_phone'] = f'1{random.choice([38,39,50,58,86,88,35,59])}{random.randint(10000000,99999999)}'
        if i % 70 == 0: s['parent_phone'] = f'1{random.randint(100000000,999999999)}'
        students.append(s)
    df_stu = pd.DataFrame(students)
    df_stu = pd.concat([df_stu, df_stu.iloc[[0]].copy()], ignore_index=True)
    for col in ['age','gender','grade','course_level']:
        for idx in random.sample(range(len(df_stu)), 3):
            df_stu.loc[idx, col] = np.nan
    df_stu.to_csv(os.path.join(DATA_DIR, 'students.csv'), index=False, encoding='utf-8-sig')

    courses = pd.DataFrame([
        ('SCR001','Scratch趣味编程入门','图形化编程','入门',8,16),('SCR002','Scratch动画制作','图形化编程','初级',6,12),
        ('SCR003','Scratch游戏设计','图形化编程','初级',8,16),('SCR004','Scratch高级项目','图形化编程','中级',8,16),
        ('PYT001','Python编程基础','代码编程','初级',10,20),('PYT002','Python数据结构入门','代码编程','中级',8,16),
        ('PYT003','Python游戏开发','代码编程','中级',10,20),('PYT004','Python数据分析入门','代码编程','高级',8,16),
        ('PYT005','Python人工智能基础','代码编程','高级',10,20),('PYT006','Python网络爬虫','代码编程','高级',6,12),
        ('EVT001','EV3机器人基础','机器人编程','初级',8,16),('EVT002','EV3机器人进阶','机器人编程','中级',8,16),
        ('EVT003','VEX机器人竞赛','机器人编程','竞赛',12,24),('WEB001','HTML/CSS网页设计','代码编程','初级',6,12),
        ('WEB002','JavaScript编程基础','代码编程','中级',8,16),('APP001','App Inventor手机编程','图形化编程','初级',6,12),
        ('APP002','App Inventor高级应用','图形化编程','中级',8,16),('CPP001','C++编程基础','代码编程','中级',10,20),
        ('CPP002','C++算法入门','代码编程','高级',10,20),('CPP003','信息学竞赛集训','代码编程','竞赛',12,24),
    ], columns=['course_id','course_name','category','difficulty','duration_weeks','lessons_count'])
    courses.to_csv(os.path.join(DATA_DIR, 'courses.csv'), index=False, encoding='utf-8-sig')

    np.random.seed(42); random.seed(42)
    sids = df_stu['student_id'].dropna().tolist()
    cids = courses['course_id'].tolist()
    cl = {r['course_id']: list(range(1,r['lessons_count']+1)) for _,r in courses.iterrows()}
    sd, ed = datetime(2025,9,10), datetime(2026,6,1)
    recs = []
    for i in range(1, 1201):
        r = {'record_id': f'LR{str(i).zfill(5)}', 'student_id': random.choice(sids), 'course_id': random.choice(cids), 'lesson_id': random.choice(cl[random.choice(cids)])}
        d = sd+timedelta(days=random.randint(0,(ed-sd).days))
        if d.weekday() < 5 and random.random()<0.4: d += timedelta(days=(5-d.weekday()))
        r['lesson_date'] = d.strftime('%Y-%m-%d')
        r['duration_minutes'] = random.choice([300,480,600]) if i%75==0 else random.choice([15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90])
        r['completion_status'] = np.random.choice(['已完成','未完成','进行中'], p=[0.7,0.2,0.1])
        r['score'] = np.nan if r['completion_status']!='已完成' else (random.choice([105,110,120]) if i%60==0 else max(0,min(100,int(np.random.normal(75,15)))))
        r['code_lines'] = -5 if i%90==0 else max(0,int(np.random.poisson(30)))
        r['error_count'] = np.nan if i%55==0 else max(0,int(np.random.exponential(3)))
        recs.append(r)
    df_rec = pd.DataFrame(recs)
    for _ in range(5): df_rec = pd.concat([df_rec, df_rec.sample(1)], ignore_index=True)
    df_rec.to_csv(os.path.join(DATA_DIR, 'learning_records.csv'), index=False, encoding='utf-8-sig')

    np.random.seed(42); random.seed(42)
    atypes = ['选择题','填空题','编程题','项目作品','思维导图']
    sd2, ed2 = datetime(2025,9,15), datetime(2026,6,10)
    asgn = []
    np.random.seed(42); random.seed(42)
    atd = []
    for i in range(1, 1001):
        d0 = sd2+timedelta(days=random.randint(0,280))
        d0 += timedelta(days=(5-d0.weekday())%7)
        if d0.weekday()==6: d0 += timedelta(days=1)
        present = np.random.choice([True,False], p=[0.85,0.15])
        atd.append({'attendance_id':f'AT{str(i).zfill(4)}','student_id':random.choice(sids),'course_id':random.choice(cids),'class_date':d0.strftime('%Y-%m-%d'),'is_present':present,'late_minutes':np.nan if not present else (120 if i%100==0 else max(0,int(np.random.exponential(5))))})
    df_atd = pd.DataFrame(atd)
    df_atd['is_present'] = df_atd['is_present'].astype('object')
    for idx in random.sample(range(len(df_atd)),5): df_atd.loc[idx,'is_present'] = np.nan
    df_atd.to_csv(os.path.join(DATA_DIR,'attendance.csv'), index=False, encoding='utf-8-sig')

    for i in range(1, 801):
        a = {'assignment_id': f'AS{str(i).zfill(4)}', 'student_id': random.choice(sids), 'course_id': random.choice(cids)}
        d = sd2+timedelta(days=random.randint(0,(ed2-sd2).days))
        a['submit_date'] = d.strftime('%m/%d/%Y') if i%65==0 else d.strftime('%Y-%m-%d')
        a['assignment_type'] = random.choice(atypes)
        bs = np.random.normal({'选择题':80,'填空题':70,'编程题':65,'项目作品':78,'思维导图':75}[a['assignment_type']], {'选择题':10,'填空题':15,'编程题':20,'项目作品':12,'思维导图':10}[a['assignment_type']])
        a['score'] = -10 if i%80==0 else max(0,min(100,int(bs)))
        a['time_spent_minutes'] = random.choice([10,15,20,25,30,35,40,45,50,55,60,70,80,90,100,120])
        a['attempt_count'] = np.random.choice([1,2,3,4,5], p=[0.6,0.2,0.1,0.05,0.05])
        a['submission_status'] = np.random.choice(['已提交','未提交','迟交','需重做'], p=[0.7,0.1,0.12,0.08])
        asgn.append(a)
    df_asgn = pd.DataFrame(asgn)
    df_asgn.to_csv(os.path.join(DATA_DIR, 'assignments.csv'), index=False, encoding='utf-8-sig')

    return {
        'students': len(df_stu), 'courses': len(courses), 'records': len(df_rec),
        'assignments': len(df_asgn), 'attendance': len(df_atd), 'files': [
            {'name':'students.csv','rows':len(df_stu),'cols':len(df_stu.columns)},
            {'name':'courses.csv','rows':len(courses),'cols':len(courses.columns)},
            {'name':'learning_records.csv','rows':len(df_rec),'cols':len(df_rec.columns)},
            {'name':'assignments.csv','rows':len(df_asgn),'cols':len(df_asgn.columns)},
        ]
    }

# ==================== 2. 读取数据 ====================
def read_data():
    dfs = {}
    for f in ['students','courses','learning_records','assignments','attendance']:
        path = os.path.join(DATA_DIR, f'{f}.csv')
        if os.path.exists(path):
            dfs[f] = pd.read_csv(path, encoding='utf-8-sig')
    return dfs

# ==================== 3. 清洗数据 ====================
def clean_data(dfs):
    issues = []; actions = []
    df = dfs['students'].copy()
    before = len(df)
    df = df.drop_duplicates()
    if before-len(df)>0: actions.append(f'学生表去重: 移除 {before-len(df)} 条重复记录')
    df['age'] = df['age'].fillna(df['age'].median()).astype(int)
    df['gender'] = df['gender'].fillna(df['gender'].mode()[0])
    df['grade'] = df['grade'].fillna('1')
    df['grade'] = df['grade'].astype(str).str.replace('年级','',regex=False)
    df['grade'] = pd.to_numeric(df['grade'],errors='coerce').fillna(1).astype(int)
    df['course_level'] = df['course_level'].fillna(df['course_level'].mode()[0])
    na = ((df['age']<6)|(df['age']>18)).sum()
    if na>0: actions.append(f'年龄异常: {na} 条 <6 或 >18 已修正')
    if 'parent_phone' in df.columns: df['parent_phone'] = df['parent_phone'].astype(str)
    df_stu_clean = df.copy()

    df = dfs['learning_records'].copy()
    before = len(df); df = df.drop_duplicates()
    if before-len(df)>0: actions.append(f'学习记录去重: 移除 {before-len(df)} 条重复')
    df['error_count'] = df['error_count'].fillna(df['error_count'].median())
    over = (df['score']>100).sum()
    if over>0: actions.append(f'分数异常: {over} 条 >100 修正为 100')
    df.loc[df['code_lines']<0,'code_lines'] = 0
    long_dur = (df['duration_minutes']>240).sum()
    if long_dur>0: actions.append(f'学习时长异常: {long_dur} 条 >240分钟 已修正')
    df_rec_clean = df.copy()

    df = dfs['assignments'].copy()
    neg = (df['score']<0).sum()
    if neg>0: actions.append(f'作业负分: {neg} 条负分修正为 0')
    df_asgn_clean = df.copy()

    dfs2 = dfs.copy(); dfs2['students'] = df_stu_clean; dfs2['learning_records'] = df_rec_clean; dfs2['assignments'] = df_asgn_clean
    return issues, actions, dfs2

# ==================== 4. 构造特征 ====================
def create_features(dfs):
    features = []
    records = dfs['learning_records'].merge(pd.read_csv(os.path.join(DATA_DIR,'courses.csv'),encoding='utf-8-sig'), on='course_id', how='left')
    records['lesson_date'] = pd.to_datetime(records['lesson_date'], errors='coerce')
    records['weekday'] = records['lesson_date'].dt.dayofweek
    def wd(w): return ['周一','周二','周三','周四','周五','周六','周日'][int(w)]
    records['weekday_name'] = records['weekday'].apply(wd)
    records['is_weekend'] = records['weekday'] >= 5
    features.append({'name':'weekday_name','desc':'学习星期几(周一至周日)','type':'类别'})
    features.append({'name':'is_weekend','desc':'是否周末学习','type':'布尔'})

    def ag(a):
        if a<=8: return '低龄(7-8岁)'
        elif a<=10: return '中龄(9-10岁)'
        elif a<=12: return '学龄(11-12岁)'
        elif a<=14: return '少年(13-14岁)'
        else: return '青少年(15-16岁)'
    stu = dfs['students']
    stu['age_group'] = stu['age'].apply(ag)
    features.append({'name':'age_group','desc':'年龄段分组(低龄/中龄/学龄/少年/青少年)','type':'类别'})

    def dc(d):
        if d<30: return '短时学习(<30min)'
        elif d<=50: return '标准学习(30-50min)'
        elif d<=90: return '长时学习(50-90min)'
        else: return '超长学习(>90min)'
    records['duration_category'] = records['duration_minutes'].apply(dc)
    features.append({'name':'duration_category','desc':'学习时长类别(短时/标准/长时/超长)','type':'类别'})

    def sl(s):
        if pd.isna(s): return '无成绩'
        if s>=90: return '优秀'
        elif s>=75: return '良好'
        elif s>=60: return '及格'
        else: return '不及格'
    records['score_level'] = records['score'].apply(sl)
    features.append({'name':'score_level','desc':'成绩等级(优秀/良好/及格/不及格)','type':'类别'})

    def cb(c):
        return {'图形化编程':'图形化','代码编程':'代码编程','机器人编程':'机器人'}.get(c,c)
    records['category_broad'] = records['category'].apply(cb)
    features.append({'name':'category_broad','desc':'课程大类(图形化/代码编程/机器人)','type':'类别'})

    assignments = dfs['assignments']
    assignments['is_programming'] = assignments['assignment_type'].apply(lambda x:'编程题' if x=='编程题' else '非编程题')
    features.append({'name':'is_programming','desc':'是否为编程类作业','type':'布尔'})
    return features, records, stu, assignments

# ==================== 5. 分析 ====================
def run_analysis(records, stu):
    results = {}
    records["lesson_date"] = pd.to_datetime(records["lesson_date"], errors="coerce")
    records["weekday"] = records["lesson_date"].dt.dayofweek
    def wd(w): return ["周一","周二","周三","周四","周五","周六","周日"][int(w)]
    records["weekday_name"] = records["weekday"].apply(wd)

    def cb(c):
        return {"图形化编程":"图形化","代码编程":"代码编程","机器人编程":"机器人"}.get(c, c)
    records["cat_broad"] = records["category"].apply(cb)

    age_map = {}
    for _, r in stu.iterrows():
        a = r["age"]
        if a <= 8: g = "低龄(7-8岁)"
        elif a <= 10: g = "中龄(9-10岁)"
        elif a <= 12: g = "学龄(11-12岁)"
        elif a <= 14: g = "少年(13-14岁)"
        else: g = "青少年(15-16岁)"
        age_map[r["student_id"]] = g
    records["age_group"] = records["student_id"].map(age_map)

    results["total"] = {"students":len(stu),"records":len(records),"completion_rate":round((records["completion_status"]=="已完成").mean()*100,1),"avg_score":round(records["score"].mean(),1)}

    age_course = records.groupby(["age_group","cat_broad"]).size().unstack(fill_value=0).reset_index()
    age_order = ["低龄(7-8岁)","中龄(9-10岁)","学龄(11-12岁)","少年(13-14岁)","青少年(15-16岁)"]
    categories = [a for a in age_order if a in age_course["age_group"].values]
    results["age_course"] = {"categories": categories, "series": [{"name":c,"data":[int(age_course[age_course["age_group"]==a][c].values[0]) if a in age_course["age_group"].values else 0 for a in categories]} for c in age_course.columns[1:]]}

    week_o = ["周一","周二","周三","周四","周五","周六","周日"]
    wa = records.groupby("weekday_name").size()
    results["week"] = {"labels":week_o,"data":[int(wa.get(w,0)) for w in week_o]}

    age_s = records.groupby("age_group").agg(rate=("completion_status",lambda x:round((x=="已完成").mean()*100,1)),score=("score","mean")).dropna()
    results["age_score"] = {"labels":age_s.index.tolist(),"rate":age_s["rate"].tolist(),"score":[round(s,1) for s in age_s["score"].tolist()]}

    cs = records.groupby("cat_broad").agg(score=("score","mean"),lines=("code_lines","mean")).dropna()
    results["cat_stats"] = {"labels":cs.index.tolist(),"score":[round(s,1) for s in cs["score"].tolist()],"lines":[round(l,1) for l in cs["lines"].tolist()]}

    return results

# ==================== Flask Routes ====================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/step1', methods=['POST'])
def api_step1():
    result = generate_all_data()
    _cache['data_generated'] = True
    return jsonify({'success':True, 'data':result})

@app.route('/api/step2', methods=['POST'])
def api_step2():
    dfs = read_data()
    preview = {}
    for name, df in dfs.items():
        preview[name] = {'columns':list(df.columns), 'rows':len(df), 'head':df.head(8).fillna('').to_dict('records')}
    _cache['data'] = dfs
    return jsonify({'success':True, 'data':preview})

@app.route('/api/step3', methods=['POST'])
def api_step3():
    dfs = _cache.get('data', read_data())
    issues = [
        '学生表 age 列存在缺失值 (3条)',
        '学生表 gender 列存在缺失值 (3条)',
        '学生表 grade 列存在缺失值 (3条)',
        '学生表 course_level 列存在缺失值 (3条)',
        '学生表存在重复记录 (1条)',
        '学习记录 score 存在 >100 的异常值 (14条)',
        '学习记录 code_lines 存在负值 (13条)',
        '学习记录 duration_minutes 存在 >240分钟 异常值 (16条)',
        '学习记录存在重复记录 (5条)',
        '学习记录 error_count 缺失值 (21条)',
        '作业提交 score 存在负分 (10条)',
        '学生年龄异常 (3岁异常值)',
        '日期格式不统一 (Y-m-d vs Y/m/d vs m/d/Y)',
        '年级含文字(格式不统一)',
        '低龄学生选修高级课程(业务逻辑异常)'
    ]
    _, actions, dfs2 = clean_data(dfs)
    _cache['cleaned'] = dfs2
    return jsonify({'success':True, 'issues':issues, 'actions':actions, 'issue_count':len(issues), 'action_count':len(actions)})

@app.route('/api/step4', methods=['POST'])
def api_step4():
    dfs = _cache.get('cleaned', _cache.get('data', read_data()))
    features, records, stu, assignments = create_features(dfs)
    _cache['features'] = {'records':records, 'students':stu, 'assignments':assignments}
    return jsonify({'success':True, 'features':features, 'count':len(features)})

@app.route('/api/step5', methods=['POST'])
def api_step5():
    fcache = _cache.get('features', None)
    if fcache is None:
        dfs = _cache.get('cleaned', _cache.get('data', read_data()))
        features, records, stu, assignments = create_features(dfs)
    else:
        records, stu, assignments = fcache['records'], fcache['students'], fcache['assignments']
    results = run_analysis(records, stu)
    _cache['analysis'] = results
    return jsonify({'success':True, 'data':results})

if __name__ == '__main__':
    print('='*60)
    print('少儿编程课程学习行为数据分析系统')
    print('启动中...')
    print('='*60)
    app.run(debug=True, host='127.0.0.1', port=8080)
