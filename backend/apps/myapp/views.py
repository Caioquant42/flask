from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ReactView(APIView):

    serializer_class = ReactSerializer

    def get(self, request):
        output = [{"employee": output.employee, "department": output.department}
                  for output in React.objects.all()]
        return Response(output)

    def post(self, request):

        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        


from .serializers import SalesDataSerializer
import random
from datetime import datetime, timedelta

class SalesDataView(APIView):
    def get(self, request):
        # Generate 12 months of random sales data
        start_date = datetime.now().replace(day=1, month=1)
        sales_data = []
        
        for i in range(12):
            month = (start_date + timedelta(days=30*i)).strftime('%b')
            sales = random.randint(5000, 15000)  # Random sales between 5000 and 15000
            sales_data.append({"month": month, "sales": sales})
        
        serializer = SalesDataSerializer(sales_data, many=True)
        return Response(serializer.data)

