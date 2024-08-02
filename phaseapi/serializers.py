from rest_framework import serializers
from phaseapi.models import Phase

class PhaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Phase
        fields = "__all__"      