from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import datetime
from .models import LSA

class StudentOnboardingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.lsa = LSA.objects.create(name="Test LSA")
        
        # Valid baseline data (should be CLEARED)
        self.valid_data = {
            "student_full_name": "John Doe",
            "date_of_birth": (datetime.date.today() - datetime.timedelta(days=365*10)).isoformat(),
            "learning_difficulty_confirmed": True,
            "parent_consent_signed": True,
            "emergency_contact_name": "Jane Doe",
            "emergency_contact_phone": "+1234567890",
            "school_grade": 5,
            "iep_document_attached": True,
            "assigned_lsa": self.lsa.id
        }

    def test_successful_onboarding_cleared(self):
        response = self.client.post('/api/onboarding/submit/', self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'CLEARED')

    def test_missing_iep_with_confirmed_diagnosis(self):
        data = self.valid_data.copy()
        data['iep_document_attached'] = False
        response = self.client.post('/api/onboarding/submit/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data['errors'])
        self.assertEqual(
            response.data['errors']['non_field_errors'][0].code, 
            'iep_required'
        )

    def test_invalid_phone_number(self):
        data = self.valid_data.copy()
        data['emergency_contact_phone'] = "123-456" # Invalid E.164
        response = self.client.post('/api/onboarding/submit/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('emergency_contact_phone', response.data['errors'])

    def test_age_out_of_range(self):
        data = self.valid_data.copy()
        data['date_of_birth'] = (datetime.date.today() - datetime.timedelta(days=365*20)).isoformat() # 20 years old
        response = self.client.post('/api/onboarding/submit/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date_of_birth', response.data['errors'])

    def test_successful_onboarding_blocked(self):
        data = self.valid_data.copy()
        data['learning_difficulty_confirmed'] = False # Will fail validation completely
        response = self.client.post('/api/onboarding/submit/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['errors']['learning_difficulty_confirmed'][0].code, 
            'diagnosis_unconfirmed'
        )
