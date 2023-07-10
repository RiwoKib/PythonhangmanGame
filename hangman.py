import pygame
import random
import math
import random

pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("The Hangman Game")

#game variables
hangman_status = 0
words = ["HELLO","JAVA","DEVELOP","CODE","JAVASCRIPT","GAME","HANGMAN"]
word = random.choice(words)
guessed = []

#button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS*2+GAP)*13)/2)
starty = 400
A = 65

for i in range(26):
	x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
	y = starty + ((i // 13) * (GAP + RADIUS * 2))
	letters.append([x,y, chr(A + i), True])

#fonts 
letter_font = pygame.font.SysFont('comicsans', 40)
word_font = pygame.font.SysFont('comicsans', 60)
title_font = pygame.font.SysFont('comicsans', 70)
play_font = pygame.font.SysFont('comicsans',40)
text_font = pygame.font.Font('freesansbold.ttf',18)

#load images
images = []
for i in range(7):
	image = pygame.image.load("hangman/"+str(i)+".png")
	images.append(image)

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)

def draw():
	win.fill(WHITE)

	#draw title
	text = title_font.render("HANGMAN GAME", 1, BLACK)
	win.blit(text,(WIDTH/2-text.get_width()/2, 20))

	#draw word
	display_word = ""
	for letter in word:
		if letter in guessed:
			display_word += letter + " "
		else:
			display_word += "_ "	

	text = word_font.render(display_word, 1, BLACK)
	win.blit(text,(400,200))		


	#draw buttons
	for letter in letters:
		x, y, ltr, visible = letter
		if visible:
			pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
			text = letter_font.render(ltr, 1, BLACK) 
			win.blit(text,(x-text.get_width()/2,y-text.get_height()/2))

	win.blit(images[hangman_status], (150,100))
	pygame.display.update()

def text_objects(text,color,size="small"):
	if size == "small":
		textsurface = text_font.render(text,True,color)	

	return textsurface,textsurface.get_rect()	

def text_to_button(text,color,btnx,btny,btnw,btnh,size="small"):
	textsurface, textrect = text_objects(text,color,size)	
	textrect.center = (btnx+(btnw/2),btny+(btnh/2))
	win.blit(textsurface,textrect)

def draw_1():
	#begin with a question
	text = play_font.render("Would you like to play Again?",1,BLACK)
	win.blit(text,(100,200))
	pygame.draw.rect(win,(0,200,0),(200,250,100,50))
	text_to_button("Yes",WHITE,200,250,100,50)
	pygame.draw.rect(win,(200,0,0),(350,250,100,50))
	text_to_button("No",WHITE,350,250,100,50)

	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	
	if 350+100 > mouse[0] > 350 and 250+50 > mouse[1] > 250:
		pygame.draw.rect(win,(100,0,0),(350,250,100,50))
		text_to_button("No",WHITE,350,250,100,50)
		if click[0] == 1:
			print(clicked)
	else:
		pygame.draw.rect(win,(200,0,0),(350,250,100,50))
		text_to_button("No",WHITE,350,250,100,50)

	pygame.display.update()

def display_message(message):
	win.fill(WHITE)
	text = word_font.render(message, 1, BLACK)
	win.blit(text,(WIDTH/2-text.get_width()/2,50))
	pygame.display.update()

def game_loop():
	global hangman_status
	#setup game loop
	FPS = 60
	clock = pygame.time.Clock()
	run = True 

	while run:
		#game runs on 60 frames/sec
		clock.tick(FPS)

		draw()	

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				m_x,m_y = pygame.mouse.get_pos()
				for letter in letters:
					x, y, ltr, visible = letter
					if visible:
						dist = math.sqrt((x-m_x)**2 + (y-m_y)**2)
						if dist < RADIUS:
							letter[3] = False
							guessed.append(ltr)
							if ltr not in word:
								hangman_status += 1					

		won = True
		for letter in word:
			if letter not in guessed:
				won = False
				break

		if won:
			display_message("YOU WON!")
			

		if hangman_status == 6:
			display_message("YOU LOST!!")


play = True
while play:
	game_loop()

pygame.quit()			

