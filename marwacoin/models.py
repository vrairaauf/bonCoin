from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.conf import settings
# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, mobile, **extra_fields):
        if not email:
            raise ValueError('email not povide')
        if not password:
            raise ValueError('password is not provided')
        user =self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, mobile, password, **extra_fields)
    def create_superuser(self, email, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, mobile, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email=models.EmailField(unique=True, max_length=255)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    mobile=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    is_staff=models.CharField(default=True, max_length=255)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    objects=CustomUserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name', 'last_name', 'mobile']
    def __str__(self):
         return self.first_name

 
class Profile(models.Model):
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone=models.IntegerField(null=True)
    adresse=models.CharField(null=True,max_length=255)
    age=models.IntegerField(null=True)
    registerCookie=models.BooleanField(default=False, null=True)
    code_verification=models.IntegerField(null=True)
    is_verified=models.CharField(max_length=20, default='non', null=True)
    slug=models.CharField(max_length=255, null=True)
    avatar=models.ImageField(blank=True, null=True, default='OIP.jpg')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True)
    deleted_at=models.DateTimeField(null=True)
    def __str__(self):
        return self.user
  

class Notification(models.Model):
    titre=models.CharField(max_length=255)
    contenu=models.TextField()
    user=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    lire=models.CharField(max_length=20,default='non')
    def __str__(self):
        return self.titre
    def extrai(self):
        return self.contenu[ : 30 ] + "..."

class Categorie(models.Model):
     titre=models.CharField(max_length=255)
     slug=models.CharField(max_length=255, default='AZERTY')
     avatar=models.ImageField(blank=True, null=True, default='OIP.jpg')
     created_at=models.DateTimeField(auto_now_add=True)
     deleted_at=models.BooleanField(default=False)
     updated_at=models.DateTimeField(auto_now_add=True ,null=True)
     def __str__(self):
         return self.titre
class firstSousCategorie(models.Model):
    titre=models.CharField(max_length=255)
    slug=models.CharField(max_length=255, default='AZERTY')
    avatar=models.ImageField(blank=True, null=True, default='OIP.jpg')
    categorie=models.ForeignKey(Categorie,null=True, related_name="categorie",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    deleted_at=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now_add=True ,null=True)
    def __str__(self):
        return self.titre
class secondSousCategorie(models.Model):
    titre=models.CharField(max_length=255)
    slug=models.CharField(max_length=255, default='AZERTY')
    avatar=models.ImageField(blank=True, null=True, default='OIP.jpg')
    firstCategore=models.ForeignKey(firstSousCategorie, null=True, related_name="firstCategorie",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    deleted_at=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now_add=True ,null=True)
    def __str__(self):
        return self.titre
class Produit(models.Model):
    METHODE={
    ('vente', 'vente'),
    ('louer', 'louer'),
    ('échange', 'échange'),
    ('donation', 'donation')
    }
    ETAT={
        ('occasion', 'occasion'),
        ('bon état', 'bon état'),
        ('presq neuf', 'presq neuf'),
        ('neuf', 'neuf')
    }
    entete=models.CharField(max_length=255)
    contenu=models.TextField(null=True)
    prix=models.FloatField(null=True)
    quantite=models.IntegerField(null=True)
    operation=models.CharField(max_length=255, choices=METHODE, default='vente')
    location=models.CharField(max_length=255, null=True)
    user=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    categorie=models.ForeignKey(Categorie, null=True, on_delete=models.CASCADE)
    firstSousCat=models.ForeignKey(firstSousCategorie, null=True, on_delete=models.CASCADE)
    secondSousCat=models.ForeignKey(secondSousCategorie, null=True, on_delete=models.CASCADE)
    affiche=models.ImageField(blank=True, null=True, default='OIP.jpg')
    vendu=models.BooleanField(default=False)
    etat=models.CharField(max_length=255, choices=ETAT, null=True, default="normal")
    slug=models.CharField(max_length=255, null=True)
    created_at=models.DateTimeField(auto_now_add=True, null=True)
    deleted_at=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now_add=True ,null=True)
    def extrai(self):
        return self.contenu[ : 40] + " ..."
    def __str__(self):
        return self.entete

class helperWord(models.Model):
    word=models.CharField(max_length=255)
    produit=models.ManyToManyField(Produit)
    created_at=models.DateTimeField(auto_now_add=True)
    deleted_at=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now_add=True ,null=True)
class vendeur(models.Model):
    user=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    prixDelivration=models.IntegerField(null=True)
    oui_condition=models.BooleanField(default=False)
    Paypal_business=models.CharField(null=True, max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    deleted_at=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now_add=True ,null=True)
class ImageProduit(models.Model):
    image=models.ImageField(blank=True, null=True, default='OIP.jpg')
    produit=models.ForeignKey(Produit, null=True, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    deleted_at=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now_add=True ,null=True)
class IpMembre(models.Model):
    ip=models.CharField(max_length=255, null=True)
    timeZone=models.CharField(max_length=255, null=True)
    location=models.CharField(max_length=255, null=True)
    continent=models.CharField(max_length=255, null=True)
    created_at=models.DateTimeField(auto_now_add=True, null=True)
    user=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    nationalite=models.CharField(max_length=255, null=True)


class Emailer(models.Model):
    email=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    deleted_at=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now_add=True ,null=True)
class Contact(models.Model):
    CAUSE={
    ('Un contract de partenariat', 'Un contract de partenariat'),
    ('Signaler un probléme', 'Signaler un probléme'),
    ('Suggérer une fonctionnalité', 'Suggérer une fonctionnalité'),

    }
    nom=models.CharField(max_length=255,null=True)
    email=models.CharField(max_length=255)
    message=models.TextField()
    cause=models.CharField(max_length=255,null=True, choices=CAUSE)
    created_at=models.DateTimeField(auto_now_add=True)
    lire=models.BooleanField(default=False)
class Enregistre(models.Model):
    user=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    produit=models.ForeignKey(Produit, null=True, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    deleted_at=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now_add=True ,null=True)
class Commande(models.Model):
    user=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    produit=models.ForeignKey(Produit, null=True, on_delete=models.CASCADE)
    nbPiece=models.IntegerField(null=True, default=1)
    destination=models.CharField(null=True, max_length=500)
    paid=models.BooleanField(default=False)
    livre=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    deleted_at=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now_add=True ,null=True)
