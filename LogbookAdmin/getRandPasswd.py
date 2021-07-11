from sys import exit, argv
import numpy as np

if __name__ == '__main__':
	if len(argv) < 2:
		print("Usage: getRandPasswd [length]")
		exit(0)
	N = int(argv[1])
	chars = [chr(ord('a') + i) for i in range(0, 26)] + [chr(ord('A') + i) for i in range(0, 26)] + range(0, 10)
	chars += "@!$&*"
	indices = np.random.randint(0, len(chars), N)
	string = ""
	for idx in indices:
		string = "%s%s"%(string, chars[idx])
	print(string)
