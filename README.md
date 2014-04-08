structure-learning
==================

##Solving software dependency

Please do:

`> pip install -r requirements.txt`

##Chow&Liu tree algorithm

To run the chow-liu tree algorithm, please run the file `chow_liu_tree.py`

Usage:

`> python chow_liu_tree.py [predict|sorted_edges|graphviz]`

Argument: 

1. predict: print the prediction of the joint probabilities of test set
2. sorted_edge: print the edges by order of their mutual information gain
3. graphviz: print the graphviz format file of the learned tree structure


##GPT (Generating poly-tree) algorithm

To run the GPT algorithm, please run the file `gpt.py`

Usage:

`> python gpt.py [orig|mod] [predict|sorted_edges|graphviz]`

Argument: 
1. [orig|mod]: original or modified version of GPT
2. [predict|sorted_edges|graphviz]: same as above

