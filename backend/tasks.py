import csv
import json
import os
import smtplib
import urllib.request
from email.message import EmailMessage

from flask import current_app, render_template_string

from celery_app import celery
from models.booking import Booking
from models.user import User

REPORT_TEMPLATE = """
<div style="font-family: Arial, Helvetica, sans-serif; max-width: 600px; margin: 0 auto;">
  <div style="background: linear-gradient(135deg, #2e7d32, #1b5e20); padding: 24px; border-radius: 8px 8px 0 0;">
    <h1 style="color: #ffffff; margin: 0; font-size: 22px;">🏔️ Monthly Trekking Report</h1>
  </div>

  <div style="background: #f4f9f4; padding: 20px;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td style="background: #ffffff; border-left: 4px solid #2e7d32; border-radius: 6px; padding: 14px; width: 50%;">
          <div style="color: #6b6b6b; font-size: 12px; text-transform: uppercase;">Treks Conducted</div>
          <div style="color: #2e7d32; font-size: 26px; font-weight: bold;">{{ treks_conducted }}</div>
        </td>
        <td style="width: 8px;"></td>
        <td style="background: #ffffff; border-left: 4px solid #1565c0; border-radius: 6px; padding: 14px; width: 50%;">
          <div style="color: #6b6b6b; font-size: 12px; text-transform: uppercase;">Total Treks</div>
          <div style="color: #1565c0; font-size: 26px; font-weight: bold;">{{ treks }}</div>
        </td>
      </tr>
      <tr><td colspan="3" style="height: 8px;"></td></tr>
      <tr>
        <td style="background: #ffffff; border-left: 4px solid #e65100; border-radius: 6px; padding: 14px;">
          <div style="color: #6b6b6b; font-size: 12px; text-transform: uppercase;">Staff</div>
          <div style="color: #e65100; font-size: 26px; font-weight: bold;">{{ staff }}</div>
        </td>
        <td></td>
        <td style="background: #ffffff; border-left: 4px solid #6a1b9a; border-radius: 6px; padding: 14px;">
          <div style="color: #6b6b6b; font-size: 12px; text-transform: uppercase;">Trekkers</div>
          <div style="color: #6a1b9a; font-size: 26px; font-weight: bold;">{{ trekkers }}</div>
        </td>
      </tr>
    </table>

    <div style="background: #ffffff; border-radius: 6px; padding: 14px; margin-top: 12px;">
      <div style="color: #6b6b6b; font-size: 12px; text-transform: uppercase;">Total Bookings</div>
      <div style="color: #c62828; font-size: 26px; font-weight: bold;">{{ bookings }}</div>
    </div>
  </div>

  <div style="background: #ffffff; padding: 20px; border-radius: 0 0 8px 8px; border: 1px solid #e0e0e0; border-top: none;">
    <h2 style="color: #1b5e20; font-size: 16px; border-bottom: 2px solid #2e7d32; padding-bottom: 8px;">
      🔥 Popular Treks
    </h2>
    <table width="100%" cellpadding="0" cellspacing="0">
      {% for name, count in popular_treks %}
      <tr>
        <td style="padding: 8px 0; border-bottom: 1px solid #f0f0f0; color: #333;">{{ loop.index }}. {{ name }}</td>
        <td style="padding: 8px 0; border-bottom: 1px solid #f0f0f0; text-align: right;">
          <span style="background: #e8f5e9; color: #2e7d32; padding: 2px 10px; border-radius: 12px; font-size: 13px; font-weight: bold;">
            {{ count }} booking{{ 's' if count != 1 else '' }}
          </span>
        </td>
      </tr>
      {% else %}
      <tr><td style="color: #999; padding: 8px 0;">No bookings yet</td></tr>
      {% endfor %}
    </table>
  </div>
</div>
"""


def send_email(to, subject, body):
    server = current_app.config["MAIL_SERVER"]
    if not server:
        print(f"[email suppressed] to={to} subject={subject}\n{body}")
        return

    msg = EmailMessage()
    msg["From"] = current_app.config["MAIL_FROM"]
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body, subtype="html")
    with smtplib.SMTP(server, current_app.config["MAIL_PORT"]) as smtp:
        smtp.starttls()
        smtp.login(current_app.config["MAIL_USERNAME"], current_app.config["MAIL_PASSWORD"])
        smtp.send_message(msg)


def send_gchat_message(text):
    webhook_url = current_app.config["GCHAT_WEBHOOK_URL"]
    if not webhook_url:
        print(f"[gchat suppressed] {text}")
        return

    req = urllib.request.Request(
        webhook_url,
        data=json.dumps({"text": text}).encode(),
        headers={"Content-Type": "application/json; charset=UTF-8"},
    )
    urllib.request.urlopen(req, timeout=10)


@celery.task(name="tasks.send_daily_reminders")
def send_daily_reminders():
    bookings = Booking.query.filter_by(status="Booked").all()
    sent = 0
    for b in bookings:
        if b.trek.status != "Open":
            continue
        send_email(
            b.user.email,
            f"Reminder: your trek '{b.trek.name}' is coming up",
            f"<p>Hi {b.user.name}, this is a reminder about your upcoming trek "
            f"<strong>{b.trek.name}</strong> in {b.trek.location}.</p>",
        )
        send_gchat_message(
            f"Reminder: {b.user.name}, your trek *{b.trek.name}* in {b.trek.location} is coming up."
        )
        sent += 1
    return sent


@celery.task(name="tasks.generate_monthly_report")
def generate_monthly_report():
    from sqlalchemy import func

    from models.trek import Trek

    popular_treks = (
        Trek.query.join(Booking)
        .with_entities(Trek.name, func.count(Booking.id).label("count"))
        .group_by(Trek.id)
        .order_by(func.count(Booking.id).desc())
        .limit(5)
        .all()
    )

    stats = {
        "treks": Trek.query.count(),
        "treks_conducted": Trek.query.filter_by(status="Completed").count(),
        "staff": User.query.filter_by(role="staff").count(),
        "trekkers": User.query.filter_by(role="trekker").count(),
        "bookings": Booking.query.count(),
        "popular_treks": popular_treks,
    }
    html = render_template_string(REPORT_TEMPLATE, **stats)
    send_email(current_app.config["ADMIN_EMAIL"], "Monthly Trekking Report", html)
    return {k: v for k, v in stats.items() if k != "popular_treks"}


@celery.task(name="tasks.export_booking_history_csv", bind=True)
def export_booking_history_csv(self, user_id):
    os.makedirs(current_app.config["EXPORT_DIR"], exist_ok=True)
    path = os.path.join(current_app.config["EXPORT_DIR"], f"booking_history_{user_id}_{self.request.id}.csv")

    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.booked_at.desc()).all()
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "trek_name", "location", "status", "booked_at"])
        for b in bookings:
            writer.writerow([b.user_id, b.trek.name, b.trek.location, b.status, b.booked_at.isoformat()])

    return path
