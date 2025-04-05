# 🏋️‍♀️ SchedUREC

SchedUREC is a full-stack Django web application that helps James Madison University (JMU) students browse UREC group exercise classes, save their favorites, and add them to their calendar. Designed for a smooth user experience with a clean, JMU-themed interface.

---

## ✨ Features

- 🔐 Google login with Django Allauth
- 📋 View all upcoming UREC classes
- ✅ Save selected classes to “My Classes”
- ❌ Remove classes from “My Classes”
- 🗓 Add saved classes to Apple Calendar (.ics file)
- ⏰ Receive reminders 48 hours before class time
- 🔄 Live scraping of UREC class data using Selenium
- 💜 Styled with Bootstrap and JMU colors

---

## 💡 Stretch Topics (for A grade)

- 📅 iCalendar integration with .ics downloads
- ⏰ Calendar reminder automation
- 📦 Selenium-based scraping pipeline
- 🧠 Advanced per-user data storage and filtering
- 💬 Planned: Websockets for real-time calendar updates (via Django Channels)

---

## 🔧 Tech Stack

- **Backend**: Django 5 + Django Allauth
- **Database**: SQLite (for development)
- **Frontend**: HTML, CSS, Bootstrap 5
- **Scraping**: Selenium + BeautifulSoup
- **Calendar**: iCalendar (.ics file generation)
- **Authentication**: Google OAuth (via Allauth)

---

## 🛠 Local Development Setup

```bash
git clone https://github.com/347S25/final-project-rach_steph.git
cd final-project-rach_steph
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


## 🧪 Running the UREC Scraper
python manage.py scrape_urec
This fetches the latest UREC group exercise schedule from the official website and stores it in your database.


