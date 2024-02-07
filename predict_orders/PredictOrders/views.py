# views.py
from django.http import JsonResponse
from rest_framework.views import APIView
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .calculate_max import find_max


def process_dataframe(input_df):
    output_df = find_max(input_df)
    return output_df


@api_view(['GET', 'POST'])
def calculate_max(request):
    try:
        # Assuming 'data' is the key for your DataFrame in the JSON payload
        df_data = request.data.get('data', [])  # [] is a default value if "data" is not find in request body this []
        # returns

        # Deserialize the JSON back to DataFrame
        input_df = pd.DataFrame(df_data)

        # Process the DataFrame using your function
        processed_df = process_dataframe(input_df)

        # Convert the processed DataFrame back to JSON
        processed_df_json = processed_df.to_json(orient='records')

        return JsonResponse({'result': processed_df_json})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
