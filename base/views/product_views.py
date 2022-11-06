from itertools import product
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from ..serializers import ReviewSerializer

from base.models import Product, Review
from base.serializers import ProductSerializer

from django.contrib.auth.hashers import make_password
from rest_framework import status


# products
@api_view(['GET'])
def getProducts(request):
    query=request.query_params.get('keyword')
    if query==None:
        query=""
    
    products=Product.objects.filter(name__icontains=query)
    serializer=ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTopProducts(request):
    products=Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request,pk):
    product=Product.objects.get(_id=pk)
    serializer=ProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request,pk):
    user=request.user
    product=Product.objects.get(_id=pk)
    data=request.data

    # case 1: review already exists
    alreadyExists= product.review_set.filter(user=user).exists()

    if alreadyExists:
        content= {'detail':'Product alreadt reviewed'}
        return Response(content,status=status.HTTP_400_BAD_REQUEST) 
    
    # case 2: No rating or 0
    elif data['rating']==0:
        content= {'detail':'Please select a rating'}
        return Response(content,status=status.HTTP_400_BAD_REQUEST)
    
    # case 3: create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews=product.review_set.all()
        product.numReviews= len(reviews)

        total=0
        for i in reviews:
            total+=i.rating
        
        product.rating= total/len(reviews)
        product.save()

        serializer=ReviewSerializer(review)

        return Response(serializer.data)
