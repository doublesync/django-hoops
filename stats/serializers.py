from rest_framework import serializers
from stats.models import SeasonAverage
from stats.models import SeasonTotal

class SeasonAverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonAverage
        fields = "__all__"

class SeasonTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonTotal
        fields = "__all__"