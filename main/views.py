from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def index(request):
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
    sheet.update_acell('O' + str(index + 1), status)



@csrf_exempt
def update_sheets(request):
    if request.method == 'POST':
        post_uft8 = request.body.decode("utf-8")
        print('post_uft8: ', post_uft8)
        try:
            post = request.body
            print('post: ', post)
            pars = post_uft8.split('&')
            body = pars[1]
            message = pr.unquote(pars[2].split('=')[1])
            print('pars2: ', message)
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
        Feedback.objects.update_or_create(
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

