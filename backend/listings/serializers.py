from rest_framework import serializers
from .models import Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ('title', 'address', 'city', 'state', 'sale_type', 'price', 'bedrooms',
                  'bathrooms', 'home_type', 'sqft', 'photo_main', 'slug')


class ListingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
        lookup_field = 'slug'
