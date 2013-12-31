#
#	 Trapping Rain Water
#
# Given n non-negative integers representing an elevation map where the 
# width of each bar is 1, compute how much water it is able to trap after 
# raining.
#

import unittest

def volume(heights):
	volume = 0
	for index in range(len(heights)):
		leftwallheight = max(heights[0:index+1])
		rightwallheight = max(heights[index:])
		volume += min(leftwallheight, rightwallheight) - heights[index]
	return volume

class TestVolume(unittest.TestCase):
	def test_ramp_up_zero(self):
		self.assertEqual(volume([1,2,3]), 0)
	def test_ramp_down_zero(self):
		self.assertEqual(volume([1,2,3]), 0)
	def test_hill_zero(self):
		self.assertEqual(volume([1,2,3,2,1]), 0)
	def test_single_valley(self):
		self.assertEqual(volume([1,0,1]), 1)
	def test_multi_valley(self):
		self.assertEqual(volume([1,0,1,0,1]), 2)
	def test_example(self):
		self.assertEqual(volume([2,5,1,2,3,4,7,7,6]), 10)
	def test_example2(self):
		self.assertEqual(volume([2,5,1,3,1,2,1,7,7,6]), 17)

if __name__ == '__main__':
	unittest.main()