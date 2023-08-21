import os
import json
from flask import Blueprint, render_template, flash, request, jsonify
from mysite import db
from .forms import Policy
from mysite.models.models import Post
from flask_login import current_user, login_required
from .api import get_penguins
from .config import EAI_USERNAME, EAI_PASSWORD
from . import policies
from .utils import analyze_text, read_politics_data, merge_data, agent, chat

#NLP with expert.ai
from expertai.nlapi.cloud.client import ExpertAiClient

#Data Science with pandas
import pandas as pd
import joblib

public_policies = Blueprint('public_policies',__name__)

@public_policies.route('/policy/new', methods=['GET', 'POST'])
#@login_required
def policy():
    output = ""
    form = Policy()
    df_pl = pd.DataFrame()
    df_ps = pd.DataFrame()

    if request.method == "POST": #form.validate_on_submit():
        flash('Your post has been created', 'success')
        os.environ["EAI_USERNAME"] = EAI_USERNAME
        os.environ["EAI_PASSWORD"] = EAI_PASSWORD
        client = ExpertAiClient()
        flash('Pasaste', 'info')

            # prediction = request.form.get("Policy")
        text = form.comment.data #prediction
        language= 'es'
        output = client.full_analysis(body={"document": {"text": text}}, params={'language': language})

        fields = ['value', 'score']
        df_lemmas = pd.DataFrame([{fn: getattr(f, fn) for fn in fields} for f in output.main_lemmas])

        fields = ['lemma', 'score']
        df_syncons = pd.DataFrame([{fn: getattr(f, fn) for fn in fields} for f in output.main_syncons])

        df_politics_lemmas = pd.read_csv("/home/3karopolus/mysite/datasets/politic_lemas.csv")
        df_politics_syncons = pd.read_csv("/home/3karopolus/mysite/datasets/politic_syncons.csv")

        df_pl = pd.merge(df_politics_lemmas, df_lemmas, how='inner', on = 'value')
        df_ps = pd.merge(df_politics_syncons, df_syncons, how='inner', on = 'lemma')

        post = Post(title= "Política Pública", content = form.comment.data, author = current_user, state = 'Mexico', level = 1)
        db.session.add(post)
        db.session.commit()
    elif request.method == 'GET':
           output = ""
    return render_template("policy/policy.html", \
                                table_lemmas=[df_pl.to_html(classes='table table-hover table-striped table-dark', table_id = "dtHorizontalVerticalExample")], \
                                title_lemmas=df_pl.columns.values, \
                                table_syncons=[df_ps.to_html(classes='table table-hover table-striped table-dark', table_id = "dtHorizontalVerticalExample" )], \
                                title_syncons=df_ps.columns.values, \
                                output = output, tittle = 'Crea una Política Pública',form=form)

@public_policies.route('/app/penguins/', methods=['GET', 'POST'])
def hello_machine_learning():
    model_path = "mysite/models/clf.pkl"
    if request.method == "POST":
       # Unpickle classifier
       clf = joblib.load(model_path)
       # Get values through input bars
       culmen_length_mm = request.form.get("culmen_length_mm")
       culmen_depth_mm = request.form.get("culmen_depth_mm")
       flipper_length_mm = request.form.get("flipper_length_mm")
       body_mass_g = request.form.get("body_mass_g")
       # Put inputs to dataframe
       X = pd.DataFrame([[culmen_length_mm, culmen_depth_mm,flipper_length_mm,body_mass_g]], columns = ["culmen_length_mm", "culmen_depth_mm","flipper_length_mm","body_mass_g"])
       # Get prediction
       prediction = clf.predict(X)[0]
    else:
        prediction = ""
    return render_template("penguins/penguins.html", tittle = '¿Quién es pingüino?', output = prediction)



@public_policies.get('/get/penguins/')
def api_get_penguins():
    return get_penguins()

@public_policies.route('/policy/ask/', methods=['GET', 'POST'])
def policy_view():
    try:
        output = ""
        form = Policy()
        df_pl = pd.DataFrame()
        df_ps = pd.DataFrame()
        answer = ""
        agent_response = ""

        if request.method == "POST":
            text = form.comment.data
            output = analyze_text(text)
            df_politics_lemmas, df_politics_syncons = read_politics_data()
            df_pl, df_ps = merge_data(output, df_politics_lemmas, df_politics_syncons)
            answer, agent_response = chat(form.comment.data, df_pl)

        elif request.method == 'GET':
            output = ""

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")

    return render_template("policy/ask.html",
                            table_lemmas=df_pl.to_html(),
                            table_syncons=df_ps.to_html(),
                            output=output, title='Crea una Política Pública', form=form, answer=answer, agent_response = agent_response)


@public_policies.route('/policy/responses/', methods=['GET'])
def get_responses():
    try:
        return jsonify(policies)
    except Exception as e:
        return jsonify({"error": str(e)})
