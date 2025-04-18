import smtplib
from email.message import EmailMessage

# Set the sender email and password and recipient email
from_email_addr = "2303085802@qq.com"
from_email_pass = "nefgniwnwhiadhhi"
to_email_addr = "2303085802@qq.com"

# Create a message object
msg = EmailMessage()

# Set the email body
body = "Hello from Raspberry Pi"
msg.set_content(body)

# Set sender and recipient
msg['From'] = from_email_addr
msg['To'] = to_email_addr

# Set your email subject
msg['Subject'] = 'TEST EMAIL'

try:
    # Connecting to server and sending email
    # Edit the following line with your provider's SMTP server details
    server = smtplib.SMTP('smtp.qq.com', 587)

    # Comment out the next line if your email provider doesn't use TLS
    server.starttls()
    # login to the SMTP server
    server.login(from_email_addr, from_email_pass)

    # Send the message
    server.send_message(msg)
    print('Email sent successfully!')

except smtplib.SMTPAuthenticationError:
    print("Authentication failed. Please check your email address and password.")
except smtplib.SMTPConnectError:
    print("Could not connect to the SMTP server. Please check your network connection.")
except smtplib.SMTPException as e:
    print(f"An SMTP error occurred: {str(e)}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
finally:
    try:
        # Disconnect from the Server
        server.quit()
        print("Successfully disconnected from the server.")
    except NameError:
        print("Server connection was never established, no need to disconnect.")
