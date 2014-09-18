from pivrot import results_table

table = results_table(range(1, 35), transform=lambda x: 2**x)

for line in table:
    print(line)

