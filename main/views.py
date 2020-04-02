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
configuration.username = 'pc.crumbs@gmail.com'
configuration.password = 'CB6272BA-A570-5DAC-A86E-4236FF780AD4'
api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))


# {'number': number,
#  'message_body': message_body,
#  'schedule': schedule,
#  'project_id': project_id
#  }
@csrf_exempt
def send_sms(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        number = data['number']
        message_body = data['message_body']
        schedule = data['schedule']
        project_id = data['project_id']
        status = '0'
        sms_message = SmsMessage(source="api", body=message_body, to="+972{}".format(number), schedule=schedule)
        sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])

        try:
            api_response = ast.literal_eval(api_instance.sms_send_post(sms_messages))
            message_id = api_response["data"]["messages"][0]["message_id"]
            if schedule and project_id:
                # genesral_dict[sn] = (number, message_id)
                sms = Sms()
                sms.number = number
                sms.message_id = message_id
                sms.project_id = project_id
                sms.status = status
                sms.save()
        except ApiException as e:
            print("Exception when calling SMSApi->sms_send_post: {}\n".format(e))
        return HttpResponse('')

@csrf_exempt
def cancel_sms(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        project_id = data['project_id']
        sms = Sms.objects.get(project_id=project_id)
        message_id = sms.message_id
        api_response = api_instance.sms_cancel_by_message_id_put(message_id)
        print('api_response: ', api_response)
        return HttpResponse('')


def index(request):
    # https: // bootsnipp.com / snippets / ZXKKD
    return render(request, 'main/corona.html')


def login():
    scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_dict = {}
    try:
        json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")
        creds_dict = json.loads(json_creds)
    except:
        file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'client-secret.json')
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
    sh = client.create('coronaap spreadsheet')
    sh.share('aviadm24@gmail.com', perm_type='user', role='writer')
    return render(request, 'main/index.html')


def copy_sheet(request):
    client = login()
    sh = client.copy('18fUM43kYh4Ac6kgNItlSKJbbjKhIoSCMGYqTCWqGUzk', title='new coronaap', )
    sh.share('aviadm24@gmail.com', perm_type='user', role='writer')
    return render(request, 'main/index.html')


def aviad_sheets(id, status):
    # based on https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
    # read that file for how to generate the creds and how to use gspread to read and write to the spreadsheet

    # use creds to create a client to interact with the Google Drive API
    scopes = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")

    creds_dict = json.loads(json_creds)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    client = gspread.authorize(creds)

    # Find a workbook by url
    korona_url = 'https://docs.google.com/spreadsheets/d/18fUM43kYh4Ac6kgNItlSKJbbjKhIoSCMGYqTCWqGUzk/edit#gid=2084856787'
    spreadsheet = client.open_by_url(korona_url)
    worksheet_list = spreadsheet.worksheets()
    # print(worksheet_list)
    sheet = spreadsheet.worksheet("תגובות לטופס 1")

    # Extract and print all of the values
    # rows = sheet.get_all_records()
    # print(rows)
    values_list = sheet.col_values(1)
    print(values_list)
    index = None
    for i in values_list:
        if i == id:
            index = values_list.index(i)
    sheet.update_acell('P' + str(index + 1), status)



def check_status(text):
    if "טופל" in text:
        return '2'
    elif "נוצר" in text:
        return '1'
    elif "ממתין" in text:
        return '0'
    else:
        return '3'


@csrf_exempt
def update_sheets(request):
    if request.method == 'POST':
        post_uft8 = request.body.decode("utf-8")
        # print('post_uft8: ', post_uft8)
        try:
            pars = post_uft8.split('&')
            # body = pars[1]
            message = pr.unquote(pars[2].split('=')[1])
            # print('pars2: ', message)
            id = re.findall(r'\d+', str(message))[0] #  message.split(' ')[0]
            print('id: ', id)
            status = message.replace(id, '').strip()
            print('status: ', status)
            for s in ['טופל', 'ממתין', 'נוצר קשר', 'וידוא משימה']:
                if status in s:
                    aviad_sheets(id=id, status=status)
        except:
            # id = re.findall(r'\d+', str(post))[0]
            id = post_uft8.split(' ')[0]
            status = post_uft8.split(' ')[1]
            aviad_sheets(id=id, status=status)
        print("id: ", id)
        print("status: ", status)
        Sms.objects.update_or_create(
            project_id=id,
            status=check_status(str(status))
        )
        # fb = Feedback()
        # fb.project_id = id
        # fb.status = check_status(str(status))
        # fb.save()
        return render(request, 'home/list.html')
    else:
        aviad_sheets(id=None, status=None)
        return render(request, 'home/list.html')

# not in use
# @csrf_exempt
# def check_update(request):
#     if request.method == 'POST':
#         data = request.body.decode("utf-8")
#         print('req: ', data)
#         # id = re.findall(r'\d+', str(data))[0]
#         try:
#             status = Feedback.objects.get(project_id=str(data)).status
#             print('status: ', status)
#             return JsonResponse({'success': True, 'status': str(status)})
#         except:
#             return JsonResponse({'success': False, 'status': '3'})
