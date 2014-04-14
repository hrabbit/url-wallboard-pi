import os
import pygame
import time

class layout :
	screen = None;
	size = None;

	def __init__(self, configuration):
	        "Ininitializes a new pygame screen using the framebuffer"
		self.configuration = configuration
	        # Based on "Python GUI in Linux frame buffer"            
	        # http://www.karoltomala.com/blog/?p=679                 
	        disp_no = os.getenv("DISPLAY")                           
	        if disp_no:                                              
			print "I'm running under X display = {0}".format(disp_no)
                                                                     
		# Check which frame buffer drivers are available             
	        # Start with fbcon since directfb hangs with composite output
	        drivers = ['fbcon', 'directfb', 'svgalib']                   
	        found = False                                                
	        for driver in drivers:                                       
			# Make sure that SDL_VIDEODRIVER is set                  
			if not os.getenv('SDL_VIDEODRIVER'):                     
				os.putenv('SDL_VIDEODRIVER', driver)                 
			try:                                                     
				pygame.display.init()               
			except pygame.error:                    
				print 'Driver: {0} failed.'.format(driver)
				continue                                  
			found = True                                  
			break                                         
                                                          
		if not found:                                     
			raise Exception('No suitable video driver found!')
                                                              
		self.size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
	        print "Framebuffer size: %d x %d" % (self.size[0], self.size[1])                   
	        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)           
	        # Clear the screen to start                                              
	        self.screen.fill((0, 0, 0))                                              
	        # Initialise font support                                                
	        pygame.font.init()                                                       
		# Disable the mouse
		pygame.mouse.set_visible(False)
	        # Render the screen                                                      
	        pygame.display.update() 

	def render(self, records) :
		borderColor = (255, 255, 255)
		lineColor = (64, 64, 64)                        
		subDividerColor = (128, 128, 128)      
		#pygame.draw.rect(self.screen, borderColor, (0,0,self.size[0],self.size[1]), 4)

		'''
		 {u'average_wait_time': u'0:00:00',
		  u'average_wait_time_seconds': 0,
		  u'callers': [],
		  u'calls_active': 0,
		  u'calls_waiting': 0,
		  u'logged_in': [u'Alex', u'Neri', u'Charles', u'Jovanne'],
		  u'longest_wait_time': u'0:00:00',
		  u'longest_wait_time_seconds': 0,
		  u'portlet_id': u'105',
		  u'queue_name': u'Other',
		  u'queue_number': u'3',
		  u'type': u'queue_stats'},
		'''

		# Clear the screen so we don't overwrite data directly
	        self.screen.fill((0, 0, 0))                                              

		# We need to find out how many records we will be rendering
		vertWidth = self.size[0]/len(records)

		row_height = 70

		colours = {
			'white': (255, 255, 255),
			'red': (255, 0, 0),
			'blue': (0, 0, 255),
			'orange': (255, 100, 0),
			'gray': (50, 50, 50)
		}

		colour = colours['white']

		for i in range(0, len(records)):

			pygame.draw.line(self.screen, colours['orange'], (0, 90), (self.size[0],90), 1)
			pygame.draw.line(self.screen, colours['orange'], (0, 340), (self.size[0],340), 1)

			pygame.draw.line(self.screen, colours['gray'], (i*vertWidth, 0), (i*vertWidth, self.size[1]), 1)

			#print "Col: {} > {}" .  format(i*vertWidth, (i+1)*vertWidth)
			#pygame.draw.rect(self.screen, borderColor, (i*vertWidth,0,(i+1)*vertWidth,self.size[1]), 1)

			colour = colours['blue']

		        font = pygame.font.Font(None, 120)
			queue_name = font.render('%s' % records[i]['queue_name'],True, colour)  # White text                              
			self.screen.blit(queue_name, ((i*vertWidth)+10, 0)) 

		        font = pygame.font.Font(None, 80)

			colour = colours['white']

			calls_waiting_label = font.render('Calls waiting:',True, colour)  # White text                              
			self.screen.blit(calls_waiting_label, ((i*vertWidth)+10, row_height*2)) 

			calls_waiting = font.render('%s' % records[i]['calls_waiting'], True, colour)  # White text                              
			size = font.size('%s' % records[i]['calls_waiting'])
			self.screen.blit(calls_waiting, (((i+1)*vertWidth)-size[0]-10, row_height*2)) 

			longest_wait_time_label = font.render('Wait time:',True, colour)  # White text                              
			self.screen.blit(longest_wait_time_label, ((i*vertWidth)+10, row_height*3)) 

			if(records[i]['longest_wait_time_seconds'] > 30):
				colour = colours['orange']
			elif(records[i]['longest_wait_time_seconds'] > 60):
				colour = colours['red']
			else:
				colour = colours['white']

			longest_wait_time = font.render('%s' % records[i]['longest_wait_time'], True, colour)  # White text                              
			size = font.size('%s' % records[i]['longest_wait_time'])
			self.screen.blit(longest_wait_time, (((i+1)*vertWidth)-size[0]-10, row_height*3)) 
			
			calls_active_label = font.render('Active calls:',True, colour)  # White text                              
			self.screen.blit(calls_active_label, ((i*vertWidth)+10, row_height*4)) 

			calls_active = font.render('%s' % records[i]['calls_active'], True, colour)  # White text                              
			size = font.size('%s' % records[i]['calls_active'])
			self.screen.blit(calls_active, (((i+1)*vertWidth)-size[0]-10, row_height*4)) 

			row = 4
			for j in records[i]['logged_in']:
				row += 1
				agent = font.render('%s' % j, True, colour)
				self.screen.blit(agent, ((i*vertWidth)+10, row_height*row)) 

#		text_surface = font.render('pyScope (%s)' % "123",True, (255, 255, 255))  # White text                              
		# Blit the text at 10, 0                                      

		pygame.display.update()                          
		return

	        def __del__(self):
	        	"Destructor to make sure pygame shuts down, etc."

