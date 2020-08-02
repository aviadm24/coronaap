"""
1. test (run code)
2. add conditional formatting
3. add backup
"""

from oauth2client.service_account import ServiceAccountCredentials
from django.shortcuts import render
from datetime import datetime
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
    sick_sheet_records = sick_sheet.get_all_records(numericise_ignore=["all"])
    sick_sheet_ids = [record["מספר זהות"] for record in sick_sheet_records]
    healing_sheet_records = healing_sheet.get_all_records(numericise_ignore=["all"])
    healing_sheet_ids = [record["מספר זהות"] for record in healing_sheet_records]
    rows_to_delete_from_sick_sheet = []
    rows_to_delete_from_healing_sheet = []
    rows_to_add_to_sick_sheet = []
    rows_to_add_to_healing_sheet = []
    
    for new_record in xls_data:
        new_row = [new_record["last_name"],
                   new_record["first_name"],
                   new_record["phone_1"],
                   datetime.today().strftime('%d/%m/%Y'),
                   new_record["status"],
                   "לא - נמצא באשפוז" if new_record["hospitalization_date"] and not new_record["release_date"] else "לא",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   "",
                   new_record["id"],
                   new_record["address"],
                   new_record["phone_2"],
                   new_record["result_date"]]
        if new_record["status"] == "החלים":
            if new_record["id"] in sick_sheet_ids:
                src_row_num = sick_sheet_ids.index(new_record["id"])
                sick_record = sick_sheet_records[src_row_num]
                if new_record["hospitalization_date"] and new_record["release_date"] and sick_record["נוצר קשר?"] == "לא - נמצא באשפוז":
                    sick_record["נוצר קשר?"] = "לא"
                rows_to_add_to_healing_sheet.append([sick_record["שם משפחה"],
                                                     sick_record["שם פרטי"],
                                                     sick_record["טלפון"],
                                                     sick_record["תאריך הוספה לטבלה"],
                                                     new_record["status"],
                                                     sick_record["נוצר קשר?"],
                                                     sick_record["תאריך יצירת קשר"],
                                                     sick_record["סך הנפשות בבית?"],
                                                     sick_record["אפשרות לבידוד ביתי"],
                                                     sick_record["שכבת גיל"],
                                                     sick_record["סטטוס פינוי"],
                                                     sick_record["האם צריך סיוע אחר?"],
                                                     sick_record["האם נפתחה פנייה לסיוע"],
                                                     sick_record["מספר זהות"],
                                                     sick_record["כתובת"],
                                                     sick_record["טלפון 2"],
                                                     sick_record["תאריך תוצאה ראשונה"]])
                rows_to_delete_from_sick_sheet.append(src_row_num + 2)
            elif new_record["id"] in healing_sheet_ids:
                row_num = healing_sheet_ids.index(new_record["id"])
                contacted = healing_sheet_records[row_num]["נוצר קשר?"]
                if new_record["hospitalization_date"] and new_record["release_date"] and contacted == "לא - נמצא באשפוז":
                    healing_sheet.update_acell("F{}".format(row_num + 2), "לא")
            else:
                rows_to_add_to_healing_sheet.append(new_row)
        elif new_record["status"] == "מאומת":
            if new_record["id"] in sick_sheet_ids:
                row_num = sick_sheet_ids.index(new_record["id"])
                contacted = sick_sheet_records[row_num]["נוצר קשר?"]
                if new_record["hospitalization_date"] and new_record["release_date"] and contacted == "לא - נמצא באשפוז":
                    sick_sheet.update_acell("F{}".format(row_num + 2), "לא")
            elif new_record["id"] in healing_sheet_ids:
                src_row_num = healing_sheet_ids.index(new_record["id"])
                healing_record = healing_sheet_records[src_row_num]
                if new_record["hospitalization_date"] and new_record["release_date"] and healing_record["נוצר קשר?"] == "לא - נמצא באשפוז":
                    healing_record["נוצר קשר?"] = "לא"
                rows_to_add_to_sick_sheet.append([healing_record["שם משפחה"],
                                                  healing_record["שם פרטי"],
                                                  healing_record["טלפון"],
                                                  healing_record["תאריך הוספה לטבלה"],
                                                  new_record["status"],
                                                  healing_record["נוצר קשר?"],
                                                  healing_record["תאריך יצירת קשר"],
                                                  healing_record["סך הנפשות בבית?"],
                                                  healing_record["אפשרות לבידוד ביתי"],
                                                  healing_record["שכבת גיל"],
                                                  healing_record["סטטוס פינוי"],
                                                  healing_record["האם צריך סיוע אחר?"],
                                                  healing_record["האם נפתחה פנייה לסיוע"],
                                                  healing_record["מספר זהות"],
                                                  healing_record["כתובת"],
                                                  healing_record["טלפון 2"],
                                                  healing_record["תאריך תוצאה ראשונה"]])
                rows_to_delete_from_healing_sheet.append(src_row_num + 2)
            else:
                rows_to_add_to_sick_sheet.append(new_row)
    
    sick_sheet.append_rows(rows_to_add_to_sick_sheet)
    healing_sheet.append_rows(rows_to_add_to_healing_sheet)
    
    rows_to_delete_from_sick_sheet.sort(reverse=True)
    rows_to_delete_from_healing_sheet.sort(reverse=True)
    for row_num in rows_to_delete_from_sick_sheet:
        sick_sheet.delete_row(row_num)
    for row_num in rows_to_delete_from_healing_sheet:
        healing_sheet.delete_row(row_num)

def get_col_data(sheet):
    col_data = {}
    first_full_row = sheet._first_full_rowx
    for i in range(0, sheet.ncols):
        if sheet.cell(first_full_row, i).value == "מספר זהות":
            col_data["id"] = i
        elif sheet.cell(first_full_row, i).value == "שם משפחה":
            col_data["last_name"] = i
        elif sheet.cell(first_full_row, i).value == "שם פרטי":
            col_data["first_name"] = i
        elif sheet.cell(first_full_row, i).value == "כתובת":
            col_data["address"] = i
        elif sheet.cell(first_full_row, i).value == "טלפון 1":
            col_data["phone_1"] = i
        elif sheet.cell(first_full_row, i).value == "טלפון 2":
            col_data["phone_2"] = i
        elif sheet.cell(first_full_row, i).value == "סטטוס":
            col_data["status"] = i
        elif sheet.cell(first_full_row, i).value == "תאריך תוצאה ראשונה חיובי לקורונה":
            col_data["result_date"] = i
        elif sheet.cell(first_full_row, i).value == "תאריך אשפוז":
            col_data["hospitalization_date"] = i
        elif sheet.cell(first_full_row, i).value == "תאריך שחרור":
            col_data["release_date"] = i
    return col_data

def convert_date_format(old_date_format):
    if not old_date_format:
        return ""
    old_date_format_list = old_date_format.split("-")
    new_date_format = "{}/{}/{}".format(old_date_format_list[2], old_date_format_list[1], old_date_format_list[0])
    return new_date_format

def get_data_from_file(excel_file):
    wb = xlrd.open_workbook(file_contents=excel_file.read())
    report_sheet = wb.sheet_by_name("CReport_Patient")
    first_data_row = report_sheet._first_full_rowx + 1

    col_title_to_number = get_col_data(report_sheet)
    xls_data = []
    for i in range(first_data_row, report_sheet.nrows):
        xls_data.append({"id": report_sheet.cell(i, col_title_to_number["id"]).value,
                         "last_name": report_sheet.cell(i, col_title_to_number["last_name"]).value,
                         "first_name": report_sheet.cell(i, col_title_to_number["first_name"]).value,
                         "address": report_sheet.cell(i, col_title_to_number["address"]).value,
                         "phone_1": report_sheet.cell(i, col_title_to_number["phone_1"]).value,
                         "phone_2": report_sheet.cell(i, col_title_to_number["phone_2"]).value,
                         "status": report_sheet.cell(i, col_title_to_number["status"]).value,
                         "result_date": convert_date_format(report_sheet.cell(i, col_title_to_number["result_date"]).value),
                         "hospitalization_date": report_sheet.cell(i, col_title_to_number["hospitalization_date"]).value,
                         "release_date": report_sheet.cell(i, col_title_to_number["release_date"]).value})
    return xls_data

def index(request):  # based on - https://github.com/anuragrana/excel-file-upload-django
    if "GET" == request.method:
        return render(request, 'index.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        xls_data = get_data_from_file(excel_file)
        update_google_sheet(xls_data)
        return render(request, 'index.html', {"status": "העדכון בוצע בהצלחה!"})
