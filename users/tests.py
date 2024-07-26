from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lms.models import Course
from users.models import User, CoursePurchase


class CoursePurchaseCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("users:create_payment")
        self.course = Course.objects.create(id=2, title="Test Course")

    # def test_perform_create(self):
    #     data = {
    #         'course': 2,
    #         'amount': 1000
    #     }
    #     response = self.client.post(self.url, data, format='json')
    #     self.assertEqual(response.status_code, 201)
    #     purchase = CoursePurchase.objects.get(id=response.data['id'])
    #     self.assertIsNotNone(purchase.session_id)
    #     self.assertIsNotNone(purchase.link)

    def test_perform_create(self):
        data = {"course": 2, "amount": 1000}
        response = self.client.post(self.url, data, format="json")
        print(response.status_code)
        print(response.data)
        self.assertEqual(response.status_code, 201)
