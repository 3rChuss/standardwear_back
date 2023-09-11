from django.test import TestCase
from rest_framework.test import APIClient
from .models import User, UserProfile

client = APIClient()

# Create your tests here.

class UserTestCase(TestCase):
    def setUp(self):
        data = {
        "email": "test@test.test",
        "password": "123!QWE.__",
        "confirm_password": "123!QWE.__",
        "language": "es",
        "accepted_terms": True,
        "accepted_privacy": True,
        "accepted_marketing" : False
      }
        response = client.post('/api/v1/users/register/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'])
                         

    def test_user(self):
        # profile has been created
        user = User.objects.get(
            email='test@test.test'
        )
        self.assertEqual(user.email, 'test@test.test')
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        #  profile, instance of UserProfile
        profile = UserProfile.objects.get(
            user=user
        )
        self.assertEqual(profile.language, 'es')
        self.assertEqual(profile.accepted_terms, True)
        self.assertEqual(profile.accepted_privacy, True)
        self.assertEqual(profile.accepted_marketing, False)
                         
      