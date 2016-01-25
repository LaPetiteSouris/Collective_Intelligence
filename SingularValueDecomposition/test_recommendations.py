import random
import unittest
import sure

import recommendations
import data

TITLES = [
	'Lady in the Water',
	'Snakes on a Plane',
	'Just My Luck',
	'Superman Returns',
	'You, Me and Dupree',
 	'The Night Listener',
]


def pick_a_name():
	return random.choice(data.critics.keys())


class TestSimilarities(unittest.TestCase):

	def test_sim_distance_range(self):
		distance = recommendations.similarity(
			data.critics, pick_a_name(), pick_a_name())
		(distance).should.be.within(-1, 1)

	def test_identical(self):
		name = pick_a_name()
		distance = recommendations.similarity(
			data.critics, name, name)
		self.assertAlmostEqual((distance), 1)


class TestTopMatches(unittest.TestCase):

	def test_top_matches_length(self):
		limit = random.randint(0, len(data.critics) - 1)
		matches = recommendations.top_matches(data.critics, pick_a_name(), n=limit)
		(matches).should.have.length_of(limit)


class TestRecommendations(unittest.TestCase):

	def test_recommendations_ranges(self):
		ranking = recommendations.get_recommendations(data.critics, pick_a_name())
		for score in ranking:
			(score[0]).should.be.within(0, 5)
			(score[1]).should.be.within(TITLES)
		l = len(ranking)
		(l).should.be.within(0, 3)
