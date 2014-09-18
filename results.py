from pivrot import results_table

table = results_table(range(1, 10**6))

with open('results.txt', 'w') as file:
    for line in table:
        file.write(line + '\n')
        print(line)

