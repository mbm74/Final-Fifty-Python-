# HALPIN-TSAI MICROMECHANICS
### VIDEO DEMO: [HALPIN-TSAI MICROMECHANICS](https://youtu.be/jAjZDPWGSHc)
<br/>

### DESCRIPTIONS:

In this final project of CS50P, we present a python code that employs Halpin-Tsai micromechanics method that can predict the effective elastic stiffness properties of a unidirectional advanced fiber reinforced matrix composite material or simply, UD composite based on user inputs on its individual constituent's elastic moduli while varying the volumetric content of the constituents that constitute the composite. At the same time, to code allows us to do quick and simple micromechanics and comparison analysis as well.

The UD composite which exhibits transversely isotropic behaviors is schematically shown below.


                                 _____________________________
             3                  /----------------------------/|
             |                 /----------------------------/o|
             |___1            /----------------------------/oo/
            /                /----------------------------/oo/
           2                /____________________________/oo/
                           |                             |o/
                           |_____________________________|/

                                a) 3D composite ply

            ---------------------------
            |-------------------------|
    2       |-------------------------|         ------------------------    3
    |       |-------------------------|         |o o o o o o o o o o o |    |
    |____1  |-------------------------|         | o o o o o o o o o o o|    |_____2
            |-------------------------|         |o o o o o o o o o o o |
            |-------------------------|         ------------------------
            ---------------------------

               b) in-plane top view       c) out-of-plane side view (transverse symmetry)

            Figure 1: Unidirectional advanced fiber reinforced matrix composite ply


### INTRODUCTION - The Motivation
UD composite is a material that has all its reinforcing fibers aligned in one single direction embedded in a continuous resin matrix material to produce a strong and stiff, thin-lightweight structure.

The schematic figure shown above seems to suggest that UD composite is a thick structure but the exaggeration is due to the need to show the long continuous circle fibers within the matrix material in its transverse isotropic plane. In reality, it is an extremely thin ply structure.

Generally, the mechanical effective properties of such material in the most basic case, depend on its constituent properties, i.e. the mechanical properties of fiber and matrix material and also the volumetric content of fibers in the composite. Thus, to design structures made from this type of material, the selection of fibers and matrix as well as its fiber to matrix ratio in a composite become critical parameters.

Often, these parameters of effective properties are determined from experiments and the results are highly influenced by the manufacturing methods and processes that produced the composite.

Nevertheless, during material selection process, blindly conducting experiments for all possible pre-selected constituent materials over a wide range of possible fiber volume fraction value in a composite is not really a viable or practical solution because experiments are time-consuming and costly activities, which are full with daunting and meticiulous tasks.

Hence, micromechanics analysis is normally conducted first as a tool for preliminary investigation to identify potential candidates, i.e. combination of constituent materials with best practical fiber volume fractions that produce the desired effective elastic properties of UD composite material before more or detail experimental works or even, further numerical analyses can be performed.

Here, we have python code that will help the investigators to narrow down the selection of fiber and matrix materials as well as identifying practical and optimized range of fiber volume fraction. Thus, it contains tools for fast numerical computations for micromechanics and comparison analyses as well as other tools that can assist them in record keeping, plotting trends and data reporting purposes 😁.

Note that this micromechanics code at the moment, is only focusing on the average elastic performances of UD fiber reinforced matrix composite material.

### CONTENTS

- [FEATURES](#features)
- [COMPARISON](#comparison)
- [INSTALLATION](#installation)
- [DOCUMENTATION](#documentation)
- [USAGE AND TUTORIALS](#usage-and-tutorials)
- [DISCLOSURE](#disclosure)
- [ACKNOWLEDGEMENT](#acknowledgement)

### FEATURES

#### Halpin-Tsai Formulation
This python code uses [Halpin-Tsai method](https://github.com/mbm74/Halpin-Tsai-Micromechanics/blob/61893bd6a6e286e6ac013a30f98a9ad328c726e5/Halpin_Tsai_A_Review.pdf) for its composite micromechanics analysis where it allows us to predict the minimum five effective elastic constants of transversely isotropic UD composite material. Furthermore, from transverse-isotropic relations, additional effective elastic constants can also be found.

With this code, six (6) homogenized effective elastic moduli of UD composite can be estimated and these are:
1. Effective axial Young's modulus - E1eff / E1*
2. Effective transverse Young's modulus - E2eff / E2*
3. Effective axial shear modulus - G12eff / G12*
4. Effective transverse shear modulus - G23eff / G23*
5. Effective major Poisson's ratio - v12eff / v12*
6. Effectuve plane-strain bulk modulus - K23eff / K23*

Note: Except for Poisson's ratio which has no unit, all effective properties have units in terms of Giga Pascal (GPa).

It is worth noted that the simplicity in the Halpin-Tsai formulations allows for faster, yet accurate numerical computations and therefore, is suitable for preliminary investigation.

#### Accurate Estimation

The code utilizes 'decimal' standard python module to take the advantage of Decimal datatype's capability where it offers more correctly rounded decimal floating point arithmetic computations when compared to float datatype arithmetic operations.

#### Simple, Versatile & Prompt Analysis

Using this micromechanics code, creating fiber and matrix constituent material from isotropic and transversely isotropic material is easy as A, B, C. In fact, the code offers various approaches to instantiate these constituent materials, e.g. with direct use of Constructor call, through user-interactive interaction and from csv data inputs.

With constituent materials at hands, creating transversely isotropic UD composite material is even more simpler, e.g. with a short, single line statement such as the following:

    ud_composite = HT(fiber, matrix)

and voila! we have our first UD composite material with its six (6) effective elastic properties estimated by Halpin-Tsai micromechanics method.

Once we have our composite, various quick and prompt micromechanics analysis and actions on the results of micromechanics analysis can be performed using several tools or specifically, functions offered by this code.

For example, the overall performances of a UD composite with all its effective elastic properties versus full range of fiber volume fraction from 0 to 1 can be displayed in stylish table format onto the console screen. In fact, the constituent's  elastic moduli will be displayed as well. Furthermore, the analysis can be customized to focus on specific range or specific values of effective elastic moduli by defining the custom range or value of fiber volume fraction.

The code also offers comparison analysis where specific effective elastic constant of two and not more than five UD composites can be compared together side by side. Based on user preferences, the comparison can be done over the whole range of fiber volume fraction or at specific custom range or value of fiber volume fraction.

For effective and meaningful comparison, we can choose baseline material where its specific effective elastic modulus can be used as a reference and the code will give us the percentage difference when the effective elastic modulus of other UD composite is compared to this reference value.

Additionally, for better understanding on the results of micromechanics analysis on a single UD composite, plots of estimated effective elastic moduli versus full range of fiber volume fraction can be generated. In fact, this plotting capability is also available for comparison analysis that involves multiple UD composite materials.

All plots are saved as png format files with unique, distinguishable filenames in a folder that has default name or custom name defined by the user.

If the micromechanics or comparison analysis is worth for further investigation in other applications, their data can easily be saved as csv format files.

Last but not least, the code offers the capability to document the micromechanics or comparison analysis where clean, minimalist style pdf report can be generated and saved accordingly.

Thus, when it comes to micromechanics analysis on a single UD composite material, or micromechanics comparison analysis on several UD composite materials, we intend to make our user's life easier, happier and healthier 😁.

To sum up, the code:
- ensures simple rapid test on micromechanics analysis<sup>*</sup>,
- guarantees accurate numerical computations<sup>**</sup>,
- provides visually-pleasing in-situ analysis,
- generates well-formated data in csv files
- generates clean png format graphs for trend analysis,
- generates minimalistic style pdf report on test's data and comparison results,
- organizes output files with consistent, easy-recognized filename and folder, and
- last but not least, is a super user-friendly program!<sup>***</sup>

<br/>
<sup>* Due to simple formulations provided by Halpin-Tsai micromechanics method.</sup>

<sup>** Due to the precision advantages of 'Decimal' type over 'float' datatype.</sup>
<br/><sup>*** 😉😛.</sup>

<sup> # GO BACK TO [CONTENTS](#contents) </sup>

### COMPARISON

Err, sorry. To the best of our searching capability in the GitHub repository, this is the only Halpin-Tsai micromechanics code found so far.

<sup> # GO BACK TO [CONTENTS](#contents) </sup>

### INSTALLATION

To run **project.py** in the *vscode cs50 codespaces*, the exact requirements of modules and packages can be found in `requirements.txt` file for pip-install, e.g.

    pip install -r requirements.txt

<sup> # GO BACK TO [CONTENTS](#contents) </sup>

### DOCUMENTATION

1. [ISOTROPIC MATERIAL](#isotropic-material)
2. [TRANSVERSELY ISOTROPIC MATERIAL](#transversely-isotropic-material)
3. [UNIDIRECTIONAL COMPOSITE MATERIAL](#unidirectional-composite-material)
4. [MICROMECHANICS ANALYSIS](#micromechanics-analysis)
5. [MICROMECHANICS COMPARISON ANALYSIS](#micromechanics-comparison-analysis)

<br>

<sup> # GO BACK TO [CONTENTS](#contents) </sup>

#### ISOTROPIC MATERIAL

Isotropic material is represented by ```Isotropic``` object such as the following:

    ```Isotropic``` object with five (5) attributes:
    - `name`                 : Name of isotropic material
    - `youngs_modulus`       : Young's modulus value, E (GPa)
    - `poissons_ratio`       : Poisson's ratio value, v
    - `shear_modulus`        : Shear modulus value, G (GPa)
    - `pstrain_bulk_modulus` : Plane-strain bulk modulus value, K (GPa)

#### Constructor

**`Isotropic( name , youngs_modulus , poissons_ratio )`**

*Description*

    Instantiate ```Isotropic``` object that represents isotropic constituent material.

*Parameters*

name

    Name of isotropic material.
    Only alphanumerical, underscore '_' and dashed '-' characters are allowed.

youngs_modulus

    Young's modulus of isotropic material.
    Only digits with no or single dot allowed representing positive values.
    To initialize, can be `int`, `float`, `str` and `Decimal` type number. Once initialized, it assumes `Decimal` type value.

poissons_ratio

    Poisson's ratio of isotropic material.
    Only digits with no or single dot allowed representing positive value between 0 and 0.5 inclusive, i.e. 0 < Poisson's ratio <= 0.5.
    To initialize, the number can be `int`, `float`, `str` and `Decimal` type value. Once initialized, it assumes `Decimal` type value.

#### Class Method

**`Isotropic.get()`**

*Description*

    Instantiate ```Isotropic``` object that represents isotropic constituent material through user interaction.
    Return constructor call.


**`Isotropic.read( csv_filename )`**

*Description*

    Instantiate ```Isotropic``` object that represents isotropic constituent material using data read from csv file.
    Return list of ```Isotropic``` objects.

*Parameter*

csv_filename

    The name of csv file where data on isotropic material that includes name, Young's modulus and Poisson's ratio.

#### Instance Method

**`__str__( isotropic_object )`**

*Description*

    Return string representation of current ```Isotropic``` object where all its instance attributes and their values are shown.

*Parameter*

isotropic_object

    Instantiated ```Isotropic``` object

<br>

<sup> # GO BACK TO [DOCUMENTATION](#documentation) </sup>

#### TRANSVERSELY ISOTROPIC MATERIAL

Transversely isotropic material is represented as ```Transtropic``` object such as the following:

    ```Transtropic``` object with seven (7) attributes:
    - `name`                      : Name of transversely isotropic material
    - `axial_youngs_modulus`      : Axial Young's modulus value, E1 (GPa)
    - `transverse_youngs_modulus` : Transverse Young's modulus value, E2 (GPa)
    - `axial_shear_modulus`       : Axial shear modulus value, G12 (GPa)
    - `transverse_shear_modulus`  : Transverse shear modulus value, G23 (GPa)
    - `major_poissons_ratio`      : major Poisson's ratio value, v12

#### Constructor

**`Transtropic( name , axial_youngs_modulus , transverse_youngs_modulus , axial_shear_modulus , transverse_shear_modulus , major_poissons_ratio )`**

*Description*

    Instantiate ```Transtropic``` object that represents transversely isotropic constituent material.

*Parameters*

name

    Name of transversely isotropic constituent material.
    Only alphanumerical, underscore '_' and dashed '-' characters are allowed.

axial_youngs_modulus

    Axial Young's modulus of transversely isotropic constituent material.
    Only digits with no or single dot allowed representing positive values.
    To initialize, can be `int`, `float`, `str` and `Decimal` type number. Once initialized, it assumes `Decimal` type value.

transverse_youngs_modulus

    Transverse Young's modulus of transversely isotropic constituent material.
    Only digits with no or single dot allowed representing positive values.
    To initialize, can be `int`, `float`, `str` and `Decimal` type number. Once initialized, it assumes `Decimal` type value.

axial_shear_modulus

    Axial shear modulus of transversely isotropic constituent material.
    Only digits with no or single dot allowed representing positive values.
    To initialize, can be `int`, `float`, `str` and `Decimal` type number. Once initialized, it assumes `Decimal` type value.

transverse_shear_modulus

    Transverse shear modulus of transversely isotropic constituent material.
    Only digits with no or single dot allowed representing positive values.
    To initialize, can be `int`, `float`, `str` and `Decimal` type number. Once initialized, it assumes `Decimal` type value.

major_poissons_ratio

    Poisson's ratio of transversely isotropic material.
    Only digits with no or single dot allowed representing positive value between 0 and 0.5 inclusive, i.e. 0 < Poisson's ratio <= 0.5
    To initialize, can be `int`, `float`, `str` and `Decimal` type number. Once initialized, it assumes `Decimal` type value.

#### Class method

**`Transtropic.get()`**

*Description*

    Instantiate ```Transtropic``` object that represents transversely isotropic constituent material through user interaction.
    Return constructor call.


**`Transtropic.read( csv_filename )`**

*Description*

    Instantiate ```Transtropic``` object that represents transversely isotropic constituent material using data read from csv file.
    Return list of ```Transtropic``` objects

*Parameter*

csv_filename

    The name of csv file where data on transversely isotropic material that includes name, axial Young's modulus, transverse Young's modulus, axial shear modulus, transverse shear modulus and major Poisson's ratio

#### Instance Method

**`__str__( transtropic_object )`**

*Description*

    Return string representation of current ```Transtropic``` object where all its instance attributes and their values are shown.

*Parameter*

transtropic_object

    Instantiated ```Transtropic``` object.

<br>

<sup> # GO BACK TO [DOCUMENTATION](#documentation) </sup>

#### UNIDIRECTIONAL COMPOSITE MATERIAL

Unidirectional (UD) composite material is also a transversely isotropic but not homogeneoues material where the material is a actually a combination of two different distinct materials, having effective elastic properties influenced by the properties of its constituents and fiber volume fraction.

A UD composite where its effective elastic properties are defined by the Halpin-Tsai micromechanics is represented by ```HT``` object such as the following:

    ```HT``` object with eleven (11) attributes:
    - `fiber`                        : Fiber constituent material - ```Isotropic``` or ```Transtropic``` object
    - `matrix`                       : Matrix constituent material - ```Isotropic``` or ```Transtropic``` object
    - `name`                         : Name of UD composite - combination of names of fiber and matrix constituent material
    - `eff_axial_youngs_moduli`      : Effective axial Young's modulus values^, E1eff / E1* (GPa)
    - `eff_transverse_youngs_moduli` : Effective transverse Young's modulus values^, E2eff / E2* (GPa)
    - `eff_axial_shear_moduli`       : Effective axial shear modulus values^, G12eff / G12* (GPa)
    - `eff_major_poissons_ratios`    : Effective major Poisson's ratios^, v12eff / v12*
    - `eff_transverse_shear_moduli`  : Effective transverse shear modulus values^, G23eff / G23* (GPa)
    - `eff_pstrain_bulk_moduli`      : Effective plane-strain bulk modulus values^, K23eff / K23* (GPa)
    - `micromechanics`               : Micromechanics method to estimate effective elastic moduli^^
    - `fiber_volfract`               : Fiber volume fraction in UD composite^^^

    Notes: ^ Values follow the incremental values of fiber volume fraction
          ^^ Class attribute whose value equals "Halpin-Tsai"
         ^^^ Class attribute whose values are ranging from 0 to 1 with 0.01 increments

#### Constructor

**`HT(fiber, matrix)`**

*Description*

    Instantiate ```HT`` object that represents transversely isotropic unidirectional composite material (UD composite).
    'HT' stands for UD composite with Halpin-Tsai estimated effective elastic moduli.

*Parameters*

fiber

    Fiber constituent material that can either be ```Isotropic``` or ```Transtropic``` object.

matrix

    Matrix constituent material that can either be ```Isotropic``` or ```Transtropic``` object.

#### Instance method

**`__str__( composite )`**

*Description*

    String representation of current ```HT``` object that represents UD composite material.

*Parameter*

composite

    composite of ```HT``` object


**`E1eff(min, max)`**

*Description*

    Display ratio between user-defined specific custom value or range of fiber volume fraction and effective axial Young's modulus of UD composite for quick in-situ analysis

*Parameters*

min

    Single int or float value in between 0 to 1 inclusive if custom value of fiber volume fraction is defined, or int or float minimum value between 0 and 1 inclusive if custom range of fiber volume fraction to be defined.

max

    None if single custom value of fiber volume fraction is defined, or int or float maximum value between 0 and 1 inclusive and also, must be greater than min value of custom range of fiber volume fraction to be defined.

**`E2eff(min, max)`**

*Description*

    Display ratio between user-defined specific custom value or range of fiber volume fraction and effective transverse Young's modulus of UD composite for quick in-situ analysis

*Parameters*

min

    Single int or float value in between 0 to 1 inclusive if custom value of fiber volume fraction is defined, or int or float minimum value between 0 and 1 inclusive if custom range of fiber volume fraction to be defined.

max

    None if single custom value of fiber volume fraction is defined, or int or float maximum value between 0 and 1 inclusive and also, must be greater than min value of custom range of fiber volume fraction to be defined.

**`G12eff(min, max)`**

*Description*

    Display ratio between user-defined specific custom value or range of fiber volume fraction and effective axial shear modulus of UD composite for quick in-situ analysis

*Parameters*

min

    Single int or float value in between 0 to 1 inclusive if custom value of fiber volume fraction is defined, or int or float minimum value between 0 and 1 inclusive if custom range of fiber volume fraction to be defined.

max

    None if single custom value of fiber volume fraction is defined, or int or float maximum value between 0 and 1 inclusive and also, must be greater than min value of custom range of fiber volume fraction to be defined.


**`v12eff(min, max)`**

*Description*

    Display ratio between user-defined specific custom value or range of fiber volume fraction and effective major Poisson's ratio of UD composite for quick in-situ analysis

*Parameters*

min

    Single int or float value in between 0 to 1 inclusive if custom value of fiber volume fraction is defined, or int or float minimum value between 0 and 1 inclusive if custom range of fiber volume fraction to be defined.

max

    None if single custom value of fiber volume fraction is defined, or int or float maximum value between 0 and 1 inclusive and also, must be greater than min value if custom range of fiber volume fraction to be defined.

**`G23eff(min, max)`**

*Description*

    Display ratio between user-defined specific custom value or range of fiber volume fraction and effective transverse shear modulus of UD composite for quick in-situ analysis

*Parameters*

min

    Single int or float value in between 0 to 1 inclusive if custom value of fiber volume fraction is defined, or int or float minimum value between 0 and 1 inclusive if custom range of fiber volume fraction to be defined.

max

    None if single custom value of fiber volume fraction is defined, or int or float maximum value between 0 and 1 inclusive and also, must be greater than min value of custom range of fiber volume fraction to be defined.

**`K23eff(min, max)`**

*Description*

    Display ratio between user-defined specific custom value or range of fiber volume fraction and effective plane-strain bulk modulus of UD composite for quick in-situ analysis

*Parameters*

min

    Single int or float value in between 0 to 1 inclusive if custom value of fiber volume fraction is defined, or int or float minimum value between 0 and 1 inclusive if custom range of fiber volume fraction to be defined.

max

    None if single custom value of fiber volume fraction is defined, or int or float maximum value between 0 and 1 inclusive and also, must be greater than min value of custom range of fiber volume fraction to be defined.

<br>

<sup> # GO BACK TO [DOCUMENTATION](#documentation) </sup>

#### MICROMECHANICS ANALYSIS

Several functions are provided for micromechanics analysis consisting of:

- display
- plot
- save
- doc

**`display( composite , min=None , max=None )`**

*Description*

    Function that displays elastic moduli of the UD composite's constituents and also the effective elastic moduli of UD composite versus either full range, custom range or custom value of fiber volume fraction defined by user.

*Parameters*

composite

    UD composite material of ```HT``` object.

min=None

    Either None if when full range of fiber volume fraction is to be displayed, single int or float value in between 0 and 1 inclusive if custom value of fiber volume fraction is defined, or int or float minimum value between 0 and 1 inclusive and also, less than max value if custom range of fiber volume fraction is defined.

max=None

    None if single custom value of fiber volume fraction or full range of fiber volume fraction is defined, or int or float maximum value in between 0 and 1, and also greater than minimum value if custom range of fiber volume fraction is defined.

**`plot( *composites , folder="png" )`**

*Description*

    Plot six (6) effective elastic moduli for every UD composite versus full range of fiber volume fraction where each plot shall be saved as png format file with unique file name according to the name of UD composite postfixed with the effective elastic moduli in a folder that has default name - "png".

*Parameters*

*composites

    variable number of UD composite materials of ```HT``` object.

folder="png"

    folder's name that has default value - "png" where all png files will be saved into.

**`save( *composites , folder="csv" )`**

*Description*

    Save two (2) csv files for UD composite that has constituent materials of the same type where 1 csv file for elastic moduli of constituent and the other is for effective elastic moduli of UD composite, or save three (3) csv files for UD composite that has different types of constituent material where 1 csv file for each type of constituent material and the other as usual is for effective elastic moduli of UD composite. All csv files will have unique names comprising the name of UD composite postfixed with appropriate code names and saved into a folder that has a default name - "csv".

*Parameters*

*composite

    variable number of UD composite materials of ```HT``` object.

folder="csv"

    folder's name that has default value - "csv" where all csv files will be saved into.

**`doc( *composites , doc_name="analysis" , doc_num="Appx. A" )`**

*Description*

    Create a pdf document documenting the results of Halpin-Tsai micromechanics analysis for a single UD or multiple UD composite material and save it with a filename that has prefix name defined by default value based on the keyword parameter - `doc_name`, e.g. `doc_name` = "analysis". The pdf will then be saved in a folder called "pdf", which is the sub-folder of the main, master folder that has the same name defined by the keyword parameter `doc_name`, which by default is "analysis".

    The pdf consists of i) front page, ii) elastic moduli of UD composite's constituents, iii) the plots of effective elastic moduli of UD composite versus full range of fiber volume fraction and iv) the table of data of effective elastic moduli of UD composite versus full range of fiber volume fraction. Except for the front page, the data in other sections are obtained from the csv and png files generated by the respective ``save`` and ``plot`` function called by this ``doc`` function. Thus, the main master folder shall contains three sub-folders of "png", "csv" and "pdf", in which contains the respective png, csv and pdf format files.

*Parameters*

\*composites

    Variable number of UD composites of ```HT``` object.

doc_name="analysis"

    Name of the document where its default value is "analysis".

doc_num="Appx. A"

    Reference number of the document where its default value is "Appx. A", which stands for Appendix A.

<br>

<sup> # GO BACK TO [DOCUMENTATION](#documentation) </sup>

#### MICROMECHANICS COMPARISON ANALYSIS
Several functions are provided for micromechanics comparison analysis comprising:

- compare
- plot_compare
- save_compare
- doc_compare

**`compare( *composites , property="E1eff" , min=None , max=None )`**

*Description*

    Compares two or at most five UD composites on specific effective elastic modulus, e.g. by default as defined by keyword parameter, property="E1eff" is the effective Young's modulus, or can be user-defined effective property defined through this keyword property, which the property are shown versus either full range, custom range or custom value of fiber volume fraction. At the same time, it displays comparison of elastic moduli of the all UD composites' constituent materials but only the relevant moduli that really affect or influence the effective elastic modulus of interest, i.e the property being compared.

*Parameters*

\*composites

    Variable number of UD composites of ```HT``` object being compared. Minimum is two and at most is five UD composites.

property="E1eff"

    Effective elastic modulus under comparison with default value set to E1eff, i.e. effective axial Young's modulus. The other valid property for comparison are "E2eff" - effective transverse Young's modulus, "G12eff" - effective axial shear modulus, "v12eff" - effective major Poisson's ratio, "G23eff" - effective transverse shear modulus and "K23eff" - plane-strain bulk modulus.

min=None

    Either None if when full range of fiber volume fraction is to be displayed, single int or float value in between 0 and 1 inclusive if custom value of fiber volume fraction is defined, or int or float minimum value between 0 and 1 inclusive and also, less than max value if custom range of fiber volume fraction is defined.

max=None

    None if single custom value of fiber volume fraction or full range of fiber volume fraction is defined, or int or float maximum value in between 0 and 1, and also greater than minimum value if custom range of fiber volume fraction is defined.

**`plot_compare( *composites , test_name="compare" , folder="png" )`**

*Description*

    Plot of six (6) comparison effective elastic moduli where in each plot, all relevant effective elastic modulus for every UD composites are plotted against full range of fiber volume and the plots will be saved as png format file with unique filename in a folder with default name given as "png".

*Parameters*

\*composites

    Variable number of UD composites of ```HT``` object being compared. Minimum is two and at most is five UD composites.

test_name="compare"

    The name for comparison analysis where its default value is defined as "compare".

folder="png"

    The name of the folder that has a default name as "png" into which all png files will be saved.

**`save_compare( *composites , test_name="compare" ,  folder="csv" )`**

*Description*

    Save six (6) csv files where each contains the comparison data of specific effective elastic moduli for every UD composites being compared.

*Parameters*

\*composites

    Variable number of UD composites of ```HT``` object being compared. Minimum is two and at most is five UD composites.

test_name="compare"

    The name for comparison analysis where its default value is termed as "compare".

folder="csv"

    The name of the folder that has a default name as "csv" where all csv files will be saved into.

**`doc_compare( *composites , doc_name="compare" , doc_num="Appx. A")`**

*Description*

    Create a pdf document documenting the results of Halpin-Tsai micromechanics comparison analysis for multiple UD composite material being compared and save it with a filename that has prefix name defined by default value based on the keyword parameter - `doc_name`, e.g. `doc_name` = "analysis". The pdf will then be saved in a folder called "pdf", which is the sub-folder of the main, master folder that has the same name defined by the keyword parameter `doc_name`, which by default is "analysis".

    The pdf consists of i) front page, ii) the comparison of elastic moduli of every UD composite's constituents, iii) the comparison plots of effective elastic moduli for every UD composite versus full range of fiber volume fraction and iv) tables of data of effective elastic moduli for every UD composite versus full range of fiber volume fraction. Except for the front page, the data in other sections are obtained from the csv and png files generated by the respective ``save_compare`` and ``plot_compare`` function called by this ``doc_compare`` function. Thus, the main master folder shall contains three sub-folders of "png", "csv" and "pdf", in which contains the respective png, csv and pdf format files.

*Parameters*

\*composites

    Variable number of UD composites of ```HT``` object being compared. Minimum is two and at most is five UD composites.

doc_names="compare"

    The type of pdf document where since this is a comparison analysis report, it has a default name called "compare".

doc_num="Appx. A"

    Reference number of the document where its default value is "Appx. A", which stands for Appendix A.

<br>

<sup> # GO BACK TO [DOCUMENTATION](#documentation) </sup>


### USAGE AND TUTORIALS

- [EXAMPLES OF CONSTITUENT MATERIALS](#examples-of-constituent-materials)
- [EXECUTE PROJECT.PY](#execute-projectpy)
- [HELP](#help)
- [INSTANTIATE ISOTROPIC AND TRANSTROPIC OBJECTS](#instantiate-isotropic-and-transtropic-objects)
- [INSTANCE ATTRIBUTES AND INSTANCE METHODS OF ISOTROPIC AND TRANSTROPIC OBJECT](#instance-attributes-and-instance-methods-of-isotropic-and-transtropic-object)
- [INSTANTIATE HT OBJECTS](#instantiate-ht-objects)
- [INSTANCE ATTRIBUTES AND INSTANCE METHODS OF HT OBJECT](#instance-attributes-and-instance-methods-of-ht-object)
- [CONDUCTING IN-SITU MICROMECHANICS ANALYSIS](#conducting-in-situ-micromechanics-analysis)
- [CONDUCTING IN-SITU MICROMECHANICS COMPARISON ANALYSIS](#conducting-in-situ-micromechanics-comparison-analysis)
- [PLOTTING GRAPH OF MICROMECHANICS ANALYSIS](#plotting-graph-of-micromechanics-analysis)
- [PLOTTING GRAPH OF MICROMECHANICS COMPARISON ANALYSIS](#plotting-graph-of-micromechanics-comparison-analysis)
- [SAVING DATA OF MICROMECHANICS ANALYSIS](#saving-data-of-micromechanics-analysis)
- [SAVING DATA OF MICROMECHANICS COMPARISON ANALYSIS](#saving-data-of-micromechanics-comparison-analysis)
- [DOCUMENTING REPORT ON MICROMECHANICS ANALYSIS](#documenting-report-on-micromechanics-analysis)
- [DOCUMENTING REPORT ON MICROMECHANICS COMPARISON ANALYSIS](#documenting-report-on-micromechanics-comparison-analysis)

<br>

<sup> # GO BACK TO [CONTENTS](#contents) </sup>

#### EXAMPLES OF CONSTITUENT MATERIALS

It is recommended that constituent's elastic properties to be readied at hands first prior to the start of Halpin-Tsai Micromechanics program. Herein, several dummy constituent materials are readied for our usage and tutorial purposes:

**Carbon Fiber - Transversely Isotropic Constituent Material**

    Axial Young's modulus, E1 (GPa)         : 250
    Transverse Young's modulus, E2 (GPa)    : 25
    Axial shear modulus, G12 (GPa)          : 20
    Transverse shear modulus, G23 (GPa)     : 10
    Major Poisson's ratio, v12              : 0.28

**Fiberglass Fiber - Isotropic Constituent Material**

    Young's modulus, E (GPa)                : 120
    Poisson's ratio, v                      : 0.29

**Epoxy Matrix - Isotropic Constituent Material**

    Young's modulus, E (GPa)                : 2.8
    Poisson's ratio, v                      : 0.3

**Graphite Matrix - Transversely Isotropic Constituent Material**

    Axial Young's modulus, E1 (GPa)         : 180
    Transverse Young's modulus, E2 (GPa)    : 20
    Axial shear modulus, G12 (GPa)          : 15
    Transverse shear modulus, G23 (GPa)     : 10
    Major Poisson's ratio, v12              : 0.29

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

#### EXECUTE PROJECT.PY

Since project.py is a final project of CS50P and thus, not a package yet, its usage in other python scripts is simply achieved with

    import project

Nonetheless, project.py can be a stand-alone program and it is best to execute it in *python interpreter shell* by typing in the command-line interface as

    python -i project.py

This brings us to the **Welcoming text-based image of CS50P: Halpin-Tsai Micromechanics** analysis such as follow

![Welcoming page](https://github.com/mbm74/Halpin-Tsai-Micromechanics/blob/main/gif/intro.gif?raw=true)

To exit, simply type in

    exit()

or in vscode interface, press

    CTRL + D

on keyboard.

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

#### HELP

In the .gif image given above, prior to the start of Halpin-Tsai micromechanics analysis just before the python shell command- prompt, there are instructions about help function offered by this code on the associated tools that can be used for micromechanics and comparison analysis. These tools include classes, instance methods and major functions for micromechanics and comparison analysis as described in the documentation section. To access information about these tools, simply type in at python shell command prompt as, e.g.

    help(display)

and press ENTER. This brings us to the docstrings of ``display`` function explaining what's the function is all about as well as its parameters and their types, error-raised and return value and types.

Let's do one on the plot function, e.g.

    help(plot)

and this brings us to the following:

    Help on function plot in module __main__:

    plot(*materials: __main__.HT, folder: str = 'png') -> None
        Plot UD composite's complete effective elastic properties versus fiber volume
        fraction and save them as png format file with a filename according to the effecitve
        elastic property being investigated postfixed with the name of UD composite being
        examed. Every png file will then be saved into a folder that bears the default name
        specifed by keyword parameter `folder`, e.g. `folder` = "png" unless re-specified by
        user. If successfully plotted and png files containing plots are saved in png
        folder, a confirmation status will be printed.

        Note 1: Whenever a new file is generated and saved, a message stating the png file
        with relevant name is saved will be printed out.

        Note 2: If any of the folder does not exist yet, it will then be created and a
        message will appear saying a new folder with relevant name is created.

        : param `materials`: Single UD or multiple UD composites to be plotted.
        : type: ```HT```
        : param `folder`: keyword parameter that defines the name of a folder where all plots
            are saved into. The default folder name is "png"
        : raise TypeError: if material is None or not ```HT``` object.
        : rtype: None

        Example 1: Plot effective elastic properties of 1 UD composite where each elastic
            property has its own plot, and save them as png format files inside default
            'png' folder

            >>> carbon = Transtropic.get()
            Constituent: Carbon
            Axial Young's modulus, E1 (GPa): 250
            Transverse Young's modulus, E2 (GPa): 25
            Axial shear modulus, G12 (GPa): 20
            Transverse shear modulus, G23 (GPa): 10
            Major Poisson's ratio, v12: .28
            >>>
            >>> epoxy = Isotropic.get()
            Constituent: Epoxy
            Young's modulus, E (GPa): 2.8
            Poisson's ratio, v: .3
            >>>
            >>> composite = HT(carbon, epoxy)
            >>>
            >>> plot(composite)
            Folder ./png created
            ================= Carbon-Phenolic_E1eff.png file saved! ==================
            ================= Carbon-Phenolic_E2eff.png file saved! ==================
            ================= Carbon-Phenolic_G12eff.png file saved! =================
            ================= Carbon-Phenolic_G23eff.png file saved! =================
            ================= Carbon-Phenolic_K23eff.png file saved! =================
            ================= Carbon-Phenolic_v12eff.png file saved! =================
            >>>

        Example 2: Plot effective elastic properties of 4 UD composite where each UD
            composite has its own 6 png files.

            >>> carbon = Transtropic.get()
            Constituent: Carbon
            Axial Young's modulus, E1 (GPa): 250
            Transverse Young's modulus, E2 (GPa): 25
            Axial shear modulus, G12 (GPa): 20
            Transverse shear modulus, G23 (GPa): 10
            Major Poisson's ratio, v12: .28
            >>>
            >>> fiberglass = Isotropic.get()
            Constituent: Fiberglass
            Young's modulus, E (GPa): 120
            Poisson's ratio, v: .29
            >>>
            >>> epoxy = Isotropic.get()
            Constituent: Epoxy
            Young's modulus, E (GPa): 2.8
            Poisson's ratio, v: .3
            >>>
            >>> phenolic = Isotropic.get()
            Constituent: Phenolic
            Young's modulus, E (GPa): 5
            Poisson's ratio, v: .33
            >>>
            >>> compositeA = HT(carbon, phenolic)
            >>> compositeB = HT(carbon, epoxy)
            >>> compositeC = HT(fiberglass, phenolic)
            >>> compositeD = HT(fiberglass, epoxy)
            >>>
            >>> plot(compositeA, compositeB, compositeC, compositeD)
            Folder ./png created
            ================= Carbon-Phenolic_E1eff.png file saved! ==================
            ================= Carbon-Phenolic_E2eff.png file saved! ==================
            ================= Carbon-Phenolic_G12eff.png file saved! =================
            ================= Carbon-Phenolic_G23eff.png file saved! =================
            ================= Carbon-Phenolic_K23eff.png file saved! =================
            ================= Carbon-Phenolic_v12eff.png file saved! =================
            =================== Carbon-Epoxy_E1eff.png file saved! ===================
            =================== Carbon-Epoxy_E2eff.png file saved! ===================
            ================== Carbon-Epoxy_G12eff.png file saved! ===================
            ================== Carbon-Epoxy_G23eff.png file saved! ===================
            ================== Carbon-Epoxy_K23eff.png file saved! ===================
            ================== Carbon-Epoxy_v12eff.png file saved! ===================
            =============== Fiberglass-Phenolic_E1eff.png file saved! ================
            =============== Fiberglass-Phenolic_E2eff.png file saved! ================
            =============== Fiberglass-Phenolic_G12eff.png file saved! ===============
            =============== Fiberglass-Phenolic_G23eff.png file saved! ===============
            =============== Fiberglass-Phenolic_K23eff.png file saved! ===============
            =============== Fiberglass-Phenolic_v12eff.png file saved! ===============
            ================= Fiberglass-Epoxy_E1eff.png file saved! =================
            ================= Fiberglass-Epoxy_E2eff.png file saved! =================
            ================ Fiberglass-Epoxy_G12eff.png file saved! =================
            ================ Fiberglass-Epoxy_G23eff.png file saved! =================
            ================ Fiberglass-Epoxy_K23eff.png file saved! =================
            ================ Fiberglass-Epoxy_v12eff.png file saved! =================
            >>>

To exit from this docstring, simply press q and ENTER.

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

#### INSTANTIATE ISOTROPIC AND TRANSTROPIC OBJECTS

As per documentation, there are three (3) ways we can instantiate ```Isotropic``` and ```Transtropic``` objects to respectively represent isotropic and transversely isotropic constituent materials and all these three approaches will be exhibited as follows:

#### Using Constructor Call

**Isotropic**

![Isotropic - Constructor Call](https://github.com/mbm74/Halpin-Tsai-Micromechanics/blob/main/gif/isotropic_1.gif?raw=true)

Assuming we want to create a fiberglass fiber isotropic constituent,

    >>> fiberglass = Isotropic("Fiberglass", 120, .29)
    >>>

where

    fiberglass - variable name of ```Isotropic``` object that represents isotropic fiber constituent material,
    Fiberglass - the name for isotropic fiber constituent material,
    120        - Young's modulus value, E in GPa of fiberglass isotropic material, and
    .29        - Poisson's ratio value, v (unitless) of fiberglass isotropic material.

To confirm the creation of ```Isotropic``` object in our machine, simply type in `fiberglass` and press ENTER, to which we have

    >>> fiberglass
    <__main__.Isotropic object at 0x759d59fa1280>

Let's understand the difference between the two terminologies - `fiberglass` and `Fiberglass`. Basically, `fiberglass` is a variable name for the ```Isotropic``` object that we have instantiated earlier where it represents isotropic material while `Fiberglass` is the name of that isotropic material.

**Transtropic**

![Transtropic - Constructor Call](https://github.com/mbm74/Halpin-Tsai-Micromechanics/blob/main/gif/transtropic_1.gif?raw=true)

If the creation of carbon fiber of transversely isotropic constituent material is desired, as per documentation for             ```Transtropic``` object instantiation, more arguments are needed since it is a transversely isotropic material. For example,

    >>> carbon = Transtropic("Carbon", 250, 25, 20, 10, .28)

where

    carbon      - the variable name of ```Transtropic``` object that represent transversely isotropic fiber constituent material,
    Carbon      - the name for transversely isotropic fiber constituent material,
    250         - axial Young's modulus value, E1 in GPa of carbon transversely isotropic material,
    25          - transverse Young's modulus value, E2 in GPa of carbon transversely isotropic material,
    20          - axial shear modulus value, G12 in GPa of carbon transversely isotropic material,
    10          - transverse Young's modulus value, G23 in GPa of carbon transversely isotropic material, and
    .28         - major Poisson's ratio value, v12 (unitless) of carbon transversely isotropic material.

Similarly, `carbon` is a variable name for the instantiated ```Transtropic``` object that represents transversely isotropic material while `Carbon` is the name of that transversely isotropic material.

On final note, `ValueError` will be raised if anytime the values entered for initializing instance attributes for either ```Isotropic``` or ```Transtropic``` do not confirm to the allowable values set in the validation methods when instantiating these objects. As per documentation, the arguments and their valid values are such as follows:

    Name                : Only alphanumerical, underscore '_' and dashed '-' characters
    Elastic constants   : Only digit characters with no or single dot only. Must be positive values
    Poisson's ratio     : Only digit characters with no or single dot only. Must be in between 0 and 0.5 values.

#### Using @classmethod - ``get``

``get`` @classmethod is used to instantiate ```Isotropic``` or ```Transtropic``` object through user interactive interaction.

**Isotropic**

![Isotropic - ``get`` classmethod](https://github.com/mbm74/Halpin-Tsai-Micromechanics/blob/main/gif/isotropic_2.gif?raw=true)

To instantiate epoxy matrix of isotropic constituent material, e.g.

    >>> epoxy = Isotropic.get()
    Constituent: Epoxy
    Young's modulus, E (GPa): 2.8
    Poisson's ratio, v: .3
    >>>

where

    epoxy       : the variable name for ```Isotropic``` object that represents isotropic matrix constituent,
    Epoxy       : the name of isotropic matrix constituent,
    2.8         : Young's modulus value, E in GPa of epoxy isotropic material, and
    .3          : Poisson's ratio value, v (unitless) of epoxy isotropic material.

**Transtropic**

![Transtropic - ``get`` classmethod](https://github.com/mbm74/Halpin-Tsai-Micromechanics/blob/main/gif/transtropic_2.gif?raw=true)

Similarly, to instantiate ```Transtropic``` object for graphite matrix of transversely isotropic constituent material,

    >>> graphite = Transtropic.get()
    Constituent: Graphite
    Axial Young's modulus, E1 (GPa): 180
    Transverse Young's modulus, E2 (GPa): 20
    Axial shear modulus, G12 (GPa): 15
    Transverse shear modulus, G23 (GPa): 10
    Major Poisson's ratio, v12: .29
    >>>

where

    graphite    : the variable name for ```Transtropic``` object that represents transversely isotropic matrix constituent
    Graphite    : the name of transversely isotropic matrix constituent,
    180         : axial Young's modulus value, E1 in GPa of graphite transversely isotropic material,
    20          : transverse Young's modulus value, E2 in GPa of graphite transversely isotropic material,
    15          : axial shear modulus value, G12 in GPa of graphite transversely isotropic material,
    10          : transverse shear modulus value, G23 in GPa of graphite transversely isotropic material, and
    .29         : major Poisson's ratio value, v12 (unitless) of graphite transversely isotropic material.


If any of the values entered do not confirm with the validation method, the user will be kept prompted to enter the correct values again and again until the correct and valid values are entered, e.g.

    >>> epoxy = Isotropic.get()
    Constituent: EPON 862                   # invalid due to whitespace in between characters
    Constituent: EPON862*                   # invalid due to non-alphanumerical and other than '_' and '-' characters
    Constituent: EPON-862                   # valid
    Axial Young's modulus, E1 (GPa): -2     # invalid due to negative value
    Axial Young's modulus, E1 (GPa): 2      # valid
    Poisson's ratio, v: -0.3                # invalid due to negative value
    Poisson's ratio, v: 0.6                 # invalid due to greater than 0.5
    Poisson's ratio, v: 0.3.0               # invalid due to extra decimal point
    Poisson's ratio, v: 0.3                 # valid
    >>>

#### Using @classmethod - ``read``

``read`` @classmethod is used to instantiate ```Isotropic``` or ```Transtropic``` objects using data set that are obtained from csv files. As per documentation, this @classmethod returns a list of specific type of materials. Based on this fact, several or multiple isotropic or transverse isotropic constituent materials can possibly be created. Nonetheless, only the same type of materials can be read from any csv file, i.e. the csv file must contain data for one type of materials only.

**Isotropic**

![Isotropic - ``read`` classmethod](https://github.com/mbm74/Halpin-Tsai-Micromechanics/blob/main/gif/isotropic_3.gif?raw=true)

Assuming isotropic material data of fiberglass fiber and epoxy matrix are available in the *isotropic.csv* and thus, to instantiate those two isotropic materials, we have

    >>> isotropic = Isotropic.read("isotropic.csv")
    >>>

If we were to type in *isotropic* and we get

    >>> isotropic
    [<__main__.Isotropic object at 0x759d59e66810>, <__main__.Isotropic object at 0x759d59e669c0>]
    >>>

Above shows that two ```Isotropic``` objects were instantiated by reading the csv file provided to the ``read`` @classmethod where as per the csv file, the first ```Isotropic``` object represents fiberglass isotropic fiber material while the second ```Isotropic``` object represents epoxy matrix material. We can confirm this by accessing the first element of `isotropic` list and using dot notation with name instance attribute to get the name of isotropic material of the first object, e.g.

    >>> isotropic[0].name
    'Fiberglass'
    >>>

and if do the same for the other isotropic's element, we have

    >>> isotropic[1].name
    'Epoxy'
    >>>

Perhaps, if we wish to be explicit, we can then initialize these isotropic's elements with new variable names and delete the isotropic list if needed to, e.g.

    >>> fiberglass = isotropic[0]
    >>> epoxy = isotropic[1]
    >>> del isotropic
    >>>

Done!

On final note, please ensure that **csv file has headers**, e.g. see [*isotropic.csv*](https://github.com/mbm74/Halpin-Tsai-Micromechanics/blob/60fb84d031693dd3a6976eb85b9133fbbbdb012e/csv%20input/isotropic.csv) here.

**Transtropic**

![Transtropic - ``read`` classmethod](https://github.com/mbm74/Halpin-Tsai-Micromechanics/blob/main/gif/transtropic_3.gif?raw=true)

Of course, we can do the same for instantiating ```Transtropic``` objects with csv [*transtropic.csv*](https://github.com/mbm74/Halpin-Tsai-Micromechanics/blob/60fb84d031693dd3a6976eb85b9133fbbbdb012e/csv%20input/transtropic.csv) file here, e.g.

    transtropic = Transtropic.read("transtropic.csv")

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

#### INSTANCE ATTRIBUTES AND INSTANCE METHODS OF ISOTROPIC AND TRANSTROPIC OBJECT

Previously, we have seen how we can access one of the instance attributes of our ```Isotropic``` objects when we needed to confirm their names where we accessed those attributes with dot notation. Let's dive into a bit detail on the instance attributes and instance methods of both ```Isotropic``` and ```Transtropic``` object.

#### __str__ method and instance attributes

To see all their instance attributes and their respective values, we can use the magic ``__str__`` method offered by both classes of materials.

**Isotropic**

Taking fiberglass isotropic material for example, we can simply type in using print function such as the following, to which we will get

    >>> print(fiberglass)
    obj.name: 'Fiberglass', obj.youngs_modulus: Decimal('120.000'), obj.poissons_ratio: Decimal('0.290'),obj.shear_modulus: Decimal('46.512'), obj.pstrain_bulk_modulus: Decimal('110.742'),
    >>>

Notice that the first three instance attributes are correlated with the arguments that we used to instantiate this particular object but for the other two attributes, i.e. `shear_modulus` and `pstrain_bulk_modulus`, they are automatically computed based on the values of `youngs_modulus` and `poissons_ratio` instance attributes. Thus, we have

    Independent instance attributes:
        name, youngs_modulus, poissons_ratio

    Dependent instance attributes:
        shear_modulus, pstrain_bulk_modulus

**Transtropic**

We can do the same for our carbon fiber of transversely isotropic material, e.g.

    >>> print(carbon)
    obj.name: 'Carbon', obj.axial_youngs_modulus: Decimal('250.000'), obj.transverse_youngs_modulus: Decimal('25.000'), obj.axial_shear_modulus: Decimal('20.000'), obj.transverse_shear_modulus: Decimal('10.000'), obj.major_poissons_ratio: Decimal('0.280'),obj.pstrain_bulk_modulus: Decimal('17.023')
    >>>

As we can see, the first six instance attributes are the same arguments having the same values that we used to instantiate this `carbon` material but as for the last instance attribute, which is `pstrain_bulk_modulus`, it is automatically computed based on the values of other instance attributes involving `axial_youngs_modulus`, `transverse_youngs_modulus`, `transverse_shear_modulus` and `major_poissons_ratio`. Thus, we also have for ```Transtropic``` object with the followings

    Independent instance attributes:
        name, axial_youngs_modulus, transverse_youngs_modulus, axial_shear_modulus, transverse_shear_modulus, major_poissons_ratio

    Dependent instance attributes:
        pstrain_bulk_modulus

**Re-initialize instance attribute's value**

On final note, our code has ability to re-initialize the values of all these instance attributes. However, the same validation methods or procedures still apply. Hence, they are not read-only attributes and this is just to serve for one purpose. Of course, we can use this ability to rectify our mistakes if wrong values were initialized during the first time we instantiated these objects but the main reason is more related to the ability of this code to conduct micromechanics analysis.

To recap, one of the goals of the analysis is to evaluate whether the selected constituent materials are able to produce the desired effective elastic moduli of UD composite at practical range of fiber volume fraction. Sometimes rather than changing the constituent materials, we can also tweak the values of elastic moduli of the constituent within reasonable values such that the desired effective elastic moduli can be achieved. From this, we can always go back to material supplier and request from them whether they are able to find such material or even engineer new constituent material that has these tweaked elastic properties. Of course, this new material will be very expensive material but then again, the code allows us to do just that when and if necessary.

But for now, let's re-initialize some of the values of independent instance attributes and see the effects on their dependent attributes. Let's re-initialize the value of Young's modulus of fiberglass isotropic fiber material, e.g. we have

    >>> fiberglass.youngs_modulus           # show the original value of independent attribute, `youngs_modulus`
    Decimal('120.000')
    >>> fiberglass.shear_modulus            # show the original value of dependent attribute, `shear_modulus`
    Decimal('46.512')
    >>>
    >>> fiberglass.youngs_modulus = 100     # re-initialize the value of independent attribute, `youngs_modulus`
    >>>
    >>> fiberglass.youngs_modulus           # show the re-initialized value of independent attribute, `youngs_modulus`
    Decimal('100.000')
    >>> fiberglass.shear_modulus            # show the changed valyue of dependent attribute, `shear_modulus`
    Decimal('38.760')
    >>>

As can be seen, the values of dependent instance attributes for any object are always dependent upon the values of their independent instance attributes. Now, this also means that we cannot simply re-initialize the values of dependent instance attributes. `ValueError` will be raised if the re-initialized values do not confirm with the values obtained from some isotropic or transverse-isotropic formula constrained by the physical reality of isotropic or transversely isotropic material behavior respectively. For example, in the case of fiberglass isotropic material,

    >>> fiberglass.shear modulus = 100      # attempt to re-initialize the value of dependent attribute, shear modulus
    Traceback (most recent call last):
      ...
      ...
    ValueError: Violated shear modulus value based on isotropic formula
    >>>

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

#### INSTANTIATE HT OBJECTS

![HT - UD composite](https://github.com/mbm74/Halpin-Tsai-Micromechanics/blob/main/gif/ht_1.gif?raw=true)

We are now ready to create our own UD composite materials.

From the constituent materials that we have, either ```Isotropic``` or ```Transtropic``` object, we can easily create unidirectional composite material or ply just by instantiating ```HT``` object.

As per documentation, there is only one way for us to achieve this, which is through the **Constructor call**.

Assuming that we wanted to create UD composite comprise fiberglass isotropic fiber and epoxy isotropic matrix where both are ```Isotropic``` objects; thus, all we have to do is just to type in the following Constructor call as follow:

    >>> composite1 = HT(fiberglass, epoxy)
    >>>

where

    composite1  - variable name of ```HT``` object representing unidirectional composite material
    fiberglass  - ```Isotropic``` object that has a variable name called 'fiberglass'
    epoxy       - ```Isotropic``` object that has a variable name called 'epoxy'

As usual, to confirm the existence of our instantiated ```HT``` object in our machine, just type in the following and we shall get

    >>> composite1
    <__main__.HT object at 0x759d59fa1550>
    >>>

Basically, we could make various types of UD composites based on the types of their constituent materials. Let's create another UD composite and this time, from carbon fiber of transversely isotropic material with epoxy matrix of isotropic material, e.g.

    >>> composite2 = HT(carbon, epoxy)
    >>>

Super easy right? Let's create another two UD composites where the first is a combination of both transversely isotropic fiber and matrix materials from carbon and graphite respecively, while the second is a combination of isotropic fiber from fiberglass with transversely isotropic matrix material from graphite. Thus,

    >>> composite3 = HT(carbon, graphite)
    >>> composite4 = HT(fiberglass, graphite)
    >>>

Alright, that's enough for now.

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

#### INSTANCE ATTRIBUTES AND INSTANCE METHODS OF HT OBJECT

#### Attributes

As per documentation, ```HT``` object has eleven (11) attributes consisting of two (2) independent instance attributes, seven (7) dependent instance attributes and two (2) class attributes. In general, these are **read-only** attributes where their values cannot be re-initialized to a certain extent. This will be explained in detail later.

The two class attributes are sort of like constants, which are

    micromechanics
    fiber_volfract

`micromechanics` attribute is just to show that the effective elastic moduli of the instantiated ```HT``` object are estimated by Halpin-Tsai method. For now, it doesn't have much usefulness as there are no other micromechanics methods used in this code when instantiating UD composite's object. However, if we were to access the attribute, we will get like the following

    >>> composite = HT(fiberglass, epoxy)
    >>> composite.micromechanics
    'Halpin-Tsai'
    >>>

As for `fiber_volfract` attribute, its value is a tuple that contains 101 elements of `Decimal` type numbers starting from 0, i.e. no fiber in a composite, all the way up to 1, i.e. the composite is 100% fiber, with 0.01 increments. Of course, anything greater than 0.9 fiber volume fraction is physically impossible but it is customary to represent such range interval and that is because of value 1 has a significant theoretical meaning, e.g. the composite's effective elastic moduli at fiber volume fraction equals 1 will be the same as elastic moduli of fiber material, on which the estimation on effective elastic properties can be validated.

In general, the effective moduli of any composite as has been mentioned earlier, depends on the properties of its constituents and the content of reinforcing fiber in the composite. Thus, this attribute plays important role in estimating the values of other instance attributes, i.e. attributes associated with effective elastic moduli as we shall see. If we were to access the values inside the tuple of this attribute, we have

    >>> composite.fiber_volfract
    (Decimal('0'), Decimal('0.01'), Decimal('0.02'), Decimal('0.03'), Decimal('0.04'), Decimal('0.05'), Decimal('0.06'), Decimal('0.07'), Decimal('0.08'), Decimal('0.09'), Decimal('0.1'), Decimal('0.11'), Decimal('0.12'), Decimal('0.13'), Decimal('0.14'), Decimal('0.15'), Decimal('0.16'), Decimal('0.17'), Decimal('0.18'), Decimal('0.19'), Decimal('0.2'), Decimal('0.21'), Decimal('0.22'), Decimal('0.23'), Decimal('0.24'), Decimal('0.25'), Decimal('0.26'), Decimal('0.27'), Decimal('0.28'), Decimal('0.29'), Decimal('0.3'), Decimal('0.31'), Decimal('0.32'), Decimal('0.33'), Decimal('0.34'), Decimal('0.35'), Decimal('0.36'), Decimal('0.37'), Decimal('0.38'), Decimal('0.39'), Decimal('0.4'), Decimal('0.41'), Decimal('0.42'), Decimal('0.43'), Decimal('0.44'), Decimal('0.45'), Decimal('0.46'), Decimal('0.47'), Decimal('0.48'), Decimal('0.49'), Decimal('0.5'), Decimal('0.51'), Decimal('0.52'), Decimal('0.53'), Decimal('0.54'), Decimal('0.55'), Decimal('0.56'), Decimal('0.57'), Decimal('0.58'), Decimal('0.59'), Decimal('0.6'), Decimal('0.61'), Decimal('0.62'), Decimal('0.63'), Decimal('0.64'), Decimal('0.65'), Decimal('0.66'), Decimal('0.67'), Decimal('0.68'), Decimal('0.69'), Decimal('0.7'), Decimal('0.71'), Decimal('0.72'), Decimal('0.73'), Decimal('0.74'), Decimal('0.75'), Decimal('0.76'), Decimal('0.77'), Decimal('0.78'), Decimal('0.79'), Decimal('0.8'), Decimal('0.81'), Decimal('0.82'), Decimal('0.83'), Decimal('0.84'), Decimal('0.85'), Decimal('0.86'), Decimal('0.87'), Decimal('0.88'), Decimal('0.89'), Decimal('0.9'), Decimal('0.91'), Decimal('0.92'), Decimal('0.93'), Decimal('0.94'), Decimal('0.95'), Decimal('0.96'), Decimal('0.97'), Decimal('0.98'), Decimal('0.99'), Decimal('1'))
    >>>

Let's move on next to the two independent instance attributes UD composite of ```HT``` object, which are fiber and matrix or we simply refer them to as '```HT``` fiber attribute' and '```HT``` matrix attribute'. These independent attributes can either be ```Isotropic``` or ```Transtropic``` material. For example, in the case of UD composite which is created from fiberglass and epoxy, both fiber and matrix should be isotropic material and we can verify this, e.g.

    >>> composite = HT(fiberglass, epoxy)           # instantiate UD composite with fiberglass and epoxy isotropic material
    >>>
    >>> composite.fiber                             # fiber attribute of composite of ```HT``` object
    <__main__.Isotropic object at 0x7efc0ba452e0>   # notice the address
    >>>
    >>> fiberglass
    <__main__.Isotropic object at 0x7efc0ba452e0>   # same address as the above
    >>>

We can do the same for its matrix attribute where we have

    >>> composite.matrix                            # matrix attribute of composite of ```HT``` object
    <__main__.Isotropic object at 0x7efc0ba46540>
    >>>
    >>> epoxy
    <__main__.Isotropic object at 0x7efc0ba46540>
    >>>

This means that we can access the original attributes of fiberglass and epoxy constituent material through composite's object but with twice dot notation, e.g.

    >>> fiberglass.name
    'Fiberglass'
    >>>
    >>> composite.fiber.name        # Use dot notation twice to access fiber's original name attribute from ```HT``` object
    'Fiberglass'
    >>>
    >>> epoxy.name
    'Epoxy'
    >>>
    >>> composite.matrix.name       # twice dot notation to access matrix's original name attribute from ```HT``` object
    'Epoxy'
    >>>

Now, let's evaluate the next seven (7) dependent instance attributes that depend on the two independent `fiber` and `matrix` attribute, which are

    name
    eff_axial_youngs_moduli
    eff_transverse_youngs_moduli
    eff_axial_shear_moduli
    eff_major_poissons_ratio
    eff_transverse_shear_moduli
    eff_pstrain_bulk_modulus

Please refer to the documentation to understand the definition of these attributes.

The first, which is `name` attribute of UD composite object, basically takes the names of both fiber's and matrix's original name attribute, which are then combined into one name separated by dashed '-' character. For example,

    >>> composite.fiber.name
    'Fiberglass'
    >>>
    >>> composite.matrix.name
    'Epoxy'
    >>>
    >>> composite.name
    'Fiberglass-Epoxy'
    >>>

For the remaining six (6) dependent instance attributes of ```HT``` object, their values are given in terms of tuples which contains 101 `Decimal` type numbers that were estimated with Halpin-Tsai micromechanics formulations following the incremental values in tuple of `fiber_volfract`'s class attribute.

For example, let's try to access the effective axial Young's moduli of our UD composite, which we have

    >>> composite.eff_axial_youngs_moduli
    (Decimal('2.800'), Decimal('3.972'), Decimal('5.144'), Decimal('6.316'), Decimal('7.488'), Decimal('8.660'), Decimal('9.832'), Decimal('11.004'), Decimal('12.176'), Decimal('13.348'), Decimal('14.520'), Decimal('15.692'), Decimal('16.864'), Decimal('18.036'), Decimal('19.208'), Decimal('20.380'), Decimal('21.552'), Decimal('22.724'), Decimal('23.896'), Decimal('25.068'), Decimal('26.240'), Decimal('27.412'), Decimal('28.584'), Decimal('29.756'), Decimal('30.928'), Decimal('32.100'), Decimal('33.272'), Decimal('34.444'), Decimal('35.616'), Decimal('36.788'), Decimal('37.960'), Decimal('39.132'), Decimal('40.304'), Decimal('41.476'), Decimal('42.648'), Decimal('43.820'), Decimal('44.992'), Decimal('46.164'), Decimal('47.336'), Decimal('48.508'), Decimal('49.680'), Decimal('50.852'), Decimal('52.024'), Decimal('53.196'), Decimal('54.368'), Decimal('55.540'), Decimal('56.712'), Decimal('57.884'), Decimal('59.056'), Decimal('60.228'), Decimal('61.400'), Decimal('62.572'), Decimal('63.744'), Decimal('64.916'), Decimal('66.088'), Decimal('67.260'), Decimal('68.432'), Decimal('69.604'), Decimal('70.776'), Decimal('71.948'), Decimal('73.120'), Decimal('74.292'), Decimal('75.464'), Decimal('76.636'), Decimal('77.808'), Decimal('78.980'), Decimal('80.152'), Decimal('81.324'), Decimal('82.496'), Decimal('83.668'), Decimal('84.840'), Decimal('86.012'), Decimal('87.184'), Decimal('88.356'), Decimal('89.528'), Decimal('90.700'), Decimal('91.872'), Decimal('93.044'), Decimal('94.216'), Decimal('95.388'), Decimal('96.560'), Decimal('97.732'), Decimal('98.904'), Decimal('100.076'), Decimal('101.248'), Decimal('102.420'), Decimal('103.592'), Decimal('104.764'), Decimal('105.936'), Decimal('107.108'), Decimal('108.280'), Decimal('109.452'), Decimal('110.624'), Decimal('111.796'), Decimal('112.968'), Decimal('114.140'), Decimal('115.312'), Decimal('116.484'), Decimal('117.656'), Decimal('118.828'), Decimal('120.000'))
    >>>

We can do the same for the remaining attributes of effective moduli but let's just do one more where this time, we wish to access the values of effective elastic shear moduli of our UD composite and furthermore, we are going to use pprint module, e.g.

    >>> pp.pprint(composite.eff_axial_shear_moduli)
    (Decimal('1.077'),
     Decimal('1.098'),
     Decimal('1.119'),
     Decimal('1.141'),
     Decimal('1.163'),
     Decimal('1.185'),
     Decimal('1.208'),
     Decimal('1.231'),
     Decimal('1.255'),
     Decimal('1.279'),
     Decimal('1.304'),
     Decimal('1.330'),
     Decimal('1.356'),
     Decimal('1.382'),
     Decimal('1.409'),
     Decimal('1.437'),
     Decimal('1.465'),
     Decimal('1.494'),
     Decimal('1.524'),
     Decimal('1.554'),
     Decimal('1.585'),
     Decimal('1.617'),
     Decimal('1.650'),
     Decimal('1.683'),
     Decimal('1.717'),
     Decimal('1.752'),
     Decimal('1.788'),
     Decimal('1.825'),
     Decimal('1.863'),
     Decimal('1.902'),
     Decimal('1.942'),
     Decimal('1.983'),
     Decimal('2.025'),
     Decimal('2.068'),
     Decimal('2.112'),
     Decimal('2.158'),
     Decimal('2.205'),
     Decimal('2.254'),
     Decimal('2.303'),
     Decimal('2.355'),
     Decimal('2.408'),
     Decimal('2.463'),
     Decimal('2.519'),
     Decimal('2.577'),
     Decimal('2.637'),
     Decimal('2.700'),
     Decimal('2.764'),
     Decimal('2.830'),
     Decimal('2.899'),
     Decimal('2.971'),
     Decimal('3.044'),
     Decimal('3.121'),
     Decimal('3.201'),
     Decimal('3.283'),
     Decimal('3.369'),
     Decimal('3.459'),
     Decimal('3.552'),
     Decimal('3.649'),
     Decimal('3.750'),
     Decimal('3.855'),
     Decimal('3.966'),
     Decimal('4.081'),
     Decimal('4.202'),
     Decimal('4.328'),
     Decimal('4.461'),
     Decimal('4.600'),
     Decimal('4.747'),
     Decimal('4.901'),
     Decimal('5.064'),
     Decimal('5.235'),
     Decimal('5.417'),
     Decimal('5.610'),
     Decimal('5.814'),
     Decimal('6.031'),
     Decimal('6.262'),
     Decimal('6.509'),
     Decimal('6.773'),
     Decimal('7.056'),
     Decimal('7.360'),
     Decimal('7.688'),
     Decimal('8.042'),
     Decimal('8.426'),
     Decimal('8.844'),
     Decimal('9.300'),
     Decimal('9.801'),
     Decimal('10.352'),
     Decimal('10.962'),
     Decimal('11.640'),
     Decimal('12.400'),
     Decimal('13.256'),
     Decimal('14.228'),
     Decimal('15.342'),
     Decimal('16.631'),
     Decimal('18.139'),
     Decimal('19.928'),
     Decimal('22.084'),
     Decimal('24.734'),
     Decimal('28.069'),
     Decimal('32.392'),
     Decimal('38.222'),
     Decimal('46.512'))
    >>>

Alright! But this output although every value was accurately estimated by Halpin-Tsai formulations, it is not that useful to us as we cannot make effective assessment, e.g. we do not know at which fiber volume fraction, these values represent.

Before we delve into this much further, let's take a step back where we mentioned earlier that all these attributes are read-only attributes, i.e. their values cannot be re-initialized. Attempting to do so will lead to futile effort and result, e.g.

    >>> composite.name
    'Fiberglass-Epoxy'
    >>>
    >>> composite.name = "Carbon-Epoxy"
    Traceback (most recent call last):
      ...
    AttributeError: property 'name' of 'HT' object has no setter
    >>>

However, this is only true if it is done directly but remember about the ability of our ```Isotropic``` or ```Transtropic``` object where the values of their instance attributes can be re-initialized? Hence, if we were to change the values of fiber's and matrix' original instance attributes, all the values of dependent instance attributes of ```HT``` object will be changed as well.

Let's do one example to exemplify this scenario. Let's change the name of our UD composite material by changing the original name attribute of fiber isotropic material, e.g.

    >>> composite.name
    'Fiberglass-Epoxy'
    >>>
    >>> composite.fiber.name
    'Fiberglass'
    >>>
    >>> composite.fiber.name = "Glass_fiber"
    >>>
    >>> composite.fiber.name
    'Glass_fiber'
    >>>
    >>> composite.name
    'Glass_fiber-Epoxy'
    >>>

`WARNING`: Any changes to the values of original attributes of fiber and matrix, the values of other dependent instance attributes of ```HT``` object will be changed accordingly.

#### Instance Method: In-situ micromechanics analysis

Prior to this, we have seen the values in tuples of effective elastic moduli and we stated that we cannot make effective assessment because we do not see at which fiber volume fraction, the values of effective elastic moduli represent.

To overcome this limitation, ```HT``` object offers several instance methods that allows us to do a quick, in-situ assessment on the effective properties of UD composite.

As per documentation, these instance methods are

    E1eff
    E2eff
    G12eff
    v12eff
    G23eff
    K23eff

Let's make a quick in-situ assessment on the effective axial Young's modulus value at 0.5 fiber volume fraction. To this, we type in as follow, which we will get

    >>> composite = HT(carbon, epoxy)
    >>>
    >>> composite.E1eff(0.5)
    Vf : E1*
    0.5 : 126.400
    >>>

As can be seen above, it shows sort of like a ratio between fiber volume fraction, Vf and the value of effective axial Young's modulus, E1*. Basically, it tells us that at 0.5 fiber volume fraction, the estimated value of effective axial Young's modulus of UD composite based on Halpin-Tsai estimation is equal to 126.4 Giga Pascal or simply, GPa.

We could also specifiy custom range of fiber volume fraction. Let's for example, we wish to evaluate the percentage difference of values of axial shear modulus between 0.5 and 0.55 since our manufacturing capability cuurently ables to produce UD composites at that range of fiber volume fraction. Hence, we have

    >>> composite.G12eff(0.5, 0.55)
    Vf : G12*
    0.5 : 2.832
    0.51 : 2.896
    0.52 : 2.963
    0.53 : 3.032
    0.54 : 3.104
    0.55 : 3.178
    >>>

From the output, it can be calculated that the difference of effective axial shear modulus at 0.5 and 0.55 fiber volume fraction is about 12%.

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

#### CONDUCTING IN-SITU MICROMECHANICS ANALYSIS

In previous in-situ analysis offered by ```HT```'s instance methods, it only gives us the relationship between fiber volume fraction and specific effective elastic constant. It does not however, give us the complete picture of the values of overall effective elastic moduli at whatever values of fiber volume fraction. Additionally, we cannot make qualitative assessment to relate the values of effective properties with the elastic moduli of constituents which was obviously not made available to us.

Thus, we need better in-situ analysis tool and ``display`` function allows us to do just that. For example, it can produce tables of elastic moduli of constituents and also, values of effective moduli of UD composites versus fiber volume fraction altogether for better and more effective assessment. For example,

    >>> composite = HT(carbon, epoxy)
    >>> display(composite)  # full range of fiber volume fraction will be tabled out

    [1] UD COMPOSITE: CARBON-EPOXY


    A) Fiber material: Carbon

    +---------------+------------+--------------+-------------+--------------+-------------+----------------+
    | Constituent   |      Axial |   Transverse |       Axial |   Transverse |       Major |   Plane-strain |
    |               |    Young's |      Young's |       Shear |        Shear |   Poisson's |           Bulk |
    |               |   Modulus, |     Modulus, |    Modulus, |     Modulus, |      Ratio, |       Modulus, |
    |               |   E1 (GPa) |     E2 (GPa) |   G12 (GPa) |    G23 (GPa) |         v12 |      K23 (GPa) |
    +===============+============+==============+=============+==============+=============+================+
    | Carbon        |     250.00 |        25.00 |       20.00 |        10.00 |        0.28 |          17.02 |
    +---------------+------------+--------------+-------------+--------------+-------------+----------------+

    B) Matrix material: Epoxy

    +---------------+------------+-------------+------------+-----------------+
    | Constituent   |    Young's |   Poisson's |      Shear |    Plane-strain |
    |               |   Modulus, |      Ratio, |   Modulus, |   Bulk Modulus, |
    |               |    E (GPa) |           v |    G (GPa) |         K (GPa) |
    +===============+============+=============+============+=================+
    | Epoxy         |       2.80 |        0.30 |       1.08 |            2.69 |
    +---------------+------------+-------------+------------+-----------------+

    C) Effective Elastic Moduli of Carbon-Epoxy

    +------+---------+---------+---------+--------+---------+---------+
    |   Vf |     E1* |     E2* |    G12* |   v12* |    G23* |    K23* |
    |      |   (GPa) |   (GPa) |   (GPa) |        |   (GPa) |   (GPa) |
    +======+=========+=========+=========+========+=========+=========+
    | 0.00 |    2.80 |    2.80 |    1.08 |   0.30 |    1.08 |    2.69 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.01 |    5.27 |    2.96 |    1.10 |   0.30 |    1.09 |    2.72 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.02 |    7.74 |    3.04 |    1.12 |   0.30 |    1.11 |    2.75 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.03 |   10.22 |    3.11 |    1.14 |   0.30 |    1.12 |    2.78 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.04 |   12.69 |    3.16 |    1.16 |   0.30 |    1.14 |    2.81 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.05 |   15.16 |    3.22 |    1.18 |   0.30 |    1.15 |    2.85 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.06 |   17.63 |    3.27 |    1.20 |   0.30 |    1.17 |    2.88 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.07 |   20.10 |    3.31 |    1.22 |   0.30 |    1.18 |    2.91 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.08 |   22.58 |    3.36 |    1.24 |   0.30 |    1.20 |    2.95 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.09 |   25.05 |    3.41 |    1.27 |   0.30 |    1.21 |    2.98 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.10 |   27.52 |    3.46 |    1.29 |   0.30 |    1.23 |    3.02 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.11 |   29.99 |    3.51 |    1.31 |   0.30 |    1.25 |    3.05 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.12 |   32.46 |    3.56 |    1.34 |   0.30 |    1.26 |    3.09 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.13 |   34.94 |    3.60 |    1.36 |   0.30 |    1.28 |    3.12 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.14 |   37.41 |    3.65 |    1.39 |   0.30 |    1.30 |    3.16 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.15 |   39.88 |    3.71 |    1.41 |   0.30 |    1.32 |    3.20 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.16 |   42.35 |    3.76 |    1.44 |   0.30 |    1.34 |    3.24 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.17 |   44.82 |    3.81 |    1.47 |   0.30 |    1.36 |    3.28 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.18 |   47.30 |    3.86 |    1.49 |   0.30 |    1.38 |    3.32 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.19 |   49.77 |    3.92 |    1.52 |   0.30 |    1.40 |    3.36 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.20 |   52.24 |    3.97 |    1.55 |   0.30 |    1.42 |    3.40 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.21 |   54.71 |    4.03 |    1.58 |   0.30 |    1.44 |    3.44 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.22 |   57.18 |    4.09 |    1.61 |   0.30 |    1.46 |    3.49 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.23 |   59.66 |    4.14 |    1.64 |   0.30 |    1.48 |    3.53 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.24 |   62.13 |    4.20 |    1.67 |   0.30 |    1.50 |    3.58 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.25 |   64.60 |    4.27 |    1.70 |   0.29 |    1.52 |    3.62 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.26 |   67.07 |    4.33 |    1.73 |   0.29 |    1.55 |    3.67 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.27 |   69.54 |    4.39 |    1.77 |   0.29 |    1.57 |    3.72 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.28 |   72.02 |    4.46 |    1.80 |   0.29 |    1.59 |    3.77 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.29 |   74.49 |    4.52 |    1.83 |   0.29 |    1.62 |    3.81 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.30 |   76.96 |    4.59 |    1.87 |   0.29 |    1.64 |    3.87 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.31 |   79.43 |    4.66 |    1.91 |   0.29 |    1.67 |    3.92 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.32 |   81.90 |    4.73 |    1.95 |   0.29 |    1.70 |    3.97 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.33 |   84.38 |    4.80 |    1.98 |   0.29 |    1.72 |    4.03 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.34 |   86.85 |    4.87 |    2.02 |   0.29 |    1.75 |    4.08 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.35 |   89.32 |    4.95 |    2.06 |   0.29 |    1.78 |    4.14 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.36 |   91.79 |    5.03 |    2.11 |   0.29 |    1.81 |    4.20 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.37 |   94.26 |    5.10 |    2.15 |   0.29 |    1.83 |    4.25 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.38 |   96.74 |    5.18 |    2.19 |   0.29 |    1.86 |    4.31 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.39 |   99.21 |    5.27 |    2.24 |   0.29 |    1.90 |    4.38 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.40 |  101.68 |    5.35 |    2.28 |   0.29 |    1.93 |    4.44 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.41 |  104.15 |    5.44 |    2.33 |   0.29 |    1.96 |    4.50 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.42 |  106.62 |    5.53 |    2.38 |   0.29 |    1.99 |    4.57 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.43 |  109.10 |    5.62 |    2.43 |   0.29 |    2.03 |    4.64 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.44 |  111.57 |    5.71 |    2.48 |   0.29 |    2.06 |    4.71 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.45 |  114.04 |    5.81 |    2.54 |   0.29 |    2.10 |    4.78 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.46 |  116.51 |    5.91 |    2.59 |   0.29 |    2.14 |    4.85 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.47 |  118.98 |    6.01 |    2.65 |   0.29 |    2.17 |    4.93 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.48 |  121.46 |    6.11 |    2.71 |   0.29 |    2.21 |    5.00 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.49 |  123.93 |    6.22 |    2.77 |   0.29 |    2.25 |    5.08 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.50 |  126.40 |    6.33 |    2.83 |   0.29 |    2.29 |    5.16 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.51 |  128.87 |    6.44 |    2.90 |   0.29 |    2.34 |    5.25 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.52 |  131.34 |    6.56 |    2.96 |   0.29 |    2.38 |    5.33 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.53 |  133.82 |    6.68 |    3.03 |   0.29 |    2.43 |    5.42 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.54 |  136.29 |    6.80 |    3.10 |   0.29 |    2.47 |    5.51 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.55 |  138.76 |    6.93 |    3.18 |   0.29 |    2.52 |    5.60 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.56 |  141.23 |    7.05 |    3.25 |   0.29 |    2.57 |    5.69 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.57 |  143.70 |    7.19 |    3.33 |   0.29 |    2.62 |    5.79 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.58 |  146.18 |    7.33 |    3.42 |   0.29 |    2.68 |    5.89 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.59 |  148.65 |    7.47 |    3.50 |   0.29 |    2.73 |    6.00 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.60 |  151.12 |    7.62 |    3.59 |   0.29 |    2.79 |    6.10 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.61 |  153.59 |    7.78 |    3.69 |   0.29 |    2.85 |    6.21 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.62 |  156.06 |    7.93 |    3.78 |   0.29 |    2.91 |    6.33 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.63 |  158.54 |    8.10 |    3.88 |   0.29 |    2.97 |    6.44 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.64 |  161.01 |    8.27 |    3.99 |   0.29 |    3.03 |    6.56 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.65 |  163.48 |    8.44 |    4.10 |   0.29 |    3.10 |    6.69 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.66 |  165.95 |    8.62 |    4.21 |   0.29 |    3.17 |    6.82 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.67 |  168.42 |    8.81 |    4.33 |   0.29 |    3.25 |    6.95 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.68 |  170.90 |    9.01 |    4.45 |   0.29 |    3.32 |    7.09 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.69 |  173.37 |    9.21 |    4.58 |   0.29 |    3.40 |    7.23 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.70 |  175.84 |    9.42 |    4.72 |   0.29 |    3.48 |    7.38 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.71 |  178.31 |    9.64 |    4.86 |   0.29 |    3.57 |    7.53 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.72 |  180.78 |    9.87 |    5.01 |   0.29 |    3.66 |    7.69 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.73 |  183.26 |   10.11 |    5.17 |   0.29 |    3.75 |    7.85 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.74 |  185.73 |   10.35 |    5.34 |   0.29 |    3.85 |    8.03 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.75 |  188.20 |   10.61 |    5.52 |   0.28 |    3.95 |    8.20 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.76 |  190.67 |   10.88 |    5.70 |   0.28 |    4.05 |    8.39 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.77 |  193.14 |   11.16 |    5.90 |   0.28 |    4.17 |    8.58 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.78 |  195.62 |   11.46 |    6.11 |   0.28 |    4.28 |    8.78 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.79 |  198.09 |   11.77 |    6.33 |   0.28 |    4.40 |    8.99 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.80 |  200.56 |   12.09 |    6.57 |   0.28 |    4.53 |    9.20 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.81 |  203.03 |   12.43 |    6.82 |   0.28 |    4.67 |    9.43 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.82 |  205.50 |   12.79 |    7.09 |   0.28 |    4.81 |    9.67 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.83 |  207.98 |   13.16 |    7.38 |   0.28 |    4.96 |    9.92 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.84 |  210.45 |   13.56 |    7.68 |   0.28 |    5.12 |   10.18 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.85 |  212.92 |   13.98 |    8.02 |   0.28 |    5.29 |   10.45 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.86 |  215.39 |   14.42 |    8.38 |   0.28 |    5.47 |   10.73 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.87 |  217.86 |   14.89 |    8.76 |   0.28 |    5.66 |   11.04 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.88 |  220.34 |   15.39 |    9.18 |   0.28 |    5.87 |   11.35 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.89 |  222.81 |   15.91 |    9.64 |   0.28 |    6.08 |   11.69 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.90 |  225.28 |   16.48 |   10.14 |   0.28 |    6.32 |   12.04 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.91 |  227.75 |   17.07 |   10.69 |   0.28 |    6.57 |   12.41 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.92 |  230.22 |   17.71 |   11.30 |   0.28 |    6.83 |   12.80 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.93 |  232.70 |   18.40 |   11.97 |   0.28 |    7.12 |   13.22 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.94 |  235.17 |   19.13 |   12.72 |   0.28 |    7.43 |   13.66 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.95 |  237.64 |   19.92 |   13.57 |   0.28 |    7.77 |   14.13 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.96 |  240.11 |   20.78 |   14.52 |   0.28 |    8.14 |   14.63 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.97 |  242.58 |   21.70 |   15.60 |   0.28 |    8.54 |   15.17 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.98 |  245.06 |   22.71 |   16.85 |   0.28 |    8.98 |   15.74 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.99 |  247.53 |   23.80 |   18.30 |   0.28 |    9.46 |   16.36 |
    +------+---------+---------+---------+--------+---------+---------+
    | 1.00 |  250.00 |   25.00 |   20.00 |   0.28 |   10.00 |   17.02 |
    +------+---------+---------+---------+--------+---------+---------+

    >>>

We could also specify the custom range of fiber volume fraction, e.g.

    >>> display(composite, 0.55, 0.6)  # Custom range of fiber volume fraction

    [1] UD COMPOSITE: CARBON-EPOXY


    A) Fiber material: Carbon

    +---------------+------------+--------------+-------------+--------------+-------------+----------------+
    | Constituent   |      Axial |   Transverse |       Axial |   Transverse |       Major |   Plane-strain |
    |               |    Young's |      Young's |       Shear |        Shear |   Poisson's |           Bulk |
    |               |   Modulus, |     Modulus, |    Modulus, |     Modulus, |      Ratio, |       Modulus, |
    |               |   E1 (GPa) |     E2 (GPa) |   G12 (GPa) |    G23 (GPa) |         v12 |      K23 (GPa) |
    +===============+============+==============+=============+==============+=============+================+
    | Carbon        |     250.00 |        25.00 |       20.00 |        10.00 |        0.28 |          17.02 |
    +---------------+------------+--------------+-------------+--------------+-------------+----------------+

    B) Matrix material: Epoxy

    +---------------+------------+-------------+------------+-----------------+
    | Constituent   |    Young's |   Poisson's |      Shear |    Plane-strain |
    |               |   Modulus, |      Ratio, |   Modulus, |   Bulk Modulus, |
    |               |    E (GPa) |           v |    G (GPa) |         K (GPa) |
    +===============+============+=============+============+=================+
    | Epoxy         |       2.80 |        0.30 |       1.08 |            2.69 |
    +---------------+------------+-------------+------------+-----------------+

    C) Effective Elastic Moduli of Carbon-Epoxy

    +------+---------+---------+---------+--------+---------+---------+
    |   Vf |     E1* |     E2* |    G12* |   v12* |    G23* |    K23* |
    |      |   (GPa) |   (GPa) |   (GPa) |        |   (GPa) |   (GPa) |
    +======+=========+=========+=========+========+=========+=========+
    | 0.55 |  138.76 |    6.93 |    3.18 |   0.29 |    2.52 |    5.60 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.56 |  141.23 |    7.05 |    3.25 |   0.29 |    2.57 |    5.69 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.57 |  143.70 |    7.19 |    3.33 |   0.29 |    2.62 |    5.79 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.58 |  146.18 |    7.33 |    3.42 |   0.29 |    2.68 |    5.89 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.59 |  148.65 |    7.47 |    3.50 |   0.29 |    2.73 |    6.00 |
    +------+---------+---------+---------+--------+---------+---------+
    | 0.60 |  151.12 |    7.62 |    3.59 |   0.29 |    2.79 |    6.10 |
    +------+---------+---------+---------+--------+---------+---------+

    >>>

If we are really confidence in our manufacturing process, we could specify the specific custom value of fiber volume fraction, e.g.

    >>> display(composite, 0.6)  # Specific value of fiber volume fraction

    [1] UD COMPOSITE: CARBON-EPOXY


    A) Fiber material: Carbon

    +---------------+------------+--------------+-------------+--------------+-------------+----------------+
    | Constituent   |      Axial |   Transverse |       Axial |   Transverse |       Major |   Plane-strain |
    |               |    Young's |      Young's |       Shear |        Shear |   Poisson's |           Bulk |
    |               |   Modulus, |     Modulus, |    Modulus, |     Modulus, |      Ratio, |       Modulus, |
    |               |   E1 (GPa) |     E2 (GPa) |   G12 (GPa) |    G23 (GPa) |         v12 |      K23 (GPa) |
    +===============+============+==============+=============+==============+=============+================+
    | Carbon        |     250.00 |        25.00 |       20.00 |        10.00 |        0.28 |          17.02 |
    +---------------+------------+--------------+-------------+--------------+-------------+----------------+

    B) Matrix material: Epoxy

    +---------------+------------+-------------+------------+-----------------+
    | Constituent   |    Young's |   Poisson's |      Shear |    Plane-strain |
    |               |   Modulus, |      Ratio, |   Modulus, |   Bulk Modulus, |
    |               |    E (GPa) |           v |    G (GPa) |         K (GPa) |
    +===============+============+=============+============+=================+
    | Epoxy         |       2.80 |        0.30 |       1.08 |            2.69 |
    +---------------+------------+-------------+------------+-----------------+

    C) Effective Elastic Moduli of Carbon-Epoxy

    +------+---------+---------+---------+--------+---------+---------+
    |   Vf |     E1* |     E2* |    G12* |   v12* |    G23* |    K23* |
    |      |   (GPa) |   (GPa) |   (GPa) |        |   (GPa) |   (GPa) |
    +======+=========+=========+=========+========+=========+=========+
    | 0.60 |  151.12 |    7.62 |    3.59 |   0.29 |    2.79 |    6.10 |
    +------+---------+---------+---------+--------+---------+---------+

    >>>

Pretty neat stuff, right?

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

#### CONDUCTING IN-SITU MICROMECHANICS COMPARISON ANALYSIS

If there is a need to compare effective elastic moduli of two (2) or at most, five (5) different UD composite materials, we can use ``compare`` function.

However, ``compare`` function only compare specific effective elastic constants of the UD composites chosen or defined by user, i.e. not all effective elastic moduli comparison are shown all at once on the screen.

At the same time, only relevant and not all elastic moduli of constituents of every UD composite that affects the specific user-defined effective elastic constants are shown on the screen in table format. Now, how do we know which constituent elastic moduli that have influence or greater effects on which effective elastic moduli? Well, that is based on the Halpin-Tsai formulations.

The ability to compare specific elastic moduli of the constituents will provide us the qualitative assessment on how these elastic moduli affecting the final value of their respective effective modulus.

In addition, the specific comparison on the effective elastic modulus is accompanied with extra information which shows the percentage difference between the compared effective elastic constant of one UD composite and the baseline effective elastic constant of one baseline UD composite material. In this case, the baseline UD composite will always be the first UD composite specified in the argument of ``compare`` function.

For example, let's compare the results of micromechanics analysis on specifically effective axial Young's modulus of 4 different UD composites such as the follows.

    >>> carbon = Transtropic("Carbon", 250, 25, 20, 10, .28)
    >>> fiberglass = Isotropic("Fiberglass", 120, .29)
    >>> graphite = Transtropic("Graphite", 180, 20, 15, 10, .29)
    >>> epoxy = Isotropic("Epoxy", 2.8, .3)
    >>>
    >>> composite1 = HT(carbon, epoxy)
    >>> composite2 = HT(fiberglass, epoxy)
    >>> composite3 = HT(carbon, graphite)
    >>> composite4 = HT(fiberglass, graphite)
    >>>
    >>> compare(composite1, composite2, composite3, composite4)  # compare effective axial Young's modulus by default

    A) 4 UD Composites for Comparison Analysis

    [1] - CARBON-EPOXY      # baseline UD composite
    [2] - FIBERGLASS-EPOXY
    [3] - CARBON-GRAPHITE
    [4] - FIBERGLASS-GRAPHITE

    B) 4 Fibers of UD Composites

    [1] : Carbon - Transtropic
    [2] : Fiberglass - Isotropic
    [3] : Carbon - Transtropic
    [4] : Fiberglass - Isotropic

    i) 4 Fibers on Young's / Axial Young's Modulus Comparison

    +---------------------------------+----------+--------------+----------+--------------+
    | Fiber Material                  |      [1] |          [2] |      [3] |          [4] |
    |                                 |   Carbon |   Fiberglass |   Carbon |   Fiberglass |
    +=================================+==========+==============+==========+==============+
    | Young's Modulus, E or           |   250.00 |       120.00 |   250.00 |       120.00 |
    | Axial Young's Modulus, E1 (GPa) |          |              |          |              |
    +---------------------------------+----------+--------------+----------+--------------+

    C) 4 Matrices of UD Composites

    [1] : Epoxy - Isotropic
    [2] : Epoxy - Isotropic
    [3] : Graphite - Transtropic
    [4] : Graphite - Transtropic

    i) 4 Matrices on Young's / Axial Young's Modulus Comparison

    +---------------------------------+---------+---------+------------+------------+
    | Matrix Material                 |     [1] |     [2] |        [3] |        [4] |
    |                                 |   Epoxy |   Epoxy |   Graphite |   Graphite |
    +=================================+=========+=========+============+============+
    | Young's Modulus, E or           |    2.80 |    2.80 |     180.00 |     180.00 |
    | Axial Young's Modulus, E1 (GPa) |         |         |            |            |
    +---------------------------------+---------+---------+------------+------------+

    D) Comparison of Effective Elastic Property of 4 UD Composites

    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    |   Vf |     [1] |     [2] |     diff. of |     [3] |     diff. of |     [4] |     diff. of |
    |      |     E1* |     E1* |   [2] to [1] |     E1* |   [3] to [1] |     E1* |   [4] to [1] |
    |      |   (GPa) |   (GPa) |          (%) |   (GPa) |          (%) |   (GPa) |          (%) |
    +======+=========+=========+==============+=========+==============+=========+==============+
    | 0.00 |    2.80 |    2.80 |         0.00 |  180.00 |      6328.60 |  180.00 |      6328.60 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.01 |    5.27 |    3.97 |       -24.70 |  180.70 |      3327.50 |  179.40 |      3302.90 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.02 |    7.74 |    5.14 |       -33.60 |  181.40 |      2242.50 |  178.80 |      2208.90 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.03 |   10.22 |    6.32 |       -38.20 |  182.10 |      1682.50 |  178.20 |      1644.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.04 |   12.69 |    7.49 |       -41.00 |  182.80 |      1340.70 |  177.60 |      1299.70 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.05 |   15.16 |    8.66 |       -42.90 |  183.50 |      1110.40 |  177.00 |      1067.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.06 |   17.63 |    9.83 |       -44.20 |  184.20 |       944.70 |  176.40 |       900.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.07 |   20.10 |   11.00 |       -45.30 |  184.90 |       819.70 |  175.80 |       774.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.08 |   22.58 |   12.18 |       -46.10 |  185.60 |       722.10 |  175.20 |       676.00 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.09 |   25.05 |   13.35 |       -46.70 |  186.30 |       643.80 |  174.60 |       597.10 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.10 |   27.52 |   14.52 |       -47.20 |  187.00 |       579.50 |  174.00 |       532.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.11 |   29.99 |   15.69 |       -47.70 |  187.70 |       525.80 |  173.40 |       478.20 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.12 |   32.46 |   16.86 |       -48.10 |  188.40 |       480.30 |  172.80 |       432.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.13 |   34.94 |   18.04 |       -48.40 |  189.10 |       441.30 |  172.20 |       392.90 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.14 |   37.41 |   19.21 |       -48.70 |  189.80 |       407.40 |  171.60 |       358.70 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.15 |   39.88 |   20.38 |       -48.90 |  190.50 |       377.70 |  171.00 |       328.80 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.16 |   42.35 |   21.55 |       -49.10 |  191.20 |       351.50 |  170.40 |       302.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.17 |   44.82 |   22.72 |       -49.30 |  191.90 |       328.10 |  169.80 |       278.80 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.18 |   47.30 |   23.90 |       -49.50 |  192.60 |       307.20 |  169.20 |       257.70 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.19 |   49.77 |   25.07 |       -49.60 |  193.30 |       288.40 |  168.60 |       238.80 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.20 |   52.24 |   26.24 |       -49.80 |  194.00 |       271.40 |  168.00 |       221.60 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.21 |   54.71 |   27.41 |       -49.90 |  194.70 |       255.90 |  167.40 |       206.00 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.22 |   57.18 |   28.58 |       -50.00 |  195.40 |       241.70 |  166.80 |       191.70 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.23 |   59.66 |   29.76 |       -50.10 |  196.10 |       228.70 |  166.20 |       178.60 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.24 |   62.13 |   30.93 |       -50.20 |  196.80 |       216.80 |  165.60 |       166.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.25 |   64.60 |   32.10 |       -50.30 |  197.50 |       205.70 |  165.00 |       155.40 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.26 |   67.07 |   33.27 |       -50.40 |  198.20 |       195.50 |  164.40 |       145.10 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.27 |   69.54 |   34.44 |       -50.50 |  198.90 |       186.00 |  163.80 |       135.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.28 |   72.02 |   35.62 |       -50.50 |  199.60 |       177.20 |  163.20 |       126.60 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.29 |   74.49 |   36.79 |       -50.60 |  200.30 |       168.90 |  162.60 |       118.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.30 |   76.96 |   37.96 |       -50.70 |  201.00 |       161.20 |  162.00 |       110.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.31 |   79.43 |   39.13 |       -50.70 |  201.70 |       153.90 |  161.40 |       103.20 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.32 |   81.90 |   40.30 |       -50.80 |  202.40 |       147.10 |  160.80 |        96.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.33 |   84.38 |   41.48 |       -50.80 |  203.10 |       140.70 |  160.20 |        89.90 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.34 |   86.85 |   42.65 |       -50.90 |  203.80 |       134.70 |  159.60 |        83.80 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.35 |   89.32 |   43.82 |       -50.90 |  204.50 |       129.00 |  159.00 |        78.00 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.36 |   91.79 |   44.99 |       -51.00 |  205.20 |       123.50 |  158.40 |        72.60 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.37 |   94.26 |   46.16 |       -51.00 |  205.90 |       118.40 |  157.80 |        67.40 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.38 |   96.74 |   47.34 |       -51.10 |  206.60 |       113.60 |  157.20 |        62.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.39 |   99.21 |   48.51 |       -51.10 |  207.30 |       109.00 |  156.60 |        57.90 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.40 |  101.68 |   49.68 |       -51.10 |  208.00 |       104.60 |  156.00 |        53.40 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.41 |  104.15 |   50.85 |       -51.20 |  208.70 |       100.40 |  155.40 |        49.20 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.42 |  106.62 |   52.02 |       -51.20 |  209.40 |        96.40 |  154.80 |        45.20 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.43 |  109.10 |   53.20 |       -51.20 |  210.10 |        92.60 |  154.20 |        41.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.44 |  111.57 |   54.37 |       -51.30 |  210.80 |        88.90 |  153.60 |        37.70 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.45 |  114.04 |   55.54 |       -51.30 |  211.50 |        85.50 |  153.00 |        34.20 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.46 |  116.51 |   56.71 |       -51.30 |  212.20 |        82.10 |  152.40 |        30.80 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.47 |  118.98 |   57.88 |       -51.40 |  212.90 |        78.90 |  151.80 |        27.60 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.48 |  121.46 |   59.06 |       -51.40 |  213.60 |        75.90 |  151.20 |        24.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.49 |  123.93 |   60.23 |       -51.40 |  214.30 |        72.90 |  150.60 |        21.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.50 |  126.40 |   61.40 |       -51.40 |  215.00 |        70.10 |  150.00 |        18.70 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.51 |  128.87 |   62.57 |       -51.40 |  215.70 |        67.40 |  149.40 |        15.90 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.52 |  131.34 |   63.74 |       -51.50 |  216.40 |        64.80 |  148.80 |        13.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.53 |  133.82 |   64.92 |       -51.50 |  217.10 |        62.20 |  148.20 |        10.70 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.54 |  136.29 |   66.09 |       -51.50 |  217.80 |        59.80 |  147.60 |         8.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.55 |  138.76 |   67.26 |       -51.50 |  218.50 |        57.50 |  147.00 |         5.90 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.56 |  141.23 |   68.43 |       -51.50 |  219.20 |        55.20 |  146.40 |         3.70 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.57 |  143.70 |   69.60 |       -51.60 |  219.90 |        53.00 |  145.80 |         1.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.58 |  146.18 |   70.78 |       -51.60 |  220.60 |        50.90 |  145.20 |        -0.70 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.59 |  148.65 |   71.95 |       -51.60 |  221.30 |        48.90 |  144.60 |        -2.70 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.60 |  151.12 |   73.12 |       -51.60 |  222.00 |        46.90 |  144.00 |        -4.70 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.61 |  153.59 |   74.29 |       -51.60 |  222.70 |        45.00 |  143.40 |        -6.60 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.62 |  156.06 |   75.46 |       -51.60 |  223.40 |        43.10 |  142.80 |        -8.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.63 |  158.54 |   76.64 |       -51.70 |  224.10 |        41.40 |  142.20 |       -10.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.64 |  161.01 |   77.81 |       -51.70 |  224.80 |        39.60 |  141.60 |       -12.10 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.65 |  163.48 |   78.98 |       -51.70 |  225.50 |        37.90 |  141.00 |       -13.80 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.66 |  165.95 |   80.15 |       -51.70 |  226.20 |        36.30 |  140.40 |       -15.40 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.67 |  168.42 |   81.32 |       -51.70 |  226.90 |        34.70 |  139.80 |       -17.00 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.68 |  170.90 |   82.50 |       -51.70 |  227.60 |        33.20 |  139.20 |       -18.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.69 |  173.37 |   83.67 |       -51.70 |  228.30 |        31.70 |  138.60 |       -20.10 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.70 |  175.84 |   84.84 |       -51.80 |  229.00 |        30.20 |  138.00 |       -21.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.71 |  178.31 |   86.01 |       -51.80 |  229.70 |        28.80 |  137.40 |       -22.90 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.72 |  180.78 |   87.18 |       -51.80 |  230.40 |        27.40 |  136.80 |       -24.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.73 |  183.26 |   88.36 |       -51.80 |  231.10 |        26.10 |  136.20 |       -25.70 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.74 |  185.73 |   89.53 |       -51.80 |  231.80 |        24.80 |  135.60 |       -27.00 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.75 |  188.20 |   90.70 |       -51.80 |  232.50 |        23.50 |  135.00 |       -28.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.76 |  190.67 |   91.87 |       -51.80 |  233.20 |        22.30 |  134.40 |       -29.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.77 |  193.14 |   93.04 |       -51.80 |  233.90 |        21.10 |  133.80 |       -30.70 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.78 |  195.62 |   94.22 |       -51.80 |  234.60 |        19.90 |  133.20 |       -31.90 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.79 |  198.09 |   95.39 |       -51.80 |  235.30 |        18.80 |  132.60 |       -33.10 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.80 |  200.56 |   96.56 |       -51.90 |  236.00 |        17.70 |  132.00 |       -34.20 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.81 |  203.03 |   97.73 |       -51.90 |  236.70 |        16.60 |  131.40 |       -35.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.82 |  205.50 |   98.90 |       -51.90 |  237.40 |        15.50 |  130.80 |       -36.40 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.83 |  207.98 |  100.08 |       -51.90 |  238.10 |        14.50 |  130.20 |       -37.40 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.84 |  210.45 |  101.25 |       -51.90 |  238.80 |        13.50 |  129.60 |       -38.40 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.85 |  212.92 |  102.42 |       -51.90 |  239.50 |        12.50 |  129.00 |       -39.40 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.86 |  215.39 |  103.59 |       -51.90 |  240.20 |        11.50 |  128.40 |       -40.40 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.87 |  217.86 |  104.76 |       -51.90 |  240.90 |        10.60 |  127.80 |       -41.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.88 |  220.34 |  105.94 |       -51.90 |  241.60 |         9.70 |  127.20 |       -42.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.89 |  222.81 |  107.11 |       -51.90 |  242.30 |         8.70 |  126.60 |       -43.20 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.90 |  225.28 |  108.28 |       -51.90 |  243.00 |         7.90 |  126.00 |       -44.10 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.91 |  227.75 |  109.45 |       -51.90 |  243.70 |         7.00 |  125.40 |       -44.90 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.92 |  230.22 |  110.62 |       -51.90 |  244.40 |         6.20 |  124.80 |       -45.80 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.93 |  232.70 |  111.80 |       -52.00 |  245.10 |         5.30 |  124.20 |       -46.60 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.94 |  235.17 |  112.97 |       -52.00 |  245.80 |         4.50 |  123.60 |       -47.40 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.95 |  237.64 |  114.14 |       -52.00 |  246.50 |         3.70 |  123.00 |       -48.20 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.96 |  240.11 |  115.31 |       -52.00 |  247.20 |         3.00 |  122.40 |       -49.00 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.97 |  242.58 |  116.48 |       -52.00 |  247.90 |         2.20 |  121.80 |       -49.80 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.98 |  245.06 |  117.66 |       -52.00 |  248.60 |         1.40 |  121.20 |       -50.50 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.99 |  247.53 |  118.83 |       -52.00 |  249.30 |         0.70 |  120.60 |       -51.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 1.00 |  250.00 |  120.00 |       -52.00 |  250.00 |         0.00 |  120.00 |       -52.00 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+

    >>>

As can be seen, there are four sections numbered by uppercase letters on the output of ``compare`` function, which are

    A) 4 UD Composites for Comparison Analysis
    B) 4 Fibers of UD Composites
    C) 4 Matrices of UD Composites
    D) Comparison of Effective Elastic Property of 4 UD Composites

In section A, all the four (4) names of UD composites are stated. The are numbered numerically according to the order of these UD composites specified as arguments in the ``compare`` function.

In section B and C, all four (4) names of fibers and matrices of UD composites are given respectively. In each of this section, it can be seen that there is a table comparing the values of either Young's modulus for isotropic constituent material or axial Young's modulus for transversely isotropic constituent material. Similar to before, they are also numbered accordingly according to the number assigned to their respective UD composite material.

Why only either Young's or axial Young's modulus of constituents are shown in the tables of section B and section C? This is because the final values of effective axial Young's modulus of every UD composite shown in table of section D depends only on either of those two elastic moduli of constituents (plus of course, fiber volume fraction) as per Halpin-Tsai formulation.

But why ``compare`` function displays comparison analysis on effective axial Young's modulus only as shown in table of section D? What about the other effective elastic moduli? Well, this is because the default value of keyword parameter of the ``compare`` function is set to effective axial Young's modulus, e.g. property="E1eff".

As per documentation, the followings are the effective elastic moduli recognized by the keyword parameter, `property` of ``compare`` function:

    E1eff   - effective axial Young's modulus
    E2eff   - effective transverse Young's modulus
    G12eff  - effective axial shear modulus
    v12eff  - effective major Poisson's ratio
    G23eff  - effective transverse shear modulus
    K23eff  - effective plane-strain bulk modulus

Finally, the section D of ``compare`` function shows the comparison values of every UD composite's effective axial Young's modulus. Notice that the first UD composite in the argument of ``compare`` function becomes the baseline material in the comparison table in section D where all other values on effective axial Young's modulus of all UD compsites are being compared to the baseline value of effective axial Young's modulus, from which percentage difference between the two compared values are given or shown.

Now, just like ``display`` function, we could also specify custom range or specific value of fiber volume fraction using the keyword parameter `min` and `max` of ``compare`` function.

Let's for example, evaluate the effective axial shear modulus, 'G12eff' of four (4) UD composites within the fiber volume fraction range from 0.55 to 0.6. Thus, we have

    >>> compare(composite1, composite2, composite3, composite4, property="G12eff", min=0.55, max=0.6)

    A) 4 UD Composites for Comparison Analysis

    [1] - CARBON-EPOXY
    [2] - FIBERGLASS-EPOXY
    [3] - CARBON-GRAPHITE
    [4] - FIBERGLASS-GRAPHITE

    B) 4 Fibers of UD Composites

    [1] : Carbon - Transtropic
    [2] : Fiberglass - Isotropic
    [3] : Carbon - Transtropic
    [4] : Fiberglass - Isotropic

    i) 4 Fibers on Shear / Axial Shear Modulus Comparison

    +--------------------------------+----------+--------------+----------+--------------+
    | Fiber Material                 |      [1] |          [2] |      [3] |          [4] |
    |                                |   Carbon |   Fiberglass |   Carbon |   Fiberglass |
    +================================+==========+==============+==========+==============+
    | Shear Modulus, G or            |    20.00 |        46.51 |    20.00 |        46.51 |
    | Axial Shear Modulus, G12 (GPa) |          |              |          |              |
    +--------------------------------+----------+--------------+----------+--------------+

    C) 4 Matrices of UD Composites

    [1] : Epoxy - Isotropic
    [2] : Epoxy - Isotropic
    [3] : Graphite - Transtropic
    [4] : Graphite - Transtropic

    i) 4 Matrices on Shear / Axial Shear Modulus Comparison

    +--------------------------------+---------+---------+------------+------------+
    | Matrix Material                |     [1] |     [2] |        [3] |        [4] |
    |                                |   Epoxy |   Epoxy |   Graphite |   Graphite |
    +================================+=========+=========+============+============+
    | Shear Modulus, G or            |    1.08 |    1.08 |      15.00 |      15.00 |
    | Axial Shear Modulus, G12 (GPa) |         |         |            |            |
    +--------------------------------+---------+---------+------------+------------+

    D) Comparison of Effective Elastic Property of 4 UD Composites

    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    |   Vf |     [1] |     [2] |     diff. of |     [3] |     diff. of |     [4] |     diff. of |
    |      |    G12* |    G12* |   [2] to [1] |    G12* |   [3] to [1] |    G12* |   [4] to [1] |
    |      |   (GPa) |   (GPa) |          (%) |   (GPa) |          (%) |   (GPa) |          (%) |
    +======+=========+=========+==============+=========+==============+=========+==============+
    | 0.55 |    3.18 |    3.46 |         8.80 |   17.56 |       452.50 |   26.77 |       742.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.56 |    3.25 |    3.55 |         9.10 |   17.61 |       441.00 |   27.07 |       731.60 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.57 |    3.33 |    3.65 |         9.40 |   17.66 |       429.50 |   27.37 |       720.80 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.58 |    3.42 |    3.75 |         9.70 |   17.71 |       418.30 |   27.68 |       710.10 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.59 |    3.50 |    3.85 |        10.00 |   17.76 |       407.00 |   28.00 |       699.20 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    | 0.60 |    3.59 |    3.97 |        10.40 |   17.81 |       395.90 |   28.31 |       688.20 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+

    >>>

Finally, let's compare effective plane strain bulk modulus of the four (4) UD composites at specific value of fiber volume fraction equals 0.6

    >>> compare(composite1, composite2, composite3, composite4, property="K23eff", min=0.6)

    A) 4 UD Composites for Comparison Analysis

    [1] - CARBON-EPOXY
    [2] - FIBERGLASS-EPOXY
    [3] - CARBON-GRAPHITE
    [4] - FIBERGLASS-GRAPHITE

    B) 4 Fibers of UD Composites

    [1] : Carbon - Transtropic
    [2] : Fiberglass - Isotropic
    [3] : Carbon - Transtropic
    [4] : Fiberglass - Isotropic

    i) 4 Fibers on Shear / Transverse Shear Modulus Comparison

    +-------------------------------------+----------+--------------+----------+--------------+
    | Fiber Material                      |      [1] |          [2] |      [3] |          [4] |
    |                                     |   Carbon |   Fiberglass |   Carbon |   Fiberglass |
    +=====================================+==========+==============+==========+==============+
    | Shear Modulus, G or                 |    10.00 |        46.51 |    10.00 |        46.51 |
    | Transverse Shear Modulus, G23 (GPa) |          |              |          |              |
    +-------------------------------------+----------+--------------+----------+--------------+

    ii) 4 Fibers on Plane-Strain Bulk Modulus Comparison

    +--------------------------------------+----------+--------------+----------+--------------+
    | Fiber Material                       |      [1] |          [2] |      [3] |          [4] |
    |                                      |   Carbon |   Fiberglass |   Carbon |   Fiberglass |
    +======================================+==========+==============+==========+==============+
    | Plane-Strain Bulk Modulus, K23 (GPa) |    17.02 |       110.74 |    17.02 |       110.74 |
    +--------------------------------------+----------+--------------+----------+--------------+

    C) 4 Matrices of UD Composites

    [1] : Epoxy - Isotropic
    [2] : Epoxy - Isotropic
    [3] : Graphite - Transtropic
    [4] : Graphite - Transtropic

    i) 4 Matrices on Shear / Transverse Shear Modulus Comparison

    +-------------------------------------+---------+---------+------------+------------+
    | Matrix Material                     |     [1] |     [2] |        [3] |        [4] |
    |                                     |   Epoxy |   Epoxy |   Graphite |   Graphite |
    +=====================================+=========+=========+============+============+
    | Shear Modulus, G or                 |    1.08 |    1.08 |      10.00 |      10.00 |
    | Transverse Shear Modulus, G23 (GPa) |         |         |            |            |
    +-------------------------------------+---------+---------+------------+------------+

    ii) 4 Matrices on Plane-Strain Bulk Modulus Comparison

    +--------------------------------------+---------+---------+------------+------------+
    | Matrix Material                      |     [1] |     [2] |        [3] |        [4] |
    |                                      |   Epoxy |   Epoxy |   Graphite |   Graphite |
    +======================================+=========+=========+============+============+
    | Plane-Strain Bulk Modulus, K23 (GPa) |    2.69 |    2.69 |      10.19 |      10.19 |
    +--------------------------------------+---------+---------+------------+------------+

    D) Comparison of Effective Elastic Property of 4 UD Composites

    +------+---------+---------+--------------+---------+--------------+---------+--------------+
    |   Vf |     [1] |     [2] |     diff. of |     [3] |     diff. of |     [4] |     diff. of |
    |      |    K23* |    K23* |   [2] to [1] |    K23* |   [3] to [1] |    K23* |   [4] to [1] |
    |      |   (GPa) |   (GPa) |          (%) |   (GPa) |          (%) |   (GPa) |          (%) |
    +======+=========+=========+==============+=========+==============+=========+==============+
    | 0.60 |    6.10 |    7.89 |        29.30 |   13.80 |       126.10 |   30.35 |       397.30 |
    +------+---------+---------+--------------+---------+--------------+---------+--------------+

    >>>

Alright, we are good for now.

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

#### PLOTTING GRAPH OF MICROMECHANICS ANALYSIS

Sometimes, micromechanics analysis data shown in table form is not sufficient and we have to evaluate the trends or change of effective elastic properties with increasing fiber volume fraction by plotting the graph.

With ``plot`` function, six effective elastic moduli can be plotted against the full range of fiber volume fraction and they will all be saved as png file format accordingly, e.g.

    >>> composite = HT(carbon, epoxy)
    >>> plot(composite)
    Folder ./png created  # new folder called "png" is created
    =================== Carbon-Epoxy_E1eff.png file saved! ===================
    =================== Carbon-Epoxy_E2eff.png file saved! ===================
    ================== Carbon-Epoxy_G12eff.png file saved! ===================
    ================== Carbon-Epoxy_G23eff.png file saved! ===================
    ================== Carbon-Epoxy_K23eff.png file saved! ===================
    ================== Carbon-Epoxy_v12eff.png file saved! ===================
    >>>

As can be seen, all these plots are individually saved as a png file with unique, specific name as to distinguish one from the other. Here are link to samples of plots on [Fiberglass-Epoxy UD composite](https://github.com/mbm74/Halpin-Tsai-Micromechanics/tree/a05fcf4bcf868d0761c7b2e5f659b644c9a2e2f6/plot_output).

Notice further the output of plot function where it says 'Folder ./png created'. Basically, all these png files will be saved in the default "png" folder but since "png" folder does not exist yet in our working directory, thus one is created, from which the user is notified.

It is also possible for us to plot multiple UD composites where each composite will have their own six (6) plots of effective elastic moduli versus fiber volume fraction, e.g.

    >>> composite1 = HT(carbon, epoxy)
    >>> composite2 = HT(fiberglass, epoxy)
    >>> plot(composite1, composite2)  # multiple ud composites
    =================== Carbon-Epoxy_E1eff.png file saved! ===================
    =================== Carbon-Epoxy_E2eff.png file saved! ===================
    ================== Carbon-Epoxy_G12eff.png file saved! ===================
    ================== Carbon-Epoxy_G23eff.png file saved! ===================
    ================== Carbon-Epoxy_K23eff.png file saved! ===================
    ================== Carbon-Epoxy_v12eff.png file saved! ===================
    ================= Fiberglass-Epoxy_E1eff.png file saved! =================
    ================= Fiberglass-Epoxy_E2eff.png file saved! =================
    ================ Fiberglass-Epoxy_G12eff.png file saved! =================
    ================ Fiberglass-Epoxy_G23eff.png file saved! =================
    ================ Fiberglass-Epoxy_K23eff.png file saved! =================
    ================ Fiberglass-Epoxy_v12eff.png file saved! =================
    >>>

Notice this time that no new folder message is printed out since "png" folder has been created earlier in our working directory.

On the other hand, it is also possible for us to replace that default folder's name with our own custom name and this is achieved by specifying the keyword parameter, `folder` of the plot function, e.g.

    >>> plot(composite1, folder="Carbon-Epoxy")  # specifying custom folder's name as 'Carbon-Epoxy'
    Folder ./Carbon-Epoxy created
    =================== Carbon-Epoxy_E1eff.png file saved! ===================
    =================== Carbon-Epoxy_E2eff.png file saved! ===================
    ================== Carbon-Epoxy_G12eff.png file saved! ===================
    ================== Carbon-Epoxy_G23eff.png file saved! ===================
    ================== Carbon-Epoxy_K23eff.png file saved! ===================
    ================== Carbon-Epoxy_v12eff.png file saved! ===================
    >>>

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

#### PLOTTING GRAPH OF MICROMECHANICS COMPARISON ANALYSIS

Previously, we have seen that each plotted graph contains a single curve of specific effective elastic property versus fiber volume fraction for one (1) UD composite material. Next, we want do a comparison analysis by plotting the comparison of effective moduli on the graphs, e.g. we can have specific effective elastic modulus of multiple UD composite plotted in a single graph. For this, we use ``plot_compare`` function.

``plot_compare`` function allows us to plot and compare the trends or behaviors of all six (6) effective elastic moduli between at least two (2) or at most five (5) UD composite materials. As in ``plot`` function, all these comparison plots will be saved as png format files in a folder.

Each png file for each effective elastic moduli will have a unique filename, which consists of two parts where the first part takes the name set by the keyword parameter, e.g. test_name="compare" while the second indicates which effective elastic modulus is being compared between the multiple UD composites.

All these files are then saved in a folder called 'png', which is the default name set by the keyword parameter, e.g. folder="png" of this ``plot_compare`` function.

Let's do comparison plot on the following UD composites, e.g.

    >>> carbon = Transtropic("Carbon", 250, 25, 20, 10, .28)
    >>> fiberglass = Isotropic("Fiberglass", 120, .29)
    >>> graphite = Transtropic("Graphite", 180, 20, 15, 10, .29)
    >>> epoxy = Isotropic("Epoxy", 2.8, .3)
    >>>
    >>> comp1 = HT(carbon, epoxy)
    >>> comp2 = HT(fiberglass, epoxy)
    >>> comp3 = HT(carbon, graphite)
    >>> comp4 = HT(fiberglass, graphite)
    >>>
    >>> plot_compare(comp1, comp2, comp3, comp4)
    Folder ./png created
    ===================== compare_E1eff.png file saved! ======================
    ===================== compare_E2eff.png file saved! ======================
    ===================== compare_G12eff.png file saved! =====================
    ===================== compare_G23eff.png file saved! =====================
    ===================== compare_K23eff.png file saved! =====================
    ===================== compare_v12eff.png file saved! =====================
    >>>

The sample of plotted graphs can be found in the link given here where the [comparison graphs of effective elastic properties for four (4) UD composites](https://github.com/mbm74/Halpin-Tsai-Micromechanics/tree/73a40d2c483cd2e566aee58bbfa4fd3299f041f0/plot_compare_output) are plotted and saved as png files.

Let's do one more and this time, we are going to define a different test_name value, e.g. 'comparison_micromechanics', which will be reflected on every png file's filename and we will save them in a folder called 'comparison'.

    >>> plot_compare(comp1, comp2, comp3, comp4, test_name="comparison_micromechanics", folder="comparison")
    Folder ./comparison created
    ============ comparison_micromechanics_E1eff.png file saved! =============
    ============ comparison_micromechanics_E2eff.png file saved! =============
    ============ comparison_micromechanics_G12eff.png file saved! ============
    ============ comparison_micromechanics_G23eff.png file saved! ============
    ============ comparison_micromechanics_K23eff.png file saved! ============
    ============ comparison_micromechanics_v12eff.png file saved! ============
    >>>

Easy stuff, right?

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

#### SAVING DATA OF MICROMECHANICS ANALYSIS

For record-keeping or saving micromechanics data purposes, the code provides a ``save`` function.

With ``save`` function, the elastic moduli of the constituents, both fiber and matrix, and also, effective moduli of UD composites are saved as csv files. Hence, if fiber and matrix is of the same type, i.e. both can either be ```Isotropic``` or ```Transtropic```, then only one (1) csv on their elastic moduli is saved plus of course, one (1) more csv file for the UD composite's effective elastic moduli. Hence, that's two (2) csv files generated.

On other hands, if fiber and matrix is of different type, i.e. one could be ```Isotropic``` while the other is ```Transtropic```, then two (2) csv files for different material types of elastic moduli will be saved plus again, one (1) csv file on the effective elastic moduli of the UD composite. Thus, we will be having three (3) csv files.

All these csv files are saved with unique filenames that distinguish one from the other. In general, the filenames are divided into two major categories where one is for elastic moduli of constituent and the other is for effective elastic moduli of UD composite.

For csv file that saves the effective moduli of UD composite, the filename consist of two (2) parts only where the first is the name of UD composite while the second is just the wording - 'eff_moduli', which of course, means effective moduli, e.g.

    Carbon-Epoxy_eff_moduli.csv
    Fiberglass-epoxy_eff_moduli.csv
    Carbon-Graphite_eff_moduli.csv
    Fiberglass-Graphite_eff_moduli.csv

However, for filename of the csv file that stores data on the elastic moduli of composite's constituents, it comprises three parts  where the first part will always be the name of the UD composite, the second part indicates whether the content of csv file is related to either 'fiber', 'matrix' or 'phases', i.e. both fiber and matrix, and finally the third part indicates whether the saved data represents isotropic or transversely isotropic material, i.e. either as 'iso' or 'tra' respectively, e.g.

    Carbon-Epoxy_fiber_tra_moduli.csv           # Carbon-Epoxy with transversely isotropic fiber
    Carbon-Epoxy_matrix_iso_moduli.csv          # Carbon-Epoxy with isotropic matrix
    Fiberglass-Epoxy_phases_iso_moduli.csv      # Fiberglass-Epoxy with both fiber and matrix as isotropic material
    Carbon-Graphite_phases_tra_moduli.csv       # Carbon-Graphite with both fiber and matrix as transversely isotropic
    Fiberglass-Graphite_fiber_iso_moduli.csv    # Fiberglass-Graphite with isotropic fiber
    Fiberglass-Graphite_matrix_tra_moduli.csv   # Fiberglass-Graphite with transversely isotropic matrix

As in the ``plot`` function, all csv files that are generated from ``save`` function are saved into a folder called "csv", which is the default name specified by the keyword parameter of ``save`` function. Of course, this folder's name can be renamed by user.

Let's create a UD composite where both fiber and matrix is of the same ```Isotropic``` type and we intend to save their data in csv file into default "csv" file, to which we will use ``save`` function. Thus, we have

    >>> fiberglass = Isotropic("Fiberglass", 120, .29)
    >>> epoxy = Isotropic("Epoxy", 2.8, .3)
    >>>
    >>> composite1 = HT(fiberglass, epoxy)
    >>>
    >>> save(composite1)
    Folder ./csv created
    =========== Fiberglass-Epoxy_phases_iso_moduli.csv file saved! ===========
    ============== Fiberglass-Epoxy_eff_moduli.csv file saved! ===============

As can be seen, a new folder csv is created since in our working directory, the csv folder does not exist yet. Let's create another composite that the fiber is transversely isotropic material and the matrix is from isotropic material. Let's save their data on the same existing 'csv' folder using ``save`` function, e.g.

    >>> carbon = Transtropic.get()
    Constituent: Carbon
    Axial Young's modulus, E1 (GPa): 250
    Transverse Young's modulus, E2 (GPa): 25
    Axial shear modulus, G12 (GPa): 20
    Transverse shear modulus, G23 (GPa): 10
    Major Poisson's ratio, v12: .28
    >>>
    >>> epoxy = Isotropic.get()
    Constituent: Epoxy
    Young's modulus, E (GPa): 2.8
    Poisson's ratio, v: .3
    >>>
    >>> composite2 = HT(carbon, epoxy)
    >>>
    ============= Carbon-Epoxy_fiber_tra_moduli.csv file saved! ==============
    ============= Carbon-Epoxy_matrix_iso_moduli.csv file saved! =============
    ================ Carbon-Epoxy_eff_moduli.csv file saved! =================

From above, it can clearly be seen that there are three (3) csv files created and all of them are saved into 'csv' folder. Nevertheless, there is no new user notification about the creation of 'csv' folder because that folder is already exist in our working directory. Here is the link to the sample of csv files on [Carbon-Epoxy UD composite](https://github.com/mbm74/Halpin-Tsai-Micromechanics/tree/a05fcf4bcf868d0761c7b2e5f659b644c9a2e2f6/save_output).

For the sake of example, let's save these two composites into a new folder called 'csv2' by specifying the keyword parameter `folder`, e.g. folder="csv2", of the ``save`` function. It will be seen that five (5) csv files will be created and the user will be informed with the new folder creation such as follows

    >>> save(composite1, composite2, folder="csv2")
    Folder ./csv2 created
    =========== Fiberglass-Epoxy_phases_iso_moduli.csv file saved! ===========
    ============== Fiberglass-Epoxy_eff_moduli.csv file saved! ===============
    ============= Carbon-Epoxy_fiber_tra_moduli.csv file saved! ==============
    ============= Carbon-Epoxy_matrix_iso_moduli.csv file saved! =============
    ================ Carbon-Epoxy_eff_moduli.csv file saved! =================

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

#### SAVING DATA OF MICROMECHANICS COMPARISON ANALYSIS

The data from comparison analysis on the effective elastic properties versus fiber volume fraction of multiple UD composites, e.g. at least two (2) or at most, five (5) UD composites, can be saved as csv format data in csv files.

Since there are six (6) effective elastic moduli estimated by Halpin-Tsai method in this micromechanics code, a total of six (6) comparison csv files will be saved in a folder.

Each file as usual, will have a unique filename where the first part takes the default name specified by the keyword parameter, test_name="compare", while the second part represents the effective elastic modulus under comparison.

All these csv files are then saved in a folder that has default name - 'csv' as specified by the keyword parameter, `folder`,  e.g. folder="csv" of this ``save_compare`` function.

Let's save the comparison data of effective elastic moduli between these four (4) UD composite materials such as the followings

    >>> carbon = Transtropic("Carbon", 250, 25, 20, 10, .28)
    >>> fiberglass = Isotropic("Fiberglass", 120, .29)
    >>> graphite = Transtropic("Graphite", 180, 20, 15, 10, .29)
    >>> epoxy = Isotropic("Epoxy", 2.8, .3)
    >>>
    >>> comp1 = HT(carbon, epoxy)
    >>> comp2 = HT(fiberglass, epoxy)
    >>> comp3 = HT(carbon, graphite)
    >>> comp4 = HT(fiberglass, graphite)
    >>>
    >>> save_compare(comp1, comp2, comp3, comp4)
    Folder ./csv created
    ===================== compare_E1eff.csv file saved! ======================
    ===================== compare_E2eff.csv file saved! ======================
    ===================== compare_G12eff.csv file saved! =====================
    ===================== compare_v12eff.csv file saved! =====================
    ===================== compare_G23eff.csv file saved! =====================
    ===================== compare_K23eff.csv file saved! =====================
    >>>

The sample of csv files can be found in the link given here where [comparison analysis data on the four (4) UD composites](https://github.com/mbm74/Halpin-Tsai-Micromechanics/tree/a4b4ad1cfbe80e9835ac4c291557abdbba0985ba/save_compare_ouput) are saved.

Before we end this tutorial, let's save the comparison data again but this time, we are going to change the keyword parameter `test_name` with new name, e.g. test_name="comparison_micromechanics" and also, change the default folder's name, e,g, folder="comparison",  and as such, we have

    >>> save_compare(comp1, comp2, comp3, comp4, test_name="comparison_micromechanics", folder="comparison")
    Folder ./comparison created
    ============ comparison_micromechanics_E1eff.csv file saved! =============
    ============ comparison_micromechanics_E2eff.csv file saved! =============
    ============ comparison_micromechanics_G12eff.csv file saved! ============
    ============ comparison_micromechanics_v12eff.csv file saved! ============
    ============ comparison_micromechanics_G23eff.csv file saved! ============
    ============ comparison_micromechanics_K23eff.csv file saved! ============
    >>>

Cool stuff, eh?

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

#### DOCUMENTING REPORT ON MICROMECHANICS ANALYSIS

All micromechanics analysis can be documented in [pdf report](https://github.com/mbm74/Halpin-Tsai-Micromechanics/blob/a05fcf4bcf868d0761c7b2e5f659b644c9a2e2f6/doc_output/analysis/pdf/analysis_report.pdf) for reporting purposes. The report consists of

    i) front page, in which contains title, sub-title, date, document number and space for document sign-off by a person who conducted the analysis and a person who can certify the results of micromechanics analysis,
    ii) section on elastic moduli of the UD composite's constituents,
    iii) section on plot figures of effective elastic moduli versus full range of fiber volume fraction, and
    iv) section on data of effective elastic moduli versus full range of fiber volume fraction presented in table form.

All data including the plots reported in this pdf document are obtained from the csv and png files, which are generated by the respective ``save`` and ``plot`` functions called by this ``doc`` function.

All these generated csv and png files are saved in their respective 'csv' and 'png' folders while the generated pdf report is saved in 'pdf' folder. The first part of the pdf report's filename assumes the default name specified by the keyword parameter, `doc_name`, which is doc_name="analysis" while the second part is simply the word, "report". Thus, the full file name as per default value is

    'analysis_report.pdf'.

For information, these 'csv', 'png' and 'pdf' folders become the sub-folders of the main, master folder that assumes default folder's name - "analysis", which is defined by the same keyword parameter, `doc_name="analysis"` of this ``doc`` function.

Another keyword parameter, `doc_num="Appx. A"` specifies the document reference number, which is given on the front page section of the pdf report. Reason for such default name is perhaps, the report is highly packed with information where most likely, it will not be used as main report but rather, the information therein will be extracted for the main report. Hence, the documentation number suitably becomes 'Appx. A', i.e. the first appendix of whatever main report. Well, we can change this if we want.

The sample output of this ``doc`` function that include all 'csv', 'png' and 'pdf' files and folders can be found here for [Fiberglass-Epoxy UD composite](https://github.com/mbm74/Halpin-Tsai-Micromechanics/tree/a05fcf4bcf868d0761c7b2e5f659b644c9a2e2f6/doc_output/analysis).

Let's now document the micromechanics analysis of Carbon-Epoxy UD composite material.

    >>> carbon = Transtropic("Carbon", 250, 25, 20, 10, .28)
    >>> epoxy = Isotropic("Epoxy", 120, .29)
    >>>
    >>> composite = HT(carbon, epoxy)
    >>>
    >>> doc(composite1)
    Folder ./analysis/csv created
    ============= Carbon-Epoxy_fiber_tra_moduli.csv file saved! ==============
    ============= Carbon-Epoxy_matrix_iso_moduli.csv file saved! =============
    ================ Carbon-Epoxy_eff_moduli.csv file saved! =================
    Folder ./analysis/png created
    =================== Carbon-Epoxy_E1eff.png file saved! ===================
    =================== Carbon-Epoxy_E2eff.png file saved! ===================
    ================== Carbon-Epoxy_G12eff.png file saved! ===================
    ================== Carbon-Epoxy_G23eff.png file saved! ===================
    ================== Carbon-Epoxy_K23eff.png file saved! ===================
    ================== Carbon-Epoxy_v12eff.png file saved! ===================
    Folder ./analysis/pdf created
    --------------------------------------------------------------------------
                        analysis_report.pdf file saved!
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    >>>

The report is not limited to just one UD composite and we can actually document micromechanics analysis on multiple UD composites. Let's document the results of micromechanics analysis on three (3) different UD composites e.g. Fiberglass-Epoxy as composite2, Carbon-Graphite as composite3 and Fiberglass-Graphite as composite4, and this time, we are going to give a specific name for the analysis as 'micromechanics', which is achieved by specifying the keyword parameter, `doc_name` of this ``doc`` function, e.g. 'doc_name="micromechanics". Additionally, the doc reference number as 'Appendix 1', which can be specified by keyword parameter, doc_num, e.g. `doc_num="Appendix 1"`. Thus, we have

    >>> doc(composite2, composite3, composite4, doc_name="micromechanics", doc_num="Appendix 1")
    Folder ./micromechanics/csv created
    =========== Fiberglass-Epoxy_phases_iso_moduli.csv file saved! ===========
    ============== Fiberglass-Epoxy_eff_moduli.csv file saved! ===============
    Folder ./micromechanics/png created
    ================= Fiberglass-Epoxy_E1eff.png file saved! =================
    ================= Fiberglass-Epoxy_E2eff.png file saved! =================
    ================ Fiberglass-Epoxy_G12eff.png file saved! =================
    ================ Fiberglass-Epoxy_G23eff.png file saved! =================
    ================ Fiberglass-Epoxy_K23eff.png file saved! =================
    ================ Fiberglass-Epoxy_v12eff.png file saved! =================
    =========== Carbon-Graphite_phases_tra_moduli.csv file saved! ============
    =============== Carbon-Graphite_eff_moduli.csv file saved! ===============
    ================= Carbon-Graphite_E1eff.png file saved! ==================
    ================= Carbon-Graphite_E2eff.png file saved! ==================
    ================= Carbon-Graphite_G12eff.png file saved! =================
    ================= Carbon-Graphite_G23eff.png file saved! =================
    ================= Carbon-Graphite_K23eff.png file saved! =================
    ================= Carbon-Graphite_v12eff.png file saved! =================
    ========== Fiberglass-Graphite_fiber_iso_moduli.csv file saved! ==========
    ========= Fiberglass-Graphite_matrix_tra_moduli.csv file saved! ==========
    ============= Fiberglass-Graphite_eff_moduli.csv file saved! =============
    =============== Fiberglass-Graphite_E1eff.png file saved! ================
    =============== Fiberglass-Graphite_E2eff.png file saved! ================
    =============== Fiberglass-Graphite_G12eff.png file saved! ===============
    =============== Fiberglass-Graphite_G23eff.png file saved! ===============
    =============== Fiberglass-Graphite_K23eff.png file saved! ===============
    =============== Fiberglass-Graphite_v12eff.png file saved! ===============
    Folder ./micromechanics/pdf created
    --------------------------------------------------------------------------
                    micromechanics_report.pdf file saved!
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

#### DOCUMENTING REPORT ON MICROMECHANICS COMPARISON ANALYSIS

``doc_compare`` function allows us to document micromechanics comparison analysis between at minimum, two (2) or at maximum, five (5) UD composite materials as [pdf report](https://github.com/mbm74/Halpin-Tsai-Micromechanics/blob/60fb84d031693dd3a6976eb85b9133fbbbdb012e/doc_compare_output/comparison/pdf/comparison_report.pdf) file.

The pdf report consists of

    i) front page, in which contains title, sub-title, date, document number and space for document sign-off by a person who conducted the analysis and a person who can certify the results of micromechanics comparison analysis,
    ii) section on constituent's elastic moduli of every UD composite being compared,
    iii) section on comparison plot figures of effective elastic moduli versus full range of fiber volume fraction, and
    iv) section on comparison data of effective elastic moduli versus full range of fiber volume fraction presented in table form.

Similar to ``doc`` function, all data that are used in the pdf comparison report are obtained from the 'csv' and 'png' files that are generated by their respective ``save_compare`` and ``plot_compare`` function called by this ``doc_compare`` function.

Similarly, all these generated csv and png files are saved with their unique filenames in their respective 'csv' and 'png' folders and on the other hand, the generated pdf report is saved in 'pdf' folder.

The first part of the pdf report's filename takes the default name specified by the keyword parameter, `doc_name`, e.g. doc_name="comparison" while the second part is simply "report". Thus, the full file name as per default value is

    'comparison_report.pdf'.

These 'csv', 'png' and 'pdf' folders are basically the sub-folders to the main, master folder that assumes default folder's name - "comparison", which is defined by the same keyword parameter, e.g. `doc_name="comparison"` of ``doc_compare`` function.

Again, similar to ``doc`` function, this ``doc_compare`` function has a keyword parameter that defines the documentation reference number at the front page, i.e. `doc_num`, which its default value equals 1, e.g. doc_num="1".

Let's now document the comparison analysis between these four (4) UD composite such as the followings

    >>> carbon = Transtropic("Carbon", 250, 25, 20, 10, .28)
    >>> fiberglass = Isotropic("Fiberglass", 120, .29)
    >>> graphite = Transtropic("Graphite", 180, 20, 15, 10, .29)
    >>> epoxy = Isotropic("Epoxy", 2.8, .3)
    >>>
    >>> comp1 = HT(carbon, epoxy)
    >>> comp2 = HT(fiberglass, epoxy)
    >>> comp3 = HT(carbon, graphite)
    >>> comp4 = HT(fiberglass, graphite)
    >>>
    >>> doc_compare(comp1, comp2, comp3, comp4)
    Folder ./comparison/csv created
    ============= Carbon-Epoxy_fiber_tra_moduli.csv file saved! ==============
    ============= Carbon-Epoxy_matrix_iso_moduli.csv file saved! =============
    ================ Carbon-Epoxy_eff_moduli.csv file saved! =================
    =========== Fiberglass-Epoxy_phases_iso_moduli.csv file saved! ===========
    ============== Fiberglass-Epoxy_eff_moduli.csv file saved! ===============
    =========== Carbon-Graphite_phases_tra_moduli.csv file saved! ============
    =============== Carbon-Graphite_eff_moduli.csv file saved! ===============
    ========== Fiberglass-Graphite_fiber_iso_moduli.csv file saved! ==========
    ========= Fiberglass-Graphite_matrix_tra_moduli.csv file saved! ==========
    ============= Fiberglass-Graphite_eff_moduli.csv file saved! =============
    Folder ./comparison/png created
    ==================== comparison_E1eff.png file saved! ====================
    ==================== comparison_E2eff.png file saved! ====================
    =================== comparison_G12eff.png file saved! ====================
    =================== comparison_G23eff.png file saved! ====================
    =================== comparison_K23eff.png file saved! ====================
    =================== comparison_v12eff.png file saved! ====================
    ==================== comparison_E1eff.csv file saved! ====================
    ==================== comparison_E2eff.csv file saved! ====================
    =================== comparison_G12eff.csv file saved! ====================
    =================== comparison_v12eff.csv file saved! ====================
    =================== comparison_G23eff.csv file saved! ====================
    =================== comparison_K23eff.csv file saved! ====================
    Folder ./comparison/pdf created
    --------------------------------------------------------------------------
                        comparison_report.pdf file saved!
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    >>>

The sample output of this ``doc_compare`` function can be found here where the [comparison analysis on four (4) UD composites](https://github.com/mbm74/Halpin-Tsai-Micromechanics/tree/60fb84d031693dd3a6976eb85b9133fbbbdb012e/doc_compare_output) as shown above were performed and documented.

Alright, let's document the same comparison analysis between these four (4) UD composite but this time, we are going to change the value of keyword parameter, `doc_name` to doc_name="comparison_micromechanics", and also, the document reference number using keyword parameter, `doc_num` to doc_num="Appx. 1", e.g.

        >>> doc_compare(comp1, comp2, comp3, comp4, doc_name="comparison_micromechanics", doc_num="Appx. 1")
        Folder ./comparison_micromechanics/csv created
        ============= Carbon-Epoxy_fiber_tra_moduli.csv file saved! ==============
        ============= Carbon-Epoxy_matrix_iso_moduli.csv file saved! =============
        ================ Carbon-Epoxy_eff_moduli.csv file saved! =================
        =========== Fiberglass-Epoxy_phases_iso_moduli.csv file saved! ===========
        ============== Fiberglass-Epoxy_eff_moduli.csv file saved! ===============
        =========== Carbon-Graphite_phases_tra_moduli.csv file saved! ============
        =============== Carbon-Graphite_eff_moduli.csv file saved! ===============
        ========== Fiberglass-Graphite_fiber_iso_moduli.csv file saved! ==========
        ========= Fiberglass-Graphite_matrix_tra_moduli.csv file saved! ==========
        ============= Fiberglass-Graphite_eff_moduli.csv file saved! =============
        Folder ./comparison_micromechanics/png created
        ============ comparison_micromechanics_E1eff.png file saved! =============
        ============ comparison_micromechanics_E2eff.png file saved! =============
        ============ comparison_micromechanics_G12eff.png file saved! ============
        ============ comparison_micromechanics_G23eff.png file saved! ============
        ============ comparison_micromechanics_K23eff.png file saved! ============
        ============ comparison_micromechanics_v12eff.png file saved! ============
        ============ comparison_micromechanics_E1eff.csv file saved! =============
        ============ comparison_micromechanics_E2eff.csv file saved! =============
        ============ comparison_micromechanics_G12eff.csv file saved! ============
        ============ comparison_micromechanics_v12eff.csv file saved! ============
        ============ comparison_micromechanics_G23eff.csv file saved! ============
        ============ comparison_micromechanics_K23eff.csv file saved! ============
        Folder ./comparison_micromechanics/pdf created
        --------------------------------------------------------------------------
                    comparison_micromechanics_report.pdf file saved!
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        >>>

Alright, that's all there is to it about this code!

<br>

<sup> # GO BACK TO [USAGE AND TUTORIALS](#usage-and-tutorials) </sup>

### DISCLOSURE

`project.py` is written and developed in OOP style. It is formatted according to `Black` and `cs50` style to ensure code quality. This python code is also documented properly with `docstrings` following the format and style taught in this cs50p course as well as a bit from google docstring format found [here](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html). Additionaly, it is also properly typehinted with type checker - `mypy` without any 'type: ignore ' comment.

As for unit testing with pytest fulfilling the minimum requirements of final project of cs50p and according to the codes in `test_project.py`, only the followings are unit tested:
- ```Isotropic class``` and all its methods
- ``display`` function with all its helper functions
- ``plot`` function with all its helper functions
- ``save`` function with all its helper functions

Finally, the code is licensed under the `MIT license`.

<sup> # GO BACK TO [CONTENTS](#contents) </sup>

### ACKNOWLEDGEMENT

Thank you to HarvardX for offering this online course for free although I'm on verified track but still, it has been a very knowledgable journey.

Thank you to Prof. David J Malan and his team for delivering such a magnificent course and its course contents and not to forget, special thank you to Mr. Rong Xin for his kind assistance and suggestions with regards to cs50 codespace. Last but not least, thank you for reading this README.md!

<sup> # GO BACK TO [CONTENTS](#contents) </sup>
