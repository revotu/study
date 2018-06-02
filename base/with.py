

with open('input.txt', 'r') as source:
    with open('output.txt', 'w') as target:
        target.write(source.read())


with open('input.txt', 'r') as source, open('output.txt', 'w') as target:
    target.write(source.read())