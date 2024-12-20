import time
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


MAX_REQUESTS = 100
TIME_WINDOW = 5 * 60


class RateLimitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_ip = self.get_client_ip(request)
        cache_key = f"rate_limit_{user_ip}"
        current_time = int(time.time())
        request_data = cache.get(cache_key, [])

        request_data = [
            timestamp for timestamp in request_data if current_time - timestamp < TIME_WINDOW]

        if len(request_data) >= MAX_REQUESTS:
            remaining_time = TIME_WINDOW - (current_time - request_data[0])
            return JsonResponse({
                "error": "Rate limit exceeded, try again later.",
                "retry_after": remaining_time
            }, status=429)

        request_data.append(current_time)
        cache.set(cache_key, request_data, timeout=TIME_WINDOW)
        remaining_requests = MAX_REQUESTS - len(request_data)
        request.META['HTTP_X_RATELIMIT_REMAINING'] = remaining_requests

    def get_client_ip(self, request):
        """ Get the client IP address """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
