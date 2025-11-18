from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Question
from .serializers import QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('id')
    serializer_class = QuestionSerializer

    # /questions/by_level/?level=A1  -- версияи умумӣ
    def get_queryset(self):
        level = self.request.query_params.get('level')
        if level:
            return self.queryset.filter(level=level)
        return self.queryset

    # --- Сатҳҳои ҷудогона ---

    @action(detail=False, methods=['get'])
    def a1(self, request):
        data = self.queryset.filter(level='A1')
        return Response(QuestionSerializer(data, many=True).data)

    @action(detail=False, methods=['get'])
    def a2(self, request):
        data = self.queryset.filter(level='A2')
        return Response(QuestionSerializer(data, many=True).data)

    @action(detail=False, methods=['get'])
    def b1(self, request):
        data = self.queryset.filter(level='B1')
        return Response(QuestionSerializer(data, many=True).data)

    @action(detail=False, methods=['get'])
    def b2(self, request):
        data = self.queryset.filter(level='B2')
        return Response(QuestionSerializer(data, many=True).data)

    @action(detail=False, methods=['get'])
    def c1(self, request):
        data = self.queryset.filter(level='C1')
        return Response(QuestionSerializer(data, many=True).data)

    @action(detail=False, methods=['get'])
    def c2(self, request):
        data = self.queryset.filter(level='C2')
        return Response(QuestionSerializer(data, many=True).data)
