# NerualNetSailer
This repo is dedicated to learning neural networks using a sailing game. The goal is to create an AI that can sail fastest round a simple course. I realise this readme is starting to get a little long and so will be generating a wiki with my thought porcesses. 

## The idea
I have always enjoyed sailing, recently I have had some interest in neural netowrks and how they work. So I though hey why not make a neural network that can play a sailing game? The idea is fairly simple we will first make the game, this might be simple to begin with. It will involve making a simple sailing simulator which has a boat going round a course. There will be wind (constant from one direction) the boat will have a velocity, acceleration (up to a max velocity) and some initial starting direction on a race line. (This might be one of two directions along some line).
The goal is from the intial starting position to race round the course in the fastest time.

Note boats cannot sail upwind directly and so there will be a limited number of directions that the boat can sail. Plus the direction of the boat gives its maximum speed, for instance going at 90-120 degrees to the wind is often the fastest this is called beam reaching in sailing terminlogy. I will have to figure out how the acceleration will work since this will be integral. I am also going to make it so that the boat does not have an inifinte space to sail in so this will probably be a simple regctangular area to begin with with auto tacking/jibing if you hit a wall. 

## Physics
I found a pretty useful graph on the physics of sailing on the IOP website. Will have to try and replicate this in mathematical form. Or possibly a simple interpolation will do. 
No indication on the acceleration though so this will have to be thought about. For instance a great way of gain speed used to be going for a reach before turning upwind especially in light conditions. Might have to fully replicate force to see if the machine learns about pumping. 

https://physicstoday.scitation.org/doi/pdf/10.1063/1.2883908 

Additionally the wikipedia page on sails seems to be pretty well stocked with information.
https://en.wikipedia.org/wiki/Forces_on_sails 

## How will this be made
I intend to write this whole thing in python 3.10. I dont want to make it too complex but it will be interesting to see how the time element of the game plays in reality. 

After some intial research it appears reinforcement learning such as deep Q learning might be exactly what I need to train my AI to play. Of course the game needs to be written first. Will use Keras API as the basis for the machine learning, I suspect my GPU will be getting a work out shortly. 

## Current tasks
* Add main line indicator
* Add boat acceleration
* Add boat momentum
* Add race track
* Add conditions on passing a bouy
* Add in bouy class
* Create headless version





