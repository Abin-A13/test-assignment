import json
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from api.serializers import UserSerializer
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

        response_data = {
            "saved_records": saved_records,
            "rejected_records": rejected_records,
            "errors": errors
        }

        # Use Django's FileSystemStorage to handle file creation
        fs = FileSystemStorage(
            location=os.path.join(settings.BASE_DIR, 'data'))

        # Ensure the directory exists
        directory = fs.location
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save the response data to a JSON file
        file_path = os.path.join(directory, 'response_output.json')
        with open(file_path, 'w') as json_file:
            json.dump(response_data, json_file, indent=4)

        return Response(response_data, status=status.HTTP_200_OK)


def request_endpoint(request):
    """
    A simple view that returns a JSON response.
    """
    return JsonResponse({'message': 'Request successful'})
