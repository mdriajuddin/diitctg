from rest_framework.throttling import BaseThrottle
import time
from collections import deque

class SlidingWindowThrottle(BaseThrottle):
    def __init__(self, rate='10/min'):

        self.rate = rate
        self.num_requests, self.duration = self.parse_rate(rate)
        self.request_logs = {}  # Store request timestamps for each user

    def parse_rate(self, rate):
        """
        Parses the rate limit string (e.g., '10/min') into num_requests and duration.
        """
        num, period = rate.split('/')
        num_requests = int(num)
        if period == 'min':
            duration = 60
        elif period == 'hour':
            duration = 3600
        elif period == 'day':
            duration = 86400
        else:
            raise ValueError("Invalid throttle rate")
        return num_requests, duration

    def allow_request(self, request, view):
        user_ident = self.get_ident(request)
        current_time = time.time()

        # If user not in logs, initialize an empty deque
        if user_ident not in self.request_logs:
            self.request_logs[user_ident] = deque()

        # Remove timestamps outside the time window
        while self.request_logs[user_ident] and self.request_logs[user_ident][0] < current_time - self.duration:
            self.request_logs[user_ident].popleft()

        # Check if user is within the limit
        if len(self.request_logs[user_ident]) < self.num_requests:
            self.request_logs[user_ident].append(current_time)
            return True
        return False

    def wait(self):
        # Calculate time until next request is allowed
        if self.request_logs:
            user_timestamps = self.request_logs[self.get_ident()]
            if user_timestamps:
                return self.duration - (time.time() - user_timestamps[0])
        return None


