from flask import Flask, render_template, abort

app = Flask(__name__)

PROJECTS = [
    {
        "slug": "project-management-rag",
        "number": "01",
        "category": "AI / KNOWLEDGE SYSTEMS",
        "title": "Project Management System",
        "short": "A project workspace concept enhanced with retrieval-augmented generation (RAG).",
        "summary": "A project-management experience that connects project information with knowledge retrieval, helping users find relevant context without digging through disconnected notes.",
        "problem": "Project details can become scattered across tasks, documents, and conversations. The project explores how a structured workspace and retrieval-based AI can make that information easier to find and use.",
        "approach": "Organize project information in a consistent workspace and use a retrieval layer to surface relevant context for a user's question. The exact retrieval pipeline and implemented features should be confirmed against the final source code.",
        "features": ["Project information in one workspace", "Knowledge retrieval using a RAG approach", "Structured data storage", "Container-friendly development workflow"],
        "stack": ["RAG", "PostgreSQL", "Docker"],
        "stack_note": "These technologies were identified in the portfolio brief. Add any embedding model, vector store, backend framework, or LLM only if it is present in your implementation.",
        "accent": "violet",
        "mark": "RAG"
    },
    {
        "slug": "cloud-campus",
        "number": "02",
        "category": "CLOUD / WEB APPLICATION",
        "title": "Cloud Campus",
        "short": "A campus-focused digital experience built around accessible web services.",
        "summary": "A cloud-oriented campus project intended to bring useful student-facing information or workflows into a single digital experience.",
        "problem": "Campus information and student workflows can be spread across separate channels. This project presents a digital approach to making campus-related services easier to access.",
        "approach": "Use a web application as the central experience, with cloud deployment and service configuration documented alongside the implementation. Confirm the exact user roles and features from your project repository before publishing.",
        "features": ["Campus-oriented digital experience", "Web-based access", "Potential for cloud deployment and scaling", "A foundation for adding student services"],
        "stack": [],
        "stack_note": "Technology details were not included in the supplied brief. Replace this note with the exact framework, database, and cloud services you used.",
        "accent": "blue",
        "mark": "CC"
    },
    {
        "slug": "face-recognition-attendance",
        "number": "03",
        "category": "COMPUTER VISION",
        "title": "Face Recognition Attendance",
        "short": "An attendance workflow explored through face recognition.",
        "summary": "A computer-vision project focused on using face recognition as part of an attendance workflow.",
        "problem": "Manual attendance can take time and may introduce recording errors. This project explores how facial recognition can support a more streamlined attendance process.",
        "approach": "A typical workflow detects a face, compares it against enrolled identities, and records a result when the match meets the application's criteria. Keep only the steps and safeguards that your implementation actually includes.",
        "features": ["Face-based identification concept", "Attendance recording workflow", "Computer-vision pipeline", "Opportunity to evaluate recognition accuracy and edge cases"],
        "stack": [],
        "stack_note": "Add the actual libraries and storage layer used in your project, such as OpenCV or a database, only if they are part of your code.",
        "accent": "lime",
        "mark": "CV"
    },
    {
        "slug": "voice-controlled-ai-agent",
        "number": "04",
        "category": "AI / VOICE INTERACTION",
        "title": "Voice-Controlled AI Agent",
        "short": "A voice-first interface for interacting with an AI assistant.",
        "summary": "An AI-agent project exploring how spoken input can become an accessible way to issue commands or request assistance.",
        "problem": "Typing is not always the most convenient way to interact with a digital assistant. Voice interaction can make common actions feel more direct and natural.",
        "approach": "A voice-agent workflow commonly combines speech input, intent or language processing, an action or response layer, and spoken or on-screen output. Update this section to match the components implemented in your project.",
        "features": ["Voice-first interaction concept", "Natural-language request handling", "Assistant response workflow", "Potential for hands-free use cases"],
        "stack": [],
        "stack_note": "The exact speech-recognition, LLM, automation, and text-to-speech technologies were not included in the supplied brief.",
        "accent": "orange",
        "mark": "VOX"
    },
    {
        "slug": "emotion-detection",
        "number": "05",
        "category": "MACHINE LEARNING",
        "title": "Emotion Detection",
        "short": "A machine-learning project exploring emotion classification.",
        "summary": "A project focused on classifying emotional signals from the input type supported by the implementation.",
        "problem": "Emotion-related signals are complex and context-dependent. This project explores a machine-learning approach to categorizing signals into a defined set of classes.",
        "approach": "The application processes an input, applies a trained or configured model, and presents a predicted class. The input modality, dataset, labels, and evaluation results should be specified from your actual project.",
        "features": ["Emotion-classification workflow", "Model-driven prediction", "Results presented to the user", "Scope to document model evaluation and limitations"],
        "stack": [],
        "stack_note": "Confirm whether your implementation uses facial images, text, audio, or another input type, and list the actual model and libraries.",
        "accent": "pink",
        "mark": "EM"
    },
    {
        "slug": "milo-ai-study-partner",
        "number": "06",
        "category": "AI LEARNING",
        "title": "Milo — AI Study Partner",
        "short": "An AI-assisted learning companion designed to support study sessions.",
        "summary": "Milo is an AI study-partner concept that helps learners interact with study support through a focused learning experience.",
        "problem": "Students often need a convenient way to ask questions, revisit concepts, and maintain momentum while studying. Milo explores an AI-supported interface for that experience.",
        "approach": "The project brief identifies React, FastAPI, and Supabase. Together, these can support a frontend, API layer, and backend data services; describe specific AI capabilities only where they are implemented.",
        "features": ["Dedicated study-partner experience", "Frontend and API separation", "Backend data services", "Potential to extend with study history and personalized support"],
        "stack": ["React", "FastAPI", "Supabase"],
        "stack_note": "The supplied brief names these technologies. Add the specific model provider and study features only if they are implemented in your current code.",
        "accent": "lime",
        "mark": "MILO"
    },
]

@app.route("/")
def home():
    return render_template("index.html", projects=PROJECTS)

@app.route("/projects/<slug>")
def project_detail(slug):
    project = next((item for item in PROJECTS if item["slug"] == slug), None)
    if project is None:
        abort(404)
    index = PROJECTS.index(project)
    next_project = PROJECTS[(index + 1) % len(PROJECTS)]
    previous_project = PROJECTS[(index - 1) % len(PROJECTS)]
    return render_template(
        "project_detail.html",
        project=project,
        next_project=next_project,
        previous_project=previous_project,
    )

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
