from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.queen import Queen
from ..serializers import QueenSerializer

# Create your views here.
class Queens(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = QueenSerializer
    def get(self, request):
        """Index request"""
        # Get all the queens:
        # queens = Queen.objects.all()
        # Filter the queens by owner, so you can only see your owned queens
        queens = Queen.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = QueenSerializer(queens, many=True).data
        return Response({ 'queens': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['queen']['owner'] = request.user.id
        # Serialize/create queen
        queen = QueenSerializer(data=request.data['queen'])
        # If the queen data is valid according to our serializer...
        if queen.is_valid():
            # Save the created queen & send a response
            queen.save()
            return Response({ 'queen': queen.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(queen.errors, status=status.HTTP_400_BAD_REQUEST)

class QueenDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the queen to show
        queen = get_object_or_404(Queen, pk=pk)
        # Only want to show owned queens?
        if not request.user.id == queen.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this queen')

        # Run the data through the serializer so it's formatted
        data = QueenSerializer(queen).data
        return Response({ 'queen': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate queen to delete
        queen = get_object_or_404(Queen, pk=pk)
        # Check the queen's owner agains the user making this request
        if not request.user.id == queen.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this queen')
        # Only delete if the user owns the  queen
        queen.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate Queen
        # get_object_or_404 returns a object representation of our Queen
        queen = get_object_or_404(Queen, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == queen.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this queen')

        # Ensure the owner field is set to the current user's ID
        request.data['queen']['owner'] = request.user.id
        # Validate updates with serializer
        data = QueenSerializer(queen, data=request.data['queen'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
