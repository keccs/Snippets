import itertools
def checkio(sticks):
	def is_triangle(t):
		return t[0]+t[1]>=t[2] and t[1]+t[2]>=t[0] and t[0]+t[2]>=t[1]
	return sum(not is_triangle(triplet) for triplet in itertools.combinations(sticks, 3))

print(checkio([4, 2, 10]), 1)
print(checkio([1, 2, 3]), 0)
print(checkio([5, 2, 9, 6]), 2)