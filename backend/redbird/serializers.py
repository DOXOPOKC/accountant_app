from rest_framework import serializers

from .models import Journal, JournalRecord


class JournalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalRecord
        fields = '__all__'


class JournalSerializer(serializers.ModelSerializer):
    records = JournalRecordSerializer(many=True)

    class Meta:
        model = Journal
        fields = '__all__'
