
# Wave Function Collapse (WFC)

WFC is a algorithm that is used in generative art and various other fields to create complex, randomized patterns or structures while adhering to certain constraints or patterns defined by the user

This script is a simple implementation of WFC that samples a given user image and extracts all possible NxN sized portions(kernels) of the image and also takes the flipped and rotated versions of it and then generates a much larger image from these kernels keeping the constraint that adjacent kernels must be superimposable


## Installation

For this project you need python 3.11.2 or later 

```bash
pip install -r requirements.txt
```
    
## Usage
Here is a example of how to run this script
```bash
python main.py "./samples/MagicOffice.png" 3 80 80 800 800 10
```
<img width="831" alt="WFC" src="https://github.com/Bhuvansh-Goyal-IITB/Wave-Function-Collapse/assets/128956146/5b324212-4729-4228-b4e0-46a2a0838c5c">
