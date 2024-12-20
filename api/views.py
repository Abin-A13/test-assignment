from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from api.serializers import UserSerializer
from .models import User
from .utils import parse_csv_file


class CreateCSVdataView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, requests, *args, **kwargs):
        """
        create data by upload csv files
        """
        file = requests.FILES.get('file')
        if not file.name.endswith('.csv'):
            return Response({"error": "Allowed file format .csv"}, status=status.HTTP_400_BAD_REQUEST)
        data_list, error = parse_csv_file(file)
        if error:
            return Response({"error": f"Failed to parse CSV file: {error}"}, status=status.HTTP_400_BAD_REQUEST)

        saved_records = 0
        rejected_records = 0
        errors = []

        for data in data_list:
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    saved_records += 1
                except Exception as e:
                    errors.append({"row": data_list, "error": str(e)})
                    rejected_records += 1
            else:
                errors.append({"row": data_list, "errorss": serializer.errors})
                rejected_records += 1

        return Response({
            "saved_records": saved_records,
            "rejected_records": rejected_records,
            "errors": errors
        }, status=status.HTTP_200_OK)
