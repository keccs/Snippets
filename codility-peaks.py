import unittest
import itertools

def peak_indices(a):
	def is_peak(heights, index, value):
		return index > 0 and index < len(heights)-1 and heights[index-1] < value > heights[index+1]
	return [index for (index, value) in enumerate(a) if is_peak(a, index, value)]

def max_flags_from_peaks(peaks):
	for flags_taken in range(len(peaks), 0, -1):
		for placement in itertools.combinations(peaks, flags_taken):
			valid = True
			for peakIndex in range(len(placement)):
				if peakIndex > 0 and placement[peakIndex]-placement[peakIndex-1] < flags_taken:
					valid = False
			if valid:
				return flags_taken
	return 0

def max_flags_from_heights(heights):
	return max_flags_from_peaks(peak_indices(heights))

class PeaksTest(unittest.TestCase):
	def test_empty(self):
		self.assertEquals(peak_indices([]), [])
	def test_simple(self):
		self.assertEquals(peak_indices([1,2,1]), [1])
	def test_example(self):
		self.assertEquals(peak_indices([1, 5, 3, 4, 3, 4, 1, 2, 3, 4, 6, 2]), [1, 3, 5, 10])
	def test_sorted(self):
		peaks = peak_indices([1,4,1,3,1,5,1,3,1,7])
		sorted = list(peaks)
		sorted.sort()
		self.assertEquals(peaks, sorted)

class FlagsTest(unittest.TestCase):
	def test_empty(self):
		self.assertEquals(max_flags_from_heights([]), 0)
	def test_singlePeak(self):
		self.assertEquals(max_flags_from_peaks([1]), 1)
	def test_singlePeak(self):
		self.assertEquals(max_flags_from_peaks([1]), 1)
	def test_example(self):
		self.assertEquals(max_flags_from_heights([1, 5, 3, 4, 3, 4, 1, 2, 3, 4, 6, 2]), 3)

if __name__ == '__main__':
	unittest.main()