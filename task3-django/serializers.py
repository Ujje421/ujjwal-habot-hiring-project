# Name: Ujjwal [Last Name]
# Contact: [Email / LinkedIn / GitHub]

from rest_framework import serializers
from .models import StudentOnboarding
from django.core.validators import RegexValidator
import datetime

class StudentOnboardingSerializer(serializers.ModelSerializer):
    student_full_name = serializers.CharField(
        max_length=100,
        validators=[RegexValidator(
            regex=r'^[A-Za-z ]{1,100}$',
            message="Name contains invalid characters",
            code='invalid_name'
        )]
    )
    emergency_contact_phone = serializers.CharField(
        max_length=20,
        validators=[RegexValidator(
            regex=r'^\+[1-9]\d{7,14}$',
            message="Invalid phone number format",
            code='invalid_phone'
        )]
    )

    class Meta:
        model = StudentOnboarding
        fields = [
            'student_full_name', 'date_of_birth', 'learning_difficulty_confirmed',
            'parent_consent_signed', 'emergency_contact_name', 'emergency_contact_phone',
            'school_grade', 'iep_document_attached', 'assigned_lsa'
        ]

    def validate_date_of_birth(self, value):
        """DCYN Rule: Age must be between 4 and 18 years from today."""
        today = datetime.date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if not (4 <= age <= 18):
            raise serializers.ValidationError("Age out of acceptable range", code="age_out_of_range")
        return value

    def validate_learning_difficulty_confirmed(self, value):
        """DCYN Rule: Referral cannot proceed without confirmed diagnosis."""
        if not value:
            raise serializers.ValidationError("Referral cannot proceed without confirmed diagnosis", code="diagnosis_unconfirmed")
        return value

    def validate_parent_consent_signed(self, value):
        """DCYN Rule: Consent is mandatory."""
        if not value:
            raise serializers.ValidationError("Parent consent is missing", code="consent_missing")
        return value

    def validate_school_grade(self, value):
        """DCYN Rule: Grade must be 1-12."""
        if not (1 <= value <= 12):
            raise serializers.ValidationError("Grade out of range", code="grade_out_of_range")
        return value

    def validate(self, data):
        """Cross-field DCYN Rule: IEP document mandatory if diagnosis confirmed."""
        iep = data.get('iep_document_attached', getattr(self.instance, 'iep_document_attached', False))
        confirmed = data.get('learning_difficulty_confirmed', getattr(self.instance, 'learning_difficulty_confirmed', False))
        
        if confirmed and not iep:
            raise serializers.ValidationError(
                "IEP document is mandatory for confirmed diagnoses.", 
                code="iep_required"
            )
        return data

    def to_representation(self, instance):
        """Inject strict DCYN computed status - eliminates human judgment."""
        ret = super().to_representation(instance)
        all_true = (
            instance.learning_difficulty_confirmed and
            instance.parent_consent_signed and
            instance.iep_document_attached
        )
        ret['dcyn_clearance_status'] = 'CLEARED' if all_true else 'BLOCKED'
        return ret
