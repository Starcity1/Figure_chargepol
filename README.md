#Python HLMA Figure Generator.

**Requirements**: Python 3.8+, chargepol, anaconda.

**Author**: David Rodriguez Sanchez (david.rodriguez24@tamu.edu).

**Version**: 0.0.1

**Description**: Using the modified chargepol version, the program can generate a multiple number of figures. *Note*: This version does still contain major bugs and errors. If you find any errors please contact David Rodriguez Sanchez.

Usage ::
```
python Create_Figures.py <path_to_chargepol_csv>
```

Before running, please make sure to have Anaconda **installed**. The script has to run in an **Anaconda environment**. Here is a link on how to install Anaconda and how to setup an environment.
Installing Anaconda: https://www.anaconda.com/products/distribution
Setting up an Anaconda environment: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

At the bottom of ```Create_Figures.py``` there is a params variable. Here you can modify the title and date of the figure. Apart from that,you do not need to perform any other modificaiton to the program. An example of such parameters may be.


```
params = {
        "Title": "Lightning Data",
        "Date": "November 11, 2022"
}
```

Contact the author if you would like to change another variable/aspect of the figures (e.g. the x and y labels).

The code is able to generate **4** unique figures:

1. A density graph
2. A vertical histogram
3. A scatter plot
4. An event layer across the Houston area.

As for now, the code can also create **3** figures which are a combination of our unique plots. Note that there is an 8th option which is not implemented yet.
