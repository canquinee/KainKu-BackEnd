from rest_framework import serializers
#polanya = from (nama folder yang menyimpan app1; dimana app1 itu merupakan app yang diunduh menggunakan command python manage.py startapp app1).
#models import (nama class yang terdapat pada models.py)
from appTubesPI.models import User
from appTubesPI.models import list_toko
from appTubesPI.models import detail_toko
from appTubesPI.models import kain
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.Serializer):
    # id tidak akan diubah (read only)
    pk = serializers.IntegerField(read_only=True)
    # validasi data - data yang akan disimpan ke tabel
    email = serializers.EmailField(max_length = 100)
    username = serializers.CharField(max_length = 50)
    password = serializers.CharField(max_length = 100, allow_null = True) 
    address = serializers.CharField(max_length = 255)
    level = serializers.ChoiceField(choices = [("2", "Super Admin"), ("1", "Admin"),("0", "Customer"),], default = "0")

    #or you can use this :
    #fields = '__all__' (to indicate that all fields in the model should be used.)

    # fungsi ketika melakukan CREATE
    def create(self, validated_data):
        # menyimpan password ke dalam sebuah variabel password
        password = validated_data.pop('password', None)
        # jika password ada (tidak kosong)
        if password is not None:
            # password dihash sebelum disimpan ke tabel
            validated_data['password'] = make_password(password)
        # Simpan ke tabel user
        return User.objects.create(**validated_data)
    
    #fungsi update data user
    def update(self, instance, validated_data):
        # Mengganti data lama dengan data baru yang sudah valid kecuali data password
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.level = validated_data.get('level', instance.level)
        # Update data password jika ada
        password = validated_data.get('password')
        if password:
            instance.password = make_password(password)
        # Menyimpan data baru ke tabel user
        instance.save()
        return instance
    
class list_tokoSerializer(serializers.Serializer):
    # id tidak akan diubah (read only)
    pk = serializers.IntegerField(read_only=True)
    # validasi data - data yang akan disimpan ke tabel
    nama_toko = serializers.CharField(max_length = 255)
    lokasi = serializers.CharField(max_length = 255)
    jamBuka_operasional = serializers.TimeField()
    jamTutup_operasional = serializers.TimeField()
    # contact_person = serializers.CharField(max_length = 255, unique = True)
    contact_person = serializers.CharField(max_length = 255)

    def create(self, validated_data):
        # Menyimpan data yang valid ke tabel list_toko
        return list_toko.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Mengganti data lama dengan data baru yang sudah valid
        instance.nama_toko = validated_data.get('nama_toko', instance.nama_toko)
        instance.lokasi = validated_data.get('lokasi', instance.lokasi)
        instance.jamBuka_operasional = validated_data.get('jamBuka_operasional', instance.jamBuka_operasional)
        instance.jamTutup_operasional = validated_data.get('jamTutup_operasional', instance.jamTutup_operasional)
        instance.contact_person = validated_data.get('contact_person', instance.contact_person)
        # Menyimpan data baru ke tabel shop
        instance.save()
        return instance
    
class kainSerializer(serializers.Serializer):
    # id tidak akan diubah (read only)
    pk = serializers.IntegerField(read_only=True)
    # validasi data - data yang akan disimpan ke tabel
    name = serializers.CharField(max_length = 100)
    desc = serializers.CharField(max_length = 299)
    img = serializers.CharField()
    lowest_est = serializers.IntegerField()
    highest_est = serializers.IntegerField()

    def create(self, validated_data):
        # menyimpan data kain valid ke tabel
        return kain.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Mengganti data lama dengan data baru yang sudah valid
        instance.name = validated_data.get('name', instance.name)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.img = validated_data.get('img', instance.img)
        instance.lowest_est = validated_data.get('lowest_est', instance.lowest_est)
        instance.highest_est = validated_data.get('highest_est', instance.highest_est)
        # Menyimpan data baru ke tabel shop
        instance.save()
        return instance

class UserLoginSerializer(serializers.Serializer):
    # validasi data - data yang akan digunakan untuk login
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100, write_only=True)

class detail_tokoSerializer(serializers.Serializer):
    # id tidak akan diubah (read only)
    pk = serializers.IntegerField(read_only=True)
    # validasi data - data yang akan disimpan ke tabel
    harga = serializers.IntegerField()
    id_kain = kainSerializer(read_only = True)
    id_toko = list_tokoSerializer(read_only = True)
    #id_toko = serializers.PrimaryKeyRelatedField(queryset=list_toko.objects.all())

    def create(self, validated_data):
        # menyimpan data dari id_toko ke kolom id_toko pada data yang divalidasi
        id_toko = self.initial_data.get("id_toko")
        try:
            # Retrieve the "list_toko" instance based on the ID
            list_toko_instance = list_toko.objects.get(pk=id_toko)
        except list_toko.DoesNotExist:
            # Handle the case when the "list_toko" instance doesn't exist
            raise serializers.ValidationError("Invalid 'id_toko' provided")
        # Assign the retrieved "list_toko" instance to the "id_toko" field
        validated_data["id_toko"] = list_toko_instance

        # menyimpan data dari id_kain ke kolom id_kain pada data yang divalidasi
        id_kain = self.initial_data.get("id_kain")
        try:
            # Retrieve the "kain" instance based on the ID
            kain_instance = kain.objects.get(pk=id_kain)
        except list_toko.DoesNotExist:
            # Handle the case when the "kain" instance doesn't exist
            raise serializers.ValidationError("Invalid 'id_kain' provided")
        # Assign the retrieved "kain" instance to the "id_toko" field
        validated_data["id_kain"] = kain_instance

        # Menyimpan data yang valid ke tabel detail_toko
        return detail_toko.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # menyimpan data dari id_toko ke kolom id_toko pada data yang divalidasi
        id_toko = self.initial_data.get("id_toko")
        # menyimpan data dari id_kain ke kolom id_kain pada data yang divalidasi
        id_kain = self.initial_data.get("id_kain")
        # update data id_toko jika ada pada request body
        if id_toko:
            instance.id_toko = id_toko
        # update data id_kain jika ada pada request body
        if id_kain:
            instance.id_kain = id_kain
        # Mengganti data lama dengan data baru yang sudah valid
        instance.harga = validated_data.get('harga', instance.harga)
        # Menyimpan data baru ke tabel shop
        instance.save()
        return instance
    