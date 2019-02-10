from rest_framework import serializers

from . import models

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title', 
            'teacher', 
            'description', 
            'subject', 
            'created_at',
        )
        model = models.Course


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'course',
            'reviewer',
            'rating',
            'comment',
            'created_at',

        )
        model = models.Review
