from PIL import Image
import math
import numpy as np
# Class to allow keeping track of x and y easier
class Point(object):
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)

# Keeps track of RGB values of a pixel
class Pixel(object):
	def __init__(self, color = [-1, -1, -1], topLeft = Point(0, 0), bottomRight = Point(0, 0)):
		self.R = int(color[0])
		self.G = int(color[1])
		self.B = int(color[2])
		self.topLeft = topLeft
		self.bottomRight = bottomRight

# The main class
class QuadTree():
	def __init__(self, image):
		# Store image pixelmap
		self.image = image.load()
		self.x = image.size[0]
		self.y = image.size[1]
		# Total levels in tree
		self.levels = int(np.log2(max(self.x, self.y) - 1) + 2)
		# Array of nodes
		self.tree = []
		for i in range(self.levels):
		    self.tree.append([])
		# Place nodes into array
		self.createNode(0, Point(0, 0), Point(self.x - 1, self.y - 1))
		
	def createNode(self, pos, topLeft, bottomRight):
		# Check if node is a leaf node
		if(topLeft.x == bottomRight.x and topLeft.y == bottomRight.y):
			self.tree[pos].append(Pixel(self.image[topLeft.x, topLeft.y], topLeft, bottomRight))
			return Pixel(self.image[topLeft.x, topLeft.y], topLeft, bottomRight)

		# Store relevant positions
		mid = Point((topLeft.x + bottomRight.x) / 2, (topLeft.y + bottomRight.y) / 2)
		topMid = Point((topLeft.x + bottomRight.x) / 2, topLeft.y)
		leftMid = Point(topLeft.x, (topLeft.y + bottomRight.y) / 2)
		rightMid = Point(bottomRight.x, (topLeft.y + bottomRight.y) / 2)
		bottomMid = Point((topLeft.x + bottomRight.x) / 2, bottomRight.y)

		nodes = []
		# Create children of current node
		nodes.append(self.createNode(pos + 1, topLeft, mid))
		if(topLeft.x != bottomRight.x):
			nodes.append(self.createNode(pos + 1, Point(topMid.x + 1, topMid.y), rightMid))
		if(topLeft.y != bottomRight.y):
			nodes.append(self.createNode(pos + 1, Point(leftMid.x, leftMid.y + 1), bottomMid))
		if(topLeft.x != bottomRight.x and topLeft.y != bottomRight.y):
			nodes.append(self.createNode(pos + 1, Point(mid.x + 1, mid.y + 1), bottomRight))
		
		R, G, B = 0, 0, 0
		# Store requisite color information
		for i in nodes:
			R = R + i.R
			G = G + i.G
			B = B + i.B
			
		R = R / len(nodes)
		G = G / len(nodes)
		B = B / len(nodes)
		
		# Update current node with values
		self.tree[pos].append(Pixel([R, G, B], topLeft, bottomRight))
		return Pixel([R, G, B], topLeft, bottomRight)
		
	def disp(self, level):
		# Invalid height given
		if(level >= self.levels):
			print("Invalid tree level")
			return
		# Create a new image
		img = Image.new("RGB", (self.x, self.y), "black")
		pixels = img.load()
		# Move from starting to last node on given height
		for i in self.tree[level]:
			x1 = i.topLeft.x
			y1 = i.topLeft.y
			x2 = i.bottomRight.x
			y2 = i.bottomRight.y
			for x in range(x1, x2 + 1):
				for y in range(y1, y2 + 1):
					# Set colour
					pixels[x,y] = (i.R, i.G, i.B)
		# Display image
		img.show()


img_name = raw_input("Enter name of image\n")
img = Image.open(img_name).convert("RGB")
tree = QuadTree(img)
A = input("Input tree level (0 = Most Compressed - " + str(tree.levels - 1) + " = Original Image)")
tree.disp(A)
