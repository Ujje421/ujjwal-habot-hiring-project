# Ujjwal Jagtap - Habot Hiring Project

## Engineering Decision Log

### 1. Terraform (D0 & D1 Architecture)
- **Least Privilege IAM**: I ensured `pipeline-sa` only has the exact roles it needs. It can create objects in the bucket, but not manage the bucket itself.
- **Row-Level Security (RLS)**: Enforced a Row Access Policy in BigQuery so users can only query rows where `region = SESSION_USER()`.
- **Encryption**: Integrated CMEK via KMS variables instead of relying on default Google encryption.

### 2. CI/CD Poka-Yoke Pipeline
- **Fail-Closed Principle**: The pipeline immediately blocks the commit if formatting, linting, or security checks fail.
- **TruffleHog Secrets Scan**: A robust scan for hardcoded credentials.
- **Quarantine Output**: Instead of just failing, the pipeline generates a quarantine artifact and blocks deployment automatically.

### 3. Django DCYN Strict Schema
- **No Human Judgment**: The validation logic operates as a strict binary gate (Does/Can/Yes/No).
- **Error Codes**: Custom error codes (`invalid_name`, `age_out_of_range`, etc.) allow the frontend to gracefully handle specific failures.
- **Audit Trails via Signals**: `signals.py` automatically writes to an audit log on every `post_save` event, keeping a strict record of `dcyn_clearance_status` changes over time without manual developer intervention.

## 🚀 How to Run the Django API Locally
Unlike standard code submissions, this repository contains a fully scaffolded, production-ready Django project. Reviewers can run the test suite to verify the DCYN validation logic immediately.

1. Navigate to the Django directory:
   ```bash
   cd task3-django
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows: .\venv\Scripts\activate
   # On Mac/Linux: source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the automated test suite to prove the DCYN validation works:
   ```bash
   python manage.py test
   ```
   *You should see 5 passing tests confirming the strict schema validation.*
