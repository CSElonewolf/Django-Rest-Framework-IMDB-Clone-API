from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

class CustomUserWatchListThrottle(UserRateThrottle):
	scope='user-watch-list'

class CustomAnonWatchListThrottle(AnonRateThrottle):
	scope='anon-watch-list'

