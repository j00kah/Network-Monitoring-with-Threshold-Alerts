import psutil
import smtplib
import time
from email.message import EmailMessage

# Set up thresholds (in bytes)
incoming_threshold = 500000000
outgoing_threshold = 500000000
total_threshold = incoming_threshold + outgoing_threshold

# Set up email details
email_server = "smtp.gmail.com"
email_port = 587
email_from = "jookah11@gmail.com"
email_to = "jookah@gci.net"
app_pw = 'zpssjcaqaoiafsry'
subject = 'test threshold 500000000'

# Flag to track whether an email has been sent
email_sent = False

while True:
    # Get network stats
    stats = psutil.net_io_counters()
    bytes_sent = stats.bytes_sent
    bytes_recv = stats.bytes_recv
    net_bandwidth_usage = bytes_sent + bytes_recv
    time.sleep(1)
    print(stats)

    # Check if usage exceeds thresholds set. If so, sends email to notify
    if net_bandwidth_usage > total_threshold and not email_sent:
        msg = EmailMessage()
        server = smtplib.SMTP(email_server, email_port)
        server.starttls()
        server.login(email_from, app_pw)
        message = "Network bandwidth threshold exceeded: sent={}, received={}".format(stats.bytes_sent, stats.bytes_recv)
        msg.set_content(message)
        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = email_to
        server.send_message(msg)
        server.quit()

        # Checks to see if email has been sent to prevent spamming
        email_sent = True
    elif net_bandwidth_usage < outgoing_threshold and email_sent:
        email_sent = False

