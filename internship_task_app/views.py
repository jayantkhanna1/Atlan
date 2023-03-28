from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User,Form,Responses
from .serializer import UserSerializer,FormSerializer,ResponsesSerializer
from rest_framework import status
from django.http import Http404
import json

class UserMethods:
    @api_view(['POST'])
    def NewUser(request):
        # Making sure request is POST although it is already checked but just to be sure
        if request.method == 'POST':
            # Checking if we got all necessary data
            if request.data.get('name') and request.data.get('email') and request.data.get('password') and request.data.get('phone') and request.data.get('address'):
                # Checking if user already exists
                if User.objects.filter(email=request.data['email']).exists():
                    return Response({"error":"User already exists"},status=status.HTTP_400_BAD_REQUEST)
                # If not creating new user
                User.objects.create(address = request.data['address'], name = request.data['name'],email = request.data['email'],password = request.data['password'],phone = request.data['phone'])
                user = User.objects.get(email=request.data['email'])
                serializer = UserSerializer(user)
                # Confirming new user is added
                return Response({"data":serializer.data},status=status.HTTP_201_CREATED)
            # Returning some data is missing
            return Response({"error":"Name, Email, password, phone, address something is missing"}, status=status.HTTP_400_BAD_REQUEST)
        # Returning method not allowed
        return Response({"error":"Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @api_view(['GET'])
    def GetUser(request):
        # Making sure request is GET although it is already checked but just to be sure
        if request.method == 'GET':
            # Checking if we got all necessary data
            
            if request.GET.get('email') and request.GET.get('password'):
                # Checking if user exists
                if User.objects.filter(email=request.GET['email']).exists():
                    user = User.objects.get(email=request.GET['email'])
                     # Checking if password is correct
                    if user.password == request.GET['password']:
                        # Returning user data
                        serializer = UserSerializer(user)
                        return Response({"data":serializer.data},status=status.HTTP_200_OK)
                    # Returning password is incorrect
                    return Response({"error":"Password is incorrect"},status=status.HTTP_400_BAD_REQUEST)
                # Returning user does not exists
                return Response({"error":"User does not exists"},status=status.HTTP_400_BAD_REQUEST)
            # Returning some data is missing
            return Response({"error":"Email or password is missing"}, status=status.HTTP_400_BAD_REQUEST)
        # Returning method not allowed
        return Response({"error":"Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @api_view(['Delete'])
    def DeleteUser(request):
        # Making sure request is DELETE although it is already checked but just to be sure
        if request.method == 'DELETE':
            # Checking if we got all necessary data
            if request.data.get('email') and request.data.get('password'):
                # Checking if user exists
                if User.objects.filter(email=request.data['email'], password = request.data['password']).exists():
                    user = User.objects.get(email=request.data['email'])
                    # Deleting user
                    user.delete()
                    # Confirming user is deleted
                    return Response({"message":"User deleted successfully"},status=status.HTTP_200_OK)
                # Returning user does not exists
                return Response({"error":"User does not exists"},status=status.HTTP_400_BAD_REQUEST)
            
            # Deleting user by id
            elif request.data.get('id') and request.data.get('password'):
                # Checking if user exists
                if User.objects.filter(id=request.data['id'], password = request.data['password']).exists():
                    user = User.objects.get(id=request.data['id'])
                    # Deleting user
                    user.delete()
                    # Confirming user is deleted
                    return Response({"message":"User deleted successfully"},status=status.HTTP_200_OK)

                # Returning user does not exists
                return Response({"error":"User does not exists"},status=status.HTTP_400_BAD_REQUEST)

            # Returning some data is missing
            return Response({"error":"Email or id is missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Returning method not allowed
        return Response({"error":"Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @api_view(['PUT'])
    def UpdateUser(request):
        if request.method == 'PUT':
            if request.data.get('email') and request.data.get('password'):
                if User.objects.filter(email=request.data['email'], password = request.data['password']).exists():
                    user = User.objects.get(email=request.data['email'])
                    if request.data.get('name'):
                        user.name = request.data['name']
                    if request.data.get('password'):
                        user.password = request.data['password']
                    if request.data.get('phone'):
                        user.phone = request.data['phone']
                    if request.data.get('address'): 
                        user.address = request.data['address']
                    user.save()
                    return Response({"message":"User updated successfully"},status=status.HTTP_200_OK)
                return Response({"error":"User does not exists or is Unauthorized"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"error":"Email is missing"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class FormsMethods:
    @api_view(['POST'])
    def NewForm(request):
        # Making sure request is POST although it is already checked but just to be sure
        if request.method == 'POST':
            # Checking if we got all necessary data
            if request.data['user_id'] and request.data['form_name'] and request.data['form_description'] and request.data['form_data']:
                form_data = request.data['form_data']
                form_data = json.dumps(form_data)
                # Checking if user exists
                try:
                    user = User.objects.get(id=request.data['user_id'])
                except User.DoesNotExist:
                    return Response({"error":"User not found because he/she doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
                
                # Checkign if form questions are correct
                res = CheckJsonData.checkForm(form_data)
                
                # If form questions are correct creating new form
                if res == True:
                    form = Form.objects.create(user = User.objects.get(id=request.data['user_id']) ,form_name=request.data['form_name'],form_description=request.data['form_description'],form_data=form_data)
                    form_id = form.id
                    form_obj = Form.objects.get(id=form_id)
                    serializer = FormSerializer(form_obj)
                    return Response({'data':serializer.data},status=status.HTTP_201_CREATED)
                # If form questions are not correct returning error
                return Response({"error":res},status=status.HTTP_400_BAD_REQUEST)
            else:
                # Returning some data is missing
                return Response({'error':"Missing Form name or Form description or form data or user id"},status=status.HTTP_400_BAD_REQUEST)
        else:
            # Returning method not allowed
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    def GetForm(request):
        # Making sure request is GET although it is already checked but just to be sure
        if request.method == 'GET':

            form = Form.objects.none()
            # Only getting forms with user id that was provided to us in request
            if request.GET.get('user_id'):
                user_id = request.GET.get('user_id')
                # Getting data from form_id attribute
                if request.GET.get('form_id'):
                    try:
                        form_by_id = Form.objects.filter(id=request.GET['form_id'],user = User.objects.get(id=user_id))
                        form = form | form_by_id
                    except:
                        pass
                # Getting data from user_id attribute
                elif request.GET.get('user_id'):
                    try:
                        form_by_user_id = Form.objects.filter(user=request.GET['user_id'])
                        form = form | form_by_user_id
                    except:
                        pass
                # Getting data from form_name attribute
                elif request.GET.get('form_name'):
                    try:
                        name = request.GET['form_name']
                        name = name.lower()
                        name = name.split(" ")
                        for x in name:
                            form_by_name = Form.objects.filter(form_name__icontains=x,user = User.objects.get(id=user_id))
                            form = form | form_by_name
                    except:
                        pass
                # Getting data from form_description attribute
                elif request.GET.get('form_description'):
                    try:
                        form_by_description = Form.objects.filter(form_description__icontains=request.GET['form_description'],user = User.objects.get(id=user_id))
                        form = form | form_by_description
                    except:
                        pass
                # Getting data from query attribute
                elif request.GET.get('query'):
                    try:
                        form_by_query = Form.objects.filter(form_name__icontains=request.GET['query'],user = User.objects.get(id=user_id)) | Form.objects.filter(form_description__icontains=request.GET['query'],user = User.objects.get(id=user_id)) | Form.objects.filter(form_data__icontains=request.GET['query'],user = User.objects.get(id=user_id))
                        form = form | form_by_query
                    except:
                        pass
                # Getting all data from user id
                else:
                    all_forms = Form.objects.filter(user = user_id)
                    form = form | all_forms
                               
                serializer = FormSerializer(form, many=True)
                return Response({'data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"error" : "Request type not allowed"},status=status.HTTP_400_BAD_REQUEST)

    @api_view(['PUT'])
    def UpdateForm(request):
        # Making sure request is PUT although it is already checked but just to be sure
        if request.method == 'PUT':
            # Checking if we got all necessary data
            if request.data.get('user_id') and request.data.get('form_id') and request.data.get('form_name') and request.data.get('form_description') and request.data.get('form_data'):
                # Getting form data
                form_data = request.data['form_data']
                form_data = json.dumps(form_data)
                user_id = request.data['user_id']

                # Checking if form exists
                try:
                    form = Form.objects.get(id=request.data['form_id'])
                except Form.DoesNotExist:
                    return Response({"error":"Form not found because he/she doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
                
                # Checking if new form data is correct
                res = CheckJsonData.checkForm(form_data)

                # Checking if user is authorized to update this form
                if form.user != User.objects.get(id=user_id):
                    return Response({"error":"Unauthorized"}, status=status.HTTP_404_NOT_FOUND)

                # If form data is correct updating form
                if res == True:
                    form.form_name = request.data['form_name']
                    form.form_description = request.data['form_description']
                    form.form_data = form_data
                    form.save() 
                    serializer = FormSerializer(form)
                    return Response({'data':serializer.data},status=status.HTTP_200_OK)
                # If form data is not correct returning error
                return Response({"error":res},status=status.HTTP_400_BAD_REQUEST)
            else:
                # Returning some data is missing
                return Response({'error':"Missing Form name or Form description or form data or form id"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @api_view(['DELETE'])
    def DeleteForm(request):
        # Making sure request is DELETE although it is already checked but just to be sure
        if request.method == 'DELETE':
            # Checking if we got all necessary data
            if request.data.get('form_id') and request.data.get('user_id'):
                # Getting form data returning if no form is found
                try:
                    form = Form.objects.get(id=request.data['form_id'])
                except Form.DoesNotExist:
                    return Response({"error":"Form not found because it doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
                
                # Checking if user is authorized to delete this form
                if form.user != User.objects.get(id=request.data['user_id']):
                    return Response({"error":"Unauthorized"}, status=status.HTTP_404_NOT_FOUND)
                
                # Deleting form
                form.delete()
                # Returning success
                return Response({"message":"Form deleted successfully"},status=status.HTTP_200_OK)
            else:
                # Returning some data is missing
                return Response({'error':"Missing Form id or user id"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class ResponsesMethods:
    @api_view(['POST'])
    def NewResponse(request):
        # Making sure request is POST although it is already checked but just to be sure
        if request.method == 'POST':
            # Checking if we got all necessary data
            if request.data.get('responder') and request.data.get('admin') and request.data.get('form') and request.data.get('response'):
                response_data = request.data['response']
                response_data = json.dumps(response_data)

                # Checking if response data format is correct
                res = CheckJsonData.checkResponse(response_data)

                # Checking if user and admin exists
                try:
                    admin = User.objects.get(id=request.data['admin'])
                    responder = User.objects.get(id=request.data['responder'])
                except:
                    return Response({"error":"User or responder not found because he/she doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
                
                # Checking if form exists
                try:
                    form = Form.objects.get(id=request.data['form'])
                except:
                    return Response({"error":"Form not found"}, status=status.HTTP_404_NOT_FOUND)
                
                # If response data is correct creating response
                if res == True:
                    response = Responses.objects.create(admin = User.objects.get(id = request.data['admin']),response=response_data,responder =  User.objects.get(id = request.data['responder']),form = Form.objects.get(id = request.data['form']))
                    response_id = response.id
                    serializer = ResponsesSerializer(Responses.objects.get(id = response_id))
                    return Response({'data':serializer.data},status=status.HTTP_201_CREATED)
                # If response data is not correct returning error
                return Response({"error":res},status=status.HTTP_400_BAD_REQUEST)
            else:
                # Returning some data is missing
                return Response({'error':"Missing Form id or response"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)          

    @api_view(['GET'])
    def GetResponse(request):
        # Making sure request is GET although it is already checked but just to be sure
        if request.method == 'GET':
            # Checking if we got all necessary data
            response = Responses.objects.none()
            # Checking if we got admin id
            if request.GET.get('admin'):
                # Getting responses by form id
                if request.GET.get('form_id'):
                    try:
                        response_by_formid = Responses.objects.filter(form=request.GET['form_id'],admin = request.GET['admin'])
                        response = response | response_by_formid
                    except:
                        pass
                # Getting responses by response id
                if request.GET.get('response_id'):
                    try:
                        responses_id = Responses.objects.filter(id=request.GET['response_id'], admin = request.GET['admin'])
                        response = response | responses_id
                    except:
                        pass
                # Getting responses by name of responder
                if request.GET.get('responder'):
                    try:
                        name = request.GET['responder']
                        name = name.lower()
                        name = name.split(" ")
                        for x in name:
                            user = User.objects.filter(name__icontains = x)
                            for y in user:
                                response_by_name = Responses.objects.filter(user =y.id, admin = request.GET['admin'])
                                response = response | response_by_name
                    except:
                        pass
                # Getting responses by address_of_responder
                if request.GET.get('address_of_responder'):
                    try:
                        name = request.GET['address_of_responder']
                        name = name.lower()
                        name = name.split(" ")
                        for x in name:
                            user = User.objects.filter(address__icontains = x)
                            for y in user:
                                response_by_name = Responses.objects.filter(user =y.id, admin = request.GET['admin'])
                                response = response | response_by_name
                    except:
                        pass
                # Getting responses by email_of_responder
                if request.GET.get('email_of_responder'):
                    try:
                        email = request.GET['email_of_responder']
                        email = email.lower()
                        response_by_email = User.objects.filter(email = email)
                        for x in response_by_email:
                            response_by_email = Responses.objects.filter(user = x.id, admin = request.GET['admin'])
                            response = response | response_by_email
                        
                    except:
                        pass
                # Getting responses by phone_of_responder
                if request.GET.get('phone_of_responder'):
                    try:
                        phone = request.GET['phone_of_responder']
                        response_by_phone = User.objects.filter(phone = phone)
                        for x in response_by_phone:
                            response_by_phone = Responses.objects.filter(user = x.id, admin = request.GET['admin'])
                            response = response | response_by_phone
                        
                    except:
                        pass
                # Getting responses by query
                if request.GET.get('query'):
                    try:
                        response_by_query = Responses.objects.filter(response__icontains=request.GET['query'], admin = request.GET['admin'])
                        response = response | response_by_query
                    except:
                        pass
                
            serializer = ResponsesSerializer(response, many=True)
            return Response({'data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"error" : "Request type not allowed"},status=status.HTTP_400_BAD_REQUEST)

    @api_view(['PUT'])
    def UpdateResponse(request):
        # Making sure request is PUT although it is already checked but just to be sure
        if request.method == 'PUT':
            # Checking if we got all necessary data
            if request.data.get('response_id') and request.data.get('response') and request.data.get('admin') and request.data.get('responder') and request.data.get('form'):
                response_data = request.data['response']
                response_data = json.dumps(response_data)

                # Checking if response data format is correct
                res = CheckJsonData.checkResponse(response_data)

                # If response data is correct updating response
                if res == True:
                    try:
                        response = Responses.objects.get(id=request.data['response_id'], admin = request.data['admin'])
                    except Responses.DoesNotExist:
                        # Returning response not found or user unauthorized error
                        return Response({"error":"Response not found because he/she doesn't exists or User is Unauthorized"}, status=status.HTTP_404_NOT_FOUND)
                    response.response = response_data
                    response.save()
                    serializer = ResponsesSerializer(response)
                    return Response({'data':serializer.data},status=status.HTTP_200_OK)
                # If response data is not correct returning error
                return Response({"error":res},status=status.HTTP_400_BAD_REQUEST)
            else:
                # Returning some data is missing
                return Response({'error':"Missing Response id or response"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['DELETE'])
    def DeleteResponse(request):
        # Making sure request is DELETE although it is already checked but just to be sure
            if request.method == 'DELETE':
                # Checking if we got all necessary data
                if request.data.get('response_id') and request.data.get('admin'):
                    try:
                        response = Responses.objects.get(id=request.data['response_id'], admin = request.data['admin'])
                    except Responses.DoesNotExist:
                        # Returning response not found or user unauthorized error
                        return Response({"error":"Response not found because he/she doesn't exists or User is unauthorized"}, status=status.HTTP_404_NOT_FOUND)
                    response.delete()
                    # Returning success message
                    return Response({"message":"Response deleted successfully"},status=status.HTTP_200_OK)
                else:
                    # Returning some data is missing
                    return Response({'error':"Missing Response id"},status=status.HTTP_400_BAD_REQUEST)
            else:
                # Returning request type not allowed
                return Response(status=status.HTTP_400_BAD_REQUEST)



class CheckJsonData:
    def checkForm(data):
        flag = 0
        data = json.loads(data)
        for x in data:
            try:
                if x["question_type"]:
                    ques_type = x['question_type']
                    ques_type = ques_type.lower()
                    if ques_type == 'single choice' or ques_type == 'multiple choice':
                        try : 
                            if not x['option 1'] or not x['option 2'] or not x['option 3'] or not x['option 4']:
                                return "Options are missing in question : " + str(flag)
                        except:
                            return "Options are missing in question : " + str(flag)
                        try:
                            if not x['question_title']:
                                return "Question title is missing in question : " + str(flag)
                        except:
                            return "Question title is missing in question : " + str(flag)
                        try:
                            if not x['question_description']:
                                return "Question description is missing in question : " + str(flag)
                        except:
                            return "Question description is missing in question : " + str(flag)
                        try:
                            if not x['required']:
                                return "Required is missing please set it to False if not required in question : " + str(flag)
                        except:
                            return "Required is missing please set it to False if not required in question : " + str(flag)
                    elif ques_type == 'text' or ques_type == 'number' or ques_type == 'date' or ques_type == 'time' or ques_type == 'file':
                        try:
                            if not x['question_title']:
                                return "Question title is missing in question : " + str(flag)
                        except:
                            return "Question title is missing in question : " + str(flag)

                        try:
                            if not x['question_description']:
                                return "Question description is missing in question : " + str(flag)
                        except:
                            return "Question description is missing in question : " + str(flag)
                        try:
                            if not x['required']:
                                return "Required is missing please set it to False if not required in question : " + str(flag)
                        except:
                            return "Required is missing please set it to False if not required in question : " + str(flag)
                    else:
                        return "Invalid Question type in question : " + str(flag)
                
                else : 
                    return "Question Type missing in question : " + str(flag)
            except:
                return "Question Type missing in question : " + str(flag)
            flag = flag + 1
        return True

    def checkResponse(data):
        flag = 0
        data = json.loads(data)
        for x in data:
            try:
                if x["question_type"]:
                    ques_type = x['question_type']
                    ques_type = ques_type.lower()
                    if ques_type == 'single choice':
                        try : 
                            if not x['option 1'] or not x['option 2'] or not x['option 3'] or not x['option 4']:
                                return "Options are missing in question : " + str(flag)
                        except:
                            return "Options are missing in question : " + str(flag)
                        try:
                            if not x['question_title']:
                                return "Question title is missing in question : " + str(flag)
                        except:
                            return "Question title is missing in question : " + str(flag)
                        try:
                            if not x['question_description']:
                                return "Question description is missing in question : " + str(flag)
                        except:
                            return "Question description is missing in question : " + str(flag)
                        try:
                            if not x['required']:
                                return "Required is missing please set it to False if not required in question : " + str(flag)
                        except:
                            return "Required is missing please set it to False if not required in question : " + str(flag)
                        try:
                            if not x['answer']:
                                return "Answer is missing in response : " + str(flag)
                        except:
                            return "Answer is missing in response : " + str(flag)

                    elif ques_type == 'multiple choice':
                        try : 
                            if not x['option 1'] or not x['option 2'] or not x['option 3'] or not x['option 4']:
                                return "Options are missing in response : " + str(flag)
                        except:
                            return "Options are missing in response : " + str(flag)
                        try:
                            if not x['question_title']:
                                return "Question title is missing in response : " + str(flag)
                        except:
                            return "Question title is missing in response : " + str(flag)
                        try:
                            if not x['question_description']:
                                return "Question description is missing in response : " + str(flag)
                        except:
                            return "Question description is missing in response : " + str(flag)
                        try:
                            if not x['required']:
                                return "Required is missing please set it to False if not required in response : " + str(flag)
                        except:
                            return "Required is missing please set it to False if not required in response : " + str(flag)
                        try:
                            if not x['answer'] or type(x['answer']) != list:
                                return "Answer is missing in response or is of incorrect type : " + str(flag)
                        except:
                            return "Answer is missing in response : " + str(flag)
      
                    elif ques_type == 'text' or ques_type == 'number' or ques_type == 'date' or ques_type == 'time' or ques_type == 'file':
                        try:
                            if not x['question_title']:
                                return "Question title is missing in response : " + str(flag)
                        except:
                            return "Question title is missing in response : " + str(flag)

                        try:
                            if not x['question_description']:
                                return "Question description is missing in response : " + str(flag)
                        except:
                            return "Question description is missing in response : " + str(flag)
                        try:
                            if not x['required']:
                                return "Required is missing please set it to False if not required in response : " + str(flag)
                        except:
                            return "Required is missing please set it to False if not required in response : " + str(flag)
                    else:
                        return "Invalid Question type in response : " + str(flag)
                
                else : 
                    return "Question Type missing in response : " + str(flag)
            except:
                return "Question Type missing in response : " + str(flag)
            flag = flag + 1
        return True


# Handling error requests
@api_view(['GET', 'POST', 'DELETE','PATCH','PUT','COPY','HEAD','OPTIONS','LINK','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW'])
def handler404(request,exception):
        raise Http404