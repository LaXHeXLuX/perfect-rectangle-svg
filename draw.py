import svg

STROKE_WIDTH = 0.1

def rect(w: int, h: int, color: str = "none"):
	return svg.Rect(
		width=w, height=h,
		fill=color,
		stroke="black",
		stroke_width=STROKE_WIDTH
	)

def square(size: int, color: str = "none"):
	return svg.SVG(
		width=size, height=size,
		elements=[
			rect(size, size, color),
			svg.Text(
				x="50%", y="50%",
				text=size,
				font_size=max(1, size/5),
				color="black",
				dominant_baseline="central",
				text_anchor="middle"
			)
		]
	)

def outer(w, h, scale=1, color="none"):
	return svg.SVG(
		width=scale*w,
		height=scale*h,
		viewBox = f"0 0 {w} {h}",
		elements=[rect(w, h, color=color)]
	)

def draw(w: int, h: int, squares: list, scale=1, color = lambda _ : "none"):
	canvas = outer(w, h, scale=scale)
	canvas.elements[0].stroke_width = STROKE_WIDTH * 2

	for s, x, y in squares:
		sq = square(s, color=color(s))
		sq.x, sq.y = x, y
		canvas.elements.append(sq)

	return canvas