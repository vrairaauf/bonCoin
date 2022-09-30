from django.forms import ModelForm
from .models import *
from django.contrib.auth import get_user_model
User=get_user_model()
from django.contrib.auth.forms import UserCreationForm

class CreateNewUser(UserCreationForm):
	class Meta:
		model=User
		fields=['first_name', 'email', 'password1', 'password2']

class ProfileFormDebut(ModelForm):
	class Meta:
		model=Profile
		fields=['user', 'code_verification', 'slug']


class ProfileRegisterForm(ModelForm):
	class Meta:
		model=Profile
		fields=['is_verified']
class ProfileForm(ModelForm):
	class Meta:
		model=Profile
		fields=['adresse', 'age', 'phone', 'avatar']

#ajouter un vendeur
class AjoutVendeurForm(ModelForm):
	class Meta:
		model=vendeur
		fields=['user', 'oui_condition', 'Paypal_business']
class ProduitForm(ModelForm):
	class Meta:
		model=Produit
		fields=['entete', 'categorie','user', 'etat', 'firstSousCat', 'secondSousCat', 'quantite', 'contenu','operation', 'prix', 'location', 'slug']
class FormIp(ModelForm):
	class Meta:
		model=IpMembre
		fields=['ip', 'user', 'nationalite', 'timeZone', 'continent', 'location']
class ImageProduitForm(ModelForm):
	class Meta:
		model=ImageProduit
		fields=['image', 'produit']
class EmailerForm(ModelForm):
	class Meta:
		model=Emailer
		fields=['email']
class ContactForm(ModelForm):
	class Meta:
		model=Contact
		fields=['nom','email', 'message', 'cause']

class EnregistrerForm(ModelForm):
	class Meta:
		model=Enregistre
		fields=['user', 'produit']
class CategorieForm(ModelForm):
	class Meta:
		model=Categorie
		fields=['titre', 'slug', 'avatar']

class FirstSousCategorieForm(ModelForm):
	class Meta:
		model=firstSousCategorie
		fields=['titre', 'slug', 'avatar', 'categorie']
class SecondSousCategorieForm(ModelForm):
	class Meta:
		model=secondSousCategorie
		fields=['titre', 'slug', 'avatar', 'firstCategore']		
class ProfileFormLogin(ModelForm):
	class Meta:
		model=Profile
		fields=['user', 'code_verification']

