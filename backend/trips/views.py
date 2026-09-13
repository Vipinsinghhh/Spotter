from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import TripPlanSerializer
from .services import calculate_available_hours

@api_view(['POST'])
def plan_trip(request):
    serializer = TripPlanSerializer(data=request.data)

    if serializer.is_valid():
        trip_data = serializer.validated_data

        hos_data = calculate_available_hours(
            trip_data['cycle_used_hours']
        )

        return Response({
            'message': 'Trip planning API is working',
            'received_data': trip_data,
            'hos_data': hos_data,
        })

    return Response(serializer.errors, status=400)