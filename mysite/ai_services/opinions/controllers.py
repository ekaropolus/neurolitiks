from flask import render_template, url_for, flash, redirect
from mysite import db
import speech_recognition as sr
import json
import base64
from os import path
import subprocess


def opinions(request):
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)
    return render_template('opinions/opinion.html',transcript=transcript)

