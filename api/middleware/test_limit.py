from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from django.test.utils import override_settings


class ReqestRateLimitTestCase(TestCase):
    def setUp(self):
        cache.clear()

    @override_settings(RATELIMIT_VIEW='100/m')
    def test_rate_limit(self):
        url = reverse('request_endpoint')

        # Make MAX_REQUESTS successful requests
        for _ in range(100):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        # The next request should exceed the rate limit
        response = self.client.get(url)
        self.assertEqual(response.status_code, 429)
        self.assertIn('Retry-After', response.headers)
        self.assertGreater(int(response.headers['Retry-After']), 0)

    @override_settings(RATELIMIT_VIEW='100/m')
    def test_rate_limit_headers(self):
        url = reverse('request_endpoint')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('X-Ratelimit-Remaining', response.headers)
        self.assertEqual(int(response.headers['X-Ratelimit-Remaining']), 99)
