from matplotlib import pyplot


file_lengths = [
    109, 397, 52, 84, 66, 82, 223, 471, 89, 1639, 919, 59, 409, 209, 75, 68, 54, 50,
    267, 156, 118, 61, 1260, 592, 162, 544, 67, 731, 52, 89, 59, 1238, 943, 293, 
]
pyplot.hist(file_lengths, bins=20)

pyplot.xlabel('Value')
pyplot.ylabel('Frequency')

pyplot.show()