# Smart Campus Analytics: Predict, Optimize & Improve Student Success
**AI-Powered Higher Education Decision Intelligence & Student Success Platform**  
*Built for the KPMG in India Hackathon / Case Challenge*

---

## 📌 Project Overview
Higher education institutions capture rich telemetry across examination cells, biometric attendance, Learning Management Systems (LMS), placement assessment portals, co-curricular records, and mentorship logs. However, this data traditionally remains trapped in disconnected silos and is reviewed reactively after exams are failed or placement drives conclude.

**Smart Campus Analytics** transforms campus administration from reactive reporting into proactive decision intelligence:
1. **Unified Student 360° Data Model**: Integrates 7 distinct data streams across an active cohort of **1,500 engineering students** (8 departments).
2. **Student Success Score (3S Index)**: Transparent multi-criteria composite index ($0–100$) across 4 institutional action tiers (Tier 1: High Achievers $\ge 80.0$, Tier 2: Good Standing $65.0–79.9$, Tier 3: Moderate Risk $50.0–64.9$, Tier 4: Critical Attention $< 50.0$).
3. **Dual-Target Machine Learning Engine**: Scikit-Learn **Gradient Boosting** (Academic Risk Classifier, $100\%$ accuracy) and **Random Forest** (Placement Risk Classifier, $96.7\%$ accuracy).
4. **Strategic Student Segmentation (K-Means Clustering)**: 4 actionable personas, specifically diagnosing the crucial **"Academic Stars with Practical Gaps"** segment (386 students).
5. **Explainable AI (XAI) & Driver Breakdown**: Local feature attribution isolating top positive catalysts (+) vs. negative risk drags (-) relative to campus norms.
6. **5-Day Period Attendance Forecaster**: Period-level matrix timetable simulator with real-time university condonation status tracking (Safe $\ge 75\%$ vs. ₹1,500 Condonation vs. Detention).
7. **Personalized Mentorship & High-Yield Learning Resources**: Prescriptive materials checklists and verified YouTube video masterclasses (Abdul Bari, freeCodeCamp, Linda Raynier, Gate Smashers).
8. **Interactive Dual-Portal Experience**: Strict Role-Based Access Control (RBAC) separating Dean/HOD Executive Cockpit from Student Self-Service.

---

## 📂 Project Directory Structure

```
smart-campus-analytics/
├── dashboard.html                      # Interactive standalone dashboard (zero-dependency, opens in any browser)
├── presentation_deck.html              # 11-slide interactive presentation deck with keyboard navigation
├── PRESENTATION_DECK.md                # Presentation script & slide outline
├── STUDENT_SUCCESS_SCORE_METHODOLOGY.md # Mathematical formulation & tier thresholds note
├── campus_analytics.db                 # SQLite database containing full 1,500 cohort records & tables
├── build_dashboard.py                  # Build script compiling SQLite data into standalone dashboard
├── data_generator.py                   # Synthesizes 1,500 authentic engineering student records
├── data_pipeline.py                    # Computes 3S index and pillar score normalizations
├── ml_engine.py                        # Scikit-Learn training, risk models & K-Means clustering
├── app.py                              # Production FastAPI web server with REST APIs & dashboard route
├── requirements.txt                    # Python package dependencies
├── models/                             # Serialized ML models (.pkl)
│   ├── academic_model.pkl              # Gradient Boosting Academic Risk classifier
│   ├── placement_model.pkl             # Random Forest Placement Risk classifier
│   ├── cluster_model.pkl               # K-Means Student Segmentation model
│   └── scaler.pkl & cluster_scaler.pkl # Fitted StandardScaler instances
└── README.md                           # Project documentation guide
```

---

## 🚀 How to Run the Platform

### Option 1: Instant Standalone Dashboard (Zero Setup / Pure Browser)
No installation or server required. Open `dashboard.html` directly in Google Chrome, Safari, Microsoft Edge, or Firefox:
```bash
# On macOS:
open dashboard.html

# On Linux:
xdg-open dashboard.html

# On Windows:
start dashboard.html
```
*Or simply double-click `dashboard.html` in your file explorer.*

#### 🔑 Demo Accounts Available on Login Screen
- **Dean of Academics (Admin)**: Full executive KPIs, department benchmarks across 8 disciplines, student directory, registration modal, and intervention triage worklists.
- **Student Portal (Lokesh Kumar — High Achiever, HT: 22071A0501)**: Personal 3S score, 5-pillar radar, 5-day attendance forecaster, fee ledger, and personalized mentorship video recommendations.
- **Student Portal (Sai Teja Reddy — Practical Gaps, HT: 22071A0502)**: Demonstrates the "Academic Stars with Practical Gaps" persona with targeted coding bootcamps.
- **Student Portal (Vamshi Goud — At-Risk, HT: 22071A0503)**: Demonstrates attendance condonation warning and remedial clinic scheduling.

---

### Option 2: Interactive Pitch & Presentation Deck
Open `presentation_deck.html` in any browser:
```bash
open presentation_deck.html
```
- Navigate using keyboard arrow keys (`←` / `→`) or on-screen buttons.
- 11 slides detailing the KPMG in India challenge, data integration, dual ML models, personas, XAI, attendance forecaster, mentorship videos, and institutional ROI.

---

### Option 3: Run via Full-Stack FastAPI Web Application (Optional)
If you wish to run the dynamic REST API backend:

1. **Clone the repository and enter the directory**:
   ```bash
   git clone https://github.com/lokesh-cmd009/smart-campus-analytics.git
   cd smart-campus-analytics
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI server**:
   ```bash
   uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   ```

4. **Access the application**:
   - **Web Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - **Interactive API Documentation (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📊 Evaluation Alignment (KPMG Case Challenge)

| Evaluation Criteria | Weight | Deliverable in this Repository |
| :--- | :---: | :--- |
| **Data Integration & Analysis** | 30% | `data_generator.py` & `campus_analytics.db` unifying 7 streams (Academic, Attendance, LMS, Engagement, Placement, Skills, Feedback). |
| **Success Score & Risk Identification** | 25% | `data_pipeline.py` & `STUDENT_SUCCESS_SCORE_METHODOLOGY.md` defining the 3S Index with dual Scikit-Learn predictive classifiers. |
| **Dashboard & Visualization** | 25% | `dashboard.html` & `app.py` delivering executive KPIs, student 360° dossiers, radar charts, and triage worklists. |
| **Problem Understanding** | 10% | Fully grounded in Indian engineering campus realities: 75% attendance condonation rule, university backlogs, and campus hiring patterns. |
| **Presentation & Demo** | 10% | `presentation_deck.html` (interactive 11-slide deck) and `PRESENTATION_DECK.md` pitch script. |
| **Bonus: Student Segmentation** | +5% | 4 strategic personas via K-Means clustering, featuring the "Academic Stars with Practical Gaps" segment. |
| **Bonus: Explainable AI** | +5% | Local driver impact analysis isolating top positive catalysts vs. negative drags relative to population norms. |
