import pygame
import os
import io
from lol_winrates.scrape import top_tierlist, jungle_tierlist, mid_tierlist, adc_tierlist, support_tierlist
from urllib.request import urlopen
import sys

#-----------------------------------------------------------------
#The code in this file has not yet been furnished and optimized.
#-----------------------------------------------------------------

class Window():
	def __init__(self, win):
		pygame.init()
		self.current_path = os.path.dirname(__file__) 
		self.resource_path = os.path.join(self.current_path, 'res')
		self.win = win
		self.background = pygame.image.load(os.path.join(self.resource_path,'background.png'))
		self.coverLoad = pygame.image.load(os.path.join(self.resource_path,'replacement_background.png'))
		self.button = pygame.image.load(os.path.join(self.resource_path,'button.png'))
		self.highlight = pygame.image.load(os.path.join(self.resource_path,'highlight.png'))
		self.icon = pygame.image.load(os.path.join(self.resource_path,'icon.png'))

		self.highlighted = False
		self.win.blit(self.background, (0,0))

		self.reload = True
		self.dontLoadBar = False

		self.font = pygame.font.Font(os.path.join(self.resource_path,'monog__.ttf'), 32)
		self.font_pick = pygame.font.Font(os.path.join(self.resource_path,'monog__.ttf'), 25)

		self.current_load = 0
		self.total_load = 65
		self.dontLoadBar = False

		#Graphics
		self.frame_animations_first = True
		self.alpha_value = 0
		self.data_alpha_value = 0
		self.coverLoad_alpha_value = 0

		#Containers
		self.top_image_render = False
		self.top_image_list = []
		self.top_winrate_list = []
		self.jungle_image_render = False
		self.jungle_image_list = []
		self.jungle_winrate_list = []
		self.mid_image_render = False
		self.mid_image_list = []
		self.mid_winrate_list = []
		self.bot_image_render = False
		self.bot_image_list = []
		self.bot_winrate_list = []
		self.sup_image_render = False
		self.sup_image_list = []
		self.sup_winrate_list = []

	def run(self):
		run = True
		clock = pygame.time.Clock()

		while run:
			clock.tick(30)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					pygame.quit()
					sys.exit(0)

				if pygame.mouse.get_pos()[0] >= 960-39 and pygame.mouse.get_pos()[1] >= 540-39:
					if pygame.mouse.get_pressed()[0]:
						self.info_screen()
					self.highlighted = True
				else:
					self.highlighted = False
			
			if self.alpha_value <= 40:
				self.alpha_value += 1
			elif self.data_alpha_value <= 40:
				self.data_alpha_value += 1

			self.draw()

		pygame.quit()

	def draw(self):

		if self.reload:
			if self.alpha_value <= 40:
				if not self.dontLoadBar:
					loadbar = pygame.draw.rect(self.win, (255,255,255), (191,500,575,5), 1 )
				self.createDivider(191,150, "top", 96, 40)
				self.createDivider(382,150, "jung", 288, 40)
				self.createDivider(575,150, "mid", 480, 40)
				self.createDivider(766,150, "bot", 672, 40)
				self.createDivider(-1,-1, "sup", 864, 40)
				self.load()

			elif self.data_alpha_value <= 40:
				self.displayInfo(top_tierlist, 'top')
				if not (self.top_image_render and self.jungle_image_render and self.mid_image_render and self.bot_image_render and self.sup_image_render):
					loadstate = pygame.draw.rect(self.win, (255,255,255), (191,502, (self.current_load*575)/self.total_load ,1) )
				self.displayInfo(jungle_tierlist, 'jung')
				if not (self.top_image_render and self.jungle_image_render and self.mid_image_render and self.bot_image_render and self.sup_image_render):
					loadstate = pygame.draw.rect(self.win, (255,255,255), (191,502, (self.current_load*575)/self.total_load ,1) )
				self.displayInfo(mid_tierlist, 'mid')
				if not (self.top_image_render and self.jungle_image_render and self.mid_image_render and self.bot_image_render and self.sup_image_render):
					loadstate = pygame.draw.rect(self.win, (255,255,255), (191,502, (self.current_load*575)/self.total_load ,1) )
				self.displayInfo(adc_tierlist, 'bot')
				if not (self.top_image_render and self.jungle_image_render and self.mid_image_render and self.bot_image_render and self.sup_image_render):
					loadstate = pygame.draw.rect(self.win, (255,255,255), (191,502, (self.current_load*575)/self.total_load ,1) )
				self.displayInfo(support_tierlist, 'sup')
				if not (self.top_image_render and self.jungle_image_render and self.mid_image_render and self.bot_image_render and self.sup_image_render):
					loadstate = pygame.draw.rect(self.win, (255,255,255), (191,502, (self.current_load*575)/self.total_load ,1) )

			loadstate = pygame.draw.rect(self.win, (255,255,255), (191,502, (self.current_load*575)/self.total_load ,1) )

			if self.top_image_render and self.jungle_image_render and self.mid_image_render and self.bot_image_render and self.sup_image_render:
				self.win.blit(self.coverLoad, (0,0))

			if self.data_alpha_value >= 40:
				self.reload = False

		self.win.blit(self.button, (0,0))

		if self.highlighted:
			self.win.blit(self.highlight, (0,0))

		pygame.display.update()

	def createDivider(self, x, y, role, roleX, roleY):
		divider = pygame.Surface((1,240))  
		divider.fill((255,255,255))

		text = self.font.render(role, True, (255,255,255))
		alpha_img = pygame.Surface(text.get_size(), pygame.SRCALPHA)
		alpha_img.fill((255, 255, 255, self.alpha_value))
		text.blit(alpha_img, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
		textRect = text.get_rect()
		textRect.center = (roleX, roleY)

		divider.set_alpha(self.alpha_value)  
		text.set_alpha(self.alpha_value)  

		self.win.blit(divider, (x,y))
		self.win.blit(text, (textRect))  

		pygame.display.update()

	def displayInfo(self, data, role):

		if role == 'top':

			imgX = 18
			imgY = 90

			winrateX = 128
			winrateY = 99

			pickrateX = 128
			pickrateY = 128

			if not self.top_image_render:
				for champion in data:
					image_url = data[champion][1]
					image_str = urlopen(image_url).read()
					image_file = io.BytesIO(image_str)
					image = pygame.image.load(image_file).convert(self.win)
					image = pygame.transform.scale(image,(50,50))
					self.top_image_list.append(image)
					self.top_winrate_list.append(data[champion][0])
					self.top_image_render = True
					self.load()

			for i in self.top_image_list:
				i.set_alpha(self.data_alpha_value)  
				self.win.blit(i, (imgX,imgY))
				imgY += 50 + 35

			for champion in data:
				#Winrate
				text = self.font.render(data[champion][0], True, (255,255,255))
				alpha_img = pygame.Surface(text.get_size(), pygame.SRCALPHA)
				alpha_img.fill((255, 255, 255, self.data_alpha_value))
				text.blit(alpha_img, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
				textRect = text.get_rect()
				textRect.center = (winrateX, winrateY)
				text.set_alpha(self.data_alpha_value) 

				#Pickrate
				text_pick = self.font_pick.render(data[champion][2], True, (255,255,255))
				alpha_img_pick = pygame.Surface(text_pick.get_size(), pygame.SRCALPHA)
				alpha_img_pick.fill((255, 255, 255, self.data_alpha_value))
				text_pick.blit(alpha_img_pick, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
				textRect_pick = text_pick.get_rect()
				textRect_pick.center = (pickrateX, pickrateY)
				text_pick.set_alpha(self.data_alpha_value) 

				self.win.blit(text, (textRect)) 
				winrateY += 50 + 35

				self.win.blit(text_pick, (textRect_pick)) 
				pickrateY += 50 + 35

				pygame.display.update()

		if role == 'jung':

			imgX = 18+192
			imgY = 90

			winrateX = 128+192
			winrateY = 99

			pickrateX = 128+192
			pickrateY = 128

			if not self.jungle_image_render:
				for champion in data:
					image_url = data[champion][1]
					image_str = urlopen(image_url).read()
					image_file = io.BytesIO(image_str)
					image = pygame.image.load(image_file).convert(self.win)
					image = pygame.transform.scale(image,(50,50))
					self.jungle_image_list.append(image)
					self.jungle_winrate_list.append(data[champion][0])
					self.jungle_image_render = True
					self.load()			

			for i in self.jungle_image_list:
				i.set_alpha(self.data_alpha_value)  
				self.win.blit(i, (imgX,imgY))
				imgY += 50 + 35

			for champion in data:
				#Winrate
				text = self.font.render(data[champion][0], True, (255,255,255))
				alpha_img = pygame.Surface(text.get_size(), pygame.SRCALPHA)
				alpha_img.fill((255, 255, 255, self.data_alpha_value))
				text.blit(alpha_img, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
				textRect = text.get_rect()
				textRect.center = (winrateX, winrateY)
				text.set_alpha(self.data_alpha_value)

				#Pickrate
				text_pick = self.font_pick.render(data[champion][2], True, (255,255,255))
				alpha_img_pick = pygame.Surface(text_pick.get_size(), pygame.SRCALPHA)
				alpha_img_pick.fill((255, 255, 255, self.data_alpha_value))
				text_pick.blit(alpha_img_pick, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
				textRect_pick = text_pick.get_rect()
				textRect_pick.center = (pickrateX, pickrateY)
				text_pick.set_alpha(self.data_alpha_value) 
 
				self.win.blit(text, (textRect)) 
				winrateY += 50 + 35

				self.win.blit(text_pick, (textRect_pick)) 
				pickrateY += 50 + 35
				pygame.display.update()

		if role == 'mid':

			imgX = 18+192+192
			imgY = 90

			winrateX = 128+192+192
			winrateY = 99

			pickrateX = 128+192+192
			pickrateY = 128

			if not self.mid_image_render:
				for champion in data:
					image_url = data[champion][1]
					image_str = urlopen(image_url).read()
					image_file = io.BytesIO(image_str)
					image = pygame.image.load(image_file).convert(self.win)
					image = pygame.transform.scale(image,(50,50))
					self.mid_image_list.append(image)
					self.mid_winrate_list.append(data[champion][0])
					self.mid_image_render = True
					self.load()
					pygame.display.update()

			for i in self.mid_image_list:
				i.set_alpha(self.data_alpha_value)  
				self.win.blit(i, (imgX,imgY))
				imgY += 50 + 35

			for champion in data:
				#Winrate
				text = self.font.render(data[champion][0], True, (255,255,255))
				alpha_img = pygame.Surface(text.get_size(), pygame.SRCALPHA)
				alpha_img.fill((255, 255, 255, self.data_alpha_value))
				text.blit(alpha_img, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
				textRect = text.get_rect()
				textRect.center = (winrateX, winrateY)
				text.set_alpha(self.data_alpha_value) 

				#Pickrate
				text_pick = self.font_pick.render(data[champion][2], True, (255,255,255))
				alpha_img_pick = pygame.Surface(text_pick.get_size(), pygame.SRCALPHA)
				alpha_img_pick.fill((255, 255, 255, self.data_alpha_value))
				text_pick.blit(alpha_img_pick, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
				textRect_pick = text_pick.get_rect()
				textRect_pick.center = (pickrateX, pickrateY)
				text_pick.set_alpha(self.data_alpha_value) 

				self.win.blit(text, (textRect)) 
				winrateY += 50 + 35

				self.win.blit(text_pick, (textRect_pick)) 
				pickrateY += 50 + 35


		if role == 'bot':

			imgX = 18+192+192+192
			imgY = 90

			winrateX = 128+192+192+192
			winrateY = 99

			pickrateX = 128+192+192+192
			pickrateY = 128

			if not self.bot_image_render:
				for champion in data:
					image_url = data[champion][1]
					image_str = urlopen(image_url).read()
					image_file = io.BytesIO(image_str)
					image = pygame.image.load(image_file).convert(self.win)
					image = pygame.transform.scale(image,(50,50))
					self.bot_image_list.append(image)
					self.bot_winrate_list.append(data[champion][0])
					self.bot_image_render = True
					self.load()
					pygame.display.update()

			for i in self.bot_image_list:
				i.set_alpha(self.data_alpha_value)  
				self.win.blit(i, (imgX,imgY))
				imgY += 50 + 35

			for champion in data:
				#Winrate
				text = self.font.render(data[champion][0], True, (255,255,255))
				alpha_img = pygame.Surface(text.get_size(), pygame.SRCALPHA)
				alpha_img.fill((255, 255, 255, self.data_alpha_value))
				text.blit(alpha_img, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
				textRect = text.get_rect()
				textRect.center = (winrateX, winrateY)
				text.set_alpha(self.data_alpha_value) 

				#Pickrate
				text_pick = self.font_pick.render(data[champion][2], True, (255,255,255))
				alpha_img_pick = pygame.Surface(text_pick.get_size(), pygame.SRCALPHA)
				alpha_img_pick.fill((255, 255, 255, self.data_alpha_value))
				text_pick.blit(alpha_img_pick, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
				textRect_pick = text_pick.get_rect()
				textRect_pick.center = (pickrateX, pickrateY)
				text_pick.set_alpha(self.data_alpha_value) 

				self.win.blit(text, (textRect)) 
				winrateY += 50 + 35

				self.win.blit(text_pick, (textRect_pick)) 
				pickrateY += 50 + 35


		if role == 'sup':

			imgX = 18+192+192+192+192
			imgY = 90

			winrateX = 128+192+192+192+192
			winrateY = 99

			pickrateX = 128+192+192+192+192
			pickrateY = 128


			if not self.sup_image_render:
				for champion in data:
					image_url = data[champion][1]
					image_str = urlopen(image_url).read()
					image_file = io.BytesIO(image_str)
					image = pygame.image.load(image_file).convert(self.win)
					image = pygame.transform.scale(image,(50,50))
					self.sup_image_list.append(image)
					self.sup_winrate_list.append(data[champion][0])
					self.sup_image_render = True
					self.load()
					pygame.display.update()

			for i in self.sup_image_list:
				i.set_alpha(self.data_alpha_value)  
				self.win.blit(i, (imgX,imgY))
				imgY += 50 + 35

			for champion in data:
				#Winrate
				text = self.font.render(data[champion][0], True, (255,255,255))
				alpha_img = pygame.Surface(text.get_size(), pygame.SRCALPHA)
				alpha_img.fill((255, 255, 255, self.data_alpha_value))
				text.blit(alpha_img, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
				textRect = text.get_rect()
				textRect.center = (winrateX, winrateY)
				text.set_alpha(self.data_alpha_value) 

				#Pickrate
				text_pick = self.font_pick.render(data[champion][2], True, (255,255,255))
				alpha_img_pick = pygame.Surface(text_pick.get_size(), pygame.SRCALPHA)
				alpha_img_pick.fill((255, 255, 255, self.data_alpha_value))
				text_pick.blit(alpha_img_pick, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
				textRect_pick = text_pick.get_rect()
				textRect_pick.center = (pickrateX, pickrateY)
				text_pick.set_alpha(self.data_alpha_value)

				self.win.blit(text, (textRect)) 
				winrateY += 50 + 35

				self.win.blit(text_pick, (textRect_pick)) 
				pickrateY += 50 + 35

	def load(self):
		self.current_load += 1

	def info_screen(self):
		infoImg = pygame.image.load(os.path.join(self.resource_path,'info.png'))
		self.win.blit(infoImg, (0,0))
		pygame.display.update()

		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					sys.exit()

				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					running = False
					self.win.blit(self.background, (0,0))
					self.reload = True
					self.data_alpha_value = 0
					self.alpha_value = 0
					self.dontLoadBar = True

