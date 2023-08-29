from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
 
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
# import classes from models.py
from appTubesPI.models import User
from appTubesPI.models import list_toko
from appTubesPI.models import detail_toko
from appTubesPI.models import kain
# import classes from serializers.py
from appTubesPI.serializers import UserSerializer
from appTubesPI.serializers import list_tokoSerializer
from appTubesPI.serializers import kainSerializer
from appTubesPI.serializers import UserLoginSerializer
from appTubesPI.serializers import detail_tokoSerializer
# import rest framework
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import logout

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        # mengembalikan data dalam bentuk json
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
@api_view(['GET', 'POST']) # hanya menerima method GET dan POST
@authentication_classes([TokenAuthentication]) # memastikan user memiliki token yang valid sebelum mengakses resource
@permission_classes([IsAuthenticated]) # memastikan apakah user telah terautentikasi
def user_list(request, lev = "all"):
    # jika request method GET
    if request.method == 'GET':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403 (Admin = 1, Super Admin = 2)
        if request.user.level != "1" and request.user.level != "2":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ambil data dari tabel user sesuai dengan level, dikembalikan dalam bentuk data json
        elif lev == "2":
            users = User.objects.all()
            users_serializer = UserSerializer(users, many=True)
            return JSONResponse(users_serializer.data)
        elif lev == "1":
            lev1="0"
            users = User.objects.all().filter(level = lev1)
            users_serializer = UserSerializer(users, many=True)
            return JSONResponse(users_serializer.data)
    # jika request method POST untuk create user oleh admin dan super admin (beda dgn registrasi)
    elif request.method == 'POST':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "2":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # mengubah data json dari request body menjadi dictionary
        user_data = JSONParser().parse(request)
        # membuat level default user biasa
        user_data['level'] = '0'
        # validasi data user
        user_serializer = UserSerializer(data=user_data)
        # jika valid, simpan user ke tabel user
        if user_serializer.is_valid():
            user = user_serializer.save()
            return JSONResponse({'data':user_serializer.data}, status=status.HTTP_201_CREATED)
        # jika tidak valid, return response 400
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def user_create(request):
    # jika request method POST untuk proses registrasi
    if request.method == 'POST':
        # mengubah data json dari request body menjadi dictionary
        user_data = JSONParser().parse(request)
        # membuat level user pada level default Customer ketika registrasi
        user_data['level'] = '0'
        # validasi data user
        user_serializer = UserSerializer(data=user_data)
        # jika valid, simpan user ke tabel user dan buat access token
        if user_serializer.is_valid():
            user = user_serializer.save()
            token, created = Token.objects.get_or_create(user=user) #untuk mendapatkan atau membuat token untuk user
            return JSONResponse({'data':user_serializer.data}, status=status.HTTP_201_CREATED)
        # jika tidak valid, return response 400
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def user_login(request):
    # jika request method POST (login)
    if request.method == 'POST':
        # mengubah data json dari request body menjadi dictionary
        user_data = JSONParser().parse(request)
        # validasi data user
        user_serializer = UserLoginSerializer(data=user_data)
        # jika valid, cek apakah user dan password sesuai dengan yang ada di tabel user
        if user_serializer.is_valid():
            user = authenticate(request=request, username=user_data['username'], password=user_data['password'])
            # Jika ya, buat access token
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return JSONResponse({'data': UserSerializer(user).data, 'token': token.key})
            else:
                # Jika tidak kembalikan response 401
                return JSONResponse(user_serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        # Jika tidak valid, kembalikan response 400
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST']) # hanya menerima method POST
@authentication_classes([TokenAuthentication]) # melakukan autentikasi token
@permission_classes([IsAuthenticated]) # hanya user yang terautentikasi yang bisa mengakses
def user_logout(request):
    # jika request method POST untuk proses logout
    if request.method == "POST":
        # hapus access token user
        request.user.auth_token.delete()

        # logout user
        logout(request)

        # return response 200
        return JSONResponse("User Logout Successfully", status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE']) # hanya menerima method GET, PUT, PATCH, dan DELETE
@authentication_classes([TokenAuthentication]) # Autentikasi token
@permission_classes([IsAuthenticated]) # Hanya user terautentikasi yang bisa mengakses
def user_detail(request, pk):
    # ambil data user sesuai primary key (pk) user yang mengakses
    try:
        user = User.objects.get(pk=pk)
    # return response 404 jika user tidak ada
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # jika request method GET
    if request.method == 'GET':
        # validasi data user
        user_serializer = UserSerializer(user)
        # kembalikan dalam bentuk json
        return JSONResponse(user_serializer.data)

    # jika request method PUT
    elif request.method == 'PUT':
        # mengubah data json dari request body menjadi dictionary
        user_data = JSONParser().parse(request)
        # validasi data user
        user_serializer = UserSerializer(user, data=user_data)
        # jika valid simpan data user baru
        if user_serializer.is_valid():
            user_serializer.save()
            return JSONResponse(user_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method PATCH
    elif request.method == 'PATCH':
        # mengubah data json dari request body menjadi dictionary
        user_data = JSONParser().parse(request)
        # validasi data user
        user_serializer = UserSerializer(user, data=user_data, partial=True)
        # jika valid simpan data user baru
        if user_serializer.is_valid():
            user_serializer.save()
            return JSONResponse(user_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method DELETE (khusus untuk super admin)
    elif request.method == 'DELETE':
        # apabila yang mengakses bukan level super admin, return response 403
        if request.user.level != "2":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # hapus user
        user.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST']) # hanya menerima method GET dan POST
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user yang terautentikasi yang bisa mengakses
def kain_list(request):
    # jika request method GET
    if request.method == 'GET':
        # semua level user boleh mengakses
        kains = kain.objects.all()
        kains_serializer = kainSerializer(kains, many=True)
        return JSONResponse(kains_serializer.data)

    # jika request method POST
    elif request.method == 'POST':
        # apabila yang mengakses bukan level super admin dan admin, kembalikan response 403
        if request.user.level != "2" and request.user.level != "1":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ubah data json menjadi dictionary
        kain_data = JSONParser().parse(request)
        # validasi data kain
        kain_serializer = kainSerializer(data=kain_data)
        # jika valid, data akan disimpan
        if kain_serializer.is_valid():
            kain_serializer.save()
            return JSONResponse(kain_serializer.data, status=status.HTTP_201_CREATED)
        # jika tidak valid, return response 400
        return JSONResponse(kain_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE']) # hanya menerima method GET, PUT, PATCH, dan DELETE
@authentication_classes([TokenAuthentication]) # Autentikasi token
@permission_classes([IsAuthenticated]) # Hanya user terautentikasi yang bisa mengakses
def kain_detail(request, pk):
    # ambil data kain sesuai primary key (pk) data yang diakses
    try:
        Kain = kain.objects.get(pk=pk)
    # return response 404 jika user tidak ada
    except kain.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # jika request method GET
    if request.method == 'GET':
        # validasi data kain
        kain_serializer = kainSerializer(Kain)
        # kembalikan dalam bentuk json
        return JSONResponse(kain_serializer.data)

    # jika request method PUT
    elif request.method == 'PUT':
        # apabila yang mengakses bukan level super admin dan admin, kembalikan response 403
        if request.user.level != "2" and request.user.level != "1":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # mengubah data json dari request body menjadi dictionary
        kain_data = JSONParser().parse(request)
        # validasi data kain
        kain_serializer = kainSerializer(Kain, data=kain_data)
        # jika valid simpan data kain baru
        if kain_serializer.is_valid():
            kain_serializer.save()
            return JSONResponse(kain_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(kain_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method PATCH
    elif request.method == 'PATCH':
        # apabila yang mengakses bukan level super admin dan admin, kembalikan response 403
        if request.user.level != "2" and request.user.level != "1":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # mengubah data json dari request body menjadi dictionary
        kain_data = JSONParser().parse(request)
        # validasi data kain
        kain_serializer = kainSerializer(Kain, data=kain_data, partial=True)
        # jika valid simpan data kain baru
        if kain_serializer.is_valid():
            kain_serializer.save()
            return JSONResponse(kain_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(kain_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method DELETE (khusus untuk admin dan super admin)
    elif request.method == 'DELETE':
        # apabila yang mengakses bukan level admin dan super admin, return response 403
        if request.user.level != "1" and request.user.level != "2":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # hapus kain
        Kain.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST']) # hanya menerima method GET dan POST
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user yang terautentikasi yang bisa mengakses
def toko_list(request):
    # jika request method GET
    if request.method == 'GET':
        # semua level user boleh mengakses
        listToko = list_toko.objects.all()
        listToko_serializer = list_tokoSerializer(listToko, many=True)
        return JSONResponse(listToko_serializer.data)

    # jika request method POST
    elif request.method == 'POST':
        # apabila yang mengakses bukan level super admin dan admin, kembalikan response 403
        if request.user.level != "2" and request.user.level != "1":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ubah data json menjadi dictionary
        list_toko_data = JSONParser().parse(request)
        # validasi data list toko
        list_toko_serializer = list_tokoSerializer(data=list_toko_data)
        # jika valid, data akan disimpan
        if list_toko_serializer.is_valid():
            list_toko_serializer.save()
            return JSONResponse(list_toko_serializer.data, status=status.HTTP_201_CREATED)
        # jika tidak valid, return response 400
        return JSONResponse(list_toko_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE']) # hanya menerima method GET, PUT, PATCH, dan DELETE
@authentication_classes([TokenAuthentication]) # Autentikasi token
@permission_classes([IsAuthenticated]) # Hanya user terautentikasi yang bisa mengakses
def listToko_detail(request, pk):
    # ambil data kain sesuai primary key (pk) data yang diakses
    try:
        ListToko = list_toko.objects.get(pk=pk)
    # return response 404 jika user tidak ada
    except list_toko.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # jika request method GET
    if request.method == 'GET':
        # validasi data list toko
        listToko_serializer = list_tokoSerializer(ListToko)
        # kembalikan dalam bentuk json
        return JSONResponse(listToko_serializer.data)

    # jika request method PUT
    elif request.method == 'PUT':
        # apabila yang mengakses bukan level super admin dan admin, kembalikan response 403
        if request.user.level != "2" and request.user.level != "1":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # mengubah data json dari request body menjadi dictionary
        listToko_data = JSONParser().parse(request)
        # validasi data list toko
        listToko_serializer = list_tokoSerializer(ListToko, data=listToko_data)
        # jika valid simpan data list toko baru
        if listToko_serializer.is_valid():
            listToko_serializer.save()
            return JSONResponse(listToko_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(listToko_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method PATCH
    elif request.method == 'PATCH':
        # apabila yang mengakses bukan level super admin dan admin, kembalikan response 403
        if request.user.level != "2" and request.user.level != "1":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # mengubah data json dari request body menjadi dictionary
        listToko_data = JSONParser().parse(request)
        # validasi data list toko
        listToko_serializer = list_tokoSerializer(ListToko, data=listToko_data, partial=True)
        # jika valid simpan data list toko baru
        if listToko_serializer.is_valid():
            listToko_serializer.save()
            return JSONResponse(listToko_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(listToko_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method DELETE (khusus untuk admin dan super admin)
    elif request.method == 'DELETE':
        # apabila yang mengakses bukan level admin dan super admin, return response 403
        if request.user.level != "1" and request.user.level != "2":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # hapus list toko
        ListToko.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST']) # hanya menerima method GET dan POST
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user yang terautentikasi yang bisa mengakses
def detailToko_list(request):
    # jika request method GET
    if request.method == 'GET':
        # apabila yang mengakses bukan level super admin dan admin, kembalikan response 403
        if request.user.level != "2" and request.user.level != "1":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        detailToko = detail_toko.objects.all()
        detailToko_serializer = detail_tokoSerializer(detailToko, many=True)
        return JSONResponse(detailToko_serializer.data)

    # jika request method POST
    elif request.method == 'POST':
        # apabila yang mengakses bukan level super admin dan admin, kembalikan response 403
        if request.user.level != "2" and request.user.level != "1":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ubah data json menjadi dictionary
        detail_toko_data = JSONParser().parse(request)
        # validasi data detail toko
        detail_toko_serializer = detail_tokoSerializer(data=detail_toko_data)
        # jika valid, data akan disimpan
        if detail_toko_serializer.is_valid():
            detail_toko_serializer.save()
            return JSONResponse(detail_toko_serializer.data, status=status.HTTP_201_CREATED)
        # jika tidak valid, return response 400
        return JSONResponse(detail_toko_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PATCH', 'DELETE']) # hanya menerima method GET, PATCH, dan DELETE
@authentication_classes([TokenAuthentication]) # Autentikasi token
@permission_classes([IsAuthenticated]) # Hanya user terautentikasi yang bisa mengakses
def detailToko_detail(request, pk):
    # ambil data toko sesuai primary key (pk) data yang diakses
    try:
        detailToko = detail_toko.objects.get(pk=pk)
    # return response 404 jika user tidak ada
    except detail_toko.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # jika request method GET
    if request.method == 'GET':
        # validasi data detail toko
        detailToko_serializer = detail_tokoSerializer(detailToko)
        # kembalikan dalam bentuk json
        return JSONResponse(detailToko_serializer.data)

    # jika request method PATCH
    elif request.method == 'PATCH':
        # apabila yang mengakses bukan level super admin dan admin, kembalikan response 403
        if request.user.level != "2" and request.user.level != "1":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # mengubah data json dari request body menjadi dictionary
        detailToko_data = JSONParser().parse(request)
        # validasi data detail toko
        detailToko_serializer = detail_tokoSerializer(detailToko, data=detailToko_data, partial=True)
        # jika valid simpan data detail toko baru
        if detailToko_serializer.is_valid():
            detailToko_serializer.save()
            return JSONResponse(detailToko_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(detailToko_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method DELETE (khusus untuk admin dan super admin)
    elif request.method == 'DELETE':
        # apabila yang mengakses bukan level admin dan super admin, return response 403
        if request.user.level != "1" and request.user.level != "2":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # hapus detail toko
        detailToko.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
