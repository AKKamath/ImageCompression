from PIL import Image
import math
import numpy
class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
class Pixel(object):
	def __init__(self, color = [0, 0, 0], topLeft = Point(0, 0), bottomRight = Point(0, 0)):
		self.R = color[0]
		self.G = color[1]
		self.B = color[2]
		self.topLeft = topLeft
		self.bottomRight = bottomRight
	def update(self, child1, child2, child3, child4):
		self.R = (child1.R + child2.R + child3.R + child4.R) / 4
		self.G = (child1.G + child2.G + child3.G + child4.G) / 4
		self.B = (child1.B + child2.B + child3.B + child4.B) / 4
		self.topLeft.x = min(child1.topLeft.x, child2.topLeft.x, child3.topLeft.x, child4.topLeft.x)
		self.topLeft.y = min(child1.topLeft.y, child2.topLeft.y, child3.topLeft.y, child4.topLeft.y)
		print "Debug" + str(min(child1.topLeft.x, child2.topLeft.x, child3.topLeft.x, child4.topLeft.x))
		self.bottomRight.x = max(child1.bottomRight.x, child2.bottomRight.x, child3.bottomRight.x, child4.bottomRight.x)
		self.bottomRight.y = max(child1.bottomRight.y, child2.bottomRight.y, child3.bottomRight.y, child4.bottomRight.y)

class quadtree():
	def __init__(self, image):
		self.size = 0
		self.image = image.load()
		self.tree = []
		self.x = image.size[0]
		self.y = image.size[1]
		size = image.size[0] * image.size[1]
		while(size >= 1):
			self.size += size
			size /= 4
		size = image.size[0] * image.size[1]
		for i in range(0, self.size):
			self.tree.append(1)
			self.tree[i] = Pixel([0, 0, 0])
		count = 0
		for i in range(image.size[0] - 1, 0, -2):
			for j in range(image.size[1] - 1, 0, -2):
				self.tree[self.size - 1 - 4 * count] = Pixel(self.image[i, j], Point(i, j), Point(i, j))
				self.tree[self.size - 2 - 4 * count] = Pixel(self.image[i, j - 1], Point(i, j - 1), Point(i, j - 1))
				self.tree[self.size - 3 - 4 * count] = Pixel(self.image[i - 1, j], Point(i - 1, j), Point(i - 1, j))
				self.tree[self.size - 4 - 4 * count] = Pixel(self.image[i - 1, j - 1], Point(i - 1, j - 1), Point(i - 1, j - 1))
				count += 1
		for i in range(self.size - 4 * count - 1, self.size - 4 * count - 3, -1):
			self.tree[i] = Pixel([self.tree[i].R + self.tree[i].R + self.tree[i].R + self.tree[i].R, 0, 0], self.tree[4 * i + 1].topLeft, self.tree[4 * i + 1].bottomRight)
		f = open("File.txt", "w")
		for i in range(self.size - 1, -1, -1):
			f.write(str(self.tree[i].topLeft.x) + " " + str(self.tree[i].bottomRight.x) + " " + str(self.tree[i].topLeft.y) + " " + str(self.tree[i].bottomRight.y) + " " + str(i) + "\n")
	def disp(self, level):
		start = 0
		for i in range(0, level):
			start = 4 * start + 1
		if(start > self.size):
			return
		img = Image.new("RGB", (self.x, self.y), "black")
		pixels = img.load()
		for i in self.tree[start:4 * start]:
			x1 = i.topLeft.x
			y1 = i.topLeft.y
			x2 = i.bottomRight.x
			y2 = i.bottomRight.y
			for x in range(x1, x2 + 1):
				for y in range(y1, y2 + 1):
					pixels[x,y] = (i.R, i.G, i.B) # set the colour accordingly
		img.show()
		
img = Image.open("Image.ico").convert("RGB")
tree = quadtree(img)
A = input("Input tree level\n")
tree.disp(A)
