from oauth2client.service_account import ServiceAccountCredentials
from django.shortcuts import render
import xlrd
import json
import gspread
import os

def google_sheets_login():
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")
    creds_dict = json.loads(json_creds)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    client = gspread.authorize(creds)
    return client

def update_google_sheet(xls_data):
    google_sheets_client = google_sheets_login()
    
    corona_sheet_url = "https://docs.google.com/spreadsheets/d/1QOTNCNN4RiXSChOD309I4PGUtCHZ6u5qeJwMBi_B1qM/edit#gid=502702629"
    spreadsheet = google_sheets_client.open_by_url(corona_sheet_url)
    
    sick_sheet = spreadsheet.worksheet("מידע")
    healing_sheet = spreadsheet.worksheet("מחלימים")
    
    print("*************")
    print(sick_sheet.get_all_records())
    print("*************")

def get_col_by_name(sheet, col_name):
    first_full_row = sheet._first_full_rowx
    for i in range(0, sheet.ncols):
        if sheet.cell(first_full_row, i).value == col_name:
            return i

def get_data_from_file(excel_file):
    wb = xlrd.open_workbook(file_contents=excel_file.read())
    report_sheet = wb.sheet_by_name("CReport_Patient")
    first_data_row = report_sheet._first_full_rowx + 1

    id_col = get_col_by_name(report_sheet, "מספר זהות")
    status_col = get_col_by_name(report_sheet, "סטטוס")
    hospitalization_date_col = get_col_by_name(report_sheet, "תאריך אשפוז")
    release_date_col = get_col_by_name(report_sheet, "תאריך שחרור")
    
    xls_data = []
    for i in range(first_data_row, report_sheet.nrows):
        xls_data.append({"id": report_sheet.cell(i, id_col).value,
                         "status": report_sheet.cell(i, status_col).value,
                         "hospitalization_date": report_sheet.cell(i, hospitalization_date_col).value,
                         "release_date": report_sheet.cell(i, release_date_col).value})
    return xls_data

def index(request):  # based on - https://github.com/anuragrana/excel-file-upload-django
    if "GET" == request.method:
        return render(request, 'index.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        xls_data = get_data_from_file(excel_file)
        update_google_sheet(xls_data)
        
        excel_data = ["Done test"]
        return render(request, 'index.html', {"excel_data": excel_data})
