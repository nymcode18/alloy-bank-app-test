# Alloy Bank Application

A web application that integrates with [Alloy's](https://www.alloy.com/) identity decisioning API to evaluate bank account applications. Applicants submit their personal information through a form, which is verified via Alloy's sandbox API, and receive an instant decision: **Approved**, **Manual Review**, or **Denied**.

## Architecture

| Layer    | Technology       | File              |
|----------|-----------------|-------------------|
| Backend  | Python / Flask   | `server.py`       |
| Frontend | HTML / CSS / JS  | `public/index.html` |
| API      | Alloy Sandbox    | `sandbox.alloy.co` |

### How It Works

1. User fills out the application form in the browser
2. Frontend sends a `POST` request to `/apply` on the Flask server
3. Server forwards the data to Alloy's `POST /v1/evaluations/` endpoint (with Basic Auth)
4. Alloy evaluates the applicant and returns an outcome
5. Server extracts the outcome and sends it back to the frontend
6. Frontend displays the result to the user

## Setup & Run

### Prerequisites
- Python 3.10+

### Installation

```bash
# Clone the repo
git clone https://github.com/nymcode18/alloy-bank-app-test.git
cd alloy-bank-app-test

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Copy the example env file and add your Alloy credentials:

```bash
cp .env.example .env
```

Edit `.env` and replace the placeholder values with your Alloy workflow token and secret:

```
ALLOY_TOKEN=your_workflow_token_here
ALLOY_SECRET=your_workflow_secret_here
```

> ⚠️ Never commit your `.env` file. It is already in `.gitignore`.

### Run

```bash
python server.py
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Testing with Sandbox Personas

Alloy's sandbox returns predictable outcomes based on the applicant's last name:

| Last Name   | Outcome        |
|-------------|----------------|
| `Smith` (or any name) | Approved       |
| `Review`    | Manual Review  |
| `Deny`      | Denied         |

## API Endpoints Used

- `POST https://sandbox.alloy.co/v1/evaluations/` — Submit an evaluation
- `GET https://sandbox.alloy.co/v1/parameters/` — Field format reference

## Form Fields

| Field                | Format             | Required |
|----------------------|-------------------|----------|
| First Name           | Text              | Yes      |
| Last Name            | Text              | Yes      |
| Email Address        | Valid email       | Yes      |
| Date of Birth        | `YYYY-MM-DD`     | Yes      |
| SSN                  | 9 digits, no dashes | Yes   |
| Address Line 1       | Text              | Yes      |
| Address Line 2       | Text              | No       |
| City                 | Text              | Yes      |
| State                | 2-letter code     | Yes      |
| ZIP Code             | 5 digits          | Yes      |
| Country              | Always `US`       | Auto     |
