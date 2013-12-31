def checkio(pair):
	b0 = bin(pair[0])[2:]
	b1 = bin(pair[1])[2:]
	maxlen = max(len(b0), len(b1))
	b0 = b0.zfill(maxlen)
	b1 = b1.zfill(maxlen)
	return sum(b0[i] != b1[i] for i in range(maxlen))

print(checkio([117, 17]), 3)
print(checkio([1, 2]), 2)
print(checkio([16, 15]), 5)