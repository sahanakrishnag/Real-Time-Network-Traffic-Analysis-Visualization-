from flask import Flask, render_template, request
from live_capture import process_pcap
import os

app = Flask(__name__)
UPLOAD_FOLDER = "Documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'pcapfile' not in request.files:
            return "No file part"

        file = request.files["pcapfile"]
        if file.filename == '':
            return "No selected file"

        # Save the uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Call your processing function
        process_pcap(filepath)

        return render_template("map.html")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
