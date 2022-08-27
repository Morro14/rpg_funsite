from django_filters import FilterSet
from .models import Comment


class CommentsFilter(FilterSet):
    class Meta:
        model = Comment
        fields = {
            'time_in': ['week__lt']
        }

