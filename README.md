# SmartEval AI — Setup & Run Guide

## The error you saw ("Failed to fetch") means:
The **frontend is working perfectly** — but the **Flask backend was not running**.
You must start the backend first before opening any HTML page.

---

## STEP 1 — Get Your Gemini API Key (free)

1. Go to: https://aistudio.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy the key (starts with `AIza...`)

---

## STEP 2 — Start the Backend

### On Windows:
```
Double-click:  Backend/START_BACKEND.bat
```
It will install packages and ask for your API key if not set.

### OR manually (Windows CMD):
```cmd
cd Backend
set GEMINI_API_KEY=AIzaYourKeyHere
pip install -r requirements.txt
python app.py
```

### On Mac / Linux:
```bash
cd Backend
export GEMINI_API_KEY=AIzaYourKeyHere
pip install -r requirements.txt
python app.py
```

You should see:
```
==================================================
  SmartEval AI Backend
  http://127.0.0.1:5000
==================================================
```

**Keep this terminal/CMD window open while using the app.**

---

## STEP 3 — Open the Frontend

Open `Frontend/index.html` in your browser.

**Workflow:**
1. Faculty logs in → goes to **faculty-dashboard.html**
2. Faculty clicks **"+ Create Assignment"** → fills form + uploads task PDF
3. Student logs in → goes to **student-dashboard.html**
4. Student selects the assignment from the dropdown
5. Student uploads their submission PDF
6. AI evaluates the student's PDF **against the faculty's task requirements**

---

## How the AI Comparison Works

When a student submits their PDF:

```
[Faculty Task PDF] + [Student Submission PDF]
         ↓               ↓
    Gemini reads      Gemini reads
    requirements      student work
         ↓
  Outputs per-requirement checklist:
  ✔ Step 1 — Done correctly
  ✘ Step 2 — Missing screenshot
  + Score + Strengths + Weaknesses + Feedback
```

If no assignment is selected, the AI does a **general evaluation** without comparison.

---

## File Structure
```
SmartEval/
├── Backend/
│   ├── app.py              ← Flask server (main backend)
│   ├── requirements.txt    ← Python packages
│   ├── START_BACKEND.bat   ← Windows one-click starter
│   ├── start_backend.sh    ← Mac/Linux starter
│   ├── uploads/            ← Auto-created: student PDFs + page images
│   ├── assignments/        ← Auto-created: faculty task PDFs + metadata
│   └── reports/            ← Auto-created: saved JSON evaluation reports
└── Frontend/
    ├── index.html           ← Landing page
    ├── login.html           ← Login (Faculty / Student toggle)
    ├── signup.html          ← Student registration
    ├── faculty-dashboard.html
    ├── student-dashboard.html
    ├── create-assignment.html
    ├── upload-test.html     ← Quick test page
    ├── script.js
    ├── style.css
    └── dashboard.css
```
# SmartEval AI

## 1. Login Page
![Login Page](01-Login%20Page.jpeg)

## 2. Faculty Sign In
![Faculty Sign In](02-Faculty%20Sign%20In.jpeg)

## 3. Student Registration
![Student Registration](03-Student%20Registration.jpeg)

## 4. Student Sign In
![Student Sign In](04-Student%20Sign%20In.jpeg)

## 5. Student Dashboard
![Student Dashboard](05-Student%20Dashboard.jpeg)

## 6. Assignments Page
![Assignments](06-Assignments%20Page.jpeg)

## 7. Student Submissions Page
![Submissions](07-Student%20Submissions%20Page.jpeg)

## 8. Assignment Submission Upload Page
![Upload](08-Assignment%20Submission%20Upload%20Page.jpeg)

## 9. Faculty Dashboard
![Faculty Dashboard](09-Faculty%20Dashboard.jpeg)

## 10. Faculty Student Submissions Review Page
![Review](10-Faculty%20Student%20Submissions%20Review%20Page.jpeg)
