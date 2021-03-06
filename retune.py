"""A soon to be command line utility, which produces the best tuning to change to given your current tuning,
and the desired one.

More concisely:

If you are in Tuning A, and want to achieve Tuning B (but don't care about the exact key tuning B is in), then
this program will determine the most optimal Tuning C, which conforms to B (but is raised or lowered uniformly by
a number of half steps), and does so in the fewest amount of half step modifications done to the guitar.

Motivation: I change between alternate tunings, and I don't like to leap up multiple steps per string each time"""

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
  return (abs(original) - 12) if (abs(abs(original) - 12) < abs(original)) else original


def transpose(note,distance):
  nidx = nposition[note]
  tidx = nidx + distance
  return notes[tidx % 12]

def compute_optimal_tuning(target,current):
  """determine the tuning which is symmetrically similar to *target* that can be reached from *current*,
  within the minimum number of half step modifications"""
  target = target.split(' ')
  current = current.split(' ')

  initial = [calculate_note_distance(current[i],target[i]) for i in range(min(len(current), len(target)))]
  total_modifications = reduce(lambda x,y: abs(x) + abs(y), initial)

  winner = []
  min_sum = total_modifications
  for i in initial:
    mods = abs(i)
    tmp = [abs(i - mods) if i > 0 else abs(i + mods) for i in initial]
    tsum = sum(tmp)
    if tsum < min_sum:
      min_sum = tsum
      winner = tmp
  #transpose the current tuning into the optimal one
  ret = [transpose(note=current[i],distance=winner[i]) for i in range(min(len(current), len(target)))]
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
