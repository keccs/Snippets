def checkio(table):
	rows = table
	cols = [''.join([row[i] for row in table]) for i in range(3)]
	diags = [[table[i][i] for i in range(3)], [table[i][2-i] for i in range(3)]]

	def determine_winner(triple):
		if len(set(triple)) == 1:
			return triple[0]

	for row in rows + cols + diags:
		winner = determine_winner(row)
		if winner:
			return winner

	return 'D'

assert checkio([
    "X.O",
    "XX.",
    "XOO"]) == "X", "Xs wins"
assert checkio([
    "OO.",
    "XOX",
    "XOX"]) == "O"
assert checkio([
    "OOX",
    "XXO",
    "OXX"]) == "D"