import requests
import gspread
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
class FormToGoogleSheet:
    @api_view(['POST'])
    def getSheet(request):
        # Checking if we have all the data we need
            if request.data.get('form_id') and request.data.get('sheet name') and request.data.get('worksheet name'):
                try:
                    # Getting the form_id from the request
                    form_id = request.data['form_id']
                    url = 'http://127.0.0.1:8000/get_form'
                    params = {'form_id': form_id}
                    # Sending request to views.py function and getting form_data
                    FormData = requests.get(url = url, params = params)
                    FormData = FormData.content

                    # Sending request to views.py function and getting response_data
                    url2 = 'http://127.0.0.1:8000/get_response'
                    params2 = {'form_id': form_id}
                    ResponsesData = requests.get(url = url2, params = params2)
                    ResponsesData = ResponsesData.content
                    
                except:
                    # If data given to us is wrong
                    return Response("Form Id is incorrect or Invalid please check",status=status.HTTP_404_NOT_FOUND)

                # Decoding Form data to json
                FormData = FormData.decode('utf-8')
                FormData = json.loads(FormData)

                # Decoding Response data to json
                ResponsesData = ResponsesData.decode('utf-8')
                ResponsesData = json.loads(ResponsesData)
                
                # getting google sheet keys
                sa = gspread.service_account(filename='internship_task_app/keys/atlankeys.json')

                # opening the google sheet and worksheet
                sheetname = request.data['sheet name']
                worksheetname = request.data['worksheet name']
                try:
                    # Checking if multiple sheets of same name exists by getting number of sheets
                    sh2 = sa.openall(sheetname)
                    if len(sh2) > 1:
                        return Response("Sheet name is not unique please check",status=status.HTTP_400_BAD_REQUEST)
                    
                    # If we have one sheet opening it
                    sh = sa.open(sheetname)
                    worksheet = sh.worksheet(worksheetname)
                
                except Exception as e:
                    print(e)
                    return Response("Sheet name or worksheet name is incorrect or Invalid please check",status=status.HTTP_400_BAD_REQUEST)
            
                # Clearing worksheet so we can enter new data
                worksheet.clear()

                # Making columns in worksheet
                FormData = FormData['data']
                form_questions = FormData[0]['form_data']
                form_questions = json.loads(form_questions)
                lst = ['Responder Name']
                for x in form_questions:
                    temp = x["question_title"]
                    lst.append(str(temp))
                worksheet.append_row(lst)
                
                # Adding responses to worksheet
                ResponsesData = ResponsesData['data']
                lst = []
                for x in ResponsesData:
                    temp = x['response']
                    temp = json.loads(temp)
                    lst = [x['name_of_responder']]
                    for y in temp:
                        lst.append(str(y['answer'])) 
                    worksheet.append_row(lst)
                    
                # Returning success message
                return Response("Done Please check your google sheet", status=status.HTTP_200_OK)
            else:
             return Response("Missing Form id or Worksheet name or Sheet name",status=status.HTTP_400_BAD_REQUEST)