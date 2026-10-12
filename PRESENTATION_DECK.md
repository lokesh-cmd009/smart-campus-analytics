# Smart Campus Analytics: Pitch & Presentation Deck
**AI-Powered Student Success & Early-Warning Platform**  
*Challenge Brief: KPMG in India — Prediction and Optimisation on Student Analytics and Success Platform*

---

## Slide 1: Title Slide & Project Overview
- **Title**: Smart Campus Analytics: Predict, Optimize & Improve Student Success
- **Subtitle**: Turning Disconnected Campus Data into Proactive Decision Intelligence
- **Challenge**: KPMG in India Hackathon — Prediction & Optimization on Student Analytics & Success Platform
- **Target Audience**: College Deans, Academic Directors, Head of Departments (HODs), Training & Placement Officers (TPO), Faculty Mentors, and Students
- **Key Proposition**:
  - Unifies 7 distinct campus data streams across an active cohort of 1,500 engineering students.
  - Formulates a transparent, explainable **Student Success Score (3S Index: 0–100)** across 4 institutional action tiers.
  - Deploys dual Scikit-Learn predictive classifiers (Academic Risk & Placement Risk) with >96% accuracy and zero data leakage.
  - Performs unsupervised K-Means segmentation into 4 actionable personas (specifically targeting *Academic Stars with Practical Gaps*).
  - Offers Explainable AI (XAI) feature attribution, an interactive "What-If" simulation sandbox, and a period-level 5-day attendance forecaster.

---

## Slide 2: Problem Statement & Campus Realities (KPMG in India Brief)
- **The Challenge**: Higher education institutions capture rich telemetry across ERP databases, LMS platforms, biometric attendance readers, and placement portals, but data remains trapped in isolated silos.
- **The Pain Points**:
  - **Lagging Indicator Trap**: Interventions only occur after students fail end-semester examinations, get detained under the statutory 75% university attendance threshold, or get rejected in campus placement rounds.
  - **Homogeneous Policies**: Colleges treat academic struggles and placement vulnerabilities with one-size-fits-all blunt measures, failing to diagnose nuanced root causes.
  - **Student Blind Spots**: Students lack visibility into how missing specific upcoming class periods impacts their condonation fee standing and overall graduation trajectory.
- **The Solution**: An integrated predictive and prescriptive intelligence platform that predicts risks months in advance and prescribes targeted, high-yield interventions.

---

## Slide 3: Unified 360° Data Architecture (7 Core Streams)
1. **Academic Pillar**: Cumulative GPA (CGPA), Current SGPA, Previous SGPA, Semester SGPA Momentum, Active Backlogs, Arrear History, Internal & Core Exam Marks, TS EAMCET Entrance Rank.
2. **Attendance Pillar**: Overall Classroom Attendance %, Practical Lab Attendance %, Consecutive Absences, 75% Statutory Condonation Standing.
3. **LMS Discipline**: Login Frequency, Assignment Completion %, Video Watch %, Average Submission Delay Hours, Discussion Forum Posts.
4. **Campus Engagement**: Technical Club Activity, Hackathon Participation, NPTEL/Coursera Certifications, Student Leadership Roles, Event Attendance.
5. **Placement Readiness**: Quantitative Aptitude Percentile, Coding & DSA Assessment Scores, Mock HR Interview Performance, Resume Quality Score.
6. **Skill Assessments**: Primary Tech Stack Proficiency, GitHub Projects Count, Problem-Solving Assessment Scores.
7. **Mentorship & Feedback**: Faculty Mentor Reviews, Student Satisfaction Index, Disciplinary Action Records.

---

## Slide 4: Student Success Score (3S Index) Methodology
- **Composite Formulation (0 to 100 Scale)**:
  $$\mathbf{3S} = 0.30 \cdot S_{\text{Academic}} + 0.20 \cdot S_{\text{Placement}} + 0.20 \cdot S_{\text{Engagement}} + 0.15 \cdot S_{\text{Attendance}} + 0.15 \cdot S_{\text{LMS}}$$
- **Four Institutional Action Tiers**:
  - **Tier 1: High Achievers ($3S \ge 80.0$)**: Fast-track for Tier-1 Product MNCs (FAANG/MNCs), research fellowships, and peer tutoring leadership.
  - **Tier 2: Good Standing ($65.0 \le 3S < 80.0$)**: Stable academic track. Guide into specialized domain electives and advanced certifications.
  - **Tier 3: Moderate Risk ($50.0 \le 3S < 65.0$)**: Vulnerable in 1–2 specific dimensions. Targeted faculty mentor coaching and aptitude drilling.
  - **Tier 4: Critical Attention ($3S < 50.0$)**: Compound crisis. Immediate Dean/HOD review, condonation warning notices, and Saturday backlog clinics.

---

## Slide 5: Predictive AI & Machine Learning Engine
- **Academic Risk Classifier (Gradient Boosting)**:
  - Predicts probability of semester failure, year-back, or detention risk.
  - **Accuracy**: $100.0\%$ | **F1-Score**: $1.000$ | **ROC-AUC**: $1.000$
  - Dominant Features: Cumulative GPA ($36.4\%$), Active Backlogs Count ($29.8\%$), Classroom Attendance ($18.5\%$).
- **Placement Outcome Classifier (Random Forest)**:
  - Predicts students at high risk of remaining unplaced during campus placement seasons.
  - **Accuracy**: $96.7\%$ | **F1-Score**: $0.970$ | **ROC-AUC**: $0.995$
  - Dominant Features: Coding Test Score ($34.2\%$), Aptitude Percentile ($26.7\%$), Mock Interview Score ($18.1\%$), Backlogs ($12.3\%$).

---

## Slide 6: Strategic Student Segmentation (4 Personas via K-Means)
Unsupervised clustering on the 1,500-student cohort identifies 4 distinct personas:
1. **All-Round Achievers (28.4% · 426 Students)**: High CGPA ($8.50$), strong coding ($71.1$), high aptitude ($70.5\%$). Target for Marquee Tier-1 Product MNC recruitment.
2. **Placement-Ready Pragmatists (30.3% · 454 Students)**: Moderate CGPA ($6.97$), strong hands-on coding ($55.9$). Target for software engineering & core developer tracks.
3. **Academic Stars with Practical Gaps (25.7% · 386 Students)** *(Direct KPMG Prompt Target)*: Strong exams ($7.01$ CGPA), but severe deficits in competitive coding ($27.9$) and mock interviews. Target for mandatory 4-week coding bootcamp and mock drills.
4. **High-Priority Comprehensive Intervention (15.6% · 234 Students)**: Compound crisis: active backlogs, low attendance ($64.8\%$), low coding ($28.5$). Target for joint HOD counseling and Saturday remedial classes.

---

## Slide 7: Explainable AI (XAI) & Interactive "What-If" Simulation
- **Explainable Driver Attribution**:
  - Decomposes each student's score relative to campus population norms.
  - Identifies top **Positive Catalysts (+)** (e.g. $+2.8$ from high CGPA, $+1.9$ from NPTEL certifications) vs. top **Negative Drags (-)** (e.g. $-3.4$ from 2 active backlogs, $-2.1$ from low coding score).
- **Interactive "What-If" Intervention Simulator**:
  - Allows faculty to model: *What if classroom attendance increases $+10\%$, LMS assignments are completed $+15\%$, and backlogs are cleared?*
  - Instantly recalculates 3S Score ($48.2 \to 63.5$, $+15.3$ pts) and predicts Academic Risk reduction ($88\% \to 12\%$).

---

## Slide 8: Interactive 5-Day Period Attendance Forecaster
- **Period-Level Matrix Planning**:
  - Empowers students to view their upcoming 5-day class timetable and select/deselect specific periods they plan to attend.
- **Dynamic Standing & Condonation Recalculation**:
  - Instantly projects end-of-semester attendance % and displays statutory status:
    - **Safe ($\ge 75\%$)**: University Hall Ticket granted with zero fee penalty.
    - **Condonation ($65\% - 74.9\%$)**: Flags mandatory ₹1,500 condonation fee and required medical/HOD exemption letter.
    - **Detained ($< 65\%$)**: Barred from semester examinations under university regulations.
  - Computes exact minimum periods required to achieve $75\%$ standing.

---

## Slide 9: Personalized Mentorship Plans & High-Yield Learning Resources
Every prescriptive mentorship action item provides tangible deliverables:
1. **Required Study Materials & Checklists**:
   - DSA topic roadmap (Striver’s SDE Sheet, LeetCode Blind 75).
   - Single-page ATS-compliant tech resume templates.
   - Previous 5 years university exam question papers (PYQs) and formula mind maps.
2. **Curated YouTube Video Recommendations (Highest Views & Likes)**:
   - Coding/DSA: freeCodeCamp Algorithms Course (6.0M+ views) & Abdul Bari Algorithms (7.8M+ views).
   - HR & Interviews: Linda Raynier "Tell Me About Yourself" (25.2M+ views) & CareerVidz.
   - Aptitude: TalentSprint Shortcuts (5.8M+ views) & OnlineStudy4u.
   - Academic Remedial: Gate Smashers Full DBMS Syllabus (7.1M+ views).
   - Study & Exam Recovery: Ali Abdaal Evidence-Based Masterclass (5.4M+ views).

---

## Slide 10: Production Architecture & Role-Based Access Control (RBAC)
- **Zero-Bleed Role Separation**:
  - **Dean & HOD Cockpit**: Institutional overview, student directory, AI persona triage, risk filters, and student registration.
  - **Student Self-Service Portal**: Personal 3S analytics, 5-day attendance forecaster, fee ledger, internal CIE marks, and certifications.
- **Zero-Dependency Standalone Execution**:
  - Single-file deliverable (`dashboard.html`) running locally in any browser with embedded SQLite data and client-side encryption.
- **FastAPI REST API (`app.py`)**:
  - Endpoints for `/api/auth/login`, `/api/admin/add-student`, `/api/kpis`, `/api/students`, and `/api/simulate`.

---

## Slide 11: Institutional Impact & ROI (KPMG Challenge Alignment)
1. **Retention & Pass Rate Lift**: Proactive early warning prevents attendance detentions and academic probations months before semester finals.
2. **Placement Conversion Surge**: Targeted coding bootcamps for the 386 "Academic Stars with Practical Gaps" translate theoretical grades into marquee product offers.
3. **NIRF & NAAC Accreditation Compliance**: Directly fulfills NAAC Criterion II (Teaching-Learning Evaluation) and Criterion V (Student Support & Progression) institutional audit requirements.
