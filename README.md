# Team-Vulture

## Overview
This car was made for a Highschool AP Computer Science Class.
We were the only group to get this far. 

This project was planned to be used with Tensorflow in python3. After months of having truble importing images, and only a few days left before the semester ended, we moved ot Keras. It still uses tensorflow, but simplifies it.


## Raspberry Pi (car)

### Training Images Save Filepath

Filepath to save images while training: /home/<username>/Documents/**forward**, **turnLeft**, **turnRight**, **stop**, **other**
  
1. All of the **bold** letters must be folders created in the filesystem
2. The user should be "jax" or "pi"
3. A spot where things could go wrong: This uses the username "jax" (in the filename) if it cannot find the raspberry pi camera package. If it does find it, it uses "pi" as the username.
4. There is the ability to add a "prefix". That changes the filename slightly so that it does not overwrite previous files.

  
