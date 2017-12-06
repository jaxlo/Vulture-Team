# Team-Vulture
## H2 Training Images Save Filepath
Filepath to save images while training: /home/<username>/Documents/**forward**, **turnLeft**, **turnRight**, **stop**, **other**
  
1. All of the **bold** letters must be folders in the filesystem
2. The user should be "jax" or "pi"
3. There is the ability to add a "prefix". That changes the filename slightly so that it does not overwrite previous files.
4. A spot where things could go wrong: This uses the username "jax" (in the filename) if it cannot find the raspberry pi camera package. If it does find it, it uses "pi" as the username.

  
