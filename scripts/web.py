"""
A simple flask server for serving a web interface to change the config and view
the contents of the "/data/outputs" folder.
"""
import datetime
import os
import json
import subprocess

from flask import Blueprint, Flask, render_template, send_from_directory, request, redirect, send_file

from .check import check_files_and_folders


web = Blueprint("web", __name__, template_folder="templates")


@web.route("/")
def index():
    current_config = open("/data/config.json", "r").read()
    current_config = json.loads(current_config)
    current_config['prompts'] = ", ".join(current_config['prompts'])
    return render_template("index.html", current_config=current_config)


@web.route("/outputs")
def outputs():
    """
    Returns the contents of the "/data/outputs" folder
    """

    files = os.listdir("/data/outputs")

    # sort files by date created
    files.sort(key=lambda x: -os.path.getmtime("/data/outputs/" + x))

    # remove 'steps' from the list of directories
    if 'steps' in files:
        files.remove('steps')

    # create a list of links to the outputs
    links = []
    for file in files:
        date = os.path.getmtime("/data/outputs/" + file)
        date = datetime.datetime.fromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S")
        id = file.split("--")[0]
        title = ' '.join(file.split("--")[1].split('.')[0].split('-'))
        links.append({"file": "/outputs/" + file, "date": date, "id" : id, "title": title})

    return render_template("outputs.html", links=links)


@web.route("/outputs/<path:path>")
def outputs_path(path):
    """
    Returns the image at the given path.
    """
    return send_from_directory("/data/outputs", path)


@web.route("/generate")
def generate():
    """
    Runs the script "scripts/generate.py" and writes the output to /data/outputs
    as it is generate with threading
    """

    command = [
        "python",
        "-m",
        "scripts.generate",
        "-c",
        "/data/config.json",
    ]

    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = p.communicate()[0]

    return output.decode("utf-8")


@web.route("/update_config", methods=["POST"])
def update_config():
    """
    Updates the config.json file with the given values. The values that can be
    updated and are in the POST request are:

    prompts: A string of comma separated prompts to use, turn into a list of strings
    init_image: An image that we need to download and set this path to.
    width: The width of the image. (is the first dimension of size list)
    height: The height of the image. (is the second dimension of size list)
    max_iterations: The number of iterations to run.
    """

    old_config = json.loads(open("/data/config.json", "r").read())

    # get the values from the POST request
    prompts = request.form.get("prompts")
    width = request.form.get("width")
    height = request.form.get("height")
    max_iterations = request.form.get("max_iterations")

    # get the init_image from the POST request if we have one
    init_image = request.files.get("init_image")
    if init_image.filename != "":
        # make "/data/init_images" if it doesn't exist
        if not os.path.exists("/data/init_images"):
            os.mkdir("/data/init_images")
        init_image.save("/data/init_images/" + init_image.filename)
        init_image = "/data/init_images/" + init_image.filename
    elif request.form.get("clear_init_image") == "true":
        init_image = ""
    else:
        init_image = old_config["init_image"]

    # create a new config object
    config = {
        "prompts": [x.strip() for x in prompts.split(",")],
        "init_image": init_image,
        "size": [int(width), int(height)],
        "max_iterations": int(max_iterations),
    }

    # write the config to the config file
    with open("/data/config.json", "w") as f:
        json.dump(config, f)

    return redirect("/")


@web.route("/latest_output")
def latest_output():
    """
    Returns the latest output file.
    """
    if os.path.exists("/data/outputs/steps"):
        files = os.listdir("/data/outputs/steps")
        files.sort(key=lambda x: -os.path.getmtime("/data/outputs/steps/" + x))
        try:
            return send_file("/data/outputs/steps/" + files[0], mimetype="image/png")
        except IndexError:
            return "No output found"
    else:
        return "No output found"


app = Flask(__name__)
app.register_blueprint(web)

check_files_and_folders()

print("-----------------------------------------------------")
print("")
print("AI-Art by Isaac Bythewood")
print("https://github.com/overshard/ai-art")
print("")
print("Open the following in you browser to see the UI:")
print("")
print("    http://localhost:3000/")
print("")
print("-----------------------------------------------------")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
