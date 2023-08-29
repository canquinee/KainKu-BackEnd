from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # 3 Pilihan Level User
    class LoginLevel(models.TextChoices):
        SUPERADMIN = "2", "Super Admin"
        ADMIN = "1", "Admin"
        CUSTOMER = "0", "Customer"
  
    # Email unik setiap user
    email = models.EmailField(max_length = 100, unique = True)
    # Username unik setiap user
    username = models.CharField(max_length = 50, unique = True)
    # Password (akan dihash ketika disimpan ke database)
    # password = models.CharField(max_length = 100, null = True)
    password = models.CharField(max_length = 100)
    # alamat user
    address = models.CharField(max_length = 255)
    # Level User (3 pilihan)
    level = models.CharField(max_length = 1, choices = LoginLevel.choices, default = LoginLevel.CUSTOMER)

    # mengembalikan nama username ketika object dibuat
    def __str__(self):
        return self.username

    # Urut berdasarkan usernama
    class Meta:
        ordering = ('level',)

class list_toko(models.Model):
    #nama toko
    nama_toko = models.CharField(max_length = 50)
    #lokasi toko
    lokasi = models.CharField(max_length = 50)
    #waktu kerja operasional
    jamBuka_operasional = models.TimeField(default='00:00:00')
    jamTutup_operasional = models.TimeField(default='00:00:00')
    #contact person (nomor telepon pihak penting dari toko)
    # contact_person = models.CharField(max_length = 20, unique = True)
    contact_person = models.CharField(max_length = 20)
    
class kain(models.Model):
    #nama kain
    name = models.CharField(max_length = 100)
    #deskripsi terkait kain yang tersedia
    desc = models.TextField(max_length = 299)
    #referensi gambar melalui link
    img = models.TextField()
    #perkiraan harga terendah
    lowest_est = models.BigIntegerField()
    #perkiraan harga tertinggi
    highest_est = models.BigIntegerField()

    #special method __str__ used to provide a string representation of an object. Mengembalikan nama jenis kain ketika objectnya telah dibuat
    def __str__(self) -> str:
        return self.name

class detail_toko(models.Model):
    #harga dari kain yang dijual pada suatu toko
    harga = models.BigIntegerField()
    #id toko dan id kain merupakan Foreign key yang digunakan pada table detail_toko
    id_toko = models.ForeignKey(list_toko, on_delete=models.CASCADE)
    id_kain = models.ForeignKey(kain, on_delete=models.CASCADE)


