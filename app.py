from datetime import datetime
import os

from flask import Flask, jsonify, render_template, request
import gspread
from google.oauth2.service_account import Credentials


app = Flask(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
SHEET_URL = "https://docs.google.com/spreadsheets/d/1pMLBCmT7gZwHJ7BkLuLSxtnKDK9RZzHI1i1FfY7xukg/edit?usp=sharing"
BACKUP_FILE = os.path.join(os.path.dirname(__file__), "quote_requests.txt")


def connect_sheet():
    try:
        creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
        client = gspread.authorize(creds)
        return client.open_by_url(SHEET_URL).worksheet("websiteData")
    except Exception as exc:
        print(f"Sheet connection unavailable: {exc}")
        return None


sheet = connect_sheet()


def clean(value):
    return (value or "").strip()


def save_to_file(record):
    with open(BACKUP_FILE, "a", encoding="utf-8") as file_obj:
        file_obj.write("=" * 60 + "\n")
        file_obj.write(f"Date:         {record['date']}\n")
        file_obj.write(f"Locale:       {record['locale']}\n")
        file_obj.write(f"Name:         {record['name']}\n")
        file_obj.write(f"Phone:        {record['phone']}\n")
        file_obj.write(f"Email:        {record['email']}\n")
        file_obj.write(f"Area:         {record['area']}\n")
        file_obj.write(f"Service Type: {record['service_type']}\n")
        file_obj.write(f"Project Size: {record['project_size']}\n")
        file_obj.write(f"Timeline:     {record['timeline']}\n")
        file_obj.write(f"Budget:       {record['budget']}\n")
        file_obj.write(f"Message:      {record['message']}\n")
        file_obj.write("=" * 60 + "\n\n")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/fr")
def home_fr():
    return render_template("index_fr.html")


@app.route("/submit-quote", methods=["POST"])
def submit_quote():
    company = clean(request.form.get("company"))
    form_loaded_at = clean(request.form.get("form_loaded_at"))

    if company:
        return jsonify({"status": "ignored"}), 200

    try:
        loaded_ts = int(form_loaded_at)
        if int(datetime.now().timestamp() * 1000) - loaded_ts < 3000:
            return jsonify({"status": "ignored"}), 200
    except ValueError:
        return jsonify({"status": "invalid"}), 400

    record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "locale": clean(request.form.get("locale", "en")),
        "name": clean(request.form.get("name")),
        "phone": clean(request.form.get("phone")),
        "email": clean(request.form.get("email")),
        "area": clean(request.form.get("area")),
        "service_type": clean(request.form.get("service_type")),
        "project_size": clean(request.form.get("project_size")),
        "timeline": clean(request.form.get("timeline")),
        "budget": clean(request.form.get("budget")),
        "message": clean(request.form.get("message")),
    }

    required = ["name", "phone", "area", "service_type", "project_size", "timeline", "budget"]
    if any(not record[field] for field in required):
        return jsonify({"status": "invalid", "error": "missing required fields"}), 400

    try:
        save_to_file(record)
        print(f"Saved backup quote: {record['name']} ({record['phone']})")
    except Exception as exc:
        print(f"File save error: {exc}")

    if sheet is not None:
        try:
            sheet.append_row(
                [
                    record["date"],
                    record["locale"],
                    record["name"],
                    record["phone"],
                    record["email"],
                    record["area"],
                    record["service_type"],
                    record["project_size"],
                    record["timeline"],
                    record["budget"],
                    record["message"],
                    "New",
                ]
            )
            print(f"Saved sheet quote: {record['name']} ({record['phone']})")
        except Exception as exc:
            print(f"Sheet save error: {exc}")

    return jsonify({"status": "success"}), 200


@app.route("/robots.txt")
def robots():
    return (
        "User-agent: *\nAllow: /\nSitemap: https://abbottmaintenance.ca/sitemap.xml",
        200,
        {"Content-Type": "text/plain"},
    )


@app.route("/sitemap.xml")
def sitemap():
    return (
        """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <url>
    <loc>https://abbottmaintenance.ca/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://abbottmaintenance.ca/fr</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>""",
        200,
        {"Content-Type": "application/xml"},
    )


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
