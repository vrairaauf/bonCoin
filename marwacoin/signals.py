from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from .models import *
from django.core.mail import send_mail

def client_create_notification(sender, instance, created, **kwargs):
	if created:
		Notification.objects.create(
			titre='votre compte sur notre site est bien creer',
			contenu="pour beneficier de notre service il faux au debut completer votre profil",
			user=instance
			)
		print('Notification created suuccesfully')
post_save.connect(client_create_notification, sender=User)
def client_send_mail_after_insert_product(sender, instance, created, **kwargs):
    if created:
        emails=Emailer.objects.all()
        for item in emails:
            send_mail(
                    'un nouveaux produits sur Minimalist ',
                    'des nouveaux produits sur minimalist vites connecter sur le site pour voir tous les nouveaux produits',
                    'minimalistplatform@gmail.com',
                    [item.email],
                    )
        print('tous les emails sont envoyer')
post_save.connect(client_send_mail_after_insert_product, sender=Produit)        
@receiver(valid_ipn_received)
def validCommandeAfterPayement(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
    	commande=Commande.objects.get(id=ipn.invoice)
    	commande.paid=True
    	commande.save()
    	produit=Produit.objects.get(id=commande.produit.id)
    	restent=produit.quantite
    	if restent-commande.nbPiece>0:
    		produit.quantite-=1
    	else:
    		produit.deleted_at=True

    	print('situation de produit est mise a jour')	
    	produit.save()
    	
    	

@receiver(invalid_ipn_received)
def invalidCommandeAfterPayement(sender,  **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
    	Commande.objects.create()
      
