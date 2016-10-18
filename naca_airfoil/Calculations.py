
def mean(values):
	sum = 0
	for val in values:
		sum = sum + val

	return sum/len(values)


def calc_mean(file_name):
	lift_values = []
	drag_values = []
	with open(file_name, 'r') as f:
		for line in f:
			if 'drag' not in line
				all_values_of_line = line.split()
				lift_values.append(float(all_values_of_line[-2]))
				drag_values.append(float(all_values_of_line[-1]))

	start_val = int(len(lift_values)/3)
	return mean(lift_values[start_val:]), mean(drag_values[start_val:])
