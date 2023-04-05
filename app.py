import os
import json
import openai
from flask import Flask, redirect, render_template, request, url_for
import samples

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")



@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        resource = request.form["resource"]
        prefix = request.form["prefix"]
        print(generate_prompt(resource,prefix))
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(resource, prefix),
            max_tokens=1000,
            temperature=0.6,
        )
        json_response = json.dumps(response.choices[0].text, sort_keys = False, indent = 2)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(resources, prefix):
    return """Generate sample Terraform code to deploy cloud resource

{}
{}

Resource: {}
Name Prefix: {}
Terraform:""".format(
        samples.storage_sample,
        samples.cosmos_sample,
        resources,
        prefix
    )
