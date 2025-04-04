from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from base_347_example.urec.models import Class  # adjust to match your import path
import time

WEEKDAYS = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}

class Command(BaseCommand):
    help = "Scrapes the JMU UREC class schedule and loads into the database"

    def handle(self, *args, **options):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)

        try:
            self.stdout.write("📥 Fetching UREC schedule...")
            driver.get("https://www.jmu.edu/recreation/activities/group-exercise/index.shtml")
            time.sleep(5)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            table = soup.find("table", {"id": "DataTables_Table_0"})

            if not table:
                self.stderr.write("❌ Could not find class table.")
                return

            rows = table.find("tbody").find_all("tr")
            Class.objects.all().delete()

            today = datetime.today()

            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 5:
                    weekday_str = cols[0].text.strip()
                    start_time = cols[1].text.strip()
                    end_time = cols[2].text.strip()
                    name = cols[3].text.strip()
                    location = cols[4].text.strip()
                    time_range = f"{start_time} - {end_time}"

                    # Calculate next occurrence of the weekday
                    class_weekday = WEEKDAYS.get(weekday_str)
                    if class_weekday is None:
                        continue

                    days_ahead = (class_weekday - today.weekday() + 7) % 7
                    class_date = today + timedelta(days=days_ahead)
                    class_start_datetime = datetime.strptime(f"{class_date.date()} {start_time}", "%Y-%m-%d %I:%M %p")

                    # 48 hours before the class
                    deadline = class_start_datetime - timedelta(hours=48)

                    Class.objects.create(
                        name=name,
                        time=time_range,
                        location=location,
                        registration_deadline=deadline,
                        date=class_date.date(),
                    )

            self.stdout.write(self.style.SUCCESS(f"✅ Loaded {len(rows)} classes from UREC."))
        finally:
            driver.quit()
