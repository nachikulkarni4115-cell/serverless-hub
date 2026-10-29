"""Nachiket Kulkarni: personal portfolio (Flask).

Entry point for Gunicorn is ``app:app``. Project facts below come from the
project reports (TYBScCS / SYBScCS, MIT-WPU) and, for the Cloud Campus stack,
from the code snippets inside that report.
"""
import os
from datetime import datetime

from flask import Flask, abort, jsonify, render_template, url_for

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

SITE = {
    "name": "Nachiket Kulkarni",
    "email": "nachikulkarni4115@gmail.com",
    "github": "https://github.com/nachikulkarni4115-cell",
    "linkedin": "https://www.linkedin.com/in/nachiket-kulkarni-636498299/",
    "location": "Pune, India",
    # Drop a PDF at static/files/Nachiket_Kulkarni_Resume.pdf and the resume
    # buttons appear automatically. Until then they are hidden.
    "resume_file": "files/Nachiket_Kulkarni_Resume.pdf",
    # Paste your Google Drive link for project demos (Anyone with the link → Viewer)
    "demos": "https://drive.google.com/drive/folders/1JsLxu-YLe5j23Ee22BG6pX4UsjlgdOO6",
}


PIPELINE = [
    {"step": "Push", "tool": "GitHub"},
    {"step": "Build", "tool": "Jenkins"},
    {"step": "Publish", "tool": "Docker Hub"},
    {"step": "Run", "tool": "Kubernetes on AWS EC2"},
]

SKILLS = [
    {
        "name": "Backend",
        "blurb": "Server-side code behind most of my projects.",
        "items": ["Python", "Flask", "FastAPI", "Node.js", "Express", "SQLAlchemy", "Pydantic"],
        "used_in": "Cloud Campus, Milo, project management system, Agrisakha, maintenance dashboard",
    },
    {
        "name": "Frontend",
        "blurb": "Interfaces that talk to those backends.",
        "items": ["HTML", "CSS", "JavaScript", "React", "Vite", "Axios", "Jinja templates"],
        "used_in": "Milo, project management system, this portfolio",
    },
    {
        "name": "Cloud and DevOps",
        "blurb": "Getting an app packaged, tested and running somewhere real.",
        "items": ["AWS EC2", "AWS S3", "Docker", "Docker Compose", "Jenkins", "Kubernetes", "Git and GitHub", "Gunicorn", "Render", "Vercel"],
        "used_in": "This portfolio, Cloud Campus, Milo, maintenance dashboard, Agrisakha",
    },
    {
        "name": "Data stores",
        "blurb": "Where application and AI data lives.",
        "items": ["PostgreSQL", "pgvector", "SQLite", "Supabase", "Firebase Realtime Database"],
        "used_in": "Project management system, Milo, attendance system, maintenance dashboard",
    },
    {
        "name": "AI and computer vision",
        "blurb": "Language models, speech and vision libraries used in coursework.",
        "items": ["Retrieval-augmented generation", "Ollama", "Groq API", "Gemini", "LiveKit", "Google speech APIs", "OpenCV", "face_recognition", "DeepFace", "TensorFlow", "Keras", "MobileNetV2"],
        "used_in": "Voice agent, attendance system, emotion detection, Milo, Agrisakha",
    },
]

# Order here is the order shown on the homepage. Slugs are the public URLs.
PROJECTS = [
    {
        "slug": "agrisakha",
        "title": "Agrisakha",
        "kind": "AI, web app",
        "year": None,
        "term": None,
        "team": None,
        "live": "https://agrisakha.nachiketkulkarni.in",
        "live_host": "agrisakha.nachiketkulkarni.in",
        "live_note": "Choose a language, then take or upload a photo of a single leaf.",
        "demo": None,
        "repo": "https://github.com/nachikulkarni4115-cell/Agri-sakha",
        "short": "A crop-leaf health assistant: upload a photo and get the likely condition, a confidence score and what to do next, in English, Hindi or Marathi.",
        "summary": "Agrisakha reads a photo of a crop leaf and says what it most likely shows: a disease, a pest problem, a nutrient deficiency or a healthy leaf. It covers eight crops and 24 conditions, answers in English, Hindi or Marathi, and shows a confidence score and a heatmap of the parts of the leaf the model paid attention to.",
        "problem": "Many leaf diseases look alike by eye, and a farmer often has to decide what to do before an expert can look at the crop. Agrisakha gives a quick first-level reading from a phone photo, in the language the farmer uses, along with symptoms, prevention tips and what to check next.",
        "audience": "Farmers who want a quick first check of a leaf, in English, Hindi or Marathi, before asking an agricultural expert.",
        "how": "The browser resizes and compresses the photo, then sends it to a Flask endpoint. The server checks that the file is a real JPG, PNG or WEBP image, corrects its phone rotation, resizes it to 224 by 224 pixels and scales the pixels the way the model expects. A MobileNetV2 model built with TensorFlow and Keras scores the photo against 24 classes. If the best score is below a 60% confidence threshold, the app does not name a disease and asks for a better photo. Otherwise it returns the top three candidates, plus symptoms, prevention tips and next steps in the chosen language. An occlusion heatmap, made by hiding patches of the leaf and measuring how much the score drops, shows which regions drove the result. Photos are processed in memory and never written to disk.",
        "flow": [
            {"label": "Phone or browser", "detail": "Photo taken or picked, then resized and compressed"},
            {"label": "Flask /predict", "detail": "Checks the image, fixes rotation, resizes to 224×224"},
            {"label": "MobileNetV2", "detail": "TensorFlow and Keras model scores 24 classes"},
            {"label": "Result in your language", "detail": "Top three matches, confidence, advice and heatmap"},
        ],
        "features": [
            "Take a photo or pick one from the gallery",
            "24 classes across eight crops: rice, maize, soyabean, wheat, groundnut, potato, tomato and cotton, including healthy leaves",
            "English, Hindi and Marathi, switchable from the navigation bar",
            "Confidence score with the top three candidate conditions",
            "Declines to guess below a confidence threshold and asks for a better photo",
            "Symptoms, prevention and next steps for each condition",
            "Heatmap showing which parts of the leaf influenced the result",
            "Light and dark themes",
        ],
        "stack": ["Python", "Flask", "TensorFlow", "Keras", "MobileNetV2", "Gunicorn", "Docker", "Pillow", "NumPy", "JavaScript"],
        "limits": [
            "Every result is a first-level assessment from one photo and does not replace an agricultural expert; the app says so on each result",
            "It only knows the 24 classes it was trained on, so a leaf outside them is matched to the nearest class or flagged as uncertain",
            "The heatmap adds about 50 extra model passes per photo, so it can be switched off on small servers",
            "The container runs one Gunicorn worker with two threads, which suits a small number of users at a time",
        ],
        "next_steps": [
            "Add more crops and conditions",
            "Publish the model’s measured accuracy for each class",
        ],
        "images": [],
    },
    {
        "slug": "industrial-maintenance-dashboard",
        "title": "Industrial Maintenance Dashboard",
        "kind": "Cloud, full-stack",
        "year": None,
        "term": None,
        "team": None,
        "live": "https://maintenance.nachiketkulkarni.in",
        "live_host": "maintenance.nachiketkulkarni.in",
        "live_note": "Most of the dashboard sits behind a sign-in. The project page explains what is inside.",
        "demo": None,
        "repo": "https://github.com/nachikulkarni4115-cell/industrial-maintenance-dashboard",
        "short": "A maintenance dashboard for industrial equipment: live telemetry, threshold alerts and work orders, with separate data for each facility.",
        "summary": "A web dashboard where maintenance teams track equipment, watch live telemetry, respond to alerts and manage work orders. Readings arrive through an authenticated API, the dashboard refreshes every five seconds without reloading, and each facility sees only its own equipment.",
        "problem": "Equipment readings, alerts and repair jobs can end up in separate tools, so a rising temperature or vibration reading is easy to miss and hard to tie to the job that fixes it. This project keeps them in one workflow: a reading crosses a threshold, an alert is raised, a technician acknowledges it and a work order tracks the repair.",
        "audience": "Maintenance managers, technicians and read-only viewers at one or more industrial sites.",
        "how": "Readings for temperature, vibration, pressure, rpm and current are posted as JSON to /api/v1/telemetry with a bearer token. The server validates every value, rejects NaN, infinity and out-of-range numbers, and uses an idempotency key so a retried reading is never stored twice. Each reading is checked against warning and critical thresholds for temperature, vibration, pressure and current. A breach opens an alert, and a later critical reading escalates an open warning. Technicians acknowledge and resolve alerts, and managers open work orders against equipment. The dashboard polls a no-cache JSON endpoint every five seconds to update the readings table and the headline counts. Every query is filtered by facility, and important actions are written to an audit log. A Jenkins pipeline runs the tests, builds and pushes the Docker image and updates the Kubernetes deployment.",
        "flow": [
            {"label": "Telemetry source", "detail": "A simulator posts readings with a bearer token; an Azure IoT Hub bridge is included for the same API"},
            {"label": "Flask API", "detail": "Validates readings, drops duplicates and raises threshold alerts"},
            {"label": "SQLAlchemy and SQLite", "detail": "Equipment, readings, alerts, work orders and an audit log on a persistent volume"},
            {"label": "Dashboard", "detail": "Refreshes every five seconds, with role-based pages for each facility"},
        ],
        "features": [
            "Sign-in with four roles: admin, maintenance manager, technician and viewer",
            "Separate data for each facility, with tests that one facility cannot see another’s equipment",
            "Equipment register with type, criticality, status and manufacturer",
            "Live telemetry that refreshes every five seconds without a page reload",
            "Warning and critical alerts that can be acknowledged and resolved with notes",
            "Work orders with priority, assignee, due date and status",
            "Audit log of important actions",
            "Token-protected, idempotent ingestion API with strict input validation",
            "Health and readiness endpoints for Kubernetes",
        ],
        "stack": ["Python", "Flask", "SQLAlchemy", "SQLite", "Docker", "Kubernetes", "Jenkins", "Gunicorn", "Flask-Login", "pytest", "Azure IoT Hub"],
        "limits": [
            "Readings on the live site come from a simulator, not from physical sensors",
            "Alert thresholds are example values; real limits depend on the equipment and its manufacturer",
            "rpm is stored but is not yet checked against thresholds",
            "SQLite on a single persistent volume means the dashboard runs as one replica",
            "The Azure IoT Hub bridge is packaged as a separate service template for review",
        ],
        "next_steps": [
            "Move to a shared database so the dashboard can run more than one replica",
            "Feed real sensor data through the Azure IoT Hub bridge",
            "Set alert thresholds per equipment type",
        ],
        "images": [],
    },
    {
        "slug": "project-management-rag",
        "title": "Project Management System with RAG",
        "kind": "AI, full-stack",
        "year": "2025–26",
        "term": "TYBScCS, semester 6",
        "team": "Team of 4",
        "demo": "https://drive.google.com/drive/folders/1JsLxu-YLe5j23Ee22BG6pX4UsjlgdOO6",
        "repo": None,   # GitHub repo URL
        "short": "A self-hostable project tracker that answers questions about your own tickets and comments.",
        "summary": "A project management platform that turns every project, ticket and comment into searchable meaning. Ask a question in plain language and a local language model answers from your project data instead of guessing.",
        "problem": "Tools like Jira and Trello store tickets well but search them by keyword, so a decision or bug fix is easy to lose unless you remember the exact words used. As a project grows, past work gets buried and teams repeat effort.",
        "how": "When a project, ticket, comment or document is created, the Express backend asks a separate Flask service to turn the text into a 384-dimension embedding and store it in PostgreSQL with pgvector. A question is embedded the same way, matched against the stored vectors, and the closest context is passed to a local model running in Ollama. Relational data and vectors share one database, so no separate vector store is needed.",
        "flow": [
            {"label": "React 19 and Vite", "detail": "Projects, tickets, comments and a chat widget"},
            {"label": "Express 5 API", "detail": "CRUD operations; triggers embedding in the background"},
            {"label": "Flask RAG service", "detail": "/ingest and /chat endpoints"},
            {"label": "PostgreSQL and Ollama", "detail": "pgvector stores embeddings; Ollama runs phi3:mini"},
        ],
        "features": [
            "Create, update and delete projects, tickets, comments and documents",
            "Embeddings generated in the background whenever content is created",
            "Chat assistant that answers from project data",
            "Similar-ticket suggestions ranked by vector distance",
            "Docker Compose setup for the database",
        ],
        "stack": ["React 19", "Vite", "Node.js", "Express 5", "Flask", "PostgreSQL 16", "pgvector", "Ollama", "phi3:mini", "Docker Compose"],
        "limits": [
            "No authentication or authorisation yet",
            "CORS currently allows all origins",
            "Chat memory is not kept between sessions",
            "Ollama has to be run separately",
            "Embeddings for older records must be backfilled manually",
            "Performance under heavy load has not been tested",
        ],
        "images": [
            {"file": "rag-assistant.webp", "w": 1280, "h": 610, "alt": "Ticket page with the RAG assistant open, answering a question and listing similar tickets with distance scores.", "caption": "The assistant answers from ticket history; similar tickets are ranked by vector distance."},
            {"file": "rag-projects.webp", "w": 1280, "h": 610, "alt": "Projects workspace showing a grid of project cards.", "caption": "The projects workspace."},
        ],
    },
    {
        "slug": "milo-ai-study-partner",
        "title": "Milo: AI Study Partner",
        "kind": "AI, full-stack",
        "year": "2025–26",
        "term": "TYBScCS, semester 6",
        "team": "Team of 3",
        "demo": "https://drive.google.com/drive/folders/1JsLxu-YLe5j23Ee22BG6pX4UsjlgdOO6",
        "repo": None,   # GitHub repo URL
        "short": "A study companion with an AI chat, a study-plan generator and task tracking.",
        "summary": "Milo brings AI help and study planning into one place. Ask an academic question, generate a day-by-day plan for an exam, and keep study tasks organised without switching between apps.",
        "problem": "Students juggle planners, note apps and separate AI tools, and most planners cannot explain a concept or respond to what you ask.",
        "how": "A React and Vite front end talks to a FastAPI backend through Axios. FastAPI validates data with Pydantic, stores users, tasks and interaction records in Supabase, and sends study questions to the Groq API for answers. The front end is deployed on Vercel and the API on Render.",
        "flow": [
            {"label": "React and Vite", "detail": "Interface, hosted on Vercel"},
            {"label": "FastAPI", "detail": "Pydantic validation, hosted on Render"},
            {"label": "Supabase and Groq API", "detail": "Data storage and AI responses"},
        ],
        "features": [
            "AI chat for academic questions",
            "Study-plan generator from subject, exam date, topics and daily hours",
            "Curated learning resources for a topic",
            "Task management and progress tracking, as described in the report",
            "Registration and login",
        ],
        "stack": ["React", "Vite", "Axios", "Python", "FastAPI", "Pydantic", "Supabase", "Groq API", "Vercel", "Render"],
        "limits": [
            "AI answers are not always accurate or complete",
            "Needs a constant internet connection",
            "No notifications, reminders or collaboration yet",
            "Only basic authentication and error handling",
            "Scaling on Render and Supabase has not been tuned",
        ],
        "images": [
            {"file": "milo-chat.webp", "w": 1280, "h": 610, "alt": "Milo AI chat answering a question about loops in Python.", "caption": "AI chat answering a study question."},
            {"file": "milo-study-plan.webp", "w": 1280, "h": 610, "alt": "Milo study plan generator form with subject, date, topics and hours fields.", "caption": "The study-plan generator form."},
            {"file": "milo-dashboard.webp", "w": 1280, "h": 610, "alt": "Milo dashboard with AI Chat, Study Plan and Resources shortcuts.", "caption": "Dashboard."},
        ],
    },
    {
        "slug": "cloud-campus",
        "title": "Cloud Campus",
        "kind": "Cloud, web app",
        "year": "2025–26",
        "term": "TYBScCS, semester 5",
        "team": "Team of 4",
        "demo": "https://drive.google.com/drive/folders/1JsLxu-YLe5j23Ee22BG6pX4UsjlgdOO6",
        "repo": None,   # GitHub repo URL
        "short": "A study-notes platform where students upload, find and download course material.",
        "summary": "Cloud Campus is a Flask web app that replaces scattered chat groups and drive links with one searchable library of study notes. Students sign up, upload files tagged by subject, and browse what others have shared.",
        "problem": "Notes circulate through chat groups and personal drives, where links expire, files get buried and seniors’ material is rarely kept for the next batch. Finding reliable notes before exams means asking around.",
        "how": "A Flask application served by Gunicorn handles registration and login with Flask-Login. Note details are stored in a SQL database through SQLAlchemy, while the files themselves go to an AWS S3 bucket using boto3, so they stay available independently of the app server. Uploads are limited to PDF, Word and PowerPoint files up to 16 MB, and the app was deployed on Render.",
        "flow": [
            {"label": "Browser", "detail": "Works on phones and desktops"},
            {"label": "Flask on Gunicorn", "detail": "Login, upload, search and download routes"},
            {"label": "SQL database", "detail": "Note details through SQLAlchemy"},
            {"label": "AWS S3", "detail": "Uploaded files through boto3"},
        ],
        "features": [
            "Register and log in",
            "Personal dashboard listing your uploads",
            "Upload notes with a title, subject and description",
            "Browse with title search and a subject filter",
            "Download counts on each note",
            "Delete a note, which also removes its file from S3",
            "Profile page with total uploads and downloads",
        ],
        "stack": ["Python", "Flask", "Flask-Login", "Flask-SQLAlchemy", "AWS S3", "boto3", "Gunicorn", "Render"],
        "limits": [],
        "images": [
            {"file": "cloud-campus-screens.webp", "w": 1320, "h": 720, "alt": "Three mobile screens of Cloud Campus: login, upload note form and browse notes.", "caption": "Login, upload and browse screens on a phone."},
        ],
    },
    {
        "slug": "face-recognition-attendance",
        "title": "Attendance System with Face Recognition",
        "kind": "Computer vision",
        "year": "2025–26",
        "term": "TYBScCS, semester 5",
        "team": "Team of 6",
        "demo": "https://drive.google.com/drive/folders/1JsLxu-YLe5j23Ee22BG6pX4UsjlgdOO6",
        "repo": None,   # GitHub repo URL
        "short": "A webcam attendance prototype that recognises a student’s face and records the visit.",
        "summary": "Students stand in front of a webcam and are identified from their face, so attendance is marked without sign-in sheets or ID cards. The recognised student’s record is updated in the cloud and shown on screen.",
        "problem": "Manual roll calls take class time, invite proxy attendance and are easy to record wrongly. The project explores a contactless alternative.",
        "how": "Face encodings for enrolled students are generated ahead of time and saved to a file that the live app loads on start-up. For each webcam frame the app finds faces with the face_recognition library, compares them with the stored encodings and takes the closest match. A match loads the student’s record from Firebase Realtime Database, fetches their photo from Firebase Storage, increments their attendance count and stores the time, with a cool-down before the same person can be marked again. OpenCV draws the result on screen.",
        "flow": [
            {"label": "Webcam", "detail": "Frames captured with OpenCV"},
            {"label": "Face matching", "detail": "face_recognition compared with saved encodings"},
            {"label": "Firebase", "detail": "Realtime Database records and Storage photos"},
            {"label": "On-screen result", "detail": "Attendance count and student details"},
        ],
        "features": [
            "Generates and stores face encodings for enrolled students",
            "Real-time recognition from a webcam feed",
            "Attendance count and last-marked time kept per student",
            "Cool-down between repeat marks",
            "Student photo and details shown after a match",
        ],
        "stack": ["Python", "OpenCV", "cvzone", "face_recognition", "dlib", "NumPy", "Firebase Realtime Database", "Firebase Storage"],
        "limits": [
            "A proof of concept without enterprise-grade security or role-based access",
            "No native mobile app",
            "Needs more optimisation before serving thousands of users",
        ],
        "images": [],
    },
    {
        "slug": "voice-controlled-ai-agent",
        "title": "Voice-Controlled AI Agent",
        "kind": "AI, voice",
        "year": "2024–25",
        "term": "SYBScCS, project based learning",
        "team": "Team of 4",
        "demo": "https://drive.google.com/drive/folders/1JsLxu-YLe5j23Ee22BG6pX4UsjlgdOO6",
        "repo": None,   # GitHub repo URL
        "short": "A real-time voice assistant that listens, thinks with an LLM and answers out loud.",
        "summary": "A voice agent you talk to through a browser. It converts speech to text, passes it to a large language model, can call tools such as a weather lookup, and speaks the reply.",
        "problem": "Typing is not always the quickest way to ask an assistant for something, and mainstream assistants run in closed ecosystems that limit customisation.",
        "how": "A Python agent built on LiveKit’s VoicePipelineAgent routes audio in real time. Silero voice-activity detection spots when you are speaking, Google speech-to-text transcribes it, a Google language model decides how to respond and Google text-to-speech reads the answer aloud. The agent can call functions, such as a weather lookup, and a React front end provides microphone, camera and screen-share controls.",
        "flow": [
            {"label": "Microphone", "detail": "Browser audio routed through LiveKit"},
            {"label": "Silero VAD", "detail": "Detects when you are speaking"},
            {"label": "Google speech-to-text", "detail": "Transcribes your request"},
            {"label": "Google LLM", "detail": "Gemini, with function calling"},
            {"label": "Google text-to-speech", "detail": "Speaks the reply"},
        ],
        "features": [
            "Real-time spoken conversation",
            "Voice-activity detection to tell when you have finished speaking",
            "Function calling, including a weather lookup",
            "Modular layout so new skills can be added",
            "React interface with microphone, camera and screen-share controls",
        ],
        "stack": ["Python", "LiveKit Agents", "Silero VAD", "Google Speech-to-Text", "Google Text-to-Speech", "Gemini", "React"],
        "limits": [
            "Needs a stable internet connection",
            "Recognition accuracy varies with background noise and accents",
            "Replies can sound robotic and carry little emotional nuance",
        ],
        "images": [],
    },
    {
        "slug": "emotion-detection",
        "title": "Emotion Detection",
        "kind": "Machine learning",
        "year": "2024–25",
        "term": "SYBScCS, project based learning",
        "team": "Individual report",
        "demo": "https://drive.google.com/drive/folders/1JsLxu-YLe5j23Ee22BG6pX4UsjlgdOO6",
        "repo": None,   # GitHub repo URL
        "credit": "Written and submitted by Razi Kauchali as an individual project report. Included here as related coursework, not as my own contribution.",
        "short": "A computer-vision script that finds a face in an image or webcam frame and labels the dominant emotion.",
        "summary": "A short pipeline that detects faces in an image or live webcam feed and writes the dominant emotion, such as happy or sad, onto the output.",
        "problem": "Emotion recognition is useful in areas like user experience and human–computer interaction, but many systems handle only still images or are too heavy to run live.",
        "how": "OpenCV converts each frame to grayscale and a Haar cascade finds faces, drawing a green box around each. DeepFace analyses the frame and returns the dominant emotion, which is written onto the image. The same loop runs on a live webcam feed until you press q.",
        "flow": [
            {"label": "Image or webcam frame", "detail": "Read with OpenCV"},
            {"label": "Haar cascade", "detail": "Finds faces in grayscale"},
            {"label": "DeepFace", "detail": "Returns the dominant emotion"},
            {"label": "Labelled output", "detail": "Green box and emotion text"},
        ],
        "features": [
            "Works on still images and live webcam video",
            "Face boxes and an emotion label drawn on the output",
            "Seven emotion classes: angry, disgust, fear, happy, neutral, sad and surprise",
        ],
        "stack": ["Python", "OpenCV", "DeepFace", "NumPy", "Matplotlib"],
        "limits": [
            "Needs a clear, front-facing face and decent lighting",
            "Analyses one frame at a time, with no smoothing over time",
            "Can fail when no face is found",
            "Privacy and consent need care outside a classroom demo",
        ],
        "images": [],
    },
]

EDUCATION = {
    "degree": "B.Sc. Computer Science (Cloud Computing)",
    "school": "School of Computer Science & Engineering, Dr. Vishwanath Karad MIT World Peace University, Pune",
    "timeline": [
        {
            "period": "2024–25",
            "stage": "Second year, SYBScCS",
            "slugs": ["voice-controlled-ai-agent"],
        },
        {
            "period": "2025–26",
            "stage": "Third year, TYBScCS (Cloud Computing)",
            "slugs": ["cloud-campus", "face-recognition-attendance", "project-management-rag", "milo-ai-study-partner"],
        },
    ],
}


# ---------------------------------------------------------------------------
# About copy. Everything here is drawn from the project reports and from this
# site's own deployment pipeline. Nothing personal (hobbies, awards, internships)
# is claimed because none was supplied.
# ---------------------------------------------------------------------------
ABOUT = {
    "title": "Learning cloud by building on it",
    "paragraphs": [
        "I’m studying B.Sc. Computer Science with a Cloud Computing specialisation at MIT World Peace University in Pune. Most of what I’ve built has been team work for coursework, and the projects on this site are the clearest record of how that work has developed.",
        "It started in second year with a voice-controlled AI agent: a team project on LiveKit that chained speech recognition, a language model and speech synthesis into one real-time pipeline. Its limits (background noise, accents, a robotic voice) taught as much as its features did.",
        "Third year brought four projects across two semesters. In semester 5: Cloud Campus, a Flask study-notes platform that keeps its files in AWS S3, and a webcam attendance system built on OpenCV and Firebase. In semester 6: a project tracker with retrieval-augmented search on PostgreSQL and pgvector, and Milo, an AI study partner built with React, FastAPI and Groq.",
        "Two more projects now run live on their own subdomains of this site: Agrisakha, a crop-leaf health assistant in English, Hindi and Marathi, and an industrial maintenance dashboard with live telemetry, alerts and work orders.",
        "Python is the thread through most of them. I enjoy the part after the code works: containers, CI/CD and getting an app running somewhere real. This portfolio is one example. It’s a Flask app that ships through Jenkins and Docker Hub to Kubernetes on AWS EC2.",
    ],
}

TAUGHT = [
    {"title": "Files and records belong in different places", "text": "Cloud Campus keeps note details in a SQL database and the files themselves in S3, so uploads stay available whatever happens to the app server."},
    {"title": "One database can do two jobs", "text": "The project tracker stores ordinary rows and 384-dimension embeddings together in PostgreSQL with pgvector, so it needs no separate vector store."},
    {"title": "A voice feature is a chain", "text": "In the voice agent, voice detection, transcription, the model and speech synthesis each hand off to the next, so every link matters to how fast it feels."},
    {"title": "A prototype should say what it lacks", "text": "Every report lists what is missing, from authentication to load testing. I carry those lists onto the project pages instead of hiding them."},
    {"title": "Shipping is part of building", "text": "Pushing to GitHub, building in Jenkins, publishing to Docker Hub and rolling out on Kubernetes made deployment a routine step rather than a last-minute scramble."},
]

TICKER = [
    "Cloud engineering",
    "Backend systems",
    "AI and machine learning",
    "Containers and CI/CD",
    "Computer vision",
]

# Extra project-page sections. Only what the existing report facts support:
#   audience    -> who the project is for, from each report's problem statement
#   targets     -> design targets (not measured results)
#   next_steps  -> the limitations each report lists, restated as work to do
PROJECT_EXTRAS = {
    "project-management-rag": {
        "audience": "Software teams that track work in tickets and want to ask questions about past decisions, not just search for keywords.",
        "next_steps": [
            "Add authentication and authorisation",
            "Restrict CORS to known origins",
            "Keep chat memory between sessions",
            "Backfill embeddings for older records automatically",
            "Test performance under heavy load",
        ],
    },
    "milo-ai-study-partner": {
        "audience": "Students who currently juggle planners, note apps and separate AI tools.",
        "next_steps": [
            "Notifications and reminders",
            "Collaboration between students",
            "Stronger authentication and error handling",
            "Tune scaling on Render and Supabase",
        ],
    },
    "cloud-campus": {
        "audience": "Students who need reliable notes before exams, and seniors whose material should be kept for the next batch.",
    },
    "face-recognition-attendance": {
        "audience": "Classes that lose time to roll calls and want a contactless way to record attendance.",
        "next_steps": [
            "Add security and role-based access",
            "Build a native mobile app",
            "Optimise for far more users",
        ],
    },
    "voice-controlled-ai-agent": {
        "audience": "People who find speaking quicker than typing, and developers who want an assistant they can customise.",
        "targets": [
            "Respond in under 2 seconds",
            "Recognise speech with over 90% accuracy",
        ],
        "next_steps": [
            "Hold up better against background noise and accents",
            "Make replies sound less robotic and more expressive",
        ],
    },
    "emotion-detection": {
        "next_steps": [
            "Smooth emotion labels over several frames",
            "Handle frames where no face is found",
            "Add consent and privacy handling before any use beyond a classroom demo",
        ],
    },
}
for _slug, _extra in PROJECT_EXTRAS.items():
    for _p in PROJECTS:
        if _p["slug"] == _slug:
            _p.update(_extra)


def _existing_images(project):
    """Keep only images that really exist, so a missing file never 404s."""
    folder = os.path.join(STATIC_DIR, "images", "projects")
    return [img for img in project.get("images", []) if os.path.isfile(os.path.join(folder, img["file"]))]


for _project in PROJECTS:
    _project["images"] = _existing_images(_project)

PROJECTS_BY_SLUG = {p["slug"]: p for p in PROJECTS}


@app.context_processor
def inject_globals():
    resume_path = os.path.join(STATIC_DIR, *SITE["resume_file"].split("/"))
    resume_url = url_for("static", filename=SITE["resume_file"]) if os.path.isfile(resume_path) else None

    def asset(filename):
        """url_for('static') plus a version stamp so redeploys bust the cache."""
        try:
            version = int(os.path.getmtime(os.path.join(STATIC_DIR, *filename.split("/"))))
        except OSError:
            version = 0
        return url_for("static", filename=filename, v=version)

    return {
        "site": SITE,
        "asset": asset,
        "resume_url": resume_url,
        "current_year": datetime.now().year,
    }


@app.route("/")
def home():
    return render_template(
        "index.html",
        projects=PROJECTS,
        skills=SKILLS,
        pipeline=PIPELINE,
        education=EDUCATION,
        projects_by_slug=PROJECTS_BY_SLUG,
        about=ABOUT,
        taught=TAUGHT,
        ticker=TICKER,
    )


@app.route("/live")
def live_projects():
    return render_template(
        "live.html",
        live=[p for p in PROJECTS if p.get("live")],
    )


@app.route("/projects/<slug>")
def project_detail(slug):
    project = PROJECTS_BY_SLUG.get(slug)
    if project is None:
        abort(404)
    index = PROJECTS.index(project)
    return render_template(
        "project_detail.html",
        project=project,
        next_project=PROJECTS[(index + 1) % len(PROJECTS)],
        previous_project=PROJECTS[(index - 1) % len(PROJECTS)],
    )


@app.route("/healthz")
def healthz():
    return jsonify(status="ok")


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.after_request
def security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    return response


if __name__ == "__main__":
    # Local development only. In Docker the app is started by Gunicorn (app:app).
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
