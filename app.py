import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/home/")
def index():
    return render_template("index.html")

@app.route("/unit/<unit>/<section>/", methods=("GET", "POST"))
def unit(unit, section):
    topic = "Write a short overview of AP Physics Unit {} Section {}".format(unit, section)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=topic,
        max_tokens=1000,
        temperature=0,
    )
    overview = response.choices[0].text
    topic = "Write 3 example problems for AP Physics Unit {} Section {} in an html table with solutions".format(unit, section)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=topic,
        max_tokens=1000,
        temperature=0,
    )
    examples = response.choices[0].text
    return render_template("unit.html", overview=overview, unit=unit, section=section, examples=examples)


def generatePrompt(topic):
    return """

Instruction: Give me a question and answer off a past AP Physics 1 algebra based exam to test my knowledge of {}. 
Provide response in three parts: Question, Answer, and Explanation


""".format(
        topic
    )

@app.route("/", methods=("GET", "POST"))
def problems():
    if request.method == "POST":
        topic = request.form["topic"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generatePrompt(topic),
            max_tokens=1000,
            temperature=0,
        )
        generatedText = response.choices[0].text
        question = generatedText
        answer = ""
        explanation = ""
        if "answer" in generatedText.lower():
            s = generatedText.split("Answer:", 1)
            question = s[0]
            answer = s[1]
            if "explanation" in answer.lower():
                s = answer.split("Explanation:", 1)
                answer = s[0]
                explanation = s[1]
        return redirect(url_for("problems", question=question, answer=answer, explanation=explanation))
    question = request.args.get("question")
    answer = request.args.get("answer")
    explanation = request.args.get("explanation")
    return render_template("problems.html", question=question, answer=answer, explanation=explanation)
