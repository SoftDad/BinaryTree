# Binary Tree
import sys
import string
max_word_len = 9
base_letter_value = 10	# this makes each value at least 10 (two digits)
#print(base_letter_value, ord("A") - base_letter_value, ord("z") - base_letter_value) 

# Need a couple of global variables to compute average depth of search
word_count = 0
level_sum = 0

class Item:
	""" An item to be referenced from a Node it the tree """
	# for this type of Item, word is a single word (alpha only) up to 9 characters
	def __init__(self, word):
		self.word = word
#		print(self.word)
		# compute self.value - this is used for comparison in the binary tree
		# it is an 18-digit integer (just to keep withing 64 bits)
		ln = len(self.word)
		value_text = ""
		n_caps = 0
		if ln > max_word_len: ln = max_word_len
		for i in range(ln):		# limit the value computation to the first max_word_len letters
			num = letter_value(self.word[i])
			value_text = value_text + str(num)
			if is_upper(self.word[i]): n_caps += 1
		while len(value_text) < 2 * max_word_len:
			value_text += "00"
		self.value = int(value_text)
		self.value -= n_caps
#		print(self.value, self.word)			###
		
	# Check for equality of items, usint the computed value
	def __eq__(self, other):
		if not instance(other, Item):
			return NotImplemented
		return self.item.value == other.item.value
		
# Need few helper functions to support the BTree & friends
# Computer a letter value for the character, independant of case
def letter_value(ch):
#	""" Interleave upper and lower case, so value of a is that of A + 1, etc """
#	lval = ord(ch.lower)
#	if lval >= ord("A") and lval <= ord("Z"):		# It's upper case
#		ret_val = lval - ord("A") + base_letter_value
#	elif lval >= ord("a") and lval <= ord("z"):		# It's lower case
#		ret_val = lval - ord("a") + base_letter_value
	ret_val = ord(ch.lower()) - ord("a") + base_letter_value
	return ret_val
	
# Need a function to check if a character is a letter (including upper and lower case)
def is_letter(ch):
	val = ord(ch)
	return ((val >= ord("A") and val <= ord("Z")) or
		(val >= ord("a") and val <= ord("z")))	

# Need a couple of global variables to compute average depth of search
word_count = 0
level_sum = 0

# Is the character an upper case letter?
def is_upper(ch):
	lval = ord(ch)
	return lval >= ord("A") and lval <= ord("Z")
			
class Node:
	""" A node in the tree """
	def __init__(self, an_item, parent = None):
		self.item = an_item
		self.count = 0
		self.right = None
		self.left = None
		self.parent = parent
#		if self.parent is None:
#			self.node_count = 1
#		else:
#			self.node_count = self.parent.node_count + 1
#		up_node = self.parent
#		while up_node is not None:
#			self.node_count += up_node.node_count
#			up_node = up_node.parent		

class BTree:
	""" An ordered binary tree - each added item goes in it's place """
	def __init__(self):
		self.root = None
	
	def add_item (self, word):
		""" Make a new Item and put it into a new Node, then use add_node to place it in the tree"""
		item  = Item(word)
		node = Node(item)
		return self.add_node(node)
	
	def add_node (self, node, cur_node = None, level=0):  # Need to go recursive, starting with None => root
		"""Add a node to the tree in its ordered place"""
		global level_sum
		# retuns the count of occurances of the item
		if cur_node is None:
			cur_node = self.root
		if cur_node is None:
			self.root = node
			self.root.count += 1
			ret_val = self.root.count
		elif node.item.value < cur_node.item.value:
			if cur_node.left is None:
				cur_node.left = node
				node.count += 1
				node.parent = cur_node
				ret_val = self.root.count
				level_sum += level
			else:
				ret_val = self.add_node(node, cur_node.left, level+1)
		elif node.item.value > cur_node.item.value:
			if cur_node.right is None:
				cur_node.right = node
				node.count += 1
				node.parent = cur_node
				ret_val = self.root.count
				level_sum += level
			else:
				ret_val = self.add_node(node, cur_node.right, level+1)
		else:				# value equals cur_node.value
			cur_node.count += 1
			ret_val = cur_node.count		
		return ret_val
	
	def traverse(self, node_func, level, a_node = None):
		"""Traverse the tree, executing the the given function on each node"""
		global level_count
		global node_count
#		breakpoint()
		if a_node is None:
			a_node = self.root
#		breakpoint()
		if a_node is not None:
#			print(level, "got a node: ", a_node.item.word, "left: ", a_node.left)
			if a_node.left is not None:
				self.traverse(node_func, level + 1, a_node.left)
			node_func(a_node, level)
			node_count += 1
			level_count += level
#			print(level, "found one on right: ", a_node.item.word)
			if a_node.right is not None:
				self.traverse(node_func, level + 1, a_node.right)

	def search(self, word, func, level=0, new_item=[], a_node=None):
		"""searches through the tree for a node whose word is word."""
		# And go search for node.item with same value
		if a_node is None:
			a_node = self.root
			# First, make new item word, computing its value
			new_item = Item(word)
		else:
			if a_node.item is None:
				return None, level		# Error - a node without an item!
			elif  __eq__(node.item, new_item):	# we found it
				return word, level
			else:
				if new_item.value < a_node.item.value:
					self.search(a_node.left, level + 1, new_item)
				elif new_item.value > a_node.item.value:
					self.search(a_node.right, level + 1, new_item)

# Instatiate the tree - we'll be needing it soon...
b_tree = BTree()

# Take words from a long stream and add each one to the tree...
words = """It was the best of times, it was the worst of times, 
it was the age of wisdom, it was the age of foolishness, 
it was the epoch of belief, it was the epoch of incredulity, 
it was the season of Light, it was the season of Darkness, 
it was the spring of hope, it was the winter of despair, 
we had everything before us, we had nothing before us, 
we were all going direct to Heaven, 
we were all going direct the other way-in short, 
the period was so far like the present period, 
that some of its noisiest authorities insisted on its being received, 
for good or for evil, in the superlative degree of comparison only. 
There were a king with a large jaw and a queen with a plain face, 
on the throne of England; 
there were a king with a large jaw and a queen with a fair face, 
on the throne of France. 
In both countries it was clearer than crystal 
to the lords of the State preserves of loaves and fishes, 
that things in general were settled for ever. 
It was the year of Our Lord one thousand seven hundred and seventy-five."""

# Parse the text, inserting each word item into the tree
def parse_text (words, func):
	i = 0
	while i < len(words):
		global word_count
		start = i
		while i < len(words) and not is_letter(words[i]):
			i += 1
			start = i
	#	print(f"start is {start}")					###
		while i < len(words) and is_letter(words[i]):
			i += 1
			end = i
	#	print(f"end is {end}")						###
		word = words[start:end]
		if len(word) > 0:
	#		print(len(word), word)					###
	#		node = Node(Item(word))
	#		print ("Node: ", node.item.word) 		###
			func(word)
			word_count += 1
			
parse_text (words, b_tree.add_item)

print ("Word count:", word_count, ", Level sum:", level_sum)
print ("Average level:", level_sum/word_count)

def print_node(a_node, level):
#	global level
	print(a_node.item.value, level, a_node.item.word)	



# Traverse the tree, printing each node
node_count = 0
level_count = 0
print()
print("OK, Here are the nodes, in order, with value and level:")
b_tree.traverse(print_node, 0)

print ("\nNode count:", node_count, ", Level sum:", level_sum)
print ("Average level:", level_sum/node_count)

# Search the tree for each word, return level of depth for each
	
	


	