import smtplib
from email.message import EmailMessage
import datetime

# Set the sender email address, password and recipient email address
from_email_addr = "2303085802@qq.com"
from_email_pass = "nefgniwnwhiadhhi"
to_email_addr = "2303085802@qq.com"

# Define the hours at which emails need to be sent
send_times = [8, 12, 16, 20]

while True:
    # Get the current date and time
    now = datetime.datetime.now()
    current_hour = now.hour

    # Check if the current hour is one of the specified send times
    if current_hour in send_times:
        # Create an email message object
        msg = EmailMessage()

        # Set the content of the email
        body = "Hello from Raspberry Pi"
        msg.set_content(body)

        # Set the sender and recipient of the email
        msg['From'] = from_email_addr
        msg['To'] = to_email_addr

        # Set the subject of the email
        msg['Subject'] = 'TEST EMAIL'

        try:
            # Connect to the SMTP server. Here we use QQ's SMTP server and port
            server = smtplib.SMTP('smtp.qq.com', 587)

            # Start a TLS encrypted connection
            server.starttls()
            # Log in to the SMTP server
            server.login(from_email_addr, from_email_pass)

            # Send the email message
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
                # Disconnect from the SMTP server
                server.quit()
                print("Successfully disconnected from the server.")
            except NameError:
                print("Server connection was never established, no need to disconnect.")

    # Pause for a certain period (e.g., 1 minute or 60 seconds) to avoid frequent checking
    import time
    time.sleep(60)
