import time
from datetime import datetime
import bs4
from bs4 import BeautifulSoup
import requests
import twilio
from twilio.rest import Client

def get_open_sections(url):
    r = requests.get(url).text
    soup = bs4.BeautifulSoup(r, 'html.parser')
    instructor_name = soup.findAll("span", {"class": "section-instructor"})
    section_id = soup.findAll("span", {"class": "section-id"})
    open_seats = soup.findAll("span", {"class": "open-seats-count"})
    return zip(instructor_name, section_id, open_seats)

def text(body ):
    account_sid = "#"
    auth_token = "#"
    client = Client(account_sid, auth_token)
    client.messages.create(
    to="#",
    from_="#",
    body=body)


if __name__ == '__main__':
    #{"Stat":'https://app.testudo.umd.edu/soc/search?courseId=stat400&sectionId=&termId=202008&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on'
    classes = { 
    "Math240": 'https://app.testudo.umd.edu/soc/search?courseId=MATH240&sectionId=&termId=202008&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on'
    }
    message = ''
    for course in classes:
        check = get_open_sections(classes[course])
        for name, c_id, seats in check:
            name = name.text.strip()
            c_id =c_id.text.strip()
            seats = seats.text.strip()
            #print(name, c_id, seats)
            if name == "Eoin Mackall" or name =="Allan Yashinski":
                if int(seats) > 0 :
                    message += f'SECTION {c_id} PROF: {name}; {seats} SEATS OPEN!!! \n'
    if message:
        text(message)
            