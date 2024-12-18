from flask import Flask, request, render_template
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    matches = None
    pattern = None

    if request.method == "POST":
        try:
            file = request.files["file"]
            pattern = request.form["pattern"]
            
            if not file or not pattern:
                error = "Please provide a file and a regex pattern."
            else:
                content = file.read().decode("utf-8").splitlines()
                
                matches = [
                    (i + 1, line)
                    for i, line in enumerate(content)
                    for word in line.split()
                    if re.fullmatch(pattern, word)
                ]
        except re.error:
            error = "Invalid regex pattern. Please check your input."
        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render_template("index.html", error=error, matches=matches, pattern=pattern)

if __name__ == "__main__":
    app.run(debug=True)