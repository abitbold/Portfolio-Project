# <img src="https://i.ibb.co/FKVnNkw/Poke-Quantlogo.png" alt="Poke-Quantlogo" border="0" height="50" width="55"> PokeQuant

PokeQuant is a software tool to perform financial analyses of stocks, options, and portfolios of stocks.

---

## Installation
* Install [Anaconda](https://www.anaconda.com/distribution/#download-section) with Python 3.7
* Install the following packages:

  * `pandas_datareader`

  * `wallstreet`

  * `bs4`

  * `urllib`


In your command prompt, to install `package`, type:


>`pip install package`

For example, to install `wallstreet`, enter:

<p align="center">
<img src="https://i.ibb.co/ZGr5p0h/pip-install.png" alt="pip-install" border="0" height="120" width="360">
</p>

&nbsp;

---

## How to Use
1. Download the zip file and extract all the contents to the same folder.
2. Navigate to the folder that contains the PokeQuant files.
3. Launch IDLE.
4. Run the following code.
```python
import os
```
5. Set directory to the location of the PokeQuant folder.
```python
os.chdir(r'Path/To/Folder')
```
6. Run the `mainmenu.py` script with the following code.
```python
exec(open("./mainmenu.py").read())
```

7. Follow the instructions on the console to begin your analyses!

&nbsp;

<p align="center">
<img src="https://i.ibb.co/zRw05PD/mainmenu2.png" alt="mainmenu2" border="0" height="300" width="430">
</p>

&nbsp;

   * The program will look the same in IDLE.


## Tutorial
[YouTube Tutorial](https://www.youtube.com/watch?v=g4JIjngaqfs&feature=youtu.be)

### Note on Options
When using the stock analysis tool to view options data, we recommend viewing options for at most **two** stocks at a time. Compiling the options data for more than this number will consume a large amount of time.


---

#### Contributors
* David Abitbol - [dabitbol@andrew.cmu.edu](dabitbol@andrew.cmu.edu)
* Arjun Alagappan - [aalagapp@andrew.cmu.edu](aalagapp@andrew.cmu.edu)
* Cody Cao - [codyc@andrew.cmu.edu](codyc@andrew.cmu.edu)
* Kurtis Lee - [kurtisl@andrew.cmu.edu](kurtisl@andrew.cmu.edu)
* Lily Li - [yangminl@andrew.cmu.edu](yangminl@andrew.cmu.edu)
* Shanshan Liu - [shansha3@andrew.cmu.edu](shansha3@andrew.cmu.edu)
