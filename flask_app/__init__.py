from flask import Flask
import os



app = Flask(__name__)
app.secret_key="whateveryou123213432"

app.config["UPLOAD_DIR"] = os.path.join(app.instance_path, "uploads")


@app.template_filter('basename')
def get_basename(path):
    from os.path import basename
    return basename(path)

# Create the upload directory if it doesn't exist
if not os.path.exists(app.config["UPLOAD_DIR"]):
    os.makedirs(app.config["UPLOAD_DIR"])