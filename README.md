
# Wave Function Collapse (WFC)

WFC is a algorithm that is used in generative art and various other fields to create complex, randomized patterns or structures while adhering to certain constraints or patterns defined by the user

This script is a simple implementation of WFC that samples a given user image and extracts all possible NxN sized portions(kernels) of the image and also takes the flipped and rotated versions of it and then generates a much larger image from these kernels keeping the constraint that adjacent kernels must be superimposable


## Installation

For this project you need python 3.11.2 or later <br/>
For installing the dependencies run the given command

```bash
python -m pip install -r requirements.txt
```
    
## Usage
Here is a example of how to run this script
```bash
python main.py "./samples/MagicOffice.png" 3 800 800 20
```
<img width="641" alt="WFC" src="https://github.com/Bhuvansh-Goyal-IITB/Wave-Function-Collapse/assets/128956146/4a59b702-c36d-478d-b47c-7dacb6d04c41">

## Example
<div align="center">
  <img src="https://github.com/Bhuvansh-Goyal-IITB/Wave-Function-Collapse/assets/128956146/e8be760d-7af3-4279-a691-e95baa4df94a" alt="GIF"/>
</div>

## License

[MIT](https://choosealicense.com/licenses/mit/)
