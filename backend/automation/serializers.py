from rest_framework import serializers


class SITRAMSearchSerializer(serializers.Serializer):
    """
    Serializer for SITRAM search request.
    """
    start_date = serializers.CharField(required=True, help_text="Start date in DD/MM/YYYY format")
    end_date = serializers.CharField(required=True, help_text="End date in DD/MM/YYYY format")
    cnpj = serializers.CharField(required=True, help_text="CNPJ in XX.XXX.XXX/XXXX-XX format")

    def validate_start_date(self, value):
        """Validate date format."""
        if not self._is_valid_date(value):
            raise serializers.ValidationError("Invalid date format. Use DD/MM/YYYY")
        return value

    def validate_end_date(self, value):
        """Validate date format."""
        if not self._is_valid_date(value):
            raise serializers.ValidationError("Invalid date format. Use DD/MM/YYYY")
        return value

    def validate_cnpj(self, value):
        """Validate CNPJ format."""
        # Remove non-digits for validation
        cnpj_digits = ''.join(c for c in value if c.isdigit())
        if len(cnpj_digits) != 14:
            raise serializers.ValidationError("CNPJ must have 14 digits")
        return value

    @staticmethod
    def _is_valid_date(date_str):
        """Check if date string is in valid DD/MM/YYYY format."""
        try:
            parts = date_str.split('/')
            if len(parts) != 3:
                return False
            day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
            if not (1 <= day <= 31 and 1 <= month <= 12 and year >= 1900):
                return False
            return True
        except (ValueError, AttributeError):
            return False


class SITRAMResponseSerializer(serializers.Serializer):
    """
    Serializer for SITRAM search response.
    """
    success = serializers.BooleanField()
    data = serializers.CharField(required=False, allow_blank=True, help_text="CSV content or parsed data")
    error = serializers.CharField(required=False, allow_blank=True, help_text="Error message if failed")
