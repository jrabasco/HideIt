# HideIt

Hide your texts in images !

## Requirements

* Python 3
* Pillow
* NumPy

## Usage

* Hide examples/txt in examples/original.jpg and stores it in output.png

```python hide.py examples/original.jpg examples/txt output.png```

* Extracts the text hidden in output.png and stores it in res

```python discover.py output.png res```

## Note

Some image formats do not work well (for compression reasons), this script works well if the output is stored as a *.png, *.bmp or *.ppm (those have been tested). The *.jpg format seems not to work.

