from flask import Flask, render_template, request
from live_capture import process_pcap  # you must define this function
import os

app = Flask(__name__)
UPLOAD_FOLDER = "Documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    locations = []
    if request.method == "POST":
        file = request.files["pcap_file"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Process the pcap file and extract IP geolocations
            locations = process_pcap(filepath)

    return render_template("index.html", locations=locations)

if __name__ == "__main__":
    app.run(debug=True)

