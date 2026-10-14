from draw import draw
from parse import parse

def export(svg, output, suffix=""):
	file_name = f"{output}/output{suffix}.svg"
	file = open(file_name, "w+", encoding="UTF8")
	file.write(str(svg))
	file.close()

def color(n, start="#505050", end="#ffffff"):
	if MAX_VAL == 1: return end
	import math
	n = max(1, min(n, MAX_VAL))

	# Position along the gradient, 0.0 to 1.0, on a log scale
	t = math.log(n) / math.log(MAX_VAL)

	# Parse hex colors into (r, g, b)
	def hex_to_rgb(h):
		h = h.lstrip("#")
		return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

	r1, g1, b1 = hex_to_rgb(start)
	r2, g2, b2 = hex_to_rgb(end)

	# Linear interpolation between the two colors
	r = round(r1 + (r2 - r1) * t)
	g = round(g1 + (g2 - g1) * t)
	b = round(b1 + (b2 - b1) * t)

	return f"#{r:02x}{g:02x}{b:02x}"

def verify_unique(squares):
	distinct = set()
	for square in squares:
		if square[0] in distinct: raise Exception(f"Verification error: square {square[0]} not distinct")
		distinct.add(square[0])

def create(code, output, scale=1, verify=False, suffix=""):
	x, y, squares = parse(code)
	if verify: verify_unique(squares)
	global MAX_VAL
	MAX_VAL = max(x, y)
	svg = draw(x, y, squares, scale=scale, color=color)
	export(svg, output, suffix=suffix)

def create_all(input, output, scale=1, verify=False):
	lines = open(input, "r").readlines()
	lines = [line.strip() for line in lines]
	for i in range(len(lines)):
		create(lines[i], output, scale=scale, verify=verify, suffix=i)

def test():
	code = "21 112 112 50 35 27 8 19 15 17 11 6 24 29 25 9 2 7 18 16 42 4 37 33"
	encoding = "t"
	create(code, encoding)

def parser():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-L", "--layout",
		help="layout of the squares"
	)
	parser.add_argument(
		"-s", "--scale",
		default="1",
		help="scale up the SVG"
	)
	parser.add_argument(
		"-v", "--verify-unique",
		action="store_true",
		help="verify the layout only has distinct squares"
	)
	from conf import TEST_LAYOUTS
	parser.add_argument(
		"-t", "--test",
		nargs="?",
		const="0",
		help=f"test the program with an example value (0-{len(TEST_LAYOUTS)-1})",
	)
	parser.add_argument(
		"-i", "--input",
		metavar="FILE",
		help="path for layouts. One output file will be produced per each layout"
	)
	from conf import DEFAULT_OUTPUT
	parser.add_argument(
		"-o", "--output",
		default=DEFAULT_OUTPUT,
		metavar="FILE",
		help="path for the SVG output file"
	)
	return parser

def main():
	args = parser().parse_args()

	layout = None
	if args.test != None: 
		from conf import TEST_LAYOUTS
		layout = TEST_LAYOUTS[int(args.test)]
	elif args.layout:
		layout = args.layout

	if args.input: create_all(
		args.input, 
		output=args.output, 
		scale=args.scale, 
		verify=args.verify_unique
	)
	else: create(
		layout, 
		output=args.output, 
		scale=args.scale, 
		verify=args.verify_unique
	)

if __name__ == '__main__':
	main()