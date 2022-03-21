from re import T
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# inner prodject imports
from watchlist_app.api import serializers
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):

	# create an user to test the streamplatform create feature
	def setUp(self):
		self.user = User.objects.create_user(username ="example",password="example@123")
		self.token = Token.objects.get(user__username=self.user)
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

		# create a streamplatform to test the get request against
		self.stream = models.StreamPlatform.objects.create(name = "Netflix", about = "#1 Platform for streaming media",website="https://www.netflix.com")

	# try to create a stream using a normal user credentials gives an 403-forbidden error
	def test_streamplatform_create(self):
		data = {
			"name":"Netflix",
			"about":"#1 streaming platform",
			"website":"https://www.netflix.com"
		}

		response = self.client.post(reverse('streamplatform-list'),data)
		self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

	# try to access the streampaltform list using get requests
	def test_streamplatform_list(self):
		response = self.client.get(reverse('streamplatform-list'))
		self.assertEqual(response.status_code,status.HTTP_200_OK)

	# try to access any specific streamplatform
	def test_individual_streamplatform(self):
		response = self.client.get(reverse('streamplatform-detail',args=(self.stream.id,)))
		self.assertEqual(response.status_code,status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

	def setUp(self):
		self.user = User.objects.create_user(username="example",password="example@123")
		self.token = Token.objects.get(user__username=self.user)
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

		# create an streamplatform to add to the watchlist that we will try to create
		self.stream = models.StreamPlatform.objects.create(name = "Netflix", about = "#1 Platform for streaming media",website="https://www.netflix.com")

		# create a watchlist to test the get request
		self.watchlist = models.WatchList.objects.create(platform=self.stream,title="Example",storyline="Example Movie",active = True)

	def test_watchlist_create(self):
		data = {
			"platform":self.stream,
			"title": "example watchlist",
			"storyline":"example storyline",
			"active":True
		}

		response = self.client.post(reverse('movie-list'),data)
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def test_watchlist_list(self):
		response = self.client.get(reverse('movie-list'))
		self.assertEqual(response.status_code,status.HTTP_200_OK)

	def test_individual_watchlist(self):
		response = self.client.get(reverse('movie-detail',args=(self.watchlist.id,)))
		self.assertEqual(response.status_code,status.HTTP_200_OK)
		self.assertEqual(models.WatchList.objects.count(),1)
		self.assertEqual(models.WatchList.objects.get().title,"Example")


class ReviewTestCase(APITestCase):
		def setUp(self):
			self.user = User.objects.create_user(username="example",password="example@123")
			self.token = Token.objects.get(user__username=self.user)
			self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

			# create an streamplatform to add to the watchlist that we will try to create
			self.stream = models.StreamPlatform.objects.create(name = "Netflix", about = "#1 Platform for streaming media",website="https://www.netflix.com")

			# create a watchlist to test the get request
			self.watchlist = models.WatchList.objects.create(platform=self.stream,title="Example",storyline="Example Movie",active = True)

			# create a watchlist to test update feature using put request
			self.watchlist2 = models.WatchList.objects.create(platform=self.stream,title="Example2",storyline="Example Movie2",active = True)

			# create a review to test for the newly created watchlist2
			self.review = models.Review.objects.create(review_user=self.user,rating = 5,description="test desc",watchlist = self.watchlist2,active = True)


		# tests the review create feature
		def test_review_create(self):
			data = {
				"review_user":self.user,
				"rating":5,
				"description":"test desc of the watchlist",
				"watchlist":self.watchlist,
				"active":True
			}

			response = self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
			self.assertEqual(response.status_code,status.HTTP_201_CREATED)


			# let's try to add a new review for the same movie from the same user
			response = self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
			self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

		# tests whether review can be posted without authenticating
		def test_review_create_unauthorized(self):
			data = {
				"review_user":self.user,
				"rating":5,
				"description":"test desc of the watchlist",
				"watchlist":self.watchlist,
				"active":True
			}
			# forcefully authenticate without passing te user credentials
			self.client.force_authenticate(user = None)
			response = self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
			self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

		# test to update the review created for the watchlist2
		def test_review_update(self):
			data = {
				"review_user":self.user,
				"rating":5,
				"description":"test desc updated",
				"watchlist":self.watchlist2,
				"active":False
			}
			response = self.client.put(reverse('review-detail',args = (self.review.id,)),data)
			self.assertEqual(response.status_code,status.HTTP_200_OK)

		# test to recieve the list of reviews for the watchlist
		def test_review_list(self):
			response = self.client.get(reverse('review-list',args = (self.watchlist.id,)))
			self.assertEqual(response.status_code,status.HTTP_200_OK)

		# make get requests to an individual review
		def test_individual_review(self):
			response = self.client.get(reverse('review-detail',args = (self.review.id,)))
			self.assertEqual(response.status_code,status.HTTP_200_OK)

		# test the UserReview class
		def test_review_user(self):
			response = self.client.get('/watch/reviews/?username'+self.user.username)
			self.assertEqual(response.status_code,status.HTTP_200_OK)
