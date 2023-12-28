import os
import json
from flask import Blueprint, render_template, flash, request, jsonify
# from mysite import db
from .forms import Policy
# from mysite.models.models import Post
# from flask_login import current_user, login_required
from .api import get_penguins
from .config import EAI_USERNAME, EAI_PASSWORD
from . import policies
from .utils import analyze_text, read_politics_data, merge_data, agent, chat, query_policy_neurolitiks, query_policy_web
import logging

# Imports main tools:
from trulens_eval import Feedback, OpenAI as fOpenAI, Tru
tru = Tru()
tru.reset_database()

from trulens_eval import TruBasicApp

#NLP with expert.ai
from expertai.nlapi.cloud.client import ExpertAiClient

#Data Science with pandas
import pandas as pd
import joblib

public_policies = Blueprint('public_policies',__name__)


@public_policies.route('/policy/dashboard/', methods=['GET', 'POST'])
def policy_view():
    try:
        output = ""
        form = Policy()
        df_pl = pd.DataFrame()
        df_ps = pd.DataFrame()
        answer = ""
        agent_response = ""
        # Initialize OpenAI-based feedback function collection class:
        # fopenai = fOpenAI()

        # Define a relevance function from openai
        # f_relevance = Feedback(fopenai.relevance).on_input_output()
        # tru_llm_standalone_recorder = TruBasicApp(chat, app_id="Neurolitiks", feedbacks=[f_relevance])

        if request.method == "POST":
            text = form.comment.data
            output = analyze_text(text)
            df_politics_lemmas, df_politics_syncons = read_politics_data()
            df_pl, df_ps = merge_data(output, df_politics_lemmas, df_politics_syncons)
            #with tru_llm_standalone_recorder as recording:
                #answer, agent_response = tru_llm_standalone_recorder.app(form.comment.data, df_pl)
            answer, agent_response = chat(form.comment.data, df_pl)

        elif request.method == 'GET':
            output = ""

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")

    return render_template("policy/ask.html",
                            table_lemmas=df_pl.to_html(),
                            table_syncons=df_ps.to_html(),
                            output=output, title='Crea una Política Pública', form=form, answer=answer, agent_response = agent_response)




@public_policies.route('/policy/query/neurolitiks/', methods=['GET'])
def policy_query_neurolitiks_response():
    query = request.args.get('query', '')
    df_pl = pd.DataFrame()
    df_ps = pd.DataFrame()
    # Get the city response based on the query
    output = analyze_text(query)
    df_politics_lemmas, df_politics_syncons = read_politics_data()
    df_pl, df_ps = merge_data(output, df_politics_lemmas, df_politics_syncons)
    response = query_policy_neurolitiks(query)
    answer, agent_response = chat(form.comment.data, df_pl)
    return jsonify(response)

@public_policies.route('/policy/query/web/', methods=['GET'])
def policy_query_web_response():
    query = request.args.get('query', '')
    # Get the city response based on the query
    response = query_policy_web(query)
    return jsonify(response)

@public_policies.route('/policy/TrueLens/monitor/')
def truelens():
    return render_template('policy/monitor.html', dataframe=tru.get_records_and_feedback(app_ids=[])[0].to_html(index=False))

@public_policies.route('/policy/responses/', methods=['GET'])
def get_responses():
    try:
        return jsonify(policies)
    except Exception as e:
        return jsonify({"error": str(e)})
