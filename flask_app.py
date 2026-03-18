from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

ZOHO_TOKEN = "1000.8776274676e599d29cd3fd1927ab208e.46cf1fd7374598a12e2872d413bddf91"


# Local ATS Mock Data - self-contained
jobs_data = [
    {"id": "1", "title": "Python Developer", "location": "Pune", "status": "OPEN", "external_url": "http://example.com/job/1"},
    {"id": "2", "title": "Frontend Developer", "location": "Mumbai", "status": "OPEN", "external_url": "http://example.com/job/2"}
]

candidates_list = []
applications_list = []

def get_jobs():
    return jobs_data

def create_candidate(data):
    candidate = {
        "id": str(len(candidates_list) + 1),
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "resume_url": data.get("resume_url")
    }
    candidates_list.append(candidate)

    application = {
        "id": str(len(applications_list) + 1),
        "candidate_name": candidate["name"],
        "email": candidate["email"],
        "status": "APPLIED",
        "job_id": data.get("job_id")
    }
    applications_list.append(application)

    headers = {
        "Authorization": "Zoho-oauthtoken 1000.8776274676e599d29cd3fd1927ab208e.46cf1fd7374598a12e2872d413bddf91",
        "Content-Type": "application/json"
    }

    try:
        payload = {
            "data": [
                {
                    "First_Name": data.get("name"),
                    "Last_Name": "User",   
                    "Email": data.get("email"),
                    "Phone": data.get("phone"),
                    "Resume": data.get("resume_url")
                }
            ]
        }

        zoho_res = requests.post(
            "https://recruit.zoho.in/recruit/v2/Candidates",
            json=payload,
            headers=headers
        )

        print("Zoho Response:", zoho_res.json())

    except Exception as e:
        print("Zoho Error:", str(e))


    return {
        "message": "Candidate created & applied successfully",
        "candidate": candidate
    }

def get_applications(job_id):
    result = []
    for app in applications_list:
        if app["job_id"] == job_id:
            result.append({
                "id": app["id"],
                "candidate_name": app["candidate_name"],
                "email": app["email"],
                "status": app["status"]
            })
    return result

@app.route('/jobs', methods=['GET'])
def jobs():
    return jsonify(get_jobs())

@app.route('/candidates', methods=['GET', 'POST', 'OPTIONS'])
def candidates():
    if request.method == 'GET':
        return jsonify([candidates_list])
    if request.method == 'OPTIONS':
        return '', 200
    data = request.json
    result = create_candidate(data)
    return jsonify(result)

@app.route('/applications', methods=['GET', 'OPTIONS'])
def applications():
    if request.method == 'OPTIONS':
        return '', 200
    job_id = request.args.get('job_id')
    result = get_applications(job_id or '')
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
