"""
ml_engine.py
Machine Learning Engine for Smart Campus Analytics.
Trains Scikit-Learn predictive models for Academic & Placement Risk,
performs K-Means Student Segmentation into 4 Personas, and provides Explainable AI (XAI) drivers.
Imports training data directly from SQLite database (campus_analytics.db).
"""

import os
import joblib
import sqlite3
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report, roc_auc_score, f1_score, accuracy_score
from data_pipeline import get_feature_columns

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "campus_analytics.db")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

class SmartCampusMLEngine:
    def __init__(self):
        self.feature_cols = get_feature_columns()
        self.scaler = StandardScaler()
        self.academic_model = None
        self.placement_model = None
        self.cluster_model = None
        self.cluster_scaler = StandardScaler()
        self.feature_means = {}
        self.feature_stds = {}
        self.academic_feature_importance = {}
        self.placement_feature_importance = {}
        self.cluster_names = {}

    def train_models(self, df: pd.DataFrame):
        X = df[self.feature_cols]
        y_academic = df["academic_at_risk"]
        y_placement = df["placement_at_risk"]

        # Store baseline population statistics for XAI
        for col in self.feature_cols:
            self.feature_means[col] = float(X[col].mean())
            self.feature_stds[col] = float(X[col].std()) if X[col].std() > 0 else 1.0

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        # 1. ACADEMIC RISK MODEL (Gradient Boosting Classifier)
        X_train_a, X_test_a, y_train_a, y_test_a = train_test_split(
            X_scaled, y_academic, test_size=0.2, random_state=42, stratify=y_academic
        )
        self.academic_model = GradientBoostingClassifier(
            n_estimators=120, learning_rate=0.08, max_depth=4, random_state=42
        )
        self.academic_model.fit(X_train_a, y_train_a)
        y_pred_a = self.academic_model.predict(X_test_a)
        y_prob_a = self.academic_model.predict_proba(X_test_a)[:, 1]
        
        acc_a = accuracy_score(y_test_a, y_pred_a)
        f1_a = f1_score(y_test_a, y_pred_a)
        roc_a = roc_auc_score(y_test_a, y_prob_a)
        print(f"Academic Risk Model -> Accuracy: {acc_a:.4f}, F1: {f1_a:.4f}, ROC-AUC: {roc_a:.4f}")

        self.academic_feature_importance = dict(
            sorted(
                zip(self.feature_cols, [float(v) for v in self.academic_model.feature_importances_]),
                key=lambda x: x[1], reverse=True
            )
        )

        # 2. PLACEMENT RISK MODEL (Random Forest Classifier)
        X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
            X_scaled, y_placement, test_size=0.2, random_state=42, stratify=y_placement
        )
        self.placement_model = RandomForestClassifier(
            n_estimators=150, max_depth=6, random_state=42, class_weight='balanced'
        )
        self.placement_model.fit(X_train_p, y_train_p)
        y_pred_p = self.placement_model.predict(X_test_p)
        y_prob_p = self.placement_model.predict_proba(X_test_p)[:, 1]

        acc_p = accuracy_score(y_test_p, y_pred_p)
        f1_p = f1_score(y_test_p, y_pred_p)
        roc_p = roc_auc_score(y_test_p, y_prob_p)
        print(f"Placement Risk Model -> Accuracy: {acc_p:.4f}, F1: {f1_p:.4f}, ROC-AUC: {roc_p:.4f}")

        self.placement_feature_importance = dict(
            sorted(
                zip(self.feature_cols, [float(v) for v in self.placement_model.feature_importances_]),
                key=lambda x: x[1], reverse=True
            )
        )

        # 3. UNSUPERVISED STUDENT SEGMENTATION (K-Means Clustering)
        segmentation_features = [
            "cgpa", "core_subject_avg", "active_backlogs",
            "coding_score", "aptitude_percentile", "mock_interview_score",
            "overall_attendance", "assignment_completion_rate", "certifications_completed"
        ]
        X_cluster = df[segmentation_features]
        X_cluster_scaled = self.cluster_scaler.fit_transform(X_cluster)

        self.cluster_model = KMeans(n_clusters=4, random_state=42, n_init=15)
        clusters = self.cluster_model.fit_predict(X_cluster_scaled)

        cluster_df = pd.DataFrame(X_cluster, columns=segmentation_features)
        cluster_df["cluster"] = clusters
        means = cluster_df.groupby("cluster")[["cgpa", "coding_score", "active_backlogs", "aptitude_percentile"]].mean()

        critical_cid = means.sort_values(by="cgpa").index[0]
        achiever_cid = means.sort_values(by="cgpa", ascending=False).index[0]
        
        remaining = [c for c in means.index if c not in [critical_cid, achiever_cid]]
        if means.loc[remaining[0], "coding_score"] > means.loc[remaining[1], "coding_score"]:
            pragmatist_cid = remaining[0]
            gap_cid = remaining[1]
        else:
            pragmatist_cid = remaining[1]
            gap_cid = remaining[0]

        self.cluster_names = {
            critical_cid: "High-Priority Comprehensive Intervention",
            achiever_cid: "All-Round Achievers",
            pragmatist_cid: "Placement-Ready Pragmatists",
            gap_cid: "Academic Stars with Practical Gaps"
        }

        self.save_models()

    def save_models(self):
        joblib.dump(self.academic_model, os.path.join(MODELS_DIR, "academic_model.pkl"))
        joblib.dump(self.placement_model, os.path.join(MODELS_DIR, "placement_model.pkl"))
        joblib.dump(self.cluster_model, os.path.join(MODELS_DIR, "cluster_model.pkl"))
        joblib.dump(self.scaler, os.path.join(MODELS_DIR, "scaler.pkl"))
        joblib.dump(self.cluster_scaler, os.path.join(MODELS_DIR, "cluster_scaler.pkl"))
        joblib.dump(self.cluster_names, os.path.join(MODELS_DIR, "cluster_names.pkl"))
        joblib.dump(self.feature_means, os.path.join(MODELS_DIR, "feature_means.pkl"))
        joblib.dump(self.feature_stds, os.path.join(MODELS_DIR, "feature_stds.pkl"))
        joblib.dump(self.academic_feature_importance, os.path.join(MODELS_DIR, "acad_feat_imp.pkl"))
        joblib.dump(self.placement_feature_importance, os.path.join(MODELS_DIR, "place_feat_imp.pkl"))

    def load_models(self):
        self.academic_model = joblib.load(os.path.join(MODELS_DIR, "academic_model.pkl"))
        self.placement_model = joblib.load(os.path.join(MODELS_DIR, "placement_model.pkl"))
        self.cluster_model = joblib.load(os.path.join(MODELS_DIR, "cluster_model.pkl"))
        self.scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
        self.cluster_scaler = joblib.load(os.path.join(MODELS_DIR, "cluster_scaler.pkl"))
        self.cluster_names = joblib.load(os.path.join(MODELS_DIR, "cluster_names.pkl"))
        self.feature_means = joblib.load(os.path.join(MODELS_DIR, "feature_means.pkl"))
        self.feature_stds = joblib.load(os.path.join(MODELS_DIR, "feature_stds.pkl"))
        self.academic_feature_importance = joblib.load(os.path.join(MODELS_DIR, "acad_feat_imp.pkl"))
        self.placement_feature_importance = joblib.load(os.path.join(MODELS_DIR, "place_feat_imp.pkl"))

    def predict_student(self, student_row: dict) -> dict:
        feats_df = pd.DataFrame([[student_row.get(col, 0.0) for col in self.feature_cols]], columns=self.feature_cols)
        X_scaled = self.scaler.transform(feats_df)

        acad_prob = float(self.academic_model.predict_proba(X_scaled)[0, 1])
        place_prob = float(self.placement_model.predict_proba(X_scaled)[0, 1])

        segmentation_features = [
            "cgpa", "core_subject_avg", "active_backlogs",
            "coding_score", "aptitude_percentile", "mock_interview_score",
            "overall_attendance", "assignment_completion_rate", "certifications_completed"
        ]
        cluster_df = pd.DataFrame([[student_row.get(col, 0.0) for col in segmentation_features]], columns=segmentation_features)
        X_cluster_scaled = self.cluster_scaler.transform(cluster_df)
        cluster_id = int(self.cluster_model.predict(X_cluster_scaled)[0])
        persona = self.cluster_names.get(cluster_id, "Standard Scholar")

        positive_drivers = []
        negative_drags = []

        friendly_names = {
            "cgpa": "Cumulative GPA (CGPA)",
            "sgpa_trend": "Semester GPA Momentum",
            "active_backlogs": "Active Backlogs Count",
            "overall_attendance": "Classroom Attendance Rate",
            "lab_attendance": "Practical Lab Attendance",
            "consecutive_absences": "Consecutive Absences",
            "assignment_completion_rate": "LMS Assignment Completion",
            "lms_login_frequency": "LMS Weekly Engagement",
            "coding_score": "Coding & DSA Assessment",
            "aptitude_percentile": "Aptitude Assessment Percentile",
            "mock_interview_score": "Mock Interview Performance",
            "resume_score": "Resume Quality Score",
            "certifications_completed": "Industry Certifications",
            "hackathons_participated": "Hackathon Experience",
            "problem_solving_score": "Problem Solving Assessment",
            "faculty_mentor_rating": "Faculty Mentor Review"
        }

        for col, label in friendly_names.items():
            if col not in student_row:
                continue
            val = float(student_row[col])
            mean_val = self.feature_means.get(col, val)
            std_val = self.feature_stds.get(col, 1.0)
            z_score = (val - mean_val) / std_val

            if col in ["active_backlogs", "consecutive_absences"]:
                z_score = -z_score

            weight = self.academic_feature_importance.get(col, 0.05) + self.placement_feature_importance.get(col, 0.05)
            impact_score = round(z_score * weight * 10.0, 2)

            item = {
                "indicator": label,
                "current_value": val,
                "campus_average": round(mean_val, 1),
                "impact_score": impact_score,
                "category": "positive" if impact_score >= 0 else "negative"
            }

            if impact_score >= 0.15:
                positive_drivers.append(item)
            elif impact_score <= -0.15:
                negative_drags.append(item)

        positive_drivers = sorted(positive_drivers, key=lambda x: x["impact_score"], reverse=True)[:4]
        negative_drags = sorted(negative_drags, key=lambda x: x["impact_score"])[:4]

        action_plan = []
        if student_row.get("overall_attendance", 80) < 75.0:
            action_plan.append({
                "type": "Urgent Attendance Action",
                "priority": "HIGH",
                "description": f"Overall attendance is {student_row.get('overall_attendance')}%. Issue official condonation warning and mandate mentor 1-on-1 counseling.",
                "materials": [
                    "5-Day Weekly Class Schedule & Attendance Recovery Tracker",
                    "University Statutory Condonation Appeal & Medical Exemption Checklist",
                    "Student Time Audit & Daily Routine Planning Worksheet"
                ],
                "recommended_videos": [
                    {
                        "title": "Evidence-Based Revision & Study Tips for Students",
                        "channel": "Ali Abdaal",
                        "views": "5.4M+ views",
                        "likes": "244K+ likes",
                        "url": "http://www.youtube.com/watch?v=ukLnPbIffxE"
                    },
                    {
                        "title": "How to Study for Exams - Evidence-Based Masterclass",
                        "channel": "Ali Abdaal",
                        "views": "3.1M+ views",
                        "likes": "76K+ likes",
                        "url": "http://www.youtube.com/watch?v=Lt54CX9DmS4"
                    }
                ]
            })
        if student_row.get("active_backlogs", 0) > 0:
            action_plan.append({
                "type": "Academic Remedial Clinic",
                "priority": "HIGH",
                "description": f"Student has {student_row.get('active_backlogs')} active backlog(s). Enroll in subject-specific Saturday remedial sessions before end-semester exams.",
                "materials": [
                    "Previous 5 Years University Question Papers & Solution Blueprints (PYQs)",
                    "Core Engineering Mind Maps & One-Page High-Yield Formula Sheets",
                    "Faculty Mentorship Question Bank & Model Answer Keys"
                ],
                "recommended_videos": [
                    {
                        "title": "DBMS Full Course for College & University Students",
                        "channel": "Gate Smashers",
                        "views": "7.1M+ views",
                        "likes": "73K+ likes",
                        "url": "http://www.youtube.com/watch?v=kBdlM6hNDAE"
                    },
                    {
                        "title": "Introduction to DBMS With Real Life Examples",
                        "channel": "Gate Smashers",
                        "views": "4.3M+ views",
                        "likes": "74K+ likes",
                        "url": "http://www.youtube.com/watch?v=3EJlovevfcA"
                    }
                ]
            })
        if student_row.get("coding_score", 60) < 50.0:
            action_plan.append({
                "type": "DSA & Coding Intensive Bootcamp",
                "priority": "MEDIUM",
                "description": f"Coding score is {student_row.get('coding_score')}/100. Assign to 3-week foundational Data Structures & Algorithms lab track.",
                "materials": [
                    "Striver's SDE Sheet & A2Z DSA Roadmap Checklist",
                    "LeetCode Blind 75 Must-Do Coding Questions Repository",
                    "Big-O Space & Time Complexity Master Quick Reference Card"
                ],
                "recommended_videos": [
                    {
                        "title": "Algorithms and Data Structures Tutorial - Full Course for Beginners",
                        "channel": "freeCodeCamp.org",
                        "views": "6.0M+ views",
                        "likes": "153K+ likes",
                        "url": "http://www.youtube.com/watch?v=8hly31xKli0"
                    },
                    {
                        "title": "1. Introduction to Algorithms",
                        "channel": "Abdul Bari",
                        "views": "7.8M+ views",
                        "likes": "84K+ likes",
                        "url": "http://www.youtube.com/watch?v=0IAPZzGSbME"
                    }
                ]
            })
        if student_row.get("aptitude_percentile", 60) < 55.0:
            action_plan.append({
                "type": "Quantitative & Aptitude Drilling",
                "priority": "MEDIUM",
                "description": f"Aptitude test score is at the {student_row.get('aptitude_percentile')}th percentile. Enroll in campus placement cell mock aptitude test series.",
                "materials": [
                    "Speed Math & Vedic Math Shortcuts Compendium (Percentages, Ratios, Time-Work)",
                    "Company-Specific Aptitude Drill Packs (TCS NQT, Infosys, Capgemini)",
                    "Logical Reasoning & Deductive Logic Daily Drill Sheets"
                ],
                "recommended_videos": [
                    {
                        "title": "4 Methods to Solve Aptitude Questions in Smart Way (Shortcuts)",
                        "channel": "TalentSprint Aptitude Prep",
                        "views": "5.8M+ views",
                        "likes": "83K+ likes",
                        "url": "http://www.youtube.com/watch?v=Xe3cDAP-GIg"
                    },
                    {
                        "title": "Aptitude Questions for Campus Placements - 30 Second Tricks",
                        "channel": "OnlineStudy4u",
                        "views": "1.0M+ views",
                        "likes": "20K+ likes",
                        "url": "http://www.youtube.com/watch?v=x9xR0GLYn3s"
                    }
                ]
            })
        if student_row.get("mock_interview_score", 7) < 6.0:
            action_plan.append({
                "type": "HR & Technical Interview Mentorship",
                "priority": "MEDIUM",
                "description": f"Mock interview score is {student_row.get('mock_interview_score')}/10. Pair with senior alumni mentor for resume vetting and mock drills.",
                "materials": [
                    "STAR Method (Situation, Task, Action, Result) Behavioral Interview Framework",
                    "Single-Page ATS-Compliant Technical Resume Template (LaTeX/Word)",
                    "Top 50 HR Behavioral & Situational Questions Preparation Dossier"
                ],
                "recommended_videos": [
                    {
                        "title": "Tell Me About Yourself - A Good Answer to This Interview Question",
                        "channel": "Linda Raynier",
                        "views": "25.2M+ views",
                        "likes": "484K+ likes",
                        "url": "http://www.youtube.com/watch?v=kayOhGRcNt4"
                    },
                    {
                        "title": "HOW TO ANSWER: Tell Me About Yourself! Interview Question",
                        "channel": "CareerVidz",
                        "views": "1.0M+ views",
                        "likes": "17K+ likes",
                        "url": "http://www.youtube.com/watch?v=VUzlCG_eoFs"
                    }
                ]
            })
        if not action_plan:
            action_plan.append({
                "type": "Excellence & Career Acceleration",
                "priority": "LOW",
                "description": "Student is performing strongly across all dimensions. Nominate for Tier-1 product company recruitment, research fellowships, or student leadership.",
                "materials": [
                    "System Design Primer & High-Level Architecture (HLD) Roadmap",
                    "Open-Source GitHub Contribution & Portfolio Showcase Guide",
                    "Product MNC / FAANG Coding Competition Preparation Guide"
                ],
                "recommended_videos": [
                    {
                        "title": "Algorithms and Data Structures Tutorial - Full Course for Beginners",
                        "channel": "freeCodeCamp.org",
                        "views": "6.0M+ views",
                        "likes": "153K+ likes",
                        "url": "http://www.youtube.com/watch?v=8hly31xKli0"
                    },
                    {
                        "title": "1. Introduction to Algorithms",
                        "channel": "Abdul Bari",
                        "views": "7.8M+ views",
                        "likes": "84K+ likes",
                        "url": "http://www.youtube.com/watch?v=0IAPZzGSbME"
                    }
                ]
            })

        return {
            "academic_risk_probability": round(acad_prob, 3),
            "academic_risk_flag": bool(acad_prob >= 0.50),
            "placement_risk_probability": round(place_prob, 3),
            "placement_risk_flag": bool(place_prob >= 0.50),
            "persona": persona,
            "cluster_id": cluster_id,
            "positive_drivers": positive_drivers,
            "negative_drags": negative_drags,
            "action_plan": action_plan
        }

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()

    print(f"Loaded {len(df)} records directly from SQLite database ({DB_PATH})...")
    engine = SmartCampusMLEngine()
    engine.train_models(df)
    print("Model training from SQLite database complete.")
