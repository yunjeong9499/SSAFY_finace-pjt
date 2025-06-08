from rest_framework import generics, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import OuterRef, Subquery, FloatField
from products.models import Deposit, DepositOption, Saving, SavingOption, Scrap
from products.serializers import DepositSerializer, SavingSerializer, ScrapSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# ✅ 예금 상품 리스트 (최고 금리 포함)
class DepositListAPIView(generics.ListAPIView):
    serializer_class = DepositSerializer

    def get_queryset(self):
        max_intr_rate_subquery = DepositOption.objects.filter(
            deposit=OuterRef('pk')  # ✅ 외래키 기준으로 수정됨
        ).order_by('-intr_rate2').values('intr_rate2')[:1]

        return Deposit.objects.annotate(
            max_intr_rate=Subquery(max_intr_rate_subquery, output_field=FloatField())
        )

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'bank__name']
    filterset_fields = ['bank__name', 'join_way']
    ordering_fields = ['max_intr_rate']
    ordering = ['-max_intr_rate']


# ✅ 예금 상세
class DepositViewSet(viewsets.ModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer


# ✅ 적금 상품 리스트 (최고 금리 포함)
class SavingListAPIView(generics.ListAPIView):
    serializer_class = SavingSerializer

    def get_queryset(self):
        max_rate_sub = SavingOption.objects.filter(
            saving=OuterRef('pk')  # ✅ 외래키 기준으로 수정됨
        ).order_by('-intr_rate2').values('intr_rate2')[:1]

        return Saving.objects.annotate(
            max_intr_rate=Subquery(max_rate_sub, output_field=FloatField())
        )

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'bank__name']
    filterset_fields = ['bank__name', 'join_way']
    ordering_fields = ['max_intr_rate']
    ordering = ['-max_intr_rate']


# ✅ 적금 상세
class SavingViewSet(viewsets.ModelViewSet):
    queryset = Saving.objects.all()
    serializer_class = SavingSerializer


# ✅ 스크랩 등록
class ScrapCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {
            'deposit': request.data.get('deposit_id'),
            'saving': request.data.get('saving_id')
        }

        serializer = ScrapSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ 로그인 유저의 스크랩 목록만 표시
class ScrapViewSet(viewsets.ModelViewSet):
    serializer_class = ScrapSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Scrap.objects.filter(user=self.request.user)
