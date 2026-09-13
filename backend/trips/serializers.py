from rest_framework import serializers


class TripPlanSerializer(serializers.Serializer):
    current_location = serializers.CharField()
    pickup_location = serializers.CharField()
    dropoff_location = serializers.CharField()
    cycle_used_hours = serializers.FloatField(min_value=0, max_value=70)