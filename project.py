from decimal import *
from tabulate import tabulate
from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.enums import XPos, YPos
from typing import Type, TypeVar
import matplotlib.pyplot as plt
import pprint as pp
import datetime
import csv
import re
import os


# Define type for class as to typehint 'cls' when using @classmethod
ISO = TypeVar("ISO", bound="Isotropic")  # Isotropic class (Isotropic material)
TI = TypeVar(
    "TI", bound="Transtropic"
)  # Transtropic class (Transversely Isotropic material)
H = TypeVar(
    "H", bound="HT"
)  # HT class (composte material with effective properties estimated by Halpin-Tsai)


class Isotropic:
    """
    Class that represents isotropic material where it elastic properties are constant
    in all directions. Thus, isotropic material can be described by its two independent
    elastic constants, which typically are Young's Modulus, E and Poissons's Ratio, v.
    Other elastic constants such as Shear Modulus, G and Bulk Modulus, k or more
    specifically in acccordance to our interest, Plane-strain Bulk Modulus, K can be
    derived from the two independent elastic properties using some isotropic formulae.

    Thus, when instantiating ```Isotropic``` object, three basic information are
    required to be defined and these are:
        1) Name,
        2) Young's Modulus, E, and
        3) Poisson's Ratio, v of isotropic material,
    and from the later two, the following dependent elastic constants of isotropic
    material can be determined by using some isotropic relations:
        4) Shear Modulus, G, and
        5) Plane Strain Bulk Modulus, K.

    All 5 items above are the instance attributes of Isotropic class and they will be
    needed to later, instantiate ```HT``` object that represents the UD composite
    material with its effective elastic properties predicted by Halpin-Tsai micromechanics
    method.

    There are 3 ways to instantiate ```Isotropic``` object:

    A) Using Constructor call, e.g.: fiber = Isotropic(fiberglass, 120, 0.29) where
            the first parameter is the name of isotropic material, second parameter
            represents the Young's modulus value of isotropic material and the third is
            the Poisson's ratio value of fiberglass isotropic material.

    B) Using ``get`` ``@classmethod``, e.g.: fiber = Isotropic.get() where user inputs
            process on the name, Young's modulus and Poisson's ratio of isotropic
            material will take place. This class method returns Constructor call that
            instantiates object.

    c) Using ``read`` ``@classmethod``, e.g. materials = Isotropic.read("isotropic.csv")
            where the argument represents the csv file that contains several
            isotropic material with data on each row as name, Young's modulus and
            Poisson's ratio which can then be used to simultaneously instantiate
            several ```Isotropic``` objects. Hence, this class method returns a tuple
            of ```Isotropic``` objects.

    Note: In most UD composite materials, matrix constituent material are usually
    considered isotropic material and the same can be said about fiberglass fiber
    constituent material.
    ...

    Attributes:

    `name`: str
        Name of isotropic material  (independent instance attribute)

    `youngs_modulus`: Decimal
        Young's modulus of isotropic material  (independent instance attribute)

    `poissons_ratio`: Decimal
        Poissons's ratio of isotropic material  (independent instance attribute)

    `shear_modulus`: Decimal
        Shear modulus of isotropic material  (dependent instance attribute)

    `pstrain_bulk_modulus`: Decimal
        Plane-strain bulk modulus of isotropic material  (dependent instance attribute)

    ...

    Methods:

    ``__init__``:
        '''Isotropic''' instance attrs initializer

    ``__str__``:
        String representation on the information about ```Isotropic``` object

    ``name``:
        ``@property``: get `name` value
        ``@name.setter``: set `name` value

    ``youngs_modulus``:
        ``@property``: get `youngs_modulus` value
        ``@youngs_modulus.setter``: set `youngs_modulus` value

    ``poissons_ratio``:
        ``@property``: get `poissons_ratio` value
        ``@poissons_ratio.setter``: set `poissons_ratio` value

    `shear_modulus`:
        ``@property``: get `shear_modulus` value
        ``@shear_modulus.setter``: set `shear_modulus` value

    ``pstrain_bulk_modulus:
        ``@property'': get `pstrain_bulk_modulus` value
        ``@pstrain_bulk_modulus.setter``: set `pstrain_bulk_modulus` value

    ``get``:
        ``@classmethod``: contains constructor that instantiates ```Isotropic``` object
            based on user inputs

    ``read``:
        ``@classmethod``: contains constructor that instantiates ```Isotropic``` object
            based on file inputs

    ``_is_valid``:
        ``@staticmethod``: validates user input on `name`

    ``_isvalid_constant``:
        ``@staticmethod``: validates user input on `youngs_modulus`

    ``_is valid_ratio``:
        ``@staticmethod``: validates user input on `poissons_ratio`

    ``_get_shear_constant``:
        Computes `shear_modulus` based on the values of instance attributes -
            `youngs_modulus` and `poissons_ratio` defined by user

    ``_get_pstrain_bulk_modulus``:
        Computes `pstrain_bulk_modulus` based on the values of instance attributes -
            `youngs_modulus` and `poissons_ratio` defined by user

    ``_get_info``:
        Returns a dict of ```Isotropic```'s instance attributes with key and value pairs
            for the purpose of preparing the data either to be displayed in table form
            on console screen or to be saved as csv format data
    """

    def __init__(
        self,
        name: str,
        youngs_modulus: Decimal,
        poissons_ratio: Decimal,
    ) -> None:
        """
        Initialize instance attributes of instantiated ```Isotropic``` object.

        : param `name`: name of isotropic material
        : type: str
        : param `youngs_modulus`: Young's modulus of isotropic material
        : type: Decimal
        : param `poissons_ratio`: Poisson's ratio of isotropic material
        : type: Decimal
        : rtype: None

        ...

        Instance attributes that depends on the parameters of __init__:

        `shear_modulus`: Decimal
            Shear modulus of isotropic material, which is defined by an instance method,
            ``get_shear_modulus`` that takes uses the values of instance attributes
            `youngs_modulus` and `poissons_ratio`.

        `pstrain_bulk_modulus`: Decimal
            Plane-strain bulk modulus of isotropic material, which is defined by an
            instance method, ``_get_pstrain_bulk_modulus`` that uses the values of
            instance attributes `youngs_modulus` and `poissons_ratio`.

        """
        self.name = name
        self.youngs_modulus = youngs_modulus
        self.poissons_ratio = poissons_ratio
        self.shear_modulus = Isotropic._get_shear_constant(self)
        self.pstrain_bulk_modulus = Isotropic._get_pstrain_bulk_modulus(self)

    def __str__(self) -> str:
        """Prints out the instance attributes and their respective values of the current
        ```Isotropic``` object of isotropic material.

        : return: a string representation of ```Isotropic``` instance attributes and
            their values
        : rtype: str

        Example: Assuming ```Isotropic``` object has already been instantiated and is
        simply referred to as obj

            >>> print(obj)
            obj.name: 'Fiberglass', obj.youngs_modulus: Decimal('50.000'), obj.poissons_
            ratio: Decimal('0.250'), obj.shear_modulus: Decimal('20.000'), obj.pstrain_b
            ulk_modulus: Decimal('40.000')
            >>>
        """
        return (
            f"\033[3mobj\033[0m.name: '{self.name}', "
            + "\033[3mobj\033[0m.youngs_modulus: "
            + f"Decimal('{self.youngs_modulus}'), "
            + "\033[3mobj\033[0m.poissons_ratio: "
            + f"Decimal('{self.poissons_ratio}'),"
            + "\033[3mobj\033[0m.shear_modulus: "
            + f"Decimal('{self.shear_modulus}'), "
            + "\033[3mobj\033[0m.pstrain_bulk_modulus: "
            + f"Decimal('{self.pstrain_bulk_modulus}')"
        )

    @property
    def name(self) -> str:
        """Get `name` value.

        : return: Name of isotropic material
        : rtype: str

        Examples:
            >>> obj.name
            'Fiberglass'
            >>>
            >>> print(obj.name)
            Fiberglass
            >>>
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Set `name` value with the help of ``_is_valid`` ``@staticmethod`` where `name`
        must consist of alphanumerical, underscore '_' and dashed '-' character only.

        : param `name`: Name of isotropic material
        : type: str
        : raise ValueError: If name is missing or invalid name when initialized or
            re-initialized
        : rtype: None

        Examples when ```Isotropic``` object is being instantiated or isotropic material
        is being created:
            >>> obj = Isotropic("", 50, 0.25)
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid name (alphanumerical, _ and - characters only
            )
            >>>
            >>> obj = Isotropic("Fiber & glass", 50, 0.25)
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid name (alphanumerical, _ and - characters only
            )
            >>>
            >>> obj = Isotropic("Fiberglass", 50, 0.25)
            >>>
            >>> obj.name
            'Fiberglass'
            >>>

        Examples when value is being re-initialized:
            >>> obj.name = ""
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid name (alphanumerical, _ and - characters only
            )
            >>>
            >>> obj.name = "Fiber&glass"
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid name (alphanumerical, _ and - characters only
            )
            >>>
            >>> obj.name = "Fiberglass"
            >>>
            >>> obj.name
            'Fiberglass'
            >>>
        """
        if not Isotropic._is_valid(name):
            raise ValueError(
                "Missing or invalid name (alphanumerical, _ and - characters only)"
            )
        self._name = name.strip()

    @property
    def youngs_modulus(self) -> Decimal:
        """Get `youngs_modulus` value.

        : return: The Young's modulus value (E, unit: GPa) of isotropic material
        : rtype: Decimal

        Examples:
            >>> obj.youngs_modulus
            Decimal('50.000')
            >>>
            >>> print(obj.youngs_modulus)
            50.000
            >>>
        """
        return self._youngs_modulus

    @youngs_modulus.setter
    def youngs_modulus(self, youngs_modulus: str | int | float | Decimal) -> None:
        """Set `youngs_modulus` value with the help of ``_isvalid_constant``
        ``@staticmethod`` where the value entered must consist of digits with single or
        no period character only and the value must be positive number.

        : param `youngs_modulus`: Young's modulus, value (E, unit: GPa) of
            isotropic material
        : type: str, int, float, Decimal
        : raise ValueError: If value is missing or invalid value when initialized or
            re-initialized
        : rtype: None

        Examples when ```Isotropic``` object is being instantiated or isotropic material
        is being created:
            >>> obj = Isotropic("Fiberglass", -100, 0.25)
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid Young's modulus value (E > 0)
            >>> obj = Isotropic("Fiberglass", "", "0.25")
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid Young's modulus value (E > 0)

        Examples when value is being re-initialized:
            >>> obj.youngs_modulus = ""
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid Young's modulus value (E > 0)
            >>>
            >>> obj.youngs_modulus = Decimal('-50')
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid Young's modulus value (E > 0)
            >>>
            >>> obj.youngs_modulus = 100.00
            >>>
            >>> obj.youngs_modulus
            Decimal('100.000')
            >>>
        """
        if not Isotropic._isvalid_constant(str(youngs_modulus)):
            raise ValueError("Missing or invalid Young's modulus value (E > 0)")
        self._youngs_modulus = Decimal(youngs_modulus).quantize(Decimal("1.000"))

    @property
    def poissons_ratio(self) -> Decimal:
        """Get `poissons_ratio` value.

        : return: The Poisson's ratio value (v, unit: unitless) of isotropic material
        : rtype: Decimal

        Examples:
            >>> obj.poissons_ratio
            Decimal('0.250')
            >>>
            >>> print(obj.poissons_ratio)
            0.250
            >>>
        """
        return self._poissons_ratio

    @poissons_ratio.setter
    def poissons_ratio(self, poissons_ratio: str | int | float | Decimal) -> None:
        """Set `poissons_ratio` value with the help of ``_isvalid_ratio``
        ``@staticmethod`` where the value must consist of digit and single or no period
        character only and the value has to be greater than 0 and less but equal to 0.5.

        : param `poissons_ratio`: Poisson's ratio value (v, unit: unitless) of isotropic
            material
        : type: str, int, float, Decimal
        : raise ValueError: If value is missing or invalid value when initialized or
            re-initialized
        : rtype: None

        Examples when value is being re-initialized:
            >>> obj.poissons_ratio = ""
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid Poisson's ratio value (0 < v < 0.5 )
            >>>
            >>> obj.poissons_ratio = Decimal('0.6')
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid Poisson's ratio value (0 < v < 0.5 )
            >>>
            >>> obj.poissons_ratio = .25
            >>>
            >>> obj.poissons_ratio
            Decimal('0.250')
            >>>
        """
        if not Isotropic._isvalid_ratio(str(poissons_ratio)):
            raise ValueError("Missing or invalid Poisson's ratio value (0 < v < 0.5 )")
        self._poissons_ratio = Decimal(poissons_ratio).quantize(Decimal("1.000"))

    @property
    def shear_modulus(self) -> Decimal:
        """Get `shear_modulus` value.

        : return: The shear modulus value (G, unit: GPa) of iisotropic material
        : rtype: Decimal

        Examples:
            >>> obj.shear_modulus
            Decimal('10.000')
            >>>
            >>> print(obj.shear_modulus)
            10.000
            >>>
        """
        return Isotropic._get_shear_constant(self)

    @shear_modulus.setter
    def shear_modulus(self, shear_modulus: str | int | float | Decimal) -> None:
        """Set `shear_modulus` value with the help of instance method
        ``_get_shear_constant`` that automatically calculates the values of shear modulus
        of isotropic materials based on the values of Young's modulus and Poisson's
        ratio.

        : param `shear_modulus`: Shear modulus value (G, unit: GPa) of isotropic
            material
        : type: str, int, float, Decimal
        : raise ValueError: If value is missing or is not equal to the values computed
            by ''@staticmethod'' of ''_get_shear_constant''
        : rtype: None

        Examples when value is being re-initialized:
            >>> obj.shear_modulus = ""
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing shear modulus value
            >>>
            >>> obj.shear_modulus = Decimal('10.00')
            Traceback (most recent call last):
                ...
                ...
            ValueError: Violated shear modulus value based on isotropic formula
            >>>
            >>> obj.shear_modulus = 20
            >>>
            >>> obj.shear_modulus
            Decimal('20.000')
            >>>
        """
        if not Isotropic._isvalid_constant(str(shear_modulus)):
            raise ValueError("Missing or invalid shear_modulus value (G > 0)")
        if Decimal(shear_modulus).quantize(
            Decimal("1.000")
        ) != Isotropic._get_shear_constant(self):
            raise ValueError("Violated shear modulus value based on isotropic formula")
        self._shear_modulus = Decimal(shear_modulus).quantize(Decimal("1.000"))

    @property
    def pstrain_bulk_modulus(self) -> Decimal:
        """Get `pstrain_bulk_modulus` value.

        : return: The plane-strain bulk modulus value (K, unit: GPa) of isotropic
            material
        : rtype: Decimal

        Examples:
            >>> obj.pstrain_bulk_modulus
            Decimal('40.000')
            >>>
            >>> print(obj.pstrain_bulk_modulus)
            40.000
            >>>
        """
        return Isotropic._get_pstrain_bulk_modulus(self)

    @pstrain_bulk_modulus.setter
    def pstrain_bulk_modulus(
        self, pstrain_bulk_modulus: str | int | float | Decimal
    ) -> None:
        """Set `pstrain_bulk_modulus` value with the help of `_get_pstrain_bulk_modulus`
        ``@staticmethod`` of that automatically calculates the value of plane-strain
        bulk modulus based on the values of Young's modulus and Poisson's ratio

        : param `pstrain_bulk_modulus`: Plane-strain bulk modulus value (K, unit: GPa)
            of isotropic material
        : type: str, int, float, Decimal
        : raise ValueError: If value is missing or is not equal to the values computed
            by ''@staticmethod'' of ''_get_shear_constant''
        : rtype: None

        Examples when value is being re-initialized:
            >>> obj.pstrain_bulk_modulus = ""
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing plane-strain bulk modulus value
            >>>
            >>> obj.pstrain_bulk_modulus = Decimal('25.0')
            Traceback (most recent call last):
                ...
                ...
            ValueError: Violated plane-strain bulk modulus value based on isotropic formula
            >>>
            >>> obj.poissons_ratio = 40
            >>>
            >>> obj.poissons_ratio
            Decimal('40.000')
            >>>
        """
        if not Isotropic._isvalid_constant(str(pstrain_bulk_modulus)):
            raise ValueError(
                "Missing or invalid plane-strain bulk modulus value (K > 0)"
            )
        if Decimal(pstrain_bulk_modulus).quantize(
            Decimal("1.000")
        ) != Isotropic._get_pstrain_bulk_modulus(self):
            raise ValueError(
                "Violated plane-strain bulk modulus value based on isotropic formula"
            )
        self._pstrain_bulk_modulus = Decimal(pstrain_bulk_modulus).quantize(
            Decimal("1.000")
        )

    @classmethod
    def get(cls: Type[ISO]) -> ISO:
        """
        A ``@classmethod`` that triggers the instantiation of ```Isotropic``` object
        through its Constructor after all the appropriate values for ```Isotropic```'s
        instance attributes namely, `name`, `youngs_modulus` and `poissons_ratio`, have
        been defined by user interactively through ``input`` function and internally
        validated with the help of several ``@staticmethod``s , e.g. ``_is_valid``,
        ``_isvalid_constant`` and ``_isvalid_ratio`` method.

        In this ``@classmethod``, if the any of the value entered by user is missing or
        invalid, ValueError is raised but is caught by the ``try`` and ``except`` block
        and together with ``while True`` statement, the method keeps prompting the user
        until correct and valid value is entered.

        : return: cls(phase_name, phase_youngs_modulus, phase_poissons_ratio) which
            instantiates ```Isotropic``` object
        : rtype: ```Isotropic``` object

        Examples when ```Isotropic``` object is being instantiated or isotropic material
        is being created:
            >>> obj = Isotropic.get()
            Constituent:                            # Invalid due to missing value
            Constituent: Fiber&glass                # Invalid due to '&' character
            Constituent: "Fiberglass"               # Invalid due to " " characters
            Constituent: Fiberglass                 # Valid
            Young's modulus, E (GPa):               # Invalid due to missin value
            Young's modulus, E (GPa): Decimal('50') # Invalid since input is not digit
            Young's modulus, E (GPa): 50            # Valid
            Poissons' ratio, v:                     # Invalid due to missing value
            Poissons' ratio, v: 0.6                 # Invalid due to greater than 0.5
            Poissons' ratio, v: -0.25               # Invalid due to -ve number
            Poissons' ratio, v: .25                 # Valid
            >>>
            >>> print(obj)
            obj.name: 'Fiberglass', obj.youngs_modulus: Decimal('50.000'), obj.shear_mod
            ulus: Decimal('20.000'), obj.poissons_ratio: Decimal('0.250')
            >>>
        """
        # Get and validate phase's name
        while True:
            try:
                phase_name: str = input(f"Constituent: ").strip()
                if Isotropic._is_valid(phase_name):  # when 'name' is allowed
                    break
                else:
                    raise ValueError
            except ValueError:
                pass
        # Get and validate phase's Young's modulus
        while True:
            try:
                phase_youngs_modulus: str = input(f"Young's modulus, E (GPa): ").strip()
                if Isotropic._isvalid_constant(phase_youngs_modulus):
                    break
                else:
                    raise ValueError
            except ValueError:
                pass
        # Get and validate phase's Poisson's ratio
        while True:
            try:
                phase_poissons_ratio: str = input(f"Poisson's ratio, v: ").strip()
                if Isotropic._isvalid_ratio(phase_poissons_ratio):
                    break
                else:
                    raise ValueError
            except ValueError:
                pass
        # Class constructor
        return cls(
            phase_name,
            Decimal(phase_youngs_modulus).quantize(Decimal("1.000")),
            Decimal(phase_poissons_ratio).quantize(Decimal("1.000")),
        )

    @classmethod
    def read(
        cls: Type[ISO],
        csv_file: str | None = None,
    ) -> list:
        """
        A ``@classmethod`` that instantiates single or several ```Isotropic``` objects
        after all appropriate values for i.e. `name`, `youngs_modulus` and
        `poissons_ratio`, have been obtained by reading some inputs from csv file and
        furthermore, are validated with the help of ``_is_valid``, ``_isvalid_constant``
        and ``_isvalid_ratio`` ``@staticmethod``s. Furthermore, this ''@classmethod''
        returns list of ```Isotropic``` object/s.

        : param `csv_file`: A csv format file that contains several isotropic materials
            with their name and 2 basic independent elastic constants. Note: csv file
            must have fieldnames
        : type: str
        : raise TypeError: if csv file is None, missing its filename extension or has
            not .csv filename extension
        : return: A list of ```Isotropic``` object/s.
        : rtype: list

        Examples when ```Isotropic``` objects are being instantiated or Isotropic
        materials are being created:
            >>> constituents = Isotropic.read()
            Traceback (most recent call last):
                ...
                ...
            TypeError: Expected the name of csv file including its file extension of '.c
            sv'
            >>>
            >>> constituents = Isotropic.read("isotropic")
            Traceback (most recent call last):
                ...
                ...
            TypeError: Filename missing its filename extension
            >>>
            >>> constituents = Isotropic.read("isotropic.py")
            Traceback (most recent call last):
                ...
                ...
            TypeError: Not a csv file
            >>>
            >>> constituents = Isotropic.read("isotropic.csv")
            >>>
            >>> constituents[0]._get_info()
            {'Constituent': 'Fiberglass', 'E\n(GPa)': Decimal('50.000'), 'G\n(GPa)': Dec
            imal ('20.000'), 'v': Decimal('0.250')}
            >>>
            >>> constituents[1]._get_info()
            {'Constituent': 'Epoxy', 'E\n(GPa)': Decimal('2.000'), 'G\n(GPa)': Decimal (
            '0.769'), 'v': Decimal('0.300')}
            >>>
        """
        # Check for TypeError
        if csv_file is None:
            raise TypeError(
                "Expected the name of csv file including its file extension of '.csv'"
            )
        else:
            filename: list = csv_file.split(".")
            if len(filename) == 1:
                raise TypeError("Filename missing its filename extension")
            if filename[1] != "csv":
                raise TypeError("Not a csv file")

        # Instantiate Isotropic object
        isotropic_constituents: list = []
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip headers
            for row in reader:
                name, youngs_modulus, poissons_ratio = row
                # Call constructor
                constituent: Isotropic = Isotropic(
                    name.strip(),
                    Decimal(youngs_modulus.strip()).quantize(Decimal("1.000")),
                    Decimal(poissons_ratio.strip()).quantize(Decimal("1.000")),
                )
                isotropic_constituents.append(constituent)
        # Return list of Isotropic objects
        return isotropic_constituents

    @staticmethod
    def _is_valid(name: str) -> bool:
        """
        A ``@staticmethod`` that validates user or file input when initializing or
        re-initializing the value of instance attribute - `name`. This method contains
        regex that allows only alphanumerical, underscore '_' and dash '-' character to
        form the name of isotropic material.

        This ``@staticmethod`` is also used by ```Transtropic``` class to validate the
        `name` argument of constructor call or `name` attribute of transversely
        isotropic material.

        : param `name`: the name for isotropic or transversely isotropic material
        : type: str
        : return: Either True boolean literal when input matches the regex or False
            boolean literal when no matches between input and regex.
        : rtype: bool
        """
        match = re.search(r"^[a-zA-Z0-9_\-]+$", name.strip())
        if match:
            return True
        else:
            return False

    @staticmethod
    def _isvalid_constant(elastic_modulus: str) -> bool:
        """
        A ``@staticmethod`` that validates user or file input when initializing and
        re-initializing instance attribute - `youngs_modulus` of isotropic material.
        This method contains regex that allows for digits and single or not dot only.
        It also checks for missing value.

        This ``@staticmethod`` is borrowed by ```Transtropic``` class to validate its
        arguments of Constructor call or  instance attributes `axial_youngs_modulus`,
        `transverse_youngs_modulus`, `axial_shear_modulus`, `transverse_shear_modulus`
        and `major_poissons_ratio` of transversely isotropic material.

        : param `elastic_modulus`: the elastic modulus value for isotropic and
            transversely isotropic material
        : type: str
        : return: Either True boolean literal when input matches the regex or False
            boolean literal when no match between input and regex.
        : rtype: bool
        """
        if not elastic_modulus:
            return False
        match = re.search(r"^([0-9]*[.]?[0-9]*$)", elastic_modulus.strip())
        if match:
            if float(elastic_modulus) == 0.0:
                return False
            return True
        else:
            return False

    @staticmethod
    def _isvalid_ratio(constant: str) -> bool:
        """
        A ``@staticmethod`` that validates user or file input when initializing or
        re-initializing instance attribute - `poissons_ratio` of isotropic material.
        This method contains regex that allows for digits and single or no dot only.
        On top of it, this method checks for the missing value and any value that
        exceeds 0.5.

        This ``@staticmethod`` is also borrowed by ```Transtropic``` class to valid its
        arguments of Constructor call or its instance attribute `major_poissons_ratio`
        of transversely isotropic material.

        : param `constant`: Poisson's ratio value of isotropic and transversely
            isotropic material.
        : type: str
        : return: Either True boolean literal when input matches the regex or False
            boolean literal when no match between input and regex.
        : rtype: bool
        """
        if not constant:
            return False
        match = re.search(r"^([0-9]*[.]?[0-9]*$)", constant.strip())
        if match:
            if float(constant) > 0.5:
                return False
            if float(constant) == 0.0:
                return False
            return True
        else:
            return False

    def _get_shear_constant(self) -> Decimal:
        """
        This instance method automatically computes the shear elastic modulus, i.e.
        when initializing or re-initializing the value for instance attribute -
        `shear_modulus`, based on the isotropic relation formula that takes into account
        the values of Young's modulus and Poisson's ratio of isotropic elastic material,
        which are obtained from other instance attributes - `youngs_modulus` and
        `poissons_ratio` respectively.

        : return: Computed value of `shear_modulus` of isotropic material
        : rtype: Decimal
        """
        return (
            self.youngs_modulus / (Decimal("2") * (Decimal("1") + self.poissons_ratio))
        ).quantize(Decimal("1.000"))

    def _get_pstrain_bulk_modulus(self) -> Decimal:
        """
        This instance method automatically computes the plane-strain bulk modulus,
        i.e. for instance attribute - `pstrain_bulk_modulus` based on the
        isotropic relation formula that takes into account the Young's modulus and
        Poisson's ratio of isotropic elastic material, which are obtained from instance
        attributes - `youngs_modulus` and `poissons_ratio` respectively.

        : return: Computed value of plane-strain bulk of isotropic material
        : rtype: Decimal
        """
        return (
            self.youngs_modulus
            / (
                Decimal("2")
                * (Decimal("1") + self.poissons_ratio)
                * (Decimal("1") - (Decimal("2") * self.poissons_ratio))
            )
        ).quantize(Decimal("1.000"))

    def _get_info(self) -> dict:
        """Return information on its instance attributes (with different names) and
        their values as key-value pairs in dict format, which will be used by external
        ``display``, ``compare``, ``save``, ``save_compare`` and other external
        functions for representing data in table format form and csv format form.

        : return: Key and value pairs of information on current ```Isotropic``` object
        : rtype: dict
        """
        return {
            "Constituent": self.name,
            "Young's\nModulus,\nE (GPa)": self.youngs_modulus,
            "Poisson's\nRatio,\nv": self.poissons_ratio,
            "Shear\nModulus,\nG (GPa)": self.shear_modulus,
            "Plane-strain\nBulk Modulus,\nK (GPa)": self.pstrain_bulk_modulus,
        }


class Transtropic:
    """
    Class that represents transversely isotropic material where it has one unique axis
    of symmetry, known as the principal axis, and is isotropic in the plane perpendicular
    to this axis. Thus, this class of material has different properties in the
    direction of the principal axis compared to the properties in the plane perpendicular
    to it. Such material then has at least five independent elastic constants to fully
    describe its transversely isotropic behavior.

    Therefore, when instantiating the ```Transtropic``` object here, the name of
    transversely isotropic materials with five (5) independent elastic constants are
    required to be defined, e.g.:
        1) Name,
        2) Axial Young's Modulus, E1,
        3) Transverse Young's Modulus, E2,
        4) Axial Shear Modulus, G12,
        5) Transverse Shear Modulus, G23,
        6) Major Poisson's Ratio, v12, and

    and through some transverse-isotropic relation, the additional following property
    is defined:
        7) Plane-strain bulk modulus, K23.

    All 7 items above are the instance attributes of Isotropic class and they will be
    needed to later, instantiate ```HT``` object that represents the UD composite
    material with its effective elastic properties predicted by Halpin-Tsai micromechanics
    method.

    There are 3 ways to instantiate ```Transtropic``` object:

    A) Using Constructor call, e.g.: carbon = Transtropic(Carbon, 250, 25, 20, 10, 0.28)
            where the first parameter is the name of our transversely isotropic material,
            second parameter represents the value of axial Young's modulus, the third is
            the value of transverse Young's modulus, the fourth is the value of axial
            shear modulus, the fifth value is for transverse shear modulus and the last
            parameter represents the value of major Poisson's ratio of our transversely
            isotropic material.

    B) Using ``get`` ``@classmethod``, e.g.: carbon = Transtropic.get() where user inputs
            process to get the name of transversely isotropic material and its values on
            axial Young's modulus, transverse Young's modulus, axial shear modulus,
            transverse shear modulus and major Poisson's ratio will take place. This
            return Constructor call to instantiate an object.

    c) Using ``read`` ``@classmethod``, e.g. materials = Transtropic.read("transtropic.csv")
            where the parameter represents the csv file that contains data of single or
            several transversely isotropic material, i.e. the name and the five (5) basic
            elastic independent properties, which can then be used to simultaneously
            instantiate several ```Transtropic``` objects. It returns a list of
            ```Transtropic``` object.

    Note that in most UD composite materials, carbon- or graphite-based fiber material
    is usually considered transversely isotropic material and hence, this justifies the
    need to have ```Transtropic``` class for UD composite micromechanics analysis.
    ...

    Attributes:

    `name`: str
        Name of transversely isotropic material

    `axial_youngs_modulus`: Decimal
        Axial Young's modulus of transversely isotropic material

    `transverse_youngs_modulus`: Decimal
        Transverse Young's modulus of transversely isotropic material

    `axial_shear_modulus`: Decimal
        Axial shear modulus of transversely isotropic material

    `transverse_shear_modulus`: Decimal
        Transverse shear modulus of transversely isotropic material

    `major_poissons_ratio`: Decimal
        Major Poissons's ratio of transversely isotropic material

    `pstrain_bulk_modulus`: Decimal
        Plane-strain bulk modulus of transversely isotropic material

    ...

    Methods:

    ``__init__``:
        '''Transtropic''' instance attrs initializer

    ``__str__``:
        String representation of '''Transtropic''' object

    ``_get_info``:
        Returns a dict of ```Isotropic```'s instance attributes with key and value pairs
            for the purpose of preparing the data either to be displayed in table form
            on console screen or to be saved as csv format data

    ``name``:
        ``@property``: get `name` value
        ``@name.setter``: set `name` value

    ``axial_youngs_modulus``:
        ``@property``: get `axial_youngs_modulus` value
        ``@axial_youngs_modulus.setter``: set `axial_youngs_modulus` value

    ``transverse_youngs_modulus``:
        ``@property``: get `transverse_youngs_modulus` value
        ``@transverse_youngs_modulus.setter``: set `transverse_youngs_modulus` value

    ``axial_shear_modulus``:
        ``@property``: get `axial_shear_modulus` value
        ``@axial_shear_modulus.setter``: set `transverse_shear_modulus` value

    ``transverse_shear_modulus``:
        ``@property``: get `transverse_shear_modulus` value
        ``@transverse_shear_modulus.setter``: set `transverse_shear_modulus` value

    ``major_poissons_ratio:
        ``@property``: get `major_poissons_ratio` value
        ``@major_poissons_ratio.setter``: set `major_poissons_ratio` value

    ``pstrain_bulk_modulus``:
        ``@property``: get `pstrain_bulk_modulus` value
        ``@pstrain_bulk_modulus.setter``: set `pstrain_bulk_modulus` value

    ``get``:
        ''@classmethod``: constructor that instantiates ```Transtropic``` object based
            on user inputs

    ``read``:
        ``@classmethod``: constructor that instantiates ```Transtropic``` object based
            on file inputs

    ``_get_pstrain_bulk_modulus``:
        Computes `pstrain_bulk_modulus` based on values of other
            instance attributes - `axial_youngs_modulus`, `transverse_youngs_modulus`,
            `transverse_shear_modulus` and `major_poissons_ratio`

    ``_get_info``:
        Returns a dict of ```Isotropic```'s instance attributes with key and value pairs
            for the purpose of preparing the data either to be displayed in table form
            on console screen or to be saved as csv format data
    ....

    Instance @staticmethods borrowed from ```Isotropic``` class


    ``Isotropic._is_valid``:
        ``@staticmethod``: validates input on `name`

    ``Isotropic._isvalid_constant``:
        ``@staticmethod``: validates user input on `axial_youngs_modulus`,
        `transverse_youngs_modulus`, `axial_shear_modulus`, `transverse_shear_modulus`

    ``Isotropic._isvalid_ratio``:
        ``@staticmethod``: validates user input on `major_poissons_ratio`

    """

    def __init__(
        self,
        name: str,
        axial_youngs_modulus: Decimal,
        transverse_youngs_modulus: Decimal,
        axial_shear_modulus: Decimal,
        transverse_shear_modulus: Decimal,
        major_poissons_ratio: Decimal,
    ) -> None:
        """
        Initialize instance attributes of instantiated ```Transtropic`` object.

        : param `name`: Name of transversely isotropic material
        : type: str
        : param `axial_youngs_modulus`: Value of axial Young's modulus of transversely
            isotropic material
        : type: Decimal
        : param `transverse_youngs_modulus`: Value of transverse Young's modulus of
            transversely isotropic material
        : type: Decimal
        : param `axial_shear_modulus`: Value of axial shear modulus of transversely
            isotropic material
        : type: Decimal
        : param `transverse_shear_modulus`: Value of transverse shear modulus of
            transversely isotropic material
        : type: Decimal
        : param `major_poissons_ratio`: Value of major Poisson's ratio of transversely
            isotropic material
        : type: Decimal

        ...

        Instance attribute that depends on the few parameters of __init__:

        `pstrain_bulk_modulus`: Decimal
            Plane-strain bulk modulus of transversely isotropic material defined by
            some transverse-isotropic formula. In this class, the value is defined by a
            ``_get_pstrain_bulk_modulus`` instance method that uses the values of
            other instance attributes, e.g. `axial_youngs_modulus`,
            `transverse_youngs_modulus`, `axial_shear_modulus`,
            `transverse_shear_modulus` and `major_poissons_ratio`.

        """
        self.name = name
        self.axial_youngs_modulus = axial_youngs_modulus
        self.transverse_youngs_modulus = transverse_youngs_modulus
        self.axial_shear_modulus = axial_shear_modulus
        self.transverse_shear_modulus = transverse_shear_modulus
        self.major_poissons_ratio = major_poissons_ratio
        self.pstrain_bulk_modulus = Transtropic._get_pstrain_bulk_modulus(self)

    def __str__(self) -> str:
        """Prints out instance attributes and their respective values of the current
        ```Transtropic``` object.

        : return: a string representation about the current ```Transtropic``` instance
            attributes and values
        : rtype: str

        Example:
            >>> print(obj)
            obj.name: 'Carbon', obj.axial_youngs_modulus: Decimal('250.000'), obj.transv
            erse_youngs_modulus: Decimal('25.000'), obj.axial_shear_modulus: Decimal('20
            .000'), obj.transverse_shear_modulus: Decimal('10.000'), obj.major_poissons_
            ratio: Decimal('0.280'), obj.pstrain_bulk_modulus: Decimal('17.023')
            >>>
        """
        return (
            f"\033[3mobj\033[0m.name: '{self.name}', "
            + "\033[3mobj\033[0m.axial_youngs_modulus: "
            + f"Decimal('{self.axial_youngs_modulus}'), "
            + "\033[3mobj\033[0m.transverse_youngs_modulus: "
            + f"Decimal('{self.transverse_youngs_modulus}'), "
            + "\033[3mobj\033[0m.axial_shear_modulus: "
            + f"Decimal('{self.axial_shear_modulus}'), "
            + "\033[3mobj\033[0m.transverse_shear_modulus: "
            + f"Decimal('{self.transverse_shear_modulus}'), "
            + "\033[3mobj\033[0m.major_poissons_ratio: "
            + f"Decimal('{self.major_poissons_ratio}'),"
            + "\033[3mobj\033[0m.pstrain_bulk_modulus: "
            + f"Decimal('{self.pstrain_bulk_modulus}')"
        )

    @property
    def name(self) -> str:
        """Get `name` value.

        : return: The name of transversely isotropic material
        : rtype: str

        Examples:
            >>> obj.name
            'Carbon'
            >>>
            >>> print(obj.name)
            Carbon
            >>>
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Set `name` value with the help of ``_is_valid`` ``@staticmethod`` borrowed
        from ```Isotropic``` class.

        : param `name`: Name of transversely isotropic material
        : type: str
        : raise ValueError: If name is missing or invalid name when initialized or
            re-initialized
        : rtype: None

        Examples when ```Transtropic``` is being instantiated: or transversely isotropic
        material is being created:
            >>> obj = Transtropic("", 250, 25, 20, 10, 0.28)
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid name (alphanumerical, _ and - characters only
            )
            >>>
            >>> obj = Transtropic("Car^^^bon", 250, 25, 20, 10, 0.28)
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid name (alphanumerical, _ and - characters only
            )
            >>>
            >>> obj = Transtropic("Carbon", 250, 25, 20, 10, 0.28)
            >>>
            >>> obj.name
            'Carbon'
            >>>

        Examples when value is being re-initialized:
            >>> obj.name = ""
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid name (alphanumerical, _ and - characters only
            )
            >>>
            >>> obj.name = "Car^^^bon"
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid name (alphanumerical, _ and - characters only
            )
            >>>
            >>> obj.name = "Carbon"
            >>>
            >>> obj.name
            'Carbon'
            >>>
        """
        if not Isotropic._is_valid(name):  # Use Isotropic @staticmethod
            raise ValueError(
                "Missing or invalid name (alphanumerical, _ and - characters only)"
            )
        self._name = name.strip()

    @property
    def axial_youngs_modulus(self) -> Decimal:
        """Get `axial_youngs_modulus` value.

        : return: Value of axial Young's modulus value (E1, unit: GPa) of transversely
            isotropic material
        : rtype: Decimal

        Examples:
            >>> obj.axial_youngs_modulus
            Decimal('250.000')
            >>>
            >>> print(obj.axial_youngs_modulus)
            250.000
            >>>
        """
        return self._axial_youngs_modulus

    @axial_youngs_modulus.setter
    def axial_youngs_modulus(
        self, axial_youngs_modulus: str | int | float | Decimal
    ) -> None:
        """Set `axial_youngs_modulus` value with the help of ``_isvalid_constant``
        ``@staticmethod`` borrowed from ```Isotropic``` class.

        : param `axial_youngs_modulus`: Value of axial Young's modulus, value (E1, unit:
            GPa) of transversely isotropic material
        : type: str, int, float, Decimal
        : raise ValueError: If value is missing or invalid value when initialized or
            re-initialized
        : rtype: None

        Examples when ```Transtropic``` object is being instantiated or transversely
        isotropic material is being created:
            >>> obj = Transtropic("Carbon", "", 25, 20, 10, 0.28)
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid axial Young's modulus value (E1 > 0)
            )
            >>>
            >>> obj = Transtropic("Car^^^bon", -250, 25, 20, 10, 0.28)
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid axial Young's modulus value (E1 > 0)
            )
            >>>
            >>> obj = Transtropic("Carbon", 250, 25, 20, 10, 0.28)
            >>>
            >>> obj.axial_youngs_modulus
            Decimal('250.000')
            >>>

        Examples when its value is being re-initialized:
            >>> obj.axial_youngs_modulus = ""
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid axial Young's modulus value (E1 > 0)
            )
            >>> obj.axial_youngs_modulus = Decimal("-250")
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid axial Young's modulus value (E1 > 0)
            )
            >>>
            >>> obj.axial_youngs_modulus = Decimal("250")
            >>>
            >>> print(obj.axial_youngs_modulus)
            250.000
            >>>
        """
        if not Isotropic._isvalid_constant(
            str(axial_youngs_modulus)
        ):  # Use Isotropic @classmethod
            raise ValueError("Missing or invalid axial Young's modulus value (E1 > 0)")
        self._axial_youngs_modulus = Decimal(axial_youngs_modulus).quantize(
            Decimal("1.000")
        )

    @property
    def transverse_youngs_modulus(self) -> Decimal:
        """Get `transverse_youngs_modulus` value.

        : return: Value of transverse Young's modulus value (E2, unit: GPa) of
            transversely isotropic material
        : rtype: Decimal

        Examples:
            >>> obj.transverse_youngs_modulus
            Decimal('25.000')
            >>>
            >>> print(obj.transverse_youngs_modulus)
            25.000
            >>>
        """
        return self._transverse_youngs_modulus

    @transverse_youngs_modulus.setter
    def transverse_youngs_modulus(
        self, transverse_youngs_modulus: str | int | float | Decimal
    ) -> None:
        """Set `transverse_youngs_modulus` value with the help of ``_isvalid_constant``
        ``@staticmethod`` borrowed from ```Isotropic``` class.

        : param `transverse_youngs_modulus`: Value of transverse Young's modulus, value
            (E2, unit: GPa) of transversely isotropic material
        : type: str, int, float, Decimal
        : raise ValueError: If value is missing or invalid value when initialized or
            re-initialized
        : rtype: None

        Examples when ```Transtropic``` object is being instantiated or transversely
        isotropic material is being created:
            >>> obj = Transtropic("Carbon", 250, "", 20, 10, 0.28)
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid transverse Young's modulus value (E2 > 0)
            >>>
            >>> obj = Transtropic("Carbon", 250, -25, 20, 10, 0.28)
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid transverse Young's modulus value (E2 > 0)
            >>>
            >>> obj = Transtropic("Carbon", 250, Decimal('25'), 20, 10, 0.28)
            >>>
            >>> obj.tranverse_youngs_modulus
            Decimal('25.000')
            >>>

        Examples when value is being re-initialized:
            >>> obj.transverse_youngs_modulus = ""
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid transverse Young's modulus value (E2 > 0)
            >>>
            >>> obj.transverse_youngs_modulus = Decimal("-25")
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid transverse Young's modulus value (E2 > 0)
            >>>
            >>> obj.transverse_youngs_modulus = 25.0
            >>>
            >>> print(obj.transverse_youngs_modulus)
            25.000
            >>>
        """
        if not Isotropic._isvalid_constant(
            str(transverse_youngs_modulus)
        ):  # Use Isotropic @classmethod
            raise ValueError(
                "Missing or invalid transverse Young's modulus value (E2 > 0)"
            )
        self._transverse_youngs_modulus = Decimal(transverse_youngs_modulus).quantize(
            Decimal("1.000")
        )

    @property
    def axial_shear_modulus(self) -> Decimal:
        """Get `axial_shear_modulus` value.

        : return: Value of axial shear modulus value (G12, unit: GPa) of transversely
            isotropic material
        : rtype: Decimal

        Examples:
            >>> obj.axial_shear_modulus
            Decimal('20.000')
            >>>
            >>> print(obj.axial_shear_modulus)
            20.000
            >>>
        """
        return self._axial_shear_modulus

    @axial_shear_modulus.setter
    def axial_shear_modulus(
        self, axial_shear_modulus: str | int | float | Decimal
    ) -> None:
        """Set `axial_shear_modulus` value with the help of `_isvalid_constant`
        ``@staticmethod`` borrowed from ```Isotropic``` class.

        : param `axial_shear_modulus`: Value of axial shear modulus, value (G12, unit:
            GPa) of transversely isotropic material
        : type: str, int, float, Decimal
        : raise ValueError: If value is missing or invalid value when initialized or
            re-initialized
        : rtype: None

        Examples when ```Transtropic``` object is being instantiated or transversely
        isotropic material is being created:
            >>> obj = Transtropic("Carbon", 250, 25, "", 10, 0.28)
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid axial shear modulus value (G12 > 0)
            )
            >>>
            >>> obj = Transtropic("Carbon", 250, 25, -20, 10, 0.28)
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid axial shear modulus value (G12 > 0)
            )
            >>>
            >>> obj = Transtropic("Carbon", 250, 25, 20, 10, 0.28)
            >>>
            >>> obj.axial_shear_modulus
            Decimal('20.000')
            >>>

        Examples when value is being re-initialized:
            >>> obj.axial_shear_modulus = ""
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid axial shear modulus value (G12 > 0)
            )
            >>> obj.axial_shear_modulus = Decimal("-20")
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid axial shear modulus value (G12 > 0)
            )
            >>>
            >>> obj.axial_shear_modulus = Decimal("20")
            >>>
            >>> print(obj.axial_shear_modulus)
            20.000
            >>>
        """
        if not Isotropic._isvalid_constant(
            str(axial_shear_modulus)
        ):  # Use Isotropic @classmethod
            raise ValueError("Missing or invalid axial shear modulus value (G12 > 0)")
        self._axial_shear_modulus = Decimal(axial_shear_modulus).quantize(
            Decimal("1.000")
        )

    @property
    def transverse_shear_modulus(self) -> Decimal:
        """Get `transverse_shear_modulus` value.

        : return: Value of the transverse shear modulus value (G23, unit: GPa) of
            transversely isotropic material
        : rtype: Decimal

        Examples:
            >>> obj.transverse_shear_modulus
            Decimal('10.000')
            >>>
            >>> print(obj.transverse_shear_modulus)
            10.000
            >>>
        """
        return self._transverse_shear_modulus

    @transverse_shear_modulus.setter
    def transverse_shear_modulus(
        self, transverse_shear_modulus: str | int | float | Decimal
    ) -> None:
        """Set `transverse_shear_modulus` value with the help of ``_isvalid_constant``
        ``@staticmethod`` borrowed from ```Isotropic``` class.

        : param `transverse_shear_modulus`: Value of transverse shear modulus, value
            (G23, unit: GPa) of transversely isotropic material
        : type: str, int, float, Decimal
        : raise ValueError: If value is missing or invalid value when initialized or
            re-initialized
        : rtype: None

        Examples when ```Transtropic``` object is being instantiated or transversely
        isotropic material:
            >>> obj = Transtropic("Carbon", 250, 25, 20, "", 0.28)
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid transverse shear modulus value (G23 > 0)
            )
            >>>
            >>> obj = Transtropic("Carbon", 250, 25, 20, -10, 0.28)
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid transverse shear modulus value (G23 > 0)
            )
            >>>
            >>> obj = Transtropic("Carbon", 250, 25, 20, 10, 0.28)
            >>>
            >>> obj.transverse_shear_modulus
            Decimal('10.000')
            >>>

        Examples when value is being re-initialized:
            >>> obj.transverse_shear_modulus = ""
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid transverse shear modulus value (G23 > 0)
            )
            >>> obj.transverse_shear_modulus = Decimal("-10")
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid transverse shear modulus value (G23 > 0)
            )
            >>>
            >>> obj.transverse_shear_modulus = Decimal("10")
            >>>
            >>> print(obj.transverse_shear_modulus)
            10.000
            >>>
        """
        if not Isotropic._isvalid_constant(
            str(transverse_shear_modulus)
        ):  # Use Isotropic @classmethod
            raise ValueError(
                "Missing or invalid transverse shear modulus value (G23 > 0)"
            )
        self._transverse_shear_modulus = Decimal(transverse_shear_modulus).quantize(
            Decimal("1.000")
        )

    @property
    def major_poissons_ratio(self) -> Decimal:
        """Get `major_poissons_ratio` value.

        : return: Value of major Poisson's ratio value (v12, unit: unitless) of
            transversely isotropic material
        : rtype: Decimal

        Examples:
            >>> obj.major_poissons_ratio
            Decimal('0.280')
            >>>
            >>> print(obj.major_poissons_ratio)
            0.280
            >>>
        """
        return self._major_poissons_ratio

    @major_poissons_ratio.setter
    def major_poissons_ratio(
        self, major_poissons_ratio: str | int | float | Decimal
    ) -> None:
        """Set `major_poissons_ratio` value with the help of ``_isvalid_ratio``
        ``@staticmethod`` borrowed from ```Isotropic``` class.

        : param `major poissons_ratio`: Value of major Poisson's ratio value (v12, unit:
            unitless) of '''Transtropic''' object
        : type: str, int, float, Decimal
        : raise ValueError: If value is missing or invalid value when initialized or
            re-initialized
        : rtype: None

        Examples when ```Transtropic``` object is being instantiated or transversely
        isotropic material is being created:
            >>> obj = Transtropic("Carbon", 250, 25, 20, 10, "")
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid major Poisson's ratio value (0 < v < 0.5 )
            )
            >>>
            >>> obj = Transtropic("Carbon", 250, 25, 20, 10, -0.28)
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid major Poisson's ratio value (0 < v < 0.5 )
            )
            >>>
            >>> obj = Transtropic("Carbon", 250, 25, 20, 10, 0.28)
            >>>
            >>> obj.major_poissons_ratio
            Decimal('0.280')
            >>>

        Examples when value is being re-initialized:
            >>> obj.major_poissons_ratio = ""
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid major Poisson's ratio value (0 < v < 0.5 )
            )
            >>> obj.major_poissons_ratio = Decimal("-0.28")
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing or invalid major Poisson's ratio value (0 < v < 0.5 )
            )
            >>>
            >>> obj.major_poissons_ratio = Decimal("0.28")
            >>>
            >>> print(obj.major_poissons_ratio)
            0.280
        """
        if not Isotropic._isvalid_ratio(str(major_poissons_ratio)):
            raise ValueError(
                "Missing or invalid major Poisson's ratio value (0 < v < 0.5 )"
            )
        self._major_poissons_ratio = Decimal(major_poissons_ratio).quantize(
            Decimal("1.000")
        )

    @property
    def pstrain_bulk_modulus(self) -> Decimal:
        """Get `pstrain_bulk_modulus` value.

        : return: Value of plane-strain bulk modulus value (K23, unit: GPa) of
            transversely isotropic material
        : rtype: Decimal

        Examples:
            >>> obj.pstrain_bulk_modulus
            Decimal('17.023')
            >>>
            >>> print(obj.pstrain_bulk_modulus)
            17.023
            >>>
        """
        return Transtropic._get_pstrain_bulk_modulus(self)

    @pstrain_bulk_modulus.setter
    def pstrain_bulk_modulus(
        self, pstrain_bulk_modulus: str | int | float | Decimal
    ) -> None:
        """Set `pstrain_bulk_modulus` value with the help of instance method
        ``_get_pstrain_bulk_modulus`` that automatically calculates the value of
        plane-strain bulk modulus based on the values of axial and transvese Young's
        moduli, transverse shear modulus and major Poisson's ratio.

        : param `pstrain_bulk_modulus`: Value of plane-strain bulk modulus value (K23,
            unit: GPa) of transversely isotropic material
        : type: str, int, float, Decimal
        : raise ValueError: If value is missing or is not equal to the values computed
            by ''@staticmethod'' - ''_get_shear_constant''
        : rtype: None

        Examples when value is being re-initialized:
            >>> obj.pstrain_bulk_modulus = ""
            Traceback (most recent call last):
                ...
                ...
            ValueError: Missing plane-strain bulk modulus value
            )
            >>> obj.pstrain_bulk_modulus = 17.0
            Traceback (most recent call last):
                ...
                ...
            ValueError: Violated plane-strain bulk modulus value from transverse-isotropic formula
            )
            >>>
            >>> obj.pstrain_bulk_modulus = Decimal("17.023")
            >>>
            >>> print(obj.pstrain_bulk_modulus)
            17.023
        """
        if not pstrain_bulk_modulus:
            raise ValueError("Missing plane-strain bulk modulus value")
        if Decimal(pstrain_bulk_modulus).quantize(
            Decimal("1.000")
        ) != Transtropic._get_pstrain_bulk_modulus(self):
            raise ValueError(
                "Violated plane-strain bulk modulus value from transverse-isotropic "
                + "formula"
            )
        self._pstrain_bulk_modulus = Decimal(pstrain_bulk_modulus).quantize(
            Decimal("1.000")
        )

    @classmethod
    def get(cls: Type[TI]) -> TI:
        """
        A ``@classmethod`` that triggers the instantiation of ```Transtropic``` object
        through a Constructor call after all appropriate values for ```Transtropic```'s
        instance attributes, i.e. `name`, `axial_youngs_modulus`, `transverse_youngs_modulus`,
        `axial_shear_modulus`, `transverse_shear_modulus`, and `major_poissons_ratio`
        have been obtained from user interactively through 'input' function and
        internally validated with the help of several ``@staticmethod``s borrowed from
        ```Isotropic``` class, e.g. ``_is_valid``, ``_isvalid_constant`` and ``_isvalid_ratio``.

        In this ``@classmethod``, if any of the value entered by user is missing or
        invalid, ValueError is raised but is caught by the ``try`` and ``except`` block
        andtogether with ``while True`` statement, the method keeps prompting the user
        until correct and valid required value is entered.

        : return: cls(phase_name, phase_youngs_modulus, phase_poissons_ratio) which
            instantiates ```Transtropic``` object
        : rtype: ```Transtropic``` object

        Examples when '''Transtropic''' object is being instantiated or transversely
        isotropic material is being created:
            >>> obj = Transtropic.get()
            Constituent:                                    # Invalid due to missing value
            Constituent: Car^^^bon                          # Invalid due to invalid characters
            Constituent: "Carbon"                           # Invalid due to " " characters
            Constituent: Carbon                             # Valid name
            Axial Young's modulus, E1 (GPa):                # Invalid due to missing value
            Axial Young's modulus, E1 (GPa): Decimal('250') # Invalid due to non-digit characters
            Axial Young's modulus, E1 (GPa): 250            # Valid value
            Transverse Young's modulus, E2 (GPa):           # Invalid due to missing value
            Transverse Young's modulus, E2 (GPa): -50       # Invalid due to negative value
            Transverse Young's modulus, E2 (GPa): 50.00     # Valid value
            Axial shear modulus, G12 (GPa):                 # Invalid due to missing value
            Axial shear modulus, G12 (GPa): Decimal('20')   # Invalid due to non-digit characters
            Axial shear modulus, G12 (GPa): 20              # Valid value
            Transverse shear modulus, G23 (GPa):            # Invalid due to missing value
            Transverse shear modulus, G23 (GPa): -10        # Invalid due to negative value
            Transverse shear modulus, G23 (GPa): 10.0       # Valid value
            Major Poissons' ratio, v12:                     # Invalid due to missing value
            Major Poissons' ratio, v12: 0.6                 # Invalid due to value greater than 0.5
            Major Poissons' ratio, v12: -0.28               # Invalid due to negative value
            Major Poissons' ratio, v12: .28                 # Valid value
            >>>
            >>> print(obj)
            obj.name: 'Carbon', obj.axial_youngs_modulus: Decimal('250.000'), obj.transv
            erse_youngs_modulus: Decimal('25.000'), obj.axial_shear_modulus: Decimal('20
            .000'), obj.transverse_shear_modulus: Decimal('10.000'), obj.major_poissons_
            ratio: Decimal('0.280'), obj.pstrain_bulk_modulus: Decimal('17.023')
            >>>
        """
        # Get and validate phase's name
        while True:
            try:
                phase_name: str = input(f"Constituent: ").strip()
                if Isotropic._is_valid(phase_name):  # when 'name' is allowed
                    break
                else:
                    raise ValueError
            except ValueError:
                pass
        # Get and validate phase's axial Young's modulus
        while True:
            try:
                phase_axial_youngs_modulus: str = input(
                    f"Axial Young's modulus, E1 (GPa): "
                ).strip()
                if Isotropic._isvalid_constant(phase_axial_youngs_modulus):
                    break
                else:
                    raise ValueError
            except ValueError:
                pass
        # Get and validate phase's transverse Young's modulus
        while True:
            try:
                phase_transverse_youngs_modulus: str = input(
                    f"Transverse Young's modulus, E2 (GPa): "
                ).strip()
                if Isotropic._isvalid_constant(phase_transverse_youngs_modulus):
                    break
                else:
                    raise ValueError
            except ValueError:
                pass
        # Get and validate phase's axial shear modulus
        while True:
            try:
                phase_axial_shear_modulus: str = input(
                    f"Axial shear modulus, G12 (GPa): "
                ).strip()
                if Isotropic._isvalid_constant(phase_axial_shear_modulus):
                    break
                else:
                    raise ValueError
            except ValueError:
                pass
        # Get and validate phase's transverse shear modulus
        while True:
            try:
                phase_transverse_shear_modulus: str = input(
                    f"Transverse shear modulus, G23 (GPa): "
                ).strip()
                if Isotropic._isvalid_constant(phase_transverse_shear_modulus):
                    break
                else:
                    raise ValueError
            except ValueError:
                pass
        # Get and validate phase's major Poisson's ratio
        while True:
            try:
                phase_major_poissons_ratio: str = input(
                    f"Major Poisson's ratio, v12: "
                ).strip()
                if Isotropic._isvalid_ratio(phase_major_poissons_ratio):
                    break
                else:
                    raise ValueError
            except ValueError:
                pass
        # Class constructor
        return cls(
            phase_name,
            Decimal(phase_axial_youngs_modulus).quantize(Decimal("1.000")),
            Decimal(phase_transverse_youngs_modulus).quantize(Decimal("1.000")),
            Decimal(phase_axial_shear_modulus).quantize(Decimal("1.000")),
            Decimal(phase_transverse_shear_modulus).quantize(Decimal("1.000")),
            Decimal(phase_major_poissons_ratio).quantize(Decimal("1.000")),
        )

    @classmethod
    def read(
        cls: Type[TI],
        csv_file: str | None = None,
    ) -> list:
        """
        A ``@classmethod`` that instantiates one or more ```Transtropic``` objects
        through a Constructor after all appropriate values for the ```Transtropic```
        instance attributes, i.e. `name`, `axial_youngs_modulus`, `transverse_youngs_modulus`,
        `axial_shear_modulus`, `transverse_shear_modulus`, and `major_poissons_ratio`,
        have been obtained from the csv file and  validated with the help of ''@staticmethod''s,
        borrowed from ```Isotropic``` class e.g. ``_is_valid``, ``_isvalid_constant`` and
        ``_isvalid_ratio``. It returns a list of ```Transtropic``` object

        : param `csv_file`: The csv file that contains the name and 5 elastic constants
            of transversely isotropic materials. Note: the csv file must have fieldnames
        : type: str
        : raise TypeError: if csv file is None, missing its filename extension or has
            not .csv filename extension
        : return: A list of ```Transtropic``` objects
        : rtype: list

        Examples when ```Transtropic``` objects are being instantiated or transversely
        isotropic materials are created:
            >>> constituents = Transtropic.read()
            Traceback (most recent call last):
                ...
                ...
            TypeError: Expected the name of csv file including its file extension of '.c
            sv'
            >>>
            >>> constituents = Transtropic.read("transtropic")
            Traceback (most recent call last):
                ...
                ...
            TypeError: Filename missing its filename extension
            >>>
            >>> constituents = Transtropic.read("transtropic.py")
            Traceback (most recent call last):
                ...
                ...
            TypeError: Not a csv file
            >>>
            >>> constituents = Transtropic.read("transtropic.csv")
            >>> print(constituents[0])
            obj.name: 'Carbon', obj.axial_youngs_modulus: Decimal('250.000'), obj.transv
            erse_youngs_modulus: Decimal('25.000'), obj.axial_shear_modulus: Decimal('20
            .000'), obj.transverse_shear_modulus: Decimal('10.000'), obj.major_poissons_
            ratio: Decimal('0.280'),obj.pstrain_bulk_modulus: Decimal('17.023')
            >>> constituents[1]._get_info()
            {'Constituent': 'Graphite', "Axial\nYoung's\nModulus,\nE1 (GPa)": Decimal('2
            00.000'), "Transverse\nYoung's\nModulus,\nE2 (GPa)": Decimal('20.000'), 'Axi
            al\nShear\nModulus,\nG12 (GPa)': Decimal('18.000'), 'Transverse\nShear\nModu
            lus,\nG23 (GPa)': Decimal('8.000'), "Major\nPoisson's\nRatio,\nv12": Decimal
            ('0.280'), 'Plane-strain\nBulk\nModulus,\nK23 (GPa)': Decimal('13.618')}
            >>>
        """
        # Check for TypeError
        if csv_file is None:
            raise TypeError(
                "Expected the name of csv file including its file extension of '.csv'"
            )
        else:
            filename: list = csv_file.split(".")
            if len(filename) == 1:
                raise TypeError("Filename missing its filename extension")
            if filename[1] != "csv":
                raise TypeError("Not a csv file")
        # Instantiate Isotropic object
        transtropic_constituents: list = []
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip headers
            for row in reader:
                (
                    phase_name,
                    phase_axial_youngs_modulus,
                    phase_transverse_youngs_modulus,
                    phase_axial_shear_modulus,
                    phase_transverse_shear_modulus,
                    phase_major_poissons_ratio,
                ) = row
                # Call constructor
                transtropic_constituent: Transtropic = Transtropic(
                    phase_name.strip(),
                    Decimal(phase_axial_youngs_modulus.strip()).quantize(
                        Decimal("1.000")
                    ),
                    Decimal(phase_transverse_youngs_modulus.strip()).quantize(
                        Decimal("1.000")
                    ),
                    Decimal(phase_axial_shear_modulus.strip()).quantize(
                        Decimal("1.000")
                    ),
                    Decimal(phase_transverse_shear_modulus.strip()).quantize(
                        Decimal("1.000")
                    ),
                    Decimal(phase_major_poissons_ratio.strip()).quantize(
                        Decimal("1.000")
                    ),
                )
                transtropic_constituents.append(transtropic_constituent)
        # Return list of Isotropic objects
        return transtropic_constituents

    def _get_pstrain_bulk_modulus(self) -> Decimal:
        """
        This instance method automatically computes the plane-strain bulk modulus,
        i.e. for the initialization of instance attribute `pstrain_bulk_modulus` of
        ```Transtropic``` object based on some tranvserse-isotropic relation that takes
        into account both axial and transverse Young's moduli, transverse shear modulus
        and major Poisson's ratio of transversely isotropic.

        : return: Value of plane-strain_bulk_modulus of transversely isotropic
            material
        : rtype: Decimal
        """
        return (
            self.transverse_shear_modulus
            * self.transverse_youngs_modulus
            / (
                Decimal("4") * self.transverse_shear_modulus
                - self.transverse_youngs_modulus
                - (
                    Decimal("4")
                    * self.major_poissons_ratio**2
                    * self.transverse_shear_modulus
                    * self.transverse_youngs_modulus
                )
                / self.axial_youngs_modulus
            )
        ).quantize(Decimal("1.000"))

    def _get_info(self) -> dict:
        """Return information on its instance attributes (with different names) and
        their values as key-value pairs in dict format, which will be used by external
        ``display``, ``compare``, ``save``, ``save_compare`` and other external
        functions for representing data in table format form and csv format form.

        : return: pairs of key and value of information about the instantiated
            ```Transtropic``` object
        : rtype: dict
        """
        return {
            "Constituent": self.name,
            "Axial\nYoung's\nModulus,\nE1 (GPa)": self.axial_youngs_modulus,
            "Transverse\nYoung's\nModulus,\nE2 (GPa)": self.transverse_youngs_modulus,
            "Axial\nShear\nModulus,\nG12 (GPa)": self.axial_shear_modulus,
            "Transverse\nShear\nModulus,\nG23 (GPa)": self.transverse_shear_modulus,
            "Major\nPoisson's\nRatio,\nv12": self.major_poissons_ratio,
            "Plane-strain\nBulk\nModulus,\nK23 (GPa)": self.pstrain_bulk_modulus,
        }


class HT:
    """
    A class that represents unidirectional (UD) composite material made up from two
    constituents of fiber and matrix that can be isotropic and/or transversely isotropic
    material, i.e. ```Isotropic``` and/or ```Transtropic``` objects where its effective
    elastic properties were estimated by Halpin-Tsai micromechanics method. See figure
    below.


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

              b) in-plane view         c) out-of-plane view (transverse symmetry)

            Figure 1: Unidirectional advanced fiber reinforced matrix composites

    Note: Direction 1 refers to the principal axis of fiber, plane 1-2 refers to the
    in-plane ply layer of UD composite while plane 2-3 is the plane of symmetry or the
    transversely isotropic plane. For example:

    This UD composite is also a transversely isotropic material but somehow, cannot be
    instantiated or inherited from the ```Transtropic``` class as its effective elastic
    properties are not single-valued properties but rather multiple-valued since its
    properties, not only depend on the elastic properties of its constituents but also,
    on the content of fiber in the composite, which is known as the fiber volume fraction
    that ranges from 0, i.e. no fiber in a composite, way up to 1, i.e 100% fiber in a
    composite, with 0.01 increment. Thus, for every increment of fiber volume fraction,
    there is a unique value for every its effective elastic property. In this class,
    the value for its every elastic property is then represented by a tuple containing
    100 'Decimal' type values of effective elastic property following the 100 possible
    values of fiber volume fraction.

    Furthermore, this UD composite has effective transversely isotropic elastic
    properties estimated by Halpin-Tsai micromechanics method and thus, this justifies
    the need to have its own class of material rather than inheriting from ```Transtropic```
    class. Perhaps, in the future, there will be a different class of UD composite
    material where its effective elastic properties are defined by some other
    micromechanics methods.

    As explained before in the ```Transtropic``` class, there are five (5) independent
    elastic constants that fully describe the transversely isotropic characteristics of
    such material and from some transverse-isotropic relation, we can obtain one
    additional elastic constants. Hence, we have six (6) effective elastic properties
    that can be computed for this ```HT``` tranversely isotropic object. And as
    mentioned earlier, these effective elastic properties depends on the elastic
    properties of composite's constituents of fiber and matrix and also on the
    fiber volume fraction of a composite. With the name of UD composite and the
    micromechanics method used to estimate these effective elastic properties, this
    class has a total of nine (9) instance attributes plus two (2) class attributes
    such as the followings:

        1) Fiber material - `fiber`
        2) Matrix material - `matrix`
        3) Name of the composite - `name`
        4) Effective axial Young's moduli - `eff_axial_youngs_moduli`
        5) Effective transverse Young's moduli - `eff_transverse_youngs_moduli`
        6) Effective axial shear moduli - `eff_axial_shear_moduli`
        7) Effective transverse shear moduli - `eff_transverse_shear_moduli`
        8) Effective plane-strain bulk moduli - `eff_pstrain_bulk_moduli`
        9) Effective major Poisson's ratios - `eff_major_poissons_ratios`
        10) Micromechanics method of Halpin-Tsai - `micromechanics` (class attribute)
        11) Fiber volume fraction - `fiber_volfract` (class attribute)


    There is only one way to instantiate this ```HT``` object and this is achieved
    through Constructor call with two parameters of the fiber and matrix where these
    constituents are preiously instantiated from ```Isotropic``` and/or  ```Transtropic```
    objects. In the following example, we will first instantiate ```Transtropic```
    object for the fiber material of UD composite while the matrix material will be
    instantiated from ```Isotropic``` materials. With these two at hands, we will show
    how ```HT``` UD composite object can be instantiated.

    Example: Create UD composite material by instantiating ```HT``` object:
        >>>
        >>> fiber = Transtropic.get()  # Instantiating ```Transtropic``` object
        Constituent: Carbon
        Axial Young's modulus, E1 (GPa): 250
        Transverse Young's modulus, E2 (GPa): 25
        Axial shear modulus, G12 (GPa): 20
        Transverse shear modulus, G23 (GPa): 10
        Major Poissons' ratio, v12: .28
        >>>
        >>> matrix = Isotropic.get()  # Instantiating ```Isotropic``` object
        Constituent: Epoxy
        Young's modulus, E (GPa): 2.8
        Poissons' ratio, v: .3
        >>>
        >>> composite = HT(fiber, matrix)  # Instantiating ```HT``` object
        >>>
        >>> composite.name      # To confirm the presence of composite object
        'Carbon-Epoxy'
        >>>

    ...

    Attributes:

    `fiber_volfract`: tuple[Decimal]
        Fiber volume fraction in a composite ranging from 0 to 1 with 0.01 increment

    `micromechanics`: str
        Describe the Halpin-Tsai homogenization micromechanics method in estimating the
        UD composite's effective elastic properties

    `name`: str
        Name of the UD composite - a name combination of fiber and matrix with dash in
        between the two constituents's names.

    `fiber`: Isotropic | Transtropic
        Fiber material of a UD composite, which is represented by either ```Isotropic```
        or ```Transtropic``` object

    `matrix`: Isotropic | Transtropic
        Matrix material of a UD composite, which is represented by either
        ```Isotropic``` or ```Transtropic``` object

    `eff_axial_youngs_moduli`: tuple[Decimal]
        Effective axial Young's moduli estimated by Halpin-Tsai micromechanics method

    `eff_major_poissons_ratio`: tuple[Decimal]
        Effective major Poisson's ratios estimated by Halpin-Tsai micromechanics method

    `eff_axial_shear_moduli`: tuple[Decimal]
        Effective in-plane axial shear moduli estimated by Halpin-Tsai micromechanics
        method

    `eff_pstrain_bulk_moduli`: tuple[Decimal]
        Effective plane-strain bulk moduli estimated by Halpin-Tsai micromechanics
        method

    `eff_transverse_shear_moduli`: tuple[Decimal]
        Effective out-of-plane axial shear moduli estimated by Halpin-Tsai
        micromechanics method

    `eff_transverse_youngs_moduli`: tuple[Decimal]
        Effective in-plane transverse Young's moduli estimated by transversely-isotropic
        formual

    ...

    Instance method

    ``__init__``:
        Instance attributes of ```HT``` object initializer

    ``__str__``:
        string representation of HT object

    ``fiber_volfract``:
        ``@property``: Get the tuple of 100 ```Decimal``` values of fiber volume
        fraction starts from 0 and ends at 1 with 0.01 increment

    ``name``:
        ``@property``: Get the name of the composite

    ``fiber``:
        ``@property``: Get the fiber component of the composite, which can either be
        ```Isotropic``` or ```Transtropic``` object. As such, we can access to all its
        ```Isotropic``` or ```Transtropic``` instance attributes using dot notation
        twice

    ``matrix``:
        ``@property``: Get the matrix component of UD composite, which can either be
        ```Isotropic``` or ```Transtropic``` object. As such, we can access to all its
        ```Isotropic``` or ```Transtropic``` instance attributes using dot notation
        twice

    ``eff_axial_youngs_moduli``:
        ``@property``: Get the tuple of 100 ```Decimal``` values of effective axial
        Young's modulus of ```HT``` object

    ``eff_major_poissons_ratios``:
        ``@property``: Get the tuple of 100 ```Decimal``` values of effective major
        Poisson's ratio of ```HT``` object

    ``eff_axial_shear_moduli``:
        ``@property``: Get the tuple of 100 ```Decimal``` values of effective axial
        shear modulus of ```HT``` object

    ``eff_pstrain_bulk_moduli``:
        ``@property``: Get the tuple of 100 ```Decimal``` values of effective
        plane-strain bulk modulus of ```HT``` object

    ``eff_transverse_shear_moduli``:
        ``@property``: Get the tuple of 100 ```Decimal``` values of effective
        transverse shear moduli of ```HT``` object

    ``eff_transverse_youngs_moduli``:
        ''@property``: Get the tuple of 100 ```Decimal``` values of effective
        transverse Young's moduli of ```HT``` object

    ``E1eff``:
        Print to screen specific value or range of values of effective axial
        Young's modulus of ```HT``` object based on the respective value or range of
        values of fiber volume fraction defined by user

    ``E2eff``:
        Print to screen specific value or range of values of effective transverse
        Young's modulus of ```HT``` object based on the respective value or range of
        values of fiber volume fraction defined by user

    ``G12eff``:
        Print to screen specific value or range of values of effective axial shear
        modulus of ```HT``` object based on respective value or range of values of
        fiber volume fraction defined by user

    ``G23eff``:
        Print to screen specific value or range of values of effective transverse shear
        modulus of ```HT``` object based on the respective value or range of values of
        fiber volume fraction defined by user

    ``v12eff``:
        Print to screen specific value or range of values of effective major Poisson's
        ratio of ```HT``` object based on the respective value or range of values of
        fiber volume fraction defined by user

    ``K23eff``:
        Print to screen specific value or range of values of effective plane-strain bulk
        modulus of ```HT``` object based on the respective value or range of values of
        fiber volume fraction defined by user

    ``_estimate_E1eff``:
        Estimate the effective axial Young's modulus of composite using Halpin-Tsai
        micromechanics method based on the elastic properties of fiber and matrix and
        also, on the fiber volume fraction increments when instantiating ```HT``` object.

    ``_estimate_v12eff``:
        Estimate the effective major Poisson's ratio of composite using Halpin-Tsai
        micromechanics method based on the elastic properties of fiber and matrix and
        also, on the fiber volume fraction increments when instantiating ```HT``` object.

    ``_estimate_G12eff``:
        Estimate the effective axial shear modulus of composite using Halpin-Tsai
        micromechanics method based on the elastic properties of fiber and matrix and
        also, on the fiber volume fraction increments when instantiating ```HT``` object.

    ``_estimate_K23eff``:
        Estimate the effective plane-strain bulk mdulus of composite using Halpin-Tsai
        micromechanics method based on the elastic properties of fiber and matrix and
        also, on the fiber volume fraction increments when instantiating ```HT``` object.

    ``_estimate_G23eff``:
        Estimate the effective transverse shear modulus of composite using Halpin-Tsai
        micromechanics method based on the elastic properties of fiber and matrix and
        also, on the fiber volume fraction increments when instantiating ``HT`` object.

    ``_estimate_E2eff``:
        Estimate the effective transverse Young's modulud of composite using the
        transversely-isotropic formula that takes into account other effective elastic
        properties of UD composites.

    ``__get_index_num``:
        ``@staticmethod``: Returns the index number of specific fiber volume fraction
        value/s in the tuple of `fiber_volfract` instance attribute as requested by the
        user for the purpose of finding the respective values in the tuples of of
        specific effective elastic property of '''HT''' object requested by user
    """

    # Class attribute for micromechanics method
    _micromechanics = "Halpin-Tsai"

    # Class attribute for fiber volume fraction
    l: list = []
    for x in range(0, 101, 1):  # range start from 0 to 1 with 0.01 increment
        l.append(Decimal(str(x)) / Decimal("100"))
    _fiber_volfract: tuple = tuple(l)
    del l

    def __init__(
        self, fiber: Isotropic | Transtropic, matrix: Isotropic | Transtropic
    ) -> None:
        """
        Initialize instance attributes of ```HT``` object.

        : param `fiber`: the fiber material of UD composite
        : type: '''Isotropic``` | ```Transtropic```
        : param `matrix`: the matrix material of UD composite
        : type: ```Isotropic``` | ```Transtropic```
        : return: -
        : rtype: None

        ....

        Instance attributes that depends on the depends on the parameters of __init__:

        `name`: str
            Name of the UD composite that combines the names of `fiber.name` and
            `matrix.name` that makes up the UD composite.

        `eff_axial_youngs_moduli`: tuple[Decimal]
            The effective axial Young's moduli of UD composite estimated from Halpin-
            Tsai micromechanics method via ``_estimate_E1eff`` ``@staticmethod``

        ``eff_major_poissons_ratios``: tuple[Decimal]
            The effective major Poisson's ratios of UD composite estimated from Halpin-
            Tsai micromechanics method via ``_estimate_v12eff`` ``@staticmethod``

        ``eff_axial_shear_moduli``: tuple[Decimal]
            The effective axial shear moduli of UD composite estimated from Halpin-
            Tsai micromechanics method via ``_estimate_G12eff`` ``@staticmethod``

        ``eff_pstrain_bulk_moduli``: tuple[Decimal]
            The effective plane-strain bulk moduli of UD composite estimated from Halpin-
            Tsai micromechanics method via ``_estimate_K23eff`` ``@staticmethod``

        ``eff_transverse_shear_moduli``: tuple[Decimal]
            The effective transverse shear moduli of UD composite estimated from Halpin-
            Tsai micromechanics method via ``_estimate_G23eff`` ``@staticmethod``

        ``eff_transverse_youngs_moduli``: tuple[Decimal]
            The effective transverse Young's moduli of UD composite estimated from
            transversely-Isotropic formula via ``estimate_E2ef`` ``@staticmethod``
        """
        self._fiber = fiber
        self._matrix = matrix
        self._name: str = fiber.name + "-" + matrix.name
        self._eff_axial_youngs_moduli: tuple = HT._estimate_E1eff(self)
        self._eff_major_poissons_ratios: tuple = HT._estimate_v12eff(self)
        self._eff_axial_shear_moduli: tuple = HT._estimate_G12eff(self)
        self._eff_pstrain_bulk_moduli: tuple = HT._estimate_K23eff(self)
        self._eff_transverse_shear_moduli: tuple = HT._estimate_G23eff(self)
        self._eff_transverse_youngs_moduli: tuple = HT._estimate_E2eff(self)

    def __str__(self) -> str:
        """
        Print to screen basic information about current of UD composite with all the
        names of instance attributes of ```HT``` object.

        : return: string representation of '''HT''' object
        : rtype: str
        """
        return (
            f"{self.name} UD composite (```HT``` type) with instance attributes:\n"
            "   1) obj.name\n"
            "   2) obj.fiber\n"
            "   3) obj.matrix\n"
            "   4) obj.eff_axial_youngs_moduli\n"
            "   5) obj.eff_transverse_youngs_moduli\n"
            "   6) obj.eff_axial_shear_moduli\n"
            "   7) obj.eff_transverse_shear_moduli\n"
            "   8) obj.eff_pstrain_bulk_moduli\n"
            "   9) obj.eff_major_poissons_ratios\n"
            "   10) obj.micromechanics\n"
            "   11) obj.fiber_volfract\n"
            "Note: Instance attributes of obj.fiber and obj.matrix can be further "
            "accessed with another dot notation"
        )

    @property  # class attribute
    def micromechanics(self) -> str:
        """Get read-only value of `micromechanics` method

        : return: 'Halpin-Tsai'
        : rtype: str

        Example:
            >>> obj.micromechanics
            'Halpin-Tsai'
            >>>
        """
        return self._micromechanics

    @property  # class attribute
    def fiber_volfract(self) -> tuple:
        """Get read-only values in tuple of `fiber_volfract`

        : return: the volume fraction of fiber in UD composite
        : rtype: tuple[Decimal, ...]

        Example:
            >>> obj.fiber_volfract
            (Decimal('0'), Decimal('0.01'), Decimal('0.02'), Decimal('0.03'), Decima
            l('0.04'), Decimal('0.05'), Decimal('0.06'), Decimal('0.07'), Decimal('0.08'
            ), Decimal('0.09'), Decimal('0.1'), Decimal('0.11'), Decimal('0.12'), Decima
            l('0.13'), Decimal('0.14'), Decimal('0.15'), Decimal('0.16'), Decimal('0.17'
            ), Decimal('0.18'), Decimal('0.19'), Decimal('0.2'), Decimal('0.21'), Decima
            l('0.22'), Decimal('0.23'), Decimal('0.24'), Decimal('0.25'), Decimal('0.26'
            ), Decimal('0.27'), Decimal('0.28'), Decimal('0.29'), Decimal('0.3'), Decima
            l('0.31'), Decimal('0.32'), Decimal('0.33'), Decimal('0.34'), Decimal('0.35'
            ), Decimal('0.36'), Decimal('0.37'), Decimal('0.38'), Decimal('0.39'), Decim
            al('0.4'), Decimal('0.41'), Decimal('0.42'), Decimal('0.43'), Decimal('0.44'
            ), Decimal('0.45'), Decimal('0.46'), Decimal('0.47'), Decimal('0.48'), Decim
            al('0.49'), Decimal('0.5'), Decimal('0.51'), Decimal('0.52'), Decimal('0.53'
            ), Decimal('0.54'), Decimal('0.55'), Decimal('0.56'), Decimal('0.57'), Decim
            al('0.58'), Decimal('0.59'), Decimal('0.6'), Decimal('0.61'), Decimal('0.62'
            ), Decimal('0.63'), Decimal('0.64'), Decimal('0.65'), Decimal('0.66'), Decim
            al('0.67'), Decimal('0.68'), Decimal('0.69'), Decimal('0.7'), Decimal('0.71'
            ), Decimal('0.72'), Decimal('0.73'), Decimal('0.74'), Decimal('0.75'), Decim
            al('0.76'), Decimal('0.77'), Decimal('0.78'), Decimal('0.79'), Decimal('0.8'
            ), Decimal('0.81'), Decimal('0.82'), Decimal('0.83'), Decimal('0.84'), Decim
            al('0.85'), Decimal('0.86'), Decimal('0.87'), Decimal('0.88'), Decimal('0.89
            '), Decimal('0.9'), Decimal('0.91'), Decimal('0.92'), Decimal('0.93'), Decim
            al('0.94'), Decimal('0.95'), Decimal('0.96'), Decimal('0.97'), Decimal('0.98
            '), Decimal('0.99'), Decimal('1'))
            >>>
            >>> pprint.pprint(obj.fiber_volfract)  # Use pprint python standard library
            (Decimal('0'),
            Decimal('0.01'),
            Decimal('0.02'),
            Decimal('0.03'),
            Decimal('0.04'),
            Decimal('0.05'),
            Decimal('0.06'),
            Decimal('0.07'),
            Decimal('0.08'),
            Decimal('0.09'),
            Decimal('0.1'),
            Decimal('0.11'),
            Decimal('0.12'),
            Decimal('0.13'),
            Decimal('0.14'),
            Decimal('0.15'),
            Decimal('0.16'),
            Decimal('0.17'),
            Decimal('0.18'),
            Decimal('0.19'),
            Decimal('0.2'),
            Decimal('0.21'),
            Decimal('0.22'),
            Decimal('0.23'),
            Decimal('0.24'),
            Decimal('0.25'),
            Decimal('0.26'),
            Decimal('0.27'),
            Decimal('0.28'),
            Decimal('0.29'),
            Decimal('0.3'),
            Decimal('0.31'),
            Decimal('0.32'),
            Decimal('0.33'),
            Decimal('0.34'),
            Decimal('0.35'),
            Decimal('0.36'),
            Decimal('0.37'),
            Decimal('0.38'),
            Decimal('0.39'),
            Decimal('0.4'),
            Decimal('0.41'),
            Decimal('0.42'),
            Decimal('0.43'),
            Decimal('0.44'),
            Decimal('0.45'),
            Decimal('0.46'),
            Decimal('0.47'),
            Decimal('0.48'),
            Decimal('0.49'),
            Decimal('0.5'),
            Decimal('0.51'),
            Decimal('0.52'),
            Decimal('0.53'),
            Decimal('0.54'),
            Decimal('0.55'),
            Decimal('0.56'),
            Decimal('0.57'),
            Decimal('0.58'),
            Decimal('0.59'),
            Decimal('0.6'),
            Decimal('0.61'),
            Decimal('0.62'),
            Decimal('0.63'),
            Decimal('0.64'),
            Decimal('0.65'),
            Decimal('0.66'),
            Decimal('0.67'),
            Decimal('0.68'),
            Decimal('0.69'),
            Decimal('0.7'),
            Decimal('0.71'),
            Decimal('0.72'),
            Decimal('0.73'),
            Decimal('0.74'),
            Decimal('0.75'),
            Decimal('0.76'),
            Decimal('0.77'),
            Decimal('0.78'),
            Decimal('0.79'),
            Decimal('0.8'),
            Decimal('0.81'),
            Decimal('0.82'),
            Decimal('0.83'),
            Decimal('0.84'),
            Decimal('0.85'),
            Decimal('0.86'),
            Decimal('0.87'),
            Decimal('0.88'),
            Decimal('0.89'),
            Decimal('0.9'),
            Decimal('0.91'),
            Decimal('0.92'),
            Decimal('0.93'),
            Decimal('0.94'),
            Decimal('0.95'),
            Decimal('0.96'),
            Decimal('0.97'),
            Decimal('0.98'),
            Decimal('0.99'),
            Decimal('1'))
            >>>
        """
        return HT._fiber_volfract

    @property
    def name(self) -> str:
        """Get read-only `name` value

        : return: the name of UD composite material
        : rtype: str

        Examples (assuming the ```HT``` object has been instantiated):
        >>> obj.name
        'Carbon-Epoxy'
        >>>
        """
        return self.fiber.name + "-" + self.matrix.name

    @property
    def fiber(self) -> Transtropic | Isotropic:
        """Get read-only `fiber` value

        : return: Object which can either be ```Isotropic``` or ```Transtropic```.
            By using twice dot notation, the values of instance attributes of either
            ```Isotropic``` or ```Transtropic``` object can be accesed.
        : rtype: ```Isotropic``` | ```Transtropic```

        Example:
            >>> obj.fiber
            <__main__.Transtropic object at 0x7531c8c93cb0>
            >>> print(type(obj.fiber))
            <class '__main__.Transtropic'>
            >>> obj.fiber.name
            'Carbon'
            >>> obj.fiber.axial_youngs_modulus
            Decimal('250.000')
            >>>
        """
        return self._fiber

    @property
    def matrix(self) -> Transtropic | Isotropic:
        """Get read-only `matrix` value

        : return: the object which can either be ```Isotropic``` or ```Transtropic```
            that is used to instantiate UD composite object, which is ```HT``` object.
            By using twice dot notation, the values of instance attributes of
            ```Isotropic``` or ```Transtropic``` object can be accesed.
        : rtype: ```Isotropic``` | ```Transtropic```

        Example:
            >>> obj.matrix
            <__main__.Isotropic object at 0x7531c8c93f20>
            >>> print(type(obj.matrix))
            <class '__main__.Isotropic'>
            >>> obj.matrix.name
            'Epoxy'
            >>> obj.matrix.axial_youngs_modulus
            Decimal('2.800')
            >>>
        """
        return self._matrix

    @property
    def eff_axial_youngs_moduli(self) -> tuple:
        """Get read-only `eff_axial_youngs_moduli` values

        : return: Values in of effective axial Young's modulus estimated by Halpin-Tsai
            micromechanics method that follow the increment
            of fiber volume fraction
        : rtype: tuple[Decimal, ...]

        Example:
            >>> obj.eff_axial_youngs_moduli
            (Decimal('2.800'), Decimal('5.272'), Decimal('7.744'), Decimal('10.216'), De
            cimal('12.688'), Decimal('15.160'), Decimal('17.632'), Decimal('20.104'), De
            cimal('22.576'), Decimal('25.048'), Decimal('27.520'), Decimal('29.992'), De
            cimal('32.464'), Decimal('34.936'), Decimal('37.408'), Decimal('39.880'), De
            cimal('42.352'), Decimal('44.824'), Decimal('47.296'), Decimal('49.768'), De
            cimal('52.240'), Decimal('54.712'), Decimal('57.184'), Decimal('59.656'), De
            cimal('62.128'), Decimal('64.600'), Decimal('67.072'), Decimal('69.544'), De
            cimal('72.016'), Decimal('74.488'), Decimal('76.960'), Decimal('79.432'), De
            cimal('81.904'), Decimal('84.376'), Decimal('86.848'), Decimal('89.320'), De
            cimal('91.792'), Decimal('94.264'), Decimal('96.736'), Decimal('99.208'), De
            cimal('101.680'), Decimal('104.152'), Decimal('106.624'), Decimal('109.096')
            , Decimal('111.568'), Decimal('114.040'), Decimal('116.512'), Decimal('118.9
            84'), Decimal('121.456'), Decimal('123.928'), Decimal('126.400'), Decimal('1
            28.872'), Decimal('131.344'), Decimal('133.816'), Decimal('136.288'), Decima
            l('138.760'), Decimal('141.232'), Decimal('143.704'), Decimal('146.176'), De
            cimal('148.648'), Decimal('151.120'), Decimal('153.592'), Decimal('156.064')
            , Decimal('158.536'), Decimal('161.008'), Decimal('163.480'), Decimal('165.9
            52'), Decimal('168.424'), Decimal('170.896'), Decimal('173.368'), Decimal('1
            75.840'), Decimal('178.312'), Decimal('180.784'), Decimal('183.256'), Decima
            l('185.728'), Decimal('188.200'), Decimal('190.672'), Decimal('193.144'), De
            cimal('195.616'), Decimal('198.088'), Decimal('200.560'), Decimal('203.032')
            , Decimal('205.504'), Decimal('207.976'), Decimal('210.448'), Decimal('212.9
            20'), Decimal('215.392'), Decimal('217.864'), Decimal('220.336'), Decimal('2
            22.808'), Decimal('225.280'), Decimal('227.752'), Decimal('230.224'), Decima
            l('232.696'), Decimal('235.168'), Decimal('237.640'), Decimal('240.112'), De
            cimal('242.584'), Decimal('245.056'), Decimal('247.528'), Decimal('250.000')
            )
            >>>
        """
        return HT._estimate_E1eff(self)

    @property
    def eff_major_poissons_ratios(self) -> tuple:
        """Get read-only `eff_major_poissons_ratios` values

        : return: Values of effective major Poisson's ratios estimated by Halpin-Tsai
            micromechanics method that follow the increments
            of fiber volume fraction
        : rtype: tuple[Decimal, ...]

        Example:
            >>> obj.eff_major_poissons_ratios
            (Decimal('0.3000'), Decimal('0.2998'), Decimal('0.2996'), Decimal('0.2994'),
             Decimal('0.2992'), Decimal('0.2990'), Decimal('0.2988'), Decimal('0.2986'),
             Decimal('0.2984'), Decimal('0.2982'), Decimal('0.2980'), Decimal('0.2978'),
             Decimal('0.2976'), Decimal('0.2974'), Decimal('0.2972'), Decimal('0.2970'),
             Decimal('0.2968'), Decimal('0.2966'), Decimal('0.2964'), Decimal('0.2962'),
             Decimal('0.2960'), Decimal('0.2958'), Decimal('0.2956'), Decimal('0.2954'),
             Decimal('0.2952'), Decimal('0.2950'), Decimal('0.2948'), Decimal('0.2946'),
             Decimal('0.2944'), Decimal('0.2942'), Decimal('0.2940'), Decimal('0.2938'),
             Decimal('0.2936'), Decimal('0.2934'), Decimal('0.2932'), Decimal('0.2930'),
             Decimal('0.2928'), Decimal('0.2926'), Decimal('0.2924'), Decimal('0.2922'),
             Decimal('0.2920'), Decimal('0.2918'), Decimal('0.2916'), Decimal('0.2914'),
             Decimal('0.2912'), Decimal('0.2910'), Decimal('0.2908'), Decimal('0.2906'),
             Decimal('0.2904'), Decimal('0.2902'), Decimal('0.2900'), Decimal('0.2898'),
             Decimal('0.2896'), Decimal('0.2894'), Decimal('0.2892'), Decimal('0.2890'),
             Decimal('0.2888'), Decimal('0.2886'), Decimal('0.2884'), Decimal('0.2882'),
             Decimal('0.2880'), Decimal('0.2878'), Decimal('0.2876'), Decimal('0.2874'),
             Decimal('0.2872'), Decimal('0.2870'), Decimal('0.2868'), Decimal('0.2866'),
             Decimal('0.2864'), Decimal('0.2862'), Decimal('0.2860'), Decimal('0.2858'),
             Decimal('0.2856'), Decimal('0.2854'), Decimal('0.2852'), Decimal('0.2850'),
             Decimal('0.2848'), Decimal('0.2846'), Decimal('0.2844'), Decimal('0.2842'),
             Decimal('0.2840'), Decimal('0.2838'), Decimal('0.2836'), Decimal('0.2834'),
             Decimal('0.2832'), Decimal('0.2830'), Decimal('0.2828'), Decimal('0.2826'),
             Decimal('0.2824'), Decimal('0.2822'), Decimal('0.2820'), Decimal('0.2818'),
             Decimal('0.2816'), Decimal('0.2814'), Decimal('0.2812'), Decimal('0.2810'),
             Decimal('0.2808'), Decimal('0.2806'), Decimal('0.2804'), Decimal('0.2802'),
             Decimal('0.2800'))
            >>>
        """
        return HT._estimate_v12eff(self)

    @property
    def eff_axial_shear_moduli(self) -> tuple:
        """Get read-only `eff_axial_shear_moduli` values

        : return: Values of effective axial shear moduli estimated by Halpin-Tsai
            micromechanics method that follow the increments of fiber volume fraction
        : rtype: tuple[Decimal, ...]

        Example:
            >>> obj.eff_axial_shear_moduli
            (Decimal('1.077'), Decimal('1.097'), Decimal('1.116'), Decimal('1.137'), Dec
            imal('1.157'), Decimal('1.178'), Decimal('1.200'), Decimal('1.221'), Decimal
            ('1.244'), Decimal('1.266'), Decimal('1.289'), Decimal('1.313'), Decimal('1.
            337'), Decimal('1.362'), Decimal('1.387'), Decimal('1.412'), Decimal('1.438'
            ), Decimal('1.465'), Decimal('1.492'), Decimal('1.520'), Decimal('1.548'), D
            ecimal('1.577'), Decimal('1.607'), Decimal('1.638'), Decimal('1.669'), Decim
            al('1.700'), Decimal('1.733'), Decimal('1.766'), Decimal('1.800'), Decimal('
            1.835'), Decimal('1.871'), Decimal('1.908'), Decimal('1.945'), Decimal('1.98
            4'), Decimal('2.023'), Decimal('2.064'), Decimal('2.106'), Decimal('2.148'),
             Decimal('2.192'), Decimal('2.238'), Decimal('2.284'), Decimal('2.332'), Dec
            imal('2.381'), Decimal('2.431'), Decimal('2.484'), Decimal('2.537'), Decimal
            ('2.592'), Decimal('2.649'), Decimal('2.708'), Decimal('2.769'), Decimal('2.
            832'), Decimal('2.896'), Decimal('2.963'), Decimal('3.032'), Decimal('3.104'
            ), Decimal('3.178'), Decimal('3.255'), Decimal('3.335'), Decimal('3.417'), D
            ecimal('3.503'), Decimal('3.592'), Decimal('3.685'), Decimal('3.781'), Decim
            al('3.882'), Decimal('3.986'), Decimal('4.096'), Decimal('4.210'), Decimal('
            4.329'), Decimal('4.453'), Decimal('4.584'), Decimal('4.721'), Decimal('4.86
            4'), Decimal('5.015'), Decimal('5.174'), Decimal('5.341'), Decimal('5.517'),
             Decimal('5.704'), Decimal('5.901'), Decimal('6.110'), Decimal('6.332'), Dec
            imal('6.568'), Decimal('6.819'), Decimal('7.088'), Decimal('7.376'), Decimal
            ('7.685'), Decimal('8.017'), Decimal('8.375'), Decimal('8.763'), Decimal('9.
            183'), Decimal('9.642'), Decimal('10.143'), Decimal('10.694'), Decimal('11.3
            01'), Decimal('11.974'), Decimal('12.725'), Decimal('13.567'), Decimal('14.5
            19'), Decimal('15.604'), Decimal('16.850'), Decimal('18.298'), Decimal('20.0
            00'))
            >>>
        """
        return HT._estimate_G12eff(self)

    @property
    def eff_pstrain_bulk_moduli(self) -> tuple:
        """Get read-only `eff_pstrain_bulk_moduli` values

        : return: Values of effective pstrain bulk moduli estimated by Halpin-Tsai
            micromechanics method that follow the increments
            of fiber volume fraction
        : rtype: tuple[Decimal, ...]

        Example:
            >>> obj.eff_pstrain_bulk_moduli
            (Decimal('2.692'), Decimal('2.722'), Decimal('2.753'), Decimal('2.784'), Dec
            imal('2.815'), Decimal('2.847'), Decimal('2.880'), Decimal('2.913'), Decimal
            ('2.947'), Decimal('2.981'), Decimal('3.016'), Decimal('3.052'), Decimal('3.
            088'), Decimal('3.124'), Decimal('3.162'), Decimal('3.200'), Decimal('3.239'
            ), Decimal('3.278'), Decimal('3.318'), Decimal('3.359'), Decimal('3.401'), D
            ecimal('3.444'), Decimal('3.487'), Decimal('3.531'), Decimal('3.576'), Decim
            al('3.622'), Decimal('3.669'), Decimal('3.717'), Decimal('3.766'), Decimal('
            3.815'), Decimal('3.866'), Decimal('3.918'), Decimal('3.971'), Decimal('4.02
            5'), Decimal('4.080'), Decimal('4.137'), Decimal('4.195'), Decimal('4.254'),
             Decimal('4.314'), Decimal('4.376'), Decimal('4.439'), Decimal('4.504'), Dec
            imal('4.570'), Decimal('4.638'), Decimal('4.707'), Decimal('4.778'), Decima
            l('4.851'), Decimal('4.926'), Decimal('5.003'), Decimal('5.081'), Decimal('
            5.162'), Decimal('5.245'), Decimal('5.330'), Decimal('5.417'), Decimal('5.50
            7'), Decimal('5.599'), Decimal('5.694'), Decimal('5.792'), Decimal('5.893'),
             Decimal('5.996'), Decimal('6.103'), Decimal('6.213'), Decimal('6.326'), Dec
            imal('6.443'), Decimal('6.564'), Decimal('6.689'), Decimal('6.817'), Decimal
            ('6.950'), Decimal('7.088'), Decimal('7.231'), Decimal('7.378'), Decimal('7.
            531'), Decimal('7.690'), Decimal('7.854'), Decimal('8.025'), Decimal('8.202'
            ), Decimal('8.387'), Decimal('8.579'), Decimal('8.779'), Decimal('8.987'), D
            ecimal('9.204'), Decimal('9.431'), Decimal('9.669'), Decimal('9.917'), Decim
            al('10.177'), Decimal('10.449'), Decimal('10.735'), Decimal('11.036'), Decim
            al('11.352'), Decimal('11.685'), Decimal('12.037'), Decimal('12.408'), Decim
            al('12.801'), Decimal('13.218'), Decimal('13.661'), Decimal('14.132'), Decim
            al('14.634'), Decimal('15.170'), Decimal('15.744'), Decimal('16.360'), Decim
            al('17.023'))
            >>>
        """
        return HT._estimate_K23eff(self)

    @property
    def eff_transverse_shear_moduli(self) -> tuple:
        """Get read-only `eff_transverse_shear_moduli` values

        : return: Values of effective transverse shear moduli estimated by Halpin-Tsai
            micromechanics method that follow the increments
            of fiber volume fraction
        : rtype: tuple[Decimal, ...]

        Example:
            >>> obj.eff_transverse_shear_moduli
            (Decimal('1.077'), Decimal('1.091'), Decimal('1.106'), Decimal('1.120'), Dec
            imal('1.135'), Decimal('1.151'), Decimal('1.166'), Decimal('1.182'), Decimal
            ('1.198'), Decimal('1.214'), Decimal('1.231'), Decimal('1.248'), Decimal('1.
            265'), Decimal('1.283'), Decimal('1.301'), Decimal('1.319'), Decimal('1.338'
            ), Decimal('1.357'), Decimal('1.376'), Decimal('1.396'), Decimal('1.416'), D
            ecimal('1.437'), Decimal('1.458'), Decimal('1.479'), Decimal('1.501'), Decim
            al('1.524'), Decimal('1.546'), Decimal('1.570'), Decimal('1.594'), Decimal('
            1.618'), Decimal('1.643'), Decimal('1.669'), Decimal('1.695'), Decimal('1.72
            2'), Decimal('1.749'), Decimal('1.777'), Decimal('1.806'), Decimal('1.835'),
             Decimal('1.865'), Decimal('1.896'), Decimal('1.928'), Decimal('1.960'), Dec
            imal('1.993'), Decimal('2.028'), Decimal('2.063'), Decimal('2.099'), Decimal
            ('2.136'), Decimal('2.174'), Decimal('2.213'), Decimal('2.253'), Decimal('2.
            295'), Decimal('2.338'), Decimal('2.382'), Decimal('2.427'), Decimal('2.474'
            ), Decimal('2.522'), Decimal('2.571'), Decimal('2.623'), Decimal('2.676'), D
            ecimal('2.731'), Decimal('2.787'), Decimal('2.846'), Decimal('2.906'), Decim
            al('2.969'), Decimal('3.034'), Decimal('3.102'), Decimal('3.172'), Decimal('
            3.245'), Decimal('3.321'), Decimal('3.399'), Decimal('3.481'), Decimal('3.56
            7'), Decimal('3.656'), Decimal('3.749'), Decimal('3.846'), Decimal('3.947'),
             Decimal('4.054'), Decimal('4.165'), Decimal('4.282'), Decimal('4.404'), Dec
            imal('4.533'), Decimal('4.669'), Decimal('4.813'), Decimal('4.964'), Decimal
            ('5.124'), Decimal('5.293'), Decimal('5.473'), Decimal('5.664'), Decimal('5.
            867'), Decimal('6.085'), Decimal('6.317'), Decimal('6.566'), Decimal('6.833'
            ), Decimal('7.122'), Decimal('7.433'), Decimal('7.771'), Decimal('8.139'), D
            ecimal('8.540'), Decimal('8.980'), Decimal('9.464'), Decimal('10.000'))
            >>>
        """
        return HT._estimate_G23eff(self)

    @property
    def eff_transverse_youngs_moduli(self) -> tuple:
        """Get read-only `eff_transverse_youngs_moduli` values

        : return: Values of effective transverse Young's moduli estimated by Halpin-Tsai
            micromechanics method that follow the
            increments of fiber volume fraction
        : rtype: tuple[Decimal, ...]

        Example:
            >>> obj.eff_transverse_youngs_moduli
            (Decimal('2.800'), Decimal('2.958'), Decimal('3.045'), Decimal('3.108'), Dec
            imal('3.163'), Decimal('3.216'), Decimal('3.265'), Decimal('3.314'), Decimal
            ('3.362'), Decimal('3.409'), Decimal('3.458'), Decimal('3.506'), Decimal('3.
            555'), Decimal('3.605'), Decimal('3.655'), Decimal('3.705'), Decimal('3.758'
            ), Decimal('3.810'), Decimal('3.863'), Decimal('3.917'), Decimal('3.972'), D
            ecimal('4.030'), Decimal('4.087'), Decimal('4.144'), Decimal('4.204'), Decim
            al('4.266'), Decimal('4.326'), Decimal('4.391'), Decimal('4.456'), Decimal('
            4.521'), Decimal('4.588'), Decimal('4.658'), Decimal('4.728'), Decimal('4.80
            0'), Decimal('4.873'), Decimal('4.949'), Decimal('5.026'), Decimal('5.104'),
             Decimal('5.184'), Decimal('5.267'), Decimal('5.353'), Decimal('5.438'), Dec
            imal('5.527'), Decimal('5.619'), Decimal('5.712'), Decimal('5.808'), Decimal
            ('5.907'), Decimal('6.008'), Decimal('6.111'), Decimal('6.217'), Decimal('6.
            328'), Decimal('6.441'), Decimal('6.558'), Decimal('6.676'), Decimal('6.800'
            ), Decimal('6.926'), Decimal('7.055'), Decimal('7.191'), Decimal('7.331'), D
            ecimal('7.474'), Decimal('7.621'), Decimal('7.775'), Decimal('7.932'), Decim
            al('8.095'), Decimal('8.265'), Decimal('8.441'), Decimal('8.622'), Decimal('
            8.811'), Decimal('9.007'), Decimal('9.208'), Decimal('9.419'), Decimal('9.63
            9'), Decimal('9.868'), Decimal('10.105'), Decimal('10.353'), Decimal('10.610
            '), Decimal('10.881'), Decimal('11.163'), Decimal('11.458'), Decimal('11.766
            '), Decimal('12.090'), Decimal('12.430'), Decimal('12.789'), Decimal('13.165
            '), Decimal('13.562'), Decimal('13.979'), Decimal('14.422'), Decimal('14.890
            '), Decimal('15.386'), Decimal('15.914'), Decimal('16.475'), Decimal('17.073
            '), Decimal('17.711'), Decimal('18.397'), Decimal('19.131'), Decimal('19.923
            '), Decimal('20.778'), Decimal('21.702'), Decimal('22.707'), Decimal('23.801
            '), Decimal('25.000'))
            >>>
        """
        return HT._estimate_E2eff(self)

    def E1eff(self, min: float | None = None, max: float | None = None) -> None:
        """Print value or values of effective axial Young's modulus of UD composite
        based on the user defined fiber volume fraction for quick in-situ analysis.

        : param `min`: single value fiber volume specified by user or the starting
            value of fiber volume fraction range specified by user. Any value entered
            will be rounded off to two significant digits after decimal point.
        : type: float | None
        : param `max`: None if only one single fiber volume fraction value is specified by
            user or the inclusive end value of a range of fiber volume fraction
            specified by user. Any value entered will be rounded off to two significant
            digits after decimal point.
        : type: float | None
        : rtype: None

        Examples:
            >>> obj.E1eff(0.71154)  # specific value of fiber volume fraction
            Vf : E1*
            0.71 : 178.312
            >>>
            >>> obj.E1eff(0.5, 0.6)  # custom range of fiber volume fraction
            Vf : E1*
            0.5 : 126.400
            0.51 : 128.872
            0.52 : 131.344
            0.53 : 133.816
            0.54 : 136.288
            0.55 : 138.760
            0.56 : 141.232
            0.57 : 143.704
            0.58 : 146.176
            0.59 : 148.648
            0.6 : 151.120
            >>>
        """
        bounds: tuple = HT.__get_index_num(min, max)
        print("Vf : E1*")
        if bounds[1] is not None:
            for i in range(bounds[0], bounds[1] + 1):
                print(f"{self.fiber_volfract[i]} : {self.eff_axial_youngs_moduli[i]}")
        else:
            print(
                f"{self.fiber_volfract[bounds[0]]} : "
                + f"{self.eff_axial_youngs_moduli[bounds[0]]}"
            )

    def E2eff(self, min: float | None = None, max: float | None = None) -> None:
        """Print value or values of effective transverse Young's modulus of UD
        composite based on the user defined fiber volume fraction for quick in-situ
        analysis.

        : param `min`: single value fiber volume specified by user or the starting
            value of fiber volume fraction range specified by user. Any value entered
            will be rounded off to two significant digits after decimal point.
        : type: float | None
        : param `max`: None if only one single fiber volume fraction value is specified by
            user or inclusive end value of a range of fiber volume fraction
            specified by user. Any value entered will be rounded off to two significant
            digits after decimal point.
        : type: float | None
        : rtype: None

        Examples:
            >>> obj.E2eff(0.71154)  # specific value of fiber volume fraction
            Vf : E2*
            0.71 : 9.639
            >>>
            >>> obj.E2eff(0.5, 0.6)  # custom range of fiber volume fraction
            Vf : E1*
            0.5 : 6.328
            0.51 : 6.441
            0.52 : 6.558
            0.53 : 6.676
            0.54 : 6.800
            0.55 : 6.926
            0.56 : 7.055
            0.57 : 7.191
            0.58 : 7.331
            0.59 : 7.474
            0.6 : 7.621
            >>>
        """
        bounds: tuple = HT.__get_index_num(min, max)
        print("Vf : E2*")
        if bounds[1] is not None:
            for i in range(bounds[0], bounds[1] + 1):
                print(
                    f"{self.fiber_volfract[i]} : {self.eff_transverse_youngs_moduli[i]}"
                )
        else:
            print(
                f"{self.fiber_volfract[bounds[0]]} : "
                + f"{self.eff_transverse_youngs_moduli[bounds[0]]}"
            )

    def G12eff(self, min: float | None = None, max: float | None = None) -> None:
        """Print value or values of effective axial shear modulus of UD composite
        based on the user defined fiber volume fraction for quick in-situ analysis.

        : param `max`: single value fiber volume specified by user or the starting
            value of fiber volume fraction range specified by user. Any value entered
            will be rounded off to two significant digits after decimal point.
        : type: float | None
        : param `min`: None if only one single fiber volume fraction value is specified by
            user or the inclusive end value of a range of fiber volume fraction
            specified by user. Any value entered will be rounded off to two significant
            digits after decimal point.
        : type: float | None
        : rtype: None

        Examples:
            >>> obj.G12eff(0.71154)  # specific value of fiber volume fraction
            Vf : G12*
            0.71 : 4.864
            >>>
            >>> obj.G12eff(0.5, 0.6)  # custom range of fiber volume fraction
            Vf : G12*
            0.5 : 2.832
            0.51 : 2.896
            0.52 : 2.963
            0.53 : 3.032
            0.54 : 3.104
            0.55 : 3.178
            0.56 : 3.255
            0.57 : 3.335
            0.58 : 3.417
            0.59 : 3.503
            0.6 : 3.592
            >>>
        """
        bounds: tuple = HT.__get_index_num(min, max)
        print("Vf : G12*")
        if bounds[1] is not None:
            for i in range(bounds[0], bounds[1] + 1):
                print(f"{self.fiber_volfract[i]} : {self.eff_axial_shear_moduli[i]}")
        else:
            print(
                f"{self.fiber_volfract[bounds[0]]} : "
                + f"{self.eff_axial_shear_moduli[bounds[0]]}"
            )

    def G23eff(self, min: float | None = None, max: float | None = None) -> None:
        """Print value or values of effective transverse shear modulus of UD
        composite, based on the user defined fiber volume fraction quick in-situ analysis.

        : param `min`: single value fiber volume specified by user or the starting
            value of fiber volume fraction range specified by user. Any value entered
            will be rounded off to two significant digits after decimal point.
        : type: float | None
        : param `max`: None if only one single fiber volume fraction value is specified by
            user or the inclusive end value of a range of fiber volume fraction
            specified by user. Any value entered will be rounded off to two significant
            digits after decimal point.
        : type: float | None
        : rtype: None

        Examples:
            >>> obj.G23eff(0.71154)  # specific value of fiber volume fraction
            Vf : G23*
            0.71 : 3.567
            >>>
            >>> obj.G23eff(0.5, 0.6)  # custom range of fiber volume fraction
            Vf : G23*
            0.5 : 2.295
            0.51 : 2.338
            0.52 : 2.382
            0.53 : 2.427
            0.54 : 2.474
            0.55 : 2.522
            0.56 : 2.571
            0.57 : 2.623
            0.58 : 2.676
            0.59 : 2.731
            0.6 : 2.787
            >>>
        """
        bounds: tuple = HT.__get_index_num(min, max)
        print("Vf : G23*")
        if bounds[1] is not None:
            for i in range(bounds[0], bounds[1] + 1):
                print(
                    f"{self.fiber_volfract[i]} : {self.eff_transverse_shear_moduli[i]}"
                )
        else:
            print(
                f"{self.fiber_volfract[bounds[0]]} : "
                + f"{self.eff_transverse_shear_moduli[bounds[0]]}"
            )

    def v12eff(self, min: float | None = None, max: float | None = None) -> None:
        """Print value or values of effective major Poisson's ratio of UD
        composite, based on the user defined fiber volume fraction quick in-situ analysis.

        : param `min`: single value fiber volume specified by user or the starting
            value of fiber volume fraction range specified by user. Any value entered
            will be rounded off to two significant digits after decimal point.
        : type: float | None
        : param `max`: None if only one single fiber volume fraction value is specified by
            user or the inclusive end value of a range of fiber volume fraction
            specified by user. Any value entered will be rounded off to two significant
            digits after decimal point.
        : type: float | None
        : rtype: None

        Examples:
            >>> obj.v12eff(0.71154)  # specific value of fiber volume fraction
            Vf : v12*
            0.71 : 0.2858
            >>>
            >>> obj.v12eff(0.5, 0.6)  # custom range of fiber volume fraction
            Vf : v12*
            0.5 : 0.2900
            0.51 : 0.2898
            0.52 : 0.2896
            0.53 : 0.2894
            0.54 : 0.2892
            0.55 : 0.2890
            0.56 : 0.2888
            0.57 : 0.2886
            0.58 : 0.2884
            0.59 : 0.2882
            0.6 : 0.2880
            >>>
        """
        bounds: tuple = HT.__get_index_num(min, max)
        print("Vf : v12*")
        if bounds[1] is not None:
            for i in range(bounds[0], bounds[1] + 1):
                print(f"{self.fiber_volfract[i]} : {self.eff_major_poissons_ratios[i]}")
        else:
            print(
                f"{self.fiber_volfract[bounds[0]]} : "
                + f"{self.eff_major_poissons_ratios[bounds[0]]}"
            )

    def K23eff(self, min: float | None = None, max: float | None = None) -> None:
        """Print value or values of effective plane-strain bulk modulus of UD
        composite, based on the user defined fiber volume fraction quick in-situ analysis.

        : param `min`: single value fiber volume specified by user or the starting
            value of fiber volume fraction range specified by user. Any value entered
            will be rounded off to two significant digits after decimal point.
        : type: float | None
        : param max: None if only one single fiber volume fraction value is specified by
            user or the inclusive end value of a range of fiber volume fraction
            specified by user. Any value entered will be rounded off to two significant
            digits after decimal point.
        : type: float | None
        : rtype: None

        Examples:
            >>> obj.K23eff(0.71154)  # specific value of fiber volume fraction
            Vf : K23*
            0.71 : 7.531
            >>>
            >>> obj.K23eff(0.5, 0.6)  # custom range of fiber volume fraction
            Vf : K23*
            0.5 : 5.162
            0.51 : 5.245
            0.52 : 5.330
            0.53 : 5.417
            0.54 : 5.507
            0.55 : 5.599
            0.56 : 5.694
            0.57 : 5.792
            0.58 : 5.893
            0.59 : 5.996
            0.6 : 6.103
            >>>
        """
        bounds: tuple = HT.__get_index_num(min, max)
        print("Vf : K23*")
        if bounds[1] is not None:
            for i in range(bounds[0], bounds[1] + 1):
                print(f"{self.fiber_volfract[i]} : {self.eff_pstrain_bulk_moduli[i]}")
        else:
            print(
                f"{self.fiber_volfract[bounds[0]]} : "
                + f"{self.eff_pstrain_bulk_moduli[bounds[0]]}"
            )

    def _estimate_E1eff(self) -> tuple[Decimal, ...]:
        """Compute the effective axial Young's moduli of UD composite using
        Halpin-Tsai micromechanics formula that depends on the values of
        `youngs_modulus` or `axial_youngs_modulus` provided by instance attributes
        of `fiber` and `matrix`, and also on the values of fiber volume fraction
        provided by the tuple of `fiber_volfract`. The computed values are then
        initialized to a class instance attribute - `eff_axial_youngs_moduli`.

        : type: ```Isotropic``` | ```Transtropic``` | None
        : raise TypeError: if `fiber` and `matrix` is None or neither ```Isotropic``` nor
            ```Transtropic```
        : return: The computed effective axial Young's moduli by Halpin-Tsai
            micromechanics method
        : rtype: tuple[Decimal, ...]
        """
        # Get fiber axial Young's modulus
        if isinstance(self.fiber, Isotropic):
            fiber_axial_youngs_modulus: Decimal = self.fiber.youngs_modulus
        else:
            fiber_axial_youngs_modulus = self.fiber.axial_youngs_modulus
        # Get matrix axial Young's modulus
        if isinstance(self.matrix, Isotropic):
            matrix_axial_youngs_modulus: Decimal = self.matrix.youngs_modulus
        else:
            matrix_axial_youngs_modulus = self.matrix.axial_youngs_modulus

        # Compute effective property
        effective_axial_youngs_moduli: list[Decimal] = []
        for vf in HT._fiber_volfract:
            effective_axial_youngs_moduli.append(
                (
                    fiber_axial_youngs_modulus * vf
                    + matrix_axial_youngs_modulus * (Decimal("1") - vf)
                ).quantize(Decimal("1.000"))
            )

        # Return effective property
        return tuple(effective_axial_youngs_moduli)

    def _estimate_v12eff(self) -> tuple[Decimal, ...]:
        """Compute the effective major Poisson's ratios of UD composite using
        Halpin-Tsai micromechanics formula that depends on the values of
        `poissons_ratio` or `major_poissons_ratio` provided by instance attributes
        of `fiber` and `matrix`, and also on the values of fiber volume fraction
        provided by the tuple of `fiber_volfract`. The computed values are then
        initialized to a class instance attribute - `eff_major_poissons_ratios`.

        : raise TypeError: if `fiber` and `matrix` is None or neither ```Isotropic``` nor
            ```Transtropic```
        : return: The computed effective axial Young's moduli by Halpin-Tsai
            micromechanics method
        : rtype: tuple[Decimal, ...]
        """
        # Get fiber major Poisson's ratio
        if isinstance(self.fiber, Isotropic):
            fiber_major_poissons_ratio: Decimal = self.fiber.poissons_ratio
        else:
            fiber_major_poissons_ratio = self.fiber.major_poissons_ratio
        # Get matrix major Poisson's ratio
        if isinstance(self.matrix, Isotropic):
            matrix_major_poissons_ratio: Decimal = self.matrix.poissons_ratio
        else:
            matrix_major_poissons_ratio = self.matrix.major_poissons_ratio

        # Compute effective property
        effective_major_poissons_ratios: list[Decimal] = []
        for vf in HT._fiber_volfract:
            effective_major_poissons_ratios.append(
                (
                    fiber_major_poissons_ratio * vf
                    + matrix_major_poissons_ratio * (Decimal("1.0000") - vf)
                ).quantize(Decimal("1.0000"))
            )

        # Return effective property
        return tuple(effective_major_poissons_ratios)

    def _estimate_G12eff(self) -> tuple[Decimal, ...]:
        """Compute the effective axial shear moduli of UD composite using Halpin-Tsai
        micromechanics formula that depends on the value of `shear_modulus` and/or
        `axial_shear_modulus` provided by instance attributes of `fiber` and `matrix`,
        and also on the values of fiber volume fraction provided by the tuple of
        `fiber_volfract`. The computed values are then initialized to a class instance
        attribute - `eff_axial_shear_moduli`.

        : raise TypeError: if `fiber` and `matrix` is None or neither ```Isotropic```
            nor ```Transtropic```
        : return: The computed effective axial shear moduli by Halpin-Tsai
            micromechanics method
        : rtype: tuple[Decimal, ...]
        """
        # Get fiber axial shear modulus
        if isinstance(self.fiber, Isotropic):
            fiber_axial_shear_modulus: Decimal = self.fiber.shear_modulus
        else:
            fiber_axial_shear_modulus = self.fiber.axial_shear_modulus
        # Get matrix axial shear modulus
        if isinstance(self.matrix, Isotropic):
            matrix_axial_shear_modulus: Decimal = self.matrix.shear_modulus
        else:
            matrix_axial_shear_modulus = self.matrix.axial_shear_modulus

        # Compute effective property
        effective_axial_shear_moduli: list[Decimal] = []
        for vf in HT._fiber_volfract:
            effective_axial_shear_moduli.append(
                (
                    (
                        (fiber_axial_shear_modulus + matrix_axial_shear_modulus)
                        * matrix_axial_shear_modulus
                        * (Decimal("1.000") - vf)
                        + Decimal("2.000")
                        * fiber_axial_shear_modulus
                        * matrix_axial_shear_modulus
                        * vf
                    )
                    / (
                        (fiber_axial_shear_modulus + matrix_axial_shear_modulus)
                        * (Decimal("1.000") - vf)
                        + Decimal("2.000") * matrix_axial_shear_modulus * vf
                    )
                ).quantize(Decimal("1.000"))
            )

        # Return effective property
        return tuple(effective_axial_shear_moduli)

    def _estimate_K23eff(self) -> tuple[Decimal, ...]:
        """Compute the effective plane-strain bulk shear moduli of UD composite using
        Halpin-Tsai micromechanics formula that depends on the values of
        `pstrain_bulk_modulus` provided by instance attributes of `fiber` and `matrix`,
        and also on the values of fiber volume fraction provided by the tuple of
        `fiber_volfract`. The computed values are then initialized to a class instance
        attribute - `eff_transverse_shear_moduli`.

        : raise TypeError: if `fiber` and `matrix` is None or neither ```Isotropic```
            nor ```Transtropic```
        : return: The computed effective plane_strain bulk moduli by Halpin-Tsai
            micromechanics method
        : rtype: tuple[Decimal, ...]
        """
        # Get fiber plane-strain bulk modulus and transverse shear modulus
        if isinstance(self.fiber, Isotropic):
            fiber_pstrain_bulk_modulus: Decimal = self.fiber.pstrain_bulk_modulus
        else:
            fiber_pstrain_bulk_modulus = self.fiber.pstrain_bulk_modulus
        # Get matrix plane-strain bulk modulus and transverse shear modulus
        if isinstance(self.matrix, Isotropic):
            matrix_pstrain_bulk_modulus: Decimal = self.matrix.pstrain_bulk_modulus
            matrix_transverse_shear_modulus: Decimal = self.matrix.shear_modulus
        else:
            matrix_pstrain_bulk_modulus = self.matrix.pstrain_bulk_modulus
            matrix_transverse_shear_modulus = self.matrix.transverse_shear_modulus

        # Compute effective property
        effective_pstrain_bulk_moduli: list[Decimal] = []
        for vf in HT._fiber_volfract:
            effective_pstrain_bulk_moduli.append(
                (
                    (
                        matrix_pstrain_bulk_modulus
                        * (fiber_pstrain_bulk_modulus + matrix_transverse_shear_modulus)
                        * (Decimal("1.000") - vf)
                        + fiber_pstrain_bulk_modulus
                        * (
                            matrix_pstrain_bulk_modulus
                            + matrix_transverse_shear_modulus
                        )
                        * vf
                    )
                    / (
                        (fiber_pstrain_bulk_modulus + matrix_transverse_shear_modulus)
                        * (Decimal("1.000") - vf)
                        + (
                            matrix_pstrain_bulk_modulus
                            + matrix_transverse_shear_modulus
                        )
                        * vf
                    )
                ).quantize(Decimal("1.000"))
            )

        # Return effective property
        return tuple(effective_pstrain_bulk_moduli)

    def _estimate_G23eff(self) -> tuple[Decimal, ...]:
        """Compute the effective transverse shear moduli of UD composite using
        Halpin-Tsai micromechanics formula that depends on the value of `shear_modulus`
        and/or `transverse_shear_modulus` provided by instance attributes of `fiber` and
        `matrix`, and also on the values of fiber volume fraction provided by the tuple
        of `fiber_volfract`. The computed values are then initialized to a class
        instance attribute - `eff_transverse_shear_moduli`.

        : raise TypeError: if `fiber` and `matrix` is None or neither ```Isotropic```
            nor ```Transtropic```
        : return: The computed effective transverse shear moduli by Halpin-Tsai
            micromechanics method
        : rtype: tuple[Decimal, ...]
            >>>
        """
        # Get fiber plane-strain bulk modulus and transverse shear modulus
        if isinstance(self.fiber, Isotropic):
            fiber_transverse_shear_modulus: Decimal = self.fiber.shear_modulus
        else:
            fiber_transverse_shear_modulus = self.fiber.transverse_shear_modulus
        # Get matrix plane-strain bulk modulus and transverse shear modulus
        if isinstance(self.matrix, Isotropic):
            matrix_pstrain_bulk_modulus: Decimal = self.matrix.pstrain_bulk_modulus
            matrix_transverse_shear_modulus: Decimal = self.matrix.shear_modulus
        else:
            matrix_pstrain_bulk_modulus = self.matrix.pstrain_bulk_modulus
            matrix_transverse_shear_modulus = self.matrix.transverse_shear_modulus

        # Compute effective property
        effective_transverse_shear_moduli: list[Decimal] = []
        for vf in HT._fiber_volfract:
            effective_transverse_shear_moduli.append(
                (
                    (
                        matrix_transverse_shear_modulus
                        * (
                            Decimal("2.000")
                            * vf
                            * fiber_transverse_shear_modulus
                            * (
                                matrix_pstrain_bulk_modulus
                                + matrix_transverse_shear_modulus
                            )
                            + Decimal("2.000")
                            * (Decimal("1.000") - vf)
                            * fiber_transverse_shear_modulus
                            * matrix_transverse_shear_modulus
                            + (Decimal("1.000") - vf)
                            * matrix_pstrain_bulk_modulus
                            * (
                                fiber_transverse_shear_modulus
                                + matrix_transverse_shear_modulus
                            )
                        )
                    )
                    / (
                        Decimal("2")
                        * vf
                        * matrix_transverse_shear_modulus
                        * (
                            matrix_pstrain_bulk_modulus
                            + matrix_transverse_shear_modulus
                        )
                        + Decimal("2")
                        * (Decimal("1") - vf)
                        * fiber_transverse_shear_modulus
                        * matrix_transverse_shear_modulus
                        + (Decimal("1") - vf)
                        * matrix_pstrain_bulk_modulus
                        * (
                            fiber_transverse_shear_modulus
                            + matrix_transverse_shear_modulus
                        )
                    )
                ).quantize(Decimal("1.000"))
            )

        # Return effective property
        return tuple(effective_transverse_shear_moduli)

    def _estimate_E2eff(self) -> tuple[Decimal, ...]:
        """Compute the effective transverse Young's modulus of UD composite, i.e. ```HT```
        object using transversely-isotropic formula that depends on the values of
        other computed effective properties, e.g. `eff_axial_youngs_moduli`,
        `eff_pstrain_bulk_moduli`, `eff_transverse_shear_moduli` and
        `eff_major_poissons_ratios` of ```HT``` instantiated object and of course, on
        the values of fiber volume fraction provided by the tuple of `fiber_volfract`
        as well. The computed effective elastic property is then initialized to
        a class attribute `eff_transverse_youngs_moduli`.

        : raise TypeError: if `fiber` and `matrix` is None or neither ```Isotropic```
            nor ```Transtropic```
        : return: The computed effective transverse shear moduli by Halpin-Tsai
            micromechanics method
        : rtype: tuple[Decimal]
        """
        # Compute effective transverse Young's moduli, E2*
        return tuple(
            map(
                lambda tuple1, tuple2, tuple3, tuple4: (
                    (Decimal("4.000") * tuple1 * tuple2)
                    / (
                        tuple2
                        + tuple1
                        + (Decimal("4.000") * tuple3**2 * tuple1 * tuple2) / tuple4
                    )
                ).quantize(Decimal("1.000")),
                self.eff_transverse_shear_moduli,
                self.eff_pstrain_bulk_moduli,
                self.eff_major_poissons_ratios,
                self.eff_axial_youngs_moduli,
            )
        )

    @staticmethod
    def __get_index_num(start: float | None = None, end: float | None = None) -> tuple:
        """Get the index number of a tuple that has 101 element. Basicall, this method
        is called by other instance methods such as ``E1eff``, ``E2eff``, ``G12eff``,
        ``v12eff``, ``K23eff``, and ``G23eff`` when user requests to get the value/s of
        effective property at specific fiber volume fraction or at specific range of
        fiber volume fraction. This method will then identify the index number/s of the
        requested fiber volume fraction/s in the `fiber_volfract` tuple so that it or
        they can be used to cross-reference and fetch the desired value/s of effective
        property that has the same tuple size as the size of `fiber_volfract` tuple.

        : param `start`: specific volume fraction of fiber for a single value or the
            start of fiber volume fraction range
        : type: float | None
        : param `end`: the end of fiber volume fraction range (inclusive) or None if
            specific fiber volume fraction is desired by user
        : type: float | None
        : raise TypeError and ValueError: if first argument - `start` is None, not a
            ```float``` type number or its value does not lie between 0 and 1, and also
            if second argument if provided by user is None, not a ```float``` type
            number or its value is lesser than the value of first argument or not in
            between 0 and 1.
        : return: index number or index numbers of a tuple of size 100.
        : rtype: tuple[int]
        """
        if start is None or not isinstance(start, float):
            raise TypeError(
                "Expected fiber volume fraction value for first argument to be 'float' "
                + "type number"
            )
        if start < 0 or start > 1:
            raise ValueError("Expected fiber volume fraction to be from 0 to 1")
        if end is not None:
            if not isinstance(end, float):
                raise TypeError("Expected second argument to be a 'float' type number")
            if end < 0 or end > 1 or end <= start:
                raise ValueError(
                    "Expected value for second argument to be in between 0 and 1 and "
                    + "should be greater than value in the first argument"
                )
            start = HT._fiber_volfract.index(
                Decimal(round(start, 2)).quantize(Decimal("1.000"))
            )
            end = HT._fiber_volfract.index(
                Decimal(round(end, 2)).quantize(Decimal("1.000"))
            )
            return (start, end)
        else:
            start = HT._fiber_volfract.index(
                Decimal(round(start, 2)).quantize(Decimal("1.000"))
            )
            return (start, end)


def main():
    """
    Provide introductory to text-image based of Halpin-Tsai Micromechanics program when
    program is executed directly or otherwise, pass.
    """
    if __name__ == "__main__":
        # When code is executed directly
        print(
            "\n\n                                                                      "
        )
        print(
            "\033[94m  #######       ######      ##########      ######      #######   "
        )
        print(
            "\033[94m##########    ##########    ##########    ##########    ######### "
        )
        print(
            "\033[94m###           ###    ###    ###           ###    ###    ###    ###"
        )
        print(
            "\033[94m###           ####          ###           ###    ###    ###    ###                           \033[91m     oo      \033[0m            "
        )
        print(
            "\033[94m###             ####        ########      ###    ###    ###   ###       \033[91m                         #####,   \033[0m          M "
        )
        print(
            "\033[94m###               ####        #######     ###    ###    ########       \033[91m  ##        ###         ###     `  \033[0m       MULIA"
        )
        print(
            "\033[94m###                ####          #####    ###    ###    ######        \033[91m  #  ##     #####      ###          \033[0m          N "
        )
        print(
            "\033[94m###           ###   ####    ###  #####    ###    ###    ###        \033[91m   #     ##  ###  ###   ###            \033[0m          H "
        )
        print(
            "\033[94m##########    ##########     ########     ##########    ###        \033[91m          #####    ######              \033[0m          A "
        )
        print(
            "\033[94m  #######       ######        ######        ######      ###        \033[91m           ##       ###                \033[0m          T "
        )
        print(
            "##        ##                                                                 ############                               "
        )
        print(
            "##        ##       #       #         #######    #######   # #     #           ##########    ######       #       #######"
        )
        print(
            "############      # #      #         #      #      #      #  #    #               ##       #            # #         #   "
        )
        print(
            "############     #####     #         #######       #      #   #   #    #####      ##        #####      #####        #   "
        )
        print(
            "##        ##    #     #    #         #             #      #    #  #               ##             #    #     #       #   "
        )
        print(
            "##        ##   #       #   #######   #          #######   #     # #               ##      #######    #       #   #######"
        )
        print(
            "###      ###  ##                                                          ##                        ##                  "
        )
        print(
            "####    ####                                                              ##                                            "
        )
        print(
            "## ##  ## ##  ##   #####   ##  ##  #####   ## ### ###    #####    #####   ## ###    #####  ## ###   ##   #####    ##### "
        )
        print(
            "##  ####  ##  ##  ##   ##  ####   ##   ##  ###  ##  ##  ##   ##  ##   ##  ### ##  ##   ##  #######  ##  ##   ##  ###    "
        )
        print(
            "##   ##   ##  ##  ##       ##     ##   ##  ##   ##  ##  ######   ##       ##  ##  ##   ##  ##   ##  ##  ##         #####"
        )
        print(
            "##        ##  ##  ##   ##  ##     ##   ##  ##   ##  ##  ##       ##   ##  ##  ##  ##  ###  ##   ##  ##  ##   ##  #   ###"
        )
        print(
            "##        ##  ##   #####   ##      #####   ##   ##  ##   #####    #####   ##  ##   ### ##  ##   ##  ##   #####    ##### "
        )
        print()
        print(
            "\033[91m*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|*~~*|\033[0m"
        )
        print(
            "                                                                                                                    2024"
        )
        print()
        print("\033[94mWelcome! This is Halpin-Tsai Micromechanics Analysis\033[0m")
        print(
            "                                                                                                                        "
        )
        print("Guidelines: help(argument) and press 'q' to exit from help function")
        print("Class: Isotropic , Transtropic, HT")
        print(
            "Instance method: HT.E1eff, HT.E2eff, HT.G12eff, HT.G23eff, HT.K23eff, "
            + "HT.v12eff"
        )
        print(
            "Function: display, plot, save, doc, compare, plot_compare, save_compare, "
            + "doc_compare\n"
        )
    else:
        # When imported from other code
        pass


def display(
    material: HT, min: int | float | None = None, max: int | float | None = None
) -> None:
    """Major Function:
    Print to screen A) constituent's elastic properties of UD composite, and B) the
    six effective elastic moduli of any UD composite versus i) full range, ii) custom
    range or iii) specific value of fiber volume fraction for quick in-situ
    micromechanics analysis.

    : param `material`: UD composite
    : type: HT
    : param `min`: The minimum inclusive value of fiber volume fraction range or
        specific value of fiber volume fraction
    : type: int | float | None
    : param `max`: The maximum inclusive value of fiber volume fraction range or None
        when only specific value of fiber volume fraction is defined
    : type: int | float | None
    : raise TypeError: When first argument, material is None or not HT type
    : raise ValueError: When min is None while max is not None, or when both min and max
        are not None but their values are not in between 0 and 1 and also, when value of
        min is greater than max value.
    : rtype: None

    Example 1: User simply displays the effective elastic properties of UD composite
        versus full range of fiber volume fraction
        >>>
        >>> composite = HT(carbon, epoxy)  # Instantiating ```HT``` object called 'composite'
        >>> display(composite)   # No request from user on fiber volume fraction, all range

        [1] UD COMPOSITE: Carbon-Epoxy

        I) Elastic Properties of Constituents:
        A) Fiber: Carbon
        +---------------+------------+--------------+-------------+--------------+-------------+----------------+
        | Constituent   |      Axial |   Transverse |       Axial |   Transverse |       Major |   Plane-strain |
        |               |    Young's |      Young's |       Shear |        Shear |   Poisson's |           Bulk |
        |               |   Modulus, |     Modulus, |    Modulus, |     Modulus, |      Ratio, |       Modulus, |
        |               |   E1 (GPa) |     E2 (GPa) |   G12 (GPa) |    G23 (GPa) |         v12 |      K23 (GPa) |
        +===============+============+==============+=============+==============+=============+================+
        | Carbon        |     250.00 |        25.00 |       20.00 |        10.00 |        0.28 |          17.02 |
        +---------------+------------+--------------+-------------+--------------+-------------+----------------+

        B) Matrix: Epoxy
        +---------------+------------+-------------+------------+-----------------+
        | Constituent   |    Young's |   Poisson's |      Shear |    Plane-strain |
        |               |   Modulus, |      Ratio, |   Modulus, |   Bulk Modulus, |
        |               |    E (GPa) |           v |    G (GPa) |         K (GPa) |
        +===============+============+=============+============+=================+
        | Epoxy         |       2.80 |        0.30 |       1.08 |            2.69 |
        +---------------+------------+-------------+------------+-----------------+

        II) Effective Elastic Properties of UD Composite:
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

    Example 2: User displays specific range of effective elastic moduli of UD composite
        based on specific range of fiber volume fraction of interest
        >>> display(composite, 0.5, 0.6)   # range of fiber volume fraction is specified

        [1] UD COMPOSITE: Carbon-Epoxy

        I) Elastic Properties of Constituents:
        A) Fiber: Carbon
        +---------------+------------+--------------+-------------+--------------+-------------+----------------+
        | Constituent   |      Axial |   Transverse |       Axial |   Transverse |       Major |   Plane-strain |
        |               |    Young's |      Young's |       Shear |        Shear |   Poisson's |           Bulk |
        |               |   Modulus, |     Modulus, |    Modulus, |     Modulus, |      Ratio, |       Modulus, |
        |               |   E1 (GPa) |     E2 (GPa) |   G12 (GPa) |    G23 (GPa) |         v12 |      K23 (GPa) |
        +===============+============+==============+=============+==============+=============+================+
        | Carbon        |     250.00 |        25.00 |       20.00 |        10.00 |        0.28 |          17.02 |
        +---------------+------------+--------------+-------------+--------------+-------------+----------------+

        B) Matrix: Epoxy
        +---------------+------------+-------------+------------+-----------------+
        | Constituent   |    Young's |   Poisson's |      Shear |    Plane-strain |
        |               |   Modulus, |      Ratio, |   Modulus, |   Bulk Modulus, |
        |               |    E (GPa) |           v |    G (GPa) |         K (GPa) |
        +===============+============+=============+============+=================+
        | Epoxy         |       2.80 |        0.30 |       1.08 |            2.69 |
        +---------------+------------+-------------+------------+-----------------+

        II) Effective Elastic Properties of UD Composite:
        +------+---------+---------+---------+--------+---------+---------+
        |   Vf |     E1* |     E2* |    G12* |   v12* |    G23* |    K23* |
        |      |   (GPa) |   (GPa) |   (GPa) |        |   (GPa) |   (GPa) |
        +======+=========+=========+=========+========+=========+=========+
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

        >>>

    Example 3: User specifies specific value of effective elastic moduli of UD composite
        based on a specific fiber volume fraction
        >>> display(composite, 0.5)   # single value of fiber volume fraction is specified

        [1] UD COMPOSITE: Carbon-Epoxy

        I) Elastic Properties of Constituents:
        A) Fiber: Carbon
        +---------------+------------+--------------+-------------+--------------+-------------+----------------+
        | Constituent   |      Axial |   Transverse |       Axial |   Transverse |       Major |   Plane-strain |
        |               |    Young's |      Young's |       Shear |        Shear |   Poisson's |           Bulk |
        |               |   Modulus, |     Modulus, |    Modulus, |     Modulus, |      Ratio, |       Modulus, |
        |               |   E1 (GPa) |     E2 (GPa) |   G12 (GPa) |    G23 (GPa) |         v12 |      K23 (GPa) |
        +===============+============+==============+=============+==============+=============+================+
        | Carbon        |     250.00 |        25.00 |       20.00 |        10.00 |        0.28 |          17.02 |
        +---------------+------------+--------------+-------------+--------------+-------------+----------------+

        B) Matrix: Epoxy
        +---------------+------------+-------------+------------+-----------------+
        | Constituent   |    Young's |   Poisson's |      Shear |    Plane-strain |
        |               |   Modulus, |      Ratio, |   Modulus, |   Bulk Modulus, |
        |               |    E (GPa) |           v |    G (GPa) |         K (GPa) |
        +===============+============+=============+============+=================+
        | Epoxy         |       2.80 |        0.30 |       1.08 |            2.69 |
        +---------------+------------+-------------+------------+-----------------+

        II) Effective Elastic Properties of UD Composite:
        +------+---------+---------+---------+--------+---------+---------+
        |   Vf |     E1* |     E2* |    G12* |   v12* |    G23* |    K23* |
        |      |   (GPa) |   (GPa) |   (GPa) |        |   (GPa) |   (GPa) |
        +======+=========+=========+=========+========+=========+=========+
        | 0.50 |  126.40 |    6.33 |    2.83 |   0.29 |    2.29 |    5.16 |
        +------+---------+---------+---------+--------+---------+---------+

        >>>

    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("The first argument must be HT object of UD composite")

    # Get and print main title
    print(_get_main_title_for_UD_composite(material))

    # Get fiber and matrix properties
    constituent_properties = _get_fiber_and_matrix_properties(material)

    # Get and print fiber's sub-title
    print(_get_sub_title_for_fiber(material))

    # Get and print fiber properties
    print(_print_tabulate(constituent_properties[0], "firstrow"))

    # Get and print matrix's sub-title
    print(_get_sub_title_for_matrix(material))

    # Get and print matrix properties
    print(_print_tabulate(constituent_properties[1], "firstrow"))

    # Get and print sub-title for composite' effective elastic properties
    print(_get_sub_title_for_composite(material))

    # Get and print all effective properties vs full range of fiber volume fraction
    if min is None and max is None:

        # Get compared properties versus a full range of fiber volume fraction
        eff_properties_dict = _get_effective_properties_versus_full_range_Vf(material)

        # Print properties
        print(_print_tabulate(eff_properties_dict, "keys"))
        print()

    # Get and print all effective properties vs specific value of fiber volume fraction
    elif (min is not None and max is None) or (
        min is not None and max is not None and min == max
    ):
        if not isinstance(min, int | float):
            raise TypeError(
                "Expected specific value of fiber volume fraction to be float number"
            )
        if min < 0 and min > 1:
            raise ValueError(
                "Expected specific value of fiber volume fraction in between 0 and 1"
            )

        # Get index number for specific value of fiber volume fraction
        idx: int = HT._fiber_volfract.index(
            Decimal(round(min, 2)).quantize(Decimal("1.000"))
        )

        # Get compared properties versus a specific value of fiber volume fraction
        eff_properties_list = _get_effective_properties_versus_specific_value_Vf(
            material, idx
        )

        # Print properties
        print(_print_tabulate(eff_properties_list, "firstrow"))
        print()

    # Print all effective properties versus specific range of fiber volume fraction
    elif min is not None and max is not None:
        if not isinstance(min, int | float) or not isinstance(max, int | float):
            raise TypeError(
                "Expected min and max value of fiber volume fraction range to be float "
                + "number"
            )
        if min < 0 or min > 1 or max < 0 or max > 1 or min > max:
            raise ValueError(
                "Expected min and max value of fiber volume fraction range in between "
                + "0 and 1 and also, min value to be smaller than max value"
            )

        # Get index number for start and end of fiber volume fraction range
        start: int = HT._fiber_volfract.index(
            Decimal(round(min, 2)).quantize(Decimal("1.000"))
        )
        end: int = HT._fiber_volfract.index(
            Decimal(round(max, 2)).quantize(Decimal("1.000"))
        )

        # Get compared properties versus a specific range of fiber volume fraction
        eff_properties_dict = _get_effective_properties_versus_specific_range_Vf(
            material, start, end
        )

        # Print properties
        print(_print_tabulate(eff_properties_dict, "keys"))
        print()

    # Other option
    else:
        raise ValueError(
            "Opss!"
            + "Either both min and max of fiber volume fraction range have value\n"
            + "or just min value for a specific fiber volume fraction and not range\n"
            + "or no min and max indicating full range of fiber volume fraction.\n"
            + "Pick one perhaps?"
        )


def _get_main_title_for_UD_composite(material: HT | None = None) -> str:
    """Get the main title that introduces name of UD composite in uppercase letters to
    be dislayed on console screen.

    Note: A helper function to ``display`` function.

    : param `material`: UD composite
    : type: ```HT``` | None
    : raise TypeError: If `material` is None or not ```HT``` object
    : return: Main title that displays the UD composite's name in uppercase letters.
    : rtype: str
    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("Expect argument to be UD composite and is of 'HT' object")

    # Return main title
    return f"\n[1] UD COMPOSITE: {(material.name).upper()}\n"


def _get_sub_title_for_fiber(material: HT | None = None) -> str:
    """Get the sub-title that introduces composite's fiber material to be displayed on
    console screen.

    Note: A helper function to ``display`` function.

    : param `material`: UD composite
    : type: ```HT``` | None
    : raise TypeError: If `material` is None or not ```HT``` object
    : return: Sub-title for display information about fiber material
    : rtype: str
    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("Expect argument to be UD composite and is of 'HT' object")

    # Return sub-title for fiber
    return f"\nA) Fiber material: {material.fiber.name}\n"


def _get_sub_title_for_matrix(material: HT | None = None) -> str:
    """Get the sub-title that introduces composite's matrix material to be displayed on
    console screen.

    Note: A helper function to ``display`` function.

    : param `material`: UD composite
    : type: ```HT``` | None
    : raise TypeError: If `material` is None or not ```HT``` object
    : return: Sub-title for display information about matrix material
    : rtype: str
    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("Expect argument to be UD composite and is of 'HT' object")

    # Return sub-title for matrix
    return f"\nB) Matrix material: {material.matrix.name}\n"


def _get_sub_title_for_composite(material: HT | None = None) -> str:
    """Get the sub-title that introduces UD composite's effective elastic moduli to be
    displayed on console screen.

    Note: A helper function to ``display`` function.

    : param `material`: UD composite
    : type: ```HT``` | None
    : raise TypeError: If `material` is None or not ```HT``` object
    : return: Sub-title for effective elastic moduli of UD composite material
    : rtype: str
    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("Expect argument to be UD composite and is of 'HT' object")

    # Return sub-title for effective elastic moduli for UD composite
    return f"\nC) Effective Elastic Moduli of {material.name}\n"


def _get_fiber_and_matrix_properties(material: HT | None = None) -> list:
    """Get the elastic moduli of fiber and matrix material of UD composite to be
    displayed on console screen.

    Note: A helper function to ``display`` function.

    : param `material`: UD composite
    : type: ```HT``` | None
    : raise TypeError: If `material` is None or not ```HT``` object
    : return: the effective elastic moduli of fiber and matrix
    : rtype: str

    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("Expect argument to be UD composite and is of 'HT' object")

    # Return data on the elastic moduli of fiber and matrix material
    return [
        [
            list((material.fiber._get_info()).keys()),
            list((material.fiber._get_info()).values()),
        ],
        [
            list((material.matrix._get_info()).keys()),
            list((material.matrix._get_info()).values()),
        ],
    ]


def _get_effective_properties_versus_full_range_Vf(material: HT | None = None) -> dict:
    """Get the full range of effective elastic moduli of UD composite based on the full
    range of fiber volume fraction to be displayed on console screen.

    Note: A helper function to ``display`` function.

    : param `material`: UD composite
    : type: ```HT``` | None
    : raise TypeError: If `material` is None or not ```HT``` object
    : return: Data on the effective elastic properties versus full range of fiber volume
        fraction
    : rtype: dict
    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("Expect argument to be UD composite and is of 'HT' object")

    # Return a dict of effective properties based on the full range of Vf
    return {
        "Vf": material.fiber_volfract,
        "E1*\n(GPa)": material.eff_axial_youngs_moduli,
        "E2*\n(GPa)": material.eff_transverse_youngs_moduli,
        "G12*\n(GPa)": material.eff_axial_shear_moduli,
        "v12*": material.eff_major_poissons_ratios,
        "G23*\n(GPa)": material.eff_transverse_shear_moduli,
        "K23*\n(GPa)": material.eff_pstrain_bulk_moduli,
    }


def _get_effective_properties_versus_specific_value_Vf(
    material: HT | None = None, idx: int | None = None
) -> list:
    """Get the specific value of effective elastic moduli of UD composite based on the
    specific value of fiber volume fraction to be displayed on console screen.

    Note: A helper function to ``display`` function.

    : param `material`: UD composite
    : type: ```HT``` | None
    : param `idx`: index number of a tuple of effective elastic modulus that correlates
        with the index number of a tuple of fiber volume fraction specified by user
    : type: int | None
    : raise TypeError: If `material` is None or not ```HT``` object, or if `idx` is
        None or not an int object
    : raise ValueError: if idx is negative and more than 100
    : return: Data on the effective elastic properties versus specific value of fiber
        volume fraction
    : rtype: list
    """
    # Check for TypeError and ValueError
    if material is None or not isinstance(material, HT):
        raise TypeError(
            "Expect first argument to be UD composite and is of 'HT' object"
        )
    if idx is None or not isinstance(idx, int):
        raise TypeError(
            "Expect second argument to be index number and is of an 'int' object"
        )
    if idx < 0 or idx > 100:
        raise ValueError("Expect index number is in between 0 and 100 inclusive.")

    # Organize data of fiber volume fraction versus effective elastic moduli
    eff_properties_1st_row: list = [
        "Vf",
        "E1*\n(GPa)",
        "E2*\n(GPa)",
        "G12*\n(GPa)",
        "v12*",
        "G23*\n(GPa)",
        "K23*\n(GPa)",
    ]
    eff_properties_2nd_row: list = [
        material.fiber_volfract[idx],
        material.eff_axial_youngs_moduli[idx],
        material.eff_transverse_youngs_moduli[idx],
        material.eff_axial_shear_moduli[idx],
        material.eff_major_poissons_ratios[idx],
        material.eff_transverse_shear_moduli[idx],
        material.eff_pstrain_bulk_moduli[idx],
    ]

    # Return a list of effective properties based on the specific value of Vf
    return [eff_properties_1st_row, eff_properties_2nd_row]


def _get_effective_properties_versus_specific_range_Vf(
    material: HT | None = None, start: int | None = None, end: int | None = None
) -> dict:
    """Get the specific range of effective elastic moduli of UD composite based on
    specific range of fiber volume fraction to be displayed on console screen.

    Note: A helper function to ``display`` function.

    : param `material`: UD composite
    : type: ```HT```
    : param `start`: index number of a tuple of effective elastic modulus that
        correlates with the index number of a starting value of fiber volume fraction
        range specified by user
    : type: int
    : param `end`: index number of a tuple of effective elastic modulus that
        correlates with the index number of an ending value of fiber volume fraction
        range specified by user
    : type: int
    : raise TypeError: If `material` is None or not ```HT``` object, or if either
        `start` and `end` is either None or not an int object
    : raise ValueError: If `start` < 0, of `start` > 100, of `start` > `end`, or
        `end` < 0, or `end` > 0, or `end` < `start`
    : return: Data on the effective elastic properties versus specific range of fiber
        volume fraction
    : rtype: dict
    """
    # Check for TypeError and ValueError
    if material is None or not isinstance(material, HT):
        raise TypeError(
            "Expect first argument to be UD composite and is of 'HT' object"
        )
    if start is None or not isinstance(start, int):
        raise TypeError(
            "Expect second argument to be index number and is of an 'int' object"
        )
    if end is None or not isinstance(end, int):
        raise TypeError(
            "Expect third argument to be index number and is of an 'int' object"
        )
    if start < 0 or start > 100 or start > end:
        raise ValueError(
            "Expect second argument of index number is in between 0 and 100 inclusive "
            + "and cannot exceed or equal to index number of third argument"
        )
    if end < 0 or end > 100 or end < start:
        raise ValueError(
            "Expect third argument of index number is in between 0 and 100 inclusive "
            + "and cannot exceed or equal to index number of second argument"
        )
    if start == end:
        raise ValueError(
            "Expect second and third argument to be different index number"
        )

    # Empty lists
    vf: list = []
    e1eff: list = []
    e2eff: list = []
    g12eff: list = []
    v12eff: list = []
    g23eff: list = []
    k23eff: list = []

    # Get effective values according to the range
    for i in range(start, end + 1):
        vf.append(material.fiber_volfract[i])
        e1eff.append(material.eff_axial_youngs_moduli[i])
        e2eff.append(material.eff_transverse_youngs_moduli[i])
        g12eff.append(material.eff_axial_shear_moduli[i])
        v12eff.append(material.eff_major_poissons_ratios[i])
        g23eff.append(material.eff_transverse_shear_moduli[i])
        k23eff.append(material.eff_pstrain_bulk_moduli[i])

    # Return a dict of effective properties based on the specific range of Vf
    return {
        "Vf": vf,
        "E1*\n(GPa)": e1eff,
        "E2*\n(GPa)": e2eff,
        "G12*\n(GPa)": g12eff,
        "v12*": v12eff,
        "G23*\n(GPa)": g23eff,
        "K23*\n(GPa)": k23eff,
    }


def _print_tabulate(
    properties: dict | list | None = None, fields: str | None = None
) -> str:
    """Return strings of stylish table format of data presentation of some properties to
    be displayed on console screen.

    Note: A helper function to both ``display`` and ``compare`` function.

    : param `properties`: Elastic properties which can be constituent's elastic
        constants or composite's effective elastic constants
    : type: dict | list | None
    : param `fields`: Headers format for tabulate printing
    : type: str | None
    : raise TypeError: If `properties` is None or not either list or dict object, or
        `fields` is None or not str object
    : raise ValueError: If `properties` is dict but `fields` is not 'keys', or
        if `properties` is list but its length not equal 2, or if `properties` is list
        of length 2 but its elements are zero length, or if `properties` is list of
        length 2 but its elements are not equal in size, or if `properties` is a valid
        list but `fields` is not 'firstrow'
    : return: tabulate table format
    : rtype: str
    """
    # Check for TypeError
    if properties is None or not isinstance(properties, dict | list):
        raise TypeError(
            "Expect first argument to be some elastic moduli and of either dict or "
            + "list object"
        )
    if fields is None or not isinstance(fields, str):
        raise TypeError(
            "Expect second argument to be headers style of tabulate format and a str "
            + "object"
        )
    if isinstance(properties, dict) and fields != "keys":
        raise ValueError(
            "If first argument is a dict object, expect second argument to be'keys' "
            + "only"
        )
    if isinstance(properties, list):
        if len(properties) != 2:
            raise ValueError(
                "If first argument is a list object, expect that it has a length of two"
            )
        if len(properties[0]) == 0:
            raise ValueError(
                "If first argument is a list object, expect that its elements not to "
                + "be zero length"
            )
        if len(properties[0]) != len(properties[1]):
            raise ValueError(
                "If first argument is a list object, expect that its elements are "
                + "equal in size"
            )
        if fields != "firstrow":
            raise ValueError(
                "If first argument is a valid list object, expect the second argument "
                + "to be 'firstrow' only"
            )

    # Return table of data
    return tabulate(properties, headers=fields, tablefmt="grid", floatfmt=".2f")


def compare(
    *materials: HT,
    property: str = "E1eff",
    min: int | float | None = None,
    max: int | float | None = None,
) -> None:
    """Print to screen A) only the relevant elastic moduli of fiber and matrix that
    influence the effective elastic property for qualitative comparison assessment, and
    B) the specific user-defined effective elastic property for every UD composites
    under comparison versus either i) full range, ii) custom range or iii) specific
    value of fiber volume fraction for quick in-situ micromechanics comparison analysis.
    In addition, the values of effective property will always be compared to the values
    of baseline UD composite to get the percentage difference values for qualitative
    assessments where this baseline material will always be the one that is first
    specified in the argument of this compare function.

    : param `material`: UD composites that will be compared
    : type: ```HT```
    : param `property`: User-defined effective elastic property that becomes the subject
        of comparison
    : type: str
    : param `min`: The starting inclusive value of fiber volume fraction range or
        specific value of fiber volume fraction
    : type: int | float | None
    : param `max`: The ending inclusive value of fiber volume fraction range or None
        when specific value of fiber volume fraction is defined as min
    : type: int | float | None
    : raise TypeError: When first argument - material is None or not HT type
    : raise ValueError: When property is not one of the followings: 'E1eff', 'E2eff',
        'G21eff', 'v12eff', 'G23eff', 'K23eff', when min is None while max is not
        None, or when both min and max are not None but their values are not in between
        0 and 1 and also, when min value is greater than max value.
    : rtype: None

    Example 1: Comparison of 4 UD composites of default property - "E1eff" with default
        full range of fiber volume faction

        >>> carbon = Transtropic("Carbon", 250, 25, 20, 10, .28)
        >>> fiberglass = Isotropic("Fiberglass", 120, .29)
        >>> epoxy = Isotropic("Epoxy", 2.8, .3)
        >>> phenolic = Isotropic("Phenolic", 5, .3)
        >>> compositeA = HT(carbon, phenolic)
        >>> compositeB = HT(carbon, epoxy)
        >>> compositeC = HT(fiberglass,phenolic)
        >>> compositeD = HT(fiberglass, epoxy)
        >>> compare(compositeA, compositeB, compositeC, compositeD)

        A) 4 UD Composites for Comparison Analysis

        [1] - CARBON-PHENOLIC
        [2] - CARBON-EPOXY
        [3] - FIBERGLASS-PHENOLIC
        [4] - FIBERGLASS-EPOXY

        B) 4 Fibers of UD Composites

        [1] : Carbon - Transtropic
        [2] : Carbon - Transtropic
        [3] : Fiberglass - Isotropic
        [4] : Fiberglass - Isotropic

        i) 4 Fibers on Young's / Axial Young's Modulus Comparison

        +---------------------------------+----------+----------+--------------+--------------+
        | Fiber Material                  |      [1] |      [2] |          [3] |          [4] |
        |                                 |   Carbon |   Carbon |   Fiberglass |   Fiberglass |
        +=================================+==========+==========+==============+==============+
        | Young's Modulus, E or           |   250.00 |   250.00 |       120.00 |       120.00 |
        | Axial Young's Modulus, E1 (GPa) |          |          |              |              |
        +---------------------------------+----------+----------+--------------+--------------+

        C) 4 Matrices of UD Composites

        [1] : Phenolic - Isotropic
        [2] : Epoxy - Isotropic
        [3] : Phenolic - Isotropic
        [4] : Epoxy - Isotropic

        i) 4 Matrices on Young's / Axial Young's Modulus Comparison

        +---------------------------------+------------+---------+------------+---------+
        | Matrix Material                 |        [1] |     [2] |        [3] |     [4] |
        |                                 |   Phenolic |   Epoxy |   Phenolic |   Epoxy |
        +=================================+============+=========+============+=========+
        | Young's Modulus, E or           |       5.00 |    2.80 |       5.00 |    2.80 |
        | Axial Young's Modulus, E1 (GPa) |            |         |            |         |
        +---------------------------------+------------+---------+------------+---------+

        D) Comparison of Effective Elastic Property of 4 UD Composites

        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        |   Vf |     [1] |     [2] |     diff. of |     [3] |     diff. of |     [4] |     diff. of |
        |      |     E1* |     E1* |   [2] to [1] |     E1* |   [3] to [1] |     E1* |   [4] to [1] |
        |      |   (GPa) |   (GPa) |          (%) |   (GPa) |          (%) |   (GPa) |          (%) |
        +======+=========+=========+==============+=========+==============+=========+==============+
        | 0.00 |    5.00 |    2.80 |       -44.00 |    5.00 |         0.00 |    2.80 |       -44.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.01 |    7.45 |    5.27 |       -29.20 |    6.15 |       -17.40 |    3.97 |       -46.70 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.02 |    9.90 |    7.74 |       -21.80 |    7.30 |       -26.30 |    5.14 |       -48.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.03 |   12.35 |   10.22 |       -17.30 |    8.45 |       -31.60 |    6.32 |       -48.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.04 |   14.80 |   12.69 |       -14.30 |    9.60 |       -35.10 |    7.49 |       -49.40 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.05 |   17.25 |   15.16 |       -12.10 |   10.75 |       -37.70 |    8.66 |       -49.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.06 |   19.70 |   17.63 |       -10.50 |   11.90 |       -39.60 |    9.83 |       -50.10 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.07 |   22.15 |   20.10 |        -9.20 |   13.05 |       -41.10 |   11.00 |       -50.30 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.08 |   24.60 |   22.58 |        -8.20 |   14.20 |       -42.30 |   12.18 |       -50.50 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.09 |   27.05 |   25.05 |        -7.40 |   15.35 |       -43.30 |   13.35 |       -50.70 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.10 |   29.50 |   27.52 |        -6.70 |   16.50 |       -44.10 |   14.52 |       -50.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.11 |   31.95 |   29.99 |        -6.10 |   17.65 |       -44.80 |   15.69 |       -50.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.12 |   34.40 |   32.46 |        -5.60 |   18.80 |       -45.30 |   16.86 |       -51.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.13 |   36.85 |   34.94 |        -5.20 |   19.95 |       -45.90 |   18.04 |       -51.10 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.14 |   39.30 |   37.41 |        -4.80 |   21.10 |       -46.30 |   19.21 |       -51.10 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.15 |   41.75 |   39.88 |        -4.50 |   22.25 |       -46.70 |   20.38 |       -51.20 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.16 |   44.20 |   42.35 |        -4.20 |   23.40 |       -47.10 |   21.55 |       -51.20 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.17 |   46.65 |   44.82 |        -3.90 |   24.55 |       -47.40 |   22.72 |       -51.30 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.18 |   49.10 |   47.30 |        -3.70 |   25.70 |       -47.70 |   23.90 |       -51.30 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.19 |   51.55 |   49.77 |        -3.50 |   26.85 |       -47.90 |   25.07 |       -51.40 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.20 |   54.00 |   52.24 |        -3.30 |   28.00 |       -48.10 |   26.24 |       -51.40 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.21 |   56.45 |   54.71 |        -3.10 |   29.15 |       -48.40 |   27.41 |       -51.40 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.22 |   58.90 |   57.18 |        -2.90 |   30.30 |       -48.60 |   28.58 |       -51.50 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.23 |   61.35 |   59.66 |        -2.80 |   31.45 |       -48.70 |   29.76 |       -51.50 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.24 |   63.80 |   62.13 |        -2.60 |   32.60 |       -48.90 |   30.93 |       -51.50 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.25 |   66.25 |   64.60 |        -2.50 |   33.75 |       -49.10 |   32.10 |       -51.50 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.26 |   68.70 |   67.07 |        -2.40 |   34.90 |       -49.20 |   33.27 |       -51.60 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.27 |   71.15 |   69.54 |        -2.30 |   36.05 |       -49.30 |   34.44 |       -51.60 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.28 |   73.60 |   72.02 |        -2.20 |   37.20 |       -49.50 |   35.62 |       -51.60 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.29 |   76.05 |   74.49 |        -2.10 |   38.35 |       -49.60 |   36.79 |       -51.60 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.30 |   78.50 |   76.96 |        -2.00 |   39.50 |       -49.70 |   37.96 |       -51.60 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.31 |   80.95 |   79.43 |        -1.90 |   40.65 |       -49.80 |   39.13 |       -51.70 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.32 |   83.40 |   81.90 |        -1.80 |   41.80 |       -49.90 |   40.30 |       -51.70 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.33 |   85.85 |   84.38 |        -1.70 |   42.95 |       -50.00 |   41.48 |       -51.70 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.34 |   88.30 |   86.85 |        -1.60 |   44.10 |       -50.10 |   42.65 |       -51.70 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.35 |   90.75 |   89.32 |        -1.60 |   45.25 |       -50.10 |   43.82 |       -51.70 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.36 |   93.20 |   91.79 |        -1.50 |   46.40 |       -50.20 |   44.99 |       -51.70 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.37 |   95.65 |   94.26 |        -1.40 |   47.55 |       -50.30 |   46.16 |       -51.70 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.38 |   98.10 |   96.74 |        -1.40 |   48.70 |       -50.40 |   47.34 |       -51.70 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.39 |  100.55 |   99.21 |        -1.30 |   49.85 |       -50.40 |   48.51 |       -51.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.40 |  103.00 |  101.68 |        -1.30 |   51.00 |       -50.50 |   49.68 |       -51.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.41 |  105.45 |  104.15 |        -1.20 |   52.15 |       -50.50 |   50.85 |       -51.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.42 |  107.90 |  106.62 |        -1.20 |   53.30 |       -50.60 |   52.02 |       -51.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.43 |  110.35 |  109.10 |        -1.10 |   54.45 |       -50.70 |   53.20 |       -51.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.44 |  112.80 |  111.57 |        -1.10 |   55.60 |       -50.70 |   54.37 |       -51.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.45 |  115.25 |  114.04 |        -1.00 |   56.75 |       -50.80 |   55.54 |       -51.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.46 |  117.70 |  116.51 |        -1.00 |   57.90 |       -50.80 |   56.71 |       -51.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.47 |  120.15 |  118.98 |        -1.00 |   59.05 |       -50.90 |   57.88 |       -51.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.48 |  122.60 |  121.46 |        -0.90 |   60.20 |       -50.90 |   59.06 |       -51.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.49 |  125.05 |  123.93 |        -0.90 |   61.35 |       -50.90 |   60.23 |       -51.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.50 |  127.50 |  126.40 |        -0.90 |   62.50 |       -51.00 |   61.40 |       -51.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.51 |  129.95 |  128.87 |        -0.80 |   63.65 |       -51.00 |   62.57 |       -51.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.52 |  132.40 |  131.34 |        -0.80 |   64.80 |       -51.10 |   63.74 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.53 |  134.85 |  133.82 |        -0.80 |   65.95 |       -51.10 |   64.92 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.54 |  137.30 |  136.29 |        -0.70 |   67.10 |       -51.10 |   66.09 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.55 |  139.75 |  138.76 |        -0.70 |   68.25 |       -51.20 |   67.26 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.56 |  142.20 |  141.23 |        -0.70 |   69.40 |       -51.20 |   68.43 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.57 |  144.65 |  143.70 |        -0.70 |   70.55 |       -51.20 |   69.60 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.58 |  147.10 |  146.18 |        -0.60 |   71.70 |       -51.30 |   70.78 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.59 |  149.55 |  148.65 |        -0.60 |   72.85 |       -51.30 |   71.95 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.60 |  152.00 |  151.12 |        -0.60 |   74.00 |       -51.30 |   73.12 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.61 |  154.45 |  153.59 |        -0.60 |   75.15 |       -51.30 |   74.29 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.62 |  156.90 |  156.06 |        -0.50 |   76.30 |       -51.40 |   75.46 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.63 |  159.35 |  158.54 |        -0.50 |   77.45 |       -51.40 |   76.64 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.64 |  161.80 |  161.01 |        -0.50 |   78.60 |       -51.40 |   77.81 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.65 |  164.25 |  163.48 |        -0.50 |   79.75 |       -51.40 |   78.98 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.66 |  166.70 |  165.95 |        -0.40 |   80.90 |       -51.50 |   80.15 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.67 |  169.15 |  168.42 |        -0.40 |   82.05 |       -51.50 |   81.32 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.68 |  171.60 |  170.90 |        -0.40 |   83.20 |       -51.50 |   82.50 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.69 |  174.05 |  173.37 |        -0.40 |   84.35 |       -51.50 |   83.67 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.70 |  176.50 |  175.84 |        -0.40 |   85.50 |       -51.60 |   84.84 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.71 |  178.95 |  178.31 |        -0.40 |   86.65 |       -51.60 |   86.01 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.72 |  181.40 |  180.78 |        -0.30 |   87.80 |       -51.60 |   87.18 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.73 |  183.85 |  183.26 |        -0.30 |   88.95 |       -51.60 |   88.36 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.74 |  186.30 |  185.73 |        -0.30 |   90.10 |       -51.60 |   89.53 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.75 |  188.75 |  188.20 |        -0.30 |   91.25 |       -51.70 |   90.70 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.76 |  191.20 |  190.67 |        -0.30 |   92.40 |       -51.70 |   91.87 |       -51.90 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.77 |  193.65 |  193.14 |        -0.30 |   93.55 |       -51.70 |   93.04 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.78 |  196.10 |  195.62 |        -0.20 |   94.70 |       -51.70 |   94.22 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.79 |  198.55 |  198.09 |        -0.20 |   95.85 |       -51.70 |   95.39 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.80 |  201.00 |  200.56 |        -0.20 |   97.00 |       -51.70 |   96.56 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.81 |  203.45 |  203.03 |        -0.20 |   98.15 |       -51.80 |   97.73 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.82 |  205.90 |  205.50 |        -0.20 |   99.30 |       -51.80 |   98.90 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.83 |  208.35 |  207.98 |        -0.20 |  100.45 |       -51.80 |  100.08 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.84 |  210.80 |  210.45 |        -0.20 |  101.60 |       -51.80 |  101.25 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.85 |  213.25 |  212.92 |        -0.20 |  102.75 |       -51.80 |  102.42 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.86 |  215.70 |  215.39 |        -0.10 |  103.90 |       -51.80 |  103.59 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.87 |  218.15 |  217.86 |        -0.10 |  105.05 |       -51.80 |  104.76 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.88 |  220.60 |  220.34 |        -0.10 |  106.20 |       -51.90 |  105.94 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.89 |  223.05 |  222.81 |        -0.10 |  107.35 |       -51.90 |  107.11 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.90 |  225.50 |  225.28 |        -0.10 |  108.50 |       -51.90 |  108.28 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.91 |  227.95 |  227.75 |        -0.10 |  109.65 |       -51.90 |  109.45 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.92 |  230.40 |  230.22 |        -0.10 |  110.80 |       -51.90 |  110.62 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.93 |  232.85 |  232.70 |        -0.10 |  111.95 |       -51.90 |  111.80 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.94 |  235.30 |  235.17 |        -0.10 |  113.10 |       -51.90 |  112.97 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.95 |  237.75 |  237.64 |        -0.00 |  114.25 |       -51.90 |  114.14 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.96 |  240.20 |  240.11 |        -0.00 |  115.40 |       -52.00 |  115.31 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.97 |  242.65 |  242.58 |        -0.00 |  116.55 |       -52.00 |  116.48 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.98 |  245.10 |  245.06 |        -0.00 |  117.70 |       -52.00 |  117.66 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.99 |  247.55 |  247.53 |        -0.00 |  118.85 |       -52.00 |  118.83 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 1.00 |  250.00 |  250.00 |         0.00 |  120.00 |       -52.00 |  120.00 |       -52.00 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+

        >>>

    Example 2: Comparison between 4 UD composites on user defined value of property
        - "G12eff" based on specific range of fiber volume fraction - (0.5, 0.55)

        >>> compare(compositeA, compositeB, compositeC, compositeD, property="G12eff", min=0.5, max=0.55)

        A) 4 UD Composites for Comparison Analysis

        [1] - CARBON-PHENOLIC
        [2] - CARBON-EPOXY
        [3] - FIBERGLASS-PHENOLIC
        [4] - FIBERGLASS-EPOXY

        B) 4 Fibers of UD Composites

        [1] : Carbon - Transtropic
        [2] : Carbon - Transtropic
        [3] : Fiberglass - Isotropic
        [4] : Fiberglass - Isotropic

        i) 4 Fibers on Shear / Axial Shear Modulus Comparison

        +--------------------------------+----------+----------+--------------+--------------+
        | Fiber Material                 |      [1] |      [2] |          [3] |          [4] |
        |                                |   Carbon |   Carbon |   Fiberglass |   Fiberglass |
        +================================+==========+==========+==============+==============+
        | Shear Modulus, G or            |    20.00 |    20.00 |        46.51 |        46.51 |
        | Axial Shear Modulus, G12 (GPa) |          |          |              |              |
        +--------------------------------+----------+----------+--------------+--------------+

        C) 4 Matrices of UD Composites

        [1] : Phenolic - Isotropic
        [2] : Epoxy - Isotropic
        [3] : Phenolic - Isotropic
        [4] : Epoxy - Isotropic

        i) 4 Matrices on Shear / Axial Shear Modulus Comparison

        +--------------------------------+------------+---------+------------+---------+
        | Matrix Material                |        [1] |     [2] |        [3] |     [4] |
        |                                |   Phenolic |   Epoxy |   Phenolic |   Epoxy |
        +================================+============+=========+============+=========+
        | Shear Modulus, G or            |       1.92 |    1.08 |       1.92 |    1.08 |
        | Axial Shear Modulus, G12 (GPa) |            |         |            |         |
        +--------------------------------+------------+---------+------------+---------+

        D) Comparison of Effective Elastic Property of 4 UD Composites

        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        |   Vf |     [1] |     [2] |     diff. of |     [3] |     diff. of |     [4] |     diff. of |
        |      |    G12* |    G12* |   [2] to [1] |    G12* |   [3] to [1] |    G12* |   [4] to [1] |
        |      |   (GPa) |   (GPa) |          (%) |   (GPa) |          (%) |   (GPa) |          (%) |
        +======+=========+=========+==============+=========+==============+=========+==============+
        | 0.50 |    4.62 |    2.83 |       -38.70 |    5.20 |        12.60 |    3.04 |       -34.10 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.51 |    4.71 |    2.90 |       -38.60 |    5.33 |        13.00 |    3.12 |       -33.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.52 |    4.81 |    2.96 |       -38.40 |    5.46 |        13.40 |    3.20 |       -33.50 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.53 |    4.91 |    3.03 |       -38.20 |    5.59 |        13.80 |    3.28 |       -33.10 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.54 |    5.01 |    3.10 |       -38.00 |    5.72 |        14.30 |    3.37 |       -32.80 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        | 0.55 |    5.12 |    3.18 |       -37.90 |    5.87 |        14.70 |    3.46 |       -32.40 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+

        >>>

    Example 3: Comparison between 4 UD composites on user-defined specific property -
        'G23eff' with user-defined specific value on fiber volume fraction - 0.5

        >>> compare(compositeA, compositeB, compositeC, compositeD, property="G23eff", min=0.5)

        A) 4 UD Composites for Comparison Analysis

        [1] - CARBON-PHENOLIC
        [2] - CARBON-EPOXY
        [3] - FIBERGLASS-PHENOLIC
        [4] - FIBERGLASS-EPOXY

        B) 4 Fibers of UD Composites

        [1] : Carbon - Transtropic
        [2] : Carbon - Transtropic
        [3] : Fiberglass - Isotropic
        [4] : Fiberglass - Isotropic

        i) 4 Fibers on Shear / Transverse Shear Modulus Comparison

        +-------------------------------------+----------+----------+--------------+--------------+
        | Fiber Material                      |      [1] |      [2] |          [3] |          [4] |
        |                                     |   Carbon |   Carbon |   Fiberglass |   Fiberglass |
        +=====================================+==========+==========+==============+==============+
        | Shear Modulus, G or                 |    10.00 |    10.00 |        46.51 |        46.51 |
        | Transverse Shear Modulus, G23 (GPa) |          |          |              |              |
        +-------------------------------------+----------+----------+--------------+--------------+

        ii) 4 Fibers on Plane-Strain Bulk Modulus Comparison

        +--------------------------------------+----------+----------+--------------+--------------+
        | Fiber Material                       |      [1] |      [2] |          [3] |          [4] |
        |                                      |   Carbon |   Carbon |   Fiberglass |   Fiberglass |
        +======================================+==========+==========+==============+==============+
        | Plane-Strain Bulk Modulus, K23 (GPa) |    17.02 |    17.02 |       110.74 |       110.74 |
        +--------------------------------------+----------+----------+--------------+--------------+

        C) 4 Matrices of UD Composites

        [1] : Phenolic - Isotropic
        [2] : Epoxy - Isotropic
        [3] : Phenolic - Isotropic
        [4] : Epoxy - Isotropic

        i) 4 Matrices on Shear / Transverse Shear Modulus Comparison

        +-------------------------------------+------------+---------+------------+---------+
        | Matrix Material                     |        [1] |     [2] |        [3] |     [4] |
        |                                     |   Phenolic |   Epoxy |   Phenolic |   Epoxy |
        +=====================================+============+=========+============+=========+
        | Shear Modulus, G or                 |       1.92 |    1.08 |       1.92 |    1.08 |
        | Transverse Shear Modulus, G23 (GPa) |            |         |            |         |
        +-------------------------------------+------------+---------+------------+---------+

        ii) 4 Matrices on Plane-Strain Bulk Modulus Comparison

        +--------------------------------------+------------+---------+------------+---------+
        | Matrix Material                      |        [1] |     [2] |        [3] |     [4] |
        |                                      |   Phenolic |   Epoxy |   Phenolic |   Epoxy |
        +======================================+============+=========+============+=========+
        | Plane-Strain Bulk Modulus, K23 (GPa) |       4.81 |    2.69 |       4.81 |    2.69 |
        +--------------------------------------+------------+---------+------------+---------+

        D) Comparison of Effective Elastic Property of 4 UD Composites

        +------+---------+---------+--------------+---------+--------------+---------+--------------+
        |   Vf |     [1] |     [2] |     diff. of |     [3] |     diff. of |     [4] |     diff. of |
        |      |    G23* |    G23* |   [2] to [1] |    G23* |   [3] to [1] |    G23* |   [4] to [1] |
        |      |   (GPa) |   (GPa) |          (%) |   (GPa) |          (%) |   (GPa) |          (%) |
        +======+=========+=========+==============+=========+==============+=========+==============+
        | 0.50 |    3.64 |    2.29 |       -37.00 |    4.56 |        25.20 |    2.64 |       -27.60 |
        +------+---------+---------+--------------+---------+--------------+---------+--------------+

        >>>
    """
    # Check for TypeError and ValueError
    if len(materials) == 0:
        raise ValueError("Expect 'HT' object - UD composite material")
    for material in materials:
        if not isinstance(material, HT):
            raise TypeError("The first argument must be HT object of UD composite")
    if property not in ["E1eff", "E2eff", "G12eff", "v12eff", "G23eff", "K23eff"]:
        raise ValueError(
            "Expected one of these options - 'E1eff', 'E2eff', 'G12eff', 'v12eff', "
            + "'G23eff', 'K23eff'"
        )
    if min is None and max is not None:
        raise TypeError(
            "Opss!"
            + "Either both min and max of fiber volume fraction range have value\n"
            + "or just min value for a specific fiber volume fraction and not range\n"
            + "or no min and max indicating full range of fiber volume fraction.\n"
            + "Pick one option perhaps?"
        )

    # Get and print title to introduces number of UD composites being compared
    print(_get_main_title(materials))

    # Get and print all UD composites' number and name for identification purposes
    numbers_and_names_of_composites: list = _get_numbers_and_names_of_composites(
        materials
    )
    for number_and_name in numbers_and_names_of_composites:
        print(number_and_name)

    # Get and print sub-title to introduces fibers of UD composites
    print(_get_sub_title_fibers(materials))

    # Get and print all fibers' number and name for identification purposes
    numbers_and_names_of_fibers: list = _get_numbers_and_names_fibers(materials)
    for number_and_name in numbers_and_names_of_fibers:
        print(number_and_name)

    # Print relevant user-defined elastic modulus of fiber that influence the effective
    # elastic modulus according to Halpin-Tsai formula
    match property:

        # For relevant constituent elastic moduli that influence E1eff
        case "E1eff":
            # Get and print sub-sub-title for fibers' axial Young modulus
            print(_get_sub_sub_title_fiber_axial_youngs_modulus(materials))

            # Get all fibers' axial Young's modulus for comparison
            fibers_axial_youngs_modulus_list: list = _get_fibers_axial_youngs_modulus(
                materials
            )

            # Print comparison table for fibers' axial Young's modulus
            print(_print_tabulate(fibers_axial_youngs_modulus_list, "firstrow"))

        # For relevant constituent elastic moduli that influence E2eff
        case "E2eff":
            # Get and print sub-sub-title for fibers' transverse Young modulus
            print(_get_sub_sub_title_fiber_transverse_youngs_modulus(materials))

            # Get all fibers' transverse Young's modulus for comparison
            fibers_transverse_youngs_modulus_list: list = (
                _get_fibers_transverse_youngs_modulus(materials)
            )

            # Print comparison table for fibers' transverse Young's modulus
            print(_print_tabulate(fibers_transverse_youngs_modulus_list, "firstrow"))

        # For relevant constituent elastic moduli that influence G12eff
        case "G12eff":
            # Get and print sub-sub-title for fibers' axial shear modulus
            print(_get_sub_sub_title_fiber_axial_shear_modulus(materials))

            # Get all fibers' axial shear modulus for comparison
            fibers_axial_shear_modulus_list: list = _get_fibers_axial_shear_modulus(
                materials
            )

            # Print comparison table for fibers' axial shear modulus
            print(_print_tabulate(fibers_axial_shear_modulus_list, "firstrow"))

        # For relevant constituent elastic moduli that influence v12eff
        case "v12eff":
            # Get and print sub-sub-title for fibers' major Poisson's ratio
            print(_get_sub_sub_title_fiber_major_poissons_ratio(materials))

            # Get all fibers' major Poisson's ratio for comparison
            fibers_major_poissons_ratio_list: list = _get_fibers_major_poissons_ratio(
                materials
            )

            # Print comparison table for fibers' major Poisson's ratio
            print(_print_tabulate(fibers_major_poissons_ratio_list, "firstrow"))

        # For relevant constituent elastic moduli that influence G23eff and K23eff
        case "G23eff" | "K23eff":
            # Get and print sub-sub-title for fibers' transverse shear modulus
            print(_get_sub_sub_title_fiber_transverse_shear_modulus(materials))

            # Get all fibers' transverse shear modulus for comparison
            fibers_transverse_shear_modulus_list: list = (
                _get_fibers_transverse_shear_modulus(materials)
            )

            # Print comparison table for fibers' transverse shear modulus
            print(_print_tabulate(fibers_transverse_shear_modulus_list, "firstrow"))

            # Get and print sub-sub-title for fibers' plane-strain bulk modulus
            print(_get_sub_sub_title_fiber_pstrain_bulk_modulus(materials))

            # Get all fibers' plane-strain bulk modulus for comparison
            fibers_pstrain_bulk_modulus_list: list = _get_fibers_pstrain_bulk_modulus(
                materials
            )

            # Print comparison table for fibers' plane-strain bulk modulus
            print(_print_tabulate(fibers_pstrain_bulk_modulus_list, "firstrow"))

    # Get and print sub-title to introduces matrices of UD composites
    print(_get_sub_title_matrices(materials))

    # Get and print all matrices' number and name for identification purposes
    numbers_and_names_of_matrices: list = _get_numbers_and_names_matrices(materials)
    for number_and_name in numbers_and_names_of_matrices:
        print(number_and_name)

    # Print relevant elastic modulus of matrix that affects the effective elastic
    # modulus specified by user
    match property:

        # For relevant constituent elastic moduli that influence E1eff
        case "E1eff":
            # Get and print sub-sub-title for matrices' axial Young modulus
            print(_get_sub_sub_title_matrix_axial_youngs_modulus(materials))

            # Get all matrices' axial Young's modulus for comparison
            matrices_axial_youngs_modulus_list: list = (
                _get_matrices_axial_youngs_modulus(materials)
            )

            # Print comparison table for matrices' axial Young's modulus
            print(_print_tabulate(matrices_axial_youngs_modulus_list, "firstrow"))

        # For relevant constituent elastic moduli that influence E2eff
        case "E2eff":
            # Get and print sub-sub-title for matrices' transverse Young modulus
            print(_get_sub_sub_title_matrix_transverse_youngs_modulus(materials))

            # Get all matrices' transverse Young's modulus for comparison
            matrices_transverse_youngs_modulus_list: list = (
                _get_matrices_transverse_youngs_modulus(materials)
            )

            # Print comparison table for matrices' transverse Young's modulus
            print(_print_tabulate(fibers_transverse_youngs_modulus_list, "firstrow"))

        # For relevant constituent elastic moduli that influence G12eff
        case "G12eff":
            # Get and print sub-sub-title for matrices' axial shear modulus
            print(_get_sub_sub_title_matrix_axial_shear_modulus(materials))

            # Get all matrices' axial shear modulus for comparison
            matrices_axial_shear_modulus_list: list = _get_matrices_axial_shear_modulus(
                materials
            )

            # Print comparison table for matrices' axial shear modulus
            print(_print_tabulate(matrices_axial_shear_modulus_list, "firstrow"))

        # For relevant constituent elastic moduli that influence v12eff
        case "v12eff":
            # Get and print sub-sub-title for matrices' major Poisson's ratio
            print(_get_sub_sub_title_matrix_major_poissons_ratio(materials))

            # Get all matrices' major Poisson's ratio for comparison
            matrices_major_poissons_ratio_list: list = (
                _get_matrices_major_poissons_ratio(materials)
            )

            # Print comparison table for matrices' major Poisson's ratio
            print(_print_tabulate(matrices_major_poissons_ratio_list, "firstrow"))

        # For relevant constituent elastic moduli that influence G23eff and K23eff
        case "G23eff" | "K23eff":
            # Get and print sub-sub-title for matrices' transverse shear modulus
            print(_get_sub_sub_title_matrix_transverse_shear_modulus(materials))

            # Get all matrices' transverse shear modulus for comparison
            matrices_transverse_shear_modulus_list: list = (
                _get_matrices_transverse_shear_modulus(materials)
            )

            # Print comparison table for matrices's transverse shear modulus
            print(_print_tabulate(matrices_transverse_shear_modulus_list, "firstrow"))

            # Get and print sub-sub-title for matrices' plane-strain bulk modulus
            print(_get_sub_sub_title_matrix_pstrain_bulk_modulus(materials))

            # Get all matrices' plane-strain bulk modulus for comparison
            matrices_pstrain_bulk_modulus_list: list = (
                _get_matrices_pstrain_bulk_modulus(materials)
            )

            # Print comparison table for matrices' plane-strain bulk modulus
            print(_print_tabulate(matrices_pstrain_bulk_modulus_list, "firstrow"))

    # Get and print introduction title of effective elastic properties of UD composite
    print(_get_sub_title_effective_elastic_properties(materials))

    # Get and print data on comparison property versus a full range of fiber volume
    # fraction based on user-defined `property`
    if min is None and max is None:
        # Organized comparison property on full range of fiber volume fraction
        compared_properties_dict: dict = (
            _get_comparison_specific_property_full_range_Vf(materials, property)
        )

        # Print data in table format
        print(_print_tabulate(compared_properties_dict, "keys"))
        print()

    # Get and print data on comparison property versus a specific value of fiber volume
    # fraction based on user-defined `property`
    elif (min is not None and max is None) or (
        min is not None and max is not None and min == max
    ):
        # Check for TypeError & ValueError
        if not isinstance(min, int | float):
            raise TypeError(
                "Expected specific value of fiber volume fraction to be float number"
            )
        if min < 0 and min > 1:
            raise ValueError(
                "Expected specific value of fiber volume fraction in between 0 and 1"
            )
        # Get index number of specific value of fiber volume fraction
        idx: int = HT._fiber_volfract.index(
            Decimal(round(min, 2)).quantize(Decimal("1.000"))
        )
        # Get comparison property on specific value of fiber volume fraction
        compared_properties_list = _get_comparison_specific_property_specific_value_Vf(
            materials, property, idx
        )
        # Print data in table format
        print(_print_tabulate(compared_properties_list, "firstrow"))
        print()

    # Get and print data on comparison property versus a specific range of fiber volume
    # fraction based on user-defined `property`
    else:
        # Check for TypeError & ValueError
        if not isinstance(min, int | float) or not isinstance(max, int | float):
            raise TypeError(
                "Expected min and max value of fiber volume fraction range to be float "
                + "number"
            )
        if min < 0 or min > 1 or max < 0 or max > 1 or min > max:
            raise ValueError(
                "Expected min and max value of fiber volume fraction range in between "
                + "0 and 1 and also, min value to be smaller than max value"
            )

        # Get index number for start and end of fiber volume fraction range
        start: int = HT._fiber_volfract.index(
            Decimal(round(min, 2)).quantize(Decimal("1.000"))
        )
        end: int = HT._fiber_volfract.index(
            Decimal(round(max, 2)).quantize(Decimal("1.000"))
        )
        # Get comparison property on specific range of fiber volume fraction
        compared_properties_dict = _get_comparison_specific_property_specific_range_Vf(
            materials, property, start, end
        )
        # Print data in table format
        print(_print_tabulate(compared_properties_dict, "keys"))
        print()


def _get_main_title(materials: tuple[HT, ...]) -> str:
    """Get the main title of comparison analysis on the number of UD composites being
    compared to be displayed on console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The main title showing how many UD composites being compared
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return main title
    return f"\nA) {len(materials)} UD Composites for Comparison Analysis\n"


def _get_numbers_and_names_of_composites(materials: tuple[HT, ...]) -> list:
    """Get the numbering system for every composite being compared together with their
    names for the purpose identification when tabling the comparison data on console
    screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The numbering system assigned to each composite for identification
        associated with names for comparison purposes in table format.
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize numbers and names for every UD composites
    numbers_and_names_ud_composites = []
    for i in range(len(materials)):
        numbers_and_names_ud_composites.append(
            f"[{i+1}] - {(materials[i].name).upper()}"
        )

    # Return a list of numbers and names for every UD composites
    return numbers_and_names_ud_composites


def _get_sub_title_fibers(materials: tuple[HT, ...]) -> str:
    """Get the sub-title of number of fibers being compared that is to be displayed on
    console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The subtitle of number of fibers being compared
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return sub-title
    return f"\nB) {len(materials)} Fibers of UD Composites\n"


def _get_numbers_and_names_fibers(materials: tuple[HT, ...]) -> list:
    """Get the numbering system for every fibers being compared together with their
    names for the purpose identification when tabling the comparison data on console
    screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The numbering system assigned to each fiber for identification associated
        with names for comparison purposes in table format.
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize numbers and names for every UD composites
    numbers_and_names_fibers = []
    for i in range(len(materials)):
        numbers_and_names_fibers.append(
            f"[{i+1}] : {materials[i].fiber.name} - {type(materials[i].fiber).__name__}"
        )
    # Return a list of numbers and names for fibers of every UD composite
    return numbers_and_names_fibers


def _get_sub_sub_title_fiber_axial_youngs_modulus(materials: tuple[HT, ...]) -> str:
    """Get the sub-sub-title of number of fibers being compared for axial Young's
    modulus which is to be displayed on the console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The subtitle of number of fibers being compared for axial Young's modulus
        analysis
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return sub-sub-title
    return (
        f"\ni) {len(materials)} Fibers on Young's / Axial Young's Modulus Comparison\n"
    )


def _get_fibers_axial_youngs_modulus(materials: tuple[HT, ...]) -> list:
    """Get the comparison data on the fiber's Young's modulus for Isotropic object and
    fiber's axial Young's modulus for Transtropic object to be displayed on console
    screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The comparison data which include either Young's modulus for Isotropic
        object or fiber's axial Young's modulus for Transtropic object
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize headers and values of fiber Young's or axial Young's modulus
    row_1st_data: list[str] = ["Fiber Material"]
    row_2nd_data: list[str | Decimal] = [
        "Young's Modulus, E or \nAxial Young's Modulus, E1 (GPa)"
    ]
    for i in range(len(materials)):
        row_1st_data.append(f"[{i+1}]\n{materials[i].fiber.name}")
        if isinstance(materials[i].fiber, Isotropic):
            row_2nd_data.append(
                (materials[i].fiber._get_info())["Young's\nModulus,\nE (GPa)"]
            )  # Isotropic
        else:
            row_2nd_data.append(
                (materials[i].fiber._get_info())["Axial\nYoung's\nModulus,\nE1 (GPa)"]
            )  # Transtropic

    # Return list of fibers' Young's or axial Young's modulus
    return [row_1st_data, row_2nd_data]


def _get_sub_sub_title_fiber_transverse_youngs_modulus(
    materials: tuple[HT, ...]
) -> str:
    """Get the sub-sub-title of number of fibers being compared for transverse Young's
    modulus which is to be displayed on the console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The subtitle of number of fibers being compared for transverse Young's
        modulus
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return sub-sub-title
    return (
        f"\ni) {len(materials)} Fibers on Young's / Transverse Young's Modulus "
        + "Comparison\n"
    )


def _get_fibers_transverse_youngs_modulus(materials: tuple[HT, ...]) -> list:
    """Get the comparison data on the fiber's Young's modulus for Isotropic object and
    fiber's transverse Young's modulus for Transtropic object to be displayed on console
    screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The comparison data which include either fiber's Young's modulus for
        Isotropic object or fiber's transverse Young's modulus for Transtropic object
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize headers and values of fiber transverse Young's modulus
    row_1st_data: list[str] = ["Fiber Material"]
    row_2nd_data: list[str | Decimal] = [
        "Young's Modulus, E or\nTransverse Young's Modulus, E2 (GPa)"
    ]
    for i in range(len(materials)):
        row_1st_data.append(f"[{i+1}]\n{materials[i].fiber.name}")
        if isinstance(materials[i].fiber, Isotropic):
            row_2nd_data.append(
                (materials[i].fiber._get_info())["Young's\nModulus,\nE (GPa)"]
            )  # Isotropic
        else:
            row_2nd_data.append(
                (materials[i].fiber._get_info())[
                    "Transverse\nYoung's\nModulus,\nE2 (GPa)"
                ]
            )  # Transtropic

    # Return list of fibers' Young's or transverse Young's modulus
    return [row_1st_data, row_2nd_data]


def _get_sub_sub_title_fiber_axial_shear_modulus(materials: tuple[HT, ...]) -> str:
    """Get the sub-sub-title of number of fibers being compared for axial shear modulus
    which is to be displayed on the console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The subtitle of number of fibers being compared on axial shear modulus
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return sub-sub-title
    return f"\ni) {len(materials)} Fibers on Shear / Axial Shear Modulus Comparison\n"


def _get_fibers_axial_shear_modulus(materials: tuple[HT, ...]) -> list:
    """Get the comparison data on the fiber's shear modulus for Isotropic object and
    fiber's axial shear modulus for Transtropic object to displayed on console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The comparison data which include either fiber's shear modulus for
        Isotropic object or fiber's axial shear modulus for Transtropic object
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize headers and values of fiber shear / axial shear modulus
    row_1st_data: list[str] = ["Fiber Material"]
    row_2nd_data: list[str | Decimal] = [
        "Shear Modulus, G or\nAxial Shear Modulus, G12 (GPa)"
    ]
    for i in range(len(materials)):
        row_1st_data.append(f"[{i+1}]\n{materials[i].fiber.name}")
        if isinstance(materials[i].fiber, Isotropic):
            row_2nd_data.append(
                (materials[i].fiber._get_info())["Shear\nModulus,\nG (GPa)"]
            )  # Isotropic
        else:
            row_2nd_data.append(
                (materials[i].fiber._get_info())["Axial\nShear\nModulus,\nG12 (GPa)"]
            )  # Transtropic

    # Return list of fibers' shear / axial shear modulus
    return [row_1st_data, row_2nd_data]


def _get_sub_sub_title_fiber_major_poissons_ratio(materials: tuple[HT, ...]) -> str:
    """Get the sub-sub-title of number of fibers being compared for major Poisson's
    ratio which is to be displayed on the console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The subtitle of number of fibers being compared for major Poisson's ratio
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return sub-sub-title
    return (
        f"\ni) {len(materials)} Fibers on Poisson's / Major Poisson's Ratio "
        + "Comparison\n"
    )


def _get_fibers_major_poissons_ratio(materials: tuple[HT, ...]) -> list:
    """Get the comparison data on the fiber's Poisson's ratio for Isotropic object
    and fiber's major Poisson's ratio for Transtropic object to be displayed on console
    screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The comparison data which include either fiber's Poisson's ratio for
        Isotropic object or fiber's major Poisson's ratio for Transtropic object
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize headers and values of fiber Poisson's / major Poisson's ratio
    row_1st_data: list[str] = ["Fiber Material"]
    row_2nd_data: list[str | Decimal] = [
        f"Poisson's Ratio, v or\nMajor Poisson's Ratio, v12"
    ]
    for i in range(len(materials)):
        row_1st_data.append(f"[{i+1}]\n{materials[i].fiber.name}")
        if isinstance(materials[i].fiber, Isotropic):
            row_2nd_data.append(
                (materials[i].fiber._get_info())["Poisson's\nRatio,\nv"]
            )  # Isotropic
        else:
            row_2nd_data.append(
                (materials[i].fiber._get_info())["Major\nPoisson's\nRatio,\nv12"]
            )  # Transtropic

    # Return list of fibers' Poisson's / major Poisson's ratio
    return [row_1st_data, row_2nd_data]


def _get_sub_sub_title_fiber_transverse_shear_modulus(materials: tuple[HT, ...]) -> str:
    """Get the sub-sub-title of number of fibers being compared for transverse shear
    modulus which is to be displayed on the console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The subtitle of number of fibers being compared for transverse shear
        modulus
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return sub-sub-title
    return (
        f"\ni) {len(materials)} Fibers on Shear / Transverse Shear Modulus Comparison\n"
    )


def _get_fibers_transverse_shear_modulus(materials: tuple[HT, ...]) -> list:
    """Get the comparison data on the fiber's shear mdodulus for Isotropic object
    and fiber's transverse shear modulus for Transtropic object to be displayed on
    console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The comparison data which include either fiber's shear mdodulus for
        Isotropic object or fiber's transverse shear modulus for Transtropic object
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize headers and values of fiber shear / transverse shear modulus
    row_1st_data: list[str] = ["Fiber Material"]
    row_2nd_data: list[str | Decimal] = [
        f"Shear Modulus, G or\nTransverse Shear Modulus, G23 (GPa)"
    ]
    for i in range(len(materials)):
        row_1st_data.append(f"[{i+1}]\n{materials[i].fiber.name}")
        if isinstance(materials[i].fiber, Isotropic):
            row_2nd_data.append(
                (materials[i].fiber._get_info())["Shear\nModulus,\nG (GPa)"]
            )  # Isotropic
        else:
            row_2nd_data.append(
                (materials[i].fiber._get_info())[
                    "Transverse\nShear\nModulus,\nG23 (GPa)"
                ]
            )  # Transtropic

    # Return list of fibers' shear / transverse shear modulus
    return [row_1st_data, row_2nd_data]


def _get_sub_sub_title_fiber_pstrain_bulk_modulus(materials: tuple[HT, ...]) -> str:
    """Get the sub-sub-title of number of fibers being compared for plane-strain bulk
    modulus which is to be displayed on the console screen

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The subtitle of number of fibers being compared for plane-strain bulk
        modulus
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return sub-sub-title
    return f"\nii) {len(materials)} Fibers on Plane-Strain Bulk Modulus Comparison\n"


def _get_fibers_pstrain_bulk_modulus(materials: tuple[HT, ...]) -> list:
    """Get the comparison data on the fiber's shear mdodulus for Isotropic object
    and fiber's transverse shear modulus for Transtropic object to be displayed on
    console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The comparison data which include either fiber's shear mdodulus for
        Isotropic object or fiber's transverse shear modulus for Transtropic object
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize headers and values of fiber plane-strain bulk modulus
    row_1st_data: list[str] = ["Fiber Material"]
    row_2nd_data: list[str | Decimal] = [f"Plane-Strain Bulk Modulus, K23 (GPa)"]
    for i in range(len(materials)):
        row_1st_data.append(f"[{i+1}]\n{materials[i].fiber.name}")
        if isinstance(materials[i].fiber, Isotropic):
            row_2nd_data.append(
                (materials[i].fiber._get_info())["Plane-strain\nBulk Modulus,\nK (GPa)"]
            )  # Isotropic
        else:
            row_2nd_data.append(
                (materials[i].fiber._get_info())[
                    "Plane-strain\nBulk\nModulus,\nK23 (GPa)"
                ]
            )  # Transtropic

    # Return list of fibers' plane-strain bulk modulus
    return [row_1st_data, row_2nd_data]


def _get_sub_title_matrices(materials: tuple[HT, ...]) -> str:
    """Get the sub-title of number of matrices being compared which is to be displayed
    on console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The subtitle of number of matrices being compared
    : rtype: str
    """
    # Check for TypeError
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return sub-title
    return f"\nC) {len(materials)} Matrices of UD Composites\n"


def _get_numbers_and_names_matrices(materials: tuple[HT, ...]) -> list:
    """Get the numbering system for every matrices being compared together with their
    names for the purpose identification when tabling the comparison data on console
    screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The numbering system assigned to each matrix for identification
        associated with names for comparison purposes in table format.
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize numbers and names for every UD composites
    numbers_and_names_matrices = []
    for i in range(len(materials)):
        numbers_and_names_matrices.append(
            f"[{i+1}] : {materials[i].matrix.name} - {type(materials[i].matrix).__name__}"
        )
    # Return a list of numbers and names for fibers of every UD composite
    return numbers_and_names_matrices


def _get_sub_sub_title_matrix_axial_youngs_modulus(materials: tuple[HT, ...]) -> str:
    """Get the sub-sub-title of number of matrices being compared for axial Young's
    modulus which is to be displayed on the console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The subtitle of number of matrices being compared for axial Young's
        modulus
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return sub-sub-title
    return (
        f"\ni) {len(materials)} Matrices on Young's / Axial Young's Modulus Comparison "
        + "\n"
    )


def _get_matrices_axial_youngs_modulus(materials: tuple[HT, ...]) -> list:
    """Get the comparison data on the matrix's Young's modulus for Isotropic object and
    matrix's axial Young's modulus for Transtropic object to be displayed on console
    screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The comparison data which include either matrix's Young's modulus for
        Isotropic object or matrix's axial Young's modulus for Transtropic object
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize headers and values of fiber Young's or axial Young's modulus
    row_1st_data: list[str] = ["Matrix Material"]
    row_2nd_data: list[str | Decimal] = [
        "Young's Modulus, E or \nAxial Young's Modulus, E1 (GPa)"
    ]
    for i in range(len(materials)):
        row_1st_data.append(f"[{i+1}]\n{materials[i].matrix.name}")
        if isinstance(materials[i].matrix, Isotropic):
            row_2nd_data.append(
                (materials[i].matrix._get_info())["Young's\nModulus,\nE (GPa)"]
            )  # Isotropic
        else:
            row_2nd_data.append(
                (materials[i].matrix._get_info())["Axial\nYoung's\nModulus,\nE1 (GPa)"]
            )  # Transtropic

    # Return list of matrices' Young's or axial Young's modulus
    return [row_1st_data, row_2nd_data]


def _get_sub_sub_title_matrix_transverse_youngs_modulus(
    materials: tuple[HT, ...]
) -> str:
    """Get the sub-sub-title of number of matrices being compared for transverse Young's
    modulus which is to be displayed on the console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The subtitle of number of matrices being compared for transverse Young's
        modulus
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return sub-sub-title
    return (
        f"\ni) {len(materials)} Matrices on Young's / Transverse Young's Modulus "
        + "Comparison\n"
    )


def _get_matrices_transverse_youngs_modulus(materials: tuple[HT, ...]) -> list:
    """Get the comparison data on the matrix's Young's modulus for Isotropic object and
    matrix's transverse Young's modulus for Transtropic object to be displayed on
    console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The comparison data which include either matrix's Young's modulus for
        Isotropic object or matrix's transverse Young's modulus for Transtropic object
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize headers and values of fiber transverse Young's modulus
    row_1st_data: list[str] = ["Matrix Material"]
    row_2nd_data: list[str | Decimal] = [
        "Young's Modulus, E or\nTransverse Young's Modulus, E2 (GPa)"
    ]
    for i in range(len(materials)):
        row_1st_data.append(f"[{i+1}]\n{materials[i].matrix.name}")
        if isinstance(materials[i].matrix, Isotropic):
            row_2nd_data.append(
                (materials[i].matrix._get_info())["Young's\nModulus,\nE (GPa)"]
            )  # Isotropic
        else:
            row_2nd_data.append(
                (materials[i].matrix._get_info())[
                    "Transverse\nYoung's\nModulus,\nE2 (GPa)"
                ]
            )  # Transtropic

    # Return list of matrices' Young's or transverse Young's modulus
    return [row_1st_data, row_2nd_data]


def _get_sub_sub_title_matrix_axial_shear_modulus(materials: tuple[HT, ...]) -> str:
    """Get the sub-sub-title of number of matrices being compared for axial shear
    modulus which is to be displayed on the console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The subtitle of number of matrices being compared for axial shear modulus
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return sub-sub-title
    return f"\ni) {len(materials)} Matrices on Shear / Axial Shear Modulus Comparison\n"


def _get_matrices_axial_shear_modulus(materials: tuple[HT, ...]) -> list:
    """Get the comparison data on the matrix's shear modulus for Isotropic object and
    matrix's axial shear modulus for Transtropic object to be displayed on console
    screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The comparison data which include either matrix's shear modulus for
        Isotropic object or matrix's axial shear modulus for Transtropic object.
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize headers and values of matrix shear / axial shear modulus
    row_1st_data: list[str] = ["Matrix Material"]
    row_2nd_data: list[str | Decimal] = [
        "Shear Modulus, G or\nAxial Shear Modulus, G12 (GPa)"
    ]
    for i in range(len(materials)):
        row_1st_data.append(f"[{i+1}]\n{materials[i].matrix.name}")
        if isinstance(materials[i].matrix, Isotropic):
            row_2nd_data.append(
                (materials[i].matrix._get_info())["Shear\nModulus,\nG (GPa)"]
            )  # Isotropic
        else:
            row_2nd_data.append(
                (materials[i].matrix._get_info())["Axial\nShear\nModulus,\nG12 (GPa)"]
            )  # Transtropic

    # Return list of fibers' shear / axial shear modulus
    return [row_1st_data, row_2nd_data]


def _get_sub_sub_title_matrix_major_poissons_ratio(materials: tuple[HT, ...]) -> str:
    """Get the sub-sub-title of number of matrices being compared for major Poisson's
    ratio which is to be displayed on the console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The subtitle of number of matrices being compared for major Poisson's
        ratio
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return sub-sub-title
    return (
        f"\ni) {len(materials)} Matrices on Poisson's / Major Poisson's Ratio "
        + "Comparison\n"
    )


def _get_matrices_major_poissons_ratio(materials: tuple[HT, ...]) -> list:
    """Get the comparison data on the matrix's Poissons'ratio for Isotropic object and
    matrix's major Poisson's ratio for Transtropic object to be displayed on console
    screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The comparison data which include either matrix's Poissons'ratio for
        Isotropic object or matrix's major Poisson's ratio for Transtropic object.
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize headers and values of matrix Poisson's / major Poisson's ratio
    row_1st_data: list[str] = ["Matrix Material"]
    row_2nd_data: list[str | Decimal] = [
        f"Poisson's Ratio, v or\nMajor Poisson's Ratio, v12"
    ]
    for i in range(len(materials)):
        row_1st_data.append(f"[{i+1}]\n{materials[i].matrix.name}")
        if isinstance(materials[i].matrix, Isotropic):
            row_2nd_data.append(
                (materials[i].matrix._get_info())["Poisson's\nRatio,\nv"]
            )  # Isotropic
        else:
            row_2nd_data.append(
                (materials[i].matrix._get_info())["Major\nPoisson's\nRatio,\nv12"]
            )  # Transtropic

    # Return list of matrices' Poisson's / major Poisson's ratio
    return [row_1st_data, row_2nd_data]


def _get_sub_sub_title_matrix_transverse_shear_modulus(
    materials: tuple[HT, ...]
) -> str:
    """Get the sub-sub-title of number of matrices being compared for tranverse shear
    modulus which is to be displayed on the console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The subtitle of number of matrices being compared for transverse shear
        modulus
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return sub-sub-title
    return (
        f"\ni) {len(materials)} Matrices on Shear / Transverse Shear Modulus "
        + "Comparison\n"
    )


def _get_matrices_transverse_shear_modulus(materials: tuple[HT, ...]) -> list:
    """Get the comparison data on the matrix's shear modulus for Isotropic object and
    matrix's transverse shear modulus for Transtropic object to be displayed on console
    screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The comparison data which include either matrix's shear modulus for
        Isotropic object or matrix's transverse shear modulus for Transtropic object
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize headers and values of matrix shear / transverse shear modulus
    row_1st_data: list[str] = ["Matrix Material"]
    row_2nd_data: list[str | Decimal] = [
        f"Shear Modulus, G or\nTransverse Shear Modulus, G23 (GPa)"
    ]
    for i in range(len(materials)):
        row_1st_data.append(f"[{i+1}]\n{materials[i].matrix.name}")
        if isinstance(materials[i].matrix, Isotropic):
            row_2nd_data.append(
                (materials[i].matrix._get_info())["Shear\nModulus,\nG (GPa)"]
            )  # Isotropic
        else:
            row_2nd_data.append(
                (materials[i].matrix._get_info())[
                    "Transverse\nShear\nModulus,\nG23 (GPa)"
                ]
            )  # Transtropic

    # Return list of matrices' shear / transverse shear modulus
    return [row_1st_data, row_2nd_data]


def _get_sub_sub_title_matrix_pstrain_bulk_modulus(materials: tuple[HT, ...]) -> str:
    """Get the sub-sub-title of number of matrices being compared for plane-strain bulk
    modulus which is to be displayed on the console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The subtitle of number of matrices being compared for plane-strain bulk
        modulus
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Return sub-sub-title
    return f"\nii) {len(materials)} Matrices on Plane-Strain Bulk Modulus Comparison\n"


def _get_matrices_pstrain_bulk_modulus(materials: tuple[HT, ...]) -> list:
    """Get the comparison data on the matrix's plane-strian bulk modulus both for
    Isotropic object and matrix's plane-stain bulk modulus for Transtropic object to
    be displayed on console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than 2 or greater than 5
    : return: The comparison data which include either matrix's plane-strian bulk
        modulus both for Isotropic object or matrix's plane-stain bulk modulus for
        Transtropic object
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect all arguments are UD composites and 'HT' object")

    # Organize headers and values of matrix plane-strain bulk modulus
    row_1st_data: list[str] = ["Matrix Material"]
    row_2nd_data: list[str | Decimal] = [f"Plane-Strain Bulk Modulus, K23 (GPa)"]
    for i in range(len(materials)):
        row_1st_data.append(f"[{i+1}]\n{materials[i].matrix.name}")
        if isinstance(materials[i].matrix, Isotropic):
            row_2nd_data.append(
                (materials[i].matrix._get_info())[
                    "Plane-strain\nBulk Modulus,\nK (GPa)"
                ]
            )  # Isotropic
        else:
            row_2nd_data.append(
                (materials[i].matrix._get_info())[
                    "Plane-strain\nBulk\nModulus,\nK23 (GPa)"
                ]
            )  # Transtropic

    # Return list of matrices' plane-strain bulk modulus
    return [row_1st_data, row_2nd_data]


def _percent_diff(x, y):
    """Compute percentage difference between x and y where x is the baseline number.

    Note: A helper function to ``compare`` function.

    : param `x`: Baseline value
    : type: Decimal
    : param `y`: value to be compared
    : type: Decimal
    : return: The percentage difference either negative or positive
    : rtype: Decimal
    """
    return round(((y - x) / x) * 100, 1)


def _get_sub_title_effective_elastic_properties(materials: tuple[HT, ...]) -> str:
    """Get the sub-title of effective elastic moduli of UD composites being compared to
    be displayed on console's screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: ```HT```
    : raise TypeError: When number of UD composites is less than two (2) composites or
        at most five (5) composites
    : return: The sub-title of effective elastic moduli of UD composites being compared
    : rtype: str
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expect at least a minimum of two (2) or at most five (5) composites for "
            + "comparison analysis"
        )
    # Return sub-title
    return (
        f"\nD) Comparison of Effective Elastic Property of {len(materials)} UD "
        + "Composites\n"
    )


def _get_comparison_specific_property_full_range_Vf(
    materials: tuple[HT, ...],
    property: str,
) -> dict:
    """Get comparison data on effective elastic moduli for every UD composite under
    comparison being compared to be displayed on console's screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: tuple
    : param `property`: Effective elastic modulus of UD composite being compared
    : type: str
    : raise TypeError: If number of UD composites is less than two (2) composites and
        five (5) composites and if `property` is None and not str object
    : raise ValueError: When value of property is not 'E1eff', 'E2eff', 'G12eff',
        'v12eff', 'G23eff' and 'K23eff'
    : return: Comparison data on specific effective elastic moduli of every UD composite
        being compared
    : rtype: dict
    """
    # Check for TypeError and ValueError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expected number of UD composites at minimum two (2) or at most five (5) "
            + "UD composites for comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(property, str):
            raise TypeError("Expected UD composite to be 'HT' object")
    if property is None or not isinstance(property, str):
        raise TypeError(
            "Expected property to be 'str' and either 'E1eff', 'E2eff', 'G12eff', "
            + "'v12eff', 'G23eff' or 'K23eff'"
        )
    if property not in ["E1eff", "E2eff", "G12eff", "v12eff", "G23eff", "K23eff"]:
        raise ValueError(
            "Expected property to be either 'E1eff', 'E2eff', 'G12eff', 'v12eff', "
            + "'G23eff' or 'K23eff'"
        )

    # Organize comparison data
    compare_properties_dict: dict = {"Vf": materials[0].fiber_volfract}
    match property:
        # For axial Young's modulus
        case "E1eff":
            for i in range(len(materials)):
                compare_properties_dict.update(
                    {f"[{i+1}]\nE1*\n(GPa)": materials[i].eff_axial_youngs_moduli}
                )
                if i != 0:
                    diff_percentage = []
                    for j in range(0, 101):
                        diff_percentage.append(
                            _percent_diff(
                                materials[0].eff_axial_youngs_moduli[j],
                                materials[i].eff_axial_youngs_moduli[j],
                            )
                        )
                    compare_properties_dict.update(
                        {f"diff. of\n[{i+1}] to [1]\n(%)": diff_percentage}
                    )
        # For transverse Young's modulus
        case "E2eff":
            for i in range(len(materials)):
                compare_properties_dict.update(
                    {f"[{i+1}]\nE2*\n(GPa)": materials[i].eff_transverse_youngs_moduli}
                )
                if i != 0:
                    diff_percentage = []
                    for j in range(0, 101):
                        diff_percentage.append(
                            _percent_diff(
                                materials[0].eff_transverse_youngs_moduli[j],
                                materials[i].eff_transverse_youngs_moduli[j],
                            )
                        )
                    compare_properties_dict.update(
                        {f"diff. of\n[{i+1}] to [1]\n(%)": diff_percentage}
                    )
        # For axial shear modulus
        case "G12eff":
            for i in range(len(materials)):
                compare_properties_dict.update(
                    {f"[{i+1}]\nG12*\n(GPa)": materials[i].eff_axial_shear_moduli}
                )
                if i != 0:
                    diff_percentage = []
                    for j in range(0, 101):
                        diff_percentage.append(
                            _percent_diff(
                                materials[0].eff_axial_shear_moduli[j],
                                materials[i].eff_axial_shear_moduli[j],
                            )
                        )
                    compare_properties_dict.update(
                        {f"diff. of\n[{i+1}] to [1]\n(%)": diff_percentage}
                    )
        # For major Poisson's ratio
        case "v12eff":
            for i in range(len(materials)):
                compare_properties_dict.update(
                    {f"[{i+1}]\nv12*": materials[i].eff_major_poissons_ratios}
                )
                if i != 0:
                    diff_percentage = []
                    for j in range(0, 101):
                        diff_percentage.append(
                            _percent_diff(
                                materials[0].eff_major_poissons_ratios[j],
                                materials[i].eff_major_poissons_ratios[j],
                            )
                        )
                    compare_properties_dict.update(
                        {f"diff. of\n[{i+1}] to [1]\n(%)": diff_percentage}
                    )
        # For transverse shear modulus
        case "G23eff":
            for i in range(len(materials)):
                compare_properties_dict.update(
                    {f"[{i+1}]\nG23*\n(GPa)": materials[i].eff_transverse_shear_moduli}
                )
                if i != 0:
                    diff_percentage = []
                    for j in range(0, 101):
                        diff_percentage.append(
                            _percent_diff(
                                materials[0].eff_transverse_shear_moduli[j],
                                materials[i].eff_transverse_shear_moduli[j],
                            )
                        )
                    compare_properties_dict.update(
                        {f"diff. of\n[{i+1}] to [1]\n(%)": diff_percentage}
                    )
        # For plane-strain bulk modulus
        case "K23eff":
            for i in range(len(materials)):
                compare_properties_dict.update(
                    {f"[{i+1}]\nK23*\n(GPa)": materials[i].eff_pstrain_bulk_moduli}
                )
                if i != 0:
                    diff_percentage = []
                    for j in range(0, 101):
                        diff_percentage.append(
                            _percent_diff(
                                materials[0].eff_pstrain_bulk_moduli[j],
                                materials[i].eff_pstrain_bulk_moduli[j],
                            )
                        )
                    compare_properties_dict.update(
                        {f"diff. of\n[{i+1}] to [1]\n(%)": diff_percentage}
                    )
    # Get relevant data and return dict of compared properties
    return compare_properties_dict


def _get_comparison_specific_property_specific_value_Vf(
    materials: tuple[HT, ...], property: str, idx: int
) -> list:
    """Get comparison data of user-defined effective elastic moduli based on the
    specific value of fiber volume fraction to be displayed on console screen.

    Note: A helper function to ``compare`` function.

    : param `materials`: UD composites
    : type: tuple
    : param `property`: Effective elastic modulus of UD composite being compared
    : type: str
    : param `idx`: Index number of a tuple of effective elastic properties under
        consideration that correlates with index number of a tuple of fiber volume
        fraction
    : raise TypeError: If number of UD composites is less than two (2) composites and
        five (5) composites, if `property` is None and not str object, or if `idx` is
        None and not int object
    : raise ValueError: If 'property' is not 'E1eff', 'E2eff', 'G12eff', 'v12eff',
         'G23eff' and 'K23eff'
    : return: Comparison data on specific effective elastic moduli of every UD composite
        being compared
    : rtype: dict
    """
    # Check for TypeError and ValueError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expected number of UD composites at minimum two (2) or at most five (5) "
            + "UD composites for comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(property, str):
            raise TypeError("Expected UD composite to be 'HT' object")
    if property is None or not isinstance(property, str):
        raise TypeError(
            "Expected property to be 'str' and either 'E1eff', 'E2eff', 'G12eff', "
            + "'v12eff', 'G23eff' or 'K23eff'"
        )
    if idx is None or not isinstance(idx, int):
        raise TypeError("Expected index number to be int object")
    if property not in ["E1eff", "E2eff", "G12eff", "v12eff", "G23eff", "K23eff"]:
        raise ValueError(
            "Expected property to be either 'E1eff', 'E2eff', 'G12eff', 'v12eff', "
            + "'G23eff' or 'K23eff'"
        )

    # Get effective elastic property at specific value of fiber volume fraction
    eff_properties_1st_row: list = ["Vf"]
    eff_properties_2nd_row: list = [
        materials[0].fiber_volfract[idx],
    ]
    match property:
        # For axial Young's modulus
        case "E1eff":
            for i in range(len(materials)):
                eff_properties_1st_row.append(f"[{i+1}]\nE1*\n(GPa)")
                if i != 0:
                    eff_properties_1st_row.append(f"diff. of\n[{i+1}] to [1]\n(%)")
                eff_properties_2nd_row.append(materials[i].eff_axial_youngs_moduli[idx])
                if i != 0:
                    eff_properties_2nd_row.append(
                        _percent_diff(
                            materials[0].eff_axial_shear_moduli[idx],
                            materials[i].eff_axial_shear_moduli[idx],
                        )
                    )
        # For transverse Young's modulus
        case "E2eff":
            for i in range(len(materials)):
                eff_properties_1st_row.append(f"[{i+1}]\nE2*\n(GPa)")
                if i != 0:
                    eff_properties_1st_row.append(f"diff. of\n[{i+1}] to [1]\n(%)")
                eff_properties_2nd_row.append(
                    materials[i].eff_transverse_youngs_moduli[idx]
                )
                if i != 0:
                    eff_properties_2nd_row.append(
                        _percent_diff(
                            materials[0].eff_transverse_youngs_moduli[idx],
                            materials[i].eff_transverse_youngs_moduli[idx],
                        )
                    )
        # For axial shear modulus
        case "G12eff":
            for i in range(len(materials)):
                eff_properties_1st_row.append(f"[{i+1}]\nG12*\n(GPa)")
                if i != 0:
                    eff_properties_1st_row.append(f"diff. of\n[{i+1}] to [1]\n(%)")
                eff_properties_2nd_row.append(materials[i].eff_axial_shear_moduli[idx])
                if i != 0:
                    eff_properties_2nd_row.append(
                        _percent_diff(
                            materials[0].eff_axial_shear_moduli[idx],
                            materials[i].eff_axial_shear_moduli[idx],
                        )
                    )
        # For major Poisson's ratio
        case "v12eff":
            for i in range(len(materials)):
                eff_properties_1st_row.append(f"[{i+1}]\nv12*")
                if i != 0:
                    eff_properties_1st_row.append(f"diff. of\n[{i+1}] to [1]\n(%)")
                eff_properties_2nd_row.append(
                    materials[i].eff_major_poissons_ratios[idx]
                )
                if i != 0:
                    eff_properties_2nd_row.append(
                        _percent_diff(
                            materials[0].eff_major_poissons_ratios[idx],
                            materials[i].eff_major_poissons_ratios[idx],
                        )
                    )
        # For transverse shear modulus
        case "G23eff":
            for i in range(len(materials)):
                eff_properties_1st_row.append(f"[{i+1}]\nG23*\n(GPa)")
                if i != 0:
                    eff_properties_1st_row.append(f"diff. of\n[{i+1}] to [1]\n(%)")
                eff_properties_2nd_row.append(
                    materials[i].eff_transverse_shear_moduli[idx]
                )
                if i != 0:
                    eff_properties_2nd_row.append(
                        _percent_diff(
                            materials[0].eff_transverse_shear_moduli[idx],
                            materials[i].eff_transverse_shear_moduli[idx],
                        )
                    )
        # For plane-strain bulk modulus
        case "K23eff":
            for i in range(len(materials)):
                eff_properties_1st_row.append(f"[{i+1}]\nK23*\n(GPa)")
                if i != 0:
                    eff_properties_1st_row.append(f"diff. of\n[{i+1}] to [1]\n(%)")
                eff_properties_2nd_row.append(materials[i].eff_pstrain_bulk_moduli[idx])
                if i != 0:
                    eff_properties_2nd_row.append(
                        _percent_diff(
                            materials[0].eff_pstrain_bulk_moduli[idx],
                            materials[i].eff_pstrain_bulk_moduli[idx],
                        )
                    )
    # Collect relevant data and return list of compared properties
    return [eff_properties_1st_row, eff_properties_2nd_row]


def _get_comparison_specific_property_specific_range_Vf(
    materials: tuple[HT, ...], property: str, start: int, end: int
):
    """Get comparison data of user-defined effective elastic moduli based on the
    specific range of fiber volume fraction to be displayed on console screen.

    Note: A helper function to ``display`` function.

    : param `material`: UD composites
    : type: tuple
    : param `property`: Effective elastic modulus of UD composite being compared
    : type: str
    : param `start`: index number of a tuple of effective elastic modulus that
        correlates with the index number of a starting value of fiber volume fraction
        range specified by user
    : type: int
    : param `end`: index number of a tuple of effective elastic modulus that
        correlates with the index number of an ending value of fiber volume fraction
        range specified by user
    : type: int
    : raise TypeError: If `materials` is None or not ```HT``` object, if `property` is
        None and not str object, or if either `start` and `end` is either None or not an
        int object
    : raise ValueError: If `start` < 0, of `start` > 100, of `start` > `end`, if
        `end` < 0, or `end` > 0, or `end` < `start`, or if 'property' is not 'E1eff',
        'E2eff', 'G12eff', 'v12eff', 'G23eff' and 'K23eff'.
    : return: Data on the effective elastic properties versus specific range of fiber
        volume fraction
    : rtype: dict
    """
    # Check for TypeError and ValueError
    if len(materials) < 2 or len(materials) > 5:
        raise TypeError(
            "Expected number of UD composites at minimum two (2) or at most five (5) "
            + "UD composites for comparison analysis"
        )
    for material in materials:
        if material is None or not isinstance(property, str):
            raise TypeError("Expected UD composite to be 'HT' object")
    if property is None or not isinstance(property, str):
        raise TypeError(
            "Expected property to be 'str' and either 'E1eff', 'E2eff', 'G12eff', "
            + "'v12eff', 'G23eff' or 'K23eff'"
        )
    if start is None or not isinstance(start, int):
        raise TypeError(
            "Expected start to be starting inclusive value of index number of a tuple "
            + "a specific elastic property that correlates with the index number of "
            + "a tuple of fiber volume fraction"
        )
    if end is None or not isinstance(end, int):
        raise TypeError(
            "Expected start to be ending inclusive value of index number of a tuple "
            + "a specific elastic property that correlates with the index number of "
            + "a tuple of fiber volume fraction"
        )
    if property not in ["E1eff", "E2eff", "G12eff", "v12eff", "G23eff", "K23eff"]:
        raise ValueError(
            "Expected property to be either 'E1eff', 'E2eff', 'G12eff', 'v12eff', "
            + "'G23eff' or 'K23eff'"
        )
    if start < 0 or start > 100 or start > end:
        raise ValueError(
            "Expected 'start', the index number of a tuple of specific elastic "
            + "property to be greater and equal to zero and less than 101 and should "
            + "not be greater than 'end', the index number of a tuple of the same "
            + "specific elastic property under comparison"
        )
    if end < 0 or end > 100 or end < start:
        raise ValueError(
            "Expected 'end', the index number of a tuple of specific elastic "
            + "property to be greater and equal to zero and less than 101 and should "
            + "not be lesser than 'end', the index number of a tuple of the same "
            + "specific elastic property under comparison"
        )

    # Organize fiber volume fraction according to the range
    vf = []
    for j in range(start, end + 1):
        vf.append(materials[0].fiber_volfract[j])
    compare_properties_dict = {"Vf": vf}
    # Organize comparison property based on fiber volume fraction range
    match property:
        case "E1eff":
            for i in range(len(materials)):
                eff_properties = []
                for j in range(start, end + 1):
                    eff_properties.append(materials[i].eff_axial_youngs_moduli[j])
                compare_properties_dict.update({f"[{i+1}]\nE1*\n(GPa)": eff_properties})
                if i != 0:
                    diff_percentage = []
                    for j in range(start, end + 1):
                        diff_percentage.append(
                            _percent_diff(
                                materials[0].eff_axial_youngs_moduli[j],
                                materials[i].eff_axial_youngs_moduli[j],
                            )
                        )
                    compare_properties_dict.update(
                        {f"diff. of\n[{i+1}] to [1]\n(%)": diff_percentage}
                    )
        case "E2eff":
            for i in range(len(materials)):
                eff_properties = []
                for j in range(start, end + 1):
                    eff_properties.append(materials[i].eff_transverse_youngs_moduli[j])
                compare_properties_dict.update({f"[{i+1}]\nE2*\n(GPa)": eff_properties})
                if i != 0:
                    diff_percentage = []
                    for j in range(start, end + 1):
                        diff_percentage.append(
                            _percent_diff(
                                materials[0].eff_transverse_youngs_moduli[j],
                                materials[i].eff_transverse_youngs_moduli[j],
                            )
                        )
                    compare_properties_dict.update(
                        {f"diff. of\n[{i+1}] to [1]\n(%)": diff_percentage}
                    )
        case "G12eff":
            for i in range(len(materials)):
                eff_properties = []
                for j in range(start, end + 1):
                    eff_properties.append(materials[i].eff_axial_shear_moduli[j])
                compare_properties_dict.update(
                    {f"[{i+1}]\nG12*\n(GPa)": eff_properties}
                )
                if i != 0:
                    diff_percentage = []
                    for j in range(start, end + 1):
                        diff_percentage.append(
                            _percent_diff(
                                materials[0].eff_axial_shear_moduli[j],
                                materials[i].eff_axial_shear_moduli[j],
                            )
                        )
                    compare_properties_dict.update(
                        {f"diff. of\n[{i+1}] to [1]\n(%)": diff_percentage}
                    )
        case "v12eff":
            for i in range(len(materials)):
                eff_properties = []
                for j in range(start, end + 1):
                    eff_properties.append(materials[i].eff_major_poissons_ratios[j])
                compare_properties_dict.update({f"[{i+1}]\nv12*": eff_properties})
                if i != 0:
                    diff_percentage = []
                    for j in range(start, end + 1):
                        diff_percentage.append(
                            _percent_diff(
                                materials[0].eff_major_poissons_ratios[j],
                                materials[i].eff_major_poissons_ratios[j],
                            )
                        )
                    compare_properties_dict.update(
                        {f"diff. of\n[{i+1}] to [1]\n(%)": diff_percentage}
                    )
        case "G23eff":
            for i in range(len(materials)):
                eff_properties = []
                for j in range(start, end + 1):
                    eff_properties.append(materials[i].eff_transverse_shear_moduli[j])
                compare_properties_dict.update(
                    {f"[{i+1}]\nG23*\n(GPa)": eff_properties}
                )
                if i != 0:
                    diff_percentage = []
                    for j in range(start, end + 1):
                        diff_percentage.append(
                            _percent_diff(
                                materials[0].eff_transverse_shear_moduli[j],
                                materials[i].eff_transverse_shear_moduli[j],
                            )
                        )
                    compare_properties_dict.update(
                        {f"diff. of\n[{i+1}] to [1]\n(%)": diff_percentage}
                    )
        case "K23eff":
            for i in range(len(materials)):
                eff_properties = []
                for j in range(start, end + 1):
                    eff_properties.append(materials[i].eff_pstrain_bulk_moduli[j])
                compare_properties_dict.update(
                    {f"[{i+1}]\nK23*\n(GPa)": eff_properties}
                )
                if i != 0:
                    diff_percentage = []
                    for j in range(start, end + 1):
                        diff_percentage.append(
                            _percent_diff(
                                materials[0].eff_pstrain_bulk_moduli[j],
                                materials[i].eff_pstrain_bulk_moduli[j],
                            )
                        )
                    compare_properties_dict.update(
                        {f"diff. of\n[{i+1}] to [1]\n(%)": diff_percentage}
                    )
    # Get relevant data and return dict of compared properties
    return compare_properties_dict


def save(*materials: HT, folder: str = "csv") -> None:
    """Save A) UD composite phases' elastic properties to a csv file/s with filename/s:
            i)   both phases - Isotropic:           "'obj.name'_phases_iso_moduli.csv"
            ii)  both phases - Transtropic:         "'obj.name'_phases_tra_moduli.csv"
            iii) fiber - Isotropic & matrix - Transtropic:
                                                    "'obj.name'_fiber_iso_moduli.csv"
                                                    "'obj.name'_matrix_tra_moduli.csv"
            iv)  fiber - Transtropic & matrix - Isotropic:
                                                    "'obj.name'_fiber_tra_moduli.csv"
                                                    "'obj.name'_matrix_iso_moduli.csv"

    and B) effective elastic properties to a different csv format file with a filename:
                                                    "'obj.name' + "_eff_moduli.csv",
    and confirmations of the respective csv file saved are notified to user.

    All csv file will be saved in a folder that has the name specified by keyword
    parameter 'folder', e.g. folder = "csv" unless re-specified by user.

    Note 1: iso - Isotropic;     tra - Transtropic

    Note 2: Whenever a new file is generated and saved, a message stating the csv file
    with relevant name is saved will be printed out for notification.

    Note 3: If any of the folder does not exist yet, it will then be created and a
    notification will appear saying a new folder with relevant name is created.

    : param `materials`: one or more UD composites where each composite generates either
        two (2) or (3) csv files
    : type: ```HT```
    : param `folder`: the name of the folder where csv files will be saved into. Default
        folder name is "csv"
    : type: str
    : raise TypeError: when materials is None or when each material in materials is
        not ```HT``` type
    : rtype: None

    Example 1: Save to csv file only 1 UD composite (notice that there are 3 csv files
        generated since fiber and matrix constituent are from different material, i.e
        fiber is transversely isotropic material and matrix is isotropic material,
        which constitute two of the csv files)

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
        >>> compositeA = HT(carbon, epoxy)
        >>> compositeB = HT(fiberglass, epoxy)
        >>>
        >>> save(compositeA)
        Folder ./csv created  # New folder is created
        ============= Carbon-Epoxy_fiber_tra_moduli.csv file saved! ==============
        ============= Carbon-Epoxy_matrix_iso_moduli.csv file saved! =============
        ================ Carbon-Epoxy_eff_moduli.csv file saved! =================
        >>>

    Example 2: Save data on 2 UD composites as csv file (no notification on the creation
        of new folder since 'csv' folder has been present in the current working
        directory and furthermore, only 2 csv file generated for Fiberglass-Epoxy
        composite because both fiber and matrix is the same isotropic material)

        >>> save(compositeA, compositeB)  # Notice no new folder creation notice since "csv" folder already exists
        ============= Carbon-Epoxy_fiber_tra_moduli.csv file saved! ==============
        ============= Carbon-Epoxy_matrix_iso_moduli.csv file saved! =============
        ================ Carbon-Epoxy_eff_moduli.csv file saved! =================
        =========== Fiberglass-Epoxy_phases_iso_moduli.csv file saved! ===========
        ============== Fiberglass-Epoxy_eff_moduli.csv file saved! ===============
        >>>
    """
    # Check for TypeError:
    if len(materials) == 0:
        raise TypeError("Expect at least 1 UD composite of 'HT' object")
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect UD composite of 'HT' object")
    if folder is None or not isinstance(folder, str):
        raise TypeError(
            "Expect keyword parameter folder to have a name and is of a str type"
        )

    # Process every UD composite for csv files of record keeping
    for material in materials:

        # Save constituent elastic properties and print confirmation of csv file saved
        phases_moduli: tuple | list = _get_phase_elastic_moduli_and_filename(material)

        # For constituents that are of the same type
        if isinstance(phases_moduli, tuple):
            phase_moduli_csv_filename: str = _save_csv_file(
                phases_moduli[0],  # list of dicts of phase properties
                folder,
                phases_moduli[1],  # filename
            )
            status_saved_file: bool = _is_confirmed(folder, phase_moduli_csv_filename)
            print(
                _get_confirmation_notices(status_saved_file, phase_moduli_csv_filename)
            )

        # For constituents that are NOT of the same type
        else:
            for phase_moduli in phases_moduli:
                phase_moduli_csv_filename = _save_csv_file(
                    phase_moduli[0],  # list of dicts of phase properties
                    folder,
                    phase_moduli[1],  # filename
                )
                status_saved_file = _is_confirmed(folder, phase_moduli_csv_filename)
                print(
                    _get_confirmation_notices(
                        status_saved_file, phase_moduli_csv_filename
                    )
                )

        # Save composite effective properties and print confirmation of csv file saved
        effective_moduli: tuple = _get_effective_elastic_moduli_and_filename(material)
        effective_moduli_csv_filename: str = _save_csv_file(
            effective_moduli[0],  # list of dicts of phase properties
            folder,
            effective_moduli[1],  # filename
        )
        status_saved_file = _is_confirmed(folder, effective_moduli_csv_filename)
        print(
            _get_confirmation_notices(status_saved_file, effective_moduli_csv_filename)
        )


def _get_phase_elastic_moduli_and_filename(material: HT | None = None) -> tuple | list:
    """Get the constituent elastic moduli of UD composite and their associated
    filename/s for csv file/s, i.e get a tuple of constituent elastic moduli when both
    fiber and matrix are of the same type and thus, single csv filename associated to
    their type is assigned or get a list of constituent elastic moduli when both fiber
    and matrix are not of the same type and thus, two csv filenames associated to their
    type are assigned accordingly.

    Note: A helper function that is called by ``save`` function

    : param `material`: UD composite
    : type: ```HT``` | None
    : raise TypeError: if material is None or not of HT type
    : return: the relevant constituents' elastic moduli and their assigned csv
        filename which depends on the constituent and its type
    : rtype: tuple | list
    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("Expect UD composite of 'HT' object")

    # When both phases of the same type
    if type(material.fiber) == type(material.matrix):
        phases_properties: list = [
            material.fiber._get_info(),
            material.matrix._get_info(),
        ]

        # If both isotropic as to return phases' moduli and its assigned csv filename
        if type(material.fiber) == Isotropic:
            return (phases_properties, material.name + "_phases_iso_moduli.csv")

        # If both transtropic as to return phases' moduli and its assigned csv filename
        else:
            return (phases_properties, material.name + "_phases_tra_moduli.csv")

    # When both phases are not of the same type
    else:
        combined_properties: list = []

        # When fiber is transtropic & matrix is isotropic
        if type(material.fiber) == Transtropic:
            combined_properties.append(
                ([material.fiber._get_info()], material.name + "_fiber_tra_moduli.csv")
            )
            combined_properties.append(
                (
                    [material.matrix._get_info()],
                    material.name + "_matrix_iso_moduli.csv",
                )
            )

            # Return phases' moduli and their assigned csv filename
            return combined_properties

        # When fiber is isotropic & matrix is transtropic
        else:
            combined_properties.append(
                ([material.fiber._get_info()], material.name + "_fiber_iso_moduli.csv")
            )
            combined_properties.append(
                (
                    [material.matrix._get_info()],
                    material.name + "_matrix_tra_moduli.csv",
                )
            )

            # Return phases' moduli and their assigned csv filename
            return combined_properties


def _get_effective_elastic_moduli_and_filename(material: HT | None = None) -> tuple:
    """Get UD composite elastic moduli of UD composite and its associated filename as
    a tuple.

    Note: A helper function that is called by ``save`` function

    : param `material`: UD composite
    : type: ```HT``` | None
    : raise TypeError: if material is None or not of HT type
    : return: Effective elastic moduli of UD composite and its assigned filename
    : rtype: tuple
    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("Expect UD composite of 'HT' object")

    # Get effective elastic moduli
    eff_properties = []
    for i in range(101):
        eff_properties.append(
            {
                "Vf": material.fiber_volfract[i],
                "E1*\n(GPa)": material.eff_axial_youngs_moduli[i],
                "E2*\n(GPa)": material.eff_transverse_youngs_moduli[i],
                "G12*\n(GPa)": material.eff_axial_shear_moduli[i],
                "v12*": material.eff_major_poissons_ratios[i],
                "G23*\n(GPa)": material.eff_transverse_shear_moduli[i],
                "K23*\n(GPa)": material.eff_pstrain_bulk_moduli[i],
            }
        )

    # Return effective elastic moduli and its assigned csv filename
    return (eff_properties, material.name + "_eff_moduli.csv")


def _save_csv_file(
    properties: list | None = None,
    folder: str | None = None,
    filename: str | None = None,
) -> str:
    """Save csv file in a folder

    Note: A helper function that is called by ``save`` and ``save_compare`` function

    : param `properties`: properties of either composite's phase elastic properties
        or composite effective elastic properties
    : type: list | None
    : param `folder`: folder where csv file is saved
    : type: str | None
    : param `filename`: the filename of csv file
    : type: str | None
    : raise TypeError: If `properties` is either None or not a list or tuple, and if
        `folder` is either None and not str type, and if `filename` is either None and
        not str type
    : return: filename of csv file for verification
    : rtype: str
    """
    # Check for TypeError
    if properties is None or not isinstance(properties, list):
        raise TypeError(
            "Expect first argument to be phase properties of list object that contains "
            + " dict/s of elastic moduli or effective elastic modulli"
        )
    if folder is None or not isinstance(folder, str):
        raise TypeError("Expect second argument to a folder's name and of a str object")
    if filename is None or not isinstance(filename, str):
        raise TypeError("Expect third argument to a csv filename and of a str object")

    # Get keys from dict and stored as list
    keys_list: list = list(properties[0].keys())

    # check whether directory already exists
    folder_path = f"./{folder}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder {folder_path} created")

    # write to csv file with header from keys_list to be save in folder_path
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys_list)
        writer.writeheader()
        for data in properties:
            writer.writerow(data)

    # Return 'filename' for verification
    return filename


def save_compare(
    *materials: HT,
    test_name: str = "compare",
    folder: str = "csv",
) -> None:
    """Save the comparison analysis data between at minimum, two (2) or at most, five
    (5) UD composites for every effective elastic property to its own csv format
    file where each file shall bear a unique file name according to the effective
    elastic property postfixed with the default name defined by the keyword parameter
    `test_name`, e.g. `test_name` = "compare" unless redefined by user. Every csv file
    is then saved in a folder that takes the default name specified by the keyword
    parameter `folder`, e.g. `folder` = "csv" unless re-specified by user.

    Note 1: Whenever a new file is generated and saved, a message stating the csv file
    with relevant name is saved will be printed out.

    Note 2: If any of the folder does not exist yet, it will then be created and a
    message will appear saying a new folder with relevant name is created.

    : param `materials`: At minimum 2 and at most 5 UD composites for comparison
        analysis
    : type: '''HT'''
    : param `testname`: Keyword parameter - the name of comparison test that
        will become the prefix name of every csv file saved and also the foldername,
        to which all created csv will be saved. Default value for `test_name` is, e.g.
        `test_name` = "compare"
    : type: str
    : param `folder`: Keword parameter - the name of the folder where all csv files will
        be saved into. The default folder's name is "csv".
    : type: str
    : raise TypeError: when each of the individual material in *materials is None and not
        ```HT``` object
    : raise ValueError: when the number of material in *materials is less than two (2)
        or greater than five (5) ```HT``` objects
    : rtype: None

    Example 1: The comparison data between 4 UD composites are saved as csv files where
        each elastic property compared has its own csv file.

        >>> carbon = Transtropic("Carbon", 250, 25, 20, 10, .28)
        >>> fiberglass = Isotropic("Fiberglass", 120, .29)
        >>> epoxy = Isotropic("Epoxy", 2.8, .3)
        >>> phenolic = Isotropic("Phenolic", 5, .3)
        >>>
        >>> compositeA = HT(carbon, phenolic)
        >>> compositeB = HT(carbon, epoxy)
        >>> compositeC = HT(fiberglass,phenolic)
        >>> compositeD = HT(fiberglass, epoxy)
        >>>
        >>> save_compare(compositeA, compositeB, compositeC, compositeD)
        Folder ./csv created
        ===================== compare_E1eff.csv file saved! ======================
        ===================== compare_E2eff.csv file saved! ======================
        ===================== compare_G12eff.csv file saved! =====================
        ===================== compare_v12eff.csv file saved! =====================
        ===================== compare_G23eff.csv file saved! =====================
        ===================== compare_K23eff.csv file saved! =====================
        >>>
    """
    # Check for ValueError and TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise ValueError(
            "Expected at least 2 or at most 5 'HT' objects - UD composites for "
            + "comparison"
        )
    for material in materials:
        if not isinstance(material, HT):
            raise TypeError("Expect arguments to be 'HT' type - UD composite material")

    # Save csv for each individual compared elastic property
    # E1eff comparison
    comparison_data_E1eff_and_filename: tuple = (
        _get_csv_comparison_data_and_filename_E1eff(materials, test_name)
    )
    csv_filename_comparison_E1eff: str = _save_csv_file(
        comparison_data_E1eff_and_filename[0],  # comparison data
        folder,
        comparison_data_E1eff_and_filename[1],  # csv filename
    )
    status_E1eff_saved_file: bool = _is_confirmed(folder, csv_filename_comparison_E1eff)
    print(
        _get_confirmation_notices(
            status_E1eff_saved_file, csv_filename_comparison_E1eff
        )
    )

    # E2eff comparison
    comparison_data_E2eff_and_filename: tuple = (
        _get_csv_comparison_data_and_filename_E2eff(materials, test_name)
    )
    csv_filename_comparison_E2eff: str = _save_csv_file(
        comparison_data_E2eff_and_filename[0],  # comparison data
        folder,
        comparison_data_E2eff_and_filename[1],  # csv filename
    )
    status_E2eff_saved_file: bool = _is_confirmed(folder, csv_filename_comparison_E2eff)
    print(
        _get_confirmation_notices(
            status_E2eff_saved_file, csv_filename_comparison_E2eff
        )
    )

    # G12eff comparison
    comparison_data_G12eff_and_filename: tuple = (
        _get_csv_comparison_data_and_filename_G12eff(materials, test_name)
    )
    csv_filename_comparison_G12eff: str = _save_csv_file(
        comparison_data_G12eff_and_filename[0],  # comparison data
        folder,
        comparison_data_G12eff_and_filename[1],  # csv filename
    )
    status_G12eff_saved_file: bool = _is_confirmed(
        folder, csv_filename_comparison_G12eff
    )
    print(
        _get_confirmation_notices(
            status_G12eff_saved_file, csv_filename_comparison_G12eff
        )
    )

    # v12eff comparison
    comparison_data_v12eff_and_filename: tuple = (
        _get_csv_comparison_data_and_filename_v12eff(materials, test_name)
    )
    csv_filename_comparison_v12eff: str = _save_csv_file(
        comparison_data_v12eff_and_filename[0],  # comparison data
        folder,
        comparison_data_v12eff_and_filename[1],  # csv filename
    )
    status_v12eff_saved_file: bool = _is_confirmed(
        folder, csv_filename_comparison_v12eff
    )
    print(
        _get_confirmation_notices(
            status_v12eff_saved_file, csv_filename_comparison_v12eff
        )
    )

    # G23eff comparison
    comparison_data_G23eff_and_filename: tuple = (
        _get_csv_comparison_data_and_filename_G23eff(materials, test_name)
    )
    csv_filename_comparison_G23eff: str = _save_csv_file(
        comparison_data_G23eff_and_filename[0],  # comparison data
        folder,
        comparison_data_G23eff_and_filename[1],  # csv filename
    )
    status_G23eff_saved_file: bool = _is_confirmed(
        folder, csv_filename_comparison_G23eff
    )
    print(
        _get_confirmation_notices(
            status_G23eff_saved_file, csv_filename_comparison_G23eff
        )
    )

    # K23eff comparison
    comparison_data_K23eff_and_filename: tuple = (
        _get_csv_comparison_data_and_filename_K23eff(materials, test_name)
    )
    csv_filename_comparison_K23eff: str = _save_csv_file(
        comparison_data_K23eff_and_filename[0],  # comparison data
        folder,
        comparison_data_K23eff_and_filename[1],  # csv filename
    )
    status_K23eff_saved_file: bool = _is_confirmed(
        folder, csv_filename_comparison_K23eff
    )
    print(
        _get_confirmation_notices(
            status_K23eff_saved_file, csv_filename_comparison_K23eff
        )
    )


def _get_csv_comparison_data_and_filename_E1eff(
    materials: tuple[HT, ...], test_name: str
) -> tuple:
    """Get comparison data of effecitive axial Young's modulus, E1eff of every UD
    composite and its associated comparison csv filename

    Note: A helper function that is called by ``save_compare`` function

    : param `materials`: UD composites where their specific effective elastic constant
        is collected
    : type: tuple of ```HT``` objects
    : raise TypeError: if materials is None, or UD composite in materials is either None
        or not ```HT``` object
    : return: Comparison data of E1eff for record keeping in csv file format
    : rtype: tuple
    """
    # Check for TypeError
    if len(materials) == 0:
        raise TypeError("Expect at least 2 UD composites of HT object for comparison")
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect every argument to be UD composite of HT object")

    # Get comparison data
    e1eff_comparison_list: list = []

    # Append fiber volume fraction dict to empty list above
    for i in range(101):
        e1eff_comparison_list.append({"Vf": materials[0].fiber_volfract[i]})

    # Update every dict in comparison list with effective modulus of every composite
    for i in range(len(materials)):
        for j in range(101):
            e1eff_comparison_list[j].update(
                {f"[{i+1}]\nE1*\n(GPa)": materials[i].eff_axial_youngs_moduli[j]}
            )

    # Return a tuple consisting of comparison list and its assigned csv filename
    return (e1eff_comparison_list, test_name + "_E1eff.csv")


def _get_csv_comparison_data_and_filename_E2eff(
    materials: tuple[HT, ...], test_name: str
) -> tuple:
    """Get comparison data of effective transverse Young's moduli, E2eff of every UD
    composite and its associated comparison csv filename

    Note: A helper function that is called by ``save_compare`` function

    : param `materials`: UD composites where their specific effective elastic constant
        is collected
    : type: tuple of ```HT``` objects
    : raise TypeError: if materials is None, or UD composite in materials is either None
        or not ```HT``` object
    : return: Comparison data of E2eff for record keeping in csv file format
    : rtype: tuple
    """
    # Check for TypeError
    if len(materials) == 0:
        raise TypeError("Expect at least 2 UD composites of HT object for comparison")
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect every argument to be UD composite of HT object")

    # Get comparison data
    e2eff_comparison_list: list = []

    # Append fiber volume fraction dict to empty list above
    for i in range(101):
        e2eff_comparison_list.append({"Vf": materials[0].fiber_volfract[i]})

    # Update every dict in comparison list with effective modulus of every composite
    for i in range(len(materials)):
        for j in range(101):
            e2eff_comparison_list[j].update(
                {f"[{i+1}]\nE2*\n(GPa)": materials[i].eff_transverse_youngs_moduli[j]}
            )

    # Return a tuple consisting of comparison list and its assigned csv filename
    return (e2eff_comparison_list, test_name + "_E2eff.csv")


def _get_csv_comparison_data_and_filename_G12eff(
    materials: tuple[HT, ...], test_name: str
) -> tuple:
    """Get comparison data of effective axial shear moduli, G12eff of every UD
    composite and its associated comparison csv filename

    Note: A helper function that is called by ``save_compare`` function

    : param `materials`: UD composites where their specific effective elastic constant
        is collected
    : type: tuple of ```HT``` objects
    : raise TypeError: if materials is None, or UD composite in materials is either None
        or not ```HT``` object
    : return: Comparison data of G12eff for record keeping in csv file format
    : rtype: tuple
    """
    # Check for TypeError
    if len(materials) == 0:
        raise TypeError("Expect at least 2 UD composites of HT object for comparison")
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect every argument to be UD composite of HT object")

    # Get comparison data
    g12eff_comparison_list: list = []

    # Append fiber volume fraction dict to empty list above
    for i in range(101):
        g12eff_comparison_list.append({"Vf": materials[0].fiber_volfract[i]})

    # Update every dict in comparison list with effective modulus of every composite
    for i in range(len(materials)):
        for j in range(101):
            g12eff_comparison_list[j].update(
                {f"[{i+1}]\nG12*\n(GPa)": materials[i].eff_axial_shear_moduli[j]}
            )

    # Return a tuple consisting of comparison list and its assigned csv filename
    return (g12eff_comparison_list, test_name + "_G12eff.csv")


def _get_csv_comparison_data_and_filename_v12eff(
    materials: tuple[HT, ...], test_name: str
) -> tuple:
    """Get comparison data of effective major Poisson's ratios, v12eff of every UD
    composite and its associated comparison csv filename

    Note: A helper function that is called by ``save_compare`` function

    : param `materials`: UD composites where their specific effective elastic constant
        is collected
    : type: tuple of ```HT``` objects
    : raise TypeError: if materials is None, or UD composite in materials is either None
        or not ```HT``` object
    : return: Comparison data of v12eff for record keeping in csv file format
    : rtype: tuple
    """
    # Check for TypeError
    if len(materials) == 0:
        raise TypeError("Expect at least 2 UD composites of HT object for comparison")
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect every argument to be UD composite of HT object")

    # Get comparison data
    v12eff_comparison_list: list = []

    # Append fiber volume fraction dict to empty list above
    for i in range(101):
        v12eff_comparison_list.append({"Vf": materials[0].fiber_volfract[i]})

    # Update every dict in comparison list with effective modulus of every composite
    for i in range(len(materials)):
        for j in range(101):
            v12eff_comparison_list[j].update(
                {f"[{i+1}]\nv12*": materials[i].eff_major_poissons_ratios[j]}
            )

    # Return a tuple consisting of comparison list and its assigned csv filename
    return (v12eff_comparison_list, test_name + "_v12eff.csv")


def _get_csv_comparison_data_and_filename_G23eff(
    materials: tuple[HT, ...], test_name: str
) -> tuple:
    """Get comparison data of effective transverse shear moduli, G23eff of every UD
    composite and its associated comparison csv filename.

    Note: A helper function that is called by ``save_compare`` function.

    : param `materials`: UD composites where their specific effective elastic constant
        is collected
    : type: tuple of ```HT``` objects
    : raise TypeError: if materials is None, or UD composite in materials is either None
        or not ```HT``` object
    : return: Comparison data of G23eff for record keeping in csv file format
    : rtype: tuple
    """
    # Check for TypeError
    if len(materials) == 0:
        raise TypeError("Expect at least 2 UD composites of HT object for comparison")
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect every argument to be UD composite of HT object")

    # Get comparison data
    g23eff_comparison_list: list = []

    # Append fiber volume fraction dict to empty list above
    for i in range(101):
        g23eff_comparison_list.append({"Vf": materials[0].fiber_volfract[i]})

    # Update every dict in comparison list with effective modulus of every composite
    for i in range(len(materials)):
        for j in range(101):
            g23eff_comparison_list[j].update(
                {f"[{i+1}]\nG23*\n(GPa)": materials[i].eff_transverse_shear_moduli[j]}
            )

    # Return a tuple consisting of comparison list and its assigned csv filename
    return (g23eff_comparison_list, test_name + "_G23eff.csv")


def _get_csv_comparison_data_and_filename_K23eff(
    materials: tuple[HT, ...], test_name: str
) -> tuple:
    """Get comparison data of effective plane-strain bulk moduli, K23eff of every UD
    composite and its associated comparison csv filename

    Note: A helper function that is called by ``save_compare`` function

    : param `materials`: UD composites where their specific effective elastic constant
        is collected
    : type: tuple of ```HT``` objects
    : raise TypeError: if materials is None, or UD composite in materials is either None
        or not ```HT``` object
    : return: Comparison data of K23eff for record keeping in csv file format
    : rtype: tuple
    """
    # Check for TypeError
    if len(materials) == 0:
        raise TypeError("Expect at least 2 UD composites of HT object for comparison")
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError("Expect every argument to be UD composite of HT object")

    # Get comparison data
    k23eff_comparison_list: list = []

    # Append fiber volume fraction dict to empty list above
    for i in range(101):
        k23eff_comparison_list.append({"Vf": materials[0].fiber_volfract[i]})

    # Update every dict in comparison list with effective modulus of every composite
    for i in range(len(materials)):
        for j in range(101):
            k23eff_comparison_list[j].update(
                {f"[{i+1}]\nK23*\n(GPa)": materials[i].eff_pstrain_bulk_moduli[j]}
            )

    # Return a tuple consisting of comparison list and its assigned csv filename
    return (k23eff_comparison_list, test_name + "_K23eff.csv")


def plot(*materials: HT, folder: str = "png") -> None:
    """Plot six (6) effective elastic properties of UD composite versus fiber volume
    fraction and save them as png format file with a filename according to the effecitve
    elastic property being investigated postfixed with the name of UD composite being
    examed. Every png file will then be saved into a folder that bears the default name
    specifed by keyword parameter `folder`, e.g. `folder` = "png" unless renamed by the
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

        >>> carbon = Transtropic("Carbon", 250, 25, 20, 10, .28)
        >>> fiberglass = Isotropic("Fiberglass", 120, .29)
        >>> epoxy = Isotropic("Epoxy", 2.8, .3)
        >>> phenolic = Isotropic("Phenolic", 5, .33)
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
    """
    # Check for TypeError
    if len(materials) == 0:
        raise TypeError("Expect 'HT' object - UD composite material")
    for material in materials:
        if not isinstance(material, HT):
            raise TypeError("Expect arguments to be 'HT' type - UD composite material")

    for material in materials:
        # plot & confirm save for E1eff plot
        data_E1eff: tuple = _get_E1eff_data_for_plot_and_filename(material)
        filename_E1eff_plot: str = _plot_and_save(data_E1eff, folder)
        status_E1eff_saved_plot: bool = _is_confirmed(folder, filename_E1eff_plot)
        print(_get_confirmation_notices(status_E1eff_saved_plot, filename_E1eff_plot))

        # plot & confirm save for E2eff plot
        data_E2eff: tuple = _get_E2eff_data_for_plot_and_filename(material)
        filename_E2eff_plot: str = _plot_and_save(data_E2eff, folder)
        status_E2eff_saved_plot: bool = _is_confirmed(folder, filename_E2eff_plot)
        print(_get_confirmation_notices(status_E2eff_saved_plot, filename_E2eff_plot))

        # plot & confirm save for G12eff plot
        data_G12eff: tuple = _get_G12eff_data_for_plot_and_filename(material)
        filename_G12eff_plot: str = _plot_and_save(data_G12eff, folder)
        status_G12eff_saved_plot: bool = _is_confirmed(folder, filename_G12eff_plot)
        print(_get_confirmation_notices(status_G12eff_saved_plot, filename_G12eff_plot))

        # plot & confirm save for G23eff plot
        data_G23eff: tuple = _get_G23eff_data_for_plot_and_filename(material)
        filename_G23eff_plot: str = _plot_and_save(data_G23eff, folder)
        status_G23eff_saved_plot: bool = _is_confirmed(folder, filename_G23eff_plot)
        print(_get_confirmation_notices(status_G23eff_saved_plot, filename_G23eff_plot))

        # plot & confirm save for K23eff plot
        data_K23eff: tuple = _get_K23eff_data_for_plot_and_filename(material)
        filename_K23eff_plot: str = _plot_and_save(data_K23eff, folder)
        status_K23eff_saved_plot: bool = _is_confirmed(folder, filename_K23eff_plot)
        print(_get_confirmation_notices(status_K23eff_saved_plot, filename_K23eff_plot))

        # plot & confirm save for v12eff plot
        data_v12eff: tuple = _get_v12eff_data_for_plot_and_filename(material)
        filename_v12eff_plot: str = _plot_and_save(data_v12eff, folder)
        status_v12eff_saved_plot: bool = _is_confirmed(folder, filename_v12eff_plot)
        print(_get_confirmation_notices(status_v12eff_saved_plot, filename_v12eff_plot))


def _plot_and_save(data: tuple | None = None, folder: str | None = None) -> str:
    """Plot specific graph of effective elastic moduli according to data and defined
    style specified by user and save it as png format file with a unique name into a
    folder and then, return back the filename of the saved png file.

    Note: A helper function that is called by ``plot`` function

    : param `data`: Data that are used for plotting and labelling the graph where
        data[0] relates to filename, data[1] relates to data for x-axis, data[2] relates
        to data for y-axis, data[3] relates to name for legend, data[4] relates to x-
        axis label and data[5] relates to y-axis label
    : type: tuple
    : param `folder`: The folder where file containing the plot will be saved into
    : type: str
    : raise TypeError: If data is None and not tuple object or if folder is None and not
        str object
    : return: Return filename of saved png file that contains the plot
    : rtype: str
    """
    # Check for TypeError and ValueError
    if data is None or not isinstance(data, tuple):
        raise TypeError(
            "Expect first argument to be a tuple containing data for plotting graph"
        )
    if isinstance(data, tuple):
        if not isinstance(data[0], str):
            raise TypeError(
                "Expect tuple's first element is of str object - filename of png plot"
            )
        if isinstance(data[0], str):
            name = data[0].split(".")
            if name[1] != "png":
                raise ValueError(
                    "Expect tuple's first element is a filename of png plot"
                )
        if not isinstance(data[1], tuple) or not isinstance(data[2], tuple):
            raise TypeError(
                "Expect tuple's second and third element respectively be a tuple of "
                + "fiber volume fraction and a tuple of effective elastic modulus"
            )
        if isinstance(data[1], tuple) and isinstance(data[2], tuple):
            if len(data[1]) != len(data[2]):
                raise ValueError(
                    "Expect tuple's second and third element to be of equal size"
                )
        if (
            not isinstance(data[3], str)
            or not isinstance(data[4], str)
            or not isinstance(data[5], str)
        ):
            raise TypeError(
                "Expect tuple's fourth, fifth and sixth element is of str object"
            )
        if isinstance(data[4], str):
            if data[4] != "Vf":
                raise ValueError(
                    "Expect tuple fifth element to be 'Vf' for x-axis label"
                )
        if isinstance(data[5], str):
            if data[5] not in [
                "E1* (GPa)",
                "E2* (GPa)",
                "G12* (GPa)",
                "v12*",
                "G23* (GPa)",
                "K23* (GPa)",
            ]:
                raise ValueError(
                    "Expect tuple sixth element either 'E1* (GPa)', E2* (GPa) "
                    + "'G12* (GPa)', 'v12*', 'G23* (GPa)', 'K23* (GPa)'"
                )
    if folder is None or not isinstance(folder, str):
        raise TypeError(
            "Expect second argument to a folder where png file containing plot will be "
            + "saved and of a str type"
        )

    # Plot format
    plt.figure(figsize=(6, 4))
    plt.plot(data[1], data[2], ls="solid", color="k", label=data[3])
    plt.xlabel(data[4])
    plt.ylabel(data[5])
    plt.xticks(
        [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        fontsize=9,
    )
    plt.yticks(fontsize=9)
    if data[5] == "v12*":
        plt.legend(loc="upper right", fontsize=8.25)
    else:
        plt.legend(loc="upper left", fontsize=8.25)

    # Check whether directory already exists
    folder_path = f"./{folder}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder {folder_path} created")

    # Combine folder path and filename
    file_name = data[0]
    file_path = os.path.join(folder_path, file_name)

    # Close plot and save plot to png
    plt.savefig(file_path)
    plt.close()

    # Return filename of the png file that contains the graph for verification
    return file_name


def _get_E1eff_data_for_plot_and_filename(material: HT) -> tuple:
    """Get plot data for effective axial Young's moduli, E1eff

    Note: A helper function that is called by ``plot`` function

    : param `material`: UD composite
    : type: ```HT``` | None
    : raise TypeError: If material is not ```HT``` object and is None
    : return: Data of E1eff for graph plotting
    : rtype: tuple
    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("Expect argument to UD composite and of a HT object")

    # Return plot data for E1eff
    return (
        material.name + "_E1eff.png",
        material.fiber_volfract,
        material.eff_axial_youngs_moduli,
        material.name,
        "Vf",
        "E1* (GPa)",
    )


def _get_E2eff_data_for_plot_and_filename(material: HT) -> tuple:
    """Get plot data for effective transverse Young's moduli, E2eff

    Note: A helper function that is called by ``plot`` function

    : param `material`: UD composite
    : type: ```HT``` | None
    : raise TypeError: If material is not ```HT``` object and is None
    : return: Data of E2eff for graph plotting
    : rtype: tuple
    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("Expect argument to UD composite and of a HT object")

    # Return plot data for E2eff
    return (
        material.name + "_E2eff.png",
        material.fiber_volfract,
        material.eff_transverse_youngs_moduli,
        material.name,
        "Vf",
        "E2* (GPa)",
    )


def _get_G12eff_data_for_plot_and_filename(material: HT) -> tuple:
    """Get plot data for effective axial shear moduli, G12eff

    Note: A helper function that is called by ``plot`` function

    : param `material`: UD composite
    : type: ```HT``` | None
    : raise TypeError: If material is not ```HT``` object and is None
    : return: Data of G12eff for graph plotting
    : rtype: tuple
    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("Expect argument to UD composite and of a HT object")

    # Return plot data for G12eff
    return (
        material.name + "_G12eff.png",
        material.fiber_volfract,
        material.eff_axial_shear_moduli,
        material.name,
        "Vf",
        "G12* (GPa)",
    )


def _get_v12eff_data_for_plot_and_filename(material: HT) -> tuple:
    """Get plot data for effective major Poisson's ratios, v12eff

    Note: A helper function that is called by ``plot`` function

    : param `material`: UD composite
    : type: ```HT``` | None
    : raise TypeError: If material is not ```HT``` object and is None
    : return: Data of v12eff for graph plotting
    : rtype: tuple
    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("Expect argument to UD composite and of a HT object")

    # Return plot data for v12eff
    return (
        material.name + "_v12eff.png",
        material.fiber_volfract,
        material.eff_major_poissons_ratios,
        material.name,
        "Vf",
        "v12*",
    )


def _get_G23eff_data_for_plot_and_filename(material: HT) -> tuple:
    """Get plot data for effective transverse shear moduli, G23eff

    Note: A helper function that is called by ``plot`` function

    : param `material`: UD composite
    : type: ```HT``` | None
    : raise TypeError: If material is not ```HT``` object and is None
    : return: Data of G23eff for graph plotting
    : rtype: tuple
    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("Expect argument to UD composite and of a HT object")

    # Return plot data for G23eff
    return (
        material.name + "_G23eff.png",
        material.fiber_volfract,
        material.eff_transverse_shear_moduli,
        material.name,
        "Vf",
        "G23* (GPa)",
    )


def _get_K23eff_data_for_plot_and_filename(material: HT | None = None) -> tuple:
    """Get plot data for effective plane-strain bulk moduli, K23eff

    Note: A helper function that is called by ``plot`` function

    : param `material`: UD composite
    : type: ```HT``` | None
    : raise TypeError: If material is not ```HT``` object and is None
    : return: Data of K23eff for graph plotting
    : rtype: tuple
    """
    # Check for TypeError
    if material is None or not isinstance(material, HT):
        raise TypeError("Expect argument to be UD composite and of a HT object")

    # Return plot data for K23eff
    return (
        material.name + "_K23eff.png",
        material.fiber_volfract,
        material.eff_pstrain_bulk_moduli,
        material.name,
        "Vf",
        "K23* (GPa)",
    )


def plot_compare(
    *materials: HT,
    test_name: str = "compare",
    folder: str = "png",
) -> None:
    """Plot up to five (5) UD composites combined for each effective elastic property
    for comparison analysis and save each compared effective elastic moduli with a file
    name according to effective property under examination prefixed with the default
    name specified by keyword parameter `test_name`, e.g. `test_name` = "compare" unless
    redefined by a user. Every png file is then saved into a folder, which its name
    takes the default name of keyword parameter `folder`, e.g. `folder` = "png" unless
    re-specified by user.

    Note 1: Whenever a new file is generated and saved, a message stating the png file
    with relevant name is saved will be printed out.

    Note 2: If any of the folder does not exist yet, it will then be created and a
    message will appear saying a new folder with relevant name is created.

    : param materials: Minimum  two (2) or at most five (5) UD composites for comparison
    : type: ```HT```
    : raise TypeError: when each material in *materials is None or not ```HT``` object
    : raise ValueError: when the number of material in *materials is less than 2 or
        greater than 5.
    : rtype: None

    Example: 4 UD composites where their effective elastic properties are compared to
        one another where each elastic moduli has its own comparison png file, and they
        are saved inside a default folder - 'png'

        >>> carbon = Transtropic("Carbon", 250, 25, 20, 10, .28)
        >>> fiberglass = Isotropic("Fiberglass", 120, .29)
        >>> phenolic = Isotropic("Phenolic", 5, .3)
        >>> epoxy = Isotropic("Epoxy", 2.8, .3)
        >>>
        >>> compositeA = HT(carbon, phenolic)
        >>> compositeB = HT(carbon, epoxy)
        >>> compositeC = HT(fiberglass, phenolic)
        >>> compositeD = HT(fiberglass, epoxy)
        >>>
        >>> plot_compare(compositeA, compositeB, compositeC, compositeD)
        Folder ./png created
        ===================== compare_E1eff.png file saved! ======================
        ===================== compare_E2eff.png file saved! ======================
        ===================== compare_G12eff.png file saved! =====================
        ===================== compare_G23eff.png file saved! =====================
        ===================== compare_K23eff.png file saved! =====================
        ===================== compare_v12eff.png file saved! =====================
        >>>
    """
    # Check for TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise ValueError(
            "Expected at least two (2) or at most five (5) 'HT' objects for comparison"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError(
                "Expect argument to be a tuple of 'HT' type - UD composites"
            )

    # plot & confirm save for E1eff comparison plot
    comparison_data_E1eff: tuple = _get_comparison_E1eff_data_for_plot_and_filename(
        materials, test_name
    )
    filename_E1eff_plot: str = _plot_compare_and_save(comparison_data_E1eff, folder)
    status_E1eff_saved_plot: bool = _is_confirmed(folder, filename_E1eff_plot)
    print(_get_confirmation_notices(status_E1eff_saved_plot, filename_E1eff_plot))

    # plot & confirm save for E2eff comparison plot
    comparison_data_E2eff: tuple = _get_comparison_E2eff_data_for_plot_and_filename(
        materials, test_name
    )
    filename_E2eff_plot: str = _plot_compare_and_save(comparison_data_E2eff, folder)
    status_E2eff_saved_plot: bool = _is_confirmed(folder, filename_E2eff_plot)
    print(_get_confirmation_notices(status_E2eff_saved_plot, filename_E2eff_plot))

    # plot & confirm save for G12eff comparison_plot
    comparison_data_G12eff: tuple = _get_comparison_G12eff_data_for_plot_and_filename(
        materials, test_name
    )
    filename_G12eff_plot: str = _plot_compare_and_save(comparison_data_G12eff, folder)
    status_G12eff_saved_plot: bool = _is_confirmed(folder, filename_G12eff_plot)
    print(_get_confirmation_notices(status_G12eff_saved_plot, filename_G12eff_plot))

    # plot & confirm save for G23eff comparison plot
    comparison_data_G23eff: tuple = _get_comparison_G23eff_data_for_plot_and_filename(
        materials, test_name
    )
    filename_G23eff_plot: str = _plot_compare_and_save(comparison_data_G23eff, folder)
    status_G23eff_saved_plot: bool = _is_confirmed(folder, filename_G23eff_plot)
    print(_get_confirmation_notices(status_G23eff_saved_plot, filename_G23eff_plot))

    # plot & confirm save for K23eff comparison plot
    comparison_data_K23eff: tuple = _get_comparison_K23eff_data_for_plot_and_filename(
        materials, test_name
    )
    filename_K23eff_plot: str = _plot_compare_and_save(comparison_data_K23eff, folder)
    status_K23eff_saved_plot: bool = _is_confirmed(folder, filename_K23eff_plot)
    print(_get_confirmation_notices(status_K23eff_saved_plot, filename_K23eff_plot))

    # plot & confirm save for v12eff comparison plot
    comparison_data_v12eff: tuple = _get_comparison_v12eff_data_for_plot_and_filename(
        materials, test_name
    )
    filename_v12eff_plot: str = _plot_compare_and_save(comparison_data_v12eff, folder)
    status_v12eff_saved_plot: bool = _is_confirmed(folder, filename_v12eff_plot)
    print(_get_confirmation_notices(status_v12eff_saved_plot, filename_v12eff_plot))


def _plot_compare_and_save(comparison_data: tuple, folder: str) -> str:
    """Plot comparison graph of effective elastic properties according to the defined
    styles and save the plot as png format file into a folder.

    Note: A helper function that is called by ``plot_compare`` function

    : param `comparison_data`: Data that are used for plotting and labelling the graph
        where data[0] relates to filename, data[1] relates to data for x-axis, data[2]
        relates to data for y-axis, data[3] relates to name for legend, data[4] relates
        to x- axis label and data[5] relates to y-axis label
    : type: tuple
    : param `folder`: The folder where file containing the plot will be saved into
    : type: str
    : raise TypeError: If data is None and not tuple object or if folder is None and not
        str object
    : return: Return filename of saved png file that contains the plot
    : rtype: str
    """
    # Check for TypeError
    if comparison_data is None or not isinstance(comparison_data, tuple):
        raise TypeError(
            "Expect first argument to be a tuple containing data for plotting graph"
        )
    if folder is None or not isinstance(folder, str):
        raise TypeError(
            "Expect second argument to a folder where png file containing plot will be "
            + "saved and of a str type"
        )

    # Plot comparison data
    plt.figure(figsize=(6.5, 4))
    ln_sty = ["solid", "dashed", "dashdot", "dotted", (0, (3, 5, 1, 5))]
    for i in range(len(comparison_data[3])):
        plt.plot(
            comparison_data[1],
            comparison_data[2][i],
            ls=ln_sty[i],
            color="k",
            label=comparison_data[3][i],
        )
    plt.xlabel(comparison_data[4], fontsize=11)
    plt.ylabel(comparison_data[5], fontsize=11)
    plt.xticks(
        [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        fontsize=10,
    )
    plt.yticks(fontsize=10)
    if comparison_data[5] == "v12*":
        plt.legend(loc="upper right", fontsize=8.5)
    else:
        plt.legend(loc="upper left", fontsize=8.5)

    # Check whether directory already exists
    folder_path = f"./{folder}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("Folder %s created" % folder_path)

    # Combine folder path and filename
    file_name = comparison_data[0]
    file_path = os.path.join(folder_path, file_name)

    # Close plot and save plot to png
    plt.savefig(file_path)
    plt.close()

    # Return filename of the png file that contains the graph for verification
    return file_name


def _get_comparison_E1eff_data_for_plot_and_filename(
    materials: tuple[HT, ...], test_name: str
) -> tuple:
    """Get comparison plot data for effective axial Young's moduli, E1eff

    Note: A helper function that is called by ``plot_compare`` function

    : param `material`: UD composite
    : type: tuple[HT, ...]
    : param 'test_name': Prefix name for filename
    : type: str
    : raise TypeError: If material is not ```HT``` object and is None or test_name is
        None or not str type
    : raise ValueError: if total number of UD composite in materials is less than two
        (2) or greater than five (5)
    : return: Comparison data of E1eff for graph plotting
    : rtype: tuple
    """
    # Check for ValueError and TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise ValueError(
            "Expected at least two (2) or at most five (5) 'HT' objects for comparison"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError(
                "Expect argument to be a tuple of 'HT' type - UD composites"
            )
    if test_name is None or not isinstance(test_name, str):
        raise TypeError

    # Organize comparison data
    composite_name_group: list = []
    E1eff_group: list = []
    for material in materials:
        composite_name_group.append(material.name)
        E1eff_group.append(material.eff_axial_youngs_moduli)

    # Return comparison plot data for E1eff
    return (
        test_name + "_E1eff.png",
        materials[0].fiber_volfract,
        E1eff_group,
        composite_name_group,
        "Vf",
        "E1* (GPa)",
    )


def _get_comparison_E2eff_data_for_plot_and_filename(
    materials: tuple[HT, ...], test_name: str
) -> tuple:
    """Get comparison plot data for effective transverse Young's moduli, E2eff

    Note: A helper function that is called by ``plot_compare`` function

    : param `material`: UD composite
    : type: tuple[HT, ...]
    : param 'test_name': Prefix name for filename
    : type: str
    : raise TypeError: If material is not ```HT``` object and is None or test_name is
        None or not str type
    : raise ValueError: if total number of UD composite in materials is less than two
        (2) or greater than five (5)
    : return: Comparison data of E2eff for graph plotting
    : rtype: tuple
    """
    # Check for ValueError and TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise ValueError(
            "Expected at least two (2) or at most five (5) 'HT' objects for comparison"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError(
                "Expect argument to be a tuple of 'HT' type - UD composites"
            )
    if test_name is None or not isinstance(test_name, str):
        raise TypeError

    # Organize comparison data
    composite_name_group: list = []
    E2eff_group: list = []
    for material in materials:
        composite_name_group.append(material.name)
        E2eff_group.append(material.eff_transverse_youngs_moduli)

    # Return comparison plot data for E2eff
    return (
        test_name + "_E2eff.png",
        materials[0].fiber_volfract,
        E2eff_group,
        composite_name_group,
        "Vf",
        "E2* (GPa)",
    )


def _get_comparison_G12eff_data_for_plot_and_filename(
    materials: tuple[HT, ...], test_name: str
) -> tuple:
    """Get comparison plot data for effective axial shear moduli, G12eff

    Note: A helper function that is called by ``plot_compare`` function

    : param `material`: UD composite
    : type: tuple[HT, ...]
    : param 'test_name': Prefix name for filename
    : type: str
    : raise TypeError: If material is not ```HT``` object and is None or test_name is
        None or not str type
    : raise ValueError: if total number of UD composite in materials is less than two
        (2) or greater than five (5)
    : return: Comparison data of G12eff for graph plotting
    : rtype: tuple
    """
    # Check for ValueError and TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise ValueError(
            "Expected at least two (2) or at most five (5) 'HT' objects for comparison"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError(
                "Expect argument to be a tuple of 'HT' type - UD composites"
            )
    if test_name is None or not isinstance(test_name, str):
        raise TypeError

    # Organize comparison data
    composite_name_group: list = []
    G12eff_group: list = []
    for material in materials:
        composite_name_group.append(material.name)
        G12eff_group.append(material.eff_axial_shear_moduli)

    # Return comparison plot data for G12eff
    return (
        test_name + "_G12eff.png",
        materials[0].fiber_volfract,
        G12eff_group,
        composite_name_group,
        "Vf",
        "G12* (GPa)",
    )


def _get_comparison_v12eff_data_for_plot_and_filename(
    materials: tuple[HT, ...], test_name: str
) -> tuple:
    """Get comparison plot data for effective major Poisson's ratios, v12eff

    Note: A helper function that is called by ``plot_compare`` function

    : param `material`: UD composite
    : type: tuple[HT, ...]
    : param 'test_name': Prefix name for filename
    : type: str
    : raise TypeError: If material is not ```HT``` object and is None or test_name is
        None or not str type
    : raise ValueError: if total number of UD composite in materials is less than two
        (2) or greater than five (5)
    : return: Comparison data of v12eff for graph plotting
    : rtype: tuple
    """
    # Check for ValueError and TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise ValueError(
            "Expected at least two (2) or at most five (5) 'HT' objects for comparison"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError(
                "Expect argument to be a tuple of 'HT' type - UD composites"
            )
    if test_name is None or not isinstance(test_name, str):
        raise TypeError

    # Organize comparison data
    composite_name_group: list = []
    v12eff_group: list = []
    for material in materials:
        composite_name_group.append(material.name)
        v12eff_group.append(material.eff_major_poissons_ratios)

    # Return comparison plot data for v12eff
    return (
        test_name + "_v12eff.png",
        materials[0].fiber_volfract,
        v12eff_group,
        composite_name_group,
        "Vf",
        "v12* ",
    )


def _get_comparison_G23eff_data_for_plot_and_filename(
    materials: tuple[HT, ...], test_name: str
) -> tuple:
    """Get comparison plot data for effective transverse shear moduli, G23eff

    Note: A helper function that is called by ``plot_compare`` function

    : param `material`: UD composite
    : type: tuple[HT, ...]
    : param 'test_name': Prefix name for filename
    : type: str
    : raise TypeError: If material is not ```HT``` object and is None or test_name is
        None or not str type
    : raise ValueError: if total number of UD composite in materials is less than two
        (2) or greater than five (5)
    : return: Comparison data of G23eff for graph plotting
    : rtype: tuple
    """
    # Check for ValueError and TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise ValueError(
            "Expected at least two (2) or at most five (5) 'HT' objects for comparison"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError(
                "Expect argument to be a tuple of 'HT' type - UD composites"
            )
    if test_name is None or not isinstance(test_name, str):
        raise TypeError

    # Organize comparison data
    composite_name_group: list = []
    G23eff_group: list = []
    for material in materials:
        composite_name_group.append(material.name)
        G23eff_group.append(material.eff_transverse_shear_moduli)

    # Return comparison plot data for G23eff
    return (
        test_name + "_G23eff.png",
        materials[0].fiber_volfract,
        G23eff_group,
        composite_name_group,
        "Vf",
        "G23* (GPa)",
    )


def _get_comparison_K23eff_data_for_plot_and_filename(
    materials: tuple[HT, ...], test_name: str
) -> tuple:
    """Get comparison plot data for effective plane-strain bulk moduli, K23eff

    Note: A helper function that is called by ``plot_compare`` function

    : param `material`: UD composite
    : type: tuple[HT, ...]
    : param 'test_name': Prefix name for filename
    : type: str
    : raise TypeError: If material is not ```HT``` object and is None or test_name is
        None or not str type
    : raise ValueError: if total number of UD composite in materials is less than two
        (2) or greater than five (5)
    : return: Comparison data of K23eff for graph plotting
    : rtype: tuple
    """
    # Check for ValueError and TypeError
    if len(materials) < 2 or len(materials) > 5:
        raise ValueError(
            "Expected at least two (2) or at most five (5) 'HT' objects for comparison"
        )
    for material in materials:
        if material is None or not isinstance(material, HT):
            raise TypeError(
                "Expect argument to be a tuple of 'HT' type - UD composites"
            )
    if test_name is None or not isinstance(test_name, str):
        raise TypeError

    # Organize comparison data
    composite_name_group: list = []
    K23eff_group: list = []
    for material in materials:
        composite_name_group.append(material.name)
        K23eff_group.append(material.eff_pstrain_bulk_moduli)

    # Return comparison plot data for K23eff
    return (
        test_name + "_K23eff.png",
        materials[0].fiber_volfract,
        K23eff_group,
        composite_name_group,
        "Vf",
        "K23* (GPa)",
    )


def _is_confirmed(folder: str | None = None, file_name: str | None = None) -> bool:
    """Confirm whether the folder path with saved file exists

    Note: A helper function that is called by ``save``, ``save_compare``, ``plot``,
        ``plot_compare``, ``doc`` and ``doc_compare`` function

    : param `folder`: The path of folder where file to be saved
    : type: str | None
    : param `file_name`: Filename of png format file
    : type: str | None
    : raise TypeError: If either folder_path or file_name is None and not str type
    : return: True or False whether the folder path and the file exists
    : rtype: bool
    """
    # Check for TypeError
    if folder is None or not isinstance(folder, str):
        raise TypeError("Expect first argument to be folder path and of a str type")
    if file_name is None or not isinstance(file_name, str):
        raise TypeError("Expect second argument to be file name and of a str type")

    # Combine folder path and filename
    folder_path = f"./{folder}"
    file_path = os.path.join(folder_path, file_name)
    # Check the existence of the file and folder and as a result, return True or False
    return os.path.isfile(file_path)


def _get_confirmation_notices(
    status: bool | None = None, file_name: str | None = None
) -> str:
    """Get confirmation status notices

    Note: A helper function that is called by ``save``, ``save_compare``, ``plot``,
    ``plot_compare``, ``doc`` and ``doc_compare`` function

    : param `status`: True or False wether file exists or not respectively
    : type: bool | None
    : param `file_name`: Name of the file
    : type: str | None
    : raise TypeError: If `status` is None and not boolean type or if `file_name` is
        None and not str type
    : return: Status message wether file is saved or not saved in the respective folder
    : rtype: tuple
    """
    # Check for TypeError
    if status is None or not isinstance(status, bool):
        raise TypeError(
            "Expect first argument to be the confirmation status whether exist or not "
            + "exists and of a boolean type"
        )
    if file_name is None or not isinstance(file_name, str):
        raise TypeError("Expect second argument to be the filename and of a str type")

    # Return confirmation notices
    if status:
        sentence = f" {file_name} file saved! "
        if len(sentence) > 70:
            raise ValueError("Sentence has to be shorter than 70 total characters.")
        return sentence.center(74, "=")
    else:
        sentence = f" {file_name} is missing! "
        if len(sentence) > 70:
            raise ValueError("Sentence has to be shorter than 70 total characters.")
        return sentence.center(74, "=")


def doc(*composites: HT, doc_name: str = "analysis", doc_num: str = "Appx. A") -> None:
    """Create a pdf document documenting the result of Halpin-Tsai micromechanics
    analysis for a single UD or multiple UD composite material and save it with a
    filename that has prefix name as per defined by user or default value based on the
    keyword parameter - `doc_name`, e.g. `doc_name` = "analysis". The pdf will then be
    saved in a folder called "pdf", which is the sub-folder of the main, master folder
    that has the same name defined by the keyword parameter `doc_name`, which by default
    is "analysis".

    In general, the pdf document consists of four (4) parts. The first part is the
    front page of report where a report number can be defined by user or takes the
    default value set another keyword parameter, e.g. `report_num` = "-NA-". The front
    page also provides spaces for document sign-off, verified by the person who conduct
    the analysis and certified by a person who's authorized to approve the analysis
    results. The second part is on the UD composite's phase elastic moduli where they
    are presented in a table format. The third part shows the plots of effective
    elastic properties of UD composite versus fiber volume fraction. The fourth part
    provides a table that shows the data on effective elastic properties versus fiber
    volume fraction.

    Note 1: While generating the report, supporting files that support the documents are
    also generated. For example, for each UD composite reported, two (2) or three (3)
    csv files on its constituent's elastic moduli and its effective elastic properties
    are produced and furthermore, six (6) png format files for its six different
    effective elastic properties are also generated. Every file will be saved in a
    folder according to their default format as per ``save`` and ``plot`` functions.
    For example, png file will be saved in a folder called "png" while csv file in a
    "csv" folder. All these folders will be the sub-folders under the main, master
    folder, which by default is "analysis.

    Note 2: Whenever a new file is generated and saved, a message stating the name of
    the file is saved will appear.

    Note 3: If any of the folder does not exist yet, it will then be created and a
    message will appear saying a new folder with relevant name is created.

    : param `composites`: A single or multiple UD composites that will be documented.
    : type: ```HT```
    : param `doc_name`: Keyword parameter - the name of the pdf report and folder where
        pdf document will be saved into
    : param `doc_num`: Keyword parameter - the serial number of the report.
    : raise TypeError: When composites is None and is not ```HT``` object
    : rtype: None

    Example: 2 UD composites are being documented in a single pdf file.

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
        >>> compositeA = HT(carbon, epoxy)
        >>> compositeB = HT(fiberglass, epoxy)
        >>>
        >>> doc(compositeA, compositeB)
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
        =========== Fiberglass-Epoxy_phases_iso_moduli.csv file saved! ===========
        ============== Fiberglass-Epoxy_eff_moduli.csv file saved! ===============
        ================= Fiberglass-Epoxy_E1eff.png file saved! =================
        ================= Fiberglass-Epoxy_E2eff.png file saved! =================
        ================ Fiberglass-Epoxy_G12eff.png file saved! =================
        ================ Fiberglass-Epoxy_G23eff.png file saved! =================
        ================ Fiberglass-Epoxy_K23eff.png file saved! =================
        ================ Fiberglass-Epoxy_v12eff.png file saved! =================
        Folder ./analysis/pdf created
        --------------------------------------------------------------------------
                              analysis_report.pdf file saved!
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        >>>
    """
    # Check for TypeError
    if len(composites) == 0:
        raise TypeError("Expected argument to be 'HT' object - UD composite")

    for composite in composites:
        if not isinstance(composite, HT):
            raise TypeError("Expected argument to be 'HT' object - UD composite")

    # Set today's date for generating report's date in doc and doc_compare function
    today = datetime.date.today()

    # Define header and footer for adding new page using class
    class PDF(FPDF):  # Inherits from imported FPDF
        """Class for header and footer of FPDF"""

        def header(self):  # header function
            if self.page_no() != 1:
                pdf.set_font("Times", "B", 15)  # Set header font
                # Print title
                self.cell(
                    0,
                    15,
                    "HALPIN-TSAI MICROMECHANICS ANALYSIS",
                    border=1,
                    align="C",
                )
                self.ln(20)  # line break

        def footer(self):  # footer function
            if self.page_no() != 1:
                pdf.set_font("Times", "", 9)  # Set footer font
                self.set_y(-15)  # Position cursor 1.5 cm from bottom
                self.cell(
                    0,
                    10,
                    f"Page {self.page_no()}/{{nb}}",
                    new_x=XPos.RIGHT,
                    new_y=YPos.TOP,
                    align="C",
                )

    # Function to draw table 2 that spans 3 pages
    def __draw_table(data: list | None = None) -> None:
        """Print table of data

        : param data: Data to be tabulated
        : type: list
        : raise TypeError: When data is None or not a 'list'
        : rtype: None
        """
        # Check for TypeError
        if data is None or not isinstance(data, list):
            raise TypeError(
                "Expected 1 arguments"
                """\n\t 1st arg: 'list' type object - list of data lists"""
            )
        # Draw table with following format
        pdf.set_font("Times", "", 10)
        pdf.set_line_width(0.3)  # table header line
        headings_style = FontFace(emphasis="BOLD", color=0)
        with pdf.table(
            borders_layout="SINGLE_TOP_LINE",
            col_widths=(24, 24, 24, 24, 24, 24, 24),
            headings_style=headings_style,
            line_height=5,
            text_align=(  # type: ignore[arg-type]
                "CENTER",
                "CENTER",
                "CENTER",
                "CENTER",
                "CENTER",
                "CENTER",
                "CENTER",
            ),
            width=170,
        ) as table:
            # print data
            for data_row in data:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

    # START OF PDF DOCUMENT
    # Instantiate PDF object called pdf
    pdf = PDF(orientation="P", unit="mm", format="A4")

    # SECTION 0 - FRONT PAGE (PAGE 1)
    pdf.add_page()
    # Print title
    pdf.ln(90)  # line break
    pdf.set_font("Times", "B", 18)  # Set header font
    pdf.cell(
        0,
        50,
        f"CS50P - MICROMECHANICS LAB",
        border=1,
        align="C",
    )
    pdf.ln(5)  # line break
    pdf.set_font("Times", "B", 12)  # Set header font
    pdf.cell(
        0, 15, f"Lab Report No: {doc_num}", align="C", new_x="LMARGIN", new_y="NEXT"
    )
    pdf.ln(10)  # line break
    pdf.set_font("Times", "B", 12)  # Set header font
    pdf.cell(0, 15, f"Date: {today}", align="C", new_x="LMARGIN", new_y="NEXT")

    # Document sign-off section
    pdf.set_font("Times", "", 11)
    pdf.ln(30)
    pdf.cell(25)  # Move cell to right
    pdf.cell(50, 15, "Test performed by:", align="C")
    pdf.cell(35)  # Move cell to further right
    pdf.cell(50, 15, "Test certified by:", align="C")
    pdf.ln(25)
    pdf.cell(15)  # Move cell to right
    pdf.cell(50, 15, "Name:", align="C")
    pdf.cell(38)  # Move cell to further right
    pdf.cell(50, 15, "Name:", align="C")
    pdf.ln(5)
    pdf.cell(14)  # Move cell to right
    pdf.cell(50, 15, "Data:", align="C")
    pdf.cell(38)  # Move cell to further right
    pdf.cell(50, 15, "Date:", align="C")

    # Report for each UD composite material
    for composite in composites:
        # NEW PAGE
        pdf.add_page()

        # SECTION 1
        # Name UD composite
        pdf.ln(5)
        pdf.set_font("Times", "B", 11)
        pdf.cell(
            0,
            9,
            f"UD Composite: {(composite.name).upper()}",
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        # Save UD composite info to csv file
        save(composite, folder=f"{doc_name}/csv")

        # Print UD composite constituents' elastic moduli
        # If both constituents' types are Isotropic
        if type(composite.fiber) == Isotropic and type(composite.matrix) == Isotropic:
            # Retrieve data from csv file to print elastic moduli for fiber and matrix
            folder_path = f"./{doc_name}/csv"
            file_name = composite.name + "_phases_iso_moduli.csv"
            # Join folder_path with file_name
            file_path = os.path.join(folder_path, file_name)
            # Open csv file
            with open(file_path, encoding="utf8") as csv_file:
                data_table1 = list(csv.reader(csv_file, delimiter=","))

            # Table 1 title
            pdf.cell(
                0,
                9,
                "Table 1: Constituent's elastic properties",
                align="C",
                new_x="LMARGIN",
                new_y="NEXT",
            )

            # Set table 1 format
            pdf.set_font("Times", "", 10)
            pdf.set_line_width(0.2)
            pdf.line(x1=25, y1=53, x2=185, y2=53)  # table top line
            pdf.line(x1=25, y1=79, x2=185, y2=79)  # table bottom ine
            pdf.set_line_width(0.3)  # table header line
            headings_style = FontFace(emphasis="BOLD", color=0)
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                col_widths=(30, 30, 30, 30, 30),
                headings_style=headings_style,
                line_height=5,
                text_align=("LEFT", "CENTER", "CENTER", "CENTER", "CENTER"),  # type: ignore[arg-type]
                width=160,
            ) as table:
                # print data
                for data_row in data_table1:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
            pdf.set_line_width(0.2)
            pdf.ln(5)

        # If both constituents' types are Transtropic
        elif (
            type(composite.fiber) == Transtropic
            and type(composite.matrix) == Transtropic
        ):
            # Retrieve data from csv file to print elastic moduli for fiber and matrix
            folder_path = f"./{doc_name}/csv"
            file_name = composite.name + "_phases_tra_moduli.csv"
            # Join folder_path with file_name
            file_path = os.path.join(folder_path, file_name)
            # Open csv file
            with open(file_path, encoding="utf8") as csv_file:
                data_table1 = list(csv.reader(csv_file, delimiter=","))

            # Table 1 title
            pdf.cell(
                0,
                9,
                "Table 1: Constituent's elastic properties",
                align="C",
                new_x="LMARGIN",
                new_y="NEXT",
            )

            # Set table 1 format
            pdf.set_font("Times", "", 10)
            pdf.set_line_width(0.2)
            pdf.line(x1=20, y1=53, x2=190, y2=53)  # table top line
            pdf.line(x1=20, y1=84, x2=190, y2=84)  # table bottom ine
            pdf.set_line_width(0.3)  # table header line
            headings_style = FontFace(emphasis="BOLD", color=0)
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                col_widths=(24, 24, 24, 24, 24, 24, 24),
                headings_style=headings_style,
                line_height=5,
                text_align=(  # type: ignore[arg-type]
                    "LEFT",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                ),
                width=170,
            ) as table:
                # print data
                for data_row in data_table1:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
            pdf.set_line_width(0.2)

        # If fiber's type is Transtropic and matrix's type is Isotropic
        elif (
            type(composite.fiber) == Transtropic and type(composite.matrix) == Isotropic
        ):
            # Retrieve data from that csv file to print table for Transtropic fiber
            folder_path = f"./{doc_name}/csv"
            file_name = composite.name + "_fiber_tra_moduli.csv"
            # Join folder_path with file_name
            file_path = os.path.join(folder_path, file_name)
            # Open csv file
            with open(file_path, encoding="utf8") as csv_file:
                data_table1 = list(csv.reader(csv_file, delimiter=","))

            # Table 1 title
            pdf.cell(
                0,
                9,
                "Table 1.A: Fiber's elastic properties",
                align="C",
                new_x="LMARGIN",
                new_y="NEXT",
            )

            # Set table format for fiber
            pdf.set_font("Times", "", 10)
            pdf.set_line_width(0.2)
            pdf.line(x1=20, y1=53, x2=190, y2=53)  # table top line
            pdf.line(x1=20, y1=79, x2=190, y2=79)  # table bottom ine
            pdf.set_line_width(0.3)  # table header line
            headings_style = FontFace(emphasis="BOLD", color=0)
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                col_widths=(24, 24, 24, 24, 24, 24, 24),
                headings_style=headings_style,
                line_height=5,
                text_align=(  # type: ignore[arg-type]
                    "LEFT",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                ),
                width=170,
            ) as table:
                # print data
                for data_row in data_table1:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
            pdf.set_line_width(0.2)

            # Retrieve data from that csv file to print table for Isotropic matrix
            folder_path = f"./{doc_name}/csv"
            file_name = composite.name + "_matrix_iso_moduli.csv"
            # Join folder_path with file_name
            file_path = os.path.join(folder_path, file_name)
            # Open csv file
            with open(file_path, encoding="utf8") as csv_file:
                data_table1 = list(csv.reader(csv_file, delimiter=","))

            # Table 1 title
            pdf.ln(10)
            pdf.set_font("Times", "B", 11)
            pdf.cell(
                0,
                9,
                "Table 1.B: Matrix's elastic properties",
                align="C",
                new_x="LMARGIN",
                new_y="NEXT",
            )

            # Set table format for matrix
            pdf.set_font("Times", "", 10)
            pdf.set_line_width(0.2)
            pdf.line(x1=25, y1=97, x2=185, y2=97)  # table top line
            pdf.line(x1=25, y1=118, x2=185, y2=118)  # table bottom ine
            pdf.set_line_width(0.3)  # table header line
            headings_style = FontFace(emphasis="BOLD", color=0)
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                col_widths=(30, 30, 30, 30, 30),
                headings_style=headings_style,
                line_height=5,
                text_align=("LEFT", "CENTER", "CENTER", "CENTER", "CENTER"),  # type: ignore[arg-type]
                width=160,
            ) as table:
                # print data
                for data_row in data_table1:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
            pdf.set_line_width(0.2)
            pdf.ln(5)

        # If fiber's type is Isotropic and matrix's type is Transtropic
        else:
            # Retrieve data from that csv file to print table for isotropic fiber
            folder_path = f"./{doc_name}/csv"
            file_name = composite.name + "_fiber_iso_moduli.csv"
            # Join folder_path with file_name
            file_path = os.path.join(folder_path, file_name)
            # Open csv file
            with open(file_path, encoding="utf8") as csv_file:
                data_table1 = list(csv.reader(csv_file, delimiter=","))

            # Table 1 title
            pdf.cell(
                0,
                9,
                "Table 1.A: Fiber's elastic properties",
                align="C",
                new_x="LMARGIN",
                new_y="NEXT",
            )

            # Set table format for fiber
            pdf.set_font("Times", "", 10)
            pdf.set_line_width(0.2)
            pdf.line(x1=25, y1=53, x2=185, y2=53)  # table top line
            pdf.line(x1=25, y1=74, x2=185, y2=74)  # table bottom ine
            pdf.set_line_width(0.3)  # table header line
            headings_style = FontFace(emphasis="BOLD", color=0)
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                col_widths=(30, 30, 30, 30, 30),
                headings_style=headings_style,
                line_height=5,
                text_align=("LEFT", "CENTER", "CENTER", "CENTER", "CENTER"),  # type: ignore[arg-type]
                width=160,
            ) as table:
                # print data
                for data_row in data_table1:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
            pdf.set_line_width(0.2)
            pdf.ln(5)

            # Retrieve data from that csv file to print table for transtropic matrix
            folder_path = f"./{doc_name}/csv"
            file_name = composite.name + "_matrix_tra_moduli.csv"
            # Join folder_path with file_name
            file_path = os.path.join(folder_path, file_name)
            # Open csv file
            with open(file_path, encoding="utf8") as csv_file:
                data_table1 = list(csv.reader(csv_file, delimiter=","))

            # Table 1 title
            pdf.ln(10)
            pdf.set_font("Times", "B", 11)
            pdf.cell(
                0,
                9,
                "Table 1.B: Matrix's elastic properties",
                align="C",
                new_x="LMARGIN",
                new_y="NEXT",
            )

            # Set table format for matrix
            pdf.set_font("Times", "", 10)
            pdf.set_line_width(0.2)
            pdf.line(x1=20, y1=97, x2=190, y2=97)  # table top line
            pdf.line(x1=20, y1=123, x2=190, y2=123)  # table bottom ine
            pdf.set_line_width(0.3)  # table header line
            headings_style = FontFace(emphasis="BOLD", color=0)
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                col_widths=(24, 24, 24, 24, 24, 24, 24),
                headings_style=headings_style,
                line_height=5,
                text_align=(  # type: ignore[arg-type]
                    "LEFT",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                ),
                width=170,
            ) as table:
                # print data
                for data_row in data_table1:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
            pdf.set_line_width(0.2)

        # SECTION 2
        # NEW PAGE
        pdf.add_page()

        pdf.ln(5)
        pdf.set_font("Times", "B", 11)
        pdf.cell(
            0,
            9,
            f"UD Composite: {(composite.name).upper()}",
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        # Save plots first
        plot(composite, folder=f"{doc_name}/png")

        # Print subtitles for the figures
        pdf.ln(61)
        pdf.set_font("Times", "", 9)
        pdf.cell(27)  # Move cell to right
        pdf.cell(50, 15, "a) Effective axial Young's modulus", align="C")
        pdf.cell(38)  # Move cell to further right
        pdf.cell(50, 15, "b) Effective transverse Young's modulus", align="C")
        pdf.ln(61)
        pdf.cell(27)  # Move cell to right
        pdf.cell(50, 15, "c) Effective axial shear modulus", align="C")
        pdf.cell(38)  # Move cell to further right
        pdf.cell(50, 15, "d) Effective major Poisson's ratio", align="C")
        pdf.ln(61)
        pdf.cell(27)  # Move cell to right
        pdf.cell(50, 15, "e) Effective transverse shear modulus", align="C")
        pdf.cell(38)  # Move cell to further right
        pdf.cell(50, 15, "f) Effective plane-strain bulk modulus", align="C")
        # pdf.cell(0, 15, "", new_x="LMARGIN", new_y="NEXT", align="C")

        # Print title of figures
        pdf.ln(15)
        pdf.set_font("Times", "B", 10)
        pdf.cell(
            0,
            5,
            f"Figure 1: {composite.name} composite - Effective elastic properties",
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        # Embed PNG Images - Results of Micromechanics Rule of Mixtures analysis
        # Figure a) Effective axial Young's modulus
        pdf.image(
            f"./{doc_name}/png/{composite.name}" + "_E1eff.png",
            x=20,
            y=53,
            w=85,
            keep_aspect_ratio=True,
        )
        # Figure b) Effective transverse Young's modulus
        pdf.image(
            f"./{doc_name}/png/{composite.name}" + "_E2eff.png",
            x=108,
            y=53,
            w=85,
            keep_aspect_ratio=True,
        )
        # Figure c) Effective axial shear modulus
        pdf.image(
            f"./{doc_name}/png/{composite.name}" + "_G12eff.png",
            x=20,
            y=114,
            w=85,
            keep_aspect_ratio=True,
        )
        # Figure d) Effective major Poisson's ratio
        pdf.image(
            f"./{doc_name}/png/{composite.name}" + "_v12eff.png",
            x=108,
            y=114,
            w=85,
            keep_aspect_ratio=True,
        )
        # Figure e) Effective transverse shear modulus
        pdf.image(
            f"./{doc_name}/png/{composite.name}" + "_G23eff.png",
            x=20,
            y=175,
            w=85,
            keep_aspect_ratio=True,
        )
        # Figure f) Effective plane-strain bulk modulus
        pdf.image(
            f"./{doc_name}/png/{composite.name}" + "_K23eff.png",
            x=108,
            y=175,
            w=85,
            keep_aspect_ratio=True,
        )

        # NEW PAGE
        pdf.add_page()

        # SECTION 3
        # Print table 2 title
        pdf.ln(1)
        pdf.set_font("Times", "B", 11)
        pdf.cell(
            0,
            12,
            f"Table 2: {composite.name} composite - Effective elastic properties",
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        # Retrieve data from that csv file to print Table 1
        folder_path = f"./{doc_name}/csv"
        file_name = composite.name + "_eff_moduli.csv"
        # Join folder_path with file_name
        file_path = os.path.join(folder_path, file_name)

        # Process header data for table 2
        with open(file_path, encoding="utf8") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            # list comprehension to filter row
            data_header = [row for index, row in enumerate(data) if index == 0]

        # Process needed data for table 2 on page 2
        with open(file_path, encoding="utf8") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            # list comprehension to filter row
            data_needed = [
                row for index, row in enumerate(data) if index in range(1, 45)
            ]

        # Combine data for data 1
        data_table2_1 = data_header + data_needed

        # Draw table 2 with data_1 on page 2
        pdf.set_line_width(0.2)  # table top line
        pdf.line(x1=20, y1=42, x2=190, y2=42)
        __draw_table(data_table2_1)
        pdf.set_line_width(0.2)

        # NEW PAGE
        pdf.add_page()

        # Process continuing needed data for table 2 on subsequent second page
        with open(file_path, encoding="utf8") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            # list comprehension to filter row
            data_needed = [
                row for index, row in enumerate(data) if index in range(45, 91)
            ]

        # Combine data
        data_table2_2 = data_header + data_needed

        pdf.ln(5)
        # Continue draw table 2 with data_2 on page 3
        pdf.line(x1=20, y1=34, x2=190, y2=34)
        __draw_table(data_table2_2)
        pdf.set_line_width(0.2)

        # NEW PAGE
        pdf.add_page()

        # Process continuing needed data for table 2 on subsequent third
        with open(file_path, encoding="utf8") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            # list comprehension to filter row
            data_needed = [
                row for index, row in enumerate(data) if index in range(91, 102)
            ]

        # Combine data
        data_table2_3 = data_header + data_needed

        pdf.ln(5)
        # Continue draw table 2 with data_2 on third page
        pdf.line(x1=20, y1=34, x2=190, y2=34)
        __draw_table(data_table2_3)
        pdf.line(x1=20, y1=100, x2=190, y2=100)
        pdf.set_line_width(0.2)

    # Produce pdf report
    sentence = f"{doc_name}_report.pdf file saved!"
    folder_path = f"./{doc_name}/pdf"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("Folder %s created" % folder_path)
    file_name = doc_name + "_report.pdf"
    file_path = os.path.join(folder_path, file_name)
    pdf.output(file_path)
    print("--------------------------------------------------------------------------")
    print(sentence.center(74))
    print("''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")


def doc_compare(
    *composites: HT, doc_name: str = "comparison", doc_num: str = "1"
) -> None:
    """
    Create a pdf document documenting the result of Halpin-Tsai micromechanics
    comparison analysis between a minimum of two (2) or at most five (5) UD composites
    and save it with a filename that has prefix name as per defined by user or default
    value based on the keyword parameter - `doc_name`, e.g. `doc_name`; = "comparison".
    The pdf report will then be saved in a folder called "pdf", which is the sub-folder
    of the main master folder that has the same name specified by the keyword parameter
    `doc_name`, which by default is "analysis".

    In general, the pdf document consists of four (4) parts. The first part is the
    front page of report where a report number can be defined by user or takes the
    default value set another keyword parameter, e.g. `report_num` = "-NA-". The front
    page also contain spaces for document sign-off, verified by the person who conducts
    the comparison analysis and certified by a person who has the authority to certify
    the analysis results. The second part is on the UD composite's phase elastic moduli
    where they are presented in a table format. The third part shows the plots of
    effective elastic properties of UD composite versus fiber volume fraction. The
    fourth part provides a table that shows the data on effective elastic properties
    versus fiber volume fraction. This part has six (6) sub-parts that shows the
    comparison data on each effective elastic properties.

    Note 1: While generating the report, supporting files that support the documents are
    also generated. For example, for each UD composite being compared, two (2) or three
    (3) csv files on its constituent's elastic moduli and its effective elastic
    properties are produced. In addition to that six (6) csv files comprising the
    comparison data of every effective elastic moduli for all UD composites being
    compared. Lastly, six (6) png format files for every effective elastic moduli plots
    between all UD composites. Every file will be saved in a folder according to their
    format and folder's name following the default values specified in the ``save``,
    ``save_compare`` and ``plot_compare`` functions. For example, png file will be saved
    in a folder called "png" while csv file in a "csv" folder. All these folders will be
    the sub-folders under the main master folder, by default called "comparison" folder.

    Note 2: Whenever a new file is generated and saved, a message stating the name of
    the file is saved will appear.

    Note 3: If any of the folder does not exist yet, it will then be created and a
    message will appear saying a new folder with relevant name is created.

    : param `composites`: At minimum two (2) UD composites or at most five (5) UD
        composites for comparison analysis
    : type: ```HT```
    : param `doc_name`: The name of comparison report and the postfix name for every
        file saved
    : type: str
    : param `doc_num`: Report number of the comparison test
    : type: str
    : raise TypeError: When composites is None or not ```HT``` type
    : rtype: None

    Example: The comparison of 4 UD composites in a single pdf file

        >>> carbon = Transtropic("Carbon", 250, 25, 20, 10, .28)
        >>> fiberglass = Isotropic("Fiberglass", 120, .29)
        >>> phenolic = Isotropic("Phenolic", 5, .33)
        >>> epoxy = Isotropic("Epoxy", 2.8, .3)
        >>>
        >>> compositeA = HT(carbon, epoxy)
        >>> compositeB = HT(carbon, phenolic)
        >>> compositeC = HT(fiberglass, epoxy)
        >>> compositeD = HT(fiberglass, phenolic)
        >>>
        >>> doc_compare(compositeA, compositeB, compositeC, compositeD)
        Folder ./comparison/csv created
        ============= Carbon-Epoxy_fiber_tra_moduli.csv file saved! ==============
        ============= Carbon-Epoxy_matrix_iso_moduli.csv file saved! =============
        ================ Carbon-Epoxy_eff_moduli.csv file saved! =================
        ============ Carbon-Phenolic_fiber_tra_moduli.csv file saved! ============
        =========== Carbon-Phenolic_matrix_iso_moduli.csv file saved! ============
        =============== Carbon-Phenolic_eff_moduli.csv file saved! ===============
        =========== Fiberglass-Epoxy_phases_iso_moduli.csv file saved! ===========
        ============== Fiberglass-Epoxy_eff_moduli.csv file saved! ===============
        ========= Fiberglass-Phenolic_phases_iso_moduli.csv file saved! ==========
        ============= Fiberglass-Phenolic_eff_moduli.csv file saved! =============
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
    """
    # Checj for ValueError on composites
    if len(composites) < 2 or len(composites) > 5:
        raise ValueError(
            "Expected at least 2 or at most 5 'HT' object for comparison purposes"
        )
    # Check for TypeError
    for composite in composites:
        if not isinstance(composite, HT):
            raise TypeError("Expected argument to be 'HT' object - UD composite")

    # Set today's date for generating report's date in doc and doc_compare function
    today = datetime.date.today()

    # Define header and footer for adding new page using class
    class PDF(FPDF):  # Inherits from imported FPDF
        """Class to define header and footer"""

        def header(self):  # header function
            """Define header"""
            if self.page_no() != 1:
                pdf.set_font("Times", "B", 15)  # Set header font
                # Print title
                self.cell(
                    0,
                    15,
                    "HALPIN-TSAI MICROMECHANICS COMPARISON ANALYSIS",
                    border=1,
                    align="C",
                )
                self.ln(20)  # line break

        def footer(self):  # footer function
            """Define footer"""
            if self.page_no() != 1:
                pdf.set_font("Times", "", 9)  # Set footer font
                self.set_y(-15)  # Position cursor 1.5 cm from bottom
                self.cell(
                    0,
                    10,
                    f"Page {self.page_no()}/{{nb}}",
                    new_x=XPos.RIGHT,
                    new_y=YPos.TOP,
                    align="C",
                )

    # Function to draw complete comparison table
    def __get_comparison_table(
        path_to_file: str | None = None,
        number_of_composites: int | None = None,
    ) -> None:
        """Print whole comparison table

        : param path_to_file: Combined folder path and file name
        : type: str
        : param number_of_composites: Number of UD composites for comparison analysis
        : type: int
        : raise TypeError: If any of the parameters is None or not according to their
            types
        : rtype: None
        """
        # Check for TypeError
        if path_to_file is None or not isinstance(path_to_file, str):
            raise TypeError("Expected first argument to be list data to be printed out")
        if number_of_composites is None or not isinstance(number_of_composites, int):
            raise TypeError(
                "Expected second argument to be int - number of composites compared"
            )

        # Process header data for table
        with open(path_to_file, encoding="utf8") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            # list comprehension to filter row
            data_header = [row for index, row in enumerate(data) if index == 0]

        # Process needed data for table on data part 1
        with open(path_to_file, encoding="utf8") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            # list comprehension to filter row
            data_needed = [
                row for index, row in enumerate(data) if index in range(1, 37)
            ]

        # Combine header with data part 1
        data_table3A_1 = data_header + data_needed

        # Draw table data part 1
        __draw_comparison_table(data_table3A_1, number_of_composites)
        pdf.set_line_width(0.2)

        # NEW PAGE
        pdf.add_page()

        # Process continuing needed data for table on data part 2
        with open(path_to_file, encoding="utf8") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            # list comprehension to filter row
            data_needed = [
                row for index, row in enumerate(data) if index in range(37, 82)
            ]

        # Combine header with data part 2
        data_table3A_2 = data_header + data_needed

        pdf.ln(5)
        # Continue draw table with data part 2
        pdf.line(x1=20, y1=34, x2=190, y2=34)
        __draw_comparison_table(data_table3A_2, number_of_composites)
        pdf.set_line_width(0.2)

        # NEW PAGE
        pdf.add_page()

        # Process continuing needed data for table on data part 3
        with open(path_to_file, encoding="utf8") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            # list comprehension to filter row
            data_needed = [
                row for index, row in enumerate(data) if index in range(82, 102)
            ]

        # Combine header with data part 3
        data_table3A_3 = data_header + data_needed

        pdf.ln(5)
        # Continue draw table 3 with data part 3
        pdf.line(x1=20, y1=34, x2=190, y2=34)
        __draw_comparison_table(data_table3A_3, number_of_composites)
        pdf.line(x1=20, y1=150, x2=190, y2=150)
        pdf.set_line_width(0.2)

    # Function to draw comparison table per page
    def __draw_comparison_table(
        data: list | None = None, number_of_composites: int | None = None
    ) -> None:
        """Tabulate comparison data inside table

        : param `data`: Comparison data to be tabulated
        : type: list
        : param `number_of_composites`: Number of UD composites for comparison analysis
        : type: int
        : raise TypeError: If any of the parameters is None or not according to their
            type
        : rtype: None
        """
        # Check for TypeError
        if data is None or not isinstance(data, list):
            raise TypeError("Expected first argument to be list data to be printed out")
        if number_of_composites is None or not isinstance(number_of_composites, int):
            raise TypeError(
                "Expected second argument to be int - number of composites compared"
            )

        # Draw table with following format
        pdf.set_font("Times", "", 10)
        pdf.set_line_width(0.3)  # table header line
        headings_style = FontFace(emphasis="BOLD", color=0)
        if number_of_composites == 2:
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                headings_style=headings_style,
                line_height=5,
                col_widths=(24, 25, 25),
                text_align=(  # type: ignore[arg-type]
                    "CENTER",
                    "CENTER",
                    "CENTER",
                ),
                width=85,
            ) as table:
                # print data
                for data_row in data:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
        elif number_of_composites == 3:
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                headings_style=headings_style,
                line_height=5,
                col_widths=(25, 25, 25, 25),
                text_align=(  # type: ignore[arg-type]
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                ),
                width=110,
            ) as table:
                # print data
                for data_row in data:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
        elif number_of_composites == 4:
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                headings_style=headings_style,
                line_height=5,
                col_widths=(25, 25, 25, 25, 25),
                text_align=(  # type: ignore[arg-type]
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                ),
                width=135,
            ) as table:
                # print data
                for data_row in data:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
        else:
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                headings_style=headings_style,
                line_height=5,
                col_widths=(25, 25, 25, 25, 25, 25),
                text_align=(  # type: ignore[arg-type]
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                ),
                width=160,
            ) as table:
                # print data
                for data_row in data:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)

    # START OF THE PDF DOCUMENT
    # Instantiate PDF object called pdf
    pdf = PDF(orientation="P", unit="mm", format="A4")

    # FRONT PAGE (PAGE 1)
    pdf.add_page()
    # Print title
    pdf.ln(90)  # line break
    pdf.set_font("Times", "B", 18)  # Set header font
    pdf.cell(
        0,
        50,
        f"CS50P - MICROMECHANICS LAB",
        border=1,
        align="C",
    )
    pdf.ln(5)  # line break
    pdf.set_font("Times", "B", 12)  # Set header font
    pdf.cell(
        0, 15, f"LAB REPORT NO: {doc_num}", align="C", new_x="LMARGIN", new_y="NEXT"
    )
    pdf.ln(10)  # line break
    pdf.set_font("Times", "B", 12)  # Set header font
    pdf.cell(0, 15, f"Date: {today}", align="C", new_x="LMARGIN", new_y="NEXT")

    # Approval section
    pdf.set_font("Times", "", 11)
    pdf.ln(30)
    pdf.cell(25)  # Move cell to right
    pdf.cell(50, 15, "Test performed by:", align="C")
    pdf.cell(35)  # Move cell to further right
    pdf.cell(50, 15, "Test certified by:", align="C")
    pdf.ln(25)
    pdf.cell(15)  # Move cell to right
    pdf.cell(50, 15, "Name:", align="C")
    pdf.cell(38)  # Move cell to further right
    pdf.cell(50, 15, "Name:", align="C")
    pdf.ln(5)
    pdf.cell(14)  # Move cell to right
    pdf.cell(50, 15, "Data:", align="C")
    pdf.cell(38)  # Move cell to further right
    pdf.cell(50, 15, "Date:", align="C")

    # NEW PAGE - SECTION 1: CONSTITUENT'S ELASTIC PROPERTIES
    pdf.add_page()

    pdf.ln(10)
    pdf.set_font("Times", "B", 11)
    pdf.cell(
        0,
        5,
        "SECTION 1: UD COMPOSITE CONSTITUENT'S ELASTIC PROPERTIES",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(5)

    # Counter for page control in printing out constituent's elastic moduli
    transtropic_counter = 0
    isotropic_counter = 0
    page_counter = 0

    # Report on constituent's elastic moduli for each UD composite material
    for i in range(len(composites)):
        # Page control
        if (
            transtropic_counter == 3
            or (transtropic_counter == 2 and isotropic_counter == 2)
        ) and page_counter == 0:
            pdf.add_page()
            page_counter = 1
            # Print section title
            pdf.ln(10)
            pdf.set_font("Times", "B", 11)
            pdf.cell(
                0,
                5,
                "SECTION 1: UD COMPOSITE CONSTITUENT'S ELASTIC PROPERTIES (CONT.)",
                align="C",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            pdf.ln(5)

        # save to csv file
        save(composites[i], folder=f"{doc_name}/csv")

        # If their types are both Isotropic
        if (
            type(composites[i].fiber) == Isotropic
            and type(composites[i].matrix) == Isotropic
        ):
            isotropic_counter += 1
            # Table's title
            pdf.set_font("Times", "B", 10)
            pdf.cell(
                0,
                9,
                f"Table 1-{i+1}: {(composites[i].name).upper()}",
                align="C",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            # Retrieve data from csv file to print elastic moduli for fiber and matrix
            folder_path = f"./{doc_name}/csv"
            file_name = composites[i].name + "_phases_iso_moduli.csv"
            # Join folder_path with file_name
            file_path = os.path.join(folder_path, file_name)
            # Open csv file
            with open(file_path, encoding="utf8") as csv_file:
                data_table1 = list(csv.reader(csv_file, delimiter=","))

            # Set table 1 format
            pdf.set_font("Times", "", 10)
            pdf.set_line_width(0.2)
            pdf.set_line_width(0.3)  # table header line
            headings_style = FontFace(emphasis="", color=0)
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                col_widths=(30, 30, 30, 30, 30),
                headings_style=headings_style,
                line_height=5,
                text_align=("LEFT", "CENTER", "CENTER", "CENTER", "CENTER"),  # type: ignore[arg-type]
                width=160,
            ) as table:
                # print data
                for data_row in data_table1:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
            pdf.set_line_width(0.2)
            pdf.ln(5)

        # If their types are both Transtropic
        elif (
            type(composites[i].fiber) == Transtropic
            and type(composites[i].matrix) == Transtropic
        ):
            # Table's title
            pdf.set_font("Times", "B", 10)
            pdf.cell(
                0,
                9,
                f"Table 1-{i+1}: {(composites[i].name).upper()}",
                align="C",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            isotropic_counter += 1
            # Retrieve data from csv file to print elastic moduli for fiber and matrix
            folder_path = f"./{doc_name}/csv"
            file_name = composites[i].name + "_phases_tra_moduli.csv"
            # Join folder_path with file_name
            file_path = os.path.join(folder_path, file_name)
            # Open csv file
            with open(file_path, encoding="utf8") as csv_file:
                data_table1 = list(csv.reader(csv_file, delimiter=","))

            # Set table 1 format
            pdf.set_font("Times", "", 10)
            pdf.set_line_width(0.2)
            pdf.set_line_width(0.3)  # table header line
            headings_style = FontFace(emphasis="", color=0)
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                col_widths=(24, 24, 24, 24, 24, 24, 24),
                headings_style=headings_style,
                line_height=5,
                text_align=(  # type: ignore[arg-type]
                    "LEFT",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                ),
                width=170,
            ) as table:
                # print data
                for data_row in data_table1:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
            pdf.set_line_width(0.2)
            pdf.ln(5)

        # If fiber's type is Transtropic and matrix's type is Isotropic
        elif (
            type(composites[i].fiber) == Transtropic
            and type(composites[i].matrix) == Isotropic
        ):
            # Page control
            if transtropic_counter == 1 and isotropic_counter == 3 and i == 4:
                pdf.add_page()
                # Print section title
                pdf.ln(10)
                pdf.set_font("Times", "B", 11)
                pdf.cell(
                    0,
                    5,
                    "SECTION 1: UD COMPOSITE CONSTITUENT'S ELASTIC PROPERTIES (CONT.)",
                    align="C",
                    new_x="LMARGIN",
                    new_y="NEXT",
                )
                pdf.ln(5)
            # Table's title
            pdf.set_font("Times", "B", 10)
            pdf.cell(
                0,
                9,
                f"Table 1-{i+1}: {(composites[i].name).upper()}",
                align="C",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            transtropic_counter += 1
            # Retrieve data from that csv file to print table for Transtropic fiber
            folder_path = f"./{doc_name}/csv"
            file_name = composites[i].name + "_fiber_tra_moduli.csv"
            # Join folder_path with file_name
            file_path = os.path.join(folder_path, file_name)
            # Open csv file
            with open(file_path, encoding="utf8") as csv_file:
                data_table1 = list(csv.reader(csv_file, delimiter=","))

            # Set table format for fiber
            pdf.set_font("Times", "", 10)
            pdf.set_line_width(0.2)
            pdf.set_line_width(0.3)  # table header line
            headings_style = FontFace(emphasis="", color=0)
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                col_widths=(24, 24, 24, 24, 24, 24, 24),
                headings_style=headings_style,
                line_height=5,
                text_align=(  # type: ignore[arg-type]
                    "LEFT",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                ),
                width=170,
            ) as table:
                # print data
                for data_row in data_table1:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
            pdf.set_line_width(0.2)
            pdf.ln(5)

            # Retrieve data from that csv file to print table for Isotropic matrix
            folder_path = f"./{doc_name}/csv"
            file_name = composites[i].name + "_matrix_iso_moduli.csv"
            # Join folder_path with file_name
            file_path = os.path.join(folder_path, file_name)
            # Open csv file
            with open(file_path, encoding="utf8") as csv_file:
                data_table1 = list(csv.reader(csv_file, delimiter=","))

            # Set table format for matrix
            pdf.set_font("Times", "", 10)
            pdf.set_line_width(0.2)
            pdf.set_line_width(0.3)  # table header line
            headings_style = FontFace(emphasis="", color=0)
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                col_widths=(30, 30, 30, 30, 30),
                headings_style=headings_style,
                line_height=5,
                text_align=("LEFT", "CENTER", "CENTER", "CENTER", "CENTER"),  # type: ignore[arg-type]
                width=160,
            ) as table:
                # print data
                for data_row in data_table1:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
            pdf.set_line_width(0.2)
            pdf.ln(5)

        # If fiber's type is Isotropic and matrix's type is Transtropic
        else:
            # Page control
            if transtropic_counter == 1 and isotropic_counter == 3 and i == 4:
                pdf.add_page()
                # Print section title
                pdf.ln(10)
                pdf.set_font("Times", "B", 11)
                pdf.cell(
                    0,
                    5,
                    "SECTION 1: UD COMPOSITE CONSTITUENT'S ELASTIC PROPERTIES (CONT.)",
                    align="C",
                    new_x="LMARGIN",
                    new_y="NEXT",
                )
                pdf.ln(5)
            # Table's title
            pdf.set_font("Times", "B", 10)
            pdf.cell(
                0,
                9,
                f"Table 1-{i+1}: {(composites[i].name).upper()}",
                align="C",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            transtropic_counter += 1
            # Retrieve data from that csv file to print table for isotropic fiber
            folder_path = f"./{doc_name}/csv"
            file_name = composites[i].name + "_fiber_iso_moduli.csv"
            # Join folder_path with file_name
            file_path = os.path.join(folder_path, file_name)
            # Open csv file
            with open(file_path, encoding="utf8") as csv_file:
                data_table1 = list(csv.reader(csv_file, delimiter=","))

            # Set table format for fiber
            pdf.set_font("Times", "", 10)
            pdf.set_line_width(0.2)
            pdf.set_line_width(0.3)  # table header line
            headings_style = FontFace(emphasis="", color=0)
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                col_widths=(30, 30, 30, 30, 30),
                headings_style=headings_style,
                line_height=5,
                text_align=("LEFT", "CENTER", "CENTER", "CENTER", "CENTER"),  # type: ignore[arg-type]
                width=160,
            ) as table:
                # print data
                for data_row in data_table1:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
            pdf.set_line_width(0.2)
            pdf.ln(5)

            # Retrieve data from that csv file to print table for transtropic matrix
            folder_path = f"./{doc_name}/csv"
            file_name = composites[i].name + "_matrix_tra_moduli.csv"
            # Join folder_path with file_name
            file_path = os.path.join(folder_path, file_name)
            # Open csv file
            with open(file_path, encoding="utf8") as csv_file:
                data_table1 = list(csv.reader(csv_file, delimiter=","))

            # Set table format for matrix
            pdf.set_font("Times", "", 10)
            pdf.set_line_width(0.2)
            pdf.set_line_width(0.3)  # table header line
            headings_style = FontFace(emphasis="", color=0)
            with pdf.table(
                borders_layout="SINGLE_TOP_LINE",
                col_widths=(24, 24, 24, 24, 24, 24, 24),
                headings_style=headings_style,
                line_height=5,
                text_align=(  # type: ignore[arg-type]
                    "LEFT",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                    "CENTER",
                ),
                width=170,
            ) as table:
                # print data
                for data_row in data_table1:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
            pdf.set_line_width(0.2)
            pdf.ln(5)

    # NEW PAGE - SECTION 2: GRAPHS
    pdf.add_page()

    pdf.ln(8)
    pdf.set_font("Times", "B", 11)
    pdf.cell(
        0,
        5,
        "SECTION 2: UD COMPOSITES - GRAPHS ON EFFECTIVE ELASTOC PROPERTIES",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    # Create png files on the comparison of effective elastic properties
    if len(composites) == 2:
        plot_compare(
            composites[0],
            composites[1],
            test_name=doc_name,
            folder=f"{doc_name}/png",
        )
    elif len(composites) == 3:
        plot_compare(
            composites[0],
            composites[1],
            composites[2],
            test_name=doc_name,
            folder=f"{doc_name}/png",
        )
    elif len(composites) == 4:
        plot_compare(
            composites[0],
            composites[1],
            composites[2],
            composites[3],
            test_name=doc_name,
            folder=f"{doc_name}/png",
        )
    else:
        plot_compare(
            composites[0],
            composites[1],
            composites[2],
            composites[3],
            composites[4],
            test_name=doc_name,
            folder=f"{doc_name}/png",
        )

    # Subtitles for the figures of PNG images
    pdf.set_font("Times", "", 10)
    pdf.ln(101)
    pdf.cell(0, 10, "2-A) Effective axial Young's modulus", align="C")
    pdf.ln(102)
    pdf.cell(0, 15, "2-B) Effective transverse Young's modulus", align="C")

    # Embed PNG Images - Results of Micromechanics Rule of Mixtures analysis
    # Figure a) Effective axial Young's modulus
    pdf.image(
        f"./{doc_name}/png/{doc_name}" + "_E1eff.png",
        x=35,
        y=55,
        w=140,
        keep_aspect_ratio=True,
    )
    # Figure b) Effective transverse Young's modulus
    pdf.image(
        f"./{doc_name}/png/{doc_name}" + "_E2eff.png",
        x=35,
        y=160,
        w=140,
        keep_aspect_ratio=True,
    )

    # NEW PAGE - SECTION 2: GRAPHS (Cont.)
    pdf.add_page()

    pdf.ln(8)
    pdf.set_font("Times", "B", 11)
    pdf.cell(
        0,
        5,
        "SECTION 2: UD COMPOSITES - GRAPHS ON EFFECTIVE ELASTOC PROPERTIES (CONT.)",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    # Subtitles for the figures of PNG images
    pdf.set_font("Times", "", 10)
    pdf.ln(101)
    pdf.cell(0, 10, "2-C) Effective axial shear modulus", align="C")
    pdf.ln(102)
    pdf.cell(0, 15, "2-D) Effective major Poissons' ratio", align="C")

    # Embed PNG Images - Results of Micromechanics Rule of Mixtures analysis
    # Figure a) Effective axial Young's modulus
    pdf.image(
        f"./{doc_name}/png/{doc_name}" + "_G12eff.png",
        x=35,
        y=55,
        w=140,
        keep_aspect_ratio=True,
    )
    # Figure b) Effective transverse Young's modulus
    pdf.image(
        f"./{doc_name}/png/{doc_name}" + "_v12eff.png",
        x=35,
        y=160,
        w=140,
        keep_aspect_ratio=True,
    )

    # NEW PAGE - SECTION 2: GRAPHS (Cont.)
    pdf.add_page()

    pdf.ln(8)
    pdf.set_font("Times", "B", 11)
    pdf.cell(
        0,
        5,
        "SECTION 2: UD COMPOSITES - GRAPHS ON EFFECTIVE ELASTOC PROPERTIES (CONT.)",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    # Subtitles for the figures of PNG images
    pdf.set_font("Times", "", 10)
    pdf.ln(101)
    pdf.cell(0, 10, "2-E) Effective transverse shear modulus", align="C")
    pdf.ln(102)
    pdf.cell(0, 15, "2-F) Effective plane-strain bulk modulus", align="C")

    # Embed PNG Images - Results of Micromechanics Rule of Mixtures analysis
    # Figure a) Effective axial Young's modulus
    pdf.image(
        f"./{doc_name}/png/{doc_name}" + "_G23eff.png",
        x=35,
        y=55,
        w=140,
        keep_aspect_ratio=True,
    )
    # Figure b) Effective transverse Young's modulus
    pdf.image(
        f"./{doc_name}/png/{doc_name}" + "_K23eff.png",
        x=35,
        y=160,
        w=140,
        keep_aspect_ratio=True,
    )

    # NEW PAGE - SECTION 3: COMPARE E1eff
    pdf.add_page()

    # Save comparison data on csv for retrieval on comparison analysis
    if len(composites) == 2:
        save_compare(
            composites[0],
            composites[1],
            test_name=doc_name,
            folder=f"{doc_name}/csv",
        )
    elif len(composites) == 3:
        save_compare(
            composites[0],
            composites[1],
            composites[2],
            test_name=doc_name,
            folder=f"{doc_name}/csv",
        )
    elif len(composites) == 4:
        save_compare(
            composites[0],
            composites[1],
            composites[2],
            composites[3],
            test_name=doc_name,
            folder=f"{doc_name}/csv",
        )
    else:
        save_compare(
            composites[0],
            composites[1],
            composites[2],
            composites[3],
            composites[4],
            test_name=doc_name,
            folder=f"{doc_name}/csv",
        )

    # NEW PAGE - SECTION 3-A - COMPARING E1EFF
    # Print table 3-A title
    pdf.ln(1)
    pdf.set_font("Times", "B", 11)
    pdf.cell(
        0,
        12,
        f"SECTION 3-A: COMPARISON ON EFFECTIVE AXIAL YOUNG'S MODULI ",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.line(x1=20, y1=41, x2=190, y2=41)

    # Print UD composites involved in data representation in the table 3A
    for i in range(len(composites)):
        pdf.cell(27)  # Move cell to right
        pdf.cell(50, 8, f"[{i+1}] - {composites[i].name}", align="L")
        pdf.ln(5)
    pdf.ln(3)
    pdf.cell(0, 7, "", align="C", new_x="LMARGIN", new_y="NEXT")

    # Get number of composites to be compared
    num_comp = len(composites)

    # Retrieve data from that csv file to print Table 3A
    folder_path = f"./{doc_name}/csv"
    file_name = doc_name + "_E1eff.csv"
    # Join folder_path with file_name
    file_path = os.path.join(folder_path, file_name)

    # Print whole comparison Table 3-A for E1eff
    __get_comparison_table(file_path, num_comp)

    # NEW PAGE - SECTION 3-B: COMPARE E2eff
    pdf.add_page()

    # Print table 3B title
    pdf.ln(1)
    pdf.set_font("Times", "B", 11)
    pdf.cell(
        0,
        12,
        f"SECTION 3B: COMPARISON ON EFFECTIVE TRANSVERSE YOUNG'S MODULI ",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.line(x1=20, y1=41, x2=190, y2=41)

    # Print UD composites involved in data representation in the table 3B
    for i in range(len(composites)):
        pdf.cell(27)  # Move cell to right
        pdf.cell(50, 8, f"[{i+1}] - {composites[i].name}", align="L")
        pdf.ln(5)
    pdf.ln(3)
    pdf.cell(0, 7, "", align="C", new_x="LMARGIN", new_y="NEXT")

    # Retrieve data from that csv file to print Table 3B
    folder_path = f"./{doc_name}/csv"
    file_name = doc_name + "_E2eff.csv"
    # Join folder_path with file_name
    file_path = os.path.join(folder_path, file_name)

    # Print whole comparison Table 3-B for E2eff
    __get_comparison_table(file_path, num_comp)

    # NEW PAGE - SECTION 3-C: COMPARE G12eff
    pdf.add_page()

    # Print table 3-C title
    pdf.ln(1)
    pdf.set_font("Times", "B", 11)
    pdf.cell(
        0,
        12,
        f"SECTION 3-C: COMPARISON ON EFFECTIVE AXIAL SHEAR MODULI ",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.line(x1=20, y1=41, x2=190, y2=41)

    # Print UD composites involved in data representation in the table 3C
    for i in range(len(composites)):
        pdf.cell(27)  # Move cell to right
        pdf.cell(50, 8, f"[{i+1}] - {composites[i].name}", align="L")
        pdf.ln(5)
    pdf.ln(3)
    pdf.cell(0, 7, "", align="C", new_x="LMARGIN", new_y="NEXT")

    # Retrieve data from that csv file to print Table 3C
    folder_path = f"./{doc_name}/csv"
    file_name = doc_name + "_G12eff.csv"
    # Join folder_path with file_name
    file_path = os.path.join(folder_path, file_name)

    # Print whole comparison Table 3-C for G12eff
    __get_comparison_table(file_path, num_comp)

    # NEW PAGE - SECTION 3-D: COMPARE v12eff
    pdf.add_page()

    # Print table 3-D title
    pdf.ln(1)
    pdf.set_font("Times", "B", 11)
    pdf.cell(
        0,
        12,
        f"SECTION 3-D: COMPARISON ON EFFECTIVE MAJOR POISSON'S RATIO ",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.line(x1=20, y1=41, x2=190, y2=41)

    # Print UD composites involved in data representation in the table 3D
    for i in range(len(composites)):
        pdf.cell(27)  # Move cell to right
        pdf.cell(50, 8, f"[{i+1}] - {composites[i].name}", align="L")
        pdf.ln(5)
    pdf.ln(3)
    pdf.cell(0, 7, "", align="C", new_x="LMARGIN", new_y="NEXT")

    # Retrieve data from that csv file to print Table 3D
    folder_path = f"./{doc_name}/csv"
    file_name = doc_name + "_v12eff.csv"
    # Join folder_path with file_name
    file_path = os.path.join(folder_path, file_name)

    # Print whole comparison Table 3-D for v12eff
    __get_comparison_table(file_path, num_comp)

    # NEW PAGE - SECTION 3-E: COMPARE G23eff
    pdf.add_page()

    # Print table 3-E title
    pdf.ln(1)
    pdf.set_font("Times", "B", 11)
    pdf.cell(
        0,
        12,
        f"SECTION 3-E: COMPARISON ON EFFECTIVE TRANSVERSE SHEAR MODULI ",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.line(x1=20, y1=41, x2=190, y2=41)

    # Print UD composites involved in data representation in the table 3E
    for i in range(len(composites)):
        pdf.cell(27)  # Move cell to right
        pdf.cell(50, 8, f"[{i+1}] - {composites[i].name}", align="L")
        pdf.ln(5)
    pdf.ln(3)
    pdf.cell(0, 7, "", align="C", new_x="LMARGIN", new_y="NEXT")

    # Retrieve data from that csv file to print Table 3E
    folder_path = f"./{doc_name}/csv"
    file_name = doc_name + "_G23eff.csv"
    # Join folder_path with file_name
    file_path = os.path.join(folder_path, file_name)

    # Print whole comparison Table 3-E for G23eff
    __get_comparison_table(file_path, num_comp)

    # NEW PAGE - SECTION 3-F: COMPARE K23eff
    pdf.add_page()

    # Print table 3-F title
    pdf.ln(1)
    pdf.set_font("Times", "B", 11)
    pdf.cell(
        0,
        12,
        f"SECTION 3-F: COMPARISON ON EFFECTIVE PLANE-STRAIN BULK MODULI ",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.line(x1=20, y1=41, x2=190, y2=41)

    # Print UD composites involved in data representation in the table 3F
    for i in range(len(composites)):
        pdf.cell(27)  # Move cell to right
        pdf.cell(50, 8, f"[{i+1}] - {composites[i].name}", align="L")
        pdf.ln(5)
    pdf.ln(3)
    pdf.cell(0, 7, "", align="C", new_x="LMARGIN", new_y="NEXT")

    # Retrieve data from that csv file to print Table 3F
    folder_path = f"./{doc_name}/csv"
    file_name = doc_name + "_K23eff.csv"
    # Join folder_path with file_name
    file_path = os.path.join(folder_path, file_name)

    # Print whole comparison Table 3-F for K23eff
    __get_comparison_table(file_path, num_comp)

    # Produce pdf report
    sentence = f"{doc_name}_report.pdf file saved!"
    folder_path = f"./{doc_name}/pdf"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("Folder %s created" % folder_path)
    file_name = doc_name + "_report.pdf"
    file_path = os.path.join(folder_path, file_name)
    pdf.output(file_path)
    print("--------------------------------------------------------------------------")
    print(sentence.center(74))
    print("''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")


if __name__ == "__main__":
    main()
