import requests
from lxml import etree
from bs4 import BeautifulSoup
from .exceptions import (RequestException, InvalidUserError,
                         ValidationFailed)
from .constants import BASE_URL


class Student:
    def __init__(self, userid, password, session, viewstate, event_validation):
        self.student_id = None
        self.student_grade = None
        self.student_name = None
        self.student_image = None
        self.student_section = None
        self.student_address = None
        self.student_email = None
        self.student_father_name = None
        self.student_mother_name = None
        self.student_phone = None

        login_data = {
            "__VIEWSTATE": viewstate,
            "__EVENTVALIDATION": event_validation,
            "ddsession": session,
            "txtusername": userid,
            "txtPass": password,
            "btnLogin": "sign+in"
        }

        try:
            request = requests.post(BASE_URL, data=login_data)
        except requests.exceptions.RequestException as e:
            raise RequestException(e)

        soup = BeautifulSoup(request._content, 'html.parser')

        if ("alert('Invalid UserID OR Password')" in str(soup.prettify())):
            raise InvalidUserError
        elif ("Validation of viewstate MAC failed" in str(
                soup.prettify()
        ) or "The state information is invalid for this page and might be corrupted."
              in str(soup.prettify())
              ) or "Invalid postback or callback argument." in str(
                  soup.prettify()):
            raise ValidationFailed

        self.student_page_dom = etree.HTML(str(soup))
        
        self.student_id = self.student_page_dom.xpath(
            '//*[@id="ContentPlaceHolder1_lblAdmno"]')[0].text
        self.student_name = self.student_page_dom.xpath(
            '//*[@id="ContentPlaceHolder1_lblStudent"]')[0].text
        self.student_image = self.student_page_dom.xpath(
            '//*[@id="ContentPlaceHolder1_stdimg"]')[0].attrib.get('src')
        self.student_grade = self.student_page_dom.xpath(
            '//*[@id="ContentPlaceHolder1_lblClass"]')[0].text
        self.student_section = self.student_page_dom.xpath(
            '//*[@id="ContentPlaceHolder1_lblSection"]')[0].text
        self.student_father_name = self.student_page_dom.xpath(
            '//*[@id="ContentPlaceHolder1_lblFatherName"]')[0].text
        self.student_mother_name = self.student_page_dom.xpath(
            '//*[@id="ContentPlaceHolder1_lblMotherName"]')[0].text
        self.student_email = self.student_page_dom.xpath(
            '//*[@id="ContentPlaceHolder1_lblEmail"]')[0].text
        self.student_phone = self.student_page_dom.xpath(
            '//*[@id="ContentPlaceHolder1_lblPhone"]')[0].text
        self.student_address = self.student_page_dom.xpath(
            '//*[@id="ContentPlaceHolder1_lblAddress"]')[0].text
            
    def get_data(self):
        student_about = {
            "address": self.student_address,
            "email": self.student_email,
            "father_name": self.student_father_name,
            "mother_name": self.student_mother_name,
            "phone": self.student_phone
        }

        student_profile = {
            "grade": self.student_grade,
            "name": self.student_name,
            "section": self.student_section
        }

        student_data = {
            "student_id": self.student_id,
            "profile": student_profile,
            "about": student_about
        }

        return student_data
