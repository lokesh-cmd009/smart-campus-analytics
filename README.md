# Smart Campus Analytics: Predict, Optimize & Improve Student Success
**Analytics & AI-Powered Student Success Platform**  
*Built for the KPMG in India Hackathon / Case Challenge*

---

## 📌 Project Overview
Higher education institutions in India generate vast amounts of data across examination cells, biometric attendance, Learning Management Systems (LMS), placement assessment portals, co-curricular records, and mentorship logs. However, this data is traditionally trapped in disconnected silos and reviewed reactively.

**Smart Campus Analytics** transforms campus administration from reactive reporting into proactive decision intelligence:
1. **Unified Student 360° Data Model**: Integrates 7 distinct data streams across **1,250 engineering students**.
2. **Student Success Score (3S Index)**: Multi-criteria composite index ($0–100$) with transparent indicator weights.
3. **Dual-Target Machine Learning Engine**: Scikit-Learn **Gradient Boosting** and **Random Forest** models predicting **Academic Risk** ($99.6\%$ accuracy) and **Placement Risk** ($96.8\%$ accuracy).
4. **Strategic Student Segmentation (Bonus Feature)**: Unsupervised **K-Means clustering** discovering 4 strategic personas, specifically highlighting the crucial **"Academic Stars with Practical Gaps"** segment.
5. **Explainable AI & Driver Waterfall (Bonus Feature)**: Local feature attribution highlighting top positive catalysts vs. negative risk drags for every student.
6. **Prescriptive Action Center & "What-If" Simulator**: Actionable intervention worklists and real-time intervention simulation.
7. **Interactive Web Dashboard**: Beautiful, responsive dashboard available as both a zero-dependency standalone web app and a production **FastAPI** application.

---

## 📂 Project Directory Structure

```
smart_campus_analytics/
├── data_generator.py                   # Generates 1,250+ realistic multi-source student records using Pandas & Faker
├── data_pipeline.py                    # Transforms data, normalizes indicators & computes the Student Success Score (3S)
├── ml_engine.py                        # Scikit-Learn training, risk classifiers, K-Means clustering, and XAI engine
├── app.py                              # Production FastAPI web server with REST APIs & dashboard route
├── generate_standalone_dashboard.py    # Builds zero-dependency standalone dashboard.html with embedded data
├── dashboard.html                      # Interactive standalone dashboard (Opens instantly in any browser)
├── templates/
│   └── index.html                      # FastAPI Jinja2 / HTML5 single-page application dashboard template
├── models/                             # Serialized ML models, scalers, and feature metadata (.pkl)
│   ├── academic_model.pkl              # Gradient Boosting Academic Risk classifier
│   ├── placement_model.pkl             # Random Forest Placement Risk classifier
│   ├── cluster_model.pkl               # K-Means Student Segmentation model
│   ├── scaler.pkl & cluster_scaler.pkl # Fitted StandardScaler instances
│   └── acad_feat_imp.pkl               # Feature importance dictionaries
├── student_records.csv                 # Raw 1,250 student records
├── student_records_enriched.csv        # Enriched records with computed 3S Pillar scores
├── student_records_final.csv           # Complete dataset with ML predictions, probabilities, and personas
├── STUDENT_SUCCESS_SCORE_METHODOLOGY.md # Comprehensive mathematical & administrative methodology note
├── presentation_deck.html              # Interactive HTML slide presentation deck for hackathon evaluation
├── PRESENTATION_DECK.md                # Markdown slide outline and speaker pitch script
└── README.md                           # This documentation guide
```

---

## 🚀 Quickstart & How to Run

### Option 1: Instant Standalone Dashboard (Zero Server Setup Required)
Open `dashboard.html` directly in Google Chrome, Safari, or Microsoft Edge:
```bash
open "/Users/sravankumar/Documents/job mela/smart_campus_analytics/dashboard.html"
```
*The standalone dashboard embeds the full 1,250-student dataset and features live filtering, search, radar charts, student dossiers, explainable AI drivers, and the What-If simulation engine.*

### Option 2: Run via FastAPI Web Application
To run the full-stack REST API and dynamic dashboard on your local machine:

1. Open your terminal and navigate to the project directory:
   ```bash
   cd "/Users/sravankumar/Documents/job mela/smart_campus_analytics"
   ```
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   ```
4. Access the web platform:
   - **Interactive Web Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - **Swagger / OpenAPI Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **Interactive Slide Presentation Deck**: Open `presentation_deck.html` in your browser.

---

## 📊 Summary of Challenge Deliverables & Evaluation Alignment

| Evaluation Criteria | Weight | Deliverable in this Repository |
| :--- | :---: | :--- |
| **Data Integration & Analysis** | 30% | `data_generator.py` & `student_records_final.csv` unifying 7 streams (Academic, Attendance, LMS, Engagement, Placement, Skills, Feedback). |
| **Success Score & Risk Identification** | 25% | `data_pipeline.py` & `STUDENT_SUCCESS_SCORE_METHODOLOGY.md` defining the 3S Index, validated by Scikit-Learn models with >96% accuracy. |
| **Dashboard & Visualization** | 25% | `dashboard.html` & `app.py` delivering executive KPIs, student 360° dossiers, radar charts, and triage worklists. |
| **Problem Understanding** | 10% | Fully grounded in Indian engineering campus realities: 75% attendance condonation rule, university backlogs, and campus hiring patterns. |
| **Presentation & Demo** | 10% | `presentation_deck.html` (interactive 9-slide deck) and `PRESENTATION_DECK.md` pitch script. |
| **Bonus: Student Segmentation** | +5% | 4 strategic personas via K-Means clustering, featuring the "Academic Stars with Practical Gaps" segment. |
| **Bonus: Explainable Score** | +5% | Local driver impact analysis isolating top positive catalysts vs. negative drags relative to population norms. |
