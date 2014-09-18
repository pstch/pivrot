from pivrot import results_table

PRIMES_FILE = './primes.txt'

with open(PRIMES_FILE) as primes_file:
    PRIMES = (
        int(text)
        for text in primes_file.readlines()
        if text and text != '\n'
    )

table = results_table(PRIMES)

for line in table:
    print(line)

