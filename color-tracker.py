# by 8ryce
"""
Usuage: python3 color-tracker.py
		Hold an object in front of the camera, it will detect its color and track it
"""

"""
Opening out cam on cap 0, the built in / first connected cam ( for USB cams check where it is with the 'lsusb' cmd ) 
"""
import statistics
import time
import cv2
cap = cv2.VideoCapture(0)

#display class
"""
display handles all of our operations that involve showing data to the user
"""
class display():
	def __init__(self):
		self.WIDTH = 1800
		self.HEIGHT = 900
		self.DEFAULT_COLOR = (255,255,255)
		self.screen = cv2.namedWindow("Color Tracker", cv2.WINDOW_NORMAL)
		cv2.resizeWindow("Color Tracker", self.WIDTH,self.HEIGHT)
		_,self.image = cap.read()
		self.draw_start_box = True
		self.pic_height, self.pic_width,_ = self.image.shape
		self.start_box = [ (int(self.pic_width/2) - int(self.pic_width/10 )) ,
								(int(self.pic_height/2) - int(self.pic_height/10 )) ,
									(int(self.pic_width/2) + int(self.pic_width/10 )) , 
										(int(self.pic_height/2) + int(self.pic_height/10 )) ]

	"""
	updates image shown to user
	PARAMS: self, bb_cords-bounding box cordinates of found object
	RETURNS: NULL
	"""
	def update_image(self, bb_cords):
		_,self.image = cap.read()
		if self.draw_start_box == False:
			cv2.rectangle(self.image, ( bb_cords[0],bb_cords[1] ) , ( bb_cords[2],bb_cords[3] ) , self.DEFAULT_COLOR, 2) # cv2 takes in image, left/top, right/bottom, color, line thickness
		else:
			cv2.rectangle(self.image, ( self.start_box[0], self.start_box[1] ), ( self.start_box[2], self.start_box[3] ) , self.DEFAULT_COLOR, 2) # cv2 takes in image, left/top, right/bottom, color, line thickness
		cv2.imshow("Color Tracker", self.image)
		cv2.waitKey(10) & 0xFF

	"""
	sets the value for if we should draw the startup box
	PARAMS: self, tof-bool val for if we are doing it or not
	RETURNS: NULL
	"""
	def set_draw_start_box(self, tof):
		self.draw_start_box = tof

	"""
	getter pic_height and pic_width var
	PARAMS: self
	RETURNS: pic_height, pic_width - the displayed pics height and width
	"""
	def get_pic_size(self):
		return self.pic_height, self.pic_width

	"""
	getter for start box var
	PARAMS: self
	RETURNS: start_box- the starting detection box cords
	"""
	def get_start_box(self):
		return self.start_box

#tracker class
"""
Handles all of our computer vision detect logic
"""
class tracker():
	def __init__(self):
		self.color = [0,0,0]
		self.bb_cords = [0,0,0,0]

	"""
	scans for instances of the found color in an image, sets bb_cords if finds anything
	PARAMS: self, Display
	RETURNS: NULL, it just sets bb_cords if it finds something
	"""
	def scan_for_color(self,Display):
		# best way to scan whole pic? Lets try passing whole thing in first who knows it might work
		# lets make bounding box by:
		height, width = Display.get_pic_size()
		#print(height, width)
		left = width	# left = finding first instance of the object when going left to right
		right =	0   # right = keeping track of the farthest right val it is found at
		top = height 	# top = first val it is found row wise
		bottom = 0 	# bottom = last row it is found row wise
		counter = 0
		

		color = self.get_color()

		x,y = 0,0
		x_increment, y_increment = int(width/20), int(height/20)
		out_of_bounds_x = False
		out_of_bounds_y = False
		first_line_y = True
		first_line_x = True

		while y < height:
			#logic to make sure we add to our box only after the first section
			if y+y_increment <= height and first_line_y == False:
				y+= y_increment

				if y+y_increment > height:
					out_of_bounds_y = True

			#resetting x
			x = 0
			out_of_bounds_x = False
			first_line_y = False
			first_line_x = True

			while x < width:
				
				#if you want to see the progression of the box regions on the image
				#Display.update_image( [x,y, x+x_increment, y+y_increment] )
				
				if x+x_increment <= width and first_line_x == False:
					x += x_increment
					#print(x)
					
					if x+x_increment > width:
						out_of_bounds_x = True

				first_line_x = False
				if out_of_bounds_x == False and out_of_bounds_y == False:
					box = [x,y, x+x_increment, y+y_increment]
					#logic to find first and farthest occurance for x & first and last occurance for y
					#call to avg it
					
					rgb = self.avg_px_color(Display.image, box)

					#print(x,y,":",width,height,": color - ", rgb)

					#avg = abs(rgb - self.get_color())
					#avg = all( abs(r - c) < 10 for r in rgb and for c in self.get_color())
					avg = []

					for i in range(3):
						avg.append(abs(rgb[i] - color[i]))

					if all(i <= 20 for i in avg):
						#print(rgb, color)
						#time.sleep(3)
						#accepted_vals.append(avg)
						# first found ( x wise ) is cur left, if one is lower it replaces it
						if left > x:
							left = x+int(x_increment/2)
							#print("L:",left)
						
						# last found ( x wise ) is cur right, if one higher is found it replaces it
						if right < x:
							right = x+int(x_increment/2)
							#print("R:",right)

						# first match found is top
						if top > x:
							top = y+int(y_increment)
							#print("T:",top)

						# last match found is bottom
						bottom = y+int(y_increment)

				#time.sleep(.25)
				#else:
				#	print("out_of_bounds_x")
				

		"""
		print("\n\nLEFT: ", left)
		print("RIGHT: ",right)
		print("TOP: ", top)
		print("BOTTOM: ", bottom)
		print("COUNTER: ", counter)
		print("\n\n")
		"""
		self.set_bb_cords([left,top,right,bottom])
		
	"""
	detects color of object in our start box, sets color var
	PARAMS: self
	RETURNS: NULL
	"""
	def detect_color(self,Display):
		#when object is in box press key
		print("\n[INFO]\nFor best results, be sure to keep lighting consistent and ensure the object fills the entire box\n\n")
		print("Click on the pictures window and hold any key when desired object is in the box")
		choice = 255
		while choice == 255:
			choice = cv2.waitKey(5) & 0xFF
			Display.update_image(self.get_bb_cords())

		#call to set / avg color
		self.set_color(self.avg_px_color(Display.image, Display.get_start_box()))
	

	"""
	finds avg pxl val for a region of pxls
	PARAMS: self, image- image to check, box- region to check ( left,top,right,bottom )
	RETURNS: avg- average pxl color for a region
	"""
	def avg_px_color(self, image, box):
		#break up search region by x and y's ( search rows so we need to know how far over and how many down )

		#making a list to store all of our vals
		r_vals = []
		g_vals = []
		b_vals = []
			
		x,y = box[0],box[1] #adjust for starting point

		#print("L,T,R,B", box)

		#for how far down to go lets use box[3] for bottom
		while y < box[3]-4: #for y in range(box[3]):
			y += 4
			x = box[0]
			#for how far over to go lets take box[2] for right most
			while x < box[2]-4: #for x in range(box[2]):
				x+=4
				#print(y,x)
				#now that we have a cord pair within our box, lets take the val of cur pos and add to list
				
				rgb = image[y,x]
				r_vals.append(rgb[0])
				g_vals.append(rgb[1])
				b_vals.append(rgb[2])
				#print(rgb)
				#.append()
		r = statistics.mean(r_vals)
		g = statistics.mean(g_vals)
		b = statistics.mean(b_vals)
		#print(r,g,b)

		#display box in avg color it found
		#cv2.rectangle(image, ( box[0], box[1] ), ( box[2], box[3] ) ,(int(r),int(g),int(b)), 2) # cv2 takes in image, left/top, right/bottom, color, line thickness
		#cv2.imshow("Color Tracker", image)
		#cv2.waitKey(10) & 0xFF

		return [r,g,b]

	"""
	sets color var
	PARAMS: self, Color-the RGB for color we found
	RETURNS: NULL
	"""
	def set_color(self, Color):
		self.color = Color
	"""
	getter for color var
	PARAMS: self
	RETURNS: color
	"""
	def get_color(self): 
		return self.color
	"""
	sets bounding box cord var if we found something
	PARAMS: BB_cords-bounding box cords to save
	RETURNS: NULL
	"""
	def set_bb_cords(self, BB_cords):
		self.bb_cords = BB_cords
	
	"""	
	clears bb_cords var after a detection so we dont show detections longer than they appear
	PARAMS: self
	RETURNS: NULL
	"""
	def clear_bb_cords(self):
		self.bb_cords = [0,0,0,0]
	
	"""
	getter for bounding box cords var, clears when returned to make it free for next detection
	PARAMS: self
	RETURNS: bb_cords-current bounding box cords
	"""
	def get_bb_cords(self):
		BB_cords = self.bb_cords
		self.clear_bb_cords()
		return BB_cords

#Our little main loop
def main():
	Display = display()
	Tracker = tracker()
	image = cap.read()

	#call handler for color tracker
	ct_handler(Display, Tracker)

#Handles all of our color tracking and displaying
"""
PARAMS: Display- display class object for all of our display info, Tracker- our tracker class object for our computer vision operations
RETURNS: NULL
"""
def ct_handler(Display, Tracker):
	while True:

		#if not tracking a color yet
		if Tracker.get_color() == [0,0,0]:
			#draw starting box
			Display.set_draw_start_box(True)
			Tracker.detect_color(Display)
		#if tracking color
		else:
			Display.set_draw_start_box(False)
		
			Display.update_image(Tracker.get_bb_cords())
			#time.sleep(5)
			#search for color
			Tracker.scan_for_color(Display)
			#update bounding box with output of search ( if its still 0,0,0,0 nothing happens, else it prints )
			#time.sleep(5)

if __name__ == "__main__":
	main()