from flask import Blueprint, render_template, request, jsonify, current_app, url_for
from .utils import analyze_text, read_politics_data, merge_data, chat, query_policy_neurolitiks, query_policy_web, mongo_policy
from . import policies
import pandas as pd
import uuid  # Import the uuid module
from bson.objectid import ObjectId

public_policies = Blueprint('public_policies', __name__)



@public_policies.route('/policy/query/neurolitiks/', methods=['GET'])
def policy_query_neurolitiks_response():
    """
    Handle queries to Neurolitiks and return a JSON response.
    """

    try:
        query = request.args.get('query', '')
        df_pl = pd.DataFrame()
        df_ps = pd.DataFrame()
        output = analyze_text(query)
        df_politics_lemmas, df_politics_syncons = read_politics_data()
        df_pl, df_ps = merge_data(output, df_politics_lemmas, df_politics_syncons)
        response = query_policy_neurolitiks(query)
        answer, agent_response = chat(query, df_pl)

        # Generate a UUID as the call_id
        call_id = str(uuid.uuid4())

        # Convert df_pl and df_ps to dictionaries
        df_pl_dict = df_pl.to_dict(orient='records')
        df_ps_dict = df_ps.to_dict(orient='records')


        # Save the response, answer, and agent_response, as well as df_pl and df_ps in the policies dictionary
        policies[call_id] = {
            "query": query,
            "response": response,
            "answer": answer,
            "agent_response": agent_response,
            "lemmas": df_pl_dict,
            "syncons": df_ps_dict
        }

        # Insert the document into the MongoDB collection
        result = current_app.mongo_policies.policies.insert_one(policies[call_id])

        # Retrieve the _id from the inserted document
        policy_id = str(result.inserted_id)

        return jsonify({"policy_id": policy_id})
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)})


@public_policies.route('/policy/query/web/', methods=['GET'])
def policy_query_web_response():
    """
    Handle queries to the web and return a JSON response.
    """
    try:
        query = request.args.get('query', '')
        response = query_policy_web(query)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)})

@public_policies.route('/policy/TrueLens/monitor/')
def truelens():
    """
    Placeholder for monitoring - should be updated to return a meaningful response.
    """
    return jsonify({"message": "Monitoring functionality not implemented yet."})

@public_policies.route('/policy/policies/', methods=['GET'])
def get_responses():
    """
    Get policy responses and return them as JSON.
    """
    try:
        return jsonify(policies)
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to get the query for a specific policy_id from MongoDB
@public_policies.route('/policy/query/<string:policy_id>/query/', methods=['GET'])
def get_query(policy_id):
    try:
        # Find the policy by policy_id in MongoDB
        policy = current_app.mongo_policies.policies.find_one({"_id": ObjectId(policy_id)})
        if policy:
            return jsonify({"policy_id": policy_id, "query": policy.get("query")})
        else:
            return jsonify({"error": "Policy ID not found"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to get the response for a specific policy_id from MongoDB
@public_policies.route('/policy/query/<string:policy_id>/response/', methods=['GET'])
def get_response(policy_id):
    try:
        # Find the policy by policy_id in MongoDB
        policy = current_app.mongo_policies.policies.find_one({"_id": ObjectId(policy_id)})
        if policy:
            return jsonify({"policy_id": policy_id, "response": policy.get("response")})
        else:
            return jsonify({"error": "Policy ID not found"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to get the response for a specific policy_id from MongoDB
@public_policies.route('/policy/query/<string:policy_id>/agent_response/', methods=['GET'])
def get_agent_response(policy_id):
    try:
        # Find the policy by policy_id in MongoDB
        policy = current_app.mongo_policies.policies.find_one({"_id": ObjectId(policy_id)})
        if policy:
            return jsonify({"policy_id": policy_id, "agent_response": policy.get("agent_response")})
        else:
            return jsonify({"error": "Policy ID not found"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to get the answer for a specific policy_id from MongoDB
@public_policies.route('/policy/query/<string:policy_id>/answer/', methods=['GET'])
def get_answer(policy_id):
    try:
        # Find the policy by policy_id in MongoDB
        policy = current_app.mongo_policies.policies.find_one({"_id": ObjectId(policy_id)})
        if policy:
            return jsonify({"policy_id": policy_id, "answer": policy.get("answer")})
        else:
            return jsonify({"error": "Policy ID not found"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to get the lemmas for a specific policy_id from MongoDB
@public_policies.route('/policy/query/<string:policy_id>/lemmas/', methods=['GET'])
def get_lemmas(policy_id):
    try:
        # Find the policy by policy_id in MongoDB
        policy = current_app.mongo_policies.policies.find_one({"_id": ObjectId(policy_id)})
        if policy:
            return jsonify({"policy_id": policy_id, "lemmas": policy.get("lemmas")})
        else:
            return jsonify({"error": "Policy ID not found"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to get the syncoms for a specific policy_id from MongoDB
@public_policies.route('/policy/query/<string:policy_id>/syncons/', methods=['GET'])
def get_syncoms(policy_id):
    try:
        # Find the policy by policy_id in MongoDB
        policy = current_app.mongo_policies.policies.find_one({"_id": ObjectId(policy_id)})
        if policy:
            return jsonify({"policy_id": policy_id, "syncons": policy.get("syncons")})
        else:
            return jsonify({"error": "Policy ID not found"})
    except Exception as e:
        return jsonify({"error": str(e)})


# Route to list all available endpoints
@public_policies.route('/policy/available-endpoints/', methods=['GET'])
def list_available_endpoints():
    try:
        endpoints = {}

        # Iterate through the registered routes and add their URLs to the endpoints dictionary
        for rule in current_app.url_map.iter_rules():
            if rule.endpoint.startswith('public_policies.get_'):
                endpoint_name = rule.endpoint.split('public_policies.get_')[1]
                endpoints[endpoint_name] = url_for(rule.endpoint, call_id='<call_id>')

        return jsonify(endpoints)
    except Exception as e:
        return jsonify({"error": str(e)})

@public_policies.route('/policy/dashboard/', methods=['GET', 'POST'])
def policy_dashboard():
    """
    Render the policy dashboard template.
    """
    return render_template("policy/dashboard.html")

@public_policies.route('/policy/query/mongo/<policy_id>', methods=['GET'])
def get_policy_from_mongo(policy_id):
    try:
        # Get the policy by the specified ID
        policy = current_app.mongo_policies.policies.find_one({"_id": ObjectId(policy_id)})
        if policy:
            # Convert ObjectId to a string for JSON serialization
            policy["_id"] = str(policy["_id"])
            return jsonify(policy)
        else:
            return jsonify({"message": f"No policy found with ID: {policy_id}"})
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)})

@public_policies.route('/policy/query/mongo/last', methods=['GET'])
def get_last_policy_from_mongo():
    try:
        # Get the last policy if policy_id is -1
        last_policy = current_app.mongo_policies.policies.find_one(sort=[("_id", -1)])
        if last_policy:
            # Convert ObjectId to a string for JSON serialization
            last_policy["_id"] = str(last_policy["_id"])
            return jsonify(last_policy)
        else:
            return jsonify({"message": "No policies found in MongoDB."})
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)})

