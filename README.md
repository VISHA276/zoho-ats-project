# Zoho ATS Microservice (Serverless AWS Lambda)

## Features
Python Lambda API for ATS:
- GET /jobs - List jobs
- POST /candidates - Create candidate & apply to job
- GET /applications?job_id=1 - List applications by job

Mock data (in-memory).

## Quick Start (Local)
1. `cd ats-microservice`
2. `del serverless.yml` (if corrupted)
3. Create `serverless.yml` - copy below:

```
service: ats-microservice

frameworkVersion: '4'

provider:
  name: aws
  runtime: python3.12
  region: us-east-1

plugins:
  - serverless-offline

package:
  individually: true

functions:
  jobs:
    handler: handler.jobs
    events:
      - http:
          path: jobs
          method: get
          cors: true
  candidates:
    handler: handler.candidates
    events:
      - http:
          path: candidates
          method: post
          cors: true
  applications:
    handler: handler.applications_api
    events:
      - http:
          path: applications
          method: get
          cors: true
```

4. `npm install`
5. `npx serverless offline start`

Server at http://localhost:3000

## Test
- Browser: http://localhost:3000/jobs
- POST: `curl -X POST http://localhost:3000/candidates -H "Content-Type: application/json" -d "{\"name\":\"John Doe\",\"email\":\"john@example.com\",\"phone\":\"1234567890\",\"resume_url\":\"https://resume.ex\",\"job_id\":\"1\"}"`

## Deploy
`serverless deploy` (AWS CLI configured)

## Files
- handler.py - Lambda handlers
- ats_client.py - Mock ATS data

## Frontend
Static HTML/JS dashboard in `frontend/` folder:
- View jobs, apply as candidate, see applications
- Fully responsive, vanilla JS (no build)

**Run Frontend:**
1. Open `frontend/index.html` in browser
OR
2. `npx live-server frontend/` (auto-reload, http://127.0.0.1:65050/)

**Full Stack Test:**
1. Backend: `cd ats-microservice && npx serverless offline start` (localhost:3000)
2. Frontend in browser
3. Load jobs → Apply → View applications

