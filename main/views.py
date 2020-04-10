# coding=utf-8
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings
from django.http.response import JsonResponse
import os
import json
import urllib.parse as pr
from .models import Sms
import re
import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException
import ast

configuration = clicksend_client.Configuration()
configuration.username = os.getenv("CLICK_SEND_USERNAME")
configuration.password = os.getenv("CLICK_SEND_PASSWORD")
api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))


def cancel_sms_by_project_id(project_id):
    sms_results = Sms.objects.filter(project_id=project_id)
    for sms in sms_results:
        try:
            print("Canceling SMS with project ID: {}, Message ID: {}".format(project_id, sms.message_id))
            api_instance.sms_cancel_by_message_id_put(sms.message_id)
        except ApiException as e:
            print("Error canceling SMS: {}".format(e))


# {"number": number,
#  "message_body": message_body,
#  "schedule": schedule,
#  "project_id": project_id
#  }
@csrf_exempt
def send_sms(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        print("Sending SMS: {}".format(data))

        sms_message = SmsMessage(source="api",
                                 body=data["message_body"],
                                 to="+972{}".format(data["number"]),
                                 schedule=data["schedule"])
        sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])

        try:
            api_response = ast.literal_eval(api_instance.sms_send_post(sms_messages))
            # save sms only if it is scheduled and we have project_id
            if data["project_id"] and data["schedule"]:
                # first cancel any scheduled messages for this project_id
                cancel_sms_by_project_id(data["project_id"])
                # now save new scheduled sms
                message_id = api_response["data"]["messages"][0]["message_id"]
                Sms(number=data["number"], message_id=message_id, project_id=data["project_id"]).save()
        except ApiException as e:
            print("Exception when calling SMSApi->sms_send_post: {}\n".format(e))
        return HttpResponse("")


@csrf_exempt
def cancel_sms(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        project_id = data["project_id"]
        cancel_sms_by_project_id(project_id)
        return HttpResponse("")


def index(request):
    # https: // bootsnipp.com / snippets / ZXKKD
    return render(request, "main/index.html")


def login():
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = {}
    try:
        json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")
        creds_dict = json.loads(json_creds)
    except:
        file_path = os.path.join(os.path.dirname(settings.BASE_DIR), "client-secret.json")
        print(file_path)
        with open(file_path) as f:
            creds_dict = json.load(f)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    client = gspread.authorize(creds)
    return client


# https://gspread.readthedocs.io/en/latest/api.html#gspread.models.Worksheet.duplicate
def create_sheet(request):
    client = login()
    sh = client.create("coronaap spreadsheet")
    sh.share("aviadm24@gmail.com", perm_type="user", role="writer")
    return render(request, "main/index.html")


def copy_sheet(request):
    client = login()
    sh = client.copy("18fUM43kYh4Ac6kgNItlSKJbbjKhIoSCMGYqTCWqGUzk", title="new coronaap", )
    sh.share("aviadm24@gmail.com", perm_type="user", role="writer")
    return render(request, "main/index.html")


def update_spreadsheet(id, status):
    # based on https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
    # read that file for how to generate the creds and how to use gspread to read and write to the spreadsheet

    # use creds to create a client to interact with the Google Drive API
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")
    creds_dict = json.loads(json_creds)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    client = gspread.authorize(creds)

    # Find a workbook by url
    corona_url = "https://docs.google.com/spreadsheets/d/18fUM43kYh4Ac6kgNItlSKJbbjKhIoSCMGYqTCWqGUzk/edit#gid=2084856787"
    spreadsheet = client.open_by_url(corona_url)
    # worksheet_list = spreadsheet.worksheets()
    sheet = spreadsheet.worksheet("תגובות לטופס 1")

    # Extract and print all of the values
    # rows = sheet.get_all_records()
    ID_COLUMN = 1
    STATUS_COLUMN = "P"
    list_of_ids = sheet.col_values(ID_COLUMN)
    if id in list_of_ids:
        id_row_number = str(list_of_ids.index(i) + 1)
        sheet.update_acell(STATUS_COLUMN+id_row_number, status)


def convert_status(status):
    conversion_dict = {"טופל": "2", "נוצר": "1", "ממתין": "0"}
    return conversion_dict.get(status, "3")


def get_project_id_and_message(data):
    parsed_message = pr.unquote(data["message"])
    split_message = parsed_message.split()
    project_id = split_message[0].strip()
    status = split_message[1].strip()
    return (project_id, status) if (project_id.isdigit() and status) else (None, None)


@csrf_exempt
def incoming_sms(request):
    if request.method == "POST":
        # parse body and get SMS data (id, status)
        post_body_uft8 = request.body.decode("utf-8")
        data = dict(pr.parse_qsl(post_body_uft8))
        project_id, status = get_project_id_and_message(data)
        # update status in spreadsheet or exit if there"s a problem
        if id and status in ["טופל", "ממתין", "נוצר קשר", "וידוא משימה"]:
            print("Incoming SMS with ID: {}, Status: {}".format(id, status))
            update_spreadsheet(id=project_id, status=status)
        else:
            print("Invalid SMS")
            return

        # if task was completed - cancel an SMS reminder (if exists)
        if status == "טופל":
            cancel_sms_by_project_id(project_id)
        return HttpResponse("")
