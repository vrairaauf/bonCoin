from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
admin.site.register(User)

admin.site.register(Profile)

admin.site.register(Notification)

admin.site.register(Produit)

admin.site.register(helperWord)

admin.site.register(Categorie)
admin.site.register(firstSousCategorie)
admin.site.register(secondSousCategorie)
admin.site.register(vendeur)
admin.site.register(ImageProduit)
admin.site.register(IpMembre)


admin.site.register(Emailer)

admin.site.register(Contact)

admin.site.register(Commande)
