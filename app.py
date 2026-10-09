from flask import Flask, request, render_template_string
from markupsafe import escape

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title }} | My College</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            color: #1e293b;
        }
        header {
            background: #12376a;
            color: white;
            padding: 22px 6%;
        }
        nav { display: flex; flex-wrap: wrap; gap: 15px; }
        nav a { color: white; text-decoration: none; }
        main {
            max-width: 900px;
            margin: 30px auto;
            padding: 25px;
            background: white;
            border-radius: 10px;
        }
        a { color: #1d4ed8; }
        input, button { padding: 10px; margin: 5px 0; }
        button {
            background: #12376a;
            color: white;
            border: 0;
            cursor: pointer;
        }
        footer { text-align: center; padding: 20px; }
    </style>
</head>
<body>
<header>
    <h1>My College Website</h1>
    <nav>
        <a href="/">Home</a>
        <a href="/about.html">About</a>
        <a href="/students/login">Student Login</a>
        <a href="/faculty">Faculty</a>
        <a href="/courses/web-development">Courses</a>
        <a href="/results?year=2026">Results</a>
        <a href="/search?q=computer">Search</a>
        <a href="/2026/article.html?id=10">Blog</a>
        <a href="/url-lab">URL Lab</a>
    </nav>
</header>
<main>
    {{ content|safe }}
</main>
<footer>URL Structure Practical Project</footer>
</body>
</html>
"""

def show_page(title, content):
    return render_template_string(
        TEMPLATE, title=title, content=content
    )

@app.route("/")
def home():
    return show_page("Home", """
        <h2>Welcome to My College</h2>
        <p>This website demonstrates URL structure and routing.</p>
        <ul>
            <li><a href="/students/login">Student Login</a></li>
            <li><a href="/faculty">Faculty</a></li>
            <li><a href="/courses/web-development#modules">Courses</a></li>
            <li><a href="/results?year=2026">Examination Results</a></li>
        </ul>
        <h2 id="details">About This Project</h2>
        <p>Each page has a different URL path.</p>
        <p><a href="/#details">Open the details section</a></p>
    """)

@app.route("/about.html")
def about():
    return show_page("About", """
        <h2>About Our College</h2>
        <p>Welcome to our college website.</p>
        <p>Example file-like URL: /about.html</p>
    """)

@app.route("/students/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        message = "<p>Demo form submitted successfully.</p>"

    return show_page("Student Login", """
        <h2>Student Login</h2>
        <p>This is a demonstration form, not real authentication.</p>
        <form method="POST">
            <label>Student ID</label><br>
            <input name="student_id" required><br>
            <label>Password</label><br>
            <input type="password" name="password" required><br>
            <button type="submit">Demo Login</button>
        </form>
    """ + message)

@app.route("/faculty")
def faculty():
    return show_page("Faculty", """
        <h2>Our Faculty</h2>
        <ul>
            <li>Dr. A. Sharma - Computer Science</li>
            <li>Prof. R. Patil - Information Technology</li>
            <li>Dr. S. Mehta - Electronics</li>
        </ul>
    """)

@app.route("/courses/web-development")
def courses():
    return show_page("Courses", """
        <h2>Web Development Course</h2>
        <p>Learn HTML, CSS, JavaScript and Python.</p>
        <a href="#modules">Jump to course modules</a>
        <h3 id="modules">Course Modules</h3>
        <ol>
            <li>HTML</li>
            <li>CSS</li>
            <li>JavaScript</li>
            <li>Python and Flask</li>
        </ol>
    """)

@app.route("/results")
def results():
    year = escape(request.args.get("year", "2026"))
    return show_page("Results", f"""
        <h2>Examination Results</h2>
        <p>Selected year: {year}</p>
        <p>These are sample results.</p>
        <table border="1" cellpadding="10">
            <tr><th>Student</th><th>Subject</th><th>Marks</th></tr>
            <tr><td>Student A</td><td>Web Technology</td><td>85</td></tr>
            <tr><td>Student B</td><td>Python</td><td>90</td></tr>
        </table>
    """)

@app.route("/search")
def search():
    query = escape(request.args.get("q", ""))
    return show_page("Search", f"""
        <h2>Search Website</h2>
        <form action="/search" method="GET">
            <input name="q" placeholder="Enter search term">
            <button type="submit">Search</button>
        </form>
        <p>Search query: {query or "No query entered"}</p>
        <p>Example: /search?q=computer</p>
    """)

@app.route("/2026/article.html")
def article():
    article_id = escape(request.args.get("id", "10"))
    return show_page("Blog Article", f"""
        <h2>College Technology Blog</h2>
        <p>Article ID: {article_id}</p>
        <p>This sample article discusses web technology.</p>
    """)

@app.route("/url-lab")
def url_lab():
    return show_page("URL Lab", """
        <h2>URL Structure Lab</h2>
        <table border="1" cellpadding="8">
            <tr><th>Component</th><th>Example</th></tr>
            <tr><td>Protocol</td><td>http</td></tr>
            <tr><td>Host</td><td>127.0.0.1</td></tr>
            <tr><td>Port</td><td>5000</td></tr>
            <tr><td>Path</td><td>/students/login</td></tr>
            <tr><td>Query</td><td>?year=2026</td></tr>
            <tr><td>Fragment</td><td>#modules</td></tr>
        </table>
        <h3>College Website URLs</h3>
        <ul>
            <li>/</li>
            <li>/students/login</li>
            <li>/faculty</li>
            <li>/courses/web-development</li>
            <li>/results?year=2026</li>
        </ul>
    """)

@app.errorhandler(404)
def not_found(error):
    return show_page("Not Found", """
        <h2>404 - Page Not Found</h2>
        <a href="/">Return Home</a>
    """), 404

if __name__ == "__main__":
    app.run()