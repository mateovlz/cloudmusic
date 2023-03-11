
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from cloudmusic.models import Song, UserAccounts
from cloudmusic.serializers import SongSerializer, UserSerializer, SongUpdateSerializer
from rest_framework.views import APIView, Response,exception_handler
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.pagination import PageNumberPagination
from cloudmusic.pagination import PaginationHandlerMixin
from cloudmusic.exceptions import NotFound
from django.http import Http404
import re
import random


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class SongList(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = SongSerializer

    def get_own_songs(self, user_id):
        try:
            return Song.objects.filter(created_by=user_id)
        except Song.DoesNotExist:
            return None

    def get_public_songs(self, user_id):
        try:
            return Song.objects.filter(public=True)
        except Song.DoesNotExist:
            return None

    def get(self, request, public, format=None):
        permission_classes = [IsAuthenticated]
        user_id = request.user.id

        if public == 'private':
            song = self.get_own_songs(user_id)
            message = "Private Songs"
        elif public == 'public':
            song = self.get_public_songs(user_id)
            message = "Public Songs"
        else:
            song = None
            message = "Error to access to Songs, for acces to your own songs please refer to /song/list/private for all the publics songs refer to /songs/list/private"

        if not song:
            if public == "public" and public == "private":
                message = "Songs not found"
            return JsonResponse({"message": message}, status=status.HTTP_401_UNAUTHORIZED)

        page = self.paginate_queryset(song)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            self.serializer_class(song, many=True)

        return JsonResponse({"message": message, "data": serializer.data}, safe=False)


# Song Endpoints
class SongDetail(APIView):

    def get_object(self, pk):
        try:
            return Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return None

    def get_own_song(self, pk, user_id):
        try:
            return Song.objects.filter(pk=pk, created_by=user_id)
        except Song.DoesNotExist:
            return None

    def post(self, request, format=None):
        permission_classes = [IsAuthenticated]
        user_id = request.user.id
        data = JSONParser().parse(request)

        serializer = SongSerializer(data={
            "name": data['name'],
            "duration": data['duration'],
            "created_by": user_id,
            "public": True if data['public'] == 'Y' else False
        })

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Song Created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Error Creating Song'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        permission_classes = [IsAuthenticated]
        user_id = request.user.id
        song = self.get_object(pk)
        message = "Public Song"
        data = None

        if not song:
            message = "Song not found"
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        if not song.public and song.created_by != user_id:
            message = "Private Song, please remember you can only see the songs you created"
        else:
            serializer = SongSerializer(song)
            return JsonResponse({"message": message, "data": serializer.data}, safe=False)

        return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        data = JSONParser().parse(request)
        permission_classes = [IsAuthenticated]
        user_id = request.user.id
        song = self.get_own_song(data['id'], user_id)
        message = "Song Updated"

        if not song:
            message = "Song not found, please remember you can only update the songs you created"
            return JsonResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = SongUpdateSerializer(instance=song[0], data={
                "id": data['id'],
                "name": data['name'],
                "duration": data['duration'],
                "created_by": user_id,
                "public": True if data['public'] == 'Y' else False,
                "created_timestamp": song[0].created_timestamp
            })
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": message, "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                message = "Error in the serialization"
                return JsonResponse({"message": message, "data": serializer.errors}, status=status.HTTP_200_OK)
        return Response({"message": "Error Updating Song"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, format=None):
        permission_classes = [IsAuthenticated]
        user_id = request.user.id
        song = self.get_own_song(pk, user_id)
        message = "Song Delete"
        print(song)
        if not song:
            message = "Song Not Found, please remember you can only delete the songs you created"
            return JsonResponse({"message": message}, status=status.HTTP_404_NOT_FOUND)
        else:
            song.delete()
            return JsonResponse({"message": message}, status=status.HTTP_200_OK)
        return Response({"message": "Error Deleting Song"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh), str(refresh.access_token)


# Authentication Endpoints
class UserLogin(APIView):

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        message = 'Login'
        status_response = status.HTTP_200_OK
        refresher = ''
        access_token = ''

        user_exists, user = is_user_registered(data['email'])
        valid_email, email_message = is_valid_email(data['email'])
        valid_password, password_message = is_validate_password(data['password'])

        if user_exists:
            password_match = bool(check_password(data['password'], user.password))
            if valid_email and valid_password and password_match:
                message += ' succesfully, please use the [acces_token] to authenticated and call the others apis.'
                refresher, access_token = get_tokens_for_user(user)
            else:
                status_response = status.HTTP_406_NOT_ACCEPTABLE
                if not valid_email:
                    message += ' [error] ' + email_message
                if not valid_password:
                    message += ' [error] ' + password_message
                if not password_match:
                    message += ' [error] invalid credentials'
        else:
            message += ' [error] account not found, please create an account to Login'
            status_response = status.HTTP_404_NOT_FOUND

        return JsonResponse({'message': message, 'access_token': access_token}, status=status_response)


class UserSignUp(APIView):

    def post(self, request, format=None):
        message = 'Creating an account'
        data = JSONParser().parse(request)
        status_response = status.HTTP_200_OK

        user_exists, user = is_user_registered(data['email'])
        valid_email, email_message = is_valid_email(data['email'])
        valid_password, password_message = is_validate_password(data['password'])

        if not user_exists:
            if valid_email and valid_password:
                data['password'] = make_password(data['password'])
                user_account = UserSerializer(data=data)
                if user_account.is_valid():
                    user_account.save()
                else:
                    print('invalid serializer')
                message += ' succesfully'
            else:
                status_response = status.HTTP_406_NOT_ACCEPTABLE
                if not valid_email:
                    message += ' [error] ' + email_message
                if not valid_password:
                    message += ' [error] ' + password_message
        else:
            message += ' [error] user already exists'

        return JsonResponse({'message': message}, status=status_response)


class PublicEndpoint(APIView):
    def get(self, request):
        random_number = random.randint(1, 1000)
        message = f'This is your random number {random_number}'
        return JsonResponse({'message': message}, status=status.HTTP_200_OK)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, (TokenError, InvalidToken)) and 'Token is invalid or expired' in str(exc):
        response = Response(
            {
                'message': 'Token is invalid or expired, please Log in again to continue using the app. [Token expires every 20 minutes]'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if isinstance(exc, Http404):
        exc = NotFound()
        response = exception_handler(exc, context)

        if response is not None:
            response.data['status_code'] = response.status_code
    return response


def is_user_registered(email):
    try:
        user = UserAccounts.objects.get(email=email)
        return True, user
    except UserAccounts.DoesNotExist:
        return False, None


def is_valid_email(email):
    isvalid = True
    message = 'Email is valid'
    if not bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)):
        isvalid = False
        message = 'Email is not valid, please enter a valid email. Ex: example@musiccloud.co'
    return isvalid, message


def is_validate_password(password):
    isvalid = True
    lower_case_validation = 0
    upper_case_validation = 0
    message = "Password is valid"
    error_message = "Password is invalid"
    for char in password:
        lowercase = char.islower()
        uppercase = char.isupper()

        if lowercase:
            lower_case_validation += 1

        if uppercase:
            upper_case_validation += 1

    if len(password) < 10:
        error_message += ", should contain at least 10 characters"
        isvalid = False

    if lower_case_validation < 1:
        error_message += ", one lowercase is missing"
        isvalid = False

    if upper_case_validation < 1:
        error_message += ", one uppercase is missing"
        isvalid = False

    special_characters = re.findall(r'[@\]!?#]', password)

    if not bool(special_characters):
        error_message += ", one of this characters @ # ? ! ] is missing"
        isvalid = False

    if isvalid:
        error_message = message

    return isvalid, error_message
