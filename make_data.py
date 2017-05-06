import numpy as np

file = open('data.txt', 'w')
parts =[]
for i in range(1,7):
    for j in range(1,7):
        parts.append('RX{0}{1}'.format(i,j))
random = np.random.randint(0, 10, len(parts))
file.write('# The Title of the File \n')
file.write('# lines with # are not read in \n')
file.write('<Dataset>\tfission\n')
for id, part in enumerate(parts):
    print(part)
    print(random[id])
    file.write(part + '\t{}\n'.format(random[id]))

file.close()