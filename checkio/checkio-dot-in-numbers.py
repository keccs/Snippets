def checkio(s):
	def reverse(l):
		return l[::-1]

	needs_dotting = True
	result = ''
	for index in reverse(range(len(s))):
		char = s[index]
		if char.isdigit():
			last_three_chars = result[-3:]
			last_three_are_digits = len(last_three_chars) == 3 and all(c.isdigit() for c in last_three_chars)
			if last_three_are_digits and needs_dotting:
				result += '.'
		else:
			needs_dotting = char.isspace()
		result += char
	return reverse(result)

print(checkio('123456'))
print(checkio('333'))
print(checkio('9999999'))
print(checkio('123456 567890'))
print(checkio('price is 5799'))
print(checkio('he was born in 1966th'))

assert checkio('123456') == '123.456'
assert checkio('333') == '333'
assert checkio('9999999') == '9.999.999'
assert checkio('123456 567890') == '123.456 567.890'
assert checkio('price is 5799') == 'price is 5.799'
assert checkio('he was born in 1966th') == 'he was born in 1966th'