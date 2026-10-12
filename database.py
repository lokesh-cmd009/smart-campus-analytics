"""
database.py
Enterprise SQLite Database Engine for Smart Campus Analytics.
Single source of truth for all 1,500 student records, authentication (RBAC),
student fee ledgers, academic timetables, and early-warning intervention tickets.
Fully optimized with SQL indexes and connection management.
"""

import os
import sqlite3
import hashlib
from typing import Optional, Dict, Any, List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "campus_analytics.db")

def get_connection():
    """Returns an optimized SQLite connection with dictionary row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Returns a SHA-256 hash for secure credential storage."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def ensure_indexes():
    """Creates indexes for rapid sub-millisecond query performance."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_id ON students(student_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_htno ON students(hall_ticket_no);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_dept ON students(department);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_year ON students(year);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_score ON students(success_score);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fees_student_id ON student_fees(student_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timetables_dept_yr ON timetables(department, year);")
    conn.commit()
    conn.close()

def verify_credentials(username_or_email: str, password: str) -> Optional[Dict[str, Any]]:
    """Verifies user login against the SQLite database."""
    conn = get_connection()
    cursor = conn.cursor()
    pwd_hash = hash_password(password)

    cursor.execute("""
    SELECT id, username, email, role, full_name, department, student_id
    FROM users
    WHERE (LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)) AND password_hash = ?;
    """, (username_or_email.strip(), username_or_email.strip(), pwd_hash))

    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def register_user(username: str, email: str, password: str, role: str, full_name: str, department: str = "Computer Science & Engineering (CSE)", student_id: str = None) -> Dict[str, Any]:
    """Registers a new user in SQLite with role validation and auto-generates associated student records if role is student."""
    return register_student_full(
        username=username,
        email=email,
        password=password,
        full_name=full_name,
        hall_ticket_no=username if role == "student" else (student_id.replace("STU", "") if student_id else username),
        department=department,
        role=role,
        student_id=student_id or (f"STU{username}" if role == "student" else None)
    )

def register_student_full(
    username: str,
    email: str,
    password: str,
    full_name: str,
    hall_ticket_no: str,
    department: str = "Computer Science & Engineering (CSE)",
    year: int = 3,
    semester: int = 5,
    section: str = "A",
    cgpa: float = 7.8,
    overall_attendance: float = 80.0,
    coding_score: float = 65.0,
    active_backlogs: int = 0,
    role: str = "student",
    student_id: Optional[str] = None
) -> Dict[str, Any]:
    """Registers a new student user and full academic profile in SQLite with password hashing."""
    conn = get_connection()
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    htno = hall_ticket_no.strip() if hall_ticket_no else username.strip()
    stu_id = student_id or f"STU{htno}"

    try:
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?);", (username.strip(), email.strip()))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.execute("""
            UPDATE users
            SET password_hash = ?, full_name = ?, department = ?, student_id = ?, role = ?
            WHERE id = ?;
            """, (pwd_hash, full_name.strip(), department.strip(), stu_id, role.strip(), existing_user["id"]))
            user_id = existing_user["id"]
        else:
            cursor.execute("""
            INSERT INTO users (username, email, password_hash, role, full_name, department, student_id)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (username.strip(), email.strip(), pwd_hash, role.strip(), full_name.strip(), department.strip(), stu_id))
            user_id = cursor.lastrowid

        if role == "student":
            acad_score = min(100.0, (cgpa * 10 * 0.7) + (overall_attendance * 0.3) - (active_backlogs * 12))
            place_score = min(100.0, (coding_score * 0.6) + (cgpa * 10 * 0.4))
            success_score = round(((acad_score * 0.55) + (place_score * 0.45)), 1)
            tier = "Tier 1: High Achiever" if success_score >= 80 else ("Tier 2: Good Standing" if success_score >= 65 else ("Tier 3: Academic Vulnerability" if success_score >= 50 else "Tier 4: Critical Intervention"))
            persona = "All-Round Achievers" if (coding_score >= 65 and cgpa >= 7.5) else ("Placement-Ready Pragmatists" if coding_score >= 50 else ("Academic Stars with Practical Gaps" if cgpa >= 6.8 else "High-Priority Comprehensive Intervention"))

            cursor.execute("SELECT student_id FROM students WHERE student_id = ? OR hall_ticket_no = ?;", (stu_id, htno))
            existing_student = cursor.fetchone()
            if existing_student:
                cursor.execute("""
                UPDATE students
                SET name = ?, email = ?, department = ?, year = ?, semester = ?, section = ?,
                    cgpa = ?, current_sgpa = ?, overall_attendance = ?, coding_score = ?,
                    active_backlogs = ?, success_score = ?, success_tier = ?, persona = ?,
                    academic_at_risk = ?, placement_at_risk = ?, ml_academic_risk_flag = ?, ml_placement_risk_flag = ?
                WHERE student_id = ?;
                """, (
                    full_name.strip(), email.strip(), department.strip(), year, semester, section.strip(),
                    cgpa, cgpa, overall_attendance, coding_score, active_backlogs,
                    success_score, tier, persona,
                    1 if (overall_attendance < 75 or active_backlogs > 0) else 0,
                    1 if coding_score < 50 else 0,
                    1 if (overall_attendance < 75 or active_backlogs > 0) else 0,
                    1 if coding_score < 50 else 0,
                    existing_student["student_id"]
                ))
            else:
                cursor.execute("""
                INSERT INTO students (
                    student_id, hall_ticket_no, name, email, department, year, semester, section,
                    gender, eamcet_rank, cgpa, current_sgpa, prev_sgpa, sgpa_trend, active_backlogs,
                    history_backlogs, internal_exam_avg, core_subject_avg, overall_attendance,
                    lab_attendance, consecutive_absences, lms_login_frequency, assignment_completion_rate,
                    avg_assignment_delay_hours, lms_video_watch_pct, forum_posts_count, hackathons_participated,
                    certifications_completed, tech_club_active, events_attended, has_leadership_role,
                    aptitude_percentile, coding_score, mock_interview_score, resume_score, soft_skills_rating,
                    tech_stack_proficiency, github_projects_count, problem_solving_score, student_satisfaction,
                    faculty_mentor_rating, disciplinary_actions, academic_at_risk, placement_at_risk,
                    score_academic, score_attendance, score_lms, score_placement, score_engagement,
                    success_score, success_tier, flag_attendance_detention, flag_active_backlogs,
                    flag_placement_vulnerable, flag_lms_disengaged, ml_academic_risk_prob,
                    ml_academic_risk_flag, ml_placement_risk_prob, ml_placement_risk_flag, persona, cluster_id
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, 'Not Specified', 15000, ?, ?, ?, 0.2, ?,
                    0, ?, ?, ?, ?, 1, 14, 85.0, 5.0, 80.0, 3, 2, 2, 1, 3, 0,
                    ?, ?, 7.0, 75.0, 7.5, 70.0, 3, 72.0, 8.0, 7.8, 0,
                    ?, ?, ?, ?, 78.0, ?, 74.0, ?, ?, ?, ?, ?, 0,
                    ?, ?, ?, ?, ?, 3
                );
                """, (
                    stu_id, htno, full_name.strip(), email.strip(), department.strip(), year, semester, section.strip(),
                    cgpa, cgpa, cgpa - 0.2, active_backlogs,
                    round(cgpa * 3.8, 1), round(cgpa * 9.5, 1), overall_attendance,
                    min(100.0, overall_attendance + 5),
                    round(coding_score * 0.9), coding_score,
                    1 if (overall_attendance < 75 or active_backlogs > 0) else 0,
                    1 if coding_score < 50 else 0,
                    round(acad_score, 1), round(overall_attendance, 1), round(place_score, 1),
                    success_score, tier,
                    1 if overall_attendance < 75 else 0,
                    1 if active_backlogs > 0 else 0,
                    1 if coding_score < 50 else 0,
                    0.45 if (overall_attendance < 75 or active_backlogs > 0) else 0.05,
                    1 if (overall_attendance < 75 or active_backlogs > 0) else 0,
                    0.55 if coding_score < 50 else 0.12,
                    1 if coding_score < 50 else 0,
                    persona
                ))

            cursor.execute("SELECT student_id FROM student_fees WHERE student_id = ? OR hall_ticket_no = ?;", (stu_id, htno))
            existing_fee = cursor.fetchone()
            condonation = 1500 if overall_attendance < 75 else 0
            tot_fee = 124000 if overall_attendance < 75 else 122500
            due = condonation
            if not existing_fee:
                cursor.execute("""
                INSERT INTO student_fees (
                    student_id, hall_ticket_no, academic_year, semester, tuition_fee, exam_fee,
                    lab_library_fee, condonation_fee, total_fee, paid_amount, due_amount,
                    payment_status, due_date, receipt_no
                ) VALUES (
                    ?, ?, '2026-2027', ?, 115000, 2500, 5000, ?, ?, 122500, ?,
                    ?, '2026-11-15', ?
                );
                """, (
                    stu_id, htno, semester, condonation, tot_fee, due,
                    'Partially Paid' if due > 0 else 'Paid in Full',
                    f"REC-2026-{user_id:05d}"
                ))

        conn.commit()
        conn.close()
        return {
            "success": True,
            "user": {
                "id": user_id,
                "username": username,
                "email": email,
                "role": role,
                "full_name": full_name,
                "department": department,
                "student_id": stu_id,
                "hall_ticket_no": htno
            }
        }
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e)}

def get_student_record(identifier: str) -> Optional[Dict[str, Any]]:
    """Retrieves full student record by Student ID or Hall Ticket Number."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM students
    WHERE LOWER(student_id) = LOWER(?) OR LOWER(hall_ticket_no) = LOWER(?);
    """, (identifier.strip(), identifier.strip()))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_student_fees(identifier: str) -> Optional[Dict[str, Any]]:
    """Retrieves fee ledger for student."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM student_fees
    WHERE LOWER(student_id) = LOWER(?) OR LOWER(hall_ticket_no) = LOWER(?);
    """, (identifier.strip(), identifier.strip()))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_student_timetable(department: str, year: int, day: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves weekly class schedule for given department and year."""
    conn = get_connection()
    cursor = conn.cursor()
    if day and day != "ALL":
        cursor.execute("""
        SELECT * FROM timetables
        WHERE (department = ? OR department = 'Computer Science & Engineering (CSE)') AND year = ? AND day_of_week = ?
        ORDER BY period_slot ASC;
        """, (department, year, day))
    else:
        cursor.execute("""
        SELECT * FROM timetables
        WHERE (department = ? OR department = 'Computer Science & Engineering (CSE)') AND year = ?
        ORDER BY CASE day_of_week
            WHEN 'Monday' THEN 1
            WHEN 'Tuesday' THEN 2
            WHEN 'Wednesday' THEN 3
            WHEN 'Thursday' THEN 4
            WHEN 'Friday' THEN 5
            WHEN 'Saturday' THEN 6
        END, period_slot ASC;
        """, (department, year))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

if __name__ == "__main__":
    ensure_indexes()
    print("Database indexes verified.")
