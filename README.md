# Machine-Playing-Flappy-Bird
## How to build a machine that learns how to play a flappy bird?


https://user-images.githubusercontent.com/27281789/115113624-8379cc00-9f8b-11eb-983b-fdb106af57a8.mp4

Congratulations AI! You play yourself.


### Abstract
The line of codes were inspired by nature. It was the combination between neurons, how our brain works, and the Darwinian theory of evolution. Those combinations between the Artificial Neural Network and Genetic Algorithm compose unsupervised machine learning. The servo motor is to show how the mechanical machine learn to interact with another machine as the environment.


### Game Parameters

*  **Bird ID** is the identification of an agent.
*  **Score** is the score of the current agent playing.
*  **High score** is the highest score for all the agents whom who has played the game.
*  **Generation** is the current generation of all the agents being runned.


### Hardwares

*  Arduino Nano
*  SG90 Micro Servo
*  M2 screws and nuts
*  2x 3D printed parts
*  Wires

### Artificial Neural Network
Let us call the robot  an agent, each individual agent has its own brain of an artificial network of 4 inputs and 7 hidden nodes, and 1 output.

```python
self.wih = numpy.random.normal(0.0, pow(self.hnodes,-0.5), (self.hnodes, self.inodes))
self.who = numpy.random.normal(0.0, pow(self.onodes,-0.5), (self.onodes, self.hnodes)) 
```

Then, the forward propagation is to calculate the output result by using the weights of each node of the Artificial Neural Network. We could just simple calculate this using matrix.

```python
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
```

### Evolutionary Algorithm
The evolutionary algorithm or genetic algorithm helps to select the better agents who are more likely survive by using the techniques as following: survival of the fittest, reproduction, and mutation.


1. Create the first population
```python
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
```
2. Run all the individual agents and calculate the fitness (How far the agent can survive). In this case, we just have one agent as one machine to be evaluated at the same time.
3. Survival of the fittest describes that those birds tend to live longer and reproduce, create a new generation with the evolved genes ( the Artificial Neural Network).

```python
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
```
4. Reproduction to create a new generation of offspring.

```python
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

```
5.  Mutation to evolve.

```python
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
```
6. All parents are replaced by the offsprings.


## Pre-Trained Model
After hours of training and calibration, this is the result that you might get.Otherwise if you would like to save time, you could use this following weights.

Pre-trained Artificial Neural Network weights:
```python
self.wih = numpy.array([[-3.29829867,  0.76441159,  2.40556884, -0.27947868],
                        [ 0.3240327,   2.25160679, -1.84486032, -1.9700158 ],
                        [-2.62540542,  2.33445864, -0.46812661, -2.3635345 ],
                        [-0.90241636,  1.99882317, -2.67465566, -1.29619994],
                        [-0.15231266,  2.49082877,  1.08143091,  0.58047555],
                        [ 0.62497593,  1.42985698, -3.91579115, -0.20542114],
                        [ 2.7336978 ,  2.26497664,  1.86146316, -0.69662931]])

self.who = numpy.array([[-4.23668794, -1.10929065,  0.05054322,  0.41018827,  2.70858315, -0.42650511, -1.21117085]])
```

(c)2021
By [Marcello Tania](https://marcellotania.com/)

Special thanks to Yohanes Tjandrawidjaja for the math expert and suggestions.
