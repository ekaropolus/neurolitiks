# # Flask
# from flask import Flask, request, render_template, url_for, flash, redirect


# #NLP with expert.ai
# import requests
# import os
# from expertai.nlapi.cloud.client import ExpertAiClient

# #Data Science with pandas
# import pandas as pd
# import joblib

# #Front-End Forms
# from forms import public_policies_mx_metaverse as ppforms

# # from flask_wtf import CSRFProtect

# # SQL
# from flask_sqlalchemy import SQLAlchemy

# #Encryption
# from flask_bcrypt import Bcrypt

# #Login
# from flask_login import LoginManager, login_user


# #Configuration
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# # csrf = CSRFProtect(app)

# #Database
# from models import models as models



# @app.route('/')
# def index():
#     return render_template("index/index.html", tittle = 'Home')

# @app.route('/policy/', methods=['GET', 'POST'])
# def policy():
#     output = ""
#     df_pl = pd.DataFrame()
#     df_ps = pd.DataFrame()
#     if request.method == "POST":
#         os.environ["EAI_USERNAME"] = 'hi@hadox.org'
#         os.environ["EAI_PASSWORD"] = 'RYD.Lq5Et4nT4T4'
#         client = ExpertAiClient()

#         prediction = request.form.get("Policy")
#         text = prediction
#         language= 'es'
#         output = client.full_analysis(body={"document": {"text": text}}, params={'language': language})

#         fields = ['value', 'score']
#         df_lemmas = pd.DataFrame([{fn: getattr(f, fn) for fn in fields} for f in output.main_lemmas])

#         fields = ['lemma', 'score']
#         df_syncons = pd.DataFrame([{fn: getattr(f, fn) for fn in fields} for f in output.main_syncons])

#         df_politics_lemmas = pd.read_csv("/home/3karopolus/mysite/datasets/politic_lemas.csv")
#         df_politics_syncons = pd.read_csv("/home/3karopolus/mysite/datasets/politic_syncons.csv")

#         df_pl = pd.merge(df_politics_lemmas, df_lemmas, how='inner', on = 'value')
#         df_ps = pd.merge(df_politics_syncons, df_syncons, how='inner', on = 'lemma')

#     else:
#       output = ""
#     return render_template("policy/policy.html", \
#                             table_lemmas=[df_pl.to_html(classes='table table-hover table-striped table-dark', table_id = "dtHorizontalVerticalExample" )], \
#                             title_lemmas=df_pl.columns.values, \
#                             table_syncons=[df_ps.to_html(classes='table table-hover table-striped table-dark', table_id = "dtHorizontalVerticalExample" )], \
#                             title_syncons=df_ps.columns.values, \
#                             output = output, tittle = 'Crea una Política Pública')

# @app.route('/penguins/', methods=['GET', 'POST'])
# def hello_machine_learning():
#     model_path = "mysite/models/clf.pkl"
#     if request.method == "POST":
#       # Unpickle classifier
#       clf = joblib.load(model_path)
#       # Get values through input bars
#       culmen_length_mm = request.form.get("culmen_length_mm")
#       culmen_depth_mm = request.form.get("culmen_depth_mm")
#       flipper_length_mm = request.form.get("flipper_length_mm")
#       body_mass_g = request.form.get("body_mass_g")
#       # Put inputs to dataframe
#       X = pd.DataFrame([[culmen_length_mm, culmen_depth_mm,flipper_length_mm,body_mass_g]], columns = ["culmen_length_mm", "culmen_depth_mm","flipper_length_mm","body_mass_g"])
#       # Get prediction
#       prediction = clf.predict(X)[0]
#     else:
#         prediction = ""
#     return render_template("penguins/penguins.html", tittle = '¿Quién es pingüino?', output = prediction)

# @app.route('/register/', methods=['GET', 'POST'])
# def register():
#     form = ppforms.RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = models.User(username = form.username.data,
#                           email = form.email.data,
#                           password = hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash(f'Cuenta creada para el usuario {form.username.data}', 'success')
#         return redirect(url_for('login'))
#     return render_template("users/register.html", tittle = 'Registro', form = form)

# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     form = ppforms.LoginForm()
#     if form.validate_on_submit():
#         user = models.User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user,remember=form.remember.data)
#             flash('Acceso correcto', 'success')
#             return redirect(url_for('index'))
#         else:
#             flash('Acces incorrecto, verifique usuario y password', 'danger')
#     return render_template("users/login.html", tittle = 'Acceder', form = form)

