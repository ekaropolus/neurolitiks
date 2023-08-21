#Data Science with pandas
import pandas as pd
import joblib
import random

def get_penguins():
    model_path = "mysite/models/clf.pkl"
    # Unpickle classifier
    clf = joblib.load(model_path)
    # Get values through input bars
    culmen_length_mm = random.uniform(5.5, 75.5)
    culmen_depth_mm = random.uniform(5.5, 75.5)
    flipper_length_mm = random.uniform(5.5, 75.5)
    body_mass_g =random.uniform(5.5, 75.5)
    # Put inputs to dataframe
    X = pd.DataFrame([[culmen_length_mm, culmen_depth_mm,flipper_length_mm,body_mass_g]], columns = ["culmen_length_mm", "culmen_depth_mm","flipper_length_mm","body_mass_g"])
    # Get prediction
    prediction = clf.predict(X)[0]
    penguins = [
    {
        "culmen lenght": culmen_length_mm,
        "culmen depth": culmen_depth_mm,
        "flipper lenght": flipper_length_mm,
        "body mass": body_mass_g,
        "What penguin am I?": prediction
        }

    ]
    return { "penguins": penguins }