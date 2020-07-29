from django.shortcuts import render
import xlrd


def index(request):  # based on - https://github.com/anuragrana/excel-file-upload-django
    if "GET" == request.method:
        return render(request, 'index.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        excel_data = []
        
        wb = xlrd.open_workbook(file_contents=excel_file.read())
        report_sheet = wb.sheet_by_name("CReport_Patient")
        first_full_row = report_sheet._first_full_rowx
        first_data_row = first_full_row + 1
        id_col = get_col_by_name("מספר זהות")
        status_col = get_col_by_name("סטטוס")
        hospitalization_date_col = get_col_by_name("תאריך אשפוז")
        release_date_col = get_col_by_name("תאריך שחרור")
        
        excel_data.append(first_full_row, first_data_row, id_col, status_col, hospitalization_date_col, release_date_col)

        return render(request, 'index.html', {"excel_data": excel_data})