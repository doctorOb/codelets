"""A soon to be command line utility, which produces the best tuning to change to given you're current tuning, 
and the desired one."""

import string
import sys


notes = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]

nposition = {
	 "A" : 0,
	 "A#" : 1,
	 "B" : 2, 
	 "C" : 3, 
	 "C#" : 4,
	 "D" : 5,
	 "D#" : 6,
	 "E" : 7,
	 "F" : 8,
	 "F#" : 9,
	 "G" : 10,
	 "G#" : 11,
}

def calculate_note_distance(a,b):
	"""determine the number of (half) steps between two notes. This number is negative when a is higher then b"""
	original = nposition[b] - nposition[a]
	if abs(abs(original) - 12) < abs(original):
		return abs(original) - 12
	else:
		return original


def transpose(note,distance):
	nidx = nposition[note]
	tidx = nidx + distance
	if tidx >= 12:
		return notes[tidx - 12]
	else: 
		return notes[tidx]

def compute_optimal_tuning(target,current):
	"""determine the tuning which is symmetrically similar to *target* that can be reached from *current*, 
	within the minimum number of half step modifications"""
	target = target.split(' ')
	current = current.split(' ')
	initial = []
	abs_initial = []

	for i in range(0,len(target)):
		distance = calculate_note_distance(current[i],target[i])
		abs_initial.append(abs(distance))
		initial.append(distance)

	total_modifications = sum(abs_initial)
	winner = []
	min_sum = total_modifications
	for i in initial:
		mods = abs(i)
		tmp = []
		for i in initial:
			if i > 0:
				tmp.append(abs(i - mods))
			else:
				tmp.append(abs(i + mods))
		tsum = sum(tmp)
		if tsum < min_sum:
			min_sum = tsum
			winner = tmp

	ret = []
	for i in range(0,len(current)):
		t = transpose(note=current[i],distance=winner[i])
		print "{} -> {} ({}) modifications".format(current[i],t,winner[i])
		ret.append(t)

	
	return " ".join(ret)

if __name__ == '__main__':
	
	target_tuning = "C G C E G C"
	current_tuning = "D A C# E A C#"
	if len(sys.argv) > 2:
		current_tuning = sys.argv[1]
		target_tuning = sys.argv[2]


	assert calculate_note_distance("A","A") == 0
	assert calculate_note_distance("A","C") == 3
	assert calculate_note_distance("F","D") == -3
	assert transpose("G#",3) == "B"

	optimal = compute_optimal_tuning(target=target_tuning,current=current_tuning)
	print optimal