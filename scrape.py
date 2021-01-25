import time
from datetime import datetime
import bs4
from bs4 import BeautifulSoup
import requests
import twilio
from twilio.rest import Client
import pickle

def get_open_sections(url):
    r = requests.get(url).text
    soup = bs4.BeautifulSoup(r, "html.parser")
    instructor_name = soup.findAll("span", {"class": "section-instructor"})
    section_id = soup.findAll("span", {"class": "section-id"})
    open_seats = soup.findAll("span", {"class": "open-seats-count"})
    return zip(instructor_name, section_id, open_seats)


def text(body):
    account_sid = "ACef4e810916850ca7e12a626e3aa23da8"
    auth_token = "e7f7bb7c77c78a66de0fa9c9a85c2e4a"
    client = Client(account_sid, auth_token)
    client.messages.create(to="17322087157", from_="17609144209", body=body)


if __name__ == "__main__":
    classes = {
        "CMSC351":
       "https://app.testudo.umd.edu/soc/search?courseId=CMSC351&sectionId=&termId=202101&_openSectionsOnly=on&creditCompare=%3E%3D&credits=0.0&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on",
       "MATH241":
       "https://app.testudo.umd.edu/soc/search?courseId=Math241&sectionId=&termId=202101&_openSectionsOnly=on&creditCompare=%3E%3D&credits=0.0&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on"
    }
    message = ""
    professors = ["Justin Wyss-Gallifent", "Terence Long"]
    for course in classes:
        check = get_open_sections(classes[course])
        for name, c_id, seats in check:
            name = name.text.strip()
            c_id = c_id.text.strip()
            seats = seats.text.strip()
            if name in professors:
                if int(seats) > 0:
                    message += f"{course}; section {c_id} with {name}: {seats} seat\n"
    try:
        log = pickle.load(open("log.p", "rb"))
    except:
        log = None
    if message and log != message:
        text(message)
    pickle.dump(message, open("log.p", "wb"))

  