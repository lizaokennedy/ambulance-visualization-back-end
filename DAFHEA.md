1. Create random population of Nc individuals. Nc = 5*Na. Na = actual population size
2. Evaluate Nc individuals using the expensive eval. Build SVM approximation models using candidate solutions as inputs and the actual fitness as targets forming the training set for off-line training.
3. Select Na best individual out of Nc evaluated individuals to form the initial GA population.
4. Rank the candidate solutions based on their fitness value.
5. Preserve the elite by carrying over the best candidate solution to the next generation.
6. Select parents using suitable selection operator and apply genetic operators namely recombination and mutation to create children (new candidate solutions) for the next generation.
7. The SVM regression models created in Step two are applied to estimate the fitness of the children (new candidate solutions) created in Step six. This involves assignment of most likely or appropriate models to each candidate solution
8.The set of newly created candidate solutions is ranked based on their approximate fitness values.
9. The best performing newly created candidate solution and the elite selected in Step five are carried to the population of the next generation.
10. New candidate solutions or children are created as described in Step six.
11. Repeat Step seven to Step ten until either of the following condition is reached:
 - the predetermined maximum number of generations has been reached;
 - The periodic retraining of the SVM regression models is due.
12.  If the periodic retraining of the SVM regression models is due, this will involve actual evaluation of the candidate solutions in the current population. Based on this training data new regression models are formed. The algorithm then proceeds to execute Step four to Step eleven.









