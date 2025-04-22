import smtplib
import datetime
import time
import requests
from email.message import EmailMessage

# Email configuration
from_email_addr = "2303085802@qq.com"
from_email_pass = "nefgniwnwhiadhhi"
to_email_addr = "2303085802@qq.com"

# Weather API configuration
api_key = "SCYrvkytJze9qyzOh"
location = "nanjing"

# Define email sending times
send_times = [8, 12, 16, 20]

# Record the last sending time
last_send_time = None


def get_weather_info():
    url = f"https://api.seniverse.com/v3/weather/now.json?key={api_key}&location={location}&language=en&unit=c"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather = data['results'][0]['now']
        return f"Current weather in {location}: {weather['text']}, Temperature: {weather['temperature']}°C, Humidity: {weather.get('humidity', 'N/A')}%"
    except requests.RequestException as e:
        print(f"Network error occurred while getting weather information: {e}")
    except (KeyError, IndexError):
        print("Error occurred while parsing weather data. Please check the API response.")
    return "Unable to get weather information"


def need_watering(weather_info):
    humidity_index = weather_info.find("Humidity: ")
    if humidity_index != -1:
        humidity_str = weather_info[humidity_index + len("Humidity: "):humidity_index + len("Humidity: ") + 2]
        try:
            humidity = int(humidity_str)
            return humidity < 30  # 假设湿度低于30%需要浇水
        except ValueError:
            pass
    return False


while True:
    now = datetime.datetime.now()
    current_hour = now.hour

    if current_hour in send_times and (last_send_time is None or last_send_time.hour != current_hour):
        msg = EmailMessage()

        # Get weather information
        weather_info = get_weather_info()

        # Check if watering is needed
        watering_msg = ""
        if need_watering(weather_info):
            watering_msg = "It's time to water the plants."
        else:
            watering_msg = "No need to water the plants for now."

        # Set email content
        body = f"Hello from Raspberry Pi\n\n{weather_info}\n\n{watering_msg}"
        msg.set_content(body)

        msg['From'] = from_email_addr
        msg['To'] = to_email_addr
        msg['Subject'] = 'TEST EMAIL'

        try:
            server = smtplib.SMTP('smtp.qq.com', 587)
            server.starttls()
            server.login(from_email_addr, from_email_pass)
            server.send_message(msg)
            print('Email sent successfully!')
            last_send_time = now
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
                server.quit()
                print("Successfully disconnected from the server.")
            except NameError:
                print("Server connection was never established, no need to disconnect.")

    time.sleep(60)
        
