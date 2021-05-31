from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import permissions
from datetime import datetime, timezone, timedelta
from .models import Listing
from .serializers import ListingSerializer, ListingDetailSerializer


class AllListingsView(ListAPIView):
    queryset = Listing.objects.order_by('-list_date').filter(is_published=True)
    permission_classes = (permissions.AllowAny, )
    serializer_class = ListingSerializer
    lookup_field = 'slug'


class ListingView(RetrieveAPIView):
    queryset = Listing.objects.order_by('-list_date').filter(is_published=True)
    serializer_class = ListingDetailSerializer
    lookup_field = 'slug'


class SearchView(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ListingSerializer

    def post(self, request, format=None):
        queryset = Listing.objects.order_by('-list_date').filter(is_published=True)
        data = self.request.data

        sale_type = data['sale_type']
        queryset = queryset.filter(sale_type__iexact=sale_type)

        price = data['price']
        if price in {'Any', '$0+'}:
            price = 0
        elif price == '$200,000+':
            price = 200000
        elif price == '$400,000+':
            price = 400000
        elif price == '$600,000+':
            price = 600000
        else:
            price = 2000000000  #! Infinity
        queryset = queryset.filter(price__gte=price)

        bedrooms = data['bedrooms']
        if bedrooms == '0+':
            bedrooms = 0
        elif bedrooms == '1+':
            bedrooms = 1
        elif bedrooms == '2+':
            bedrooms = 2
        else:
            bedrooms = 3
        queryset = queryset.filter(bedrooms__gte=bedrooms)

        home_type = data['home_type']
        queryset = queryset.filter(home_type__iexact=home_type)

        bathrooms = data['bathrooms']
        if bathrooms == '0+':
            bathrooms = 0
        elif bathrooms == '1+':
            bathrooms = 1
        elif bathrooms == '2+':
            bathrooms = 2
        elif bathrooms == '3+':
            bathrooms = 3
        queryset = queryset.filter(bathrooms__gte=bathrooms)

        sqft = data['sqft']
        if sqft == '1000+':
            sqft = 1000
        elif sqft == '1200+':
            sqft = 1200
        elif sqft == '1500+':
            sqft = 1500
        elif sqft == 'Any':
            sqft = 0
        queryset = queryset.filter(sqft__gte=sqft)

        days_listed = data['days_listed']
        if days_listed == '1 or less':
            days_listed = 1
        elif days_listed == '10 or less':
            days_listed = 10
        elif days_listed == '100 or less':
            days_listed = 100
        elif days_listed == 'Any':
            days_listed = 0
        for query in queryset:
            days_passed = (datetime.now(timezone.utc) - query.list_date).days
            if days_passed > days_listed:
                queryset = queryset.exclude(slug__iexact=query.slug)

        has_photos = data['has_photos']
        if has_photos in {'0+', 'Any'}:
            has_photos = 0
        elif has_photos == '1+':
            has_photos = 1
        else:
            has_photos = 2

        for query in queryset:
            count = 0
            if query.photo_1:
                count += 1
            if query.photo_2:
                count += 1
            if count < has_photos:
                slug = query.slug
                queryset = queryset.exclude(slug__iexact=slug)

        open_house = data['open_house']
        queryset = queryset.filter(open_house__iexact=open_house)

        keywords = data['keywords']
        queryset = queryset.filter(description__icontains=keywords)

        serializer = ListingSerializer(queryset, many=True)
        return Response(serializer.data)
