from app.config import (
    WEB_PASSWORD,
    WEB_PAGE_TITLE,
    WEB_APP_SESSION_MAX_LIFETIME,
    WEB_PUBLIC_ENABLED,
    WEB_WELCOME_MESSAGE_CONTENT,
    WEB_CUSTOM_BACKGROUND,
    CRON_MINUTE, 
    CRON_HOUR, 
    CRON_DAY, 
    CRON_MONTH, 
    CRON_DAY_OF_WEEK,
    VERSION,
    DEBUG
)
from app.generate_keys import (
    generate_password, 
    calculate_psk
)
from app.services import (
    set_new_password, 
    get_current_password, 
    get_ssid
)
from flask import (
    Flask, 
    request, 
    render_template, 
    redirect, 
    url_for, 
    session,
    g
)
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import timedelta

import qrcode
import io
import base64
import secrets
import logging

if not DEBUG:
    logging.getLogger("apscheduler.scheduler").setLevel(logging.CRITICAL + 1)
    logging.getLogger("apscheduler.executors.default").setLevel(logging.CRITICAL + 1)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes = WEB_APP_SESSION_MAX_LIFETIME)

current_password = get_current_password()
ssid = None

app.logger.info(f"Initial password loaded: {current_password}")

def fetch_current_credentials():

    global current_password
    global ssid

    pw_temp = get_current_password()

    if pw_temp == current_password:
        app.logger.debug(f"Password didn't change from other source: {current_password}")
    else:
        current_password = pw_temp
        app.logger.debug(f"Password changed from other source: {current_password}")
        
    ssid = get_ssid()

def update_password():

    global current_password
    app.logger.info("Password is updated...")

    new_password = generate_password()
    new_psk = calculate_psk(new_password, ssid)

    set_new_password(new_psk, new_password)

    current_password = new_password
    app.logger.info(f"New password set: {current_password}")

def render_qr():

    global current_password
    wifi_data = f"WIFI:S:{ssid};T:WPA;P:{current_password};H:false;"

    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size = 10,
        border = 4,
    )
    qr.add_data(wifi_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color = "black", back_color = "white")
    buffer = io.BytesIO()
    img.save(buffer, format = "PNG")
    buffer.seek(0)

    return base64.b64encode(buffer.getvalue()).decode()

def render_page(page_name, customWelcomeMsg):

    return render_template(
        page_name, 
        qr_code = render_qr(), 
        password = current_password, 
        WLAN_SSID = ssid, 
        WEB_PAGE_TITLE = WEB_PAGE_TITLE, 
        WEB_WELCOME_MESSAGE_CONTENT = customWelcomeMsg, 
        WEB_CUSTOM_BACKGROUND = WEB_CUSTOM_BACKGROUND,
        VERSION = VERSION
    )

@app.before_request
def check_session():

    g.user_ip = request.remote_addr

    if "authenticated" not in session and request.endpoint not in [
        "login",
        "static",
        "public",
        "public_disabled"
    ]:

        return redirect(url_for("login"))

@app.route("/", methods = ["GET", "POST"])
def login():

    if request.method == "POST":
        entered_password = request.form.get("password")

        if entered_password == WEB_PASSWORD:
            session["authenticated"] = True
            session.permanent = True
            app.logger.info(f"{g.user_ip} - Successfully logged in")

            return redirect(url_for("admin"))
        
        else:
            app.logger.warning(f"{g.user_ip} - Failed login attempt")

            return render_template("login.html", WEB_PAGE_TITLE = WEB_PAGE_TITLE, error = "Wrong password!", WEB_CUSTOM_BACKGROUND = WEB_CUSTOM_BACKGROUND, VERSION = VERSION)
        
    return render_template("login.html", WEB_PAGE_TITLE = WEB_PAGE_TITLE, WEB_CUSTOM_BACKGROUND = WEB_CUSTOM_BACKGROUND, VERSION = VERSION)

@app.route("/admin")
def admin():

    if not session.get("authenticated"):
        return redirect(url_for("login"))

    return render_page("admin.html", "")

@app.route("/public")
def public():

    if not WEB_PUBLIC_ENABLED:
        return redirect(url_for("public_disabled"))
    
    return render_page("public.html", WEB_WELCOME_MESSAGE_CONTENT)

@app.route("/update-password", methods=["POST"])
def trigger_update_password():

    app.logger.info(f"Password update maually triggered by {g.user_ip}")
    update_password()

    return redirect(url_for("admin"))

@app.route("/logout")
def logout():

    session.pop("authenticated", None)
    app.logger.info(f"{g.user_ip} - Successfully logged out")

    return redirect(url_for("login"))

@app.route("/public_disabled")
def public_disabled():
    
    app.logger.info(f"{g.user_ip} - Public page disabled")

    return render_template("public_disabled.html")

scheduler = BackgroundScheduler()

def start_scheduler():

    fetch_current_credentials()

    scheduler.add_job(
        update_password,
        CronTrigger(
            minute = CRON_MINUTE,
            hour = CRON_HOUR,
            day = CRON_DAY,
            month = CRON_MONTH,
            day_of_week = CRON_DAY_OF_WEEK
        )
    )
    scheduler.add_job(
        fetch_current_credentials,
        IntervalTrigger(minutes = 5)
    )
    scheduler.start()

start_scheduler()