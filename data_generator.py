"""
data_generator.py
High-speed, authentic synthesis of 1,500+ realistic student records tailored for
Telangana and Indian Engineering campuses (JNTUH / Osmania / Autonomous colleges).
"""

import os
import random
import numpy as np
import pandas as pd

np.random.seed(2026)
random.seed(2026)

DEPARTMENTS = [
    "Computer Science & Engineering (CSE)",
    "CSE (AI & Machine Learning)",
    "CSE (Data Science)",
    "Information Technology (IT)",
    "Electronics & Communication (ECE)",
    "Electrical & Electronics (EEE)",
    "Mechanical Engineering (MECH)",
    "Civil Engineering (CIVIL)"
]

DEPT_CODES = {
    "Computer Science & Engineering (CSE)": "05",
    "CSE (AI & Machine Learning)": "66",
    "CSE (Data Science)": "67",
    "Information Technology (IT)": "12",
    "Electronics & Communication (ECE)": "04",
    "Electrical & Electronics (EEE)": "02",
    "Mechanical Engineering (MECH)": "03",
    "Civil Engineering (CIVIL)": "01"
}

YEARS = [2, 3, 4]
SECTIONS = ["A", "B", "C"]
GENDERS = ["Male", "Female"]

MALE_NAMES = [
    "Sai Teja", "Sravan", "Vamshi", "Karthik", "Prashanth", "Akhil", "Manoj", "Rahul", "Srikar",
    "Sandeep", "Vikram", "Tarun", "Naveen", "Abhinav", "Aditya", "Bharath", "Charan", "Dinesh",
    "Ganesh", "Harish", "Jayanth", "Kishore", "Lokesh", "Mahesh", "Nikhil", "Pavan", "Rakesh",
    "Surya", "Varun", "Yashwanth", "Anirudh", "Rohit", "Hemanth", "Chaitanya", "Shiva", "Siddharth",
    "Arun", "Bhanu", "Chetan", "Deepak", "Eshwar", "Farhan", "Girish", "Hardik", "Ishaan", "Jitendra"
]

FEMALE_NAMES = [
    "Ananya", "Keerthi", "Harini", "Sneha", "Rithika", "Meghana", "Divya", "Priyanka", "Mounika",
    "Bhavani", "Kavya", "Sowmya", "Swathi", "Poojitha", "Tejaswi", "Sindhu", "Ramya", "Shravani",
    "Alekya", "Deepika", "Gayatri", "Ishwarya", "Jahnavi", "Lavanya", "Manisha", "Navya", "Pallavi",
    "Ravali", "Sai Priya", "Tanmayi", "Usha", "Vaishnavi", "Yasaswini", "Chandana", "Sushmitha",
    "Akshitha", "Bindu", "Charitha", "Dharani", "Geethika", "Hima", "Indu", "Jyothi", "Kalyani"
]

LAST_NAMES = [
    "Reddy", "Rao", "Varma", "Goud", "Chowdary", "Sharma", "Verma", "Patel", "Kumar", "Raju",
    "Naidu", "Yadav", "Murthy", "Gupta", "Mishra", "Joshi", "Babu", "Shetty", "Nair", "Iyer",
    "Kulkarni", "Deshmukh", "Singhal", "Agarwal", "Bhat", "Chary", "Prasad", "Sastry", "Venkatesh"
]

def generate_student_dataset(n_students: int = 1500) -> pd.DataFrame:
    records = []
    
    for i in range(1, n_students + 1):
        gender = random.choice(GENDERS)
        first_name = random.choice(MALE_NAMES) if gender == "Male" else random.choice(FEMALE_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"

        dept = random.choice(DEPARTMENTS)
        year = random.choice(YEARS)
        join_year_prefix = {2: "23", 3: "22", 4: "21"}[year]
        dept_code = DEPT_CODES[dept]
        # Strictly unique 10-character Hall Ticket Number: e.g. 22071A0501 to 22071A051500
        hall_ticket_no = f"{join_year_prefix}071A{dept_code}{i:04d}"
        student_id = f"STU{hall_ticket_no}"
        
        email = f"{first_name.lower().replace(' ', '')}.{last_name.lower()}{i:04d}@campus.edu.in"
        semester = (year * 2) - random.choice([0, 1])
        section = random.choice(SECTIONS)

        latent_ability = float(np.random.normal(0, 1))
        latent_effort = float(np.random.normal(0, 1))
        base_rank = 18000 - (12000 * latent_ability) + np.random.normal(0, 5000)
        eamcet_rank = int(np.clip(base_rank, 1200, 85000))

        # Academic
        base_cgpa = 7.15 + (0.95 * latent_ability) + (0.65 * latent_effort) + np.random.normal(0, 0.35)
        cgpa = round(float(np.clip(base_cgpa, 4.25, 9.88)), 2)

        sgpa_delta = np.random.normal(0.06 * latent_effort, 0.45)
        current_sgpa = round(float(np.clip(cgpa + sgpa_delta, 3.80, 10.0)), 2)
        prev_sgpa = round(float(np.clip(cgpa - sgpa_delta, 3.80, 10.0)), 2)
        sgpa_trend = round(current_sgpa - prev_sgpa, 2)

        if cgpa < 5.8:
            active_backlogs = int(np.random.choice([1, 2, 3, 4, 5], p=[0.25, 0.30, 0.25, 0.15, 0.05]))
            history_backlogs = active_backlogs + int(np.random.choice([0, 1, 2, 3], p=[0.3, 0.4, 0.2, 0.1]))
        elif cgpa < 6.8:
            active_backlogs = int(np.random.choice([0, 1, 2, 3], p=[0.60, 0.25, 0.10, 0.05]))
            history_backlogs = active_backlogs + int(np.random.choice([0, 1, 2], p=[0.6, 0.3, 0.1]))
        else:
            active_backlogs = 0
            history_backlogs = int(np.random.choice([0, 1], p=[0.90, 0.10]))

        internal_exam_avg = round(float(np.clip((cgpa * 3.8) + np.random.normal(0, 2.0), 12.0, 39.5)), 1)
        core_subject_avg = round(float(np.clip((cgpa * 9.6) + np.random.normal(0, 4.5), 36.0, 99.0)), 1)

        # Attendance (75% rule)
        base_att = 79.5 + (6.0 * latent_effort) + np.random.normal(0, 6.5)
        overall_attendance = round(float(np.clip(base_att, 40.0, 99.5)), 1)
        lab_attendance = round(float(np.clip(overall_attendance + random.uniform(-3, 6), 45.0, 100.0)), 1)
        consecutive_absences = int(np.clip(np.random.exponential(1.2 if overall_attendance >= 75 else 5.2), 0, 21))

        # LMS
        lms_login_frequency = int(np.clip(9 + (3.5 * latent_effort) + np.random.normal(0, 3.0), 1, 28))
        assignment_completion_rate = round(float(np.clip(72.0 + (14.0 * latent_effort) + np.random.normal(0, 9.0), 18.0, 100.0)), 1)
        avg_assignment_delay_hours = round(float(np.clip(10.0 - (7.0 * latent_effort) + np.random.normal(0, 8.0), 0.0, 72.0)), 1)
        lms_video_watch_pct = round(float(np.clip(assignment_completion_rate + np.random.normal(0, 7.0), 10.0, 100.0)), 1)
        forum_posts_count = int(np.clip(np.random.poisson(max(0.1, 2.2 + max(0.0, latent_effort))), 0, 22))

        # Engagement
        hackathons_participated = int(np.clip(np.random.poisson(max(0.1, 1.4 + (0.6 * latent_ability))), 0, 8))
        certifications_completed = int(np.clip(np.random.poisson(max(0.1, 1.8 + (0.7 * latent_effort))), 0, 7))
        tech_club_active = 1 if (latent_effort > -0.25 and random.random() > 0.30) else 0
        has_leadership_role = 1 if (cgpa >= 7.6 and tech_club_active and random.random() > 0.65) else 0
        events_attended = int(np.clip(np.random.poisson(max(0.1, 3.2 + max(0.0, latent_effort))), 0, 16))

        # Placement
        coding_affinity = latent_ability + np.random.normal(0, 1.35)
        aptitude_percentile = round(float(np.clip(52.0 + (19.0 * latent_ability) + np.random.normal(0, 11.0), 8.0, 99.8)), 1)
        coding_score = round(float(np.clip(46.0 + (23.0 * coding_affinity) + np.random.normal(0, 13.0), 5.0, 100.0)), 1)
        mock_interview_score = round(float(np.clip(5.8 + (1.2 * latent_ability) + (0.9 * latent_effort) + np.random.normal(0, 1.0), 2.0, 10.0)), 1)
        resume_score = round(float(np.clip(56.0 + (7.5 * certifications_completed) + (4.0 * hackathons_participated) + np.random.normal(0, 7.5), 28.0, 98.0)), 1)
        soft_skills_rating = round(float(np.clip(6.2 + (1.1 * latent_effort) + np.random.normal(0, 1.1), 2.5, 9.8)), 1)

        # Skills
        tech_stack_proficiency = round(float(np.clip(0.65 * coding_score + 0.35 * aptitude_percentile, 10.0, 98.0)), 1)
        github_projects_count = int(np.clip(np.random.poisson(max(0.1, 1.6 + max(0.0, coding_affinity))), 0, 14))
        problem_solving_score = round(float(np.clip(52.0 + (21.0 * latent_ability) + np.random.normal(0, 9.5), 12.0, 99.5)), 1)

        # Feedback
        student_satisfaction = round(float(np.clip(7.2 + (0.6 * latent_effort) + np.random.normal(0, 1.1), 2.0, 10.0)), 1)
        faculty_mentor_rating = round(float(np.clip(7.0 + (0.75 * latent_effort) + (0.45 * (overall_attendance / 20.0)) + np.random.normal(0, 0.75), 2.0, 10.0)), 1)
        disciplinary_actions = 1 if (overall_attendance < 52.0 and random.random() < 0.22) else 0

        # Ground Truth Targets for ML
        acad_risk_score = (
            (1.0 if cgpa < 6.5 else 0.0) * 0.35 +
            (1.0 if active_backlogs > 0 else 0.0) * 0.30 +
            (1.0 if overall_attendance < 75.0 else 0.0) * 0.25 +
            (1.0 if assignment_completion_rate < 60.0 else 0.0) * 0.10
        )
        academic_at_risk = 1 if (acad_risk_score >= 0.45 or active_backlogs >= 2) else 0

        placement_risk_score = (
            (1.0 if coding_score < 50.0 else 0.0) * 0.35 +
            (1.0 if aptitude_percentile < 55.0 else 0.0) * 0.25 +
            (1.0 if mock_interview_score < 6.0 else 0.0) * 0.20 +
            (1.0 if active_backlogs > 0 else 0.0) * 0.15 +
            (1.0 if resume_score < 60.0 else 0.0) * 0.05
        )
        placement_at_risk = 1 if (placement_risk_score >= 0.45 or (active_backlogs > 0 and coding_score < 60)) else 0

        records.append({
            "student_id": student_id,
            "hall_ticket_no": hall_ticket_no,
            "name": name,
            "email": email,
            "department": dept,
            "year": year,
            "semester": semester,
            "section": section,
            "gender": gender,
            "eamcet_rank": eamcet_rank,
            # Academic
            "cgpa": cgpa,
            "current_sgpa": current_sgpa,
            "prev_sgpa": prev_sgpa,
            "sgpa_trend": sgpa_trend,
            "active_backlogs": active_backlogs,
            "history_backlogs": history_backlogs,
            "internal_exam_avg": internal_exam_avg,
            "core_subject_avg": core_subject_avg,
            # Attendance
            "overall_attendance": overall_attendance,
            "lab_attendance": lab_attendance,
            "consecutive_absences": consecutive_absences,
            # LMS
            "lms_login_frequency": lms_login_frequency,
            "assignment_completion_rate": assignment_completion_rate,
            "avg_assignment_delay_hours": avg_assignment_delay_hours,
            "lms_video_watch_pct": lms_video_watch_pct,
            "forum_posts_count": forum_posts_count,
            # Engagement
            "hackathons_participated": hackathons_participated,
            "certifications_completed": certifications_completed,
            "tech_club_active": tech_club_active,
            "events_attended": events_attended,
            "has_leadership_role": has_leadership_role,
            # Placement
            "aptitude_percentile": aptitude_percentile,
            "coding_score": coding_score,
            "mock_interview_score": mock_interview_score,
            "resume_score": resume_score,
            "soft_skills_rating": soft_skills_rating,
            # Skills
            "tech_stack_proficiency": tech_stack_proficiency,
            "github_projects_count": github_projects_count,
            "problem_solving_score": problem_solving_score,
            # Feedback & Mentorship
            "student_satisfaction": student_satisfaction,
            "faculty_mentor_rating": faculty_mentor_rating,
            "disciplinary_actions": disciplinary_actions,
            # Ground Truth Targets for ML
            "academic_at_risk": academic_at_risk,
            "placement_at_risk": placement_at_risk
        })

    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_csv = os.path.join(base_dir, "student_records.csv")
    df = generate_student_dataset(1500)
    df.to_csv(out_csv, index=False)
    print(f"Generated {len(df)} authentic records with unique Hall Ticket Numbers.")
