from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import TripPlanSerializer
from .services import (
    calculate_available_hours,
    geocode_trip_locations,
    get_route,
)

@api_view(['POST'])
def plan_trip(request):
    serializer = TripPlanSerializer(data=request.data)

    if serializer.is_valid():
        trip_data = serializer.validated_data

        locations = geocode_trip_locations(
            trip_data['current_location'],
            trip_data['pickup_location'],
            trip_data['dropoff_location'],
        )

        route = get_route([
            locations['current_location'],
            locations['pickup_location'],
            locations['dropoff_location'],
        ])

        hos_data = calculate_available_hours(
            trip_data['cycle_used_hours']
        )

        return Response({
            'message': 'Trip planning API is working',
            'received_data': trip_data,
            'locations': locations,
            'route': route,
            'hos_data': hos_data,
        })

    return Response(serializer.errors, status=400)