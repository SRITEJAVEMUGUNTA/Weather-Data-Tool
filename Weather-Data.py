'''
Sriteja Vemugunta
Setup: After replacing the api_key and the password, one can access the program.
The program itself takes in user input of a location and returns the weather of the location.
The program also asks the user whether they would like to sign up for notifications and if yes at what time.
The program then emails the user's email regarding weather infromation at the afromentioned location.

Hardest part: The hardest part of the program was being able to email the user at real-time. I couldn't seem to use
the functions abaliable in the scehdule library so I hard coded a way to compare the user's time and the current time
to resolve such a issue.
'''


# Neccesary libraries for the program

from datetime import datetime
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set your WeatherStack API key here
api_key = "WEATHER_STACK_API_KEY"

def getWeather(location, noEmail):
    base_url = "http://api.weatherstack.com/current"
    params = {
        "access_key": api_key,
        "query": location
    }
    response = requests.get(base_url, params=params).json()
    
    data = response

    # Get important data
    location = data.get('location', {}).get('name', 'Unknown Location')
    temperature = data.get('current', {}).get('temperature', 'N/A')
    description = data.get('current', {}).get('weather_descriptions', ['N/A'])[0]
    humidity = data.get('current', {}).get('humidity', 'N/A')
    precipitation = data.get('current', {}).get('precip', 'N/A')
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    
    
    if noEmail:
        print(f"Current Date/Time: {current_date}\n")  # Include the current date
        print(f"Weather in {location}:\n")
        print(f"Temperature: {temperature}°C\n")
        print(f"Description: {description}\n")
        print(f"Humidity: {humidity}%\n")
        print(f"Precipitation: {precipitation} mm\n")

    else:
        email_to_user(user_email,str(f"Current Date/Time: {current_date}\n"
        f"Weather in {location}:\n"
        f"Temperature: {temperature}°C\n"
        f"Description: {description}\n"
        f"Humidity: {humidity}%\n"
        f"Precipitation: {precipitation} mm\n"))

def email_to_user(user_email, body):
    from_address = "svemugu@gmail.com"
    password = "cbss zilm lpzc nhzm"
    to_address = user_email
    subject = 'Daily Weather Report'
    msg = body

    # Create a MIMEText object to set the character encoding to UTF-8
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    # Create a plain text part of the message and set its encoding to UTF-8
    text = MIMEText(body.encode('utf-8'), 'plain', 'utf-8')
    msg.attach(text)

    # Connect to the Gmail SMTP server and send the email
    try:
        smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_object.ehlo()
        smtp_object.starttls()
        smtp_object.login(from_address, password)
        smtp_object.sendmail(from_address, to_address, msg.as_string())
        smtp_object.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Error: {e}')
def task():
    getWeather(location, False)

    
location = input("Enter the location (e.g., City, Country/State): ")
print('\n')

print(getWeather(location, True))
print('\n')

user_choice = input('Would you like to receive email notifications regarding weather changes?(yes or no): ')


if user_choice.lower() == "yes":
    user_email = input("Enter the email of the user: ")
    scheduled_send = input("When do you want to send the email (00:00): ")

    while True:
        if(int(scheduled_send.split(":")[0]) == datetime.now().hour and int(scheduled_send.split(":")[1]) == datetime.now().minute):
            task()
            break
                

else:
    print("NO EMAILS WILL BE SENT!")

    
