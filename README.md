# NerualNetSailer
This repo is dedicated to learning neural networks using a sailing game. The goal is to create an AI that can sail fastest round a simple course. 

## The idea
I have always enjoyed sailing, recently I have had some interest in neural netowrks and how they work. So I though hey why not make a neural network that can play a sailing game? The idea is fairly simple we will first make the game, this might be simple to begin with. It will involve making a simple sailing simulator which has a boat going round a course. There will be wind (constant from one direction) the boat will have a velocity, acceleration (up to a max velocity) and some initial starting direction on a race line. (This might be one of two directions along some line).
The goal is from the intial starting position to race round the course in the fastest time.

Note boats cannot sail upwind directly and so there will be a limited number of directions that the boat can sail. Plus the direction of the boat gives its maximum speed, for instance going at 90-120 degrees to the wind is often the fastest this is called reaching in sailing terminlogy. I will have to figure out how the acceleration will work since this will be integral. I am also going to make it so that the boat does not have an inifinte space to sail in so this will probably be a simple regctangular area to begin with with auto tacking/jibing if you hit a wall. 

## How will this be made
I intend to write this whole thing in python 3.10. I dont want to make it too complex but it will be interesting to see how the time element of the game plays in reality. 

## Some intial questions
Neural networks for image analysis seem pretty clear cut in their function. But how do neuralk networks deal with time based data or instantaneous decisions? Do we intend to just give it a set of time series to learn from. Or do we make it a decision based approach, based on the previous decisions made. 





