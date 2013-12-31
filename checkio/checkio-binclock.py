def digit_to_binary(digit, bin_digits):
    assert 0 <= digit < 10
    if digit == 0:
        return '.' * bin_digits
    else:
        translation = str.maketrans('10', '-.')
        return bin(digit)[2:].translate(translation).rjust(bin_digits, '.')

def num_to_binary(num):
    assert 0 <= num < 100
    return digit_to_binary(num // 10, 3) + ' ' + digit_to_binary(num % 10, 4)

def checkio(time):
    hms = [int(part) for part in time.split(":")]
    bin_time = ' : '.join(num_to_binary(num) for num in hms)
    return bin_time[1:]

assert checkio( "10:37:49" ) == ".- .... : .-- .--- : -.. -..-"
assert checkio( "21:34:56" ) == "-. ...- : .-- .-.. : -.- .--."
assert checkio( "00:1:02" ) == ".. .... : ... ...- : ... ..-."
assert checkio( "23:59:59" ) == "-. ..-- : -.- -..- : -.- -..-"
