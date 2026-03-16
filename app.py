import email

from flask import Flask, render_template, request, jsonify
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

app = Flask(__name__)

# ── GOOGLE SHEETS SETUP ───────────────────────
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_file(
    'credentials.json', scopes=SCOPES
)
gc = gspread.authorize(creds)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1pMLBCmT7gZwHJ7BkLuLSxtnKDK9RZzHI1i1FfY7xukg/edit?usp=sharing"
sheet = gc.open_by_url(SHEET_URL).worksheet("websiteData")

# ── TEXT FILE BACKUP ──────────────────────────
BACKUP_FILE = os.path.join(os.path.dirname(__file__), 'quote_requests.txt')

def save_to_file(name, phone, area, message, date):
    with open(BACKUP_FILE, 'a', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write(f"Date:     {date}\n")
        f.write(f"Name:     {name}\n")
        f.write(f"Phone:    {phone}\n")
        f.write(f"Email:    {email}\n")
        f.write(f"Borough:  {area}\n")
        f.write(f"Message:  {message}\n")
        f.write("=" * 50 + "\n\n")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-quote', methods=['POST'])
def submit_quote():
    name    = request.form.get('name', '')
    phone   = request.form.get('phone', '')
    email   = request.form.get('email', '')
    area    = request.form.get('area', '')
    message = request.form.get('message', '')
    date    = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── Save to text file first (always works)
    try:
        save_to_file(name, phone, email, area, message, date)
        print(f"✅ Saved to file: {name} - {phone}")
    except Exception as e:
        print(f"❌ File save error: {e}")

    # ── Save to Google Sheets (bonus)
    try:
        sheet.append_row([date, name, phone, email, area, message, 'New'])
        print(f"✅ Added to sheet: {name} - {phone}")
    except Exception as e:
        print(f"❌ Sheet error: {e}")

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
# Add these routes to app.py
@app.route('/robots.txt')
def robots():
    return """User-agent: *
Allow: /
Sitemap: https://jgpaints.ca/sitemap.xml""", 200, {'Content-Type': 'text/plain'}

@app.route('/sitemap.xml')
def sitemap():
    return """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://jgpaints.ca/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>""", 200, {'Content-Type': 'application/xml'}
