import django_filters
from .models import *
class ProduitFilter(django_filters.FilterSet):
	class Meta:
		model=Produit
		fields=[
			"location",
			"operation",
		]