from PIL import Image
import math
import numpy
# Class to allow keeping track of x and y easier
class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

# Keeps track of RGB values of a pixel
class Pixel(object):
	def __init__(self, color = [-1, -1, -1], topLeft = Point(0, 0), bottomRight = Point(0, 0)):
		self.R = color[0]
		self.G = color[1]
		self.B = color[2]
		self.topLeft = topLeft
		self.bottomRight = bottomRight

# The main class
class QuadTree():
	def __init__(self, image):
		# Total number of nodes of tree
		self.size = 0
		# Store image pixelmap
		self.image = image.load()
		# Array of nodes
		self.tree = []
		self.x = image.size[0]
		self.y = image.size[1]
		# Total number of leaf nodes
		size = image.size[0] * image.size[1]
		# Count number of nodes
		while(size >= 1):
			self.size += size
			size /= 4
		size = image.size[0] * image.size[1]
		# Initialize array elements
		for i in range(0, self.size):
			self.tree.append(Pixel())
		f = open("File.txt", "w")
		f.write("\n")
		f.close()
		# Place nodes into array
		self.createNode(0, Point(0, 0), Point(self.x - 1, self.y - 1))
		
	def createNode(self, pos, topLeft, bottomRight):
		f = open("File.txt", "a")
		f.write(str(pos) + " " + str(topLeft.x) + " " + str(topLeft.y) + " " + str(bottomRight.x) + " " + str(bottomRight.y) + "\n")
		f.close()
		# Make sure node should exist
		if(pos >= self.size):
			return
		
		# Check if node is a leaf node
		if(topLeft.x == bottomRight.x and topLeft.y == bottomRight.y):
			self.tree[pos] = Pixel(self.image[topLeft.x, topLeft.y], topLeft, bottomRight)
			return

		# Parent of leaf nodes
		if(abs(topLeft.x - bottomRight.x) <= 1 and abs(topLeft.y - bottomRight.y) <= 1):
			mid = Point(topLeft.x + 1, topLeft.y)
			bottomMid = Point(topLeft.x, topLeft.y + 1)
			self.createNode(pos * 4 + 1, topLeft, topLeft)
			self.createNode(pos * 4 + 2, mid, mid)
			self.createNode(pos * 4 + 3, bottomMid, bottomMid)
			self.createNode(pos * 4 + 4, bottomRight, bottomRight)
		# Other nodes	
		else:		
			# Store relevant positions
			mid = Point((topLeft.x + bottomRight.x) / 2, (topLeft.y + bottomRight.y) / 2)
			topMid = Point((topLeft.x + bottomRight.x) / 2, topLeft.y)
			leftMid = Point(topLeft.x, (topLeft.y + bottomRight.y) / 2)
			rightMid = Point(bottomRight.x, (topLeft.y + bottomRight.y) / 2)
			bottomMid = Point((topLeft.x + bottomRight.x) / 2, bottomRight.y)

			# Create children of current node
			self.createNode(pos * 4 + 1, topLeft, mid)
			self.createNode(pos * 4 + 2, Point(topMid.x + 1, topMid.y), rightMid)
			self.createNode(pos * 4 + 3, Point(leftMid.x, leftMid.y + 1), bottomMid)
			self.createNode(pos * 4 + 4, Point(mid.x + 1, mid.y + 1), bottomRight)

		# Store requisite color information
		R = (self.tree[pos * 4 + 1].R + self.tree[pos * 4 + 2].R + 
			self.tree[pos * 4 + 3].R + self.tree[pos * 4 + 4].R) / 4
		G = (self.tree[pos * 4 + 1].G + self.tree[pos * 4 + 2].G + 
			self.tree[pos * 4 + 3].G + self.tree[pos * 4 + 4].G) / 4
		B = (self.tree[pos * 4 + 1].B + self.tree[pos * 4 + 2].B + 
			self.tree[pos * 4 + 3].B + self.tree[pos * 4 + 4].B) / 4
		
		# Update current node with values
		self.tree[pos] = Pixel([R, G, B], topLeft, bottomRight)
		
	def disp(self, level):
		start = 0
		# Calculate position of starting node of given height
		for i in range(0, level):
			start = 4 * start + 1
		# Invalid height given
		if(start > self.size):
			return
		# Create a new image
		img = Image.new("RGB", (self.x, self.y), "black")
		pixels = img.load()
        # Move from starting to last node on given height
		for i in self.tree[start : 4 * start]:
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
A = input("Input tree level\n")
tree.disp(A)
