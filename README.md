# Process boards
Image processing for boards in production

## Digital image processing
This repository contains an example of digital image processing for electronic boards in production process.
The idea behind is avoid to produces boards that missing components.
The code was written in `Python`, using `Linux` (Ubuntu) environment

## Dependencies
- Python OpenCV
- Tesseract OCR
- NumPy
- MatPlotLib

## Runing

```
$ python main.py

Process initialized
..........
Checking templates...
..........
------------------------------------------------------------
Results:
images/boards/board01.jpg ..... OK
images/boards/board02.jpg ..... OK
images/boards/board03.jpg ..... OK
images/boards/board04.jpg ..... OK
images/boards/board05.jpg ..... OK
images/boards/board06.jpg ..... not OK:  missing square
images/boards/board07.jpg ..... not OK:  missing rectangle
images/boards/board08.jpg ..... not OK:  position error
images/boards/board09.jpg ..... not OK:  missing rectangle
images/boards/board10.jpg ..... not OK:  missing rectangle
------------------------------------------------------------
```