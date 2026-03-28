from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import SITRAMSearchSerializer, SITRAMResponseSerializer
from .services.playwright_service import extract_sitram_data_sync
import logging
import threading

logger = logging.getLogger(__name__)


class SITRAMSearchView(APIView):
    """
    API endpoint for searching and extracting SITRAM data.

    POST /api/sitram/search/
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Extract SITRAM data based on search criteria.
        """
        # Validate input
        serializer = SITRAMSearchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'error': 'Invalid input',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract data from request
        search_params = {
            'start_date': serializer.validated_data.get('start_date'),
            'end_date': serializer.validated_data.get('end_date'),
            'cnpj': serializer.validated_data.get('cnpj'),
        }

        try:
            # Call Playwright automation in a separate thread to avoid asyncio conflicts
            result = extract_sitram_data_sync(search_params)
        except Exception as e:
            logger.error(f"Automation error: {str(e)}", exc_info=True)
            return Response(
                {
                    'success': False,
                    'error': f'Automation failed: {str(e)}'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Return response
        response_serializer = SITRAMResponseSerializer(result)
        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK if result.get('success') else status.HTTP_400_BAD_REQUEST
        )
