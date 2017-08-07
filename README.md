# ImageCompression
Program demonstrating the use of quadtrees in the field of image manipulation.
The program will generate a quadtree for the given image, then ask which level of compression is required.  
Maximum compression = 0, minimum compression = x, where 2^x = size of image dimension in pixels.  
Currently, the program only works for images whose dimensions are perfect powers of 2.

Program can be tested using the following command:
```
python ImageComp.py
```

Program will then ask for the level of compression required.
When level is inputted, the program will then generate the image.
