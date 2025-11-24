from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Address
from .serializers import AddressSerializer


@method_decorator(csrf_exempt, name="dispatch")
class UserAddressListCreateView(APIView):
    """
    List all user addresses or create a new one.
    GET: Return all addresses for the logged-in user
    POST: Create a new address for the logged-in user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user).order_by('-id')
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class UserAddressDetailView(APIView):
    """
    Update or delete a specific address.
    Only allows users to modify their own addresses.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, address_id):
        address = get_object_or_404(Address, id=address_id, user=request.user)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, address_id):
        address = get_object_or_404(Address, id=address_id, user=request.user)
        address.delete()
        return Response({"message": "Address deleted"}, status=200)
