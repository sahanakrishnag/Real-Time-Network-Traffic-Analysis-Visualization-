from flask import Flask, render_template, request
from live_capture import process_pcap
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["pcapfile"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            process_pcap(filepath)
            return render_template("map.html")
    return '''
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="pcapfile">
            <input type="submit">
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)

