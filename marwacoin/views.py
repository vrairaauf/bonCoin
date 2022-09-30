from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .decorators import notLoggedUser, allowed_users, notLoggedAuteur
from math import *
from django.core.mail import send_mail
from random import *
import time
from datetime import datetime
import requests
from django.conf import settings
from django.http import JsonResponse
from .tache import *
from django.contrib.gis.geoip2 import GeoIP2
from geoip import geolite2
from django.core.paginator import Paginator
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim
from .filters import *

# Create your views here.
def estIlFonctionneDansCetpaye(ip):
	test="126.53.24.5"#remplacer par ip aux environnement de production
	lookup=geolite2.lookup(test)
	if lookup.continent=="AS":
		return True
	else:
		return False
@notLoggedUser
def principal(request):
	produit=Produit.objects.all()
	p=Paginator(Produit.objects.all().filter(deleted_at=False), 10)
	page=request.GET.get('page')
	produits_list=p.get_page(page)
	emailer=EmailerForm()
	message=''
	diffrentCategorie=Categorie.objects.all()
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}

	if request.method=='POST':
		email=Emailer.objects.filter(email=request.POST.get('email'))
		sauvegarde=True
		for item in email:
			if item.email==request.POST.get('email'):
				messages.error(request,"Cet Email est déja trouvée")
				sauvegarde=False
				break
		emailer=EmailerForm(request.POST)
		if emailer.is_valid() and sauvegarde:
			emailer.save()
			messages.success(request,"Votre Email est insérer avec succées")

	context={
		'form':emailer,
		'message':message,
		'categorie':diffrentCategorie,
		'meta':donneeUtile,
		'produit':produit,
		'produits_list':produits_list,
		'longPagination':range(produits_list.paginator.num_pages)
	}
	return render(request, 'visiteur/principal.html', context)

def categoriesDetail(request, slugCatPrincipal):
	try:
		profil=Profile.objects.get(user=request.user.id)
	except Profile.DoesNotExist:
		profil=None
	categoriePrincipal=Categorie.objects.get(slug=slugCatPrincipal)
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	articlePerCategorie=ProduitFilter(request.GET ,queryset=Produit.objects.filter(categorie=categoriePrincipal.id).filter(deleted_at=False).exclude(user = request.user.id))
	FirstSouscat=firstSousCategorie.objects.filter(categorie=categoriePrincipal.id)
	p=Paginator(articlePerCategorie.qs, 2)
	page=request.GET.get('page')
	produits_list=p.get_page(page)
	context={
		'produit':articlePerCategorie,
		'search':ProduitFilter(),
		'categorie':categoriePrincipal,
		'meta':donneeUtile,
		'FirstSouscat':FirstSouscat,
		'produits_list':produits_list,
		'meta':donneeUtile,
		'profile':profil,
		'estIlVendeur':getVendeur(request),
		'longPagination':range(produits_list.paginator.num_pages),
	}
	return render(request, 'visiteur/detail.html', context)

def firstSouscategoriesDetail(request, slugCatPrincipal, slugCatSecondaire):
	try:
		profil=Profile.objects.get(user=request.user.id)
	except Profile.DoesNotExist:
		profil=None
	categoriePrincipal=Categorie.objects.get(slug=slugCatPrincipal)
	categorieSecondaire=firstSousCategorie.objects.get(slug=slugCatSecondaire)
	articlePerFirstCategorie=ProduitFilter(request.GET ,queryset=Produit.objects.filter(categorie=categoriePrincipal.id).filter(firstSousCat=categorieSecondaire.id).filter(deleted_at=False).exclude(user=request.user.id))
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	secondSousCat=secondSousCategorie.objects.filter(firstCategore=categorieSecondaire.id)
	p=Paginator(articlePerFirstCategorie.qs, 6)
	page=request.GET.get('page')
	produits_list=p.get_page(page)
	context={
	 	'meta':donneeUtile,
	 	'search':ProduitFilter(),
	 	'produit':articlePerFirstCategorie,
	 	'categorie': categoriePrincipal,
	 	'firstSousCat':categorieSecondaire,
	 	'secondSousCat':secondSousCat,
	 	'produits_list':produits_list,
	 	'meta':donneeUtile,
	 	'profile':profil,
	 	'estIlVendeur':getVendeur(request),
	 	'longPagination':range(produits_list.paginator.num_pages)
	 	
	}
	return render(request, 'visiteur/sdetail.html', context)

def secondSousCategoriesDetail(request, slugCatPrincipal, slugCatSecondaire, slugCatThird):
	try:
		profil=Profile.objects.get(user=request.user.id)
	except Profile.DoesNotExist:
		profil=None
	categoriePrincipal=Categorie.objects.get(slug=slugCatPrincipal)
	categorieSecondaire=firstSousCategorie.objects.get(slug=slugCatSecondaire)
	secondSousCat=secondSousCategorie.objects.get(slug=slugCatThird)
	articlePerSecondCategorie=ProduitFilter(request.GET ,queryset=Produit.objects.filter(categorie=categoriePrincipal.id).filter(firstSousCat=categorieSecondaire.id).filter(secondSousCat=secondSousCat.id).filter(deleted_at=False).exclude(user=request.user.id))
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	p=Paginator(articlePerSecondCategorie.qs, 2)
	page=request.GET.get('page')
	produits_list=p.get_page(page)
			
	context={
		'meta':donneeUtile,
		'search':ProduitFilter(),
	 	'produit':articlePerSecondCategorie,
	 	'categorie': categoriePrincipal,
	 	'firstSousCat':categorieSecondaire,
	 	'secondSousCat':secondSousCat,
	 	'produits_list':produits_list,
	 	'profile':profil,
	 	'estIlVendeur':getVendeur(request),
	 	'longPagination':range(produits_list.paginator.num_pages)

	}
	return render(request, 'visiteur/ssdetail.html', context)
@notLoggedUser
def user_login(request):
		if request.method=='POST':
			email=request.POST.get('email')
			password=request.POST.get('password')
			user=authenticate(request, email=email, password=password)
			if user is not None:
				login(request, user)
				profile=Profile.objects.get(user=user.id)
				if profile.is_verified=='non':
					code=randint(11111, 99999)
					send_mail(
					'Code de verification de compte sur test1',
					'votre code de verification est de compte'+str(code),
					'vrairaaufabidi@gmail.com',
					[user.email],

					)
					donne={'user' : user.id , 'code_verification' : code}
					form_profile=ProfileFormLogin(donne, instance=user)
					if form_profile.is_valid():
						form_profile.save()
					messages.success(request, 'Code de verification est envoie a votre email')
					return redirect('verification_de_compte')
				
				group=request.user.groups.all()[0].name
				if group == 'visiteur' or group=='vendeur':
					return redirect('home_page')
				
				elif group=='admin':
					return redirect('admin_home')
				
			else:
				messages.info(request, "Error ce compte introuvable")
			
		context={}
		return render(request, 'visiteur/login.html', context)
@notLoggedUser
def register(request):
		form=CreateNewUser()
		form_profile=ProfileRegisterForm()
		if request.method=='POST':
			form=CreateNewUser(request.POST)
			if form.is_valid():
				recaptcha_response=request.POST.get('g-recaptcha-response')
				data={
					'secret':settings.GOOGLE_RECAPTCHA_SECRET_KEY,
					'response': recaptcha_response
				}
				r=requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
				result=r.json()
				if result['success']:
					user=form.save()
					username=form.cleaned_data.get('first_name')
					
					email=form.cleaned_data.get('email')
					nouveau_user=User.objects.get(email=email)
					code=randint(11111, 99999)
					send_mail(
					'Code de verification de compte sur test1',
					'votre code de verification est de '+str(code),
					'minimalistplatform@gmail.com',
					[email],

					)
					emailer=EmailerForm({'email':email})
					emailer.save()

					login(request, nouveau_user)
					slug=time.time()
					slug=str(slug)
					slug=slug.replace('.', '')
					donne={'user' : request.user.id , 'code_verification' : code, 'slug':slug}
					form_profile=ProfileFormDebut(donne)

					if form_profile.is_valid():
						form_profile.save()
					messages.success(request, username+'Created Successfully')
					return redirect('verification_de_compte')
				else:
					messages.error(request, 'INVALID RECAPTCHA')
			
		context={'form':form}
		return render(request, 'visiteur/register.html', context)

@login_required(login_url='login')
def verification_de_compte(request):
	profile=Profile.objects.get(user=request.user.id)
	requete=None
	if request.method=='POST':
		code_donne_par_user=request.POST.get('codedeverification')
		#requete=Profile.objects.raw('SELECT * FROM site1_profile WHERE code_verification=%s AND user=%s', [code_donne_par_user, request.user.id])
		try:
			requete=Profile.objects.get(user=request.user.id, code_verification=code_donne_par_user)
		except Profile.DoesNotExist:
			requete=None

		if requete is None:
			messages.error(request, 'Ce code est introuvable ')
		else:
			user=User.objects.get(id=request.user.id)
			group=Group.objects.get(name='visiteur')
			user.groups.add(group)
			donne={'is_verified':'oui'}
			profile_form=ProfileRegisterForm(donne, instance=profile)
			profile_form.save()
			iptable=FormIp()
			iptable=FormIp(remplirDonne(request.META.get('REMOTE_ADDR'), request.user.id))
			print(request.META.get('REMOTE_ADDR'), request.user.id)
			if iptable.is_valid():
				iptable.save()
				
			return redirect('home_page')
			
	context={'profile':profile, 'requete':requete}
	return render(request, 'visiteur/verifier_compte.html', context)

 
def user_logout(request):
	logout(request)
	return redirect('principal')
def getVendeur(request):
	try:
		vendeurr=vendeur.objects.get(user=request.user.id)
	except vendeur.DoesNotExist:
		vendeurr=None
	if vendeurr is None:
		estIlVendeur=False
	else:
		estIlVendeur=True
	return estIlVendeur
def indexFunction(request):
	context={}
	return render(request, 'visiteur/index.html', context)
@login_required(login_url='login')
def landing_page(request):
	if request.method=='POST':
		print(request.POST.get('modele'))
	profil=Profile.objects.get(user=request.user.id)
	if profil.is_verified=='non':
		return redirect('logout')
	#en va sauvegarder lutilisateur dans la table de membre en ligne
	notifications=Notification.objects.filter(user=request.user.id).filter(lire='non')
	produit=ProduitFilter(request.GET ,queryset=Produit.objects.all().filter(deleted_at=False).exclude(user=request.user.id))
	p=Paginator(produit.qs, 2)
	page=request.GET.get('page')
	produits_list=p.get_page(page)
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	diffrentCategorie=Categorie.objects.all()
	fichier=open('static/files/nb_visite', 'r')
	nb_visite=fichier.read()
	fichier=open('static/files/nb_visite', 'w+')
	nb_visite=int(nb_visite)+1
	fichier.write(str(nb_visite))
	fichier.close()
	
	context={
		'estIlVendeur':getVendeur(request),
		'search':ProduitFilter(),
		'profile':profil,
		'meta':donneeUtile,
		'categorie':diffrentCategorie,
		'produit':produit,
		'produits_list':produits_list,
		'notifications':notifications,
		'longPagination':range(produits_list.paginator.num_pages)
		
		}
	if request.method=='POST':
		profil.registerCookie=True
		profil.save()
	return render(request, 'visiteur/landing.html', context)
@allowed_users(allowedGroups=['vendeur', 'visiteur', 'admin'])
@login_required(login_url='login')
def voirMesEnreg(request):
	profil=Profile.objects.get(user=request.user.id)
	enreg=Enregistre.objects.filter(user=request.user.id)
	produits=[]
	for item in enreg:
		produit=Produit.objects.get(id=item.produit.id)
		produits.append(produit)

	context={
		'estIlVendeur':getVendeur(request),
		'produits':produits,
		'profile':profil,
	}
	return render(request, 'visiteur/enregistrement.html', context)
@allowed_users(allowedGroups=['vendeur', 'visiteur', 'admin'])
@login_required(login_url='login')
def deleteProductFromEnreg(request, slug):
	try:
		enreg=Enregistre.objects.filter(produit=slug, user=request.user.id)
	except Enregistre.DoesNotExist:
		enreg=None
	if enreg is not None:
		enreg.delete()
		messages.success(request, 'le produit est supprimer avec sucées')
		return redirect('home_page')
	else:
		messages.error(request, 'vous navez pas ce produits dans votre enregistrements')
		return redirect('home_page')
@allowed_users(allowedGroups=['vendeur', 'visiteur', 'admin'])
@login_required(login_url='login')
def getMesProduitsVendu(request):
	mesProduits=Produit.objects.filter(user=request.user.id)
	idProduit=[]
	listProduitsVenduParUser=[]
	if mesProduits:
		for item in mesProduits:
			idProduit.append(item.id)
		for item in idProduit:
			produit=Commande.objects.filter(produit=item)
			if produit:
				for item in produit:
					listProduitsVenduParUser.append(item)
		return listProduitsVenduParUser
	else:
		return False
@allowed_users(allowedGroups=['vendeur', 'visiteur', 'admin'])
@login_required(login_url='login')
def mesProduitsVendu(request):
	profile=Profile.objects.get(user=request.user.id)
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	context={
		'meta':donneeUtile,
		'profile':profile,
		'produits':getMesProduitsVendu(request),
		'estIlVendeur':getVendeur(request)

	}
	return render(request, 'annonceur/vendu.html', context)
@allowed_users(allowedGroups=['vendeur', 'visiteur', 'admin'])
@login_required(login_url='login')
def profile(request):
	profile=Profile.objects.get(user=request.user.id)
	if profile.is_verified=='non':
		return redirect('logout')
	mesCommandes=Commande.objects.filter(user=request.user.id)
	aDesEnreg=Enregistre.objects.filter(user=request.user.id)
	
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	context={'profile':profile, 'meta':donneeUtile, 'estIlVendeur':getVendeur(request), 'aDesEnreg':aDesEnreg, 'mesCommandes':mesCommandes, 'produitVendu':getMesProduitsVendu(request)}
	return render(request, 'visiteur/profile.html', context)
@allowed_users(allowedGroups=['vendeur', 'visiteur', 'admin'])
@login_required(login_url='login')
def profile_update(request):
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	profile=Profile.objects.get(user=request.user.id)
	form=ProfileForm(instance=profile)
	if request.method=='POST':
		form=ProfileForm(request.POST, request.FILES ,instance=profile)
		if form.is_valid():
			form.save()
			return redirect('profile')
	context={'form':form, 'profile':profile, 'meta':donneeUtile, 'estIlVendeur':getVendeur(request)}
	return render(request, 'visiteur/update_profile.html', context)
	
@allowed_users(allowedGroups=['admin', 'visiteur'])
@login_required(login_url='login')
def passeModeAnnonceur(request):
	profile=Profile.objects.get(user=request.user.id)
	form=AjoutVendeurForm()

	if request.method=='POST':
		if request.POST.get('oui_condition'):
			if request.POST.get('paypalBus'):
				comptePaypalBusiness=request.POST.get('paypalBus')
			else:
				comptePaypalBusiness=settings.PAYPAL_RECEIVER_EMAIL

			donne={'user':request.user.id, 'oui_condition':request.POST.get('oui_condition'), 'Paypal_business':comptePaypalBusiness, 'prixDelivration':request.POST.get('prixDelivration')}
			form=AjoutVendeurForm(donne)
			if form.is_valid():
				form.save()
				group=Group.objects.get(name='vendeur')
				request.user.groups=group
				messages.success(request, 'Votre demande de devenir un vendeur sur Minimalist est enregistrée avec succée ')
				return redirect('home_page')
		else:
			messages.error(request, 'Erreur vos informations sont invalident')
			return redirect('home_page')
	context={
		'profile':profile,
		'form':form
	}
	return render(request, 'visiteur/etrevendeur.html', context)

@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def choisirCatPourAnnonce(request):
	categories=Categorie.objects.all()
	context={
		"categories":categories,
	}
	if request.method=="POST":
		if request.POST.get("catPrincipal"):
			return redirect("choisitFirstCatPourAnnonce", request.POST.get("catPrincipal"))
		messages.error(request, 'Veiller choisir une categorie pour votre produit')
	return render(request, "annonceur/choisirCatPourAnnonce.html", context)

@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def choisitFirstCatPourAnnonce(request, pk):
	try:
		firstCat=firstSousCategorie.objects.filter(categorie=pk)
	except firstSousCategorie.DoesNotExist:
		messages.error(request, "cette categorie n'existe pas")
		return redirect("choisirCatPourAnnonce")
	context={
		"categories":firstCat,
	}
	if request.method=='POST':
		if request.POST.get('catSecondaire'):
			return redirect("choisirSecondCatPourAnnonce", request.POST.get("catSecondaire"))
		messages.error("veiller continuer la séléction des catégorie pour terminer votre annonce")
	return render(request, 'annonceur/choisitFirstCatPourAnnonce.html', context)
@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def choisirSecondCatPourAnnonce(request,pk):
	try:
		secondesCat=secondSousCategorie.objects.filter(firstCategore=pk)
	except secondSousCategorie.DoesNotExist:
		messages.error(request, "cette categorie n'existe pas")
		return redirect("choisirCatPourAnnonce")
	context={
		"categories": secondesCat,
	}
	if request.method=='POST':
		if request.POST.get("catFinale"):
			return redirect("creerAutreInfoPourAnnonce", request.POST.get("catFinale"))
		messages.error('veiller selectionner une categorie pour terminer la distrubition de votre annonces')

	return render(request, 'annonceur/choisirSecondeCatPourAnnonce.html', context)
def slug_generator():
	return "identifientunique"
@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def creerAutreInfoPourAnnonce(request, pk):
	try:
		sousCategories=secondSousCategorie.objects.get(id=pk)
	except secondSousCategorie.DoesNotExist:
		print("cette categorie n'existe pas")
		return redirect('publierAnnonce')
	form=ProduitForm()
	modele=open('static/files/models/{}.data'.format(sousCategories.titre), 'r', encoding='utf8')
	retour=modele.readlines()
	modele.close()
	context={
		'retour':retour,
		'form':form,
		'estIlVendeur':getVendeur(request),
	}
	if request.method=='POST':
		#'entete', 'categorie','user', 'etat', 'firstSousCat', 'secondSousCat', 'quantite', 'contenu','operation', 'prix', 'location', 'slug'
		firstSousCat=secondSousCategorie.objects.get(id=pk).firstCategore
		print(request.POST)
		slug=slug_generator()
		donnee={
			"csrfmiddlewaretoken": request.POST.get("csrfmiddlewaretoken"),
			"entete": request.POST.get("entete"),
			"etat": request.POST.get("etat"),
			"prix": request.POST.get("prix"),
			"quantite": request.POST.get("quantite"),
			"user": request.user.id,
			"operation": request.POST.get("operation"),
			"contenu": request.POST.get("contenu"),
			"location": request.user.address,
			"secondSousCat": pk,
			"firstSousCat": firstSousCat.id,
			"categorie": firstSousCategorie.objects.get(titre=firstSousCat).categorie.id,
			"operation":request.POST.get("operation"),
			"slug":slug,
		}
		formAnnonce=ProduitForm(donnee)
		if formAnnonce.is_valid():
			try:
				formAnnonce.save()
				#messages.success(request,"votre produit est publier avec succées")
				return redirect("publierAnnonceImage")
			except:
				return redirect("publierAnnonceImage")
		messages.error(request,"veiller inserer tous vos champs")
	return render(request, 'annonceur/createContenuAnnonceAvecModele.html', context)

@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def publierAnnonce(request):
	profile=Profile.objects.get(user=request.user.id)
	categorie=Categorie.objects.all()
	ip=IpMembre.objects.filter(user=request.user.id)
	
	form=ProduitForm()
	image=ImageProduitForm()
	context={
		'form':form,
		'image':image,
		'ipmembre':ip,
		'categorie':categorie,
		'slug':getSlug(),
		'profile':profile
		}
	if request.method=='POST': 
		donne=request.POST
		form=ProduitForm(donne)
		if form.is_valid():
			form.save()
			messages.success(request, 'Votre produit est enregistée avec succées')
			
			return redirect("choisirUnModele", pk=request.POST.get("secondSousCat"), idprod=Produit.objects.filter(user=request.user.id).latest(field_name=None))
		else:
			messages.error(request, 'Veiller valider vos données ')
			print("le formulaire incorrect")
	return render(request, 'annonceur/publierAnnonce.html', context)

@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def createContenuAnnonceAvecModele(request, pk, idprod):
	print("le code est ici dans la nouvele fonction")
	try:
		sousCategories=secondSousCategorie.objects.get(id=pk)
	except secondSousCategorie.DoesNotExist:
		print("cette categorie n'existe pas")
		return redirect('publierAnnonce')
	try:
		produit=Produit.objects.get(id=pk)
	except Produit.DoesNotExist:
		return redirect("publierAnnonce")
	form=ProduitForm(instance=produit)
	if request.method=='POST':
		form=ProduitForm(request.POST, instance=produit)
		if form.is_valid():
			form.save()
			produit.contenu=request.POST.get("modeleContenu")
			return redirect("publierAnnonceImage")
	modele=open('static/files/models/{}.data'.format(sousCategories.titre), 'r', encoding='utf8')
	retour=modele.readlines()
	modele.close()
	context={
		'retour':retour,
		'form':form,
		'estIlVendeur':getVendeur(request),
	}
	return render(request, 'annonceur/createContenuAnnonceAvecModele.html', context)
def publierAnnonceImage(request):
	profile=Profile.objects.get(user=request.user.id)
	produit=Produit.objects.filter(user=request.user.id).latest('id')
	image=ImageProduitForm()
	if request.method=='POST':
		images=request.FILES.getlist('images')
		print(images)
		for item in images:
			ImageProduit(image=item, produit=produit).save()
			print(item)
		#update de produit
		produit.affiche=images[0]
		slug=time.time()
		slug=str(slug)
		slug=slug.replace('.', '')
		produit.slug=slug
		produit.save()
		messages.success(request, 'Votre produit est publier avec succées')
		return redirect('home_page')
		
	context={
		'image':image,
		'profile':profile,
		'estIlVendeur':getVendeur(request)
	}
	return render(request, 'annonceur/publierAnnonceImage.html', context)
#des taches ajax
@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def obtenirSousCategorie(request,pk):
	sousCategories=firstSousCategorie.objects.filter(categorie=pk)
	data={}
	i=1
	for item in sousCategories:
		data[i]=[item.id, item.titre]
		i+=1
	return JsonResponse(data)
@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def obtenirSecondSousCategorie(request, pk):
	sousCategories=secondSousCategorie.objects.filter(firstCategore=pk)
	data={}
	i=1
	for item in sousCategories:
		data[i]=[item.id, item.titre]
		i+=1
	return JsonResponse(data)
#__________________________
#les pages statique de site
def apropos(request):
	if request.user.is_authenticated:
		context={
			'profile':Profile.objects.get(user=request.user.id)
		}
	else:
		context={}
	return render(request, 'statique/apropos.html', context)
def visiteurContact(request):
	if request.user.is_authenticated:
		profile=Profile.objects.get(user=request.user.id)
	else:
		profile=None
	formContact=ContactForm()
	if request.method=='POST':
		print(request.POST.get('nom'))
		print(request.POST.get('cause'))
		donne={'nom':request.POST.get('nom'),"email":request.POST.get('email'), "message":request.POST.get('message'), "cause":request.POST.get('cause')}
		formContact=ContactForm(donne)
		if formContact.is_valid():
			print('le proframme ici')
			recaptcha_response=request.POST.get('g-recaptcha-response')
			data={
					'secret':settings.GOOGLE_RECAPTCHA_SECRET_KEY,
					'response': recaptcha_response
			}
			r=requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
			result=r.json()
			if result['success']:
				formContact.save()
				messages.success(request, 'Votre message est envoyer avec succée ')
				return redirect('visiteurContact')
	context={'form':formContact, 'profile':profile, 'estIlVendeur':getVendeur(request)}
	return render(request, 'statique/contact.html', context)
def politiqueDeConfidentialite(request):
	if request.user.is_authenticated:
		context={
			'profile':Profile.objects.get(user=request.user.id)
		}
	else:
		context={

		}

	return render(request, 'statique/politique.html', context)
@allowed_users(allowedGroups=['vendeur', 'admin'])
@login_required(login_url='login')
def updateProduct(request, pk):
	produit=Produit.objects.get(id=pk)
	form=ProduitForm(instance=produit)
	if request.method=='POST':
		form=ProduitForm(request.POST, instance=produit)
		if form.is_valid():
			form.save()
			messages.success(request, "Votre produit est mise à jour ")
			return redirect('home_page')
	context={'form':form, 'estIlVendeur':getVendeur(request)}
	return render(request, 'annonceur/updateProduct.html', context)
@allowed_users(allowedGroups=['vendeur', 'admin'])
@login_required(login_url='login')
def deleteProduct(request, pk):
	produit=Produit.objects.get(id=pk)
	if request.method=='POST':
		produit.delete()
		messages.success(request, 'Votre produit est supprimée avec succée ')
		return redirect('home_page')
	context={'produit':produit, 'estIlVendeur':getVendeur(request),'profile':Profile.objects.get(user=request.user.id)}
	return render(request, 'annonceur/delete_form.html', context)
@allowed_users(allowedGroups=['vendeur', 'admin'])
@login_required(login_url='login')
def afficherMesAnnonces(request):
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	produits=Produit.objects.filter(user=request.user.id)
	profil=Profile.objects.get(user=request.user.id)
	context={
		'produits':produits,
		'profile':profil,
		'meta':donneeUtile,
		'estIlVendeur':getVendeur(request)
	}
	return render(request, 'annonceur/annonceParUser.html', context)
@allowed_users(allowedGroups=['vendeur', 'admin'])
@login_required(login_url='login')
def afficherMesAnnoncesDetail(request):
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	if request.method=='POST':
		idProduit=request.POST.get('produitId')
		produit=Produit.objects.get(id=idProduit)
		images=ImageProduit.objects.filter(produit=idProduit)
		context={
			'produit':produit,
			'images':images,
			'meta':donneeUtile,
			'estIlVendeur':getVendeur(request),
			'profile':Profile.objects.get(user=request.user.id)
		}
		return render(request, 'annonceur/detail.html', context)
	else:
		return redirect('home_page')
@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def versAcheterUnProduit(request, pk):
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	produit=Produit.objects.get(slug=pk)
	images=ImageProduit.objects.filter(produit=produit.id)
	vendeur=User.objects.get(id=produit.user.id)
	vendeurProfile=Profile.objects.get(user=vendeur.id)
	enregistrer=Enregistre.objects.filter(user=request.user.id).filter(produit=produit.id).count()
	
	context={
			'produit':produit,
			'images':images,
			'vendeur':vendeur,
			'vendeurProfile':vendeurProfile,
			'enregistrer':enregistrer,
			'meta':donneeUtile,
			'estIlVendeur':getVendeur(request),
			'profile':Profile.objects.get(user=request.user.id)
		}
	return render(request, 'visiteur/affichage.html', context)
	
@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def contacterVendeur(request, slug):
	produit=Produit.objects.get(slug=slug)
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	userVendeur=User.objects.get(id=produit.user.id)
	if request.method=='POST':
		contenuMessage=request.POST.get('contenuMessage')
		send_mail(
					'un membre de minimalist est intersse par votre produit',
					contenuMessage+'vous avez le choix de contacter sur son email'+request.user.email,
					'vrairaaufabidi@gmail.com',
					[userVendeur.email],

					)
		messages.success(request, 'Votre message est envoyer au responsable de produit ')

	context={
		'vendeur':vendeur,
		'meta':donneeUtile,
		'estIlVendeur':getVendeur(request),
		'profile':Profile.objects.get(user=request.user.id)

	}
	return render(request, 'annonceur/contacterAnnonceur.html', context)
@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def enregistrerProduit(request, pk):
	produit=Produit.objects.get(slug=pk)
	form=EnregistrerForm({'user':request.user.id, 'produit': produit.id})
	if form.is_valid():
		messages.success(request, 'Produit est sauvegardée avec succée ')
		form.save()
		return redirect('versAcheterUnProduit', pk)
@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def configAchat(request, slug):
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	profil=Profile.objects.get(user=request.user.id)
	produit=Produit.objects.get(slug=slug)
	images=ImageProduit.objects.filter(produit=produit.id)
	vendeur=User.objects.get(id=produit.user.id)
	vendeurProfile=Profile.objects.get(user=vendeur.id)
	if request.method=='POST':
		if profil.adresse is None:
			messages.error(request, 'completer votre profile avant de passer une commandes (les profil sans adresse sans au problemes lors de delivration)')
			return redirect('updateprofile')
		nbPiece=request.POST.get('nombreDePiece')
		if int(nbPiece)==0:
			messages.error(request, 'Sélectionner le nombre de piéce ')
			return redirect('configAchat', produit.slug)
		if int(nbPiece)>produit.quantite:
			messages.error(request, f'Cette quantite nest pas disponible pour le moment (max : {produit.quantite}&nbsp&nbsp<i class="fa-solid fa-xmark"></i>')
			return redirect('configAchat', produit.slug)
		else:
			request.session[f'{request.user.id}produitQuantite']=nbPiece
			request.session[f'{request.user.id}Destination']=request.POST.get("adresseDestination")
			return redirect('payementPaypal', produit.slug)
	context={
		"produit":produit,
		'meta':donneeUtile,
		'profile':profil,
		'estIlVendeur':getVendeur(request),
		'images':images,
		'vendeur':vendeur,
		'vendeurProfile':vendeurProfile
	}
	return render(request, 'visiteur/configurationDachat.html', context)
@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def payementPaypal(request, pk):
	nbp=request.session[f'{request.user.id}produitQuantite']
	destination=request.session[f'{request.user.id}Destination']
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	profil=Profile.objects.get(user=request.user.id)
	produit=Produit.objects.get(slug=pk)
	vendeurr=vendeur.objects.get(user=produit.user)
	Commande.objects.create(user=request.user, produit=produit, nbPiece=int(nbp), destination=destination)
	lastCommande=Commande.objects.filter(produit=produit.id).filter(user=request.user.id)
	if vendeurr.prixDelivration:
		prixLivring=vendeurr.prixDelivration*int(nbp)
	else:
		prixLivring=0
	#on cherche a rendre le busines a un variable
	paypal_dict={
	#settings.PAYPAL_RECEIVER_EMAIL
        'business': vendeurr.Paypal_business,
	    'amount':produit.prix*int(nbp)+prixLivring,
	    'item_name': produit.entete,
	    'invoice': 		lastCommande[0].id,
	    'currency_code': 'USD',
	    'notify_url': 	f'http://{request.get_host()}{reverse("paypal-ipn")}',
	    'return_url':	 f'http://{request.get_host()}{reverse("paypal-return")}',                               
	    'cancel_return': f'http://{request.get_host()}{reverse("paypal-cancel")}'                                  
    	}
	form=PayPalPaymentsForm(initial=paypal_dict)
	context={
		'form':form,
		'produit':produit,
		'commande':lastCommande[0],
		'total':produit.prix*int(nbp)+prixLivring,
		'meta':donneeUtile,
		'profile':profil,
		'estIlVendeur':getVendeur(request)
	}

	return render(request, 'visiteur/payement.html', context)

@allowed_users(allowedGroups=['admin'])
@login_required(login_url='login')
def addCatgeorie(request):
	form=CategorieForm()
	if request.method=='POST':
		form=CategorieForm({'titre':request.POST.get("titre"), 'avatar' : request.FILES.get("avatar"), 'slug':getSlug()}, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Catégorie sauvegardée avec succée ')
			return redirect('addCategorie')
	context={
	'form':form
	}
	return render(request, 'admin/addCatgeorie.html', context)
@allowed_users(allowedGroups=['admin'])
@login_required(login_url='login')
def addFirstSousCat(request):
	form=FirstSousCategorieForm()
	if request.method=='POST':
		form=FirstSousCategorieForm({'titre':request.POST.get('titre'), 'avatar':request.FILES.get('avatar'), 'categorie':request.POST.get('categorie'), 'slug':getSlug()}, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Catégorie sauvegardée avec succée ')
			return redirect('addScategorie')
	context={
		'form':form
	}
	return render(request, 'admin/addScategorie.html', context)
@allowed_users(allowedGroups=['admin'])
@login_required(login_url='login')
def addSecondSousCat(request):
	form=SecondSousCategorieForm()
	if request.method=='POST':
		form=SecondSousCategorieForm({'titre':request.POST.get('titre'), 'slug':getSlug(), 'avatar':request.FILES.get('avatar'), 'firstCategore':request.POST.get('firstCategore')}, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Catégorie sauvegardée avec succée ')
			print(request.POST.get('modele'))
			modele=open("static/files/models/{}.data".format(request.POST.get('titre')), "w+", encoding='utf8')
			modele.write(request.POST.get('modele'))
			modele.close()
			#'static/files/models/vehicule.data', 'r', encoding='utf8'
			return redirect('addSScategorie')
	context={
		'form':form
	}
	return render(request, 'admin/addSScategorie.html', context)
@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def lireNotification(request, pk):
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	notification=Notification.objects.get(id=pk)
	notification.lire='oui'
	notification.save()
	context={
		'notification':notification,
		'meta':donneeUtile,
		'profile':Profile.objects.get(user=request.user.id)
	}
	return render(request, 'visiteur/notification.html', context)
def emailTrouve(request):
	try:
		email=Emailer.objects.get(email=request.user.email)
	except Emailer.DoesNotExist:
		email=None
	if email is None:
		return False
	else:
		return True
@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def userAccountParametre(request):
	profil=Profile.objects.get(user=request.user.id)

	if profil.is_verified=='non':
		return redirect('logout')
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	tache=request.GET.get('tache')
	if tache=='supprimerCompte':
		return redirect('estIlSure')
	elif tache=="supprimerLeModeVendeur":
		return redirect('supprimerModeVendeur')
	elif tache=="supprimeremailfromemailerie":
		email=Emailer.objects.get(email=request.user.email)
		email.delete()
		messages.success(request, 'Les Emails de notifications sont désactivéent avec succées ')
		return redirect('home_page')
	context={
		'profile':profile,
		'meta':donneeUtile,
		'estIlVendeur':getVendeur(request),
		'emailTrouve':emailTrouve,
		'profile':profil
	}
	return render(request, 'visiteur/parametre.html', context)
@allowed_users(allowedGroups=['vendeur', 'admin'])
@login_required(login_url='login')
def supprimerUser(request):
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	if request.method=='POST':
		group=Group.objects.get(name="vendeur")
		request.user.groups.remove(group)
		produits=Produit.objects.filter(user=request.user.id)
		for item in produits:
			item.delete()
		user=User.objects.get(id=request.user.id)
		user.is_active=False
		user.save()
		return redirect('logout')
	context={
		'profile':Profile.objects.get(user=request.user.id),
		'meta':donneeUtile
	}
	return render(request, 'frame/estIlSureDeSupprimer.html', context)
@allowed_users(allowedGroups=['vendeur', 'admin'])
@login_required(login_url='login')
def supprimerMode(request):
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	if request.method=="POST":
		vendeurr=vendeur.objects.get(user=request.user.id)
		produits=Produit.objects.filter(user=request.user.id)
		group=Group.objects.get(name="vendeur")
		request.user.groups.remove(group)
		for item in produits:
			item.delete()
		
		vendeurr.delete()
		#request.user.group=
		messages.success(request, 'Votre opération est effectuée avec succées ')
		return redirect('home_page')
	context={
		'profile':Profile.objects.get(user=request.user.id),
		'meta':donneeUtile
	}
	return render(request, 'frame/supprimerMode.html', context)

@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def prendreUnRendezVous(request, slug):
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	profil=Profile.objects.get(user=request.user.id)
	produit=Produit.objects.get(slug=slug)
	vendeur=User.objects.get(id=produit.user.id)
	vendeurProfile=Profile.objects.get(user=vendeur.id)
	images=ImageProduit.objects.filter(produit=produit.id)
	context={
		'profile':profil,
		'meta':donneeUtile,
		'produit':produit,
		'vendeur':vendeur,
		'vendeurProfile':vendeurProfile,
		'estIlVendeur':getVendeur(request),
		'images':images
	}
	return render(request, 'visiteur/rendezVous.html', context)
@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def coursPayement(request):
	data={"paye":True, "temps":"now"}
	return JsonResponse(data)

@csrf_exempt
def paypal_return(request):
	messages.success(request, "Votre payement est bien compléter")
	return redirect("home_page")
@csrf_exempt
def paypal_cancel(request):
	messages.error(request, "Votre transaction est annuler")
	return redirect('home_page')
@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def voirMesCommandes(request):
	donneeUtile={'fonctionne':estIlFonctionneDansCetpaye(request.META.get('REMOTE_ADDR'))}
	profil=Profile.objects.get(user=request.user.id)
	commandes=Commande.objects.filter(user=request.user.id)
	context={
		'commandes':commandes,
		'profile':profil,
		'meta':donneeUtile,
		'estIlVendeur':getVendeur(request),
	}
	return render(request, 'visiteur/commandes.html', context)
@allowed_users(allowedGroups=['vendeur', 'admin', 'visiteur'])
@login_required(login_url='login')
def confirmerDelivration(request, pk):
	commande=Commande.objects.filter(user=request.user.id).get(id=pk)
	if commande:
		commande.livre=True
		commande.save()
		messages.success(request, 'Votre commande est marque comme délivre merci de votre attention')
	else:
		messages.error(request, 'un probleme est suvenue')

	return redirect('voirMesCommandes')
#admin tache
#__________________________________________________
@allowed_users(allowedGroups=['admin'])
@login_required(login_url='login')
def adminHome(request):
	context={
		'profile':Profile.objects.get(user=request.user.id)
	}
	return render(request, 'admin/adminHome.html', context)
@allowed_users(allowedGroups=['admin'])
@login_required(login_url='login')	
def showSiteUsers(request):
	users=Profile.objects.all().exclude(user=request.user.id)
	context={
		'users':users,
		'profile':Profile.objects.get(user=request.user.id)
	}
	return render(request, 'admin/users.html', context)

@allowed_users(allowedGroups=['admin'])
@login_required(login_url='login')	
def detailUser(request, slug):
	try:
		userProfile=Profile.objects.get(slug=slug)
	except Profile.DoesNotExist:
		userProfile=None
	if userProfile is None:
		messages.error(request, 'cette profile nexiste pas')
		return redirect('admin_home')
	lastLogin=ceil(datetime.timestamp(userProfile.user.last_login))
	if lastLogin+15-ceil(datetime.timestamp(datetime.now()))<0:
		estIlConnecte=False
	else:
		estIlConnecte=True
	vendeurProfile=vendeur.objects.filter(user=userProfile.user)[0]
	
	context={
		'user':userProfile,
		'produits':Produit.objects.filter(user=userProfile.user),
		'estIlVendeur':getVendeur(request),
		'vendeurProfile':vendeurProfile,
		'commandes':Commande.objects.filter(user=userProfile.user),
		'ipInformation':IpMembre.objects.filter(user=userProfile.user),
		'emailer':Emailer.objects.filter(email=userProfile.user.email),
		'produitsEnregistre':Enregistre.objects.filter(user=userProfile.user),
		'profile':Profile.objects.get(user=request.user.id),
		'estIlConnecte':estIlConnecte,
	}
	return render(request, 'admin/detail.html', context)
@allowed_users(allowedGroups=['admin'])
@login_required(login_url='login')	
def adminSupprimerProduits(request, slug):
	produit=Produit.objects.get(slug=slug)
	if request.method=='POST':
		Notification.objects.create(
			titre='l\'administration de site minimalist a supprimer votre produit '+produit.entete,
			contenu=request.POST.get('causeDeSuppression'),
			user=produit.user
			)
		produit.delete()
		messages.success(request, 'le produit est supprimer')
		return redirect('admin_home')
	context={
		
	}
	return render(request, 'admin/supprimerProduct.html', context)
@allowed_users(allowedGroups=['admin', 'vendeur'])
@login_required(login_url='login')
def commandeNonLivre(request):
	produits=Produit.objects.filter(user=request.user.id)
	commandesNonDelivre=[]
	for item in produits:
		commandes=Commande.objects.filter(produit=item)
		if commandes:
			for item in commandes:
				if item.livre==False:
					commandesNonDelivre.append(item)
	context={
		'commandes':commandesNonDelivre,
		'profile':Profile.objects.get(user=request.user.id),
		'estIlVendeur':getVendeur(request)
	}
	return render(request, 'visiteur/nonLivre.html', context)
@allowed_users(allowedGroups=['admin'])
@login_required(login_url='login')
def supprimerVendeur(request, pk):
	vendeurr=vendeur.objects.get(id=pk)
	produits=Produit.objects.filter(user=vendeurr.user)

	if request.method=='POST':
		Notification.objects.create(
			titre='l\'administration de site minimalist a désactiver votre mode de vendeur',
			contenu=request.POST.get('causeDeSuppression')+"essaye de delivre les produits qui vous le vendre !!vous etes responsable si le client n'a pas recoit sa commandes</a>",
			user=vendeurr.user
			)
		vendeurr.delete()
		for item in produits:
			item.delete()
		messages.success(request, 'vendeur est supprimer avec succées')
		return redirect('admin_home')
	context={
		'profile':Profile.objects.get(user=request.user.id)
	}
	return render(request, 'admin/supprimerVendeur.html', context)
@allowed_users(allowedGroups=['admin', 'vendeur'])
@login_required(login_url='login')
def nonDelivreDetail(request, pk):
	commande=Commande.objects.get(id=pk)
	userProfile=Profile.objects.get(user=commande.user)
	
	context={
		'profile':Profile.objects.get(user=request.user.id),
		'userProfile':userProfile,
		'commande':commande,
		'estIlVendeur':getVendeur(request)
	}
	return render(request, 'annonceur/detailCommande.html', context)
@allowed_users(allowedGroups=['admin'])
@login_required(login_url='login')
def adminEnvoieEmailPourUtilisateur(request, pk):
	user=User.objects.get(id=pk)
	if request.method=='POST':
		objet=request.POST.get('objet')
		message=request.POST.get('message')
		send_mail(
			objet,
			sujet,
			"minimalistplatform@gmail.com",
			[user.email]
			)
		messages.success(request, 'Votre message envoyer avec succées ')

	context={
		'profile':Profile.objects.get(user=request.user.id)
	}
	return render(request, 'admin/emailEnvoie.html', context)
@allowed_users(allowedGroups=['admin'])
@login_required(login_url='login')
def voirContactMessages(request):
	p=Paginator(Contact.objects.all(), 10)
	page=request.GET.get('page')
	contact_list=p.get_page(page)
	context={
		'contacteMessage':contact_list,
		'profile':Profile.objects.get(user=request.user.id),
		'longPagination':range(contact_list.paginator.num_pages)
	}
	return render(request, 'admin/contact.html', context)
