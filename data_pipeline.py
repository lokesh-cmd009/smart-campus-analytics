"""
data_pipeline.py
Transforms raw multi-source campus data into unified, engineered feature matrices.
Calculates the Student Success Score (3S Index), pillar sub-scores, and normalized indicator metrics.
"""

import os
import numpy as np
import pandas as pd

def compute_pillar_scores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1. Academic Pillar Score (0 - 100)
    cgpa_norm = np.clip((df["cgpa"] / 10.0) * 100.0, 0.0, 100.0)
    backlog_score = np.clip(100.0 - (df["active_backlogs"] * 30.0), 0.0, 100.0)
    momentum_score = np.clip(50.0 + (df["sgpa_trend"] * 25.0), 0.0, 100.0)
    df["score_academic"] = (0.60 * cgpa_norm + 0.25 * backlog_score + 0.15 * momentum_score).round(1)

    # 2. Attendance Pillar Score (0 - 100)
    consec_penalty = np.clip(100.0 - (df["consecutive_absences"] * 8.0), 0.0, 100.0)
    df["score_attendance"] = (
        0.55 * df["overall_attendance"] + 
        0.25 * df["lab_attendance"] + 
        0.20 * consec_penalty
    ).round(1)

    # 3. LMS Discipline Pillar Score (0 - 100)
    login_score = np.clip(df["lms_login_frequency"] * 6.5, 0.0, 100.0)
    punctuality_score = np.clip(100.0 - (df["avg_assignment_delay_hours"] * 1.8), 0.0, 100.0)
    df["score_lms"] = (
        0.45 * df["assignment_completion_rate"] +
        0.25 * df["lms_video_watch_pct"] +
        0.15 * login_score +
        0.15 * punctuality_score
    ).round(1)

    # 4. Placement Preparedness Pillar Score (0 - 100)
    mock_interview_norm = np.clip(df["mock_interview_score"] * 10.0, 0.0, 100.0)
    df["score_placement"] = (
        0.35 * df["coding_score"] +
        0.30 * df["aptitude_percentile"] +
        0.20 * mock_interview_norm +
        0.15 * df["resume_score"]
    ).round(1)

    # 5. Holistic Skills & Engagement Pillar Score (0 - 100)
    cert_hack_score = np.clip((df["certifications_completed"] * 18.0) + (df["hackathons_participated"] * 15.0), 0.0, 100.0)
    mentor_soft_score = np.clip((df["faculty_mentor_rating"] * 5.0) + (df["soft_skills_rating"] * 5.0), 0.0, 100.0)
    activities_score = np.clip(
        (df["tech_club_active"] * 30.0) + 
        (df["has_leadership_role"] * 30.0) + 
        (df["events_attended"] * 5.0), 
        0.0, 100.0
    )
    df["score_engagement"] = (
        0.35 * df["problem_solving_score"] +
        0.25 * cert_hack_score +
        0.25 * mentor_soft_score +
        0.15 * activities_score
    ).round(1)

    # -------------------------------------------------------------
    # OVERALL STUDENT SUCCESS SCORE (3S Index: 0 - 100)
    # Weights: Academic 30%, Placement 20%, Engagement 20%, Attendance 15%, LMS 15%
    # -------------------------------------------------------------
    df["success_score"] = (
        0.30 * df["score_academic"] +
        0.20 * df["score_placement"] +
        0.20 * df["score_engagement"] +
        0.15 * df["score_attendance"] +
        0.15 * df["score_lms"]
    ).round(1)

    # Success Tier
    def assign_tier(score):
        if score >= 80.0:
            return "Tier 1: High Achiever"
        elif score >= 65.0:
            return "Tier 2: Good Standing"
        elif score >= 50.0:
            return "Tier 3: Moderate Risk"
        else:
            return "Tier 4: Critical Attention"

    df["success_tier"] = df["success_score"].apply(assign_tier)

    # Specific Risk Flags
    df["flag_attendance_detention"] = (df["overall_attendance"] < 75.0).astype(int)
    df["flag_active_backlogs"] = (df["active_backlogs"] > 0).astype(int)
    df["flag_placement_vulnerable"] = ((df["coding_score"] < 50.0) | (df["aptitude_percentile"] < 50.0)).astype(int)
    df["flag_lms_disengaged"] = (df["assignment_completion_rate"] < 60.0).astype(int)

    return df

def get_feature_columns():
    return [
        "cgpa", "sgpa_trend", "active_backlogs", "core_subject_avg",
        "overall_attendance", "lab_attendance", "consecutive_absences",
        "lms_login_frequency", "assignment_completion_rate", "avg_assignment_delay_hours", "lms_video_watch_pct",
        "hackathons_participated", "certifications_completed", "tech_club_active",
        "aptitude_percentile", "coding_score", "mock_interview_score", "resume_score", "soft_skills_rating",
        "tech_stack_proficiency", "github_projects_count", "problem_solving_score",
        "faculty_mentor_rating", "student_satisfaction"
    ]

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_csv = os.path.join(base_dir, "student_records.csv")
    enriched_csv = os.path.join(base_dir, "student_records_enriched.csv")

    raw_df = pd.read_csv(raw_csv)
    enriched_df = compute_pillar_scores(raw_df)
    enriched_df.to_csv(enriched_csv, index=False)
    print(f"Computed Student Success Scores and saved to {enriched_csv}")
    print("Success Score Statistics:")
    print(enriched_df["success_score"].describe())
    print("\nSuccess Tier Distribution:")
    print(enriched_df["success_tier"].value_counts())
