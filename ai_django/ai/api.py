from .models import Member
from rest_framework import serializers, viewsets

# 모델을 지정하고 사용할 필드를 선택한다.
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        # fields = '__all__'
        fields = ['name']

# 위의 MemberSerializer를 serializer_class에 넣어줌으로써 serializer를 연결한다.
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer