
from bisect import insort

def bouwkamp(code: str):
	code = code.replace(")(", " ").replace("(", "").replace(")", "")
	code = code.replace(",", " ").replace("  ", " ")
	return tablecode(code)

def tablecode(code: str):
    nums = [int(t) for t in code.split()]
    count, max_x, max_y, *sizes = nums
    if count != len(sizes):
        raise ValueError(f"header says {count} squares, got {len(sizes)}")

    skyline = [[0, max_x, 0]]
    squares = []
    i = 0

    while i < len(sizes):
        idx = min(range(len(skyline)), key=lambda k: skyline[k][2])
        seg_x, seg_w, y = skyline[idx]
        if y >= max_y:
            raise ValueError("more squares than the rectangle can hold")

        new_segs = []
        cx = seg_x
        while cx < seg_x + seg_w:
            if i >= len(sizes):
                raise ValueError("ran out of squares mid-row")
            s = sizes[i]
            if cx + s > seg_x + seg_w or y + s > max_y:
                raise ValueError(f"square {s} at ({cx},{y}) doesn't fit")
            squares.append([s, cx, y])
            new_segs.append([cx, s, y + s])
            cx += s
            i += 1

        skyline[idx:idx + 1] = new_segs

        merged = [skyline[0]]
        for seg in skyline[1:]:
            if seg[2] == merged[-1][2]:
                merged[-1][1] += seg[1]
            else:
                merged.append(seg)
        skyline = merged

    if any(seg[2] != max_y for seg in skyline):
        raise ValueError("squares don't fill the rectangle")

    return max_x, max_y, squares

def simple(code: str):
	squares = []

	parts = code[1:-1].split(")(")
	max_x, max_y = 0, 0
	for part in parts:
		square, x, y = [int(i) for i in part.split(" ")]
		max_x, max_y = max(max_x, x + square), max(max_y, y + square)
		squares.append([square, x, y])

	return max_x, max_y, squares

encodings = {
	'b': bouwkamp,
	't': tablecode,
	's': simple
}

import re
regexes = {
	's': re.compile(r"(\(\d+ \d+ \d+\))+"),
	't': re.compile(r"\d+ \d+ \d+( \d+)+"),
	'b': re.compile(r"\d+ \d+ \d+ (\(\d+((,|,? )\d+)*\))+")
}

def encoding(code: str):
	for key in regexes:
		if regexes[key].fullmatch(code):
			return key

def parse(code: str):
	return encodings[encoding(code)](code)