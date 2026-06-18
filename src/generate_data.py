"""
少儿编程课程学习行为数据处理与分析 —— Mock 数据生成脚本
说明：本脚本生成 AI Mock 数据，用于 Python 数据分析课程项目。
数据不是真实爬取数据，而是根据少儿编程教育业务场景模拟生成。
"""

import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

# ==================== 1. 学生信息表 ====================
def generate_students(n=200):
    """生成学生基本信息表"""
    np.random.seed(42)
    random.seed(42)

    first_names = ['子涵', '梓涵', '一诺', '浩宇', '欣怡', '子轩', '思远', '雨桐', '明哲',
                   '嘉琪', '天佑', '诗涵', '俊杰', '雅琪', '致远', '思琪', '宇航', '艺涵',
                   '博文', '雨萱', '昊然', '若曦', '鹏飞', '子墨', '子涵', '宇轩', '悦然',
                   '文博', '梓萱', '皓轩']
    last_names = ['王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴',
                  '徐', '孙', '马', '朱', '胡', '郭', '何', '高', '林', '罗',
                  '郑', '梁', '谢', '宋', '唐', '韩', '冯', '董', '程', '曹']

    records = []
    for i in range(1, n + 1):
        student_id = f'S{str(i).zfill(4)}'
        name = random.choice(last_names) + random.choice(first_names)
        age = random.choice([7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
        gender = random.choice(['男', '女'])
        grade = max(1, age - 5)
        if i % 50 == 0:
            grade = f'{grade}年级'
        if i % 100 == 0:
            age = 3

        enrollment_date = datetime(2025, 9, 1) + timedelta(days=random.randint(0, 180))
        enrollment_str = enrollment_date.strftime('%Y-%m-%d')
        if i % 80 == 0:
            enrollment_str = enrollment_date.strftime('%Y/%m/%d')

        course_level = random.choice(['入门', '初级', '中级', '高级', '竞赛'])
        if age <= 8 and random.random() < 0.05:
            course_level = '高级'

        parent_phone = f'1{random.choice([38,39,50,58,86,88,35,59])}{random.randint(10000000, 99999999)}'
        if i % 70 == 0:
            parent_phone = f'1{random.randint(100000000, 999999999)}'

        records.append({
            'student_id': student_id,
            'name': name,
            'age': age,
            'gender': gender,
            'grade': grade,
            'enrollment_date': enrollment_str,
            'course_level': course_level,
            'parent_phone': parent_phone
        })

    df = pd.DataFrame(records)
    dup_row = df.iloc[[0]].copy()
    dup_row.index = [0]
    df = pd.concat([df, dup_row], ignore_index=True)

    for col in ['age', 'gender', 'grade', 'course_level']:
        for idx in random.sample(range(len(df)), 3):
            df.loc[idx, col] = np.nan

    return df


# ==================== 2. 课程信息表 ====================
def generate_courses():
    """生成课程信息表"""
    courses_data = [
        ('SCR001', 'Scratch趣味编程入门', '图形化编程', '入门', 8, 16),
        ('SCR002', 'Scratch动画制作', '图形化编程', '初级', 6, 12),
        ('SCR003', 'Scratch游戏设计', '图形化编程', '初级', 8, 16),
        ('SCR004', 'Scratch高级项目', '图形化编程', '中级', 8, 16),
        ('PYT001', 'Python编程基础', '代码编程', '初级', 10, 20),
        ('PYT002', 'Python数据结构入门', '代码编程', '中级', 8, 16),
        ('PYT003', 'Python游戏开发', '代码编程', '中级', 10, 20),
        ('PYT004', 'Python数据分析入门', '代码编程', '高级', 8, 16),
        ('PYT005', 'Python人工智能基础', '代码编程', '高级', 10, 20),
        ('PYT006', 'Python网络爬虫', '代码编程', '高级', 6, 12),
        ('EVT001', 'EV3机器人基础', '机器人编程', '初级', 8, 16),
        ('EVT002', 'EV3机器人进阶', '机器人编程', '中级', 8, 16),
        ('EVT003', 'VEX机器人竞赛', '机器人编程', '竞赛', 12, 24),
        ('WEB001', 'HTML/CSS网页设计', '代码编程', '初级', 6, 12),
        ('WEB002', 'JavaScript编程基础', '代码编程', '中级', 8, 16),
        ('APP001', 'App Inventor手机编程', '图形化编程', '初级', 6, 12),
        ('APP002', 'App Inventor高级应用', '图形化编程', '中级', 8, 16),
        ('CPP001', 'C++编程基础', '代码编程', '中级', 10, 20),
        ('CPP002', 'C++算法入门', '代码编程', '高级', 10, 20),
        ('CPP003', '信息学竞赛集训', '代码编程', '竞赛', 12, 24),
    ]
    df = pd.DataFrame(courses_data, columns=['course_id', 'course_name', 'category', 'difficulty', 'duration_weeks', 'lessons_count'])
    return df


# ==================== 3. 学习记录表 ====================
def generate_learning_records(students_df, courses_df, n=1200):
    """生成学习记录表（核心行为数据表）"""
    np.random.seed(42)
    random.seed(42)

    student_ids = students_df['student_id'].dropna().tolist()
    course_ids = courses_df['course_id'].tolist()

    course_lessons = {}
    for _, row in courses_df.iterrows():
        course_lessons[row['course_id']] = list(range(1, row['lessons_count'] + 1))

    records = []
    start_date = datetime(2025, 9, 10)
    end_date = datetime(2026, 6, 1)

    for i in range(1, n + 1):
        record_id = f'LR{str(i).zfill(5)}'
        student_id = random.choice(student_ids)
        course_id = random.choice(course_ids)
        lesson_id = random.choice(course_lessons[course_id])

        days_offset = random.randint(0, (end_date - start_date).days)
        lesson_date = start_date + timedelta(days=days_offset)
        if lesson_date.weekday() < 5 and random.random() < 0.4:
            lesson_date += timedelta(days=(5 - lesson_date.weekday()))
        date_str = lesson_date.strftime('%Y-%m-%d')

        duration = random.choice([15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90])
        if i % 75 == 0:
            duration = random.choice([300, 480, 600])

        completion_status = np.random.choice(['已完成', '未完成', '进行中'], p=[0.7, 0.2, 0.1])

        if completion_status == '已完成':
            score = max(0, min(100, int(np.random.normal(75, 15))))
        else:
            score = np.nan

        if i % 60 == 0 and completion_status == '已完成':
            score = random.choice([105, 110, 120])

        code_lines = max(0, int(np.random.poisson(30)))
        if i % 90 == 0:
            code_lines = -5

        error_count = max(0, int(np.random.exponential(3)))
        if i % 55 == 0:
            error_count = np.nan

        records.append({
            'record_id': record_id,
            'student_id': student_id,
            'course_id': course_id,
            'lesson_id': lesson_id,
            'lesson_date': date_str,
            'duration_minutes': duration,
            'completion_status': completion_status,
            'score': score,
            'code_lines': code_lines,
            'error_count': error_count
        })

    df = pd.DataFrame(records)
    for _ in range(5):
        dup = df.sample(1)
        df = pd.concat([df, dup], ignore_index=True)

    return df


# ==================== 4. 作业提交表 ====================
def generate_assignments(students_df, courses_df, n=800):
    """生成作业提交记录表"""
    np.random.seed(42)
    random.seed(42)

    student_ids = students_df['student_id'].dropna().tolist()
    course_ids = courses_df['course_id'].tolist()
    assignment_types = ['选择题', '填空题', '编程题', '项目作品', '思维导图']

    records = []
    start_date = datetime(2025, 9, 15)
    end_date = datetime(2026, 6, 10)

    for i in range(1, n + 1):
        assignment_id = f'AS{str(i).zfill(4)}'
        student_id = random.choice(student_ids)
        course_id = random.choice(course_ids)
        submit_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        date_str = submit_date.strftime('%Y-%m-%d')
        if i % 65 == 0:
            date_str = submit_date.strftime('%m/%d/%Y')

        assign_type = random.choice(assignment_types)
        if assign_type == '选择题':
            base_score = np.random.normal(80, 10)
        elif assign_type == '填空题':
            base_score = np.random.normal(70, 15)
        elif assign_type == '编程题':
            base_score = np.random.normal(65, 20)
        elif assign_type == '项目作品':
            base_score = np.random.normal(78, 12)
        else:
            base_score = np.random.normal(75, 10)

        score = max(0, min(100, int(base_score)))
        time_spent = random.choice([10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 100, 120])
        attempt_count = np.random.choice([1, 2, 3, 4, 5], p=[0.6, 0.2, 0.1, 0.05, 0.05])
        submission_status = np.random.choice(['已提交', '未提交', '迟交', '需重做'], p=[0.7, 0.1, 0.12, 0.08])

        if i % 80 == 0:
            score = -10

        records.append({
            'assignment_id': assignment_id,
            'student_id': student_id,
            'course_id': course_id,
            'assignment_type': assign_type,
            'submit_date': date_str,
            'score': score,
            'time_spent_minutes': time_spent,
            'attempt_count': attempt_count,
            'submission_status': submission_status
        })

    df = pd.DataFrame(records)
    return df


# ==================== 5. 出勤记录表 ====================
def generate_attendance(students_df, courses_df, n=1000):
    """生成出勤记录表"""
    np.random.seed(42)
    random.seed(42)

    student_ids = students_df['student_id'].dropna().tolist()
    course_ids = courses_df['course_id'].tolist()

    records = []
    start_date = datetime(2025, 9, 15)
    end_date = datetime(2026, 6, 30)

    for i in range(1, n + 1):
        attendance_id = f'AT{str(i).zfill(4)}'
        student_id = random.choice(student_ids)
        course_id = random.choice(course_ids)
        class_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        class_date += timedelta(days=(5 - class_date.weekday()) % 7)
        if class_date.weekday() == 6:
            class_date += timedelta(days=1)
        date_str = class_date.strftime('%Y-%m-%d')

        is_present = np.random.choice([True, False], p=[0.85, 0.15])
        if is_present:
            late_minutes = max(0, int(np.random.exponential(5)))
            if i % 100 == 0:
                late_minutes = 120
        else:
            late_minutes = np.nan

        records.append({
            'attendance_id': attendance_id,
            'student_id': student_id,
            'course_id': course_id,
            'class_date': date_str,
            'is_present': bool(is_present) if not pd.isna(is_present) else None,
            'late_minutes': late_minutes if not np.isnan(late_minutes) else None
        })

    df = pd.DataFrame(records)
    df['is_present'] = df['is_present'].astype('object')
    for idx in random.sample(range(len(df)), 5):
        df.loc[idx, 'is_present'] = np.nan

    return df


# ==================== 主程序 ====================
def main(record_count=None):
    if record_count is None:
        print("\n" + "=" * 60)
        print("少儿编程课程学习行为数据处理与分析")
        print("=" * 60)
        print("\n请选择数据条数：")
        print("  1) 500 条")
        print("  2) 1000 条")
        print("  3) 1500 条（推荐）")
        print("  4) 2000 条")
        choice = input("\n请输入选项 (1-4)，回车默认1500条: ").strip()
        count_map = {"1": 500, "2": 1000, "3": 1500, "4": 2000}
        record_count = count_map.get(choice, 1500)
    n_students = max(50, min(300, record_count // 6))
    n_records = max(300, record_count)
    n_assignments = max(200, record_count * 2 // 3)
    n_attendance = max(300, record_count * 3 // 4)
    """生成所有 Mock 数据并保存为 CSV 文件"""
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("少儿编程课程学习行为数据处理与分析 —— Mock 数据生成")
    print("=" * 60)

    print("\n[1/5] 生成学生信息表...")
    students_df = generate_students(n=n_students)
    students_path = os.path.join(output_dir, 'students.csv')
    students_df.to_csv(students_path, index=False, encoding='utf-8-sig')
    print(f"    → 生成 {len(students_df)} 条记录")

    print("\n[2/5] 生成课程信息表...")
    courses_df = generate_courses()
    courses_path = os.path.join(output_dir, 'courses.csv')
    courses_df.to_csv(courses_path, index=False, encoding='utf-8-sig')
    print(f"    → 生成 {len(courses_df)} 条记录")

    print("\n[3/5] 生成学习记录表...")
    records_df = generate_learning_records(students_df, courses_df, n=n_records)
    records_path = os.path.join(output_dir, 'learning_records.csv')
    records_df.to_csv(records_path, index=False, encoding='utf-8-sig')
    print(f"    → 生成 {len(records_df)} 条记录")

    print("\n[4/5] 生成作业提交表...")
    assignments_df = generate_assignments(students_df, courses_df, n=n_assignments)
    assignments_path = os.path.join(output_dir, 'assignments.csv')
    assignments_df.to_csv(assignments_path, index=False, encoding='utf-8-sig')
    print(f"    → 生成 {len(assignments_df)} 条记录")

    print("\n[5/5] 生成出勤记录表...")
    attendance_df = generate_attendance(students_df, courses_df, n=n_attendance)
    attendance_path = os.path.join(output_dir, 'attendance.csv')
    attendance_df.to_csv(attendance_path, index=False, encoding='utf-8-sig')
    print(f"    → 生成 {len(attendance_df)} 条记录")

    print("\n" + "=" * 60)
    print(f"\n已选择 {record_count} 条数据规模")
    print("数据生成完成！文件汇总：")
    print(f"  students.csv        : {len(students_df)} 行 x {len(students_df.columns)} 列")
    print(f"  courses.csv         : {len(courses_df)} 行 x {len(courses_df.columns)} 列")
    print(f"  learning_records.csv : {len(records_df)} 行 x {len(records_df.columns)} 列")
    print(f"  assignments.csv     : {len(assignments_df)} 行 x {len(assignments_df.columns)} 列")
    print(f"  attendance.csv      : {len(attendance_df)} 行 x {len(attendance_df.columns)} 列")
    print("=" * 60)

    print("\n数据质量问题说明：")
    print("  - 缺失值：学生表 age/gender/grade/course_level，学习记录 error_count/score")
    print("  - 重复值：学生表1条重复，学习记录表5条重复")
    print("  - 异常值：年龄3岁、负分-10、分数>100、代码行数-5")
    print("  - 格式不统一：日期格式(Y-m-d vs Y/m/d vs m/d/Y)、年级含文字")
    print("  - 业务逻辑异常：低龄学生选修高级课程")


if __name__ == '__main__':
    main()
