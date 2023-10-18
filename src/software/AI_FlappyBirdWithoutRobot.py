#
# (c) Marcello Tania 17/04/21
#
# This work may be reproduced, modified, distributed,
# performed, and displayed for any purpose. Copyright is
# retained and must be preserved. The work is provided
# as is; no warranty is provided, and users accept all
# liability.
#
# This is a program of how the machine learn to play flappy
# bird without connected to the robot.

import time
import pygame, sys, random
import numpy
# scipy.special for the sigmoid function expit()
import scipy.special
import os

# neural network class for the brain of the birds
class Individual():

    # initialise the neural network
    def __init__(self, inputnodes, hiddennodes, outputnodes,fitness):
        # set number of nodes in each input, hidden, output layer
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        self.fitness = fitness


        # link weight matrices, wih and who
        # weights inside the arrays are w_i_j, where link is from node i to node j in the next layer
        # w11 w21
        # w12 w22 etc

        self.wih = numpy.random.normal(0.0, pow(self.hnodes,-0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.onodes,-0.5), (self.onodes, self.hnodes))

        # activation function is the sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)

        pass

      # query the neural network
    def query(self, inputs_list):
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T
        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        return final_outputs

class Block(pygame.sprite.Sprite):
    """
    Block class to take the surface and put a rectangle around it
    and put it on the screen
    """
    def __init__(self,path,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load(path).convert()
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))

class Floor(Block):
    """
    Floor class representing the floor of the game
    """
    VEL = 1
    def __init__(self,path,x_pos,y_pos):
        super().__init__(path,x_pos,y_pos)
        self.x_pos = x_pos
        self.y_pos = y_pos

    def move(self):
        """
        Move floor so it looks like its scrolling
        :param speed: the velocity of the floor
        :return: None
        """
        self.x_pos -= self.VEL

        if self.x_pos <= -576:
            self.x_pos = 576

    def draw(self, screen):
        """
        Draw the floor. This is two imgaes that move together.
        :param screen: the pygame surface or window
        :return: None
        """
        screen.blit(self.image, (self.x_pos,self.y_pos))

class Bird(Block):
    """
    Bird class representing the flappy bird
    """
    GRAVITY = 0.3
    VEL = 9

    def __init__(self,path,x_pos,y_pos):
        """
        Initialize the object
        :param x_pos: starting x pos (int)
        :param y_pos: starting y pos (int)
        :return: None
        """
        super().__init__(path,x_pos,y_pos)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.bird_movement = 0
        self.score = 0
        self.high_score = 0

    def jump(self):
        """
        make the bird jump
        :return: None
        """
        self.bird_movement = 0
        self.bird_movement -= self.VEL



    def move(self):
        """
        Make the bird fall and jump
        :param gravity: gravity velocity
        :return: None
        """
        self.bird_movement += self.GRAVITY


    def check_collision(self, pipes):
        """
        Check the bird if it collides vertically or with the pipes
        :param pipes: list of the pipes
        :return: True = collision detected
        :return: False = no collision
        """
        for pipe in pipes:
            if self.rect.colliderect(pipe):
                return False
        if self.rect.top <= -100 or self.rect.bottom >= 900:
            return False
        return True

    def draw(self, screen):
        """
        Draw the bird
        :param win: the pygame surface or window
        :return: None
        """
        self.rect.y += self.bird_movement
        screen.blit(self.image, (self.rect.x,self.rect.y))


    def pos_y(self):
        """
        Bird postition
        :return: y position of bird
        """
        return self.rect.y

    def pipe_score_check(self, pipes):
        """
        Add score if bird pass through the pipes
        :return: None
        """
        if pipes:
            for pipe in pipes:
                if 95 < pipe.centerx < 105:
                    self.score += 0.5

    def update_score(self):
        """
        Check for new high score
        :return: high score
        """
        if self.score > self.high_score:
            self.high_score = self.score
        return self.high_score

    def score_display(self):
        """
        Display score and highscore
        :return: none
        """
        score_surface = game_font.render(f'Score: {int(self.score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(topleft = (20,50))
        screen.blit(score_surface, score_rect)

        score_surface = game_font.render(f'High score: {int(self.update_score())}',True,(255,255,255))
        score_rect = score_surface.get_rect(topleft = (20,100))
        screen.blit(score_surface, score_rect)


class Pipe():
    """
    Pipe class representing the pipes
    """
    VEL = 5
    GAP = 400
    HEIGHT = [500,600,700]
    X_INIT = 700
    def __init__(self,path):
        """
        Initialize the object
        :return: None
        """
        self.image = pygame.image.load(path).convert()
        self.image = pygame.transform.scale2x(self.image)
        #self.height = self.image.get_height()

    def create_pipe(self):
        """
        Create a list of top and bottom pipes
        :return: tupple of top and bottom pipes
        """
        random_pipe_pos = random.choice(self.HEIGHT)
        bottom_pipe = self.image.get_rect(midtop = (self.X_INIT,random_pipe_pos))
        top_pipe =  self.image.get_rect(midbottom = (self.X_INIT,random_pipe_pos - self.GAP))
        return bottom_pipe,top_pipe

    def move(self, pipes):
        """
        Move all the pipes
        :return: visible pipes list
        """
        for pipe in pipes:
            pipe.centerx -= self.VEL
        visible_pipes = [pipe for pipe in pipes if pipe.right> -50]
        return visible_pipes


    def draw(self, screen, pipes):
        """
        Draw the pipe.
        :param screen: the pygame surface or window
        :return: None
        """
        for pipe in pipes:
            if pipe.bottom >= 1024:
                screen.blit(self.image, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.image,False,True)
                screen.blit(flip_pipe, pipe)

    def pos_x(self, pipes):
        # only take the pipe in front of the bird and shown on the screen
        visible_pipes = [pipe for pipe in pipes if pipe.centerx > 100 and pipe.right < 550]
        # only take the bottom pipe because top and bottom pipes x positions are the same
        bottom_pipes = [pipe for pipe in visible_pipes if pipe.bottom >= 1024]
        for pipe in bottom_pipes:
            x = pipe.centerx
            return x

    def pos_y_bottom(self,pipes):
        # To do: Find the clossest pipe
        visible_pipes = [pipe for pipe in pipes if pipe.centerx > 100 and pipe.right < 550]
        # only take the bottom pipe because top and bottom pipes x positions are the same
        bottom_pipes = [pipe for pipe in visible_pipes if pipe.bottom >= 1024]
        for pipe in bottom_pipes:
            y = pipe.top
            return y

    def pos_y_top(self,pipes):
        # To do: Find the clossest pipe
        visible_pipes = [pipe for pipe in pipes if pipe.centerx > 100 and pipe.right < 550]
        # only take the bottom pipe because top and bottom pipes x positions are the same
        bottom_pipes = [pipe for pipe in visible_pipes if pipe.bottom >= 1024]
        for pipe in bottom_pipes:
            y = pipe.top + self.GAP
            return y

def end_game():
    ser.write(b'L')
    print('Generation\tBest fitness')
    print('------------------------------------')

    for i in range(1,gen+1):
        print('{}\t{}'.format(i,best_fitness[i]))

    print('The best so far is {}:'.format(round(best_so_far.fitness,5)))
    print('The best so far who {}:'.format(best_so_far.who))
    print('The best so far wih {}:'.format(best_so_far.wih))

    pygame.quit()
    sys.exit()


# General Setup
pygame.init()
clock = pygame.time.Clock()
script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(script_dir, '../../res/asset/font/04B_19.TTF')
if os.path.isfile(font_path):
    game_font = pygame.font.Font(font_path,40)
else:
    print(f"ERROR: The file {font_path} does not exist.")

asset_img_path = os.path.join(script_dir, '../../res/asset/media/img/')

# Main Window
screen = pygame.display.set_mode((576,1024))
bg_surface = pygame.image.load(asset_img_path + 'background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

# Game Objects
floor_surface1 = Floor(asset_img_path + 'base.png',0,900)
floor_surface2 = Floor(asset_img_path + 'base.png',576,900)
bird_surface = Bird(asset_img_path + 'bluebird-midflap.png',100,512)
pipe_surface = Pipe(asset_img_path + 'pipe-green.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1400)

# Global Variable
game_active = True


# number of input, hidden and output nodes
input_nodes = 5
hidden_nodes = 10
output_nodes = 1


POP_SIZE = 10 # defining population size
NUM_GEN = 50

X_BIAS = 0.8
MUT_RATE = 0.3
STEP_SIZE = 0.2

person = [None] * POP_SIZE
offspring = [None] * POP_SIZE

best_fitness = [None] * (NUM_GEN+1)

flag_dead = False
indiv = 0
gen = 1

# initialize best so far
best_so_far = Individual(input_nodes,hidden_nodes,output_nodes,0)


# Create first population
print('Geration : 0, HELLO WORLD!')
print('Indiv\twho\tFitness')
print('------------------------------------------------')

for i in range(POP_SIZE):
    person[i] = Individual(input_nodes,hidden_nodes,output_nodes,0)
    offspring[i] = person[i]
    print('{}\t{}\t{}'.format(i,
                              person[i].who,
                              'UNKNOWN'))




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_surface.jump()
                actuator_status = 1
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                bird_surface.rect.center = (100,512)
                bird_surface.bird_movement = 0
                pipe_list.clear()
                bird_surface.score = 0

                for x in range(1000):
                    ser.write(b'L')

                flag_dead = False
        elif game_active:
            actuator_status = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(pipe_surface.create_pipe())

    # Background
    screen.blit(bg_surface, (0,0))

    if game_active:

        # Bird
        bird_surface.draw(screen)
        bird_surface.move()

        game_active = bird_surface.check_collision(pipe_list)

        # Pipe
        pipe_list = pipe_surface.move(pipe_list)
        pipe_surface.draw(screen,pipe_list)

        bird_surface.pipe_score_check(pipe_list)
        bird_surface.score_display()

        # Data input
        bird_y = bird_surface.pos_y()
        pipes_x = pipe_surface.pos_x(pipe_list)
        pipe_y_bottom = pipe_surface.pos_y_bottom(pipe_list)
        pipe_y_top = pipe_surface.pos_y_top(pipe_list)

        person[indiv].fitness += 0.01


        # Keep it neutral when the pipes has not shown on the screen
        if pipes_x == None:
            pipes_x = 500
            pipe_y_bottom = 600
            pipe_y_top = 900


        data_inputs = numpy.array([bird_y, pipes_x, pipe_y_bottom, pipe_y_top, actuator_status])
        # Bird think using the Artificial Neural Network
        data_output = person[indiv].query(data_inputs)



        if data_output >= 0.5:
            bird_surface.jump()



        # Show Bird ID on screen
        indiv_surface = game_font.render(f'Bird ID: {indiv}',True,(255,255,255))
        screen.blit(indiv_surface, (20,10))

        # Show generation on screen
        gen_surface = game_font.render(f'Generation: {gen}',True,(255,255,255))
        screen.blit(gen_surface, (20,150))



    else:
        # Print the performance after the player is death
        if flag_dead == False:
            flag_dead = True


            if indiv < POP_SIZE-1:
                game_active = True
                bird_surface.rect.center = (100,512)
                bird_surface.bird_movement = 0
                pipe_list.clear()
                bird_surface.score = 0
                #person[indiv].fitness = 0

                flag_dead = False
                indiv += 1


            else:


                # select parents and generating offspring phenotype
                for indiv in range(POP_SIZE):

                    #Mom
                    i1 = random.randrange(POP_SIZE) # choose parent
                    i2 = random.randrange(POP_SIZE) # choose parent
                    i3 = random.randrange(POP_SIZE) # choose parent

                    #Tournament
                    if person[i1].fitness >= person[i2].fitness:
                        mom = i1
                    else:
                        mom = i2
                    if person[i3].fitness >= person[mom].fitness:
                        mom = i3

                    #Dad
                    i1 = random.randrange(POP_SIZE) # choose parent
                    i2 = random.randrange(POP_SIZE) # choose parent
                    i3 = random.randrange(POP_SIZE) # choose parent

                    #Tournament
                    if person[i1].fitness >= person[i2].fitness:
                        dad = i1
                    else:
                        dad = i2
                    if person[i3].fitness >= person[dad].fitness:
                        dad = i3

                    #Crossover

                    # Crossover for who
                    for i in range(hidden_nodes):
                        if random.random()< X_BIAS:
                            offspring[indiv].who[0,i] = person[mom].who[0][i]
                        else:
                            offspring[indiv].who[0,i] = person[dad].who[0][i]

                    # Crossover for wih
                    for i in range(input_nodes):
                        for ii in range(hidden_nodes):
                            if random.random()< X_BIAS:
                                offspring[indiv].wih[ii,i] = person[mom].wih[ii][i]
                            else:
                                offspring[indiv].wih[ii,i] = person[dad].wih[ii][i]

                    #Mutation

                    # Mutation for who
                    for i in range(hidden_nodes):
                        if random.random()< MUT_RATE:
                            r = (random.randint(0, 1))%2 *2-1 # create a number either -1 or 1 (sign)
                            offspring[indiv].who[0,i] += r*STEP_SIZE

                    # Mutation for wih
                    for i in range(input_nodes):
                        for ii in range(hidden_nodes):
                            if random.random()< MUT_RATE:
                                r = (random.randint(0, 1))%2 *2-1 # create a number either -1 or 1 (sign)
                                offspring[indiv].wih[ii,i] += r*STEP_SIZE

                # update statistical analysis
                best_fitness[gen] = person[0].fitness

                print('Generation : {}'.format(gen))
                print('Indiv\twho\tFitness')
                print('------------------------------------------------')
                for i in range(POP_SIZE):
                    print('{}\t{}\t{}'.format(i,
                                              person[i].who,
                                              round(person[i].fitness,5)))
                    #update statistical analysis
                    if person[i].fitness >= best_fitness[gen]:
                        best_indiv = i
                        best_fitness[gen] = person[i].fitness



                if best_fitness[gen] > best_so_far.fitness:
                    best_so_far.who = person[best_indiv].who.copy()
                    best_so_far.wih = person[best_indiv].wih.copy()
                    best_so_far.fitness = person[best_indiv].fitness


                print('The best fitness is {}'.format(round(best_fitness[gen],5)))
                print('The best so far is {}:'.format(round(best_so_far.fitness,5)))


                print('Offspring :')
                print('Indiv\twho\tFitness')
                print('------------------------------------------------')
                for i in range(POP_SIZE):
                    print('{}\t{}\t{}'.format(i,
                                              person[i].who,
                                              'UNKNOWN'))

                # Restart for having a new generation
                if gen < NUM_GEN:
                    gen += 1
                    game_active = True
                    bird_surface.rect.center = (100,512)
                    bird_surface.bird_movement = 0
                    pipe_list.clear()
                    bird_surface.score = 0
                    indiv = 0 # restart for having a new generation
                    flag_dead = False

                    # Next generation parents are replaced by the offspring
                    for i in range(POP_SIZE):
                        person[i] = offspring[i]
                        #restart fitness
                        person[i].fitness = 0
                        #TO DO with best so far


                else :
                    end_game()



    # Floors
    floor_surface1.draw(screen)
    floor_surface2.draw(screen)
    floor_surface1.move()
    floor_surface2.move()

    pygame.display.update()
    clock.tick(120)
