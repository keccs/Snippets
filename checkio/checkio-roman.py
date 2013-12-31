roman_rules = (
	('M' , 1000),
	('CM', 900),
	('D' , 500),
	('CD', 400),
	('C' , 100),
	('XC', 90),
	('L' , 50),
	('XL', 40),
	('X' , 10),
	('IX', 9),
	('V' , 5),
	('IV', 4),
	('I' , 1))

def roman_numeral(n):
	for rule in roman_rules:
		roman, value = rule[0], rule[1]
		if n // value:
			return roman + roman_numeral(n - value)
	return ''

def checkio(n):
	return roman_numeral(n)

assert checkio(6) == 'VI', '6'
assert checkio(76) == 'LXXVI', '76'
assert checkio(499) == 'CDXCIX', '499'
assert checkio(3888) == 'MMMDCCCLXXXVIII', '3888'