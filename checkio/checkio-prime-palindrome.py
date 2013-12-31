import math
def checkio(n):
	def is_palindrome(n):
		return str(n) == str(n)[::-1]
	def is_prime(n):
		return all(n % i > 0 for i in range(2, int(math.sqrt(n)) + 1))
	m = n
	while True:
		if is_palindrome(m) and is_prime(m):
			return m
		m += 1

print(checkio(31), 101)
print(checkio(130), 131)
print(checkio(131), 131)