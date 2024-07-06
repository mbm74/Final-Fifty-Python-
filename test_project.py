from project import Isotropic, Transtropic, HT  # classes in project.py
from project import (  # ``display`` & helper functions that support ``display`` major function
    display,
    _get_main_title_for_UD_composite,
    _get_sub_title_for_fiber,
    _get_sub_title_for_matrix,
    _get_sub_title_for_composite,
    _get_fiber_and_matrix_properties,
    _get_effective_properties_versus_full_range_Vf,
    _get_effective_properties_versus_specific_value_Vf,
    _get_effective_properties_versus_specific_range_Vf,
    _print_tabulate,
)
from project import (  # ``save`` function & helper functions that support ``save`` major function
    save,
    _get_phase_elastic_moduli_and_filename,
    _get_effective_elastic_moduli_and_filename,
    _save_csv_file,
    _is_confirmed,
    _get_confirmation_notices,
)
from project import (  # ``plot`` function & helper functions that support ``plot`` major function
    plot,
    _get_E1eff_data_for_plot_and_filename,
    _get_E2eff_data_for_plot_and_filename,
    _get_G12eff_data_for_plot_and_filename,
    _get_G23eff_data_for_plot_and_filename,
    _get_K23eff_data_for_plot_and_filename,
    _get_v12eff_data_for_plot_and_filename,
    _plot_and_save,
)
from decimal import *
import pytest
import csv
import os


# Unit tests conducted only on:
#   - Test_Isotropic class: all methods in ```Isotropic``` class
#   - Test_Display class: ``display`` major function and all its helper functions
#   - Test_Save class: ``save`` major function and all its helper functions
#   - Test_Plot class: ``plot`` major function and all its helper functions


class Test_Isotropic:
    """Test suite that contains unit tests for all methods in Isotropic class"""

    @pytest.fixture
    def fiberglass(self):
        """
        Provide argument on fiberglass isotropic material
        """
        return Isotropic(name="Fiberglass", youngs_modulus=120, poissons_ratio=0.29)

    @pytest.fixture
    def epoxy(self):
        """
        Provide argument on epoxy isotropic material
        """
        return Isotropic(name="Epoxy", youngs_modulus=2.8, poissons_ratio=0.3)

    @pytest.fixture
    def expected_return_value_fiberglass(self, fiberglass):
        """
        Expected output of ``get_info`` method for fiberglass isotropic material
        """
        return {
            "Constituent": fiberglass.name,
            "Young's\nModulus,\nE (GPa)": fiberglass.youngs_modulus,
            "Poisson's\nRatio,\nv": fiberglass.poissons_ratio,
            "Shear\nModulus,\nG (GPa)": fiberglass.shear_modulus,
            "Plane-strain\nBulk Modulus,\nK (GPa)": fiberglass.pstrain_bulk_modulus,
        }

    @pytest.fixture
    def expected_return_value_epoxy(self, epoxy):
        """
        Expected output of ``get_info`` method for epoxy isotropic material
        """
        return {
            "Constituent": epoxy.name,
            "Young's\nModulus,\nE (GPa)": epoxy.youngs_modulus,
            "Poisson's\nRatio,\nv": epoxy.poissons_ratio,
            "Shear\nModulus,\nG (GPa)": epoxy.shear_modulus,
            "Plane-strain\nBulk Modulus,\nK (GPa)": epoxy.pstrain_bulk_modulus,
        }

    @pytest.fixture
    def expected_output_epoxy(self, epoxy):
        """
        Expected output of ``__str__`` method for epoxy isotropic material
        """
        return (
            f"\033[3mobj\033[0m.name: '{epoxy.name}', "
            + "\033[3mobj\033[0m.youngs_modulus: "
            + f"Decimal('{epoxy.youngs_modulus}'), "
            + "\033[3mobj\033[0m.poissons_ratio: "
            + f"Decimal('{epoxy.poissons_ratio}'),"
            + "\033[3mobj\033[0m.shear_modulus: "
            + f"Decimal('{epoxy.shear_modulus}'), "
            + "\033[3mobj\033[0m.pstrain_bulk_modulus: "
            + f"Decimal('{epoxy.pstrain_bulk_modulus}')"
        )

    @pytest.fixture
    def expected_output_fiberglass(self, fiberglass):
        """
        Expected output of ``__str__`` method for epoxy isotropic material
        """
        return (
            f"\033[3mobj\033[0m.name: '{fiberglass.name}', "
            + "\033[3mobj\033[0m.youngs_modulus: "
            + f"Decimal('{fiberglass.youngs_modulus}'), "
            + "\033[3mobj\033[0m.poissons_ratio: "
            + f"Decimal('{fiberglass.poissons_ratio}'),"
            + "\033[3mobj\033[0m.shear_modulus: "
            + f"Decimal('{fiberglass.shear_modulus}'), "
            + "\033[3mobj\033[0m.pstrain_bulk_modulus: "
            + f"Decimal('{fiberglass.pstrain_bulk_modulus}')"
        )

    def test_str_method_output_1(self, fiberglass, expected_output_fiberglass):
        """
        Test the output of ``__str__`` method using valid argument - fiberglass
        isotropic material
        """
        assert str(fiberglass) == expected_output_fiberglass

    def test_str_method_output_2(self, epoxy, expected_output_epoxy):
        """
        Test the output of ``__str__`` method using valid argument - epoxy isotropic
        material
        """
        assert str(epoxy) == expected_output_epoxy

    def test_get_info_output_1(self, fiberglass, expected_return_value_fiberglass):
        """
        Test the output of ``get_info`` method using valid argument - fiberglass
        isotropic material
        """
        assert fiberglass._get_info() == expected_return_value_fiberglass

    def test_get_info_output_2(self, epoxy, expected_return_value_epoxy):
        """
        Test the output of ``get_info`` method using valid argument - epoxy isotropic
        material
        """
        assert epoxy._get_info() == expected_return_value_epoxy

    def test_properties_output_1(self, fiberglass):
        """
        Test the output of every ``@property`` method using valid argument - fiberglass
        isotropic material
        """
        assert fiberglass.name == "Fiberglass"  # @property for name
        assert fiberglass.youngs_modulus == Decimal(
            "120.000"
        )  # @property for youngs_modulus
        assert fiberglass.poissons_ratio == Decimal(
            "0.290"
        )  # @property for poissons_ratio
        assert fiberglass.shear_modulus == Decimal(
            "46.512"
        )  # @property for shear_modulus
        assert fiberglass.pstrain_bulk_modulus == Decimal(
            "110.742"
        )  # @property for pstrain_bulk_modulus

    def test_properties_output_2(self, epoxy):
        """
        Test the output of every ``@property`` method using valid argument - epoxy
        isotropic material
        """
        assert epoxy.name == "Epoxy"  # @property for name
        assert epoxy.youngs_modulus == Decimal("2.800")  # @property for youngs_modulus
        assert epoxy.poissons_ratio == Decimal("0.300")  # @property for poissons_ratio
        assert epoxy.shear_modulus == Decimal("1.077")  # @property for shear_modulus
        assert epoxy.pstrain_bulk_modulus == Decimal(
            "2.692"
        )  # @property for pstrain_bulk_modulus

    def test_name_setter_output(self, epoxy):
        """
        Test the output of ``@name.setter`` using valid values on epoxy isotropic
        material
        """
        epoxy.name = "EPON862"  # Alphanumericals including uppercases allowed
        assert epoxy.name == "EPON862"
        epoxy.name = "Epon_862"  # Underscore allowed
        assert epoxy.name == "Epon_862"
        epoxy.name = "Epoxy-862"  # dash allowed
        assert epoxy.name == "Epoxy-862"

    def test_name_setter_output_with_invalid_inputs(self, epoxy):
        """
        Test the output ``@name.setter`` using invalid values associated to epoxy
        isotropic material that raise ValueError
        """
        with pytest.raises(ValueError):
            epoxy.name = ""  # Missing value
        with pytest.raises(ValueError):
            epoxy.name = "fiber^&^glass"  # Non-alphanumerical not allowed
        with pytest.raises(ValueError):
            epoxy.name = "Fiber Glass"  # In-between whitespace not allowed

    def test_youngs_modulus_setter_output(self, fiberglass):
        """
        Test the output of ``@youngs_modulus.setter`` using valid values on fiberglass
        isotropic material
        """
        fiberglass.youngs_modulus = 50  #  Allowed int number
        assert fiberglass.youngs_modulus == Decimal("50.000")
        fiberglass.youngs_modulus = "50.00"  # Allowed str with digit and single dot
        assert fiberglass.youngs_modulus == Decimal("50.000")
        fiberglass.youngs_modulus = 50.0  # Allowed float number
        assert fiberglass.youngs_modulus == Decimal("50.000")
        fiberglass.youngs_modulus = Decimal("50")  # Allowed Decimal number
        assert fiberglass.youngs_modulus == Decimal("50.000")
        fiberglass.youngs_modulus = (
            2 * 25
        )  # Algebraic operation allowed as long as result greater than 0
        assert fiberglass.youngs_modulus == Decimal("50.000")

    def test_youngs_modulus_setter_output_with_invalid_inputs(self, fiberglass):
        """
        Test output of ``@youngs_modulus.setter`` with invalid values associated to
        fiberglass isotropic material that raise ValueError
        """
        with pytest.raises(ValueError):
            fiberglass.youngs_modulus = ""  # Missing value not allowed
        with pytest.raises(ValueError):
            fiberglass.youngs_modulus = "50.A4"  # Non-digit str not allowed
        with pytest.raises(ValueError):
            fiberglass.youngs_modulus = -50  # Negative value not allowed
        with pytest.raises(ValueError):
            fiberglass.youngs_modulus = "50.0.0"  # Double dot not allowed
        with pytest.raises(ValueError):
            fiberglass.youngs_modulus = 0  # Zero value not allowed

    def test_poissons_ratio_setter_output(self, epoxy):
        """
        Test output of ``@poissons_ratio.setter`` with valid values for epoxy isotropic
        material
        """
        epoxy.poissons_ratio = 0.33  # Allowed float number
        assert epoxy.poissons_ratio == Decimal("0.330")
        epoxy.poissons_ratio = (
            0.35  # Allowed float number without number before decimal
        )
        assert epoxy.poissons_ratio == Decimal("0.350")
        epoxy.poissons_ratio = "0.3"  # Allowed str digit with single dot
        assert epoxy.poissons_ratio == Decimal("0.300")
        epoxy.poissons_ratio = "0.5"  # Allowed str digit with single dot
        assert epoxy.poissons_ratio == Decimal("0.500")

    def test_poissons_ratio_setter_output_with_invalid_inputs(self, epoxy):
        """
        Test output of ``@poissons_ratio.setter`` with invalid values for epoxy
        isotropic material
        """
        with pytest.raises(ValueError):
            epoxy.poissons_ratio = ""  # Missing value not allowed
        with pytest.raises(ValueError):
            epoxy.poissons_ratio = -0.3  # Negative value not allowed
        with pytest.raises(ValueError):
            epoxy.poissons_ratio = 0.70  # Greater than 0.5 not allowed
        with pytest.raises(ValueError):
            epoxy.poissons_ratio = "0.3AS"  # Non-digit str not allowed
        with pytest.raises(ValueError):
            epoxy.poissons_ratio = "0.3.3"  # Double dot not allowed
        with pytest.raises(ValueError):
            epoxy.poissons_ratio = 0  # Zero value not allowed

    def test_shear_modulus_setter_output(self, fiberglass):
        """
        Test output of ``@shear_modulus.setter`` with valid values for fiberglass
        isotropic material
        """
        fiberglass.shear_modulus = 46.512  # Allowed number based on isotropic formula
        assert fiberglass.shear_modulus == Decimal("46.512")
        fiberglass.youngs_modulus = 100
        fiberglass.poissons_ratio = 0.25
        fiberglass.shear_modulus = (  # Allowed number based on isotropic formula
            fiberglass.youngs_modulus
            / (Decimal("2") * (Decimal("1") + fiberglass.poissons_ratio))
        ).quantize(Decimal("1.000"))
        assert fiberglass.shear_modulus == Decimal("40.000")

    def test_shear_modulus_setter_output_with_invalid_inputs(self, fiberglass):
        """
        Test output of ``@shear_modulus.setter`` with invalid values for fiberglass
        isotropic material
        """
        with pytest.raises(ValueError):
            fiberglass.shear_modulus = ""  # Missing value not allowed
        with pytest.raises(ValueError):
            fiberglass.shear_modulus = "46.S12"  # Non-digit str not allowed
        with pytest.raises(ValueError):
            fiberglass.shear_modulus = -46.512  # Negative value not allowed
        with pytest.raises(ValueError):
            fiberglass.shear_modulus = "46.5.12"  # Double dot not allowed
        with pytest.raises(ValueError):
            fiberglass.shear_modulus = 0  # Zero value not allowed
        with pytest.raises(ValueError):
            fiberglass.shear_modulus = 47  # Not as per isotropic formula
        with pytest.raises(ValueError):
            fiberglass.youngs_modulus = 100
            fiberglass.poissons_ratio = 0.25
            fiberglass.shear_modulus = (  # Not allowed based on isotropic formula
                fiberglass.youngs_modulus
                / (Decimal("2") * (Decimal("1") + fiberglass.poissons_ratio))
            ).quantize(Decimal("1.000"))
            fiberglass.shear_modulus = 20

    def test_pstrain_bulk_modulus_setter_output(self, epoxy):
        """
        Test output of ``@pstrain_bulk_modulus.setter`` with valid values for epoxy
        isotropic material
        """
        epoxy.pstrain_bulk_modulus = 2.692  # Allowed number based on isotropic formula
        assert epoxy.pstrain_bulk_modulus == Decimal("2.692")
        epoxy.youngs_modulus = 2
        epoxy.poissons_ratio = 0.33
        epoxy.pstrain_bulk_modulus = (  # Allowed number based on isotropic formula
            epoxy.youngs_modulus
            / (
                Decimal("2")
                * (Decimal("1") + epoxy.poissons_ratio)
                * (Decimal("1") - (Decimal("2") * epoxy.poissons_ratio))
            )
        ).quantize(Decimal("1.000"))
        assert epoxy.pstrain_bulk_modulus == Decimal("2.211")

    def test_pstrain_bulk_modulus_setter_output_with_invalid_inputs(self, epoxy):
        """
        Test output of ``@pstrain_bulk_modulus.setter`` with invalid values for epoxy
        isotropic material
        """
        with pytest.raises(ValueError):
            epoxy.pstrain_bulk_modulus = ""  # Missing value not allowed
        with pytest.raises(ValueError):
            epoxy.pstrain_bulk_modulus = "2.6g2"  # Non-digit str not allowed
        with pytest.raises(ValueError):
            epoxy.pstrain_bulk_modulus = -2.692  # Negative value not allowed
        with pytest.raises(ValueError):
            epoxy.pstrain_bulk_modulus = "2.6.92"  # Double dot not allowed
        with pytest.raises(ValueError):
            epoxy.pstrain_bulk_modulus = 0  # Zero value not allowed
        with pytest.raises(ValueError):
            epoxy.pstrain_bulk_modulus = 3  # Not as per isotropic formula
        with pytest.raises(ValueError):
            epoxy.youngs_modulus = 2
            epoxy.poissons_ratio = 0.33
            epoxy.pstrain_bulk_modulus = (  # Not allowed based on isotropic formula
                epoxy.youngs_modulus
                / (
                    Decimal("2")
                    * (Decimal("1") + epoxy.poissons_ratio)
                    * (Decimal("1") - (Decimal("2") * epoxy.poissons_ratio))
                )
            ).quantize(Decimal("1.000"))
            epoxy.pstrain_bulk_modulus = 3

    @pytest.mark.parametrize(  # Parametric inputs and outputs for 'get' @classmethod
        "input_values, expected",
        [
            # All correct inputs
            (
                iter(["Fiberglass", "120", ".29"]),
                Isotropic(
                    name="Fiberglass",
                    youngs_modulus=Decimal("120"),
                    poissons_ratio=Decimal("0.29"),
                ),
            ),
            # Initially incorrect name inputs and then correct, while other inputs are correct
            (
                iter(
                    [
                        "",  # Missing name
                        "Ep@xy",  # Invalid: non-alphanumerical except _ and -
                        " E poxy ",  # # Invalid: has whitespace in between
                        "  Epoxy ",  # Valid name (whitespace after/before removed - strip)
                        "2.8",  # Valid youngs_modulus
                        ".3",  # Valid poissons_ratio
                    ]
                ),
                Isotropic(
                    name="Epoxy",
                    youngs_modulus=Decimal("2.8"),
                    poissons_ratio=Decimal("0.3"),
                ),
            ),
            # Initially incorrect Young's modulus input & then correct, other inputs are correct
            (
                iter(
                    [
                        "Fiberglass",  # Correct name
                        "",  # Missing value
                        "12 0.0",  # Invalid - whitespace in between
                        "12O",  # Invalid - contain non-digit
                        "-120",  # Invalid - negative number
                        "0",  # Invalid - zero value
                        "120.0.0",  # Invalid - double dot
                        "120.0",  # Correct youngs_modulus
                        ".29",  # Correct poissons_ratio
                    ]
                ),
                Isotropic(
                    name="Fiberglass",
                    youngs_modulus=Decimal("120"),
                    poissons_ratio=Decimal("0.29"),
                ),
            ),
            # Initially incorrect Poisson's ratio & then correct while other inputs are correct
            (
                iter(
                    [
                        "Epoxy",  # Correct name
                        "2.8",  # Correct youngs_modulus
                        "",  # Missing value
                        "O.3",  # Invalid - alphabet
                        "-0.3",  # Invalid - negative value
                        "0",  # Invalid - zero valie
                        "0.51",  # Invalid - greater than 0.5
                        "0. 3",  # Invalid - whitespace in between
                        "0.3.0",  # Invalid - double dots
                        ".3",  # Correct poissons_ratio
                    ]
                ),
                Isotropic(
                    name="Epoxy",
                    youngs_modulus=Decimal("2.8"),
                    poissons_ratio=Decimal("0.3"),
                ),
            ),
        ],
    )
    def test_get_classmethod_functionality_with_user_inputs_and_validations(
        self, monkeypatch, input_values, expected
    ):
        """
        Test ``get`` ``@classmethod`` with correct and incorrect user inputs and the
        validation functionality of ensuring the correct inputs instantiating Isotropic
        object
        """
        monkeypatch.setattr("builtins.input", lambda _: next(input_values))
        result = Isotropic.get()
        assert isinstance(result, Isotropic) == True
        assert result.name == expected.name
        assert result.youngs_modulus == expected.youngs_modulus
        assert result.poissons_ratio == expected.poissons_ratio
        assert result.shear_modulus == expected.shear_modulus
        assert result.pstrain_bulk_modulus == expected.pstrain_bulk_modulus

    def test_read_classmethod_verify_csv_file(self):
        """
        Test ``read`` ``@classmethod`` on the first part of the code to verify csv file
        """
        with pytest.raises(TypeError):
            Isotropic.read("")  # File is None
        with pytest.raises(TypeError):
            Isotropic.read("testcsv")  # No file extension
        with pytest.raises(TypeError):
            Isotropic.read("test.txt")  # Not csv file
        with pytest.raises(FileNotFoundError):
            Isotropic.read(
                "test.csv"
            )  # Successfully verify CSV file but it's not present in current working directory

    @pytest.fixture
    def mock_reading_csv_file(self):
        """
        To mock a piece of code in ``read`` ``@classmethod`` opening csv file and get
        csv data for testing of data reading and instantiating Isotropic object
        """
        # create csv file that contains two isotropic materials with defined elastic moduli
        with open("isotropic.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["constituent", "Young's modulus (GPa)", "Poisson's ratio"])  # write a header first row
            writer.writerow(["Fiberglass", 120, 0.29])  # write a data in second row
            writer.writerow(["Epoxy", 2.8, 0.3])  # write a data in third row

        # Read csv file and return its data
        with open("isotropic.csv", "r") as file:  # isotropic.csv - dummy csv file
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            data = list(reader)
        return data

    def test_read_classmethod_reading_csv_file(self, mock_reading_csv_file):
        """
        Test reading csv data from csv file of ``read`` ``@classmethod``
        """
        assert mock_reading_csv_file == [
            ["Fiberglass", "120", "0.29"], ["Epoxy", "2.8", "0.3"]
        ]
        # Clean-up file
        os.remove("isotropic.csv")

    # UNIT TEST ON 'read' @classmethod
    def test_read_classmethod_using_valid_csv_file_to_instantiate_object(
        self, fiberglass, epoxy
    ):
        """
        Test instantiating object based on csv read data of ``read`` ``@classmethod``
        """
        # create csv file that contains two isotropic materials' elastic moduli
        with open("valid_isotropic.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["constituent", "Young's modulus (GPa)", "Poisson's ratio"])  # write a header first row
            writer.writerow(["Fiberglass", 120, 0.29])  # write a data in second row
            writer.writerow(["Epoxy", 2.8, 0.3])  # write a data in third row

        # instantiate two objects based on csv file using # ``read`` ``@classmethod``
        isotropic_mater = Isotropic.read("valid_isotropic.csv")

        # validating first Isotropic object
        assert isinstance(isotropic_mater[0], Isotropic) == True
        assert fiberglass.name == isotropic_mater[0].name
        assert fiberglass.youngs_modulus == isotropic_mater[0].youngs_modulus
        assert fiberglass.poissons_ratio == isotropic_mater[0].poissons_ratio
        assert fiberglass.shear_modulus == isotropic_mater[0].shear_modulus
        assert fiberglass.pstrain_bulk_modulus == isotropic_mater[0].pstrain_bulk_modulus

        # validating second Isotropic object
        assert isinstance(isotropic_mater[1], Isotropic) == True
        assert epoxy.name == isotropic_mater[1].name
        assert epoxy.youngs_modulus == isotropic_mater[1].youngs_modulus
        assert epoxy.poissons_ratio == isotropic_mater[1].poissons_ratio
        assert epoxy.shear_modulus == isotropic_mater[1].shear_modulus
        assert epoxy.pstrain_bulk_modulus == isotropic_mater[1].pstrain_bulk_modulus

        # Clean-up file
        os.remove("valid_isotropic.csv")

    def test_read_classmethod_using_invalid_content_of_csv_file(self):
        """
        Test ``read`` ``@classmethod``'s validation of invalid data inputs read from
        csv file that raise ValueError
        """
        # Case 1: create csv file that contains one isotropic materials' elastic moduli
        # with invalid name
        with open("invalid_isotropic_1.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["constituent", "Young's modulus (GPa)", "Poisson's ratio"])
            writer.writerow(["Fiber glass", 120, 0.29])  # invalid name - whitespace in between
        # validate ValueError
        with pytest.raises(ValueError):
            Isotropic.read("invalid_isotropic_1.csv")

        # Case 2: create csv file that contains one isotropic materials' elastic moduli
        # with invalid youngs_modulus
        with open("invalid_isotropic_2.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["constituent", "Young's modulus (GPa)", "Poisson's ratio"])
            writer.writerow(["Fiber glass", -120, 0.29])  # invalid Young's modulus with negative value
        # validate ValueError
        with pytest.raises(ValueError):
            Isotropic.read("invalid_isotropic_2.csv")

        # Case 3: create csv file that contains one isotropic materials' elastic moduli
        # with invalid Poisson's ratio
        with open("invalid_isotropic_3.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["constituent", "Young's modulus (GPa)", "Poisson's ratio"])
            writer.writerow(["Fiber glass", -120, 0.51])  # invalid Poisson's ratio exceed 0.5
        # validate ValueError
        with pytest.raises(ValueError):
            Isotropic.read("invalid_isotropic_3.csv")

        # Clean-up files of invalid csv
        os.remove("invalid_isotropic_1.csv")
        os.remove("invalid_isotropic_2.csv")
        os.remove("invalid_isotropic_3.csv")

    @pytest.mark.parametrize(
        "input_value, expected",
        [
            ("", False),
            ("  Fiberglass ", True),
            ("EPOXY ", True),
            ("S-Glass", True),
            ("EPON_862", True),
            ("IM7*", False),
            ("E Glass", False),
            ("@Kevlar", False),
            ("112_F50", True),
            ("#T600", False),
        ],
    )
    def test_is_valid_input_and_output(self, input_value, expected):
        """
        Test output of ``_is_valid`` ``@staticmethod`` with input and expected values
        """
        assert Isotropic._is_valid(input_value) == expected

    @pytest.mark.parametrize(
        "input_value, expected",
        [
            ("", False),
            ("  0.1 ", True),
            ("150  ", True),
            ("-200", False),
            ("0", False),
            ("-0.1", False),
            ("-0.00001", False),
            ("500.0.0", False),
            ("2000", True),
            ("2 000", False),
            ("2,000", False),
            ("-2,000", False),
        ],
    )
    def test_isvalid_constant_input_and_output(self, input_value, expected):
        """
        Test output of ``_isvalid_constant`` ``@staticmethod`` with input and expected
        values
        """
        assert Isotropic._isvalid_constant(input_value) == expected

    @pytest.mark.parametrize(
        "input_value, expected",
        [
            ("", False),
            ("  0.1  ", True),
            ("0.3  ", True),
            ("  0.25", True),
            ("0", False),
            ("-0.1", False),
            ("0.5.0", False),
            (".3", True),
            ("0.5001", False),
            ("0.2O", False),
            ("0. 275", False),
            ("0.75", False),
            ("-0.25", False),
        ],
    )
    def test_isvalid_ratio(self, input_value, expected):
        """
        Test output of ``_isvalid_ratio`` ``@staticmethod`` with input and expected
        values
        """
        assert Isotropic._isvalid_ratio(input_value) == expected

    def test_get_shear_constant_output(self):
        """
        Test output of ``_get_shear_constant`` instance method with valid values
        """
        self.youngs_modulus = Decimal("120.000")
        self.poissons_ratio = Decimal("0.290")
        assert Isotropic._get_shear_constant(self) == Decimal("46.512")
        self.youngs_modulus = Decimal("2.800")
        self.poissons_ratio = Decimal("0.300")
        assert Isotropic._get_shear_constant(self) == Decimal("1.077")

    def test_get_shear_constant_output_with_invalid_inputs(self):
        """
        Test output of ``_get_shear_constant`` instance method with invalid values that
        raises TypeError
        """
        with pytest.raises(TypeError):
            self.youngs_modulus = None
            self.poissons_ratio = 0.29
            Isotropic._get_shear_constant(self)
        with pytest.raises(TypeError):
            self.youngs_modulus = None
            self.poissons_ratio = Decimal("0.290")
            Isotropic._get_shear_constant(self)
        with pytest.raises(TypeError):
            self.youngs_modulus = "120"
            self.poissons_ratio = Decimal("0.290")
            Isotropic._get_shear_constant(self)
        with pytest.raises(TypeError):
            self.youngs_modulus = Decimal("120.000")
            self.poissons_ratio = None
            Isotropic._get_shear_constant(self)
        with pytest.raises(TypeError):
            self.youngs_modulus = Decimal("120.000")
            self.poissons_ratio = "0.29"
            Isotropic._get_shear_constant(self)

    def test_get_pstrain_bulk_modulus_output(self):
        """
        Test output of``_get_pstrain_bulk_modulus`` instance method with valid values
        """
        self.youngs_modulus = Decimal("120.000")
        self.poissons_ratio = Decimal("0.290")
        assert Isotropic._get_pstrain_bulk_modulus(self) == Decimal("110.742")
        self.youngs_modulus = Decimal("2.800")
        self.poissons_ratio = Decimal("0.300")
        assert Isotropic._get_pstrain_bulk_modulus(self) == Decimal("2.692")

    def test_get_pstrain_bulk_modulus_output_with_invalid_inputs(self):
        """
        Test output of ``_get_pstrain_bulk_modulus`` instance method with invalid values
        that raise TypeError
        """
        with pytest.raises(TypeError):
            self.youngs_modulus = None
            self.poissons_ratio = 0.29
            Isotropic._get_pstrain_bulk_modulus(self)
        with pytest.raises(TypeError):
            self.youngs_modulus = None
            self.poissons_ratio = Decimal("0.290")
            Isotropic._get_pstrain_bulk_modulus(self)
        with pytest.raises(TypeError):
            self.youngs_modulus = "120"
            self.poissons_ratio = Decimal("0.290")
            Isotropic._get_pstrain_bulk_modulus(self)
        with pytest.raises(TypeError):
            self.youngs_modulus = Decimal("120.000")
            self.poissons_ratio = None
            Isotropic._get_pstrain_bulk_modulus(self)
        with pytest.raises(TypeError):
            self.youngs_modulus = Decimal("120.000")
            self.poissons_ratio = "0.29"
            Isotropic._get_pstrain_bulk_modulus(self)


class Test_Display:
    """
    Test suite for ``display`` major function that prints out information about UD
    composite's constituent elastic moduli and composite's effective elastic moduli to
    console screen.

    This test suite contains all unit tests for every helper functions that make up the
    ``display`` function. Once all helper functions are tested, and then ``display``
    major function is unit-tested as well.
    """

    @pytest.fixture
    def fiberglass(self):
        """
        Provide argument for isotropic fiber material called fiberglass
        """
        # Isotropic class and its methods have been fully unit-tested and all passed as done above
        return Isotropic(name="Fiberglass", youngs_modulus=120, poissons_ratio=0.29)

    @pytest.fixture
    def carbon(self):
        """
        Provide arguments for transversely isotropic fiber called carbon
        """
        # Transtropic class and all its methods are assumed to have been fully unit-tested and all passed
        return Transtropic(
            name="Carbon",
            axial_youngs_modulus=250,
            transverse_youngs_modulus=25,
            axial_shear_modulus=20,
            transverse_shear_modulus=10,
            major_poissons_ratio=0.28,
        )

    @pytest.fixture
    def epoxy(self):
        """
        Provide arguments for isotropic matrix material called epoxy
        """
        return Isotropic(name="Epoxy", youngs_modulus=2.8, poissons_ratio=0.3)

    @pytest.fixture
    def graphite(self):
        """
        Provide arguments for transversely isotropic matrix material called graphite
        """
        return Transtropic(
            name="Graphite",
            axial_youngs_modulus=180,
            transverse_youngs_modulus=20,
            axial_shear_modulus=15,
            transverse_shear_modulus=10,
            major_poissons_ratio=0.29,
        )

    @pytest.fixture
    def composite1(self, carbon, epoxy):
        """
        Provide arguments for UD composite with carbon fiber as transversely isotropic
        material and epoxy matrix as isotropic material
        """
        # HT class and all its methods are assumed to have been fully unit-tested and all passed
        return HT(fiber=carbon, matrix=epoxy)

    @pytest.fixture
    def composite2(self, fiberglass, epoxy):
        """
        Provide arguments for UD composite with both fiberglass fiber and epoxy matrix
        as isotropic materials
        """
        return HT(fiber=fiberglass, matrix=epoxy)

    @pytest.fixture
    def composite3(self, carbon, graphite):
        """
        Provide arguments for UD composite with both carbon fiber and graphite matrix as
        transversely isotropic materials
        """
        return HT(fiber=carbon, matrix=graphite)

    @pytest.fixture
    def composite4(self, fiberglass, graphite):
        """
        Provide arguments for UD composite with fiberglass fiber as isotropic material
        and graphite matrix as transversely isotropic material
        """
        return HT(fiber=fiberglass, matrix=graphite)

    @pytest.fixture
    def none_arg(self):
        """
        Provide argument with None
        """
        return None

    def test_get_main_title_for_UD_composite_output(
            self, composite1, composite2, composite3, composite4
    ):
        """
        Test output of ``_get_main_title_for_UD_composite`` helper function with valid
        arguments, i.e. 4 different UD composites having different types of constituent
        materials
        """
        result1 = _get_main_title_for_UD_composite(composite1)
        assert result1 == f"\n[1] UD COMPOSITE: CARBON-EPOXY\n"
        result2 = _get_main_title_for_UD_composite(composite2)
        assert result2 == f"\n[1] UD COMPOSITE: FIBERGLASS-EPOXY\n"
        result3 = _get_main_title_for_UD_composite(composite3)
        assert result3 == f"\n[1] UD COMPOSITE: CARBON-GRAPHITE\n"
        result4 = _get_main_title_for_UD_composite(composite4)
        assert result4 == f"\n[1] UD COMPOSITE: FIBERGLASS-GRAPHITE\n"

    def test_get_main_title_for_UD_composite_output_with_invalid_inputs(
            self, fiberglass, none_arg
    ):
        """
        Test output of ``_get_main_title_for_UD_composite`` helper function with invalid
        argument that raises TypeError
        """
        with pytest.raises(TypeError):
            _get_main_title_for_UD_composite()  # no argument
        with pytest.raises(TypeError):
            _get_main_title_for_UD_composite(none_arg)  # argument is None
        with pytest.raises(TypeError):
            _get_main_title_for_UD_composite(fiberglass)  # argument is not HT object

    def test_get_sub_title_for_fiber_output(
            self, composite1, composite2, composite3, composite4
    ):
        """
        Test output of ``_get_sub_title_for_fiber`` helper function with valid
        arguments, i.e. 4 different UD composites having different types of constituent
        materials
        """
        result1 = _get_sub_title_for_fiber(composite1)
        assert result1 == f"\nA) Fiber material: Carbon\n"
        result2 = _get_sub_title_for_fiber(composite2)
        assert result2 == f"\nA) Fiber material: Fiberglass\n"
        result3 = _get_sub_title_for_fiber(composite3)
        assert result3 == f"\nA) Fiber material: Carbon\n"
        result4 = _get_sub_title_for_fiber(composite4)
        assert result4 == f"\nA) Fiber material: Fiberglass\n"

    def test_get_sub_title_for_fiber_output_with_invalid_inputs(self, carbon, none_arg):
        """
        Test output of ``_get_sub_title_for_fiber`` helper function with invalid
        argument that raises TypeError
        """
        with pytest.raises(TypeError):
            _get_sub_title_for_fiber()  # no argument
        with pytest.raises(TypeError):
            _get_sub_title_for_fiber(none_arg)  # argument is None
        with pytest.raises(TypeError):
            _get_sub_title_for_fiber(carbon)  # argument is not HT object

    def test_get_sub_title_for_matrix_output(
            self, composite1, composite2, composite3, composite4
    ):
        """
        Test output of ``_get_sub_title_for_matrix`` helper function with valid
        arguments, i.e. 4 different UD composites having different types of constituent
        materials
        """
        result1 = _get_sub_title_for_matrix(composite1)
        assert result1 == f"\nB) Matrix material: Epoxy\n"
        result2 = _get_sub_title_for_matrix(composite2)
        assert result2 == f"\nB) Matrix material: Epoxy\n"
        result3 = _get_sub_title_for_matrix(composite3)
        assert result3 == f"\nB) Matrix material: Graphite\n"
        result4 = _get_sub_title_for_matrix(composite4)
        assert result4 == f"\nB) Matrix material: Graphite\n"

    def test_get_sub_title_for_matrix_output_with_invalid_inputs(
            self, graphite, none_arg
    ):
        """
        Test ``_get_sub_title_for_matrix`` helper function with invalid argument that
        raises TypeError
        """
        with pytest.raises(TypeError):
            _get_sub_title_for_matrix()  # no argument
        with pytest.raises(TypeError):
            _get_sub_title_for_matrix(none_arg)  # argument is None
        with pytest.raises(TypeError):
            _get_sub_title_for_matrix(graphite)  # argument is not HT object

    def test_get_sub_title_for_composite_output(
            self, composite1, composite2, composite3, composite4
    ):
        """
        Test output of ``_get_sub_title_for_composite`` helper function with valid
        arguments, i.e. 4 different UD composites having different types of constituent
        materials
        """
        result1 = _get_sub_title_for_composite(composite1)
        assert result1 == f"\nC) Effective Elastic Moduli of Carbon-Epoxy\n"
        result2 = _get_sub_title_for_composite(composite2)
        assert result2 == f"\nC) Effective Elastic Moduli of Fiberglass-Epoxy\n"
        result3 = _get_sub_title_for_composite(composite3)
        assert result3 == f"\nC) Effective Elastic Moduli of Carbon-Graphite\n"
        result4 = _get_sub_title_for_composite(composite4)
        assert result4 == f"\nC) Effective Elastic Moduli of Fiberglass-Graphite\n"

    def test_get_sub_title_for_composite_output_with_invalid_inputs(
            self, fiberglass, none_arg
    ):
        """
        Test ``_get_sub_title_for_composite`` helper function with invalid arguments
        that raises TypeError
        """
        with pytest.raises(TypeError):
            _get_sub_title_for_composite()  # argument is None
        with pytest.raises(TypeError):
            _get_sub_title_for_composite(none_arg)  # argument is None
        with pytest.raises(TypeError):
            _get_sub_title_for_composite(fiberglass)  # argument is not HT object

    def test_get_fiber_and_matrix_properties_output(
            self, composite1, composite2, composite3, composite4
    ):
        """
        Test output of ``_get_fiber_and_matrix_properties`` helper function with valid
        arguments, i.e. 4 different UD composites having different types of constituent
        materials
        """
        result1 = _get_fiber_and_matrix_properties(composite1)
        assert result1 == [
            [
                [
                    "Constituent",
                    "Axial\nYoung's\nModulus,\nE1 (GPa)",
                    "Transverse\nYoung's\nModulus,\nE2 (GPa)",
                    "Axial\nShear\nModulus,\nG12 (GPa)",
                    "Transverse\nShear\nModulus,\nG23 (GPa)",
                    "Major\nPoisson's\nRatio,\nv12",
                    "Plane-strain\nBulk\nModulus,\nK23 (GPa)",
                ],
                [
                    "Carbon",
                    Decimal("250.000"),
                    Decimal("25.000"),
                    Decimal("20.000"),
                    Decimal("10.000"),
                    Decimal("0.280"),
                    Decimal("17.023"),
                ],
            ],
            [
                [
                    "Constituent",
                    "Young's\nModulus,\nE (GPa)",
                    "Poisson's\nRatio,\nv",
                    "Shear\nModulus,\nG (GPa)",
                    "Plane-strain\nBulk Modulus,\nK (GPa)",
                ],
                [
                    "Epoxy",
                    Decimal("2.800"),
                    Decimal("0.300"),
                    Decimal("1.077"),
                    Decimal("2.692"),
                ],
            ],
        ]
        result2 = _get_fiber_and_matrix_properties(composite2)
        assert result2 == [
            [
                [
                    "Constituent",
                    "Young's\nModulus,\nE (GPa)",
                    "Poisson's\nRatio,\nv",
                    "Shear\nModulus,\nG (GPa)",
                    "Plane-strain\nBulk Modulus,\nK (GPa)",
                ],
                [
                    "Fiberglass",
                    Decimal("120.000"),
                    Decimal("0.290"),
                    Decimal("46.512"),
                    Decimal("110.742"),
                ],
            ],
            [
                [
                    "Constituent",
                    "Young's\nModulus,\nE (GPa)",
                    "Poisson's\nRatio,\nv",
                    "Shear\nModulus,\nG (GPa)",
                    "Plane-strain\nBulk Modulus,\nK (GPa)",
                ],
                [
                    "Epoxy",
                    Decimal("2.800"),
                    Decimal("0.300"),
                    Decimal("1.077"),
                    Decimal("2.692"),
                ],
            ],
        ]
        result3 = _get_fiber_and_matrix_properties(composite3)
        assert result3 == [
            [
                [
                    "Constituent",
                    "Axial\nYoung's\nModulus,\nE1 (GPa)",
                    "Transverse\nYoung's\nModulus,\nE2 (GPa)",
                    "Axial\nShear\nModulus,\nG12 (GPa)",
                    "Transverse\nShear\nModulus,\nG23 (GPa)",
                    "Major\nPoisson's\nRatio,\nv12",
                    "Plane-strain\nBulk\nModulus,\nK23 (GPa)",
                ],
                [
                    "Carbon",
                    Decimal("250.000"),
                    Decimal("25.000"),
                    Decimal("20.000"),
                    Decimal("10.000"),
                    Decimal("0.280"),
                    Decimal("17.023"),
                ],
            ],
            [
                [
                    "Constituent",
                    "Axial\nYoung's\nModulus,\nE1 (GPa)",
                    "Transverse\nYoung's\nModulus,\nE2 (GPa)",
                    "Axial\nShear\nModulus,\nG12 (GPa)",
                    "Transverse\nShear\nModulus,\nG23 (GPa)",
                    "Major\nPoisson's\nRatio,\nv12",
                    "Plane-strain\nBulk\nModulus,\nK23 (GPa)",
                ],
                [
                    "Graphite",
                    Decimal("180.000"),
                    Decimal("20.000"),
                    Decimal("15.000"),
                    Decimal("10.000"),
                    Decimal("0.290"),
                    Decimal("10.190"),
                ],
            ],
        ]
        result4 = _get_fiber_and_matrix_properties(composite4)
        assert result4 == [
            [
                [
                    "Constituent",
                    "Young's\nModulus,\nE (GPa)",
                    "Poisson's\nRatio,\nv",
                    "Shear\nModulus,\nG (GPa)",
                    "Plane-strain\nBulk Modulus,\nK (GPa)",
                ],
                [
                    "Fiberglass",
                    Decimal("120.000"),
                    Decimal("0.290"),
                    Decimal("46.512"),
                    Decimal("110.742"),
                ],
            ],
            [
                [
                    "Constituent",
                    "Axial\nYoung's\nModulus,\nE1 (GPa)",
                    "Transverse\nYoung's\nModulus,\nE2 (GPa)",
                    "Axial\nShear\nModulus,\nG12 (GPa)",
                    "Transverse\nShear\nModulus,\nG23 (GPa)",
                    "Major\nPoisson's\nRatio,\nv12",
                    "Plane-strain\nBulk\nModulus,\nK23 (GPa)",
                ],
                [
                    "Graphite",
                    Decimal("180.000"),
                    Decimal("20.000"),
                    Decimal("15.000"),
                    Decimal("10.000"),
                    Decimal("0.290"),
                    Decimal("10.190"),
                ],
            ],
        ]

    def test_get_fiber_and_matrix_properties_output_with_invalid_inputs(
            self, carbon, none_arg
    ):
        """
        Test output of ``_get_fiber_and_matrix_properties`` helper function with invalid
        arguments that raise TypeError
        """
        with pytest.raises(TypeError):
            _get_fiber_and_matrix_properties()  # no argument
        with pytest.raises(TypeError):
            _get_fiber_and_matrix_properties(none_arg)  # argument is None
        with pytest.raises(TypeError):
            _get_fiber_and_matrix_properties(carbon)  # argument is not HT object

    def test_get_effective_properties_versus_full_range_Vf_output(
            self, composite1, composite2, composite3, composite4
    ):
        """
        Test output of ``_get_effective_properties_versus_full_range_Vf`` helper
        function with valid arguments, i.e. 4 different UD composites having different
        types of constituent materials
        """
        result1 = _get_effective_properties_versus_full_range_Vf(composite1)
        assert result1 == {
            "Vf": (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            "E1*\n(GPa)": (
                Decimal("2.800"),
                Decimal("5.272"),
                Decimal("7.744"),
                Decimal("10.216"),
                Decimal("12.688"),
                Decimal("15.160"),
                Decimal("17.632"),
                Decimal("20.104"),
                Decimal("22.576"),
                Decimal("25.048"),
                Decimal("27.520"),
                Decimal("29.992"),
                Decimal("32.464"),
                Decimal("34.936"),
                Decimal("37.408"),
                Decimal("39.880"),
                Decimal("42.352"),
                Decimal("44.824"),
                Decimal("47.296"),
                Decimal("49.768"),
                Decimal("52.240"),
                Decimal("54.712"),
                Decimal("57.184"),
                Decimal("59.656"),
                Decimal("62.128"),
                Decimal("64.600"),
                Decimal("67.072"),
                Decimal("69.544"),
                Decimal("72.016"),
                Decimal("74.488"),
                Decimal("76.960"),
                Decimal("79.432"),
                Decimal("81.904"),
                Decimal("84.376"),
                Decimal("86.848"),
                Decimal("89.320"),
                Decimal("91.792"),
                Decimal("94.264"),
                Decimal("96.736"),
                Decimal("99.208"),
                Decimal("101.680"),
                Decimal("104.152"),
                Decimal("106.624"),
                Decimal("109.096"),
                Decimal("111.568"),
                Decimal("114.040"),
                Decimal("116.512"),
                Decimal("118.984"),
                Decimal("121.456"),
                Decimal("123.928"),
                Decimal("126.400"),
                Decimal("128.872"),
                Decimal("131.344"),
                Decimal("133.816"),
                Decimal("136.288"),
                Decimal("138.760"),
                Decimal("141.232"),
                Decimal("143.704"),
                Decimal("146.176"),
                Decimal("148.648"),
                Decimal("151.120"),
                Decimal("153.592"),
                Decimal("156.064"),
                Decimal("158.536"),
                Decimal("161.008"),
                Decimal("163.480"),
                Decimal("165.952"),
                Decimal("168.424"),
                Decimal("170.896"),
                Decimal("173.368"),
                Decimal("175.840"),
                Decimal("178.312"),
                Decimal("180.784"),
                Decimal("183.256"),
                Decimal("185.728"),
                Decimal("188.200"),
                Decimal("190.672"),
                Decimal("193.144"),
                Decimal("195.616"),
                Decimal("198.088"),
                Decimal("200.560"),
                Decimal("203.032"),
                Decimal("205.504"),
                Decimal("207.976"),
                Decimal("210.448"),
                Decimal("212.920"),
                Decimal("215.392"),
                Decimal("217.864"),
                Decimal("220.336"),
                Decimal("222.808"),
                Decimal("225.280"),
                Decimal("227.752"),
                Decimal("230.224"),
                Decimal("232.696"),
                Decimal("235.168"),
                Decimal("237.640"),
                Decimal("240.112"),
                Decimal("242.584"),
                Decimal("245.056"),
                Decimal("247.528"),
                Decimal("250.000"),
            ),
            "E2*\n(GPa)": (
                Decimal("2.800"),
                Decimal("2.958"),
                Decimal("3.045"),
                Decimal("3.108"),
                Decimal("3.163"),
                Decimal("3.216"),
                Decimal("3.265"),
                Decimal("3.314"),
                Decimal("3.362"),
                Decimal("3.409"),
                Decimal("3.458"),
                Decimal("3.506"),
                Decimal("3.555"),
                Decimal("3.605"),
                Decimal("3.655"),
                Decimal("3.705"),
                Decimal("3.758"),
                Decimal("3.810"),
                Decimal("3.863"),
                Decimal("3.917"),
                Decimal("3.972"),
                Decimal("4.030"),
                Decimal("4.087"),
                Decimal("4.144"),
                Decimal("4.204"),
                Decimal("4.266"),
                Decimal("4.326"),
                Decimal("4.391"),
                Decimal("4.456"),
                Decimal("4.521"),
                Decimal("4.588"),
                Decimal("4.658"),
                Decimal("4.728"),
                Decimal("4.800"),
                Decimal("4.873"),
                Decimal("4.949"),
                Decimal("5.026"),
                Decimal("5.104"),
                Decimal("5.184"),
                Decimal("5.267"),
                Decimal("5.353"),
                Decimal("5.438"),
                Decimal("5.527"),
                Decimal("5.619"),
                Decimal("5.712"),
                Decimal("5.808"),
                Decimal("5.907"),
                Decimal("6.008"),
                Decimal("6.111"),
                Decimal("6.217"),
                Decimal("6.328"),
                Decimal("6.441"),
                Decimal("6.558"),
                Decimal("6.676"),
                Decimal("6.800"),
                Decimal("6.926"),
                Decimal("7.055"),
                Decimal("7.191"),
                Decimal("7.331"),
                Decimal("7.474"),
                Decimal("7.621"),
                Decimal("7.775"),
                Decimal("7.932"),
                Decimal("8.095"),
                Decimal("8.265"),
                Decimal("8.441"),
                Decimal("8.622"),
                Decimal("8.811"),
                Decimal("9.007"),
                Decimal("9.208"),
                Decimal("9.419"),
                Decimal("9.639"),
                Decimal("9.868"),
                Decimal("10.105"),
                Decimal("10.353"),
                Decimal("10.610"),
                Decimal("10.881"),
                Decimal("11.163"),
                Decimal("11.458"),
                Decimal("11.766"),
                Decimal("12.090"),
                Decimal("12.430"),
                Decimal("12.789"),
                Decimal("13.165"),
                Decimal("13.562"),
                Decimal("13.979"),
                Decimal("14.422"),
                Decimal("14.890"),
                Decimal("15.386"),
                Decimal("15.914"),
                Decimal("16.475"),
                Decimal("17.073"),
                Decimal("17.711"),
                Decimal("18.397"),
                Decimal("19.131"),
                Decimal("19.923"),
                Decimal("20.778"),
                Decimal("21.702"),
                Decimal("22.707"),
                Decimal("23.801"),
                Decimal("25.000"),
            ),
            "G12*\n(GPa)": (
                Decimal("1.077"),
                Decimal("1.097"),
                Decimal("1.116"),
                Decimal("1.137"),
                Decimal("1.157"),
                Decimal("1.178"),
                Decimal("1.200"),
                Decimal("1.221"),
                Decimal("1.244"),
                Decimal("1.266"),
                Decimal("1.289"),
                Decimal("1.313"),
                Decimal("1.337"),
                Decimal("1.362"),
                Decimal("1.387"),
                Decimal("1.412"),
                Decimal("1.438"),
                Decimal("1.465"),
                Decimal("1.492"),
                Decimal("1.520"),
                Decimal("1.548"),
                Decimal("1.577"),
                Decimal("1.607"),
                Decimal("1.638"),
                Decimal("1.669"),
                Decimal("1.700"),
                Decimal("1.733"),
                Decimal("1.766"),
                Decimal("1.800"),
                Decimal("1.835"),
                Decimal("1.871"),
                Decimal("1.908"),
                Decimal("1.945"),
                Decimal("1.984"),
                Decimal("2.023"),
                Decimal("2.064"),
                Decimal("2.106"),
                Decimal("2.148"),
                Decimal("2.192"),
                Decimal("2.238"),
                Decimal("2.284"),
                Decimal("2.332"),
                Decimal("2.381"),
                Decimal("2.431"),
                Decimal("2.484"),
                Decimal("2.537"),
                Decimal("2.592"),
                Decimal("2.649"),
                Decimal("2.708"),
                Decimal("2.769"),
                Decimal("2.832"),
                Decimal("2.896"),
                Decimal("2.963"),
                Decimal("3.032"),
                Decimal("3.104"),
                Decimal("3.178"),
                Decimal("3.255"),
                Decimal("3.335"),
                Decimal("3.417"),
                Decimal("3.503"),
                Decimal("3.592"),
                Decimal("3.685"),
                Decimal("3.781"),
                Decimal("3.882"),
                Decimal("3.986"),
                Decimal("4.096"),
                Decimal("4.210"),
                Decimal("4.329"),
                Decimal("4.453"),
                Decimal("4.584"),
                Decimal("4.721"),
                Decimal("4.864"),
                Decimal("5.015"),
                Decimal("5.174"),
                Decimal("5.341"),
                Decimal("5.517"),
                Decimal("5.704"),
                Decimal("5.901"),
                Decimal("6.110"),
                Decimal("6.332"),
                Decimal("6.568"),
                Decimal("6.819"),
                Decimal("7.088"),
                Decimal("7.376"),
                Decimal("7.685"),
                Decimal("8.017"),
                Decimal("8.375"),
                Decimal("8.763"),
                Decimal("9.183"),
                Decimal("9.642"),
                Decimal("10.143"),
                Decimal("10.694"),
                Decimal("11.301"),
                Decimal("11.974"),
                Decimal("12.725"),
                Decimal("13.567"),
                Decimal("14.519"),
                Decimal("15.604"),
                Decimal("16.850"),
                Decimal("18.298"),
                Decimal("20.000"),
            ),
            "v12*": (
                Decimal("0.3000"),
                Decimal("0.2998"),
                Decimal("0.2996"),
                Decimal("0.2994"),
                Decimal("0.2992"),
                Decimal("0.2990"),
                Decimal("0.2988"),
                Decimal("0.2986"),
                Decimal("0.2984"),
                Decimal("0.2982"),
                Decimal("0.2980"),
                Decimal("0.2978"),
                Decimal("0.2976"),
                Decimal("0.2974"),
                Decimal("0.2972"),
                Decimal("0.2970"),
                Decimal("0.2968"),
                Decimal("0.2966"),
                Decimal("0.2964"),
                Decimal("0.2962"),
                Decimal("0.2960"),
                Decimal("0.2958"),
                Decimal("0.2956"),
                Decimal("0.2954"),
                Decimal("0.2952"),
                Decimal("0.2950"),
                Decimal("0.2948"),
                Decimal("0.2946"),
                Decimal("0.2944"),
                Decimal("0.2942"),
                Decimal("0.2940"),
                Decimal("0.2938"),
                Decimal("0.2936"),
                Decimal("0.2934"),
                Decimal("0.2932"),
                Decimal("0.2930"),
                Decimal("0.2928"),
                Decimal("0.2926"),
                Decimal("0.2924"),
                Decimal("0.2922"),
                Decimal("0.2920"),
                Decimal("0.2918"),
                Decimal("0.2916"),
                Decimal("0.2914"),
                Decimal("0.2912"),
                Decimal("0.2910"),
                Decimal("0.2908"),
                Decimal("0.2906"),
                Decimal("0.2904"),
                Decimal("0.2902"),
                Decimal("0.2900"),
                Decimal("0.2898"),
                Decimal("0.2896"),
                Decimal("0.2894"),
                Decimal("0.2892"),
                Decimal("0.2890"),
                Decimal("0.2888"),
                Decimal("0.2886"),
                Decimal("0.2884"),
                Decimal("0.2882"),
                Decimal("0.2880"),
                Decimal("0.2878"),
                Decimal("0.2876"),
                Decimal("0.2874"),
                Decimal("0.2872"),
                Decimal("0.2870"),
                Decimal("0.2868"),
                Decimal("0.2866"),
                Decimal("0.2864"),
                Decimal("0.2862"),
                Decimal("0.2860"),
                Decimal("0.2858"),
                Decimal("0.2856"),
                Decimal("0.2854"),
                Decimal("0.2852"),
                Decimal("0.2850"),
                Decimal("0.2848"),
                Decimal("0.2846"),
                Decimal("0.2844"),
                Decimal("0.2842"),
                Decimal("0.2840"),
                Decimal("0.2838"),
                Decimal("0.2836"),
                Decimal("0.2834"),
                Decimal("0.2832"),
                Decimal("0.2830"),
                Decimal("0.2828"),
                Decimal("0.2826"),
                Decimal("0.2824"),
                Decimal("0.2822"),
                Decimal("0.2820"),
                Decimal("0.2818"),
                Decimal("0.2816"),
                Decimal("0.2814"),
                Decimal("0.2812"),
                Decimal("0.2810"),
                Decimal("0.2808"),
                Decimal("0.2806"),
                Decimal("0.2804"),
                Decimal("0.2802"),
                Decimal("0.2800"),
            ),
            "G23*\n(GPa)": (
                Decimal("1.077"),
                Decimal("1.091"),
                Decimal("1.106"),
                Decimal("1.120"),
                Decimal("1.135"),
                Decimal("1.151"),
                Decimal("1.166"),
                Decimal("1.182"),
                Decimal("1.198"),
                Decimal("1.214"),
                Decimal("1.231"),
                Decimal("1.248"),
                Decimal("1.265"),
                Decimal("1.283"),
                Decimal("1.301"),
                Decimal("1.319"),
                Decimal("1.338"),
                Decimal("1.357"),
                Decimal("1.376"),
                Decimal("1.396"),
                Decimal("1.416"),
                Decimal("1.437"),
                Decimal("1.458"),
                Decimal("1.479"),
                Decimal("1.501"),
                Decimal("1.524"),
                Decimal("1.546"),
                Decimal("1.570"),
                Decimal("1.594"),
                Decimal("1.618"),
                Decimal("1.643"),
                Decimal("1.669"),
                Decimal("1.695"),
                Decimal("1.722"),
                Decimal("1.749"),
                Decimal("1.777"),
                Decimal("1.806"),
                Decimal("1.835"),
                Decimal("1.865"),
                Decimal("1.896"),
                Decimal("1.928"),
                Decimal("1.960"),
                Decimal("1.993"),
                Decimal("2.028"),
                Decimal("2.063"),
                Decimal("2.099"),
                Decimal("2.136"),
                Decimal("2.174"),
                Decimal("2.213"),
                Decimal("2.253"),
                Decimal("2.295"),
                Decimal("2.338"),
                Decimal("2.382"),
                Decimal("2.427"),
                Decimal("2.474"),
                Decimal("2.522"),
                Decimal("2.571"),
                Decimal("2.623"),
                Decimal("2.676"),
                Decimal("2.731"),
                Decimal("2.787"),
                Decimal("2.846"),
                Decimal("2.906"),
                Decimal("2.969"),
                Decimal("3.034"),
                Decimal("3.102"),
                Decimal("3.172"),
                Decimal("3.245"),
                Decimal("3.321"),
                Decimal("3.399"),
                Decimal("3.481"),
                Decimal("3.567"),
                Decimal("3.656"),
                Decimal("3.749"),
                Decimal("3.846"),
                Decimal("3.947"),
                Decimal("4.054"),
                Decimal("4.165"),
                Decimal("4.282"),
                Decimal("4.404"),
                Decimal("4.533"),
                Decimal("4.669"),
                Decimal("4.813"),
                Decimal("4.964"),
                Decimal("5.124"),
                Decimal("5.293"),
                Decimal("5.473"),
                Decimal("5.664"),
                Decimal("5.867"),
                Decimal("6.085"),
                Decimal("6.317"),
                Decimal("6.566"),
                Decimal("6.833"),
                Decimal("7.122"),
                Decimal("7.433"),
                Decimal("7.771"),
                Decimal("8.139"),
                Decimal("8.540"),
                Decimal("8.980"),
                Decimal("9.464"),
                Decimal("10.000"),
            ),
            "K23*\n(GPa)": (
                Decimal("2.692"),
                Decimal("2.722"),
                Decimal("2.753"),
                Decimal("2.784"),
                Decimal("2.815"),
                Decimal("2.847"),
                Decimal("2.880"),
                Decimal("2.913"),
                Decimal("2.947"),
                Decimal("2.981"),
                Decimal("3.016"),
                Decimal("3.052"),
                Decimal("3.088"),
                Decimal("3.124"),
                Decimal("3.162"),
                Decimal("3.200"),
                Decimal("3.239"),
                Decimal("3.278"),
                Decimal("3.318"),
                Decimal("3.359"),
                Decimal("3.401"),
                Decimal("3.444"),
                Decimal("3.487"),
                Decimal("3.531"),
                Decimal("3.576"),
                Decimal("3.622"),
                Decimal("3.669"),
                Decimal("3.717"),
                Decimal("3.766"),
                Decimal("3.815"),
                Decimal("3.866"),
                Decimal("3.918"),
                Decimal("3.971"),
                Decimal("4.025"),
                Decimal("4.080"),
                Decimal("4.137"),
                Decimal("4.195"),
                Decimal("4.254"),
                Decimal("4.314"),
                Decimal("4.376"),
                Decimal("4.439"),
                Decimal("4.504"),
                Decimal("4.570"),
                Decimal("4.638"),
                Decimal("4.707"),
                Decimal("4.778"),
                Decimal("4.851"),
                Decimal("4.926"),
                Decimal("5.003"),
                Decimal("5.081"),
                Decimal("5.162"),
                Decimal("5.245"),
                Decimal("5.330"),
                Decimal("5.417"),
                Decimal("5.507"),
                Decimal("5.599"),
                Decimal("5.694"),
                Decimal("5.792"),
                Decimal("5.893"),
                Decimal("5.996"),
                Decimal("6.103"),
                Decimal("6.213"),
                Decimal("6.326"),
                Decimal("6.443"),
                Decimal("6.564"),
                Decimal("6.689"),
                Decimal("6.817"),
                Decimal("6.950"),
                Decimal("7.088"),
                Decimal("7.231"),
                Decimal("7.378"),
                Decimal("7.531"),
                Decimal("7.690"),
                Decimal("7.854"),
                Decimal("8.025"),
                Decimal("8.202"),
                Decimal("8.387"),
                Decimal("8.579"),
                Decimal("8.779"),
                Decimal("8.987"),
                Decimal("9.204"),
                Decimal("9.431"),
                Decimal("9.669"),
                Decimal("9.917"),
                Decimal("10.177"),
                Decimal("10.449"),
                Decimal("10.735"),
                Decimal("11.036"),
                Decimal("11.352"),
                Decimal("11.685"),
                Decimal("12.037"),
                Decimal("12.408"),
                Decimal("12.801"),
                Decimal("13.218"),
                Decimal("13.661"),
                Decimal("14.132"),
                Decimal("14.634"),
                Decimal("15.170"),
                Decimal("15.744"),
                Decimal("16.360"),
                Decimal("17.023"),
            ),
        }
        result2 = _get_effective_properties_versus_full_range_Vf(composite2)
        assert result2 == {
            "Vf": (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            "E1*\n(GPa)": (
                Decimal("2.800"),
                Decimal("3.972"),
                Decimal("5.144"),
                Decimal("6.316"),
                Decimal("7.488"),
                Decimal("8.660"),
                Decimal("9.832"),
                Decimal("11.004"),
                Decimal("12.176"),
                Decimal("13.348"),
                Decimal("14.520"),
                Decimal("15.692"),
                Decimal("16.864"),
                Decimal("18.036"),
                Decimal("19.208"),
                Decimal("20.380"),
                Decimal("21.552"),
                Decimal("22.724"),
                Decimal("23.896"),
                Decimal("25.068"),
                Decimal("26.240"),
                Decimal("27.412"),
                Decimal("28.584"),
                Decimal("29.756"),
                Decimal("30.928"),
                Decimal("32.100"),
                Decimal("33.272"),
                Decimal("34.444"),
                Decimal("35.616"),
                Decimal("36.788"),
                Decimal("37.960"),
                Decimal("39.132"),
                Decimal("40.304"),
                Decimal("41.476"),
                Decimal("42.648"),
                Decimal("43.820"),
                Decimal("44.992"),
                Decimal("46.164"),
                Decimal("47.336"),
                Decimal("48.508"),
                Decimal("49.680"),
                Decimal("50.852"),
                Decimal("52.024"),
                Decimal("53.196"),
                Decimal("54.368"),
                Decimal("55.540"),
                Decimal("56.712"),
                Decimal("57.884"),
                Decimal("59.056"),
                Decimal("60.228"),
                Decimal("61.400"),
                Decimal("62.572"),
                Decimal("63.744"),
                Decimal("64.916"),
                Decimal("66.088"),
                Decimal("67.260"),
                Decimal("68.432"),
                Decimal("69.604"),
                Decimal("70.776"),
                Decimal("71.948"),
                Decimal("73.120"),
                Decimal("74.292"),
                Decimal("75.464"),
                Decimal("76.636"),
                Decimal("77.808"),
                Decimal("78.980"),
                Decimal("80.152"),
                Decimal("81.324"),
                Decimal("82.496"),
                Decimal("83.668"),
                Decimal("84.840"),
                Decimal("86.012"),
                Decimal("87.184"),
                Decimal("88.356"),
                Decimal("89.528"),
                Decimal("90.700"),
                Decimal("91.872"),
                Decimal("93.044"),
                Decimal("94.216"),
                Decimal("95.388"),
                Decimal("96.560"),
                Decimal("97.732"),
                Decimal("98.904"),
                Decimal("100.076"),
                Decimal("101.248"),
                Decimal("102.420"),
                Decimal("103.592"),
                Decimal("104.764"),
                Decimal("105.936"),
                Decimal("107.108"),
                Decimal("108.280"),
                Decimal("109.452"),
                Decimal("110.624"),
                Decimal("111.796"),
                Decimal("112.968"),
                Decimal("114.140"),
                Decimal("115.312"),
                Decimal("116.484"),
                Decimal("117.656"),
                Decimal("118.828"),
                Decimal("120.000"),
            ),
            "E2*\n(GPa)": (
                Decimal("2.800"),
                Decimal("2.916"),
                Decimal("3.002"),
                Decimal("3.075"),
                Decimal("3.140"),
                Decimal("3.203"),
                Decimal("3.263"),
                Decimal("3.321"),
                Decimal("3.380"),
                Decimal("3.438"),
                Decimal("3.497"),
                Decimal("3.556"),
                Decimal("3.614"),
                Decimal("3.675"),
                Decimal("3.738"),
                Decimal("3.799"),
                Decimal("3.863"),
                Decimal("3.929"),
                Decimal("3.994"),
                Decimal("4.061"),
                Decimal("4.129"),
                Decimal("4.199"),
                Decimal("4.272"),
                Decimal("4.346"),
                Decimal("4.422"),
                Decimal("4.497"),
                Decimal("4.577"),
                Decimal("4.658"),
                Decimal("4.741"),
                Decimal("4.825"),
                Decimal("4.913"),
                Decimal("5.002"),
                Decimal("5.095"),
                Decimal("5.190"),
                Decimal("5.286"),
                Decimal("5.388"),
                Decimal("5.490"),
                Decimal("5.595"),
                Decimal("5.705"),
                Decimal("5.818"),
                Decimal("5.934"),
                Decimal("6.054"),
                Decimal("6.178"),
                Decimal("6.305"),
                Decimal("6.437"),
                Decimal("6.574"),
                Decimal("6.714"),
                Decimal("6.860"),
                Decimal("7.010"),
                Decimal("7.167"),
                Decimal("7.329"),
                Decimal("7.498"),
                Decimal("7.672"),
                Decimal("7.855"),
                Decimal("8.044"),
                Decimal("8.241"),
                Decimal("8.444"),
                Decimal("8.657"),
                Decimal("8.882"),
                Decimal("9.114"),
                Decimal("9.357"),
                Decimal("9.612"),
                Decimal("9.879"),
                Decimal("10.158"),
                Decimal("10.453"),
                Decimal("10.761"),
                Decimal("11.086"),
                Decimal("11.427"),
                Decimal("11.790"),
                Decimal("12.171"),
                Decimal("12.577"),
                Decimal("13.007"),
                Decimal("13.463"),
                Decimal("13.948"),
                Decimal("14.467"),
                Decimal("15.021"),
                Decimal("15.615"),
                Decimal("16.252"),
                Decimal("16.938"),
                Decimal("17.680"),
                Decimal("18.484"),
                Decimal("19.357"),
                Decimal("20.310"),
                Decimal("21.354"),
                Decimal("22.504"),
                Decimal("23.774"),
                Decimal("25.186"),
                Decimal("26.764"),
                Decimal("28.541"),
                Decimal("30.555"),
                Decimal("32.857"),
                Decimal("35.514"),
                Decimal("38.618"),
                Decimal("42.287"),
                Decimal("46.694"),
                Decimal("52.086"),
                Decimal("58.834"),
                Decimal("67.525"),
                Decimal("79.138"),
                Decimal("95.441"),
                Decimal("120.001"),
            ),
            "G12*\n(GPa)": (
                Decimal("1.077"),
                Decimal("1.098"),
                Decimal("1.119"),
                Decimal("1.141"),
                Decimal("1.163"),
                Decimal("1.185"),
                Decimal("1.208"),
                Decimal("1.231"),
                Decimal("1.255"),
                Decimal("1.279"),
                Decimal("1.304"),
                Decimal("1.330"),
                Decimal("1.356"),
                Decimal("1.382"),
                Decimal("1.409"),
                Decimal("1.437"),
                Decimal("1.465"),
                Decimal("1.494"),
                Decimal("1.524"),
                Decimal("1.554"),
                Decimal("1.585"),
                Decimal("1.617"),
                Decimal("1.650"),
                Decimal("1.683"),
                Decimal("1.717"),
                Decimal("1.752"),
                Decimal("1.788"),
                Decimal("1.825"),
                Decimal("1.863"),
                Decimal("1.902"),
                Decimal("1.942"),
                Decimal("1.983"),
                Decimal("2.025"),
                Decimal("2.068"),
                Decimal("2.112"),
                Decimal("2.158"),
                Decimal("2.205"),
                Decimal("2.254"),
                Decimal("2.303"),
                Decimal("2.355"),
                Decimal("2.408"),
                Decimal("2.463"),
                Decimal("2.519"),
                Decimal("2.577"),
                Decimal("2.637"),
                Decimal("2.700"),
                Decimal("2.764"),
                Decimal("2.830"),
                Decimal("2.899"),
                Decimal("2.971"),
                Decimal("3.044"),
                Decimal("3.121"),
                Decimal("3.201"),
                Decimal("3.283"),
                Decimal("3.369"),
                Decimal("3.459"),
                Decimal("3.552"),
                Decimal("3.649"),
                Decimal("3.750"),
                Decimal("3.855"),
                Decimal("3.966"),
                Decimal("4.081"),
                Decimal("4.202"),
                Decimal("4.328"),
                Decimal("4.461"),
                Decimal("4.600"),
                Decimal("4.747"),
                Decimal("4.901"),
                Decimal("5.064"),
                Decimal("5.235"),
                Decimal("5.417"),
                Decimal("5.610"),
                Decimal("5.814"),
                Decimal("6.031"),
                Decimal("6.262"),
                Decimal("6.509"),
                Decimal("6.773"),
                Decimal("7.056"),
                Decimal("7.360"),
                Decimal("7.688"),
                Decimal("8.042"),
                Decimal("8.426"),
                Decimal("8.844"),
                Decimal("9.300"),
                Decimal("9.801"),
                Decimal("10.352"),
                Decimal("10.962"),
                Decimal("11.640"),
                Decimal("12.400"),
                Decimal("13.256"),
                Decimal("14.228"),
                Decimal("15.342"),
                Decimal("16.631"),
                Decimal("18.139"),
                Decimal("19.928"),
                Decimal("22.084"),
                Decimal("24.734"),
                Decimal("28.069"),
                Decimal("32.392"),
                Decimal("38.222"),
                Decimal("46.512"),
            ),
            "v12*": (
                Decimal("0.3000"),
                Decimal("0.2999"),
                Decimal("0.2998"),
                Decimal("0.2997"),
                Decimal("0.2996"),
                Decimal("0.2995"),
                Decimal("0.2994"),
                Decimal("0.2993"),
                Decimal("0.2992"),
                Decimal("0.2991"),
                Decimal("0.2990"),
                Decimal("0.2989"),
                Decimal("0.2988"),
                Decimal("0.2987"),
                Decimal("0.2986"),
                Decimal("0.2985"),
                Decimal("0.2984"),
                Decimal("0.2983"),
                Decimal("0.2982"),
                Decimal("0.2981"),
                Decimal("0.2980"),
                Decimal("0.2979"),
                Decimal("0.2978"),
                Decimal("0.2977"),
                Decimal("0.2976"),
                Decimal("0.2975"),
                Decimal("0.2974"),
                Decimal("0.2973"),
                Decimal("0.2972"),
                Decimal("0.2971"),
                Decimal("0.2970"),
                Decimal("0.2969"),
                Decimal("0.2968"),
                Decimal("0.2967"),
                Decimal("0.2966"),
                Decimal("0.2965"),
                Decimal("0.2964"),
                Decimal("0.2963"),
                Decimal("0.2962"),
                Decimal("0.2961"),
                Decimal("0.2960"),
                Decimal("0.2959"),
                Decimal("0.2958"),
                Decimal("0.2957"),
                Decimal("0.2956"),
                Decimal("0.2955"),
                Decimal("0.2954"),
                Decimal("0.2953"),
                Decimal("0.2952"),
                Decimal("0.2951"),
                Decimal("0.2950"),
                Decimal("0.2949"),
                Decimal("0.2948"),
                Decimal("0.2947"),
                Decimal("0.2946"),
                Decimal("0.2945"),
                Decimal("0.2944"),
                Decimal("0.2943"),
                Decimal("0.2942"),
                Decimal("0.2941"),
                Decimal("0.2940"),
                Decimal("0.2939"),
                Decimal("0.2938"),
                Decimal("0.2937"),
                Decimal("0.2936"),
                Decimal("0.2935"),
                Decimal("0.2934"),
                Decimal("0.2933"),
                Decimal("0.2932"),
                Decimal("0.2931"),
                Decimal("0.2930"),
                Decimal("0.2929"),
                Decimal("0.2928"),
                Decimal("0.2927"),
                Decimal("0.2926"),
                Decimal("0.2925"),
                Decimal("0.2924"),
                Decimal("0.2923"),
                Decimal("0.2922"),
                Decimal("0.2921"),
                Decimal("0.2920"),
                Decimal("0.2919"),
                Decimal("0.2918"),
                Decimal("0.2917"),
                Decimal("0.2916"),
                Decimal("0.2915"),
                Decimal("0.2914"),
                Decimal("0.2913"),
                Decimal("0.2912"),
                Decimal("0.2911"),
                Decimal("0.2910"),
                Decimal("0.2909"),
                Decimal("0.2908"),
                Decimal("0.2907"),
                Decimal("0.2906"),
                Decimal("0.2905"),
                Decimal("0.2904"),
                Decimal("0.2903"),
                Decimal("0.2902"),
                Decimal("0.2901"),
                Decimal("0.2900"),
            ),
            "G23*\n(GPa)": (
                Decimal("1.077"),
                Decimal("1.093"),
                Decimal("1.110"),
                Decimal("1.127"),
                Decimal("1.144"),
                Decimal("1.162"),
                Decimal("1.180"),
                Decimal("1.198"),
                Decimal("1.217"),
                Decimal("1.236"),
                Decimal("1.256"),
                Decimal("1.276"),
                Decimal("1.296"),
                Decimal("1.317"),
                Decimal("1.339"),
                Decimal("1.360"),
                Decimal("1.383"),
                Decimal("1.406"),
                Decimal("1.429"),
                Decimal("1.453"),
                Decimal("1.477"),
                Decimal("1.502"),
                Decimal("1.528"),
                Decimal("1.555"),
                Decimal("1.582"),
                Decimal("1.609"),
                Decimal("1.638"),
                Decimal("1.667"),
                Decimal("1.697"),
                Decimal("1.727"),
                Decimal("1.759"),
                Decimal("1.791"),
                Decimal("1.825"),
                Decimal("1.859"),
                Decimal("1.894"),
                Decimal("1.931"),
                Decimal("1.968"),
                Decimal("2.006"),
                Decimal("2.046"),
                Decimal("2.087"),
                Decimal("2.129"),
                Decimal("2.173"),
                Decimal("2.218"),
                Decimal("2.264"),
                Decimal("2.312"),
                Decimal("2.362"),
                Decimal("2.413"),
                Decimal("2.466"),
                Decimal("2.521"),
                Decimal("2.578"),
                Decimal("2.637"),
                Decimal("2.699"),
                Decimal("2.762"),
                Decimal("2.829"),
                Decimal("2.898"),
                Decimal("2.970"),
                Decimal("3.044"),
                Decimal("3.122"),
                Decimal("3.204"),
                Decimal("3.289"),
                Decimal("3.378"),
                Decimal("3.471"),
                Decimal("3.569"),
                Decimal("3.671"),
                Decimal("3.779"),
                Decimal("3.892"),
                Decimal("4.011"),
                Decimal("4.136"),
                Decimal("4.269"),
                Decimal("4.409"),
                Decimal("4.558"),
                Decimal("4.716"),
                Decimal("4.884"),
                Decimal("5.062"),
                Decimal("5.253"),
                Decimal("5.457"),
                Decimal("5.676"),
                Decimal("5.911"),
                Decimal("6.164"),
                Decimal("6.438"),
                Decimal("6.735"),
                Decimal("7.058"),
                Decimal("7.411"),
                Decimal("7.798"),
                Decimal("8.225"),
                Decimal("8.697"),
                Decimal("9.223"),
                Decimal("9.811"),
                Decimal("10.475"),
                Decimal("11.229"),
                Decimal("12.093"),
                Decimal("13.093"),
                Decimal("14.265"),
                Decimal("15.655"),
                Decimal("17.333"),
                Decimal("19.397"),
                Decimal("21.998"),
                Decimal("25.377"),
                Decimal("29.945"),
                Decimal("36.461"),
                Decimal("46.512"),
            ),
            "K23*\n(GPa)": (
                Decimal("2.692"),
                Decimal("2.729"),
                Decimal("2.766"),
                Decimal("2.805"),
                Decimal("2.844"),
                Decimal("2.883"),
                Decimal("2.924"),
                Decimal("2.965"),
                Decimal("3.008"),
                Decimal("3.051"),
                Decimal("3.095"),
                Decimal("3.140"),
                Decimal("3.186"),
                Decimal("3.233"),
                Decimal("3.282"),
                Decimal("3.331"),
                Decimal("3.381"),
                Decimal("3.433"),
                Decimal("3.486"),
                Decimal("3.540"),
                Decimal("3.595"),
                Decimal("3.652"),
                Decimal("3.710"),
                Decimal("3.769"),
                Decimal("3.830"),
                Decimal("3.892"),
                Decimal("3.957"),
                Decimal("4.022"),
                Decimal("4.090"),
                Decimal("4.159"),
                Decimal("4.231"),
                Decimal("4.304"),
                Decimal("4.379"),
                Decimal("4.457"),
                Decimal("4.536"),
                Decimal("4.618"),
                Decimal("4.702"),
                Decimal("4.789"),
                Decimal("4.879"),
                Decimal("4.971"),
                Decimal("5.067"),
                Decimal("5.165"),
                Decimal("5.266"),
                Decimal("5.371"),
                Decimal("5.480"),
                Decimal("5.592"),
                Decimal("5.708"),
                Decimal("5.828"),
                Decimal("5.952"),
                Decimal("6.081"),
                Decimal("6.215"),
                Decimal("6.354"),
                Decimal("6.498"),
                Decimal("6.649"),
                Decimal("6.805"),
                Decimal("6.967"),
                Decimal("7.137"),
                Decimal("7.313"),
                Decimal("7.498"),
                Decimal("7.690"),
                Decimal("7.892"),
                Decimal("8.103"),
                Decimal("8.324"),
                Decimal("8.557"),
                Decimal("8.801"),
                Decimal("9.057"),
                Decimal("9.328"),
                Decimal("9.613"),
                Decimal("9.914"),
                Decimal("10.233"),
                Decimal("10.570"),
                Decimal("10.929"),
                Decimal("11.310"),
                Decimal("11.716"),
                Decimal("12.150"),
                Decimal("12.615"),
                Decimal("13.113"),
                Decimal("13.648"),
                Decimal("14.226"),
                Decimal("14.851"),
                Decimal("15.529"),
                Decimal("16.268"),
                Decimal("17.075"),
                Decimal("17.961"),
                Decimal("18.938"),
                Decimal("20.020"),
                Decimal("21.226"),
                Decimal("22.579"),
                Decimal("24.106"),
                Decimal("25.845"),
                Decimal("27.841"),
                Decimal("30.156"),
                Decimal("32.875"),
                Decimal("36.112"),
                Decimal("40.032"),
                Decimal("44.875"),
                Decimal("51.011"),
                Decimal("59.039"),
                Decimal("69.993"),
                Decimal("85.828"),
                Decimal("110.742"),
            ),
        }
        result3 = _get_effective_properties_versus_full_range_Vf(composite3)
        assert result3 == {
            "Vf": (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            "E1*\n(GPa)": (
                Decimal("180.000"),
                Decimal("180.700"),
                Decimal("181.400"),
                Decimal("182.100"),
                Decimal("182.800"),
                Decimal("183.500"),
                Decimal("184.200"),
                Decimal("184.900"),
                Decimal("185.600"),
                Decimal("186.300"),
                Decimal("187.000"),
                Decimal("187.700"),
                Decimal("188.400"),
                Decimal("189.100"),
                Decimal("189.800"),
                Decimal("190.500"),
                Decimal("191.200"),
                Decimal("191.900"),
                Decimal("192.600"),
                Decimal("193.300"),
                Decimal("194.000"),
                Decimal("194.700"),
                Decimal("195.400"),
                Decimal("196.100"),
                Decimal("196.800"),
                Decimal("197.500"),
                Decimal("198.200"),
                Decimal("198.900"),
                Decimal("199.600"),
                Decimal("200.300"),
                Decimal("201.000"),
                Decimal("201.700"),
                Decimal("202.400"),
                Decimal("203.100"),
                Decimal("203.800"),
                Decimal("204.500"),
                Decimal("205.200"),
                Decimal("205.900"),
                Decimal("206.600"),
                Decimal("207.300"),
                Decimal("208.000"),
                Decimal("208.700"),
                Decimal("209.400"),
                Decimal("210.100"),
                Decimal("210.800"),
                Decimal("211.500"),
                Decimal("212.200"),
                Decimal("212.900"),
                Decimal("213.600"),
                Decimal("214.300"),
                Decimal("215.000"),
                Decimal("215.700"),
                Decimal("216.400"),
                Decimal("217.100"),
                Decimal("217.800"),
                Decimal("218.500"),
                Decimal("219.200"),
                Decimal("219.900"),
                Decimal("220.600"),
                Decimal("221.300"),
                Decimal("222.000"),
                Decimal("222.700"),
                Decimal("223.400"),
                Decimal("224.100"),
                Decimal("224.800"),
                Decimal("225.500"),
                Decimal("226.200"),
                Decimal("226.900"),
                Decimal("227.600"),
                Decimal("228.300"),
                Decimal("229.000"),
                Decimal("229.700"),
                Decimal("230.400"),
                Decimal("231.100"),
                Decimal("231.800"),
                Decimal("232.500"),
                Decimal("233.200"),
                Decimal("233.900"),
                Decimal("234.600"),
                Decimal("235.300"),
                Decimal("236.000"),
                Decimal("236.700"),
                Decimal("237.400"),
                Decimal("238.100"),
                Decimal("238.800"),
                Decimal("239.500"),
                Decimal("240.200"),
                Decimal("240.900"),
                Decimal("241.600"),
                Decimal("242.300"),
                Decimal("243.000"),
                Decimal("243.700"),
                Decimal("244.400"),
                Decimal("245.100"),
                Decimal("245.800"),
                Decimal("246.500"),
                Decimal("247.200"),
                Decimal("247.900"),
                Decimal("248.600"),
                Decimal("249.300"),
                Decimal("250.000"),
            ),
            "E2*\n(GPa)": (
                Decimal("20.000"),
                Decimal("20.049"),
                Decimal("20.100"),
                Decimal("20.149"),
                Decimal("20.199"),
                Decimal("20.250"),
                Decimal("20.300"),
                Decimal("20.350"),
                Decimal("20.400"),
                Decimal("20.450"),
                Decimal("20.500"),
                Decimal("20.550"),
                Decimal("20.600"),
                Decimal("20.650"),
                Decimal("20.700"),
                Decimal("20.750"),
                Decimal("20.800"),
                Decimal("20.850"),
                Decimal("20.900"),
                Decimal("20.950"),
                Decimal("21.000"),
                Decimal("21.050"),
                Decimal("21.100"),
                Decimal("21.150"),
                Decimal("21.200"),
                Decimal("21.250"),
                Decimal("21.300"),
                Decimal("21.350"),
                Decimal("21.400"),
                Decimal("21.450"),
                Decimal("21.500"),
                Decimal("21.550"),
                Decimal("21.600"),
                Decimal("21.650"),
                Decimal("21.700"),
                Decimal("21.750"),
                Decimal("21.800"),
                Decimal("21.850"),
                Decimal("21.900"),
                Decimal("21.950"),
                Decimal("22.000"),
                Decimal("22.050"),
                Decimal("22.100"),
                Decimal("22.150"),
                Decimal("22.200"),
                Decimal("22.250"),
                Decimal("22.300"),
                Decimal("22.350"),
                Decimal("22.400"),
                Decimal("22.450"),
                Decimal("22.500"),
                Decimal("22.550"),
                Decimal("22.600"),
                Decimal("22.650"),
                Decimal("22.700"),
                Decimal("22.750"),
                Decimal("22.800"),
                Decimal("22.850"),
                Decimal("22.900"),
                Decimal("22.950"),
                Decimal("23.000"),
                Decimal("23.050"),
                Decimal("23.100"),
                Decimal("23.150"),
                Decimal("23.200"),
                Decimal("23.250"),
                Decimal("23.300"),
                Decimal("23.350"),
                Decimal("23.400"),
                Decimal("23.450"),
                Decimal("23.500"),
                Decimal("23.550"),
                Decimal("23.600"),
                Decimal("23.650"),
                Decimal("23.700"),
                Decimal("23.750"),
                Decimal("23.800"),
                Decimal("23.850"),
                Decimal("23.900"),
                Decimal("23.950"),
                Decimal("24.000"),
                Decimal("24.050"),
                Decimal("24.100"),
                Decimal("24.150"),
                Decimal("24.200"),
                Decimal("24.250"),
                Decimal("24.300"),
                Decimal("24.350"),
                Decimal("24.400"),
                Decimal("24.450"),
                Decimal("24.500"),
                Decimal("24.550"),
                Decimal("24.600"),
                Decimal("24.650"),
                Decimal("24.700"),
                Decimal("24.750"),
                Decimal("24.800"),
                Decimal("24.850"),
                Decimal("24.900"),
                Decimal("24.950"),
                Decimal("25.000"),
            ),
            "G12*\n(GPa)": (
                Decimal("15.000"),
                Decimal("15.043"),
                Decimal("15.086"),
                Decimal("15.129"),
                Decimal("15.172"),
                Decimal("15.216"),
                Decimal("15.259"),
                Decimal("15.303"),
                Decimal("15.347"),
                Decimal("15.391"),
                Decimal("15.435"),
                Decimal("15.479"),
                Decimal("15.523"),
                Decimal("15.568"),
                Decimal("15.612"),
                Decimal("15.657"),
                Decimal("15.702"),
                Decimal("15.747"),
                Decimal("15.792"),
                Decimal("15.837"),
                Decimal("15.882"),
                Decimal("15.928"),
                Decimal("15.973"),
                Decimal("16.019"),
                Decimal("16.065"),
                Decimal("16.111"),
                Decimal("16.157"),
                Decimal("16.204"),
                Decimal("16.250"),
                Decimal("16.297"),
                Decimal("16.343"),
                Decimal("16.390"),
                Decimal("16.437"),
                Decimal("16.484"),
                Decimal("16.532"),
                Decimal("16.579"),
                Decimal("16.627"),
                Decimal("16.674"),
                Decimal("16.722"),
                Decimal("16.770"),
                Decimal("16.818"),
                Decimal("16.866"),
                Decimal("16.915"),
                Decimal("16.963"),
                Decimal("17.012"),
                Decimal("17.061"),
                Decimal("17.110"),
                Decimal("17.159"),
                Decimal("17.209"),
                Decimal("17.258"),
                Decimal("17.308"),
                Decimal("17.357"),
                Decimal("17.407"),
                Decimal("17.457"),
                Decimal("17.508"),
                Decimal("17.558"),
                Decimal("17.609"),
                Decimal("17.659"),
                Decimal("17.710"),
                Decimal("17.761"),
                Decimal("17.812"),
                Decimal("17.864"),
                Decimal("17.915"),
                Decimal("17.967"),
                Decimal("18.019"),
                Decimal("18.071"),
                Decimal("18.123"),
                Decimal("18.175"),
                Decimal("18.228"),
                Decimal("18.281"),
                Decimal("18.333"),
                Decimal("18.386"),
                Decimal("18.439"),
                Decimal("18.493"),
                Decimal("18.546"),
                Decimal("18.600"),
                Decimal("18.654"),
                Decimal("18.708"),
                Decimal("18.762"),
                Decimal("18.816"),
                Decimal("18.871"),
                Decimal("18.926"),
                Decimal("18.981"),
                Decimal("19.036"),
                Decimal("19.091"),
                Decimal("19.146"),
                Decimal("19.202"),
                Decimal("19.258"),
                Decimal("19.314"),
                Decimal("19.370"),
                Decimal("19.426"),
                Decimal("19.483"),
                Decimal("19.539"),
                Decimal("19.596"),
                Decimal("19.653"),
                Decimal("19.711"),
                Decimal("19.768"),
                Decimal("19.826"),
                Decimal("19.884"),
                Decimal("19.942"),
                Decimal("20.000"),
            ),
            "v12*": (
                Decimal("0.2900"),
                Decimal("0.2899"),
                Decimal("0.2898"),
                Decimal("0.2897"),
                Decimal("0.2896"),
                Decimal("0.2895"),
                Decimal("0.2894"),
                Decimal("0.2893"),
                Decimal("0.2892"),
                Decimal("0.2891"),
                Decimal("0.2890"),
                Decimal("0.2889"),
                Decimal("0.2888"),
                Decimal("0.2887"),
                Decimal("0.2886"),
                Decimal("0.2885"),
                Decimal("0.2884"),
                Decimal("0.2883"),
                Decimal("0.2882"),
                Decimal("0.2881"),
                Decimal("0.2880"),
                Decimal("0.2879"),
                Decimal("0.2878"),
                Decimal("0.2877"),
                Decimal("0.2876"),
                Decimal("0.2875"),
                Decimal("0.2874"),
                Decimal("0.2873"),
                Decimal("0.2872"),
                Decimal("0.2871"),
                Decimal("0.2870"),
                Decimal("0.2869"),
                Decimal("0.2868"),
                Decimal("0.2867"),
                Decimal("0.2866"),
                Decimal("0.2865"),
                Decimal("0.2864"),
                Decimal("0.2863"),
                Decimal("0.2862"),
                Decimal("0.2861"),
                Decimal("0.2860"),
                Decimal("0.2859"),
                Decimal("0.2858"),
                Decimal("0.2857"),
                Decimal("0.2856"),
                Decimal("0.2855"),
                Decimal("0.2854"),
                Decimal("0.2853"),
                Decimal("0.2852"),
                Decimal("0.2851"),
                Decimal("0.2850"),
                Decimal("0.2849"),
                Decimal("0.2848"),
                Decimal("0.2847"),
                Decimal("0.2846"),
                Decimal("0.2845"),
                Decimal("0.2844"),
                Decimal("0.2843"),
                Decimal("0.2842"),
                Decimal("0.2841"),
                Decimal("0.2840"),
                Decimal("0.2839"),
                Decimal("0.2838"),
                Decimal("0.2837"),
                Decimal("0.2836"),
                Decimal("0.2835"),
                Decimal("0.2834"),
                Decimal("0.2833"),
                Decimal("0.2832"),
                Decimal("0.2831"),
                Decimal("0.2830"),
                Decimal("0.2829"),
                Decimal("0.2828"),
                Decimal("0.2827"),
                Decimal("0.2826"),
                Decimal("0.2825"),
                Decimal("0.2824"),
                Decimal("0.2823"),
                Decimal("0.2822"),
                Decimal("0.2821"),
                Decimal("0.2820"),
                Decimal("0.2819"),
                Decimal("0.2818"),
                Decimal("0.2817"),
                Decimal("0.2816"),
                Decimal("0.2815"),
                Decimal("0.2814"),
                Decimal("0.2813"),
                Decimal("0.2812"),
                Decimal("0.2811"),
                Decimal("0.2810"),
                Decimal("0.2809"),
                Decimal("0.2808"),
                Decimal("0.2807"),
                Decimal("0.2806"),
                Decimal("0.2805"),
                Decimal("0.2804"),
                Decimal("0.2803"),
                Decimal("0.2802"),
                Decimal("0.2801"),
                Decimal("0.2800"),
            ),
            "G23*\n(GPa)": (
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
            ),
            "K23*\n(GPa)": (
                Decimal("10.190"),
                Decimal("10.241"),
                Decimal("10.293"),
                Decimal("10.344"),
                Decimal("10.396"),
                Decimal("10.449"),
                Decimal("10.501"),
                Decimal("10.554"),
                Decimal("10.607"),
                Decimal("10.660"),
                Decimal("10.714"),
                Decimal("10.768"),
                Decimal("10.822"),
                Decimal("10.876"),
                Decimal("10.931"),
                Decimal("10.986"),
                Decimal("11.041"),
                Decimal("11.097"),
                Decimal("11.153"),
                Decimal("11.209"),
                Decimal("11.265"),
                Decimal("11.322"),
                Decimal("11.379"),
                Decimal("11.437"),
                Decimal("11.494"),
                Decimal("11.552"),
                Decimal("11.611"),
                Decimal("11.669"),
                Decimal("11.728"),
                Decimal("11.788"),
                Decimal("11.847"),
                Decimal("11.907"),
                Decimal("11.967"),
                Decimal("12.028"),
                Decimal("12.089"),
                Decimal("12.150"),
                Decimal("12.212"),
                Decimal("12.274"),
                Decimal("12.336"),
                Decimal("12.399"),
                Decimal("12.462"),
                Decimal("12.525"),
                Decimal("12.589"),
                Decimal("12.653"),
                Decimal("12.717"),
                Decimal("12.782"),
                Decimal("12.848"),
                Decimal("12.913"),
                Decimal("12.979"),
                Decimal("13.045"),
                Decimal("13.112"),
                Decimal("13.179"),
                Decimal("13.247"),
                Decimal("13.314"),
                Decimal("13.383"),
                Decimal("13.451"),
                Decimal("13.521"),
                Decimal("13.590"),
                Decimal("13.660"),
                Decimal("13.730"),
                Decimal("13.801"),
                Decimal("13.872"),
                Decimal("13.944"),
                Decimal("14.016"),
                Decimal("14.088"),
                Decimal("14.161"),
                Decimal("14.234"),
                Decimal("14.308"),
                Decimal("14.382"),
                Decimal("14.457"),
                Decimal("14.532"),
                Decimal("14.608"),
                Decimal("14.684"),
                Decimal("14.760"),
                Decimal("14.837"),
                Decimal("14.915"),
                Decimal("14.993"),
                Decimal("15.071"),
                Decimal("15.150"),
                Decimal("15.230"),
                Decimal("15.310"),
                Decimal("15.390"),
                Decimal("15.471"),
                Decimal("15.553"),
                Decimal("15.635"),
                Decimal("15.717"),
                Decimal("15.801"),
                Decimal("15.884"),
                Decimal("15.968"),
                Decimal("16.053"),
                Decimal("16.138"),
                Decimal("16.224"),
                Decimal("16.311"),
                Decimal("16.398"),
                Decimal("16.485"),
                Decimal("16.573"),
                Decimal("16.662"),
                Decimal("16.751"),
                Decimal("16.841"),
                Decimal("16.932"),
                Decimal("17.023"),
            ),
        }
        result4 = _get_effective_properties_versus_full_range_Vf(composite4)
        assert result4 == {
            "Vf": (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            "E1*\n(GPa)": (
                Decimal("180.000"),
                Decimal("179.400"),
                Decimal("178.800"),
                Decimal("178.200"),
                Decimal("177.600"),
                Decimal("177.000"),
                Decimal("176.400"),
                Decimal("175.800"),
                Decimal("175.200"),
                Decimal("174.600"),
                Decimal("174.000"),
                Decimal("173.400"),
                Decimal("172.800"),
                Decimal("172.200"),
                Decimal("171.600"),
                Decimal("171.000"),
                Decimal("170.400"),
                Decimal("169.800"),
                Decimal("169.200"),
                Decimal("168.600"),
                Decimal("168.000"),
                Decimal("167.400"),
                Decimal("166.800"),
                Decimal("166.200"),
                Decimal("165.600"),
                Decimal("165.000"),
                Decimal("164.400"),
                Decimal("163.800"),
                Decimal("163.200"),
                Decimal("162.600"),
                Decimal("162.000"),
                Decimal("161.400"),
                Decimal("160.800"),
                Decimal("160.200"),
                Decimal("159.600"),
                Decimal("159.000"),
                Decimal("158.400"),
                Decimal("157.800"),
                Decimal("157.200"),
                Decimal("156.600"),
                Decimal("156.000"),
                Decimal("155.400"),
                Decimal("154.800"),
                Decimal("154.200"),
                Decimal("153.600"),
                Decimal("153.000"),
                Decimal("152.400"),
                Decimal("151.800"),
                Decimal("151.200"),
                Decimal("150.600"),
                Decimal("150.000"),
                Decimal("149.400"),
                Decimal("148.800"),
                Decimal("148.200"),
                Decimal("147.600"),
                Decimal("147.000"),
                Decimal("146.400"),
                Decimal("145.800"),
                Decimal("145.200"),
                Decimal("144.600"),
                Decimal("144.000"),
                Decimal("143.400"),
                Decimal("142.800"),
                Decimal("142.200"),
                Decimal("141.600"),
                Decimal("141.000"),
                Decimal("140.400"),
                Decimal("139.800"),
                Decimal("139.200"),
                Decimal("138.600"),
                Decimal("138.000"),
                Decimal("137.400"),
                Decimal("136.800"),
                Decimal("136.200"),
                Decimal("135.600"),
                Decimal("135.000"),
                Decimal("134.400"),
                Decimal("133.800"),
                Decimal("133.200"),
                Decimal("132.600"),
                Decimal("132.000"),
                Decimal("131.400"),
                Decimal("130.800"),
                Decimal("130.200"),
                Decimal("129.600"),
                Decimal("129.000"),
                Decimal("128.400"),
                Decimal("127.800"),
                Decimal("127.200"),
                Decimal("126.600"),
                Decimal("126.000"),
                Decimal("125.400"),
                Decimal("124.800"),
                Decimal("124.200"),
                Decimal("123.600"),
                Decimal("123.000"),
                Decimal("122.400"),
                Decimal("121.800"),
                Decimal("121.200"),
                Decimal("120.600"),
                Decimal("120.000"),
            ),
            "E2*\n(GPa)": (
                Decimal("20.000"),
                Decimal("20.261"),
                Decimal("20.526"),
                Decimal("20.793"),
                Decimal("21.066"),
                Decimal("21.342"),
                Decimal("21.622"),
                Decimal("21.907"),
                Decimal("22.196"),
                Decimal("22.488"),
                Decimal("22.786"),
                Decimal("23.088"),
                Decimal("23.395"),
                Decimal("23.706"),
                Decimal("24.023"),
                Decimal("24.344"),
                Decimal("24.672"),
                Decimal("25.004"),
                Decimal("25.341"),
                Decimal("25.684"),
                Decimal("26.035"),
                Decimal("26.389"),
                Decimal("26.751"),
                Decimal("27.117"),
                Decimal("27.492"),
                Decimal("27.872"),
                Decimal("28.260"),
                Decimal("28.655"),
                Decimal("29.055"),
                Decimal("29.466"),
                Decimal("29.882"),
                Decimal("30.307"),
                Decimal("30.741"),
                Decimal("31.181"),
                Decimal("31.632"),
                Decimal("32.091"),
                Decimal("32.559"),
                Decimal("33.037"),
                Decimal("33.524"),
                Decimal("34.022"),
                Decimal("34.530"),
                Decimal("35.048"),
                Decimal("35.578"),
                Decimal("36.119"),
                Decimal("36.673"),
                Decimal("37.238"),
                Decimal("37.818"),
                Decimal("38.409"),
                Decimal("39.014"),
                Decimal("39.633"),
                Decimal("40.268"),
                Decimal("40.917"),
                Decimal("41.581"),
                Decimal("42.262"),
                Decimal("42.961"),
                Decimal("43.678"),
                Decimal("44.411"),
                Decimal("45.165"),
                Decimal("45.938"),
                Decimal("46.732"),
                Decimal("47.546"),
                Decimal("48.384"),
                Decimal("49.244"),
                Decimal("50.130"),
                Decimal("51.041"),
                Decimal("51.978"),
                Decimal("52.942"),
                Decimal("53.936"),
                Decimal("54.959"),
                Decimal("56.015"),
                Decimal("57.102"),
                Decimal("58.226"),
                Decimal("59.385"),
                Decimal("60.582"),
                Decimal("61.821"),
                Decimal("63.101"),
                Decimal("64.426"),
                Decimal("65.798"),
                Decimal("67.218"),
                Decimal("68.692"),
                Decimal("70.220"),
                Decimal("71.807"),
                Decimal("73.454"),
                Decimal("75.168"),
                Decimal("76.953"),
                Decimal("78.808"),
                Decimal("80.743"),
                Decimal("82.761"),
                Decimal("84.867"),
                Decimal("87.069"),
                Decimal("89.374"),
                Decimal("91.786"),
                Decimal("94.314"),
                Decimal("96.969"),
                Decimal("99.757"),
                Decimal("102.692"),
                Decimal("105.782"),
                Decimal("109.044"),
                Decimal("112.489"),
                Decimal("116.135"),
                Decimal("120.001"),
            ),
            "G12*\n(GPa)": (
                Decimal("15.000"),
                Decimal("15.154"),
                Decimal("15.311"),
                Decimal("15.468"),
                Decimal("15.628"),
                Decimal("15.789"),
                Decimal("15.951"),
                Decimal("16.116"),
                Decimal("16.282"),
                Decimal("16.450"),
                Decimal("16.620"),
                Decimal("16.792"),
                Decimal("16.965"),
                Decimal("17.140"),
                Decimal("17.318"),
                Decimal("17.497"),
                Decimal("17.679"),
                Decimal("17.862"),
                Decimal("18.047"),
                Decimal("18.235"),
                Decimal("18.425"),
                Decimal("18.616"),
                Decimal("18.811"),
                Decimal("19.007"),
                Decimal("19.206"),
                Decimal("19.407"),
                Decimal("19.610"),
                Decimal("19.816"),
                Decimal("20.024"),
                Decimal("20.235"),
                Decimal("20.448"),
                Decimal("20.664"),
                Decimal("20.882"),
                Decimal("21.104"),
                Decimal("21.327"),
                Decimal("21.554"),
                Decimal("21.784"),
                Decimal("22.016"),
                Decimal("22.252"),
                Decimal("22.490"),
                Decimal("22.732"),
                Decimal("22.977"),
                Decimal("23.224"),
                Decimal("23.476"),
                Decimal("23.730"),
                Decimal("23.988"),
                Decimal("24.249"),
                Decimal("24.514"),
                Decimal("24.782"),
                Decimal("25.055"),
                Decimal("25.330"),
                Decimal("25.610"),
                Decimal("25.894"),
                Decimal("26.181"),
                Decimal("26.473"),
                Decimal("26.769"),
                Decimal("27.069"),
                Decimal("27.373"),
                Decimal("27.682"),
                Decimal("27.995"),
                Decimal("28.313"),
                Decimal("28.636"),
                Decimal("28.964"),
                Decimal("29.296"),
                Decimal("29.634"),
                Decimal("29.977"),
                Decimal("30.325"),
                Decimal("30.678"),
                Decimal("31.038"),
                Decimal("31.402"),
                Decimal("31.773"),
                Decimal("32.150"),
                Decimal("32.532"),
                Decimal("32.921"),
                Decimal("33.317"),
                Decimal("33.719"),
                Decimal("34.127"),
                Decimal("34.543"),
                Decimal("34.966"),
                Decimal("35.396"),
                Decimal("35.833"),
                Decimal("36.278"),
                Decimal("36.731"),
                Decimal("37.192"),
                Decimal("37.661"),
                Decimal("38.139"),
                Decimal("38.626"),
                Decimal("39.122"),
                Decimal("39.626"),
                Decimal("40.141"),
                Decimal("40.665"),
                Decimal("41.199"),
                Decimal("41.744"),
                Decimal("42.299"),
                Decimal("42.865"),
                Decimal("43.443"),
                Decimal("44.032"),
                Decimal("44.633"),
                Decimal("45.246"),
                Decimal("45.873"),
                Decimal("46.512"),
            ),
            "v12*": (
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
            ),
            "G23*\n(GPa)": (
                Decimal("10.000"),
                Decimal("10.099"),
                Decimal("10.199"),
                Decimal("10.300"),
                Decimal("10.403"),
                Decimal("10.508"),
                Decimal("10.614"),
                Decimal("10.722"),
                Decimal("10.832"),
                Decimal("10.943"),
                Decimal("11.056"),
                Decimal("11.171"),
                Decimal("11.288"),
                Decimal("11.406"),
                Decimal("11.527"),
                Decimal("11.649"),
                Decimal("11.774"),
                Decimal("11.901"),
                Decimal("12.029"),
                Decimal("12.160"),
                Decimal("12.294"),
                Decimal("12.429"),
                Decimal("12.567"),
                Decimal("12.707"),
                Decimal("12.850"),
                Decimal("12.995"),
                Decimal("13.143"),
                Decimal("13.294"),
                Decimal("13.447"),
                Decimal("13.604"),
                Decimal("13.763"),
                Decimal("13.925"),
                Decimal("14.091"),
                Decimal("14.259"),
                Decimal("14.431"),
                Decimal("14.606"),
                Decimal("14.785"),
                Decimal("14.967"),
                Decimal("15.153"),
                Decimal("15.343"),
                Decimal("15.537"),
                Decimal("15.734"),
                Decimal("15.936"),
                Decimal("16.142"),
                Decimal("16.353"),
                Decimal("16.568"),
                Decimal("16.789"),
                Decimal("17.014"),
                Decimal("17.244"),
                Decimal("17.479"),
                Decimal("17.720"),
                Decimal("17.966"),
                Decimal("18.218"),
                Decimal("18.476"),
                Decimal("18.741"),
                Decimal("19.012"),
                Decimal("19.289"),
                Decimal("19.574"),
                Decimal("19.866"),
                Decimal("20.165"),
                Decimal("20.472"),
                Decimal("20.788"),
                Decimal("21.111"),
                Decimal("21.444"),
                Decimal("21.786"),
                Decimal("22.137"),
                Decimal("22.498"),
                Decimal("22.870"),
                Decimal("23.252"),
                Decimal("23.646"),
                Decimal("24.051"),
                Decimal("24.469"),
                Decimal("24.900"),
                Decimal("25.344"),
                Decimal("25.803"),
                Decimal("26.276"),
                Decimal("26.765"),
                Decimal("27.271"),
                Decimal("27.793"),
                Decimal("28.334"),
                Decimal("28.894"),
                Decimal("29.474"),
                Decimal("30.075"),
                Decimal("30.699"),
                Decimal("31.347"),
                Decimal("32.019"),
                Decimal("32.718"),
                Decimal("33.445"),
                Decimal("34.202"),
                Decimal("34.991"),
                Decimal("35.814"),
                Decimal("36.673"),
                Decimal("37.570"),
                Decimal("38.509"),
                Decimal("39.491"),
                Decimal("40.521"),
                Decimal("41.601"),
                Decimal("42.736"),
                Decimal("43.929"),
                Decimal("45.186"),
                Decimal("46.512"),
            ),
            "K23*\n(GPa)": (
                Decimal("10.190"),
                Decimal("10.360"),
                Decimal("10.532"),
                Decimal("10.707"),
                Decimal("10.886"),
                Decimal("11.067"),
                Decimal("11.252"),
                Decimal("11.440"),
                Decimal("11.631"),
                Decimal("11.826"),
                Decimal("12.024"),
                Decimal("12.226"),
                Decimal("12.432"),
                Decimal("12.641"),
                Decimal("12.855"),
                Decimal("13.072"),
                Decimal("13.294"),
                Decimal("13.520"),
                Decimal("13.750"),
                Decimal("13.985"),
                Decimal("14.225"),
                Decimal("14.469"),
                Decimal("14.719"),
                Decimal("14.973"),
                Decimal("15.233"),
                Decimal("15.499"),
                Decimal("15.770"),
                Decimal("16.047"),
                Decimal("16.329"),
                Decimal("16.619"),
                Decimal("16.914"),
                Decimal("17.216"),
                Decimal("17.525"),
                Decimal("17.841"),
                Decimal("18.165"),
                Decimal("18.496"),
                Decimal("18.835"),
                Decimal("19.182"),
                Decimal("19.537"),
                Decimal("19.902"),
                Decimal("20.275"),
                Decimal("20.658"),
                Decimal("21.051"),
                Decimal("21.453"),
                Decimal("21.867"),
                Decimal("22.291"),
                Decimal("22.727"),
                Decimal("23.175"),
                Decimal("23.635"),
                Decimal("24.108"),
                Decimal("24.595"),
                Decimal("25.096"),
                Decimal("25.611"),
                Decimal("26.142"),
                Decimal("26.689"),
                Decimal("27.253"),
                Decimal("27.834"),
                Decimal("28.434"),
                Decimal("29.053"),
                Decimal("29.693"),
                Decimal("30.353"),
                Decimal("31.036"),
                Decimal("31.743"),
                Decimal("32.474"),
                Decimal("33.232"),
                Decimal("34.017"),
                Decimal("34.831"),
                Decimal("35.675"),
                Decimal("36.552"),
                Decimal("37.464"),
                Decimal("38.411"),
                Decimal("39.398"),
                Decimal("40.425"),
                Decimal("41.496"),
                Decimal("42.614"),
                Decimal("43.781"),
                Decimal("45.001"),
                Decimal("46.278"),
                Decimal("47.615"),
                Decimal("49.018"),
                Decimal("50.490"),
                Decimal("52.038"),
                Decimal("53.667"),
                Decimal("55.384"),
                Decimal("57.197"),
                Decimal("59.112"),
                Decimal("61.140"),
                Decimal("63.291"),
                Decimal("65.575"),
                Decimal("68.007"),
                Decimal("70.601"),
                Decimal("73.372"),
                Decimal("76.342"),
                Decimal("79.530"),
                Decimal("82.963"),
                Decimal("86.670"),
                Decimal("90.684"),
                Decimal("95.047"),
                Decimal("99.805"),
                Decimal("105.014"),
                Decimal("110.742"),
            ),
        }

    def test_get_effective_properties_versus_full_range_Vf_output_with_invalid_inputs(
            self, carbon
    ):
        """
        Test output of ``_get_effective_properties_versus_full_range_Vf`` helper
        function with invalid input that raises TypeError
        """
        with pytest.raises(TypeError):
            _get_effective_properties_versus_full_range_Vf()  # argument is None
        with pytest.raises(TypeError):
            _get_effective_properties_versus_full_range_Vf(
                carbon
            )  # argument is not HT object

    def test_get_effective_properties_versus_specific_value_Vf_output(
            self, composite1, composite2, composite3, composite4,
    ):
        """
        Test output of ``_get_effective_properties_versus_specific_value_Vf`` helper
        function with valid arguments, i.e. 4 different UD composites having different
        types of consituent materials where each will have their own trial index number
        for testing
        """
        result1 = _get_effective_properties_versus_specific_value_Vf(
            composite1, 0
        )  # At lower index 0
        assert result1 == [
            [
                "Vf",
                "E1*\n(GPa)",
                "E2*\n(GPa)",
                "G12*\n(GPa)",
                "v12*",
                "G23*\n(GPa)",
                "K23*\n(GPa)",
            ],
            [
                Decimal("0.000"),
                Decimal("2.800"),
                Decimal("2.800"),
                Decimal("1.077"),
                Decimal("0.300"),
                Decimal("1.077"),
                Decimal("2.692"),
            ],
        ]
        result2 = _get_effective_properties_versus_specific_value_Vf(
            composite2, 100
        )  # At maximum index number 100
        assert result2 == [
            [
                "Vf",
                "E1*\n(GPa)",
                "E2*\n(GPa)",
                "G12*\n(GPa)",
                "v12*",
                "G23*\n(GPa)",
                "K23*\n(GPa)",
            ],
            [
                Decimal("1.000"),
                Decimal("120.000"),
                Decimal("120.001"),
                Decimal("46.512"),
                Decimal("0.290"),
                Decimal("46.512"),
                Decimal("110.742"),
            ],
        ]
        result3 = _get_effective_properties_versus_specific_value_Vf(
            composite3, 45
        )  # At index number 45
        assert result3 == [
            [
                "Vf",
                "E1*\n(GPa)",
                "E2*\n(GPa)",
                "G12*\n(GPa)",
                "v12*",
                "G23*\n(GPa)",
                "K23*\n(GPa)",
            ],
            [
                Decimal("0.450"),
                Decimal("211.500"),
                Decimal("22.250"),
                Decimal("17.061"),
                Decimal("0.2855"),
                Decimal("10.000"),
                Decimal("12.782"),
            ],
        ]
        result4 = _get_effective_properties_versus_specific_value_Vf(
            composite4, 64
        )  # At index number 64
        assert result4 == [
            [
                "Vf",
                "E1*\n(GPa)",
                "E2*\n(GPa)",
                "G12*\n(GPa)",
                "v12*",
                "G23*\n(GPa)",
                "K23*\n(GPa)",
            ],
            [
                Decimal("0.640"),
                Decimal("141.600"),
                Decimal("51.041"),
                Decimal("29.634"),
                Decimal("0.2900"),
                Decimal("21.786"),
                Decimal("33.232"),
            ],
        ]

    def test_get_effective_properties_versus_specific_value_Vf_output_with_invalid_input(
            self, carbon, composite1, none_arg
    ):
        """
        Test output of ``_get_effective_properties_versus_specific_value_Vf`` helper
        function with invalid arguments that raise TypeError and ValueError
        """
        with pytest.raises(TypeError):
            _get_effective_properties_versus_specific_value_Vf()  # no argument
        with pytest.raises(TypeError):
            _get_effective_properties_versus_specific_value_Vf(
                none_arg, 40
            )  # first_argument is None
        with pytest.raises(TypeError):
            _get_effective_properties_versus_specific_value_Vf(
                carbon, 40
            )  # first argument is not HT object
        with pytest.raises(TypeError):
            _get_effective_properties_versus_specific_value_Vf(
                composite1, none_arg
            )  # second argument is None
        with pytest.raises(TypeError):
            _get_effective_properties_versus_specific_value_Vf(
                composite1, 40.0
            )  # second argument is not int
        with pytest.raises(ValueError):
            _get_effective_properties_versus_specific_value_Vf(
                composite1, -1
            )  # second argument is less than 0
        with pytest.raises(ValueError):
            _get_effective_properties_versus_specific_value_Vf(
                composite1, 101
            )  # second argument is greater than 100

    def test_get_effective_properties_versus_specific_range_Vf_output(
            self, composite1, composite2, composite3, composite4
    ):
        """
        Test output of ``_get_effective_properties_versus_specific_range_Vf`` helper
        function with valid arguments, i.e. 4 different UD composites with different
        types of constituent materials and each has different starting and ending index
        numbers for testing
        """
        result1 = _get_effective_properties_versus_specific_range_Vf(composite1, 0, 5)
        assert result1 == {
            "Vf": [
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
            ],
            "E1*\n(GPa)": [
                Decimal("2.800"),
                Decimal("5.272"),
                Decimal("7.744"),
                Decimal("10.216"),
                Decimal("12.688"),
                Decimal("15.160"),
            ],
            "E2*\n(GPa)": [
                Decimal("2.800"),
                Decimal("2.958"),
                Decimal("3.045"),
                Decimal("3.108"),
                Decimal("3.163"),
                Decimal("3.216"),
            ],
            "G12*\n(GPa)": [
                Decimal("1.077"),
                Decimal("1.097"),
                Decimal("1.116"),
                Decimal("1.137"),
                Decimal("1.157"),
                Decimal("1.178"),
            ],
            "v12*": [
                Decimal("0.3000"),
                Decimal("0.2998"),
                Decimal("0.2996"),
                Decimal("0.2994"),
                Decimal("0.2992"),
                Decimal("0.2990"),
            ],
            "G23*\n(GPa)": [
                Decimal("1.077"),
                Decimal("1.091"),
                Decimal("1.106"),
                Decimal("1.120"),
                Decimal("1.135"),
                Decimal("1.151"),
            ],
            "K23*\n(GPa)": [
                Decimal("2.692"),
                Decimal("2.722"),
                Decimal("2.753"),
                Decimal("2.784"),
                Decimal("2.815"),
                Decimal("2.847"),
            ],
        }
        result2 = _get_effective_properties_versus_specific_range_Vf(
            composite2, 95, 100
        )
        assert result2 == {
            "Vf": [
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ],
            "E1*\n(GPa)": [
                Decimal("114.140"),
                Decimal("115.312"),
                Decimal("116.484"),
                Decimal("117.656"),
                Decimal("118.828"),
                Decimal("120.000"),
            ],
            "E2*\n(GPa)": [
                Decimal("52.086"),
                Decimal("58.834"),
                Decimal("67.525"),
                Decimal("79.138"),
                Decimal("95.441"),
                Decimal("120.001"),
            ],
            "G12*\n(GPa)": [
                Decimal("22.084"),
                Decimal("24.734"),
                Decimal("28.069"),
                Decimal("32.392"),
                Decimal("38.222"),
                Decimal("46.512"),
            ],
            "v12*": [
                Decimal("0.2905"),
                Decimal("0.2904"),
                Decimal("0.2903"),
                Decimal("0.2902"),
                Decimal("0.2901"),
                Decimal("0.2900"),
            ],
            "G23*\n(GPa)": [
                Decimal("19.397"),
                Decimal("21.998"),
                Decimal("25.377"),
                Decimal("29.945"),
                Decimal("36.461"),
                Decimal("46.512"),
            ],
            "K23*\n(GPa)": [
                Decimal("44.875"),
                Decimal("51.011"),
                Decimal("59.039"),
                Decimal("69.993"),
                Decimal("85.828"),
                Decimal("110.742"),
            ],
        }
        result3 = _get_effective_properties_versus_specific_range_Vf(composite3, 50, 52)
        assert result3 == {
            "Vf": [
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
            ],
            "E1*\n(GPa)": [
                Decimal("215.000"),
                Decimal("215.700"),
                Decimal("216.400"),
            ],
            "E2*\n(GPa)": [
                Decimal("22.500"),
                Decimal("22.550"),
                Decimal("22.600"),
            ],
            "G12*\n(GPa)": [
                Decimal("17.308"),
                Decimal("17.357"),
                Decimal("17.407"),
            ],
            "v12*": [
                Decimal("0.2850"),
                Decimal("0.2849"),
                Decimal("0.2848"),
            ],
            "G23*\n(GPa)": [
                Decimal("10.000"),
                Decimal("10.000"),
                Decimal("10.000"),
            ],
            "K23*\n(GPa)": [
                Decimal("13.112"),
                Decimal("13.179"),
                Decimal("13.247"),
            ],
        }
        result4 = _get_effective_properties_versus_specific_range_Vf(composite4, 64, 65)
        assert result4 == {
            "Vf": [
                Decimal("0.64"),
                Decimal("0.65"),
            ],
            "E1*\n(GPa)": [
                Decimal("141.600"),
                Decimal("141.000"),
            ],
            "E2*\n(GPa)": [
                Decimal("51.041"),
                Decimal("51.978"),
            ],
            "G12*\n(GPa)": [
                Decimal("29.634"),
                Decimal("29.977"),
            ],
            "v12*": [
                Decimal("0.2900"),
                Decimal("0.2900"),
            ],
            "G23*\n(GPa)": [
                Decimal("21.786"),
                Decimal("22.137"),
            ],
            "K23*\n(GPa)": [
                Decimal("33.232"),
                Decimal("34.017"),
            ],
        }

    def test_get_effective_properties_versus_specific_range_Vf_output_with_invalid_inputs(
            self, carbon, composite1, none_arg
    ):
        """
        Test output of ``_get_effective_properties_versus_specific_range_Vf`` helper
        function with invalid arguments that raise TypeError and ValueError
        """
        with pytest.raises(TypeError):
            _get_effective_properties_versus_specific_range_Vf()  # no argument
        with pytest.raises(TypeError):
            _get_effective_properties_versus_specific_range_Vf(
                none_arg, 40, 50
            )  # first argument is None
        with pytest.raises(TypeError):
            _get_effective_properties_versus_specific_range_Vf(
                carbon, 40, 50
            )  # first argument is not HT object
        with pytest.raises(TypeError):
            _get_effective_properties_versus_specific_range_Vf(
                composite1, none_arg, 50
            )  # second argument is None
        with pytest.raises(TypeError):
            _get_effective_properties_versus_specific_range_Vf(
                composite1, 40.0, 50
            )  # second argument is not int
        with pytest.raises(TypeError):
            _get_effective_properties_versus_specific_range_Vf(
                composite1, 40, none_arg
            )  # third argument is None
        with pytest.raises(TypeError):
            _get_effective_properties_versus_specific_range_Vf(
                composite1, 40, 50.0
            )  # third argument is not int
        with pytest.raises(ValueError):
            _get_effective_properties_versus_specific_range_Vf(
                composite1, -1, 50
            )  # second argument is less than 0
        with pytest.raises(ValueError):
            _get_effective_properties_versus_specific_range_Vf(
                composite1, 101, 50
            )  # second argument is greater than 100
        with pytest.raises(ValueError):
            _get_effective_properties_versus_specific_range_Vf(
                composite1, 60, 50
            )  # second argument is greater than third argument
        with pytest.raises(ValueError):
            _get_effective_properties_versus_specific_range_Vf(
                composite1, 40, -1
            )  # third argument is less than zero and less than second argument
        with pytest.raises(ValueError):
            _get_effective_properties_versus_specific_range_Vf(
                composite1, 40, 101
            )  # third argument is greater than 100
        with pytest.raises(ValueError):
            _get_effective_properties_versus_specific_range_Vf(
                composite1, 40, 30
            )  # third argument is lesser than second argument
        with pytest.raises(ValueError):
            _get_effective_properties_versus_specific_range_Vf(
                composite1, 40, 40
            )  # second and third argument is of equal value

    @pytest.fixture
    def properties_in_list(self):
        """
        Provide arguments of elastic properties organized as a valid list
        """
        return [
            [
                "Vf",
                "E1*\n(GPa)",
                "E2*\n(GPa)",
                "G12*\n(GPa)",
                "v12*",
                "G23*\n(GPa)",
                "K23*\n(GPa)",
            ],
            [
                Decimal("0.400"),
                Decimal("101.680"),
                Decimal("5.353"),
                Decimal("2.284"),
                Decimal("0.2920"),
                Decimal("1.928"),
                Decimal("4.439"),
            ],
        ]

    def test_print_tabulate_output_with_valid_list(self, properties_in_list, capsys):
        """
        Test output of ``_print_tabulate`` helper function with valid arguments, e.g.
        first argument as list object that contains 2 lists and second argument as
        "firstrow" as per tabulate syntax
        """
        print(_print_tabulate(properties_in_list, "firstrow"))  # list with "firstrow"
        captured = capsys.readouterr()
        assert captured.out == (
            "+------+---------+---------+---------+--------+---------+---------+\n"
            + "|   Vf |     E1* |     E2* |    G12* |   v12* |    G23* |    K23* |\n"
            + "|      |   (GPa) |   (GPa) |   (GPa) |        |   (GPa) |   (GPa) |\n"
            + "+======+=========+=========+=========+========+=========+=========+\n"
            + "| 0.40 |  101.68 |    5.35 |    2.28 |   0.29 |    1.93 |    4.44 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
        )

    @pytest.fixture
    def properties_in_dict(self):
        """
        Provide arguments of elastic properties organized as a valid dict
        """
        return {
            "Vf": [
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
            ],
            "E1*\n(GPa)": [
                Decimal("126.400"),
                Decimal("128.872"),
                Decimal("131.344"),
            ],
            "E2*\n(GPa)": [
                Decimal("6.328"),
                Decimal("6.441"),
                Decimal("6.558"),
            ],
            "G12*\n(GPa)": [
                Decimal("2.832"),
                Decimal("2.896"),
                Decimal("2.963"),
            ],
            "v12*": [
                Decimal("0.2900"),
                Decimal("0.2898"),
                Decimal("0.2896"),
            ],
            "G23*\n(GPa)": [
                Decimal("2.295"),
                Decimal("2.338"),
                Decimal("2.382"),
            ],
            "K23*\n(GPa)": [
                Decimal("5.162"),
                Decimal("5.245"),
                Decimal("5.330"),
            ],
        }

    def test_print_tabulate_output_with_valid_dict(self, properties_in_dict, capsys):
        """
        Test output of ``_print_tabulate`` helper function with valid arguments, e.g.
        first argument as dict object and second argument as "keys" as per tabulate
        syntax
        """
        print(_print_tabulate(properties_in_dict, "keys"))  # dict with "keys"
        captured = capsys.readouterr()
        assert captured.out == (
            "+------+---------+---------+---------+--------+---------+---------+\n"
            + "|   Vf |     E1* |     E2* |    G12* |   v12* |    G23* |    K23* |\n"
            + "|      |   (GPa) |   (GPa) |   (GPa) |        |   (GPa) |   (GPa) |\n"
            + "+======+=========+=========+=========+========+=========+=========+\n"
            + "| 0.50 |  126.40 |    6.33 |    2.83 |   0.29 |    2.29 |    5.16 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.51 |  128.87 |    6.44 |    2.90 |   0.29 |    2.34 |    5.25 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.52 |  131.34 |    6.56 |    2.96 |   0.29 |    2.38 |    5.33 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
        )

    @pytest.fixture
    def invalid_properties_in_list_extra_length(self):
        """
        Provide arguments of elastic properties organized as a invalid list but number
        of elements are not equal to 2
        """
        return [
            [
                "Vf",
                "E1*\n(GPa)",
            ],
            [
                Decimal("0.400"),
                Decimal("101.680"),
            ],
            [
                Decimal("0.400"),
                Decimal("101.680"),
            ],
        ]

    @pytest.fixture
    def invalid_properties_in_list_elements_zero_length(self):
        """
        Provide arguments of elastic properties organized as a invalid list but elements
        are of zero length
        """
        return [
            [],
            [],
        ]

    @pytest.fixture
    def invalid_properties_in_list_elements_not_equal_length(self):
        """
        Provide arguments of elastic properties organized as a invalid list but elements
        are not equal length
        """
        return [
            [
                "Vf",
                "E1*\n(GPa)",
            ],
            [
                Decimal("0.400"),
            ],
        ]

    def test_print_tabulate_output_with_invalid_list(
        self,
        properties_in_list,
        properties_in_dict,
        invalid_properties_in_list_extra_length,
        invalid_properties_in_list_elements_zero_length,
        invalid_properties_in_list_elements_not_equal_length,
        none_arg,
    ):
        """
        Test output of ``_print_tabulate`` helper function with invalid arguments that
        raise either TypeError or ValueError
        """
        with pytest.raises(TypeError):
            _print_tabulate()  # n0 argument
        with pytest.raises(TypeError):
            _print_tabulate(none_arg, "keys")  # first argument is None
        with pytest.raises(TypeError):
            _print_tabulate(properties_in_list)  # second argument is missing
        with pytest.raises(TypeError):
            _print_tabulate(properties_in_list, none_arg)  # second argument is None
        with pytest.raises(TypeError):
            _print_tabulate(properties_in_dict, 2)  # second argument is not str object
        with pytest.raises(ValueError):
            _print_tabulate(
                properties_in_dict, "firstrow"
            )  # second argument is not 'keys' when first arg is dict object
        with pytest.raises(ValueError):
            _print_tabulate(
                invalid_properties_in_list_extra_length, "firstrow"
            )  # When first arg is list object but length not equal 2
        with pytest.raises(ValueError):
            _print_tabulate(
                invalid_properties_in_list_elements_zero_length, "firstrow"
            )  # When first arg is list object but element is zero length
        with pytest.raises(ValueError):
            _print_tabulate(
                invalid_properties_in_list_elements_not_equal_length, "firstrow"
            )  # When first arg is list object but elements are not equal length
        with pytest.raises(ValueError):
            _print_tabulate(
                properties_in_list, "keys"
            )  # When first arg is valid list object but second argument is not 'firstrow'

    def test_display_output_1(self, composite1, capsys):
        """
        Test output of ``display`` major function with valid arguments for full range of
        fiber volume fraction
        """
        display(composite1)
        captured = capsys.readouterr()
        assert captured.out == (
            "\n"
            + "[1] UD COMPOSITE: CARBON-EPOXY\n"
            + "\n"
            + "\n"
            + "A) Fiber material: Carbon\n"
            + "\n"
            + "+---------------+------------+--------------+-------------+--------------+-------------+----------------+\n"
            + "| Constituent   |      Axial |   Transverse |       Axial |   Transverse |       Major |   Plane-strain |\n"
            + "|               |    Young's |      Young's |       Shear |        Shear |   Poisson's |           Bulk |\n"
            + "|               |   Modulus, |     Modulus, |    Modulus, |     Modulus, |      Ratio, |       Modulus, |\n"
            + "|               |   E1 (GPa) |     E2 (GPa) |   G12 (GPa) |    G23 (GPa) |         v12 |      K23 (GPa) |\n"
            + "+===============+============+==============+=============+==============+=============+================+\n"
            + "| Carbon        |     250.00 |        25.00 |       20.00 |        10.00 |        0.28 |          17.02 |\n"
            + "+---------------+------------+--------------+-------------+--------------+-------------+----------------+\n"
            + "\n"
            + "B) Matrix material: Epoxy\n"
            + "\n"
            + "+---------------+------------+-------------+------------+-----------------+\n"
            + "| Constituent   |    Young's |   Poisson's |      Shear |    Plane-strain |\n"
            + "|               |   Modulus, |      Ratio, |   Modulus, |   Bulk Modulus, |\n"
            + "|               |    E (GPa) |           v |    G (GPa) |         K (GPa) |\n"
            + "+===============+============+=============+============+=================+\n"
            + "| Epoxy         |       2.80 |        0.30 |       1.08 |            2.69 |\n"
            + "+---------------+------------+-------------+------------+-----------------+\n"
            + "\n"
            + "C) Effective Elastic Moduli of Carbon-Epoxy\n"
            + "\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "|   Vf |     E1* |     E2* |    G12* |   v12* |    G23* |    K23* |\n"
            + "|      |   (GPa) |   (GPa) |   (GPa) |        |   (GPa) |   (GPa) |\n"
            + "+======+=========+=========+=========+========+=========+=========+\n"
            + "| 0.00 |    2.80 |    2.80 |    1.08 |   0.30 |    1.08 |    2.69 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.01 |    5.27 |    2.96 |    1.10 |   0.30 |    1.09 |    2.72 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.02 |    7.74 |    3.04 |    1.12 |   0.30 |    1.11 |    2.75 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.03 |   10.22 |    3.11 |    1.14 |   0.30 |    1.12 |    2.78 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.04 |   12.69 |    3.16 |    1.16 |   0.30 |    1.14 |    2.81 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.05 |   15.16 |    3.22 |    1.18 |   0.30 |    1.15 |    2.85 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.06 |   17.63 |    3.27 |    1.20 |   0.30 |    1.17 |    2.88 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.07 |   20.10 |    3.31 |    1.22 |   0.30 |    1.18 |    2.91 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.08 |   22.58 |    3.36 |    1.24 |   0.30 |    1.20 |    2.95 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.09 |   25.05 |    3.41 |    1.27 |   0.30 |    1.21 |    2.98 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.10 |   27.52 |    3.46 |    1.29 |   0.30 |    1.23 |    3.02 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.11 |   29.99 |    3.51 |    1.31 |   0.30 |    1.25 |    3.05 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.12 |   32.46 |    3.56 |    1.34 |   0.30 |    1.26 |    3.09 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.13 |   34.94 |    3.60 |    1.36 |   0.30 |    1.28 |    3.12 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.14 |   37.41 |    3.65 |    1.39 |   0.30 |    1.30 |    3.16 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.15 |   39.88 |    3.71 |    1.41 |   0.30 |    1.32 |    3.20 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.16 |   42.35 |    3.76 |    1.44 |   0.30 |    1.34 |    3.24 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.17 |   44.82 |    3.81 |    1.47 |   0.30 |    1.36 |    3.28 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.18 |   47.30 |    3.86 |    1.49 |   0.30 |    1.38 |    3.32 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.19 |   49.77 |    3.92 |    1.52 |   0.30 |    1.40 |    3.36 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.20 |   52.24 |    3.97 |    1.55 |   0.30 |    1.42 |    3.40 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.21 |   54.71 |    4.03 |    1.58 |   0.30 |    1.44 |    3.44 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.22 |   57.18 |    4.09 |    1.61 |   0.30 |    1.46 |    3.49 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.23 |   59.66 |    4.14 |    1.64 |   0.30 |    1.48 |    3.53 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.24 |   62.13 |    4.20 |    1.67 |   0.30 |    1.50 |    3.58 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.25 |   64.60 |    4.27 |    1.70 |   0.29 |    1.52 |    3.62 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.26 |   67.07 |    4.33 |    1.73 |   0.29 |    1.55 |    3.67 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.27 |   69.54 |    4.39 |    1.77 |   0.29 |    1.57 |    3.72 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.28 |   72.02 |    4.46 |    1.80 |   0.29 |    1.59 |    3.77 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.29 |   74.49 |    4.52 |    1.83 |   0.29 |    1.62 |    3.81 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.30 |   76.96 |    4.59 |    1.87 |   0.29 |    1.64 |    3.87 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.31 |   79.43 |    4.66 |    1.91 |   0.29 |    1.67 |    3.92 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.32 |   81.90 |    4.73 |    1.95 |   0.29 |    1.70 |    3.97 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.33 |   84.38 |    4.80 |    1.98 |   0.29 |    1.72 |    4.03 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.34 |   86.85 |    4.87 |    2.02 |   0.29 |    1.75 |    4.08 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.35 |   89.32 |    4.95 |    2.06 |   0.29 |    1.78 |    4.14 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.36 |   91.79 |    5.03 |    2.11 |   0.29 |    1.81 |    4.20 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.37 |   94.26 |    5.10 |    2.15 |   0.29 |    1.83 |    4.25 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.38 |   96.74 |    5.18 |    2.19 |   0.29 |    1.86 |    4.31 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.39 |   99.21 |    5.27 |    2.24 |   0.29 |    1.90 |    4.38 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.40 |  101.68 |    5.35 |    2.28 |   0.29 |    1.93 |    4.44 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.41 |  104.15 |    5.44 |    2.33 |   0.29 |    1.96 |    4.50 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.42 |  106.62 |    5.53 |    2.38 |   0.29 |    1.99 |    4.57 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.43 |  109.10 |    5.62 |    2.43 |   0.29 |    2.03 |    4.64 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.44 |  111.57 |    5.71 |    2.48 |   0.29 |    2.06 |    4.71 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.45 |  114.04 |    5.81 |    2.54 |   0.29 |    2.10 |    4.78 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.46 |  116.51 |    5.91 |    2.59 |   0.29 |    2.14 |    4.85 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.47 |  118.98 |    6.01 |    2.65 |   0.29 |    2.17 |    4.93 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.48 |  121.46 |    6.11 |    2.71 |   0.29 |    2.21 |    5.00 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.49 |  123.93 |    6.22 |    2.77 |   0.29 |    2.25 |    5.08 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.50 |  126.40 |    6.33 |    2.83 |   0.29 |    2.29 |    5.16 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.51 |  128.87 |    6.44 |    2.90 |   0.29 |    2.34 |    5.25 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.52 |  131.34 |    6.56 |    2.96 |   0.29 |    2.38 |    5.33 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.53 |  133.82 |    6.68 |    3.03 |   0.29 |    2.43 |    5.42 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.54 |  136.29 |    6.80 |    3.10 |   0.29 |    2.47 |    5.51 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.55 |  138.76 |    6.93 |    3.18 |   0.29 |    2.52 |    5.60 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.56 |  141.23 |    7.05 |    3.25 |   0.29 |    2.57 |    5.69 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.57 |  143.70 |    7.19 |    3.33 |   0.29 |    2.62 |    5.79 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.58 |  146.18 |    7.33 |    3.42 |   0.29 |    2.68 |    5.89 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.59 |  148.65 |    7.47 |    3.50 |   0.29 |    2.73 |    6.00 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.60 |  151.12 |    7.62 |    3.59 |   0.29 |    2.79 |    6.10 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.61 |  153.59 |    7.78 |    3.69 |   0.29 |    2.85 |    6.21 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.62 |  156.06 |    7.93 |    3.78 |   0.29 |    2.91 |    6.33 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.63 |  158.54 |    8.10 |    3.88 |   0.29 |    2.97 |    6.44 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.64 |  161.01 |    8.27 |    3.99 |   0.29 |    3.03 |    6.56 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.65 |  163.48 |    8.44 |    4.10 |   0.29 |    3.10 |    6.69 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.66 |  165.95 |    8.62 |    4.21 |   0.29 |    3.17 |    6.82 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.67 |  168.42 |    8.81 |    4.33 |   0.29 |    3.25 |    6.95 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.68 |  170.90 |    9.01 |    4.45 |   0.29 |    3.32 |    7.09 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.69 |  173.37 |    9.21 |    4.58 |   0.29 |    3.40 |    7.23 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.70 |  175.84 |    9.42 |    4.72 |   0.29 |    3.48 |    7.38 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.71 |  178.31 |    9.64 |    4.86 |   0.29 |    3.57 |    7.53 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.72 |  180.78 |    9.87 |    5.01 |   0.29 |    3.66 |    7.69 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.73 |  183.26 |   10.11 |    5.17 |   0.29 |    3.75 |    7.85 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.74 |  185.73 |   10.35 |    5.34 |   0.29 |    3.85 |    8.03 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.75 |  188.20 |   10.61 |    5.52 |   0.28 |    3.95 |    8.20 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.76 |  190.67 |   10.88 |    5.70 |   0.28 |    4.05 |    8.39 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.77 |  193.14 |   11.16 |    5.90 |   0.28 |    4.17 |    8.58 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.78 |  195.62 |   11.46 |    6.11 |   0.28 |    4.28 |    8.78 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.79 |  198.09 |   11.77 |    6.33 |   0.28 |    4.40 |    8.99 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.80 |  200.56 |   12.09 |    6.57 |   0.28 |    4.53 |    9.20 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.81 |  203.03 |   12.43 |    6.82 |   0.28 |    4.67 |    9.43 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.82 |  205.50 |   12.79 |    7.09 |   0.28 |    4.81 |    9.67 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.83 |  207.98 |   13.16 |    7.38 |   0.28 |    4.96 |    9.92 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.84 |  210.45 |   13.56 |    7.68 |   0.28 |    5.12 |   10.18 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.85 |  212.92 |   13.98 |    8.02 |   0.28 |    5.29 |   10.45 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.86 |  215.39 |   14.42 |    8.38 |   0.28 |    5.47 |   10.73 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.87 |  217.86 |   14.89 |    8.76 |   0.28 |    5.66 |   11.04 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.88 |  220.34 |   15.39 |    9.18 |   0.28 |    5.87 |   11.35 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.89 |  222.81 |   15.91 |    9.64 |   0.28 |    6.08 |   11.69 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.90 |  225.28 |   16.48 |   10.14 |   0.28 |    6.32 |   12.04 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.91 |  227.75 |   17.07 |   10.69 |   0.28 |    6.57 |   12.41 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.92 |  230.22 |   17.71 |   11.30 |   0.28 |    6.83 |   12.80 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.93 |  232.70 |   18.40 |   11.97 |   0.28 |    7.12 |   13.22 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.94 |  235.17 |   19.13 |   12.72 |   0.28 |    7.43 |   13.66 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.95 |  237.64 |   19.92 |   13.57 |   0.28 |    7.77 |   14.13 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.96 |  240.11 |   20.78 |   14.52 |   0.28 |    8.14 |   14.63 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.97 |  242.58 |   21.70 |   15.60 |   0.28 |    8.54 |   15.17 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.98 |  245.06 |   22.71 |   16.85 |   0.28 |    8.98 |   15.74 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.99 |  247.53 |   23.80 |   18.30 |   0.28 |    9.46 |   16.36 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 1.00 |  250.00 |   25.00 |   20.00 |   0.28 |   10.00 |   17.02 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "\n"
        )

    def test_display_output_2(self, composite2, capsys):
        """
        Test ``display`` major function with valid arguments for specific range of
        fiber volume fraction
        """
        display(composite2, 0.5, 0.55)
        captured = capsys.readouterr()
        assert captured.out == (
            "\n"
            + "[1] UD COMPOSITE: FIBERGLASS-EPOXY\n"
            + "\n"
            + "\n"
            + "A) Fiber material: Fiberglass\n"
            + "\n"
            + "+---------------+------------+-------------+------------+-----------------+\n"
            + "| Constituent   |    Young's |   Poisson's |      Shear |    Plane-strain |\n"
            + "|               |   Modulus, |      Ratio, |   Modulus, |   Bulk Modulus, |\n"
            + "|               |    E (GPa) |           v |    G (GPa) |         K (GPa) |\n"
            + "+===============+============+=============+============+=================+\n"
            + "| Fiberglass    |     120.00 |        0.29 |      46.51 |          110.74 |\n"
            + "+---------------+------------+-------------+------------+-----------------+\n"
            + "\n"
            + "B) Matrix material: Epoxy\n"
            + "\n"
            + "+---------------+------------+-------------+------------+-----------------+\n"
            + "| Constituent   |    Young's |   Poisson's |      Shear |    Plane-strain |\n"
            + "|               |   Modulus, |      Ratio, |   Modulus, |   Bulk Modulus, |\n"
            + "|               |    E (GPa) |           v |    G (GPa) |         K (GPa) |\n"
            + "+===============+============+=============+============+=================+\n"
            + "| Epoxy         |       2.80 |        0.30 |       1.08 |            2.69 |\n"
            + "+---------------+------------+-------------+------------+-----------------+\n"
            + "\n"
            + "C) Effective Elastic Moduli of Fiberglass-Epoxy\n"
            + "\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "|   Vf |     E1* |     E2* |    G12* |   v12* |    G23* |    K23* |\n"
            + "|      |   (GPa) |   (GPa) |   (GPa) |        |   (GPa) |   (GPa) |\n"
            + "+======+=========+=========+=========+========+=========+=========+\n"
            + "| 0.50 |   61.40 |    7.33 |    3.04 |   0.29 |    2.64 |    6.21 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.51 |   62.57 |    7.50 |    3.12 |   0.29 |    2.70 |    6.35 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.52 |   63.74 |    7.67 |    3.20 |   0.29 |    2.76 |    6.50 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.53 |   64.92 |    7.86 |    3.28 |   0.29 |    2.83 |    6.65 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.54 |   66.09 |    8.04 |    3.37 |   0.29 |    2.90 |    6.80 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "| 0.55 |   67.26 |    8.24 |    3.46 |   0.29 |    2.97 |    6.97 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "\n"
        )

    def test_display_output_3(self, composite3, capsys):
        """
        Test ``display`` major function with valid arguments for specific range of fiber
        volume fraction where the specified range has min and max value to be the same,
        which will be treated as a specific value of fiber volume fraction
        """
        display(composite3, 0.55, 0.55)
        captured = capsys.readouterr()
        assert captured.out == (
            "\n"
            + "[1] UD COMPOSITE: CARBON-GRAPHITE\n"
            + "\n"
            + "\n"
            + "A) Fiber material: Carbon\n"
            + "\n"
            + "+---------------+------------+--------------+-------------+--------------+-------------+----------------+\n"
            + "| Constituent   |      Axial |   Transverse |       Axial |   Transverse |       Major |   Plane-strain |\n"
            + "|               |    Young's |      Young's |       Shear |        Shear |   Poisson's |           Bulk |\n"
            + "|               |   Modulus, |     Modulus, |    Modulus, |     Modulus, |      Ratio, |       Modulus, |\n"
            + "|               |   E1 (GPa) |     E2 (GPa) |   G12 (GPa) |    G23 (GPa) |         v12 |      K23 (GPa) |\n"
            + "+===============+============+==============+=============+==============+=============+================+\n"
            + "| Carbon        |     250.00 |        25.00 |       20.00 |        10.00 |        0.28 |          17.02 |\n"
            + "+---------------+------------+--------------+-------------+--------------+-------------+----------------+\n"
            + "\n"
            + "B) Matrix material: Graphite\n"
            + "\n"
            + "+---------------+------------+--------------+-------------+--------------+-------------+----------------+\n"
            + "| Constituent   |      Axial |   Transverse |       Axial |   Transverse |       Major |   Plane-strain |\n"
            + "|               |    Young's |      Young's |       Shear |        Shear |   Poisson's |           Bulk |\n"
            + "|               |   Modulus, |     Modulus, |    Modulus, |     Modulus, |      Ratio, |       Modulus, |\n"
            + "|               |   E1 (GPa) |     E2 (GPa) |   G12 (GPa) |    G23 (GPa) |         v12 |      K23 (GPa) |\n"
            + "+===============+============+==============+=============+==============+=============+================+\n"
            + "| Graphite      |     180.00 |        20.00 |       15.00 |        10.00 |        0.29 |          10.19 |\n"
            + "+---------------+------------+--------------+-------------+--------------+-------------+----------------+\n"
            + "\n"
            + "C) Effective Elastic Moduli of Carbon-Graphite\n"
            + "\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "|   Vf |     E1* |     E2* |    G12* |   v12* |    G23* |    K23* |\n"
            + "|      |   (GPa) |   (GPa) |   (GPa) |        |   (GPa) |   (GPa) |\n"
            + "+======+=========+=========+=========+========+=========+=========+\n"
            + "| 0.55 |  218.50 |   22.75 |   17.56 |   0.28 |   10.00 |   13.45 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "\n"
        )

    def test_display_output_4(self, composite4, capsys):
        """
        Test ``display`` major function with valid arguments for specific value of fiber
        volume fraction
        """
        display(composite4, 0.6)
        captured = capsys.readouterr()
        assert captured.out == (
            "\n"
            + "[1] UD COMPOSITE: FIBERGLASS-GRAPHITE\n"
            + "\n"
            + "\n"
            + "A) Fiber material: Fiberglass\n"
            + "\n"
            + "+---------------+------------+-------------+------------+-----------------+\n"
            + "| Constituent   |    Young's |   Poisson's |      Shear |    Plane-strain |\n"
            + "|               |   Modulus, |      Ratio, |   Modulus, |   Bulk Modulus, |\n"
            + "|               |    E (GPa) |           v |    G (GPa) |         K (GPa) |\n"
            + "+===============+============+=============+============+=================+\n"
            + "| Fiberglass    |     120.00 |        0.29 |      46.51 |          110.74 |\n"
            + "+---------------+------------+-------------+------------+-----------------+\n"
            + "\n"
            + "B) Matrix material: Graphite\n"
            + "\n"
            + "+---------------+------------+--------------+-------------+--------------+-------------+----------------+\n"
            + "| Constituent   |      Axial |   Transverse |       Axial |   Transverse |       Major |   Plane-strain |\n"
            + "|               |    Young's |      Young's |       Shear |        Shear |   Poisson's |           Bulk |\n"
            + "|               |   Modulus, |     Modulus, |    Modulus, |     Modulus, |      Ratio, |       Modulus, |\n"
            + "|               |   E1 (GPa) |     E2 (GPa) |   G12 (GPa) |    G23 (GPa) |         v12 |      K23 (GPa) |\n"
            + "+===============+============+==============+=============+==============+=============+================+\n"
            + "| Graphite      |     180.00 |        20.00 |       15.00 |        10.00 |        0.29 |          10.19 |\n"
            + "+---------------+------------+--------------+-------------+--------------+-------------+----------------+\n"
            + "\n"
            + "C) Effective Elastic Moduli of Fiberglass-Graphite\n"
            + "\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "|   Vf |     E1* |     E2* |    G12* |   v12* |    G23* |    K23* |\n"
            + "|      |   (GPa) |   (GPa) |   (GPa) |        |   (GPa) |   (GPa) |\n"
            + "+======+=========+=========+=========+========+=========+=========+\n"
            + "| 0.60 |  144.00 |   47.55 |   28.31 |   0.29 |   20.47 |   30.35 |\n"
            + "+------+---------+---------+---------+--------+---------+---------+\n"
            + "\n"
        )

    def test_display_output_with_invalid_inputs_1(self, carbon, none_arg):
        """
        Test ``display`` function with intention to display effective elastic properties
        of UD composite versus full range of fiber volume fraction with invalid
        arguments that raise either TypeError
        """
        with pytest.raises(TypeError):
            display()  # no argument
        with pytest.raises(TypeError):
            display(none_arg)  # argument is None
        with pytest.raises(TypeError):
            display(carbon)  # argument is not HT object

    def test_display_output_with_invalid_inputs_2(self, composite1):
        """
        Test ``display`` function with intention to display effective elastic properties
        of UD composite versus specific value of fiber volume fraction with invalid
        arguments that raise either TypeError or ValueError
        """
        with pytest.raises(TypeError):
            display(composite1, "0.5")  # aecond argument is not int
        with pytest.raises(ValueError):
            display(composite1, -1)  # second argument is less than 0
        with pytest.raises(ValueError):
            display(composite1, 1.01)  # second argument is greater than 1

    def test_display_output_with_invalid_inputs_3(self, composite1, none_arg):
        """
        Test ``display`` function with intention to display effective elastic properties
        of UD composite versus specific range of fiber volume fraction with invalid
        arguments that raise either TypeError or ValueError
        """
        with pytest.raises(TypeError):
            display(composite1, 0.5, "0.55")  # third argument is not int
        with pytest.raises(ValueError):
            display(composite1, 0.5, -0.55)  # third argument is less than 0
        with pytest.raises(ValueError):
            display(composite1, 0.5, 0.4)  # second argument greater than third
        with pytest.raises(ValueError):
            display(
                composite1, 0.5, 1.01
            )  # Third argument is greater than 1 or vice versa
        with pytest.raises(ValueError):
            display(
                composite1, none_arg, 0.5
            )  # Second argument is None while third is not


class Test_Save:
    """
    Test suite for ``save`` major function that saves information about UD
    composite's constituent elastic moduli and composite's effective elastic moduli to
    csv format files in a default name "csv" folder, which can be redefined.

    This test suite contains all unit tests for every helper functions that make up the
    ``save`` function. Once all helper functions are tested, and then ``save`` major
    function is unit-tested as well.
    """

    @pytest.fixture
    def fiberglass(self):
        """
        Provide arguments on fiber isotropic material called fiberglass
        """
        # Isotropic class and its methods have been fully unit-tested and all passed as done above
        return Isotropic(name="Fiberglass", youngs_modulus=120, poissons_ratio=0.29)

    @pytest.fixture
    def carbon(self):
        """
        Provide arguments for transversely isotropic fiber called carbon
        """
        # Transtropic class and all its methods are assumed to have been fully unit-tested and all passed
        return Transtropic(
            name="Carbon",
            axial_youngs_modulus=250,
            transverse_youngs_modulus=25,
            axial_shear_modulus=20,
            transverse_shear_modulus=10,
            major_poissons_ratio=0.28,
        )

    @pytest.fixture
    def epoxy(self):
        """
        Provide arguments for isotropic matrix material called epoxy
        """
        return Isotropic(name="Epoxy", youngs_modulus=2.8, poissons_ratio=0.3)

    @pytest.fixture
    def graphite(self):
        """
        Provide arguments for transversely isotropic matrix material called graphite
        """
        return Transtropic(
            name="Graphite",
            axial_youngs_modulus=180,
            transverse_youngs_modulus=20,
            axial_shear_modulus=15,
            transverse_shear_modulus=10,
            major_poissons_ratio=0.29,
        )

    @pytest.fixture
    def composite1(self, carbon, epoxy):
        """
        Provide arguments for UD composite with carbon fiber as transversely isotropic
        material and epoxy matrix as isotropic material
        """
        # HT class and all its methods are assumed to have been fully unit-tested and all passed
        return HT(fiber=carbon, matrix=epoxy)

    @pytest.fixture
    def composite2(self, fiberglass, epoxy):
        """
        Provide arguments for UD composite with both fiberglass fiber and epoxy matrix
        as isotropic materials
        """
        return HT(fiber=fiberglass, matrix=epoxy)

    @pytest.fixture
    def composite3(self, carbon, graphite):
        """
        Provide arguments for UD composite with both carbon fiber and graphite matrix as
        transversely isotropic materials
        """
        return HT(fiber=carbon, matrix=graphite)

    @pytest.fixture
    def composite4(self, fiberglass, graphite):
        """
        Provide arguments for UD composite with fiberglass fiber as isotropic material
        and graphite matrix as transversely isotropic material
        """
        return HT(fiber=fiberglass, matrix=graphite)

    @pytest.fixture
    def none_arg(self):
        """
        Provide argument with None
        """
        return None

    def test_get_phase_elastic_moduli_and_filename_outputs(
            self, composite1, composite2, composite3, composite4
    ):
        """
        Test output of ``_get_phase_elastic_moduli_and_filename`` helper function with
        valid arguments, i.e. 4 different UD composites having different types of
        constituent materials
        """
        result1 = _get_phase_elastic_moduli_and_filename(composite1)
        assert result1 == [
            (
                [
                    {
                        "Constituent": "Carbon",
                        "Axial\nYoung's\nModulus,\nE1 (GPa)": Decimal("250.000"),
                        "Transverse\nYoung's\nModulus,\nE2 (GPa)": Decimal("25.000"),
                        "Axial\nShear\nModulus,\nG12 (GPa)": Decimal("20.000"),
                        "Transverse\nShear\nModulus,\nG23 (GPa)": Decimal("10.000"),
                        "Major\nPoisson's\nRatio,\nv12": Decimal("0.280"),
                        "Plane-strain\nBulk\nModulus,\nK23 (GPa)": Decimal("17.023"),
                    }
                ],
                "Carbon-Epoxy_fiber_tra_moduli.csv",
            ),
            (
                [
                    {
                        "Constituent": "Epoxy",
                        "Young's\nModulus,\nE (GPa)": Decimal("2.800"),
                        "Poisson's\nRatio,\nv": Decimal("0.300"),
                        "Shear\nModulus,\nG (GPa)": Decimal("1.077"),
                        "Plane-strain\nBulk Modulus,\nK (GPa)": Decimal("2.692"),
                    }
                ],
                "Carbon-Epoxy_matrix_iso_moduli.csv",
            ),
        ]
        result2 = _get_phase_elastic_moduli_and_filename(composite2)
        assert result2 == (
            [
                {
                    "Constituent": "Fiberglass",
                    "Young's\nModulus,\nE (GPa)": Decimal("120.000"),
                    "Poisson's\nRatio,\nv": Decimal("0.290"),
                    "Shear\nModulus,\nG (GPa)": Decimal("46.512"),
                    "Plane-strain\nBulk Modulus,\nK (GPa)": Decimal("110.742"),
                },
                {
                    "Constituent": "Epoxy",
                    "Young's\nModulus,\nE (GPa)": Decimal("2.800"),
                    "Poisson's\nRatio,\nv": Decimal("0.300"),
                    "Shear\nModulus,\nG (GPa)": Decimal("1.077"),
                    "Plane-strain\nBulk Modulus,\nK (GPa)": Decimal("2.692"),
                },
            ],
            "Fiberglass-Epoxy_phases_iso_moduli.csv",
        )
        result3 = _get_phase_elastic_moduli_and_filename(composite3)
        assert result3 == (
            [
                {
                    "Constituent": "Carbon",
                    "Axial\nYoung's\nModulus,\nE1 (GPa)": Decimal("250.000"),
                    "Transverse\nYoung's\nModulus,\nE2 (GPa)": Decimal("25.000"),
                    "Axial\nShear\nModulus,\nG12 (GPa)": Decimal("20.000"),
                    "Transverse\nShear\nModulus,\nG23 (GPa)": Decimal("10.000"),
                    "Major\nPoisson's\nRatio,\nv12": Decimal("0.280"),
                    "Plane-strain\nBulk\nModulus,\nK23 (GPa)": Decimal("17.023"),
                },
                {
                    "Constituent": "Graphite",
                    "Axial\nYoung's\nModulus,\nE1 (GPa)": Decimal("180.000"),
                    "Transverse\nYoung's\nModulus,\nE2 (GPa)": Decimal("20.000"),
                    "Axial\nShear\nModulus,\nG12 (GPa)": Decimal("15.000"),
                    "Transverse\nShear\nModulus,\nG23 (GPa)": Decimal("10.000"),
                    "Major\nPoisson's\nRatio,\nv12": Decimal("0.290"),
                    "Plane-strain\nBulk\nModulus,\nK23 (GPa)": Decimal("10.190"),
                },
            ],
            "Carbon-Graphite_phases_tra_moduli.csv",
        )
        result4 = _get_phase_elastic_moduli_and_filename(composite4)
        assert result4 == [
            (
                [
                    {
                        "Constituent": "Fiberglass",
                        "Young's\nModulus,\nE (GPa)": Decimal("120.000"),
                        "Poisson's\nRatio,\nv": Decimal("0.290"),
                        "Shear\nModulus,\nG (GPa)": Decimal("46.512"),
                        "Plane-strain\nBulk Modulus,\nK (GPa)": Decimal("110.742"),
                    }
                ],
                "Fiberglass-Graphite_fiber_iso_moduli.csv",
            ),
            (
                [
                    {
                        "Constituent": "Graphite",
                        "Axial\nYoung's\nModulus,\nE1 (GPa)": Decimal("180.000"),
                        "Transverse\nYoung's\nModulus,\nE2 (GPa)": Decimal("20.000"),
                        "Axial\nShear\nModulus,\nG12 (GPa)": Decimal("15.000"),
                        "Transverse\nShear\nModulus,\nG23 (GPa)": Decimal("10.000"),
                        "Major\nPoisson's\nRatio,\nv12": Decimal("0.290"),
                        "Plane-strain\nBulk\nModulus,\nK23 (GPa)": Decimal("10.190"),
                    }
                ],
                "Fiberglass-Graphite_matrix_tra_moduli.csv",
            ),
        ]

    def test_get_phase_elastic_moduli_and_filename_output_with_invalid_inputs(
            self, carbon, none_arg
    ):
        """
        Test output of ``_get_phase_elastic_moduli_and_filename`` helper function with
        invalid arguments that raise TypeError
        """
        with pytest.raises(TypeError):
            _get_phase_elastic_moduli_and_filename()  # No argument
        with pytest.raises(TypeError):
            _get_phase_elastic_moduli_and_filename(none_arg)  # Argument is None
        with pytest.raises(TypeError):
            _get_phase_elastic_moduli_and_filename(carbon)  # Argument is not HT object

    def test_get_effective_elastic_moduli_and_filename_output(
            self, composite1, composite2, composite3, composite4
    ):
        """
        Test output of ``_get_effective_elastic_moduli_and_filename`` helper function
        with valid arguments, i.e. 4 different UD composites having different types of
        constituent materials
        """
        result1 = _get_effective_elastic_moduli_and_filename(composite1)
        assert result1 == (
            [
                {
                    "Vf": Decimal("0"),
                    "E1*\n(GPa)": Decimal("2.800"),
                    "E2*\n(GPa)": Decimal("2.800"),
                    "G12*\n(GPa)": Decimal("1.077"),
                    "v12*": Decimal("0.3000"),
                    "G23*\n(GPa)": Decimal("1.077"),
                    "K23*\n(GPa)": Decimal("2.692"),
                },
                {
                    "Vf": Decimal("0.01"),
                    "E1*\n(GPa)": Decimal("5.272"),
                    "E2*\n(GPa)": Decimal("2.958"),
                    "G12*\n(GPa)": Decimal("1.097"),
                    "v12*": Decimal("0.2998"),
                    "G23*\n(GPa)": Decimal("1.091"),
                    "K23*\n(GPa)": Decimal("2.722"),
                },
                {
                    "Vf": Decimal("0.02"),
                    "E1*\n(GPa)": Decimal("7.744"),
                    "E2*\n(GPa)": Decimal("3.045"),
                    "G12*\n(GPa)": Decimal("1.116"),
                    "v12*": Decimal("0.2996"),
                    "G23*\n(GPa)": Decimal("1.106"),
                    "K23*\n(GPa)": Decimal("2.753"),
                },
                {
                    "Vf": Decimal("0.03"),
                    "E1*\n(GPa)": Decimal("10.216"),
                    "E2*\n(GPa)": Decimal("3.108"),
                    "G12*\n(GPa)": Decimal("1.137"),
                    "v12*": Decimal("0.2994"),
                    "G23*\n(GPa)": Decimal("1.120"),
                    "K23*\n(GPa)": Decimal("2.784"),
                },
                {
                    "Vf": Decimal("0.04"),
                    "E1*\n(GPa)": Decimal("12.688"),
                    "E2*\n(GPa)": Decimal("3.163"),
                    "G12*\n(GPa)": Decimal("1.157"),
                    "v12*": Decimal("0.2992"),
                    "G23*\n(GPa)": Decimal("1.135"),
                    "K23*\n(GPa)": Decimal("2.815"),
                },
                {
                    "Vf": Decimal("0.05"),
                    "E1*\n(GPa)": Decimal("15.160"),
                    "E2*\n(GPa)": Decimal("3.216"),
                    "G12*\n(GPa)": Decimal("1.178"),
                    "v12*": Decimal("0.2990"),
                    "G23*\n(GPa)": Decimal("1.151"),
                    "K23*\n(GPa)": Decimal("2.847"),
                },
                {
                    "Vf": Decimal("0.06"),
                    "E1*\n(GPa)": Decimal("17.632"),
                    "E2*\n(GPa)": Decimal("3.265"),
                    "G12*\n(GPa)": Decimal("1.200"),
                    "v12*": Decimal("0.2988"),
                    "G23*\n(GPa)": Decimal("1.166"),
                    "K23*\n(GPa)": Decimal("2.880"),
                },
                {
                    "Vf": Decimal("0.07"),
                    "E1*\n(GPa)": Decimal("20.104"),
                    "E2*\n(GPa)": Decimal("3.314"),
                    "G12*\n(GPa)": Decimal("1.221"),
                    "v12*": Decimal("0.2986"),
                    "G23*\n(GPa)": Decimal("1.182"),
                    "K23*\n(GPa)": Decimal("2.913"),
                },
                {
                    "Vf": Decimal("0.08"),
                    "E1*\n(GPa)": Decimal("22.576"),
                    "E2*\n(GPa)": Decimal("3.362"),
                    "G12*\n(GPa)": Decimal("1.244"),
                    "v12*": Decimal("0.2984"),
                    "G23*\n(GPa)": Decimal("1.198"),
                    "K23*\n(GPa)": Decimal("2.947"),
                },
                {
                    "Vf": Decimal("0.09"),
                    "E1*\n(GPa)": Decimal("25.048"),
                    "E2*\n(GPa)": Decimal("3.409"),
                    "G12*\n(GPa)": Decimal("1.266"),
                    "v12*": Decimal("0.2982"),
                    "G23*\n(GPa)": Decimal("1.214"),
                    "K23*\n(GPa)": Decimal("2.981"),
                },
                {
                    "Vf": Decimal("0.1"),
                    "E1*\n(GPa)": Decimal("27.520"),
                    "E2*\n(GPa)": Decimal("3.458"),
                    "G12*\n(GPa)": Decimal("1.289"),
                    "v12*": Decimal("0.2980"),
                    "G23*\n(GPa)": Decimal("1.231"),
                    "K23*\n(GPa)": Decimal("3.016"),
                },
                {
                    "Vf": Decimal("0.11"),
                    "E1*\n(GPa)": Decimal("29.992"),
                    "E2*\n(GPa)": Decimal("3.506"),
                    "G12*\n(GPa)": Decimal("1.313"),
                    "v12*": Decimal("0.2978"),
                    "G23*\n(GPa)": Decimal("1.248"),
                    "K23*\n(GPa)": Decimal("3.052"),
                },
                {
                    "Vf": Decimal("0.12"),
                    "E1*\n(GPa)": Decimal("32.464"),
                    "E2*\n(GPa)": Decimal("3.555"),
                    "G12*\n(GPa)": Decimal("1.337"),
                    "v12*": Decimal("0.2976"),
                    "G23*\n(GPa)": Decimal("1.265"),
                    "K23*\n(GPa)": Decimal("3.088"),
                },
                {
                    "Vf": Decimal("0.13"),
                    "E1*\n(GPa)": Decimal("34.936"),
                    "E2*\n(GPa)": Decimal("3.605"),
                    "G12*\n(GPa)": Decimal("1.362"),
                    "v12*": Decimal("0.2974"),
                    "G23*\n(GPa)": Decimal("1.283"),
                    "K23*\n(GPa)": Decimal("3.124"),
                },
                {
                    "Vf": Decimal("0.14"),
                    "E1*\n(GPa)": Decimal("37.408"),
                    "E2*\n(GPa)": Decimal("3.655"),
                    "G12*\n(GPa)": Decimal("1.387"),
                    "v12*": Decimal("0.2972"),
                    "G23*\n(GPa)": Decimal("1.301"),
                    "K23*\n(GPa)": Decimal("3.162"),
                },
                {
                    "Vf": Decimal("0.15"),
                    "E1*\n(GPa)": Decimal("39.880"),
                    "E2*\n(GPa)": Decimal("3.705"),
                    "G12*\n(GPa)": Decimal("1.412"),
                    "v12*": Decimal("0.2970"),
                    "G23*\n(GPa)": Decimal("1.319"),
                    "K23*\n(GPa)": Decimal("3.200"),
                },
                {
                    "Vf": Decimal("0.16"),
                    "E1*\n(GPa)": Decimal("42.352"),
                    "E2*\n(GPa)": Decimal("3.758"),
                    "G12*\n(GPa)": Decimal("1.438"),
                    "v12*": Decimal("0.2968"),
                    "G23*\n(GPa)": Decimal("1.338"),
                    "K23*\n(GPa)": Decimal("3.239"),
                },
                {
                    "Vf": Decimal("0.17"),
                    "E1*\n(GPa)": Decimal("44.824"),
                    "E2*\n(GPa)": Decimal("3.810"),
                    "G12*\n(GPa)": Decimal("1.465"),
                    "v12*": Decimal("0.2966"),
                    "G23*\n(GPa)": Decimal("1.357"),
                    "K23*\n(GPa)": Decimal("3.278"),
                },
                {
                    "Vf": Decimal("0.18"),
                    "E1*\n(GPa)": Decimal("47.296"),
                    "E2*\n(GPa)": Decimal("3.863"),
                    "G12*\n(GPa)": Decimal("1.492"),
                    "v12*": Decimal("0.2964"),
                    "G23*\n(GPa)": Decimal("1.376"),
                    "K23*\n(GPa)": Decimal("3.318"),
                },
                {
                    "Vf": Decimal("0.19"),
                    "E1*\n(GPa)": Decimal("49.768"),
                    "E2*\n(GPa)": Decimal("3.917"),
                    "G12*\n(GPa)": Decimal("1.520"),
                    "v12*": Decimal("0.2962"),
                    "G23*\n(GPa)": Decimal("1.396"),
                    "K23*\n(GPa)": Decimal("3.359"),
                },
                {
                    "Vf": Decimal("0.2"),
                    "E1*\n(GPa)": Decimal("52.240"),
                    "E2*\n(GPa)": Decimal("3.972"),
                    "G12*\n(GPa)": Decimal("1.548"),
                    "v12*": Decimal("0.2960"),
                    "G23*\n(GPa)": Decimal("1.416"),
                    "K23*\n(GPa)": Decimal("3.401"),
                },
                {
                    "Vf": Decimal("0.21"),
                    "E1*\n(GPa)": Decimal("54.712"),
                    "E2*\n(GPa)": Decimal("4.030"),
                    "G12*\n(GPa)": Decimal("1.577"),
                    "v12*": Decimal("0.2958"),
                    "G23*\n(GPa)": Decimal("1.437"),
                    "K23*\n(GPa)": Decimal("3.444"),
                },
                {
                    "Vf": Decimal("0.22"),
                    "E1*\n(GPa)": Decimal("57.184"),
                    "E2*\n(GPa)": Decimal("4.087"),
                    "G12*\n(GPa)": Decimal("1.607"),
                    "v12*": Decimal("0.2956"),
                    "G23*\n(GPa)": Decimal("1.458"),
                    "K23*\n(GPa)": Decimal("3.487"),
                },
                {
                    "Vf": Decimal("0.23"),
                    "E1*\n(GPa)": Decimal("59.656"),
                    "E2*\n(GPa)": Decimal("4.144"),
                    "G12*\n(GPa)": Decimal("1.638"),
                    "v12*": Decimal("0.2954"),
                    "G23*\n(GPa)": Decimal("1.479"),
                    "K23*\n(GPa)": Decimal("3.531"),
                },
                {
                    "Vf": Decimal("0.24"),
                    "E1*\n(GPa)": Decimal("62.128"),
                    "E2*\n(GPa)": Decimal("4.204"),
                    "G12*\n(GPa)": Decimal("1.669"),
                    "v12*": Decimal("0.2952"),
                    "G23*\n(GPa)": Decimal("1.501"),
                    "K23*\n(GPa)": Decimal("3.576"),
                },
                {
                    "Vf": Decimal("0.25"),
                    "E1*\n(GPa)": Decimal("64.600"),
                    "E2*\n(GPa)": Decimal("4.266"),
                    "G12*\n(GPa)": Decimal("1.700"),
                    "v12*": Decimal("0.2950"),
                    "G23*\n(GPa)": Decimal("1.524"),
                    "K23*\n(GPa)": Decimal("3.622"),
                },
                {
                    "Vf": Decimal("0.26"),
                    "E1*\n(GPa)": Decimal("67.072"),
                    "E2*\n(GPa)": Decimal("4.326"),
                    "G12*\n(GPa)": Decimal("1.733"),
                    "v12*": Decimal("0.2948"),
                    "G23*\n(GPa)": Decimal("1.546"),
                    "K23*\n(GPa)": Decimal("3.669"),
                },
                {
                    "Vf": Decimal("0.27"),
                    "E1*\n(GPa)": Decimal("69.544"),
                    "E2*\n(GPa)": Decimal("4.391"),
                    "G12*\n(GPa)": Decimal("1.766"),
                    "v12*": Decimal("0.2946"),
                    "G23*\n(GPa)": Decimal("1.570"),
                    "K23*\n(GPa)": Decimal("3.717"),
                },
                {
                    "Vf": Decimal("0.28"),
                    "E1*\n(GPa)": Decimal("72.016"),
                    "E2*\n(GPa)": Decimal("4.456"),
                    "G12*\n(GPa)": Decimal("1.800"),
                    "v12*": Decimal("0.2944"),
                    "G23*\n(GPa)": Decimal("1.594"),
                    "K23*\n(GPa)": Decimal("3.766"),
                },
                {
                    "Vf": Decimal("0.29"),
                    "E1*\n(GPa)": Decimal("74.488"),
                    "E2*\n(GPa)": Decimal("4.521"),
                    "G12*\n(GPa)": Decimal("1.835"),
                    "v12*": Decimal("0.2942"),
                    "G23*\n(GPa)": Decimal("1.618"),
                    "K23*\n(GPa)": Decimal("3.815"),
                },
                {
                    "Vf": Decimal("0.3"),
                    "E1*\n(GPa)": Decimal("76.960"),
                    "E2*\n(GPa)": Decimal("4.588"),
                    "G12*\n(GPa)": Decimal("1.871"),
                    "v12*": Decimal("0.2940"),
                    "G23*\n(GPa)": Decimal("1.643"),
                    "K23*\n(GPa)": Decimal("3.866"),
                },
                {
                    "Vf": Decimal("0.31"),
                    "E1*\n(GPa)": Decimal("79.432"),
                    "E2*\n(GPa)": Decimal("4.658"),
                    "G12*\n(GPa)": Decimal("1.908"),
                    "v12*": Decimal("0.2938"),
                    "G23*\n(GPa)": Decimal("1.669"),
                    "K23*\n(GPa)": Decimal("3.918"),
                },
                {
                    "Vf": Decimal("0.32"),
                    "E1*\n(GPa)": Decimal("81.904"),
                    "E2*\n(GPa)": Decimal("4.728"),
                    "G12*\n(GPa)": Decimal("1.945"),
                    "v12*": Decimal("0.2936"),
                    "G23*\n(GPa)": Decimal("1.695"),
                    "K23*\n(GPa)": Decimal("3.971"),
                },
                {
                    "Vf": Decimal("0.33"),
                    "E1*\n(GPa)": Decimal("84.376"),
                    "E2*\n(GPa)": Decimal("4.800"),
                    "G12*\n(GPa)": Decimal("1.984"),
                    "v12*": Decimal("0.2934"),
                    "G23*\n(GPa)": Decimal("1.722"),
                    "K23*\n(GPa)": Decimal("4.025"),
                },
                {
                    "Vf": Decimal("0.34"),
                    "E1*\n(GPa)": Decimal("86.848"),
                    "E2*\n(GPa)": Decimal("4.873"),
                    "G12*\n(GPa)": Decimal("2.023"),
                    "v12*": Decimal("0.2932"),
                    "G23*\n(GPa)": Decimal("1.749"),
                    "K23*\n(GPa)": Decimal("4.080"),
                },
                {
                    "Vf": Decimal("0.35"),
                    "E1*\n(GPa)": Decimal("89.320"),
                    "E2*\n(GPa)": Decimal("4.949"),
                    "G12*\n(GPa)": Decimal("2.064"),
                    "v12*": Decimal("0.2930"),
                    "G23*\n(GPa)": Decimal("1.777"),
                    "K23*\n(GPa)": Decimal("4.137"),
                },
                {
                    "Vf": Decimal("0.36"),
                    "E1*\n(GPa)": Decimal("91.792"),
                    "E2*\n(GPa)": Decimal("5.026"),
                    "G12*\n(GPa)": Decimal("2.106"),
                    "v12*": Decimal("0.2928"),
                    "G23*\n(GPa)": Decimal("1.806"),
                    "K23*\n(GPa)": Decimal("4.195"),
                },
                {
                    "Vf": Decimal("0.37"),
                    "E1*\n(GPa)": Decimal("94.264"),
                    "E2*\n(GPa)": Decimal("5.104"),
                    "G12*\n(GPa)": Decimal("2.148"),
                    "v12*": Decimal("0.2926"),
                    "G23*\n(GPa)": Decimal("1.835"),
                    "K23*\n(GPa)": Decimal("4.254"),
                },
                {
                    "Vf": Decimal("0.38"),
                    "E1*\n(GPa)": Decimal("96.736"),
                    "E2*\n(GPa)": Decimal("5.184"),
                    "G12*\n(GPa)": Decimal("2.192"),
                    "v12*": Decimal("0.2924"),
                    "G23*\n(GPa)": Decimal("1.865"),
                    "K23*\n(GPa)": Decimal("4.314"),
                },
                {
                    "Vf": Decimal("0.39"),
                    "E1*\n(GPa)": Decimal("99.208"),
                    "E2*\n(GPa)": Decimal("5.267"),
                    "G12*\n(GPa)": Decimal("2.238"),
                    "v12*": Decimal("0.2922"),
                    "G23*\n(GPa)": Decimal("1.896"),
                    "K23*\n(GPa)": Decimal("4.376"),
                },
                {
                    "Vf": Decimal("0.4"),
                    "E1*\n(GPa)": Decimal("101.680"),
                    "E2*\n(GPa)": Decimal("5.353"),
                    "G12*\n(GPa)": Decimal("2.284"),
                    "v12*": Decimal("0.2920"),
                    "G23*\n(GPa)": Decimal("1.928"),
                    "K23*\n(GPa)": Decimal("4.439"),
                },
                {
                    "Vf": Decimal("0.41"),
                    "E1*\n(GPa)": Decimal("104.152"),
                    "E2*\n(GPa)": Decimal("5.438"),
                    "G12*\n(GPa)": Decimal("2.332"),
                    "v12*": Decimal("0.2918"),
                    "G23*\n(GPa)": Decimal("1.960"),
                    "K23*\n(GPa)": Decimal("4.504"),
                },
                {
                    "Vf": Decimal("0.42"),
                    "E1*\n(GPa)": Decimal("106.624"),
                    "E2*\n(GPa)": Decimal("5.527"),
                    "G12*\n(GPa)": Decimal("2.381"),
                    "v12*": Decimal("0.2916"),
                    "G23*\n(GPa)": Decimal("1.993"),
                    "K23*\n(GPa)": Decimal("4.570"),
                },
                {
                    "Vf": Decimal("0.43"),
                    "E1*\n(GPa)": Decimal("109.096"),
                    "E2*\n(GPa)": Decimal("5.619"),
                    "G12*\n(GPa)": Decimal("2.431"),
                    "v12*": Decimal("0.2914"),
                    "G23*\n(GPa)": Decimal("2.028"),
                    "K23*\n(GPa)": Decimal("4.638"),
                },
                {
                    "Vf": Decimal("0.44"),
                    "E1*\n(GPa)": Decimal("111.568"),
                    "E2*\n(GPa)": Decimal("5.712"),
                    "G12*\n(GPa)": Decimal("2.484"),
                    "v12*": Decimal("0.2912"),
                    "G23*\n(GPa)": Decimal("2.063"),
                    "K23*\n(GPa)": Decimal("4.707"),
                },
                {
                    "Vf": Decimal("0.45"),
                    "E1*\n(GPa)": Decimal("114.040"),
                    "E2*\n(GPa)": Decimal("5.808"),
                    "G12*\n(GPa)": Decimal("2.537"),
                    "v12*": Decimal("0.2910"),
                    "G23*\n(GPa)": Decimal("2.099"),
                    "K23*\n(GPa)": Decimal("4.778"),
                },
                {
                    "Vf": Decimal("0.46"),
                    "E1*\n(GPa)": Decimal("116.512"),
                    "E2*\n(GPa)": Decimal("5.907"),
                    "G12*\n(GPa)": Decimal("2.592"),
                    "v12*": Decimal("0.2908"),
                    "G23*\n(GPa)": Decimal("2.136"),
                    "K23*\n(GPa)": Decimal("4.851"),
                },
                {
                    "Vf": Decimal("0.47"),
                    "E1*\n(GPa)": Decimal("118.984"),
                    "E2*\n(GPa)": Decimal("6.008"),
                    "G12*\n(GPa)": Decimal("2.649"),
                    "v12*": Decimal("0.2906"),
                    "G23*\n(GPa)": Decimal("2.174"),
                    "K23*\n(GPa)": Decimal("4.926"),
                },
                {
                    "Vf": Decimal("0.48"),
                    "E1*\n(GPa)": Decimal("121.456"),
                    "E2*\n(GPa)": Decimal("6.111"),
                    "G12*\n(GPa)": Decimal("2.708"),
                    "v12*": Decimal("0.2904"),
                    "G23*\n(GPa)": Decimal("2.213"),
                    "K23*\n(GPa)": Decimal("5.003"),
                },
                {
                    "Vf": Decimal("0.49"),
                    "E1*\n(GPa)": Decimal("123.928"),
                    "E2*\n(GPa)": Decimal("6.217"),
                    "G12*\n(GPa)": Decimal("2.769"),
                    "v12*": Decimal("0.2902"),
                    "G23*\n(GPa)": Decimal("2.253"),
                    "K23*\n(GPa)": Decimal("5.081"),
                },
                {
                    "Vf": Decimal("0.5"),
                    "E1*\n(GPa)": Decimal("126.400"),
                    "E2*\n(GPa)": Decimal("6.328"),
                    "G12*\n(GPa)": Decimal("2.832"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("2.295"),
                    "K23*\n(GPa)": Decimal("5.162"),
                },
                {
                    "Vf": Decimal("0.51"),
                    "E1*\n(GPa)": Decimal("128.872"),
                    "E2*\n(GPa)": Decimal("6.441"),
                    "G12*\n(GPa)": Decimal("2.896"),
                    "v12*": Decimal("0.2898"),
                    "G23*\n(GPa)": Decimal("2.338"),
                    "K23*\n(GPa)": Decimal("5.245"),
                },
                {
                    "Vf": Decimal("0.52"),
                    "E1*\n(GPa)": Decimal("131.344"),
                    "E2*\n(GPa)": Decimal("6.558"),
                    "G12*\n(GPa)": Decimal("2.963"),
                    "v12*": Decimal("0.2896"),
                    "G23*\n(GPa)": Decimal("2.382"),
                    "K23*\n(GPa)": Decimal("5.330"),
                },
                {
                    "Vf": Decimal("0.53"),
                    "E1*\n(GPa)": Decimal("133.816"),
                    "E2*\n(GPa)": Decimal("6.676"),
                    "G12*\n(GPa)": Decimal("3.032"),
                    "v12*": Decimal("0.2894"),
                    "G23*\n(GPa)": Decimal("2.427"),
                    "K23*\n(GPa)": Decimal("5.417"),
                },
                {
                    "Vf": Decimal("0.54"),
                    "E1*\n(GPa)": Decimal("136.288"),
                    "E2*\n(GPa)": Decimal("6.800"),
                    "G12*\n(GPa)": Decimal("3.104"),
                    "v12*": Decimal("0.2892"),
                    "G23*\n(GPa)": Decimal("2.474"),
                    "K23*\n(GPa)": Decimal("5.507"),
                },
                {
                    "Vf": Decimal("0.55"),
                    "E1*\n(GPa)": Decimal("138.760"),
                    "E2*\n(GPa)": Decimal("6.926"),
                    "G12*\n(GPa)": Decimal("3.178"),
                    "v12*": Decimal("0.2890"),
                    "G23*\n(GPa)": Decimal("2.522"),
                    "K23*\n(GPa)": Decimal("5.599"),
                },
                {
                    "Vf": Decimal("0.56"),
                    "E1*\n(GPa)": Decimal("141.232"),
                    "E2*\n(GPa)": Decimal("7.055"),
                    "G12*\n(GPa)": Decimal("3.255"),
                    "v12*": Decimal("0.2888"),
                    "G23*\n(GPa)": Decimal("2.571"),
                    "K23*\n(GPa)": Decimal("5.694"),
                },
                {
                    "Vf": Decimal("0.57"),
                    "E1*\n(GPa)": Decimal("143.704"),
                    "E2*\n(GPa)": Decimal("7.191"),
                    "G12*\n(GPa)": Decimal("3.335"),
                    "v12*": Decimal("0.2886"),
                    "G23*\n(GPa)": Decimal("2.623"),
                    "K23*\n(GPa)": Decimal("5.792"),
                },
                {
                    "Vf": Decimal("0.58"),
                    "E1*\n(GPa)": Decimal("146.176"),
                    "E2*\n(GPa)": Decimal("7.331"),
                    "G12*\n(GPa)": Decimal("3.417"),
                    "v12*": Decimal("0.2884"),
                    "G23*\n(GPa)": Decimal("2.676"),
                    "K23*\n(GPa)": Decimal("5.893"),
                },
                {
                    "Vf": Decimal("0.59"),
                    "E1*\n(GPa)": Decimal("148.648"),
                    "E2*\n(GPa)": Decimal("7.474"),
                    "G12*\n(GPa)": Decimal("3.503"),
                    "v12*": Decimal("0.2882"),
                    "G23*\n(GPa)": Decimal("2.731"),
                    "K23*\n(GPa)": Decimal("5.996"),
                },
                {
                    "Vf": Decimal("0.6"),
                    "E1*\n(GPa)": Decimal("151.120"),
                    "E2*\n(GPa)": Decimal("7.621"),
                    "G12*\n(GPa)": Decimal("3.592"),
                    "v12*": Decimal("0.2880"),
                    "G23*\n(GPa)": Decimal("2.787"),
                    "K23*\n(GPa)": Decimal("6.103"),
                },
                {
                    "Vf": Decimal("0.61"),
                    "E1*\n(GPa)": Decimal("153.592"),
                    "E2*\n(GPa)": Decimal("7.775"),
                    "G12*\n(GPa)": Decimal("3.685"),
                    "v12*": Decimal("0.2878"),
                    "G23*\n(GPa)": Decimal("2.846"),
                    "K23*\n(GPa)": Decimal("6.213"),
                },
                {
                    "Vf": Decimal("0.62"),
                    "E1*\n(GPa)": Decimal("156.064"),
                    "E2*\n(GPa)": Decimal("7.932"),
                    "G12*\n(GPa)": Decimal("3.781"),
                    "v12*": Decimal("0.2876"),
                    "G23*\n(GPa)": Decimal("2.906"),
                    "K23*\n(GPa)": Decimal("6.326"),
                },
                {
                    "Vf": Decimal("0.63"),
                    "E1*\n(GPa)": Decimal("158.536"),
                    "E2*\n(GPa)": Decimal("8.095"),
                    "G12*\n(GPa)": Decimal("3.882"),
                    "v12*": Decimal("0.2874"),
                    "G23*\n(GPa)": Decimal("2.969"),
                    "K23*\n(GPa)": Decimal("6.443"),
                },
                {
                    "Vf": Decimal("0.64"),
                    "E1*\n(GPa)": Decimal("161.008"),
                    "E2*\n(GPa)": Decimal("8.265"),
                    "G12*\n(GPa)": Decimal("3.986"),
                    "v12*": Decimal("0.2872"),
                    "G23*\n(GPa)": Decimal("3.034"),
                    "K23*\n(GPa)": Decimal("6.564"),
                },
                {
                    "Vf": Decimal("0.65"),
                    "E1*\n(GPa)": Decimal("163.480"),
                    "E2*\n(GPa)": Decimal("8.441"),
                    "G12*\n(GPa)": Decimal("4.096"),
                    "v12*": Decimal("0.2870"),
                    "G23*\n(GPa)": Decimal("3.102"),
                    "K23*\n(GPa)": Decimal("6.689"),
                },
                {
                    "Vf": Decimal("0.66"),
                    "E1*\n(GPa)": Decimal("165.952"),
                    "E2*\n(GPa)": Decimal("8.622"),
                    "G12*\n(GPa)": Decimal("4.210"),
                    "v12*": Decimal("0.2868"),
                    "G23*\n(GPa)": Decimal("3.172"),
                    "K23*\n(GPa)": Decimal("6.817"),
                },
                {
                    "Vf": Decimal("0.67"),
                    "E1*\n(GPa)": Decimal("168.424"),
                    "E2*\n(GPa)": Decimal("8.811"),
                    "G12*\n(GPa)": Decimal("4.329"),
                    "v12*": Decimal("0.2866"),
                    "G23*\n(GPa)": Decimal("3.245"),
                    "K23*\n(GPa)": Decimal("6.950"),
                },
                {
                    "Vf": Decimal("0.68"),
                    "E1*\n(GPa)": Decimal("170.896"),
                    "E2*\n(GPa)": Decimal("9.007"),
                    "G12*\n(GPa)": Decimal("4.453"),
                    "v12*": Decimal("0.2864"),
                    "G23*\n(GPa)": Decimal("3.321"),
                    "K23*\n(GPa)": Decimal("7.088"),
                },
                {
                    "Vf": Decimal("0.69"),
                    "E1*\n(GPa)": Decimal("173.368"),
                    "E2*\n(GPa)": Decimal("9.208"),
                    "G12*\n(GPa)": Decimal("4.584"),
                    "v12*": Decimal("0.2862"),
                    "G23*\n(GPa)": Decimal("3.399"),
                    "K23*\n(GPa)": Decimal("7.231"),
                },
                {
                    "Vf": Decimal("0.7"),
                    "E1*\n(GPa)": Decimal("175.840"),
                    "E2*\n(GPa)": Decimal("9.419"),
                    "G12*\n(GPa)": Decimal("4.721"),
                    "v12*": Decimal("0.2860"),
                    "G23*\n(GPa)": Decimal("3.481"),
                    "K23*\n(GPa)": Decimal("7.378"),
                },
                {
                    "Vf": Decimal("0.71"),
                    "E1*\n(GPa)": Decimal("178.312"),
                    "E2*\n(GPa)": Decimal("9.639"),
                    "G12*\n(GPa)": Decimal("4.864"),
                    "v12*": Decimal("0.2858"),
                    "G23*\n(GPa)": Decimal("3.567"),
                    "K23*\n(GPa)": Decimal("7.531"),
                },
                {
                    "Vf": Decimal("0.72"),
                    "E1*\n(GPa)": Decimal("180.784"),
                    "E2*\n(GPa)": Decimal("9.868"),
                    "G12*\n(GPa)": Decimal("5.015"),
                    "v12*": Decimal("0.2856"),
                    "G23*\n(GPa)": Decimal("3.656"),
                    "K23*\n(GPa)": Decimal("7.690"),
                },
                {
                    "Vf": Decimal("0.73"),
                    "E1*\n(GPa)": Decimal("183.256"),
                    "E2*\n(GPa)": Decimal("10.105"),
                    "G12*\n(GPa)": Decimal("5.174"),
                    "v12*": Decimal("0.2854"),
                    "G23*\n(GPa)": Decimal("3.749"),
                    "K23*\n(GPa)": Decimal("7.854"),
                },
                {
                    "Vf": Decimal("0.74"),
                    "E1*\n(GPa)": Decimal("185.728"),
                    "E2*\n(GPa)": Decimal("10.353"),
                    "G12*\n(GPa)": Decimal("5.341"),
                    "v12*": Decimal("0.2852"),
                    "G23*\n(GPa)": Decimal("3.846"),
                    "K23*\n(GPa)": Decimal("8.025"),
                },
                {
                    "Vf": Decimal("0.75"),
                    "E1*\n(GPa)": Decimal("188.200"),
                    "E2*\n(GPa)": Decimal("10.610"),
                    "G12*\n(GPa)": Decimal("5.517"),
                    "v12*": Decimal("0.2850"),
                    "G23*\n(GPa)": Decimal("3.947"),
                    "K23*\n(GPa)": Decimal("8.202"),
                },
                {
                    "Vf": Decimal("0.76"),
                    "E1*\n(GPa)": Decimal("190.672"),
                    "E2*\n(GPa)": Decimal("10.881"),
                    "G12*\n(GPa)": Decimal("5.704"),
                    "v12*": Decimal("0.2848"),
                    "G23*\n(GPa)": Decimal("4.054"),
                    "K23*\n(GPa)": Decimal("8.387"),
                },
                {
                    "Vf": Decimal("0.77"),
                    "E1*\n(GPa)": Decimal("193.144"),
                    "E2*\n(GPa)": Decimal("11.163"),
                    "G12*\n(GPa)": Decimal("5.901"),
                    "v12*": Decimal("0.2846"),
                    "G23*\n(GPa)": Decimal("4.165"),
                    "K23*\n(GPa)": Decimal("8.579"),
                },
                {
                    "Vf": Decimal("0.78"),
                    "E1*\n(GPa)": Decimal("195.616"),
                    "E2*\n(GPa)": Decimal("11.458"),
                    "G12*\n(GPa)": Decimal("6.110"),
                    "v12*": Decimal("0.2844"),
                    "G23*\n(GPa)": Decimal("4.282"),
                    "K23*\n(GPa)": Decimal("8.779"),
                },
                {
                    "Vf": Decimal("0.79"),
                    "E1*\n(GPa)": Decimal("198.088"),
                    "E2*\n(GPa)": Decimal("11.766"),
                    "G12*\n(GPa)": Decimal("6.332"),
                    "v12*": Decimal("0.2842"),
                    "G23*\n(GPa)": Decimal("4.404"),
                    "K23*\n(GPa)": Decimal("8.987"),
                },
                {
                    "Vf": Decimal("0.8"),
                    "E1*\n(GPa)": Decimal("200.560"),
                    "E2*\n(GPa)": Decimal("12.090"),
                    "G12*\n(GPa)": Decimal("6.568"),
                    "v12*": Decimal("0.2840"),
                    "G23*\n(GPa)": Decimal("4.533"),
                    "K23*\n(GPa)": Decimal("9.204"),
                },
                {
                    "Vf": Decimal("0.81"),
                    "E1*\n(GPa)": Decimal("203.032"),
                    "E2*\n(GPa)": Decimal("12.430"),
                    "G12*\n(GPa)": Decimal("6.819"),
                    "v12*": Decimal("0.2838"),
                    "G23*\n(GPa)": Decimal("4.669"),
                    "K23*\n(GPa)": Decimal("9.431"),
                },
                {
                    "Vf": Decimal("0.82"),
                    "E1*\n(GPa)": Decimal("205.504"),
                    "E2*\n(GPa)": Decimal("12.789"),
                    "G12*\n(GPa)": Decimal("7.088"),
                    "v12*": Decimal("0.2836"),
                    "G23*\n(GPa)": Decimal("4.813"),
                    "K23*\n(GPa)": Decimal("9.669"),
                },
                {
                    "Vf": Decimal("0.83"),
                    "E1*\n(GPa)": Decimal("207.976"),
                    "E2*\n(GPa)": Decimal("13.165"),
                    "G12*\n(GPa)": Decimal("7.376"),
                    "v12*": Decimal("0.2834"),
                    "G23*\n(GPa)": Decimal("4.964"),
                    "K23*\n(GPa)": Decimal("9.917"),
                },
                {
                    "Vf": Decimal("0.84"),
                    "E1*\n(GPa)": Decimal("210.448"),
                    "E2*\n(GPa)": Decimal("13.562"),
                    "G12*\n(GPa)": Decimal("7.685"),
                    "v12*": Decimal("0.2832"),
                    "G23*\n(GPa)": Decimal("5.124"),
                    "K23*\n(GPa)": Decimal("10.177"),
                },
                {
                    "Vf": Decimal("0.85"),
                    "E1*\n(GPa)": Decimal("212.920"),
                    "E2*\n(GPa)": Decimal("13.979"),
                    "G12*\n(GPa)": Decimal("8.017"),
                    "v12*": Decimal("0.2830"),
                    "G23*\n(GPa)": Decimal("5.293"),
                    "K23*\n(GPa)": Decimal("10.449"),
                },
                {
                    "Vf": Decimal("0.86"),
                    "E1*\n(GPa)": Decimal("215.392"),
                    "E2*\n(GPa)": Decimal("14.422"),
                    "G12*\n(GPa)": Decimal("8.375"),
                    "v12*": Decimal("0.2828"),
                    "G23*\n(GPa)": Decimal("5.473"),
                    "K23*\n(GPa)": Decimal("10.735"),
                },
                {
                    "Vf": Decimal("0.87"),
                    "E1*\n(GPa)": Decimal("217.864"),
                    "E2*\n(GPa)": Decimal("14.890"),
                    "G12*\n(GPa)": Decimal("8.763"),
                    "v12*": Decimal("0.2826"),
                    "G23*\n(GPa)": Decimal("5.664"),
                    "K23*\n(GPa)": Decimal("11.036"),
                },
                {
                    "Vf": Decimal("0.88"),
                    "E1*\n(GPa)": Decimal("220.336"),
                    "E2*\n(GPa)": Decimal("15.386"),
                    "G12*\n(GPa)": Decimal("9.183"),
                    "v12*": Decimal("0.2824"),
                    "G23*\n(GPa)": Decimal("5.867"),
                    "K23*\n(GPa)": Decimal("11.352"),
                },
                {
                    "Vf": Decimal("0.89"),
                    "E1*\n(GPa)": Decimal("222.808"),
                    "E2*\n(GPa)": Decimal("15.914"),
                    "G12*\n(GPa)": Decimal("9.642"),
                    "v12*": Decimal("0.2822"),
                    "G23*\n(GPa)": Decimal("6.085"),
                    "K23*\n(GPa)": Decimal("11.685"),
                },
                {
                    "Vf": Decimal("0.9"),
                    "E1*\n(GPa)": Decimal("225.280"),
                    "E2*\n(GPa)": Decimal("16.475"),
                    "G12*\n(GPa)": Decimal("10.143"),
                    "v12*": Decimal("0.2820"),
                    "G23*\n(GPa)": Decimal("6.317"),
                    "K23*\n(GPa)": Decimal("12.037"),
                },
                {
                    "Vf": Decimal("0.91"),
                    "E1*\n(GPa)": Decimal("227.752"),
                    "E2*\n(GPa)": Decimal("17.073"),
                    "G12*\n(GPa)": Decimal("10.694"),
                    "v12*": Decimal("0.2818"),
                    "G23*\n(GPa)": Decimal("6.566"),
                    "K23*\n(GPa)": Decimal("12.408"),
                },
                {
                    "Vf": Decimal("0.92"),
                    "E1*\n(GPa)": Decimal("230.224"),
                    "E2*\n(GPa)": Decimal("17.711"),
                    "G12*\n(GPa)": Decimal("11.301"),
                    "v12*": Decimal("0.2816"),
                    "G23*\n(GPa)": Decimal("6.833"),
                    "K23*\n(GPa)": Decimal("12.801"),
                },
                {
                    "Vf": Decimal("0.93"),
                    "E1*\n(GPa)": Decimal("232.696"),
                    "E2*\n(GPa)": Decimal("18.397"),
                    "G12*\n(GPa)": Decimal("11.974"),
                    "v12*": Decimal("0.2814"),
                    "G23*\n(GPa)": Decimal("7.122"),
                    "K23*\n(GPa)": Decimal("13.218"),
                },
                {
                    "Vf": Decimal("0.94"),
                    "E1*\n(GPa)": Decimal("235.168"),
                    "E2*\n(GPa)": Decimal("19.131"),
                    "G12*\n(GPa)": Decimal("12.725"),
                    "v12*": Decimal("0.2812"),
                    "G23*\n(GPa)": Decimal("7.433"),
                    "K23*\n(GPa)": Decimal("13.661"),
                },
                {
                    "Vf": Decimal("0.95"),
                    "E1*\n(GPa)": Decimal("237.640"),
                    "E2*\n(GPa)": Decimal("19.923"),
                    "G12*\n(GPa)": Decimal("13.567"),
                    "v12*": Decimal("0.2810"),
                    "G23*\n(GPa)": Decimal("7.771"),
                    "K23*\n(GPa)": Decimal("14.132"),
                },
                {
                    "Vf": Decimal("0.96"),
                    "E1*\n(GPa)": Decimal("240.112"),
                    "E2*\n(GPa)": Decimal("20.778"),
                    "G12*\n(GPa)": Decimal("14.519"),
                    "v12*": Decimal("0.2808"),
                    "G23*\n(GPa)": Decimal("8.139"),
                    "K23*\n(GPa)": Decimal("14.634"),
                },
                {
                    "Vf": Decimal("0.97"),
                    "E1*\n(GPa)": Decimal("242.584"),
                    "E2*\n(GPa)": Decimal("21.702"),
                    "G12*\n(GPa)": Decimal("15.604"),
                    "v12*": Decimal("0.2806"),
                    "G23*\n(GPa)": Decimal("8.540"),
                    "K23*\n(GPa)": Decimal("15.170"),
                },
                {
                    "Vf": Decimal("0.98"),
                    "E1*\n(GPa)": Decimal("245.056"),
                    "E2*\n(GPa)": Decimal("22.707"),
                    "G12*\n(GPa)": Decimal("16.850"),
                    "v12*": Decimal("0.2804"),
                    "G23*\n(GPa)": Decimal("8.980"),
                    "K23*\n(GPa)": Decimal("15.744"),
                },
                {
                    "Vf": Decimal("0.99"),
                    "E1*\n(GPa)": Decimal("247.528"),
                    "E2*\n(GPa)": Decimal("23.801"),
                    "G12*\n(GPa)": Decimal("18.298"),
                    "v12*": Decimal("0.2802"),
                    "G23*\n(GPa)": Decimal("9.464"),
                    "K23*\n(GPa)": Decimal("16.360"),
                },
                {
                    "Vf": Decimal("1"),
                    "E1*\n(GPa)": Decimal("250.000"),
                    "E2*\n(GPa)": Decimal("25.000"),
                    "G12*\n(GPa)": Decimal("20.000"),
                    "v12*": Decimal("0.2800"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("17.023"),
                },
            ],
            "Carbon-Epoxy_eff_moduli.csv",
        )
        result2 = _get_effective_elastic_moduli_and_filename(composite2)
        assert result2 == (
            [
                {
                    "Vf": Decimal("0"),
                    "E1*\n(GPa)": Decimal("2.800"),
                    "E2*\n(GPa)": Decimal("2.800"),
                    "G12*\n(GPa)": Decimal("1.077"),
                    "v12*": Decimal("0.3000"),
                    "G23*\n(GPa)": Decimal("1.077"),
                    "K23*\n(GPa)": Decimal("2.692"),
                },
                {
                    "Vf": Decimal("0.01"),
                    "E1*\n(GPa)": Decimal("3.972"),
                    "E2*\n(GPa)": Decimal("2.916"),
                    "G12*\n(GPa)": Decimal("1.098"),
                    "v12*": Decimal("0.2999"),
                    "G23*\n(GPa)": Decimal("1.093"),
                    "K23*\n(GPa)": Decimal("2.729"),
                },
                {
                    "Vf": Decimal("0.02"),
                    "E1*\n(GPa)": Decimal("5.144"),
                    "E2*\n(GPa)": Decimal("3.002"),
                    "G12*\n(GPa)": Decimal("1.119"),
                    "v12*": Decimal("0.2998"),
                    "G23*\n(GPa)": Decimal("1.110"),
                    "K23*\n(GPa)": Decimal("2.766"),
                },
                {
                    "Vf": Decimal("0.03"),
                    "E1*\n(GPa)": Decimal("6.316"),
                    "E2*\n(GPa)": Decimal("3.075"),
                    "G12*\n(GPa)": Decimal("1.141"),
                    "v12*": Decimal("0.2997"),
                    "G23*\n(GPa)": Decimal("1.127"),
                    "K23*\n(GPa)": Decimal("2.805"),
                },
                {
                    "Vf": Decimal("0.04"),
                    "E1*\n(GPa)": Decimal("7.488"),
                    "E2*\n(GPa)": Decimal("3.140"),
                    "G12*\n(GPa)": Decimal("1.163"),
                    "v12*": Decimal("0.2996"),
                    "G23*\n(GPa)": Decimal("1.144"),
                    "K23*\n(GPa)": Decimal("2.844"),
                },
                {
                    "Vf": Decimal("0.05"),
                    "E1*\n(GPa)": Decimal("8.660"),
                    "E2*\n(GPa)": Decimal("3.203"),
                    "G12*\n(GPa)": Decimal("1.185"),
                    "v12*": Decimal("0.2995"),
                    "G23*\n(GPa)": Decimal("1.162"),
                    "K23*\n(GPa)": Decimal("2.883"),
                },
                {
                    "Vf": Decimal("0.06"),
                    "E1*\n(GPa)": Decimal("9.832"),
                    "E2*\n(GPa)": Decimal("3.263"),
                    "G12*\n(GPa)": Decimal("1.208"),
                    "v12*": Decimal("0.2994"),
                    "G23*\n(GPa)": Decimal("1.180"),
                    "K23*\n(GPa)": Decimal("2.924"),
                },
                {
                    "Vf": Decimal("0.07"),
                    "E1*\n(GPa)": Decimal("11.004"),
                    "E2*\n(GPa)": Decimal("3.321"),
                    "G12*\n(GPa)": Decimal("1.231"),
                    "v12*": Decimal("0.2993"),
                    "G23*\n(GPa)": Decimal("1.198"),
                    "K23*\n(GPa)": Decimal("2.965"),
                },
                {
                    "Vf": Decimal("0.08"),
                    "E1*\n(GPa)": Decimal("12.176"),
                    "E2*\n(GPa)": Decimal("3.380"),
                    "G12*\n(GPa)": Decimal("1.255"),
                    "v12*": Decimal("0.2992"),
                    "G23*\n(GPa)": Decimal("1.217"),
                    "K23*\n(GPa)": Decimal("3.008"),
                },
                {
                    "Vf": Decimal("0.09"),
                    "E1*\n(GPa)": Decimal("13.348"),
                    "E2*\n(GPa)": Decimal("3.438"),
                    "G12*\n(GPa)": Decimal("1.279"),
                    "v12*": Decimal("0.2991"),
                    "G23*\n(GPa)": Decimal("1.236"),
                    "K23*\n(GPa)": Decimal("3.051"),
                },
                {
                    "Vf": Decimal("0.1"),
                    "E1*\n(GPa)": Decimal("14.520"),
                    "E2*\n(GPa)": Decimal("3.497"),
                    "G12*\n(GPa)": Decimal("1.304"),
                    "v12*": Decimal("0.2990"),
                    "G23*\n(GPa)": Decimal("1.256"),
                    "K23*\n(GPa)": Decimal("3.095"),
                },
                {
                    "Vf": Decimal("0.11"),
                    "E1*\n(GPa)": Decimal("15.692"),
                    "E2*\n(GPa)": Decimal("3.556"),
                    "G12*\n(GPa)": Decimal("1.330"),
                    "v12*": Decimal("0.2989"),
                    "G23*\n(GPa)": Decimal("1.276"),
                    "K23*\n(GPa)": Decimal("3.140"),
                },
                {
                    "Vf": Decimal("0.12"),
                    "E1*\n(GPa)": Decimal("16.864"),
                    "E2*\n(GPa)": Decimal("3.614"),
                    "G12*\n(GPa)": Decimal("1.356"),
                    "v12*": Decimal("0.2988"),
                    "G23*\n(GPa)": Decimal("1.296"),
                    "K23*\n(GPa)": Decimal("3.186"),
                },
                {
                    "Vf": Decimal("0.13"),
                    "E1*\n(GPa)": Decimal("18.036"),
                    "E2*\n(GPa)": Decimal("3.675"),
                    "G12*\n(GPa)": Decimal("1.382"),
                    "v12*": Decimal("0.2987"),
                    "G23*\n(GPa)": Decimal("1.317"),
                    "K23*\n(GPa)": Decimal("3.233"),
                },
                {
                    "Vf": Decimal("0.14"),
                    "E1*\n(GPa)": Decimal("19.208"),
                    "E2*\n(GPa)": Decimal("3.738"),
                    "G12*\n(GPa)": Decimal("1.409"),
                    "v12*": Decimal("0.2986"),
                    "G23*\n(GPa)": Decimal("1.339"),
                    "K23*\n(GPa)": Decimal("3.282"),
                },
                {
                    "Vf": Decimal("0.15"),
                    "E1*\n(GPa)": Decimal("20.380"),
                    "E2*\n(GPa)": Decimal("3.799"),
                    "G12*\n(GPa)": Decimal("1.437"),
                    "v12*": Decimal("0.2985"),
                    "G23*\n(GPa)": Decimal("1.360"),
                    "K23*\n(GPa)": Decimal("3.331"),
                },
                {
                    "Vf": Decimal("0.16"),
                    "E1*\n(GPa)": Decimal("21.552"),
                    "E2*\n(GPa)": Decimal("3.863"),
                    "G12*\n(GPa)": Decimal("1.465"),
                    "v12*": Decimal("0.2984"),
                    "G23*\n(GPa)": Decimal("1.383"),
                    "K23*\n(GPa)": Decimal("3.381"),
                },
                {
                    "Vf": Decimal("0.17"),
                    "E1*\n(GPa)": Decimal("22.724"),
                    "E2*\n(GPa)": Decimal("3.929"),
                    "G12*\n(GPa)": Decimal("1.494"),
                    "v12*": Decimal("0.2983"),
                    "G23*\n(GPa)": Decimal("1.406"),
                    "K23*\n(GPa)": Decimal("3.433"),
                },
                {
                    "Vf": Decimal("0.18"),
                    "E1*\n(GPa)": Decimal("23.896"),
                    "E2*\n(GPa)": Decimal("3.994"),
                    "G12*\n(GPa)": Decimal("1.524"),
                    "v12*": Decimal("0.2982"),
                    "G23*\n(GPa)": Decimal("1.429"),
                    "K23*\n(GPa)": Decimal("3.486"),
                },
                {
                    "Vf": Decimal("0.19"),
                    "E1*\n(GPa)": Decimal("25.068"),
                    "E2*\n(GPa)": Decimal("4.061"),
                    "G12*\n(GPa)": Decimal("1.554"),
                    "v12*": Decimal("0.2981"),
                    "G23*\n(GPa)": Decimal("1.453"),
                    "K23*\n(GPa)": Decimal("3.540"),
                },
                {
                    "Vf": Decimal("0.2"),
                    "E1*\n(GPa)": Decimal("26.240"),
                    "E2*\n(GPa)": Decimal("4.129"),
                    "G12*\n(GPa)": Decimal("1.585"),
                    "v12*": Decimal("0.2980"),
                    "G23*\n(GPa)": Decimal("1.477"),
                    "K23*\n(GPa)": Decimal("3.595"),
                },
                {
                    "Vf": Decimal("0.21"),
                    "E1*\n(GPa)": Decimal("27.412"),
                    "E2*\n(GPa)": Decimal("4.199"),
                    "G12*\n(GPa)": Decimal("1.617"),
                    "v12*": Decimal("0.2979"),
                    "G23*\n(GPa)": Decimal("1.502"),
                    "K23*\n(GPa)": Decimal("3.652"),
                },
                {
                    "Vf": Decimal("0.22"),
                    "E1*\n(GPa)": Decimal("28.584"),
                    "E2*\n(GPa)": Decimal("4.272"),
                    "G12*\n(GPa)": Decimal("1.650"),
                    "v12*": Decimal("0.2978"),
                    "G23*\n(GPa)": Decimal("1.528"),
                    "K23*\n(GPa)": Decimal("3.710"),
                },
                {
                    "Vf": Decimal("0.23"),
                    "E1*\n(GPa)": Decimal("29.756"),
                    "E2*\n(GPa)": Decimal("4.346"),
                    "G12*\n(GPa)": Decimal("1.683"),
                    "v12*": Decimal("0.2977"),
                    "G23*\n(GPa)": Decimal("1.555"),
                    "K23*\n(GPa)": Decimal("3.769"),
                },
                {
                    "Vf": Decimal("0.24"),
                    "E1*\n(GPa)": Decimal("30.928"),
                    "E2*\n(GPa)": Decimal("4.422"),
                    "G12*\n(GPa)": Decimal("1.717"),
                    "v12*": Decimal("0.2976"),
                    "G23*\n(GPa)": Decimal("1.582"),
                    "K23*\n(GPa)": Decimal("3.830"),
                },
                {
                    "Vf": Decimal("0.25"),
                    "E1*\n(GPa)": Decimal("32.100"),
                    "E2*\n(GPa)": Decimal("4.497"),
                    "G12*\n(GPa)": Decimal("1.752"),
                    "v12*": Decimal("0.2975"),
                    "G23*\n(GPa)": Decimal("1.609"),
                    "K23*\n(GPa)": Decimal("3.892"),
                },
                {
                    "Vf": Decimal("0.26"),
                    "E1*\n(GPa)": Decimal("33.272"),
                    "E2*\n(GPa)": Decimal("4.577"),
                    "G12*\n(GPa)": Decimal("1.788"),
                    "v12*": Decimal("0.2974"),
                    "G23*\n(GPa)": Decimal("1.638"),
                    "K23*\n(GPa)": Decimal("3.957"),
                },
                {
                    "Vf": Decimal("0.27"),
                    "E1*\n(GPa)": Decimal("34.444"),
                    "E2*\n(GPa)": Decimal("4.658"),
                    "G12*\n(GPa)": Decimal("1.825"),
                    "v12*": Decimal("0.2973"),
                    "G23*\n(GPa)": Decimal("1.667"),
                    "K23*\n(GPa)": Decimal("4.022"),
                },
                {
                    "Vf": Decimal("0.28"),
                    "E1*\n(GPa)": Decimal("35.616"),
                    "E2*\n(GPa)": Decimal("4.741"),
                    "G12*\n(GPa)": Decimal("1.863"),
                    "v12*": Decimal("0.2972"),
                    "G23*\n(GPa)": Decimal("1.697"),
                    "K23*\n(GPa)": Decimal("4.090"),
                },
                {
                    "Vf": Decimal("0.29"),
                    "E1*\n(GPa)": Decimal("36.788"),
                    "E2*\n(GPa)": Decimal("4.825"),
                    "G12*\n(GPa)": Decimal("1.902"),
                    "v12*": Decimal("0.2971"),
                    "G23*\n(GPa)": Decimal("1.727"),
                    "K23*\n(GPa)": Decimal("4.159"),
                },
                {
                    "Vf": Decimal("0.3"),
                    "E1*\n(GPa)": Decimal("37.960"),
                    "E2*\n(GPa)": Decimal("4.913"),
                    "G12*\n(GPa)": Decimal("1.942"),
                    "v12*": Decimal("0.2970"),
                    "G23*\n(GPa)": Decimal("1.759"),
                    "K23*\n(GPa)": Decimal("4.231"),
                },
                {
                    "Vf": Decimal("0.31"),
                    "E1*\n(GPa)": Decimal("39.132"),
                    "E2*\n(GPa)": Decimal("5.002"),
                    "G12*\n(GPa)": Decimal("1.983"),
                    "v12*": Decimal("0.2969"),
                    "G23*\n(GPa)": Decimal("1.791"),
                    "K23*\n(GPa)": Decimal("4.304"),
                },
                {
                    "Vf": Decimal("0.32"),
                    "E1*\n(GPa)": Decimal("40.304"),
                    "E2*\n(GPa)": Decimal("5.095"),
                    "G12*\n(GPa)": Decimal("2.025"),
                    "v12*": Decimal("0.2968"),
                    "G23*\n(GPa)": Decimal("1.825"),
                    "K23*\n(GPa)": Decimal("4.379"),
                },
                {
                    "Vf": Decimal("0.33"),
                    "E1*\n(GPa)": Decimal("41.476"),
                    "E2*\n(GPa)": Decimal("5.190"),
                    "G12*\n(GPa)": Decimal("2.068"),
                    "v12*": Decimal("0.2967"),
                    "G23*\n(GPa)": Decimal("1.859"),
                    "K23*\n(GPa)": Decimal("4.457"),
                },
                {
                    "Vf": Decimal("0.34"),
                    "E1*\n(GPa)": Decimal("42.648"),
                    "E2*\n(GPa)": Decimal("5.286"),
                    "G12*\n(GPa)": Decimal("2.112"),
                    "v12*": Decimal("0.2966"),
                    "G23*\n(GPa)": Decimal("1.894"),
                    "K23*\n(GPa)": Decimal("4.536"),
                },
                {
                    "Vf": Decimal("0.35"),
                    "E1*\n(GPa)": Decimal("43.820"),
                    "E2*\n(GPa)": Decimal("5.388"),
                    "G12*\n(GPa)": Decimal("2.158"),
                    "v12*": Decimal("0.2965"),
                    "G23*\n(GPa)": Decimal("1.931"),
                    "K23*\n(GPa)": Decimal("4.618"),
                },
                {
                    "Vf": Decimal("0.36"),
                    "E1*\n(GPa)": Decimal("44.992"),
                    "E2*\n(GPa)": Decimal("5.490"),
                    "G12*\n(GPa)": Decimal("2.205"),
                    "v12*": Decimal("0.2964"),
                    "G23*\n(GPa)": Decimal("1.968"),
                    "K23*\n(GPa)": Decimal("4.702"),
                },
                {
                    "Vf": Decimal("0.37"),
                    "E1*\n(GPa)": Decimal("46.164"),
                    "E2*\n(GPa)": Decimal("5.595"),
                    "G12*\n(GPa)": Decimal("2.254"),
                    "v12*": Decimal("0.2963"),
                    "G23*\n(GPa)": Decimal("2.006"),
                    "K23*\n(GPa)": Decimal("4.789"),
                },
                {
                    "Vf": Decimal("0.38"),
                    "E1*\n(GPa)": Decimal("47.336"),
                    "E2*\n(GPa)": Decimal("5.705"),
                    "G12*\n(GPa)": Decimal("2.303"),
                    "v12*": Decimal("0.2962"),
                    "G23*\n(GPa)": Decimal("2.046"),
                    "K23*\n(GPa)": Decimal("4.879"),
                },
                {
                    "Vf": Decimal("0.39"),
                    "E1*\n(GPa)": Decimal("48.508"),
                    "E2*\n(GPa)": Decimal("5.818"),
                    "G12*\n(GPa)": Decimal("2.355"),
                    "v12*": Decimal("0.2961"),
                    "G23*\n(GPa)": Decimal("2.087"),
                    "K23*\n(GPa)": Decimal("4.971"),
                },
                {
                    "Vf": Decimal("0.4"),
                    "E1*\n(GPa)": Decimal("49.680"),
                    "E2*\n(GPa)": Decimal("5.934"),
                    "G12*\n(GPa)": Decimal("2.408"),
                    "v12*": Decimal("0.2960"),
                    "G23*\n(GPa)": Decimal("2.129"),
                    "K23*\n(GPa)": Decimal("5.067"),
                },
                {
                    "Vf": Decimal("0.41"),
                    "E1*\n(GPa)": Decimal("50.852"),
                    "E2*\n(GPa)": Decimal("6.054"),
                    "G12*\n(GPa)": Decimal("2.463"),
                    "v12*": Decimal("0.2959"),
                    "G23*\n(GPa)": Decimal("2.173"),
                    "K23*\n(GPa)": Decimal("5.165"),
                },
                {
                    "Vf": Decimal("0.42"),
                    "E1*\n(GPa)": Decimal("52.024"),
                    "E2*\n(GPa)": Decimal("6.178"),
                    "G12*\n(GPa)": Decimal("2.519"),
                    "v12*": Decimal("0.2958"),
                    "G23*\n(GPa)": Decimal("2.218"),
                    "K23*\n(GPa)": Decimal("5.266"),
                },
                {
                    "Vf": Decimal("0.43"),
                    "E1*\n(GPa)": Decimal("53.196"),
                    "E2*\n(GPa)": Decimal("6.305"),
                    "G12*\n(GPa)": Decimal("2.577"),
                    "v12*": Decimal("0.2957"),
                    "G23*\n(GPa)": Decimal("2.264"),
                    "K23*\n(GPa)": Decimal("5.371"),
                },
                {
                    "Vf": Decimal("0.44"),
                    "E1*\n(GPa)": Decimal("54.368"),
                    "E2*\n(GPa)": Decimal("6.437"),
                    "G12*\n(GPa)": Decimal("2.637"),
                    "v12*": Decimal("0.2956"),
                    "G23*\n(GPa)": Decimal("2.312"),
                    "K23*\n(GPa)": Decimal("5.480"),
                },
                {
                    "Vf": Decimal("0.45"),
                    "E1*\n(GPa)": Decimal("55.540"),
                    "E2*\n(GPa)": Decimal("6.574"),
                    "G12*\n(GPa)": Decimal("2.700"),
                    "v12*": Decimal("0.2955"),
                    "G23*\n(GPa)": Decimal("2.362"),
                    "K23*\n(GPa)": Decimal("5.592"),
                },
                {
                    "Vf": Decimal("0.46"),
                    "E1*\n(GPa)": Decimal("56.712"),
                    "E2*\n(GPa)": Decimal("6.714"),
                    "G12*\n(GPa)": Decimal("2.764"),
                    "v12*": Decimal("0.2954"),
                    "G23*\n(GPa)": Decimal("2.413"),
                    "K23*\n(GPa)": Decimal("5.708"),
                },
                {
                    "Vf": Decimal("0.47"),
                    "E1*\n(GPa)": Decimal("57.884"),
                    "E2*\n(GPa)": Decimal("6.860"),
                    "G12*\n(GPa)": Decimal("2.830"),
                    "v12*": Decimal("0.2953"),
                    "G23*\n(GPa)": Decimal("2.466"),
                    "K23*\n(GPa)": Decimal("5.828"),
                },
                {
                    "Vf": Decimal("0.48"),
                    "E1*\n(GPa)": Decimal("59.056"),
                    "E2*\n(GPa)": Decimal("7.010"),
                    "G12*\n(GPa)": Decimal("2.899"),
                    "v12*": Decimal("0.2952"),
                    "G23*\n(GPa)": Decimal("2.521"),
                    "K23*\n(GPa)": Decimal("5.952"),
                },
                {
                    "Vf": Decimal("0.49"),
                    "E1*\n(GPa)": Decimal("60.228"),
                    "E2*\n(GPa)": Decimal("7.167"),
                    "G12*\n(GPa)": Decimal("2.971"),
                    "v12*": Decimal("0.2951"),
                    "G23*\n(GPa)": Decimal("2.578"),
                    "K23*\n(GPa)": Decimal("6.081"),
                },
                {
                    "Vf": Decimal("0.5"),
                    "E1*\n(GPa)": Decimal("61.400"),
                    "E2*\n(GPa)": Decimal("7.329"),
                    "G12*\n(GPa)": Decimal("3.044"),
                    "v12*": Decimal("0.2950"),
                    "G23*\n(GPa)": Decimal("2.637"),
                    "K23*\n(GPa)": Decimal("6.215"),
                },
                {
                    "Vf": Decimal("0.51"),
                    "E1*\n(GPa)": Decimal("62.572"),
                    "E2*\n(GPa)": Decimal("7.498"),
                    "G12*\n(GPa)": Decimal("3.121"),
                    "v12*": Decimal("0.2949"),
                    "G23*\n(GPa)": Decimal("2.699"),
                    "K23*\n(GPa)": Decimal("6.354"),
                },
                {
                    "Vf": Decimal("0.52"),
                    "E1*\n(GPa)": Decimal("63.744"),
                    "E2*\n(GPa)": Decimal("7.672"),
                    "G12*\n(GPa)": Decimal("3.201"),
                    "v12*": Decimal("0.2948"),
                    "G23*\n(GPa)": Decimal("2.762"),
                    "K23*\n(GPa)": Decimal("6.498"),
                },
                {
                    "Vf": Decimal("0.53"),
                    "E1*\n(GPa)": Decimal("64.916"),
                    "E2*\n(GPa)": Decimal("7.855"),
                    "G12*\n(GPa)": Decimal("3.283"),
                    "v12*": Decimal("0.2947"),
                    "G23*\n(GPa)": Decimal("2.829"),
                    "K23*\n(GPa)": Decimal("6.649"),
                },
                {
                    "Vf": Decimal("0.54"),
                    "E1*\n(GPa)": Decimal("66.088"),
                    "E2*\n(GPa)": Decimal("8.044"),
                    "G12*\n(GPa)": Decimal("3.369"),
                    "v12*": Decimal("0.2946"),
                    "G23*\n(GPa)": Decimal("2.898"),
                    "K23*\n(GPa)": Decimal("6.805"),
                },
                {
                    "Vf": Decimal("0.55"),
                    "E1*\n(GPa)": Decimal("67.260"),
                    "E2*\n(GPa)": Decimal("8.241"),
                    "G12*\n(GPa)": Decimal("3.459"),
                    "v12*": Decimal("0.2945"),
                    "G23*\n(GPa)": Decimal("2.970"),
                    "K23*\n(GPa)": Decimal("6.967"),
                },
                {
                    "Vf": Decimal("0.56"),
                    "E1*\n(GPa)": Decimal("68.432"),
                    "E2*\n(GPa)": Decimal("8.444"),
                    "G12*\n(GPa)": Decimal("3.552"),
                    "v12*": Decimal("0.2944"),
                    "G23*\n(GPa)": Decimal("3.044"),
                    "K23*\n(GPa)": Decimal("7.137"),
                },
                {
                    "Vf": Decimal("0.57"),
                    "E1*\n(GPa)": Decimal("69.604"),
                    "E2*\n(GPa)": Decimal("8.657"),
                    "G12*\n(GPa)": Decimal("3.649"),
                    "v12*": Decimal("0.2943"),
                    "G23*\n(GPa)": Decimal("3.122"),
                    "K23*\n(GPa)": Decimal("7.313"),
                },
                {
                    "Vf": Decimal("0.58"),
                    "E1*\n(GPa)": Decimal("70.776"),
                    "E2*\n(GPa)": Decimal("8.882"),
                    "G12*\n(GPa)": Decimal("3.750"),
                    "v12*": Decimal("0.2942"),
                    "G23*\n(GPa)": Decimal("3.204"),
                    "K23*\n(GPa)": Decimal("7.498"),
                },
                {
                    "Vf": Decimal("0.59"),
                    "E1*\n(GPa)": Decimal("71.948"),
                    "E2*\n(GPa)": Decimal("9.114"),
                    "G12*\n(GPa)": Decimal("3.855"),
                    "v12*": Decimal("0.2941"),
                    "G23*\n(GPa)": Decimal("3.289"),
                    "K23*\n(GPa)": Decimal("7.690"),
                },
                {
                    "Vf": Decimal("0.6"),
                    "E1*\n(GPa)": Decimal("73.120"),
                    "E2*\n(GPa)": Decimal("9.357"),
                    "G12*\n(GPa)": Decimal("3.966"),
                    "v12*": Decimal("0.2940"),
                    "G23*\n(GPa)": Decimal("3.378"),
                    "K23*\n(GPa)": Decimal("7.892"),
                },
                {
                    "Vf": Decimal("0.61"),
                    "E1*\n(GPa)": Decimal("74.292"),
                    "E2*\n(GPa)": Decimal("9.612"),
                    "G12*\n(GPa)": Decimal("4.081"),
                    "v12*": Decimal("0.2939"),
                    "G23*\n(GPa)": Decimal("3.471"),
                    "K23*\n(GPa)": Decimal("8.103"),
                },
                {
                    "Vf": Decimal("0.62"),
                    "E1*\n(GPa)": Decimal("75.464"),
                    "E2*\n(GPa)": Decimal("9.879"),
                    "G12*\n(GPa)": Decimal("4.202"),
                    "v12*": Decimal("0.2938"),
                    "G23*\n(GPa)": Decimal("3.569"),
                    "K23*\n(GPa)": Decimal("8.324"),
                },
                {
                    "Vf": Decimal("0.63"),
                    "E1*\n(GPa)": Decimal("76.636"),
                    "E2*\n(GPa)": Decimal("10.158"),
                    "G12*\n(GPa)": Decimal("4.328"),
                    "v12*": Decimal("0.2937"),
                    "G23*\n(GPa)": Decimal("3.671"),
                    "K23*\n(GPa)": Decimal("8.557"),
                },
                {
                    "Vf": Decimal("0.64"),
                    "E1*\n(GPa)": Decimal("77.808"),
                    "E2*\n(GPa)": Decimal("10.453"),
                    "G12*\n(GPa)": Decimal("4.461"),
                    "v12*": Decimal("0.2936"),
                    "G23*\n(GPa)": Decimal("3.779"),
                    "K23*\n(GPa)": Decimal("8.801"),
                },
                {
                    "Vf": Decimal("0.65"),
                    "E1*\n(GPa)": Decimal("78.980"),
                    "E2*\n(GPa)": Decimal("10.761"),
                    "G12*\n(GPa)": Decimal("4.600"),
                    "v12*": Decimal("0.2935"),
                    "G23*\n(GPa)": Decimal("3.892"),
                    "K23*\n(GPa)": Decimal("9.057"),
                },
                {
                    "Vf": Decimal("0.66"),
                    "E1*\n(GPa)": Decimal("80.152"),
                    "E2*\n(GPa)": Decimal("11.086"),
                    "G12*\n(GPa)": Decimal("4.747"),
                    "v12*": Decimal("0.2934"),
                    "G23*\n(GPa)": Decimal("4.011"),
                    "K23*\n(GPa)": Decimal("9.328"),
                },
                {
                    "Vf": Decimal("0.67"),
                    "E1*\n(GPa)": Decimal("81.324"),
                    "E2*\n(GPa)": Decimal("11.427"),
                    "G12*\n(GPa)": Decimal("4.901"),
                    "v12*": Decimal("0.2933"),
                    "G23*\n(GPa)": Decimal("4.136"),
                    "K23*\n(GPa)": Decimal("9.613"),
                },
                {
                    "Vf": Decimal("0.68"),
                    "E1*\n(GPa)": Decimal("82.496"),
                    "E2*\n(GPa)": Decimal("11.790"),
                    "G12*\n(GPa)": Decimal("5.064"),
                    "v12*": Decimal("0.2932"),
                    "G23*\n(GPa)": Decimal("4.269"),
                    "K23*\n(GPa)": Decimal("9.914"),
                },
                {
                    "Vf": Decimal("0.69"),
                    "E1*\n(GPa)": Decimal("83.668"),
                    "E2*\n(GPa)": Decimal("12.171"),
                    "G12*\n(GPa)": Decimal("5.235"),
                    "v12*": Decimal("0.2931"),
                    "G23*\n(GPa)": Decimal("4.409"),
                    "K23*\n(GPa)": Decimal("10.233"),
                },
                {
                    "Vf": Decimal("0.7"),
                    "E1*\n(GPa)": Decimal("84.840"),
                    "E2*\n(GPa)": Decimal("12.577"),
                    "G12*\n(GPa)": Decimal("5.417"),
                    "v12*": Decimal("0.2930"),
                    "G23*\n(GPa)": Decimal("4.558"),
                    "K23*\n(GPa)": Decimal("10.570"),
                },
                {
                    "Vf": Decimal("0.71"),
                    "E1*\n(GPa)": Decimal("86.012"),
                    "E2*\n(GPa)": Decimal("13.007"),
                    "G12*\n(GPa)": Decimal("5.610"),
                    "v12*": Decimal("0.2929"),
                    "G23*\n(GPa)": Decimal("4.716"),
                    "K23*\n(GPa)": Decimal("10.929"),
                },
                {
                    "Vf": Decimal("0.72"),
                    "E1*\n(GPa)": Decimal("87.184"),
                    "E2*\n(GPa)": Decimal("13.463"),
                    "G12*\n(GPa)": Decimal("5.814"),
                    "v12*": Decimal("0.2928"),
                    "G23*\n(GPa)": Decimal("4.884"),
                    "K23*\n(GPa)": Decimal("11.310"),
                },
                {
                    "Vf": Decimal("0.73"),
                    "E1*\n(GPa)": Decimal("88.356"),
                    "E2*\n(GPa)": Decimal("13.948"),
                    "G12*\n(GPa)": Decimal("6.031"),
                    "v12*": Decimal("0.2927"),
                    "G23*\n(GPa)": Decimal("5.062"),
                    "K23*\n(GPa)": Decimal("11.716"),
                },
                {
                    "Vf": Decimal("0.74"),
                    "E1*\n(GPa)": Decimal("89.528"),
                    "E2*\n(GPa)": Decimal("14.467"),
                    "G12*\n(GPa)": Decimal("6.262"),
                    "v12*": Decimal("0.2926"),
                    "G23*\n(GPa)": Decimal("5.253"),
                    "K23*\n(GPa)": Decimal("12.150"),
                },
                {
                    "Vf": Decimal("0.75"),
                    "E1*\n(GPa)": Decimal("90.700"),
                    "E2*\n(GPa)": Decimal("15.021"),
                    "G12*\n(GPa)": Decimal("6.509"),
                    "v12*": Decimal("0.2925"),
                    "G23*\n(GPa)": Decimal("5.457"),
                    "K23*\n(GPa)": Decimal("12.615"),
                },
                {
                    "Vf": Decimal("0.76"),
                    "E1*\n(GPa)": Decimal("91.872"),
                    "E2*\n(GPa)": Decimal("15.615"),
                    "G12*\n(GPa)": Decimal("6.773"),
                    "v12*": Decimal("0.2924"),
                    "G23*\n(GPa)": Decimal("5.676"),
                    "K23*\n(GPa)": Decimal("13.113"),
                },
                {
                    "Vf": Decimal("0.77"),
                    "E1*\n(GPa)": Decimal("93.044"),
                    "E2*\n(GPa)": Decimal("16.252"),
                    "G12*\n(GPa)": Decimal("7.056"),
                    "v12*": Decimal("0.2923"),
                    "G23*\n(GPa)": Decimal("5.911"),
                    "K23*\n(GPa)": Decimal("13.648"),
                },
                {
                    "Vf": Decimal("0.78"),
                    "E1*\n(GPa)": Decimal("94.216"),
                    "E2*\n(GPa)": Decimal("16.938"),
                    "G12*\n(GPa)": Decimal("7.360"),
                    "v12*": Decimal("0.2922"),
                    "G23*\n(GPa)": Decimal("6.164"),
                    "K23*\n(GPa)": Decimal("14.226"),
                },
                {
                    "Vf": Decimal("0.79"),
                    "E1*\n(GPa)": Decimal("95.388"),
                    "E2*\n(GPa)": Decimal("17.680"),
                    "G12*\n(GPa)": Decimal("7.688"),
                    "v12*": Decimal("0.2921"),
                    "G23*\n(GPa)": Decimal("6.438"),
                    "K23*\n(GPa)": Decimal("14.851"),
                },
                {
                    "Vf": Decimal("0.8"),
                    "E1*\n(GPa)": Decimal("96.560"),
                    "E2*\n(GPa)": Decimal("18.484"),
                    "G12*\n(GPa)": Decimal("8.042"),
                    "v12*": Decimal("0.2920"),
                    "G23*\n(GPa)": Decimal("6.735"),
                    "K23*\n(GPa)": Decimal("15.529"),
                },
                {
                    "Vf": Decimal("0.81"),
                    "E1*\n(GPa)": Decimal("97.732"),
                    "E2*\n(GPa)": Decimal("19.357"),
                    "G12*\n(GPa)": Decimal("8.426"),
                    "v12*": Decimal("0.2919"),
                    "G23*\n(GPa)": Decimal("7.058"),
                    "K23*\n(GPa)": Decimal("16.268"),
                },
                {
                    "Vf": Decimal("0.82"),
                    "E1*\n(GPa)": Decimal("98.904"),
                    "E2*\n(GPa)": Decimal("20.310"),
                    "G12*\n(GPa)": Decimal("8.844"),
                    "v12*": Decimal("0.2918"),
                    "G23*\n(GPa)": Decimal("7.411"),
                    "K23*\n(GPa)": Decimal("17.075"),
                },
                {
                    "Vf": Decimal("0.83"),
                    "E1*\n(GPa)": Decimal("100.076"),
                    "E2*\n(GPa)": Decimal("21.354"),
                    "G12*\n(GPa)": Decimal("9.300"),
                    "v12*": Decimal("0.2917"),
                    "G23*\n(GPa)": Decimal("7.798"),
                    "K23*\n(GPa)": Decimal("17.961"),
                },
                {
                    "Vf": Decimal("0.84"),
                    "E1*\n(GPa)": Decimal("101.248"),
                    "E2*\n(GPa)": Decimal("22.504"),
                    "G12*\n(GPa)": Decimal("9.801"),
                    "v12*": Decimal("0.2916"),
                    "G23*\n(GPa)": Decimal("8.225"),
                    "K23*\n(GPa)": Decimal("18.938"),
                },
                {
                    "Vf": Decimal("0.85"),
                    "E1*\n(GPa)": Decimal("102.420"),
                    "E2*\n(GPa)": Decimal("23.774"),
                    "G12*\n(GPa)": Decimal("10.352"),
                    "v12*": Decimal("0.2915"),
                    "G23*\n(GPa)": Decimal("8.697"),
                    "K23*\n(GPa)": Decimal("20.020"),
                },
                {
                    "Vf": Decimal("0.86"),
                    "E1*\n(GPa)": Decimal("103.592"),
                    "E2*\n(GPa)": Decimal("25.186"),
                    "G12*\n(GPa)": Decimal("10.962"),
                    "v12*": Decimal("0.2914"),
                    "G23*\n(GPa)": Decimal("9.223"),
                    "K23*\n(GPa)": Decimal("21.226"),
                },
                {
                    "Vf": Decimal("0.87"),
                    "E1*\n(GPa)": Decimal("104.764"),
                    "E2*\n(GPa)": Decimal("26.764"),
                    "G12*\n(GPa)": Decimal("11.640"),
                    "v12*": Decimal("0.2913"),
                    "G23*\n(GPa)": Decimal("9.811"),
                    "K23*\n(GPa)": Decimal("22.579"),
                },
                {
                    "Vf": Decimal("0.88"),
                    "E1*\n(GPa)": Decimal("105.936"),
                    "E2*\n(GPa)": Decimal("28.541"),
                    "G12*\n(GPa)": Decimal("12.400"),
                    "v12*": Decimal("0.2912"),
                    "G23*\n(GPa)": Decimal("10.475"),
                    "K23*\n(GPa)": Decimal("24.106"),
                },
                {
                    "Vf": Decimal("0.89"),
                    "E1*\n(GPa)": Decimal("107.108"),
                    "E2*\n(GPa)": Decimal("30.555"),
                    "G12*\n(GPa)": Decimal("13.256"),
                    "v12*": Decimal("0.2911"),
                    "G23*\n(GPa)": Decimal("11.229"),
                    "K23*\n(GPa)": Decimal("25.845"),
                },
                {
                    "Vf": Decimal("0.9"),
                    "E1*\n(GPa)": Decimal("108.280"),
                    "E2*\n(GPa)": Decimal("32.857"),
                    "G12*\n(GPa)": Decimal("14.228"),
                    "v12*": Decimal("0.2910"),
                    "G23*\n(GPa)": Decimal("12.093"),
                    "K23*\n(GPa)": Decimal("27.841"),
                },
                {
                    "Vf": Decimal("0.91"),
                    "E1*\n(GPa)": Decimal("109.452"),
                    "E2*\n(GPa)": Decimal("35.514"),
                    "G12*\n(GPa)": Decimal("15.342"),
                    "v12*": Decimal("0.2909"),
                    "G23*\n(GPa)": Decimal("13.093"),
                    "K23*\n(GPa)": Decimal("30.156"),
                },
                {
                    "Vf": Decimal("0.92"),
                    "E1*\n(GPa)": Decimal("110.624"),
                    "E2*\n(GPa)": Decimal("38.618"),
                    "G12*\n(GPa)": Decimal("16.631"),
                    "v12*": Decimal("0.2908"),
                    "G23*\n(GPa)": Decimal("14.265"),
                    "K23*\n(GPa)": Decimal("32.875"),
                },
                {
                    "Vf": Decimal("0.93"),
                    "E1*\n(GPa)": Decimal("111.796"),
                    "E2*\n(GPa)": Decimal("42.287"),
                    "G12*\n(GPa)": Decimal("18.139"),
                    "v12*": Decimal("0.2907"),
                    "G23*\n(GPa)": Decimal("15.655"),
                    "K23*\n(GPa)": Decimal("36.112"),
                },
                {
                    "Vf": Decimal("0.94"),
                    "E1*\n(GPa)": Decimal("112.968"),
                    "E2*\n(GPa)": Decimal("46.694"),
                    "G12*\n(GPa)": Decimal("19.928"),
                    "v12*": Decimal("0.2906"),
                    "G23*\n(GPa)": Decimal("17.333"),
                    "K23*\n(GPa)": Decimal("40.032"),
                },
                {
                    "Vf": Decimal("0.95"),
                    "E1*\n(GPa)": Decimal("114.140"),
                    "E2*\n(GPa)": Decimal("52.086"),
                    "G12*\n(GPa)": Decimal("22.084"),
                    "v12*": Decimal("0.2905"),
                    "G23*\n(GPa)": Decimal("19.397"),
                    "K23*\n(GPa)": Decimal("44.875"),
                },
                {
                    "Vf": Decimal("0.96"),
                    "E1*\n(GPa)": Decimal("115.312"),
                    "E2*\n(GPa)": Decimal("58.834"),
                    "G12*\n(GPa)": Decimal("24.734"),
                    "v12*": Decimal("0.2904"),
                    "G23*\n(GPa)": Decimal("21.998"),
                    "K23*\n(GPa)": Decimal("51.011"),
                },
                {
                    "Vf": Decimal("0.97"),
                    "E1*\n(GPa)": Decimal("116.484"),
                    "E2*\n(GPa)": Decimal("67.525"),
                    "G12*\n(GPa)": Decimal("28.069"),
                    "v12*": Decimal("0.2903"),
                    "G23*\n(GPa)": Decimal("25.377"),
                    "K23*\n(GPa)": Decimal("59.039"),
                },
                {
                    "Vf": Decimal("0.98"),
                    "E1*\n(GPa)": Decimal("117.656"),
                    "E2*\n(GPa)": Decimal("79.138"),
                    "G12*\n(GPa)": Decimal("32.392"),
                    "v12*": Decimal("0.2902"),
                    "G23*\n(GPa)": Decimal("29.945"),
                    "K23*\n(GPa)": Decimal("69.993"),
                },
                {
                    "Vf": Decimal("0.99"),
                    "E1*\n(GPa)": Decimal("118.828"),
                    "E2*\n(GPa)": Decimal("95.441"),
                    "G12*\n(GPa)": Decimal("38.222"),
                    "v12*": Decimal("0.2901"),
                    "G23*\n(GPa)": Decimal("36.461"),
                    "K23*\n(GPa)": Decimal("85.828"),
                },
                {
                    "Vf": Decimal("1"),
                    "E1*\n(GPa)": Decimal("120.000"),
                    "E2*\n(GPa)": Decimal("120.001"),
                    "G12*\n(GPa)": Decimal("46.512"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("46.512"),
                    "K23*\n(GPa)": Decimal("110.742"),
                },
            ],
            "Fiberglass-Epoxy_eff_moduli.csv",
        )
        result3 = _get_effective_elastic_moduli_and_filename(composite3)
        assert result3 == (
            [
                {
                    "Vf": Decimal("0"),
                    "E1*\n(GPa)": Decimal("180.000"),
                    "E2*\n(GPa)": Decimal("20.000"),
                    "G12*\n(GPa)": Decimal("15.000"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.190"),
                },
                {
                    "Vf": Decimal("0.01"),
                    "E1*\n(GPa)": Decimal("180.700"),
                    "E2*\n(GPa)": Decimal("20.049"),
                    "G12*\n(GPa)": Decimal("15.043"),
                    "v12*": Decimal("0.2899"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.241"),
                },
                {
                    "Vf": Decimal("0.02"),
                    "E1*\n(GPa)": Decimal("181.400"),
                    "E2*\n(GPa)": Decimal("20.100"),
                    "G12*\n(GPa)": Decimal("15.086"),
                    "v12*": Decimal("0.2898"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.293"),
                },
                {
                    "Vf": Decimal("0.03"),
                    "E1*\n(GPa)": Decimal("182.100"),
                    "E2*\n(GPa)": Decimal("20.149"),
                    "G12*\n(GPa)": Decimal("15.129"),
                    "v12*": Decimal("0.2897"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.344"),
                },
                {
                    "Vf": Decimal("0.04"),
                    "E1*\n(GPa)": Decimal("182.800"),
                    "E2*\n(GPa)": Decimal("20.199"),
                    "G12*\n(GPa)": Decimal("15.172"),
                    "v12*": Decimal("0.2896"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.396"),
                },
                {
                    "Vf": Decimal("0.05"),
                    "E1*\n(GPa)": Decimal("183.500"),
                    "E2*\n(GPa)": Decimal("20.250"),
                    "G12*\n(GPa)": Decimal("15.216"),
                    "v12*": Decimal("0.2895"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.449"),
                },
                {
                    "Vf": Decimal("0.06"),
                    "E1*\n(GPa)": Decimal("184.200"),
                    "E2*\n(GPa)": Decimal("20.300"),
                    "G12*\n(GPa)": Decimal("15.259"),
                    "v12*": Decimal("0.2894"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.501"),
                },
                {
                    "Vf": Decimal("0.07"),
                    "E1*\n(GPa)": Decimal("184.900"),
                    "E2*\n(GPa)": Decimal("20.350"),
                    "G12*\n(GPa)": Decimal("15.303"),
                    "v12*": Decimal("0.2893"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.554"),
                },
                {
                    "Vf": Decimal("0.08"),
                    "E1*\n(GPa)": Decimal("185.600"),
                    "E2*\n(GPa)": Decimal("20.400"),
                    "G12*\n(GPa)": Decimal("15.347"),
                    "v12*": Decimal("0.2892"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.607"),
                },
                {
                    "Vf": Decimal("0.09"),
                    "E1*\n(GPa)": Decimal("186.300"),
                    "E2*\n(GPa)": Decimal("20.450"),
                    "G12*\n(GPa)": Decimal("15.391"),
                    "v12*": Decimal("0.2891"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.660"),
                },
                {
                    "Vf": Decimal("0.1"),
                    "E1*\n(GPa)": Decimal("187.000"),
                    "E2*\n(GPa)": Decimal("20.500"),
                    "G12*\n(GPa)": Decimal("15.435"),
                    "v12*": Decimal("0.2890"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.714"),
                },
                {
                    "Vf": Decimal("0.11"),
                    "E1*\n(GPa)": Decimal("187.700"),
                    "E2*\n(GPa)": Decimal("20.550"),
                    "G12*\n(GPa)": Decimal("15.479"),
                    "v12*": Decimal("0.2889"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.768"),
                },
                {
                    "Vf": Decimal("0.12"),
                    "E1*\n(GPa)": Decimal("188.400"),
                    "E2*\n(GPa)": Decimal("20.600"),
                    "G12*\n(GPa)": Decimal("15.523"),
                    "v12*": Decimal("0.2888"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.822"),
                },
                {
                    "Vf": Decimal("0.13"),
                    "E1*\n(GPa)": Decimal("189.100"),
                    "E2*\n(GPa)": Decimal("20.650"),
                    "G12*\n(GPa)": Decimal("15.568"),
                    "v12*": Decimal("0.2887"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.876"),
                },
                {
                    "Vf": Decimal("0.14"),
                    "E1*\n(GPa)": Decimal("189.800"),
                    "E2*\n(GPa)": Decimal("20.700"),
                    "G12*\n(GPa)": Decimal("15.612"),
                    "v12*": Decimal("0.2886"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.931"),
                },
                {
                    "Vf": Decimal("0.15"),
                    "E1*\n(GPa)": Decimal("190.500"),
                    "E2*\n(GPa)": Decimal("20.750"),
                    "G12*\n(GPa)": Decimal("15.657"),
                    "v12*": Decimal("0.2885"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.986"),
                },
                {
                    "Vf": Decimal("0.16"),
                    "E1*\n(GPa)": Decimal("191.200"),
                    "E2*\n(GPa)": Decimal("20.800"),
                    "G12*\n(GPa)": Decimal("15.702"),
                    "v12*": Decimal("0.2884"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.041"),
                },
                {
                    "Vf": Decimal("0.17"),
                    "E1*\n(GPa)": Decimal("191.900"),
                    "E2*\n(GPa)": Decimal("20.850"),
                    "G12*\n(GPa)": Decimal("15.747"),
                    "v12*": Decimal("0.2883"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.097"),
                },
                {
                    "Vf": Decimal("0.18"),
                    "E1*\n(GPa)": Decimal("192.600"),
                    "E2*\n(GPa)": Decimal("20.900"),
                    "G12*\n(GPa)": Decimal("15.792"),
                    "v12*": Decimal("0.2882"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.153"),
                },
                {
                    "Vf": Decimal("0.19"),
                    "E1*\n(GPa)": Decimal("193.300"),
                    "E2*\n(GPa)": Decimal("20.950"),
                    "G12*\n(GPa)": Decimal("15.837"),
                    "v12*": Decimal("0.2881"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.209"),
                },
                {
                    "Vf": Decimal("0.2"),
                    "E1*\n(GPa)": Decimal("194.000"),
                    "E2*\n(GPa)": Decimal("21.000"),
                    "G12*\n(GPa)": Decimal("15.882"),
                    "v12*": Decimal("0.2880"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.265"),
                },
                {
                    "Vf": Decimal("0.21"),
                    "E1*\n(GPa)": Decimal("194.700"),
                    "E2*\n(GPa)": Decimal("21.050"),
                    "G12*\n(GPa)": Decimal("15.928"),
                    "v12*": Decimal("0.2879"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.322"),
                },
                {
                    "Vf": Decimal("0.22"),
                    "E1*\n(GPa)": Decimal("195.400"),
                    "E2*\n(GPa)": Decimal("21.100"),
                    "G12*\n(GPa)": Decimal("15.973"),
                    "v12*": Decimal("0.2878"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.379"),
                },
                {
                    "Vf": Decimal("0.23"),
                    "E1*\n(GPa)": Decimal("196.100"),
                    "E2*\n(GPa)": Decimal("21.150"),
                    "G12*\n(GPa)": Decimal("16.019"),
                    "v12*": Decimal("0.2877"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.437"),
                },
                {
                    "Vf": Decimal("0.24"),
                    "E1*\n(GPa)": Decimal("196.800"),
                    "E2*\n(GPa)": Decimal("21.200"),
                    "G12*\n(GPa)": Decimal("16.065"),
                    "v12*": Decimal("0.2876"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.494"),
                },
                {
                    "Vf": Decimal("0.25"),
                    "E1*\n(GPa)": Decimal("197.500"),
                    "E2*\n(GPa)": Decimal("21.250"),
                    "G12*\n(GPa)": Decimal("16.111"),
                    "v12*": Decimal("0.2875"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.552"),
                },
                {
                    "Vf": Decimal("0.26"),
                    "E1*\n(GPa)": Decimal("198.200"),
                    "E2*\n(GPa)": Decimal("21.300"),
                    "G12*\n(GPa)": Decimal("16.157"),
                    "v12*": Decimal("0.2874"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.611"),
                },
                {
                    "Vf": Decimal("0.27"),
                    "E1*\n(GPa)": Decimal("198.900"),
                    "E2*\n(GPa)": Decimal("21.350"),
                    "G12*\n(GPa)": Decimal("16.204"),
                    "v12*": Decimal("0.2873"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.669"),
                },
                {
                    "Vf": Decimal("0.28"),
                    "E1*\n(GPa)": Decimal("199.600"),
                    "E2*\n(GPa)": Decimal("21.400"),
                    "G12*\n(GPa)": Decimal("16.250"),
                    "v12*": Decimal("0.2872"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.728"),
                },
                {
                    "Vf": Decimal("0.29"),
                    "E1*\n(GPa)": Decimal("200.300"),
                    "E2*\n(GPa)": Decimal("21.450"),
                    "G12*\n(GPa)": Decimal("16.297"),
                    "v12*": Decimal("0.2871"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.788"),
                },
                {
                    "Vf": Decimal("0.3"),
                    "E1*\n(GPa)": Decimal("201.000"),
                    "E2*\n(GPa)": Decimal("21.500"),
                    "G12*\n(GPa)": Decimal("16.343"),
                    "v12*": Decimal("0.2870"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.847"),
                },
                {
                    "Vf": Decimal("0.31"),
                    "E1*\n(GPa)": Decimal("201.700"),
                    "E2*\n(GPa)": Decimal("21.550"),
                    "G12*\n(GPa)": Decimal("16.390"),
                    "v12*": Decimal("0.2869"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.907"),
                },
                {
                    "Vf": Decimal("0.32"),
                    "E1*\n(GPa)": Decimal("202.400"),
                    "E2*\n(GPa)": Decimal("21.600"),
                    "G12*\n(GPa)": Decimal("16.437"),
                    "v12*": Decimal("0.2868"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("11.967"),
                },
                {
                    "Vf": Decimal("0.33"),
                    "E1*\n(GPa)": Decimal("203.100"),
                    "E2*\n(GPa)": Decimal("21.650"),
                    "G12*\n(GPa)": Decimal("16.484"),
                    "v12*": Decimal("0.2867"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.028"),
                },
                {
                    "Vf": Decimal("0.34"),
                    "E1*\n(GPa)": Decimal("203.800"),
                    "E2*\n(GPa)": Decimal("21.700"),
                    "G12*\n(GPa)": Decimal("16.532"),
                    "v12*": Decimal("0.2866"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.089"),
                },
                {
                    "Vf": Decimal("0.35"),
                    "E1*\n(GPa)": Decimal("204.500"),
                    "E2*\n(GPa)": Decimal("21.750"),
                    "G12*\n(GPa)": Decimal("16.579"),
                    "v12*": Decimal("0.2865"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.150"),
                },
                {
                    "Vf": Decimal("0.36"),
                    "E1*\n(GPa)": Decimal("205.200"),
                    "E2*\n(GPa)": Decimal("21.800"),
                    "G12*\n(GPa)": Decimal("16.627"),
                    "v12*": Decimal("0.2864"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.212"),
                },
                {
                    "Vf": Decimal("0.37"),
                    "E1*\n(GPa)": Decimal("205.900"),
                    "E2*\n(GPa)": Decimal("21.850"),
                    "G12*\n(GPa)": Decimal("16.674"),
                    "v12*": Decimal("0.2863"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.274"),
                },
                {
                    "Vf": Decimal("0.38"),
                    "E1*\n(GPa)": Decimal("206.600"),
                    "E2*\n(GPa)": Decimal("21.900"),
                    "G12*\n(GPa)": Decimal("16.722"),
                    "v12*": Decimal("0.2862"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.336"),
                },
                {
                    "Vf": Decimal("0.39"),
                    "E1*\n(GPa)": Decimal("207.300"),
                    "E2*\n(GPa)": Decimal("21.950"),
                    "G12*\n(GPa)": Decimal("16.770"),
                    "v12*": Decimal("0.2861"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.399"),
                },
                {
                    "Vf": Decimal("0.4"),
                    "E1*\n(GPa)": Decimal("208.000"),
                    "E2*\n(GPa)": Decimal("22.000"),
                    "G12*\n(GPa)": Decimal("16.818"),
                    "v12*": Decimal("0.2860"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.462"),
                },
                {
                    "Vf": Decimal("0.41"),
                    "E1*\n(GPa)": Decimal("208.700"),
                    "E2*\n(GPa)": Decimal("22.050"),
                    "G12*\n(GPa)": Decimal("16.866"),
                    "v12*": Decimal("0.2859"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.525"),
                },
                {
                    "Vf": Decimal("0.42"),
                    "E1*\n(GPa)": Decimal("209.400"),
                    "E2*\n(GPa)": Decimal("22.100"),
                    "G12*\n(GPa)": Decimal("16.915"),
                    "v12*": Decimal("0.2858"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.589"),
                },
                {
                    "Vf": Decimal("0.43"),
                    "E1*\n(GPa)": Decimal("210.100"),
                    "E2*\n(GPa)": Decimal("22.150"),
                    "G12*\n(GPa)": Decimal("16.963"),
                    "v12*": Decimal("0.2857"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.653"),
                },
                {
                    "Vf": Decimal("0.44"),
                    "E1*\n(GPa)": Decimal("210.800"),
                    "E2*\n(GPa)": Decimal("22.200"),
                    "G12*\n(GPa)": Decimal("17.012"),
                    "v12*": Decimal("0.2856"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.717"),
                },
                {
                    "Vf": Decimal("0.45"),
                    "E1*\n(GPa)": Decimal("211.500"),
                    "E2*\n(GPa)": Decimal("22.250"),
                    "G12*\n(GPa)": Decimal("17.061"),
                    "v12*": Decimal("0.2855"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.782"),
                },
                {
                    "Vf": Decimal("0.46"),
                    "E1*\n(GPa)": Decimal("212.200"),
                    "E2*\n(GPa)": Decimal("22.300"),
                    "G12*\n(GPa)": Decimal("17.110"),
                    "v12*": Decimal("0.2854"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.848"),
                },
                {
                    "Vf": Decimal("0.47"),
                    "E1*\n(GPa)": Decimal("212.900"),
                    "E2*\n(GPa)": Decimal("22.350"),
                    "G12*\n(GPa)": Decimal("17.159"),
                    "v12*": Decimal("0.2853"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.913"),
                },
                {
                    "Vf": Decimal("0.48"),
                    "E1*\n(GPa)": Decimal("213.600"),
                    "E2*\n(GPa)": Decimal("22.400"),
                    "G12*\n(GPa)": Decimal("17.209"),
                    "v12*": Decimal("0.2852"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("12.979"),
                },
                {
                    "Vf": Decimal("0.49"),
                    "E1*\n(GPa)": Decimal("214.300"),
                    "E2*\n(GPa)": Decimal("22.450"),
                    "G12*\n(GPa)": Decimal("17.258"),
                    "v12*": Decimal("0.2851"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("13.045"),
                },
                {
                    "Vf": Decimal("0.5"),
                    "E1*\n(GPa)": Decimal("215.000"),
                    "E2*\n(GPa)": Decimal("22.500"),
                    "G12*\n(GPa)": Decimal("17.308"),
                    "v12*": Decimal("0.2850"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("13.112"),
                },
                {
                    "Vf": Decimal("0.51"),
                    "E1*\n(GPa)": Decimal("215.700"),
                    "E2*\n(GPa)": Decimal("22.550"),
                    "G12*\n(GPa)": Decimal("17.357"),
                    "v12*": Decimal("0.2849"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("13.179"),
                },
                {
                    "Vf": Decimal("0.52"),
                    "E1*\n(GPa)": Decimal("216.400"),
                    "E2*\n(GPa)": Decimal("22.600"),
                    "G12*\n(GPa)": Decimal("17.407"),
                    "v12*": Decimal("0.2848"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("13.247"),
                },
                {
                    "Vf": Decimal("0.53"),
                    "E1*\n(GPa)": Decimal("217.100"),
                    "E2*\n(GPa)": Decimal("22.650"),
                    "G12*\n(GPa)": Decimal("17.457"),
                    "v12*": Decimal("0.2847"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("13.314"),
                },
                {
                    "Vf": Decimal("0.54"),
                    "E1*\n(GPa)": Decimal("217.800"),
                    "E2*\n(GPa)": Decimal("22.700"),
                    "G12*\n(GPa)": Decimal("17.508"),
                    "v12*": Decimal("0.2846"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("13.383"),
                },
                {
                    "Vf": Decimal("0.55"),
                    "E1*\n(GPa)": Decimal("218.500"),
                    "E2*\n(GPa)": Decimal("22.750"),
                    "G12*\n(GPa)": Decimal("17.558"),
                    "v12*": Decimal("0.2845"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("13.451"),
                },
                {
                    "Vf": Decimal("0.56"),
                    "E1*\n(GPa)": Decimal("219.200"),
                    "E2*\n(GPa)": Decimal("22.800"),
                    "G12*\n(GPa)": Decimal("17.609"),
                    "v12*": Decimal("0.2844"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("13.521"),
                },
                {
                    "Vf": Decimal("0.57"),
                    "E1*\n(GPa)": Decimal("219.900"),
                    "E2*\n(GPa)": Decimal("22.850"),
                    "G12*\n(GPa)": Decimal("17.659"),
                    "v12*": Decimal("0.2843"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("13.590"),
                },
                {
                    "Vf": Decimal("0.58"),
                    "E1*\n(GPa)": Decimal("220.600"),
                    "E2*\n(GPa)": Decimal("22.900"),
                    "G12*\n(GPa)": Decimal("17.710"),
                    "v12*": Decimal("0.2842"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("13.660"),
                },
                {
                    "Vf": Decimal("0.59"),
                    "E1*\n(GPa)": Decimal("221.300"),
                    "E2*\n(GPa)": Decimal("22.950"),
                    "G12*\n(GPa)": Decimal("17.761"),
                    "v12*": Decimal("0.2841"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("13.730"),
                },
                {
                    "Vf": Decimal("0.6"),
                    "E1*\n(GPa)": Decimal("222.000"),
                    "E2*\n(GPa)": Decimal("23.000"),
                    "G12*\n(GPa)": Decimal("17.812"),
                    "v12*": Decimal("0.2840"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("13.801"),
                },
                {
                    "Vf": Decimal("0.61"),
                    "E1*\n(GPa)": Decimal("222.700"),
                    "E2*\n(GPa)": Decimal("23.050"),
                    "G12*\n(GPa)": Decimal("17.864"),
                    "v12*": Decimal("0.2839"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("13.872"),
                },
                {
                    "Vf": Decimal("0.62"),
                    "E1*\n(GPa)": Decimal("223.400"),
                    "E2*\n(GPa)": Decimal("23.100"),
                    "G12*\n(GPa)": Decimal("17.915"),
                    "v12*": Decimal("0.2838"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("13.944"),
                },
                {
                    "Vf": Decimal("0.63"),
                    "E1*\n(GPa)": Decimal("224.100"),
                    "E2*\n(GPa)": Decimal("23.150"),
                    "G12*\n(GPa)": Decimal("17.967"),
                    "v12*": Decimal("0.2837"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("14.016"),
                },
                {
                    "Vf": Decimal("0.64"),
                    "E1*\n(GPa)": Decimal("224.800"),
                    "E2*\n(GPa)": Decimal("23.200"),
                    "G12*\n(GPa)": Decimal("18.019"),
                    "v12*": Decimal("0.2836"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("14.088"),
                },
                {
                    "Vf": Decimal("0.65"),
                    "E1*\n(GPa)": Decimal("225.500"),
                    "E2*\n(GPa)": Decimal("23.250"),
                    "G12*\n(GPa)": Decimal("18.071"),
                    "v12*": Decimal("0.2835"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("14.161"),
                },
                {
                    "Vf": Decimal("0.66"),
                    "E1*\n(GPa)": Decimal("226.200"),
                    "E2*\n(GPa)": Decimal("23.300"),
                    "G12*\n(GPa)": Decimal("18.123"),
                    "v12*": Decimal("0.2834"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("14.234"),
                },
                {
                    "Vf": Decimal("0.67"),
                    "E1*\n(GPa)": Decimal("226.900"),
                    "E2*\n(GPa)": Decimal("23.350"),
                    "G12*\n(GPa)": Decimal("18.175"),
                    "v12*": Decimal("0.2833"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("14.308"),
                },
                {
                    "Vf": Decimal("0.68"),
                    "E1*\n(GPa)": Decimal("227.600"),
                    "E2*\n(GPa)": Decimal("23.400"),
                    "G12*\n(GPa)": Decimal("18.228"),
                    "v12*": Decimal("0.2832"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("14.382"),
                },
                {
                    "Vf": Decimal("0.69"),
                    "E1*\n(GPa)": Decimal("228.300"),
                    "E2*\n(GPa)": Decimal("23.450"),
                    "G12*\n(GPa)": Decimal("18.281"),
                    "v12*": Decimal("0.2831"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("14.457"),
                },
                {
                    "Vf": Decimal("0.7"),
                    "E1*\n(GPa)": Decimal("229.000"),
                    "E2*\n(GPa)": Decimal("23.500"),
                    "G12*\n(GPa)": Decimal("18.333"),
                    "v12*": Decimal("0.2830"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("14.532"),
                },
                {
                    "Vf": Decimal("0.71"),
                    "E1*\n(GPa)": Decimal("229.700"),
                    "E2*\n(GPa)": Decimal("23.550"),
                    "G12*\n(GPa)": Decimal("18.386"),
                    "v12*": Decimal("0.2829"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("14.608"),
                },
                {
                    "Vf": Decimal("0.72"),
                    "E1*\n(GPa)": Decimal("230.400"),
                    "E2*\n(GPa)": Decimal("23.600"),
                    "G12*\n(GPa)": Decimal("18.439"),
                    "v12*": Decimal("0.2828"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("14.684"),
                },
                {
                    "Vf": Decimal("0.73"),
                    "E1*\n(GPa)": Decimal("231.100"),
                    "E2*\n(GPa)": Decimal("23.650"),
                    "G12*\n(GPa)": Decimal("18.493"),
                    "v12*": Decimal("0.2827"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("14.760"),
                },
                {
                    "Vf": Decimal("0.74"),
                    "E1*\n(GPa)": Decimal("231.800"),
                    "E2*\n(GPa)": Decimal("23.700"),
                    "G12*\n(GPa)": Decimal("18.546"),
                    "v12*": Decimal("0.2826"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("14.837"),
                },
                {
                    "Vf": Decimal("0.75"),
                    "E1*\n(GPa)": Decimal("232.500"),
                    "E2*\n(GPa)": Decimal("23.750"),
                    "G12*\n(GPa)": Decimal("18.600"),
                    "v12*": Decimal("0.2825"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("14.915"),
                },
                {
                    "Vf": Decimal("0.76"),
                    "E1*\n(GPa)": Decimal("233.200"),
                    "E2*\n(GPa)": Decimal("23.800"),
                    "G12*\n(GPa)": Decimal("18.654"),
                    "v12*": Decimal("0.2824"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("14.993"),
                },
                {
                    "Vf": Decimal("0.77"),
                    "E1*\n(GPa)": Decimal("233.900"),
                    "E2*\n(GPa)": Decimal("23.850"),
                    "G12*\n(GPa)": Decimal("18.708"),
                    "v12*": Decimal("0.2823"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("15.071"),
                },
                {
                    "Vf": Decimal("0.78"),
                    "E1*\n(GPa)": Decimal("234.600"),
                    "E2*\n(GPa)": Decimal("23.900"),
                    "G12*\n(GPa)": Decimal("18.762"),
                    "v12*": Decimal("0.2822"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("15.150"),
                },
                {
                    "Vf": Decimal("0.79"),
                    "E1*\n(GPa)": Decimal("235.300"),
                    "E2*\n(GPa)": Decimal("23.950"),
                    "G12*\n(GPa)": Decimal("18.816"),
                    "v12*": Decimal("0.2821"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("15.230"),
                },
                {
                    "Vf": Decimal("0.8"),
                    "E1*\n(GPa)": Decimal("236.000"),
                    "E2*\n(GPa)": Decimal("24.000"),
                    "G12*\n(GPa)": Decimal("18.871"),
                    "v12*": Decimal("0.2820"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("15.310"),
                },
                {
                    "Vf": Decimal("0.81"),
                    "E1*\n(GPa)": Decimal("236.700"),
                    "E2*\n(GPa)": Decimal("24.050"),
                    "G12*\n(GPa)": Decimal("18.926"),
                    "v12*": Decimal("0.2819"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("15.390"),
                },
                {
                    "Vf": Decimal("0.82"),
                    "E1*\n(GPa)": Decimal("237.400"),
                    "E2*\n(GPa)": Decimal("24.100"),
                    "G12*\n(GPa)": Decimal("18.981"),
                    "v12*": Decimal("0.2818"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("15.471"),
                },
                {
                    "Vf": Decimal("0.83"),
                    "E1*\n(GPa)": Decimal("238.100"),
                    "E2*\n(GPa)": Decimal("24.150"),
                    "G12*\n(GPa)": Decimal("19.036"),
                    "v12*": Decimal("0.2817"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("15.553"),
                },
                {
                    "Vf": Decimal("0.84"),
                    "E1*\n(GPa)": Decimal("238.800"),
                    "E2*\n(GPa)": Decimal("24.200"),
                    "G12*\n(GPa)": Decimal("19.091"),
                    "v12*": Decimal("0.2816"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("15.635"),
                },
                {
                    "Vf": Decimal("0.85"),
                    "E1*\n(GPa)": Decimal("239.500"),
                    "E2*\n(GPa)": Decimal("24.250"),
                    "G12*\n(GPa)": Decimal("19.146"),
                    "v12*": Decimal("0.2815"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("15.717"),
                },
                {
                    "Vf": Decimal("0.86"),
                    "E1*\n(GPa)": Decimal("240.200"),
                    "E2*\n(GPa)": Decimal("24.300"),
                    "G12*\n(GPa)": Decimal("19.202"),
                    "v12*": Decimal("0.2814"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("15.801"),
                },
                {
                    "Vf": Decimal("0.87"),
                    "E1*\n(GPa)": Decimal("240.900"),
                    "E2*\n(GPa)": Decimal("24.350"),
                    "G12*\n(GPa)": Decimal("19.258"),
                    "v12*": Decimal("0.2813"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("15.884"),
                },
                {
                    "Vf": Decimal("0.88"),
                    "E1*\n(GPa)": Decimal("241.600"),
                    "E2*\n(GPa)": Decimal("24.400"),
                    "G12*\n(GPa)": Decimal("19.314"),
                    "v12*": Decimal("0.2812"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("15.968"),
                },
                {
                    "Vf": Decimal("0.89"),
                    "E1*\n(GPa)": Decimal("242.300"),
                    "E2*\n(GPa)": Decimal("24.450"),
                    "G12*\n(GPa)": Decimal("19.370"),
                    "v12*": Decimal("0.2811"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("16.053"),
                },
                {
                    "Vf": Decimal("0.9"),
                    "E1*\n(GPa)": Decimal("243.000"),
                    "E2*\n(GPa)": Decimal("24.500"),
                    "G12*\n(GPa)": Decimal("19.426"),
                    "v12*": Decimal("0.2810"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("16.138"),
                },
                {
                    "Vf": Decimal("0.91"),
                    "E1*\n(GPa)": Decimal("243.700"),
                    "E2*\n(GPa)": Decimal("24.550"),
                    "G12*\n(GPa)": Decimal("19.483"),
                    "v12*": Decimal("0.2809"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("16.224"),
                },
                {
                    "Vf": Decimal("0.92"),
                    "E1*\n(GPa)": Decimal("244.400"),
                    "E2*\n(GPa)": Decimal("24.600"),
                    "G12*\n(GPa)": Decimal("19.539"),
                    "v12*": Decimal("0.2808"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("16.311"),
                },
                {
                    "Vf": Decimal("0.93"),
                    "E1*\n(GPa)": Decimal("245.100"),
                    "E2*\n(GPa)": Decimal("24.650"),
                    "G12*\n(GPa)": Decimal("19.596"),
                    "v12*": Decimal("0.2807"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("16.398"),
                },
                {
                    "Vf": Decimal("0.94"),
                    "E1*\n(GPa)": Decimal("245.800"),
                    "E2*\n(GPa)": Decimal("24.700"),
                    "G12*\n(GPa)": Decimal("19.653"),
                    "v12*": Decimal("0.2806"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("16.485"),
                },
                {
                    "Vf": Decimal("0.95"),
                    "E1*\n(GPa)": Decimal("246.500"),
                    "E2*\n(GPa)": Decimal("24.750"),
                    "G12*\n(GPa)": Decimal("19.711"),
                    "v12*": Decimal("0.2805"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("16.573"),
                },
                {
                    "Vf": Decimal("0.96"),
                    "E1*\n(GPa)": Decimal("247.200"),
                    "E2*\n(GPa)": Decimal("24.800"),
                    "G12*\n(GPa)": Decimal("19.768"),
                    "v12*": Decimal("0.2804"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("16.662"),
                },
                {
                    "Vf": Decimal("0.97"),
                    "E1*\n(GPa)": Decimal("247.900"),
                    "E2*\n(GPa)": Decimal("24.850"),
                    "G12*\n(GPa)": Decimal("19.826"),
                    "v12*": Decimal("0.2803"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("16.751"),
                },
                {
                    "Vf": Decimal("0.98"),
                    "E1*\n(GPa)": Decimal("248.600"),
                    "E2*\n(GPa)": Decimal("24.900"),
                    "G12*\n(GPa)": Decimal("19.884"),
                    "v12*": Decimal("0.2802"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("16.841"),
                },
                {
                    "Vf": Decimal("0.99"),
                    "E1*\n(GPa)": Decimal("249.300"),
                    "E2*\n(GPa)": Decimal("24.950"),
                    "G12*\n(GPa)": Decimal("19.942"),
                    "v12*": Decimal("0.2801"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("16.932"),
                },
                {
                    "Vf": Decimal("1"),
                    "E1*\n(GPa)": Decimal("250.000"),
                    "E2*\n(GPa)": Decimal("25.000"),
                    "G12*\n(GPa)": Decimal("20.000"),
                    "v12*": Decimal("0.2800"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("17.023"),
                },
            ],
            "Carbon-Graphite_eff_moduli.csv",
        )
        result4 = _get_effective_elastic_moduli_and_filename(composite4)
        assert result4 == (
            [
                {
                    "Vf": Decimal("0"),
                    "E1*\n(GPa)": Decimal("180.000"),
                    "E2*\n(GPa)": Decimal("20.000"),
                    "G12*\n(GPa)": Decimal("15.000"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("10.000"),
                    "K23*\n(GPa)": Decimal("10.190"),
                },
                {
                    "Vf": Decimal("0.01"),
                    "E1*\n(GPa)": Decimal("179.400"),
                    "E2*\n(GPa)": Decimal("20.261"),
                    "G12*\n(GPa)": Decimal("15.154"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("10.099"),
                    "K23*\n(GPa)": Decimal("10.360"),
                },
                {
                    "Vf": Decimal("0.02"),
                    "E1*\n(GPa)": Decimal("178.800"),
                    "E2*\n(GPa)": Decimal("20.526"),
                    "G12*\n(GPa)": Decimal("15.311"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("10.199"),
                    "K23*\n(GPa)": Decimal("10.532"),
                },
                {
                    "Vf": Decimal("0.03"),
                    "E1*\n(GPa)": Decimal("178.200"),
                    "E2*\n(GPa)": Decimal("20.793"),
                    "G12*\n(GPa)": Decimal("15.468"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("10.300"),
                    "K23*\n(GPa)": Decimal("10.707"),
                },
                {
                    "Vf": Decimal("0.04"),
                    "E1*\n(GPa)": Decimal("177.600"),
                    "E2*\n(GPa)": Decimal("21.066"),
                    "G12*\n(GPa)": Decimal("15.628"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("10.403"),
                    "K23*\n(GPa)": Decimal("10.886"),
                },
                {
                    "Vf": Decimal("0.05"),
                    "E1*\n(GPa)": Decimal("177.000"),
                    "E2*\n(GPa)": Decimal("21.342"),
                    "G12*\n(GPa)": Decimal("15.789"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("10.508"),
                    "K23*\n(GPa)": Decimal("11.067"),
                },
                {
                    "Vf": Decimal("0.06"),
                    "E1*\n(GPa)": Decimal("176.400"),
                    "E2*\n(GPa)": Decimal("21.622"),
                    "G12*\n(GPa)": Decimal("15.951"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("10.614"),
                    "K23*\n(GPa)": Decimal("11.252"),
                },
                {
                    "Vf": Decimal("0.07"),
                    "E1*\n(GPa)": Decimal("175.800"),
                    "E2*\n(GPa)": Decimal("21.907"),
                    "G12*\n(GPa)": Decimal("16.116"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("10.722"),
                    "K23*\n(GPa)": Decimal("11.440"),
                },
                {
                    "Vf": Decimal("0.08"),
                    "E1*\n(GPa)": Decimal("175.200"),
                    "E2*\n(GPa)": Decimal("22.196"),
                    "G12*\n(GPa)": Decimal("16.282"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("10.832"),
                    "K23*\n(GPa)": Decimal("11.631"),
                },
                {
                    "Vf": Decimal("0.09"),
                    "E1*\n(GPa)": Decimal("174.600"),
                    "E2*\n(GPa)": Decimal("22.488"),
                    "G12*\n(GPa)": Decimal("16.450"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("10.943"),
                    "K23*\n(GPa)": Decimal("11.826"),
                },
                {
                    "Vf": Decimal("0.1"),
                    "E1*\n(GPa)": Decimal("174.000"),
                    "E2*\n(GPa)": Decimal("22.786"),
                    "G12*\n(GPa)": Decimal("16.620"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("11.056"),
                    "K23*\n(GPa)": Decimal("12.024"),
                },
                {
                    "Vf": Decimal("0.11"),
                    "E1*\n(GPa)": Decimal("173.400"),
                    "E2*\n(GPa)": Decimal("23.088"),
                    "G12*\n(GPa)": Decimal("16.792"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("11.171"),
                    "K23*\n(GPa)": Decimal("12.226"),
                },
                {
                    "Vf": Decimal("0.12"),
                    "E1*\n(GPa)": Decimal("172.800"),
                    "E2*\n(GPa)": Decimal("23.395"),
                    "G12*\n(GPa)": Decimal("16.965"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("11.288"),
                    "K23*\n(GPa)": Decimal("12.432"),
                },
                {
                    "Vf": Decimal("0.13"),
                    "E1*\n(GPa)": Decimal("172.200"),
                    "E2*\n(GPa)": Decimal("23.706"),
                    "G12*\n(GPa)": Decimal("17.140"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("11.406"),
                    "K23*\n(GPa)": Decimal("12.641"),
                },
                {
                    "Vf": Decimal("0.14"),
                    "E1*\n(GPa)": Decimal("171.600"),
                    "E2*\n(GPa)": Decimal("24.023"),
                    "G12*\n(GPa)": Decimal("17.318"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("11.527"),
                    "K23*\n(GPa)": Decimal("12.855"),
                },
                {
                    "Vf": Decimal("0.15"),
                    "E1*\n(GPa)": Decimal("171.000"),
                    "E2*\n(GPa)": Decimal("24.344"),
                    "G12*\n(GPa)": Decimal("17.497"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("11.649"),
                    "K23*\n(GPa)": Decimal("13.072"),
                },
                {
                    "Vf": Decimal("0.16"),
                    "E1*\n(GPa)": Decimal("170.400"),
                    "E2*\n(GPa)": Decimal("24.672"),
                    "G12*\n(GPa)": Decimal("17.679"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("11.774"),
                    "K23*\n(GPa)": Decimal("13.294"),
                },
                {
                    "Vf": Decimal("0.17"),
                    "E1*\n(GPa)": Decimal("169.800"),
                    "E2*\n(GPa)": Decimal("25.004"),
                    "G12*\n(GPa)": Decimal("17.862"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("11.901"),
                    "K23*\n(GPa)": Decimal("13.520"),
                },
                {
                    "Vf": Decimal("0.18"),
                    "E1*\n(GPa)": Decimal("169.200"),
                    "E2*\n(GPa)": Decimal("25.341"),
                    "G12*\n(GPa)": Decimal("18.047"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("12.029"),
                    "K23*\n(GPa)": Decimal("13.750"),
                },
                {
                    "Vf": Decimal("0.19"),
                    "E1*\n(GPa)": Decimal("168.600"),
                    "E2*\n(GPa)": Decimal("25.684"),
                    "G12*\n(GPa)": Decimal("18.235"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("12.160"),
                    "K23*\n(GPa)": Decimal("13.985"),
                },
                {
                    "Vf": Decimal("0.2"),
                    "E1*\n(GPa)": Decimal("168.000"),
                    "E2*\n(GPa)": Decimal("26.035"),
                    "G12*\n(GPa)": Decimal("18.425"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("12.294"),
                    "K23*\n(GPa)": Decimal("14.225"),
                },
                {
                    "Vf": Decimal("0.21"),
                    "E1*\n(GPa)": Decimal("167.400"),
                    "E2*\n(GPa)": Decimal("26.389"),
                    "G12*\n(GPa)": Decimal("18.616"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("12.429"),
                    "K23*\n(GPa)": Decimal("14.469"),
                },
                {
                    "Vf": Decimal("0.22"),
                    "E1*\n(GPa)": Decimal("166.800"),
                    "E2*\n(GPa)": Decimal("26.751"),
                    "G12*\n(GPa)": Decimal("18.811"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("12.567"),
                    "K23*\n(GPa)": Decimal("14.719"),
                },
                {
                    "Vf": Decimal("0.23"),
                    "E1*\n(GPa)": Decimal("166.200"),
                    "E2*\n(GPa)": Decimal("27.117"),
                    "G12*\n(GPa)": Decimal("19.007"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("12.707"),
                    "K23*\n(GPa)": Decimal("14.973"),
                },
                {
                    "Vf": Decimal("0.24"),
                    "E1*\n(GPa)": Decimal("165.600"),
                    "E2*\n(GPa)": Decimal("27.492"),
                    "G12*\n(GPa)": Decimal("19.206"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("12.850"),
                    "K23*\n(GPa)": Decimal("15.233"),
                },
                {
                    "Vf": Decimal("0.25"),
                    "E1*\n(GPa)": Decimal("165.000"),
                    "E2*\n(GPa)": Decimal("27.872"),
                    "G12*\n(GPa)": Decimal("19.407"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("12.995"),
                    "K23*\n(GPa)": Decimal("15.499"),
                },
                {
                    "Vf": Decimal("0.26"),
                    "E1*\n(GPa)": Decimal("164.400"),
                    "E2*\n(GPa)": Decimal("28.260"),
                    "G12*\n(GPa)": Decimal("19.610"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("13.143"),
                    "K23*\n(GPa)": Decimal("15.770"),
                },
                {
                    "Vf": Decimal("0.27"),
                    "E1*\n(GPa)": Decimal("163.800"),
                    "E2*\n(GPa)": Decimal("28.655"),
                    "G12*\n(GPa)": Decimal("19.816"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("13.294"),
                    "K23*\n(GPa)": Decimal("16.047"),
                },
                {
                    "Vf": Decimal("0.28"),
                    "E1*\n(GPa)": Decimal("163.200"),
                    "E2*\n(GPa)": Decimal("29.055"),
                    "G12*\n(GPa)": Decimal("20.024"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("13.447"),
                    "K23*\n(GPa)": Decimal("16.329"),
                },
                {
                    "Vf": Decimal("0.29"),
                    "E1*\n(GPa)": Decimal("162.600"),
                    "E2*\n(GPa)": Decimal("29.466"),
                    "G12*\n(GPa)": Decimal("20.235"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("13.604"),
                    "K23*\n(GPa)": Decimal("16.619"),
                },
                {
                    "Vf": Decimal("0.3"),
                    "E1*\n(GPa)": Decimal("162.000"),
                    "E2*\n(GPa)": Decimal("29.882"),
                    "G12*\n(GPa)": Decimal("20.448"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("13.763"),
                    "K23*\n(GPa)": Decimal("16.914"),
                },
                {
                    "Vf": Decimal("0.31"),
                    "E1*\n(GPa)": Decimal("161.400"),
                    "E2*\n(GPa)": Decimal("30.307"),
                    "G12*\n(GPa)": Decimal("20.664"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("13.925"),
                    "K23*\n(GPa)": Decimal("17.216"),
                },
                {
                    "Vf": Decimal("0.32"),
                    "E1*\n(GPa)": Decimal("160.800"),
                    "E2*\n(GPa)": Decimal("30.741"),
                    "G12*\n(GPa)": Decimal("20.882"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("14.091"),
                    "K23*\n(GPa)": Decimal("17.525"),
                },
                {
                    "Vf": Decimal("0.33"),
                    "E1*\n(GPa)": Decimal("160.200"),
                    "E2*\n(GPa)": Decimal("31.181"),
                    "G12*\n(GPa)": Decimal("21.104"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("14.259"),
                    "K23*\n(GPa)": Decimal("17.841"),
                },
                {
                    "Vf": Decimal("0.34"),
                    "E1*\n(GPa)": Decimal("159.600"),
                    "E2*\n(GPa)": Decimal("31.632"),
                    "G12*\n(GPa)": Decimal("21.327"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("14.431"),
                    "K23*\n(GPa)": Decimal("18.165"),
                },
                {
                    "Vf": Decimal("0.35"),
                    "E1*\n(GPa)": Decimal("159.000"),
                    "E2*\n(GPa)": Decimal("32.091"),
                    "G12*\n(GPa)": Decimal("21.554"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("14.606"),
                    "K23*\n(GPa)": Decimal("18.496"),
                },
                {
                    "Vf": Decimal("0.36"),
                    "E1*\n(GPa)": Decimal("158.400"),
                    "E2*\n(GPa)": Decimal("32.559"),
                    "G12*\n(GPa)": Decimal("21.784"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("14.785"),
                    "K23*\n(GPa)": Decimal("18.835"),
                },
                {
                    "Vf": Decimal("0.37"),
                    "E1*\n(GPa)": Decimal("157.800"),
                    "E2*\n(GPa)": Decimal("33.037"),
                    "G12*\n(GPa)": Decimal("22.016"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("14.967"),
                    "K23*\n(GPa)": Decimal("19.182"),
                },
                {
                    "Vf": Decimal("0.38"),
                    "E1*\n(GPa)": Decimal("157.200"),
                    "E2*\n(GPa)": Decimal("33.524"),
                    "G12*\n(GPa)": Decimal("22.252"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("15.153"),
                    "K23*\n(GPa)": Decimal("19.537"),
                },
                {
                    "Vf": Decimal("0.39"),
                    "E1*\n(GPa)": Decimal("156.600"),
                    "E2*\n(GPa)": Decimal("34.022"),
                    "G12*\n(GPa)": Decimal("22.490"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("15.343"),
                    "K23*\n(GPa)": Decimal("19.902"),
                },
                {
                    "Vf": Decimal("0.4"),
                    "E1*\n(GPa)": Decimal("156.000"),
                    "E2*\n(GPa)": Decimal("34.530"),
                    "G12*\n(GPa)": Decimal("22.732"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("15.537"),
                    "K23*\n(GPa)": Decimal("20.275"),
                },
                {
                    "Vf": Decimal("0.41"),
                    "E1*\n(GPa)": Decimal("155.400"),
                    "E2*\n(GPa)": Decimal("35.048"),
                    "G12*\n(GPa)": Decimal("22.977"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("15.734"),
                    "K23*\n(GPa)": Decimal("20.658"),
                },
                {
                    "Vf": Decimal("0.42"),
                    "E1*\n(GPa)": Decimal("154.800"),
                    "E2*\n(GPa)": Decimal("35.578"),
                    "G12*\n(GPa)": Decimal("23.224"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("15.936"),
                    "K23*\n(GPa)": Decimal("21.051"),
                },
                {
                    "Vf": Decimal("0.43"),
                    "E1*\n(GPa)": Decimal("154.200"),
                    "E2*\n(GPa)": Decimal("36.119"),
                    "G12*\n(GPa)": Decimal("23.476"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("16.142"),
                    "K23*\n(GPa)": Decimal("21.453"),
                },
                {
                    "Vf": Decimal("0.44"),
                    "E1*\n(GPa)": Decimal("153.600"),
                    "E2*\n(GPa)": Decimal("36.673"),
                    "G12*\n(GPa)": Decimal("23.730"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("16.353"),
                    "K23*\n(GPa)": Decimal("21.867"),
                },
                {
                    "Vf": Decimal("0.45"),
                    "E1*\n(GPa)": Decimal("153.000"),
                    "E2*\n(GPa)": Decimal("37.238"),
                    "G12*\n(GPa)": Decimal("23.988"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("16.568"),
                    "K23*\n(GPa)": Decimal("22.291"),
                },
                {
                    "Vf": Decimal("0.46"),
                    "E1*\n(GPa)": Decimal("152.400"),
                    "E2*\n(GPa)": Decimal("37.818"),
                    "G12*\n(GPa)": Decimal("24.249"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("16.789"),
                    "K23*\n(GPa)": Decimal("22.727"),
                },
                {
                    "Vf": Decimal("0.47"),
                    "E1*\n(GPa)": Decimal("151.800"),
                    "E2*\n(GPa)": Decimal("38.409"),
                    "G12*\n(GPa)": Decimal("24.514"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("17.014"),
                    "K23*\n(GPa)": Decimal("23.175"),
                },
                {
                    "Vf": Decimal("0.48"),
                    "E1*\n(GPa)": Decimal("151.200"),
                    "E2*\n(GPa)": Decimal("39.014"),
                    "G12*\n(GPa)": Decimal("24.782"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("17.244"),
                    "K23*\n(GPa)": Decimal("23.635"),
                },
                {
                    "Vf": Decimal("0.49"),
                    "E1*\n(GPa)": Decimal("150.600"),
                    "E2*\n(GPa)": Decimal("39.633"),
                    "G12*\n(GPa)": Decimal("25.055"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("17.479"),
                    "K23*\n(GPa)": Decimal("24.108"),
                },
                {
                    "Vf": Decimal("0.5"),
                    "E1*\n(GPa)": Decimal("150.000"),
                    "E2*\n(GPa)": Decimal("40.268"),
                    "G12*\n(GPa)": Decimal("25.330"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("17.720"),
                    "K23*\n(GPa)": Decimal("24.595"),
                },
                {
                    "Vf": Decimal("0.51"),
                    "E1*\n(GPa)": Decimal("149.400"),
                    "E2*\n(GPa)": Decimal("40.917"),
                    "G12*\n(GPa)": Decimal("25.610"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("17.966"),
                    "K23*\n(GPa)": Decimal("25.096"),
                },
                {
                    "Vf": Decimal("0.52"),
                    "E1*\n(GPa)": Decimal("148.800"),
                    "E2*\n(GPa)": Decimal("41.581"),
                    "G12*\n(GPa)": Decimal("25.894"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("18.218"),
                    "K23*\n(GPa)": Decimal("25.611"),
                },
                {
                    "Vf": Decimal("0.53"),
                    "E1*\n(GPa)": Decimal("148.200"),
                    "E2*\n(GPa)": Decimal("42.262"),
                    "G12*\n(GPa)": Decimal("26.181"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("18.476"),
                    "K23*\n(GPa)": Decimal("26.142"),
                },
                {
                    "Vf": Decimal("0.54"),
                    "E1*\n(GPa)": Decimal("147.600"),
                    "E2*\n(GPa)": Decimal("42.961"),
                    "G12*\n(GPa)": Decimal("26.473"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("18.741"),
                    "K23*\n(GPa)": Decimal("26.689"),
                },
                {
                    "Vf": Decimal("0.55"),
                    "E1*\n(GPa)": Decimal("147.000"),
                    "E2*\n(GPa)": Decimal("43.678"),
                    "G12*\n(GPa)": Decimal("26.769"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("19.012"),
                    "K23*\n(GPa)": Decimal("27.253"),
                },
                {
                    "Vf": Decimal("0.56"),
                    "E1*\n(GPa)": Decimal("146.400"),
                    "E2*\n(GPa)": Decimal("44.411"),
                    "G12*\n(GPa)": Decimal("27.069"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("19.289"),
                    "K23*\n(GPa)": Decimal("27.834"),
                },
                {
                    "Vf": Decimal("0.57"),
                    "E1*\n(GPa)": Decimal("145.800"),
                    "E2*\n(GPa)": Decimal("45.165"),
                    "G12*\n(GPa)": Decimal("27.373"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("19.574"),
                    "K23*\n(GPa)": Decimal("28.434"),
                },
                {
                    "Vf": Decimal("0.58"),
                    "E1*\n(GPa)": Decimal("145.200"),
                    "E2*\n(GPa)": Decimal("45.938"),
                    "G12*\n(GPa)": Decimal("27.682"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("19.866"),
                    "K23*\n(GPa)": Decimal("29.053"),
                },
                {
                    "Vf": Decimal("0.59"),
                    "E1*\n(GPa)": Decimal("144.600"),
                    "E2*\n(GPa)": Decimal("46.732"),
                    "G12*\n(GPa)": Decimal("27.995"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("20.165"),
                    "K23*\n(GPa)": Decimal("29.693"),
                },
                {
                    "Vf": Decimal("0.6"),
                    "E1*\n(GPa)": Decimal("144.000"),
                    "E2*\n(GPa)": Decimal("47.546"),
                    "G12*\n(GPa)": Decimal("28.313"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("20.472"),
                    "K23*\n(GPa)": Decimal("30.353"),
                },
                {
                    "Vf": Decimal("0.61"),
                    "E1*\n(GPa)": Decimal("143.400"),
                    "E2*\n(GPa)": Decimal("48.384"),
                    "G12*\n(GPa)": Decimal("28.636"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("20.788"),
                    "K23*\n(GPa)": Decimal("31.036"),
                },
                {
                    "Vf": Decimal("0.62"),
                    "E1*\n(GPa)": Decimal("142.800"),
                    "E2*\n(GPa)": Decimal("49.244"),
                    "G12*\n(GPa)": Decimal("28.964"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("21.111"),
                    "K23*\n(GPa)": Decimal("31.743"),
                },
                {
                    "Vf": Decimal("0.63"),
                    "E1*\n(GPa)": Decimal("142.200"),
                    "E2*\n(GPa)": Decimal("50.130"),
                    "G12*\n(GPa)": Decimal("29.296"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("21.444"),
                    "K23*\n(GPa)": Decimal("32.474"),
                },
                {
                    "Vf": Decimal("0.64"),
                    "E1*\n(GPa)": Decimal("141.600"),
                    "E2*\n(GPa)": Decimal("51.041"),
                    "G12*\n(GPa)": Decimal("29.634"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("21.786"),
                    "K23*\n(GPa)": Decimal("33.232"),
                },
                {
                    "Vf": Decimal("0.65"),
                    "E1*\n(GPa)": Decimal("141.000"),
                    "E2*\n(GPa)": Decimal("51.978"),
                    "G12*\n(GPa)": Decimal("29.977"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("22.137"),
                    "K23*\n(GPa)": Decimal("34.017"),
                },
                {
                    "Vf": Decimal("0.66"),
                    "E1*\n(GPa)": Decimal("140.400"),
                    "E2*\n(GPa)": Decimal("52.942"),
                    "G12*\n(GPa)": Decimal("30.325"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("22.498"),
                    "K23*\n(GPa)": Decimal("34.831"),
                },
                {
                    "Vf": Decimal("0.67"),
                    "E1*\n(GPa)": Decimal("139.800"),
                    "E2*\n(GPa)": Decimal("53.936"),
                    "G12*\n(GPa)": Decimal("30.678"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("22.870"),
                    "K23*\n(GPa)": Decimal("35.675"),
                },
                {
                    "Vf": Decimal("0.68"),
                    "E1*\n(GPa)": Decimal("139.200"),
                    "E2*\n(GPa)": Decimal("54.959"),
                    "G12*\n(GPa)": Decimal("31.038"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("23.252"),
                    "K23*\n(GPa)": Decimal("36.552"),
                },
                {
                    "Vf": Decimal("0.69"),
                    "E1*\n(GPa)": Decimal("138.600"),
                    "E2*\n(GPa)": Decimal("56.015"),
                    "G12*\n(GPa)": Decimal("31.402"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("23.646"),
                    "K23*\n(GPa)": Decimal("37.464"),
                },
                {
                    "Vf": Decimal("0.7"),
                    "E1*\n(GPa)": Decimal("138.000"),
                    "E2*\n(GPa)": Decimal("57.102"),
                    "G12*\n(GPa)": Decimal("31.773"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("24.051"),
                    "K23*\n(GPa)": Decimal("38.411"),
                },
                {
                    "Vf": Decimal("0.71"),
                    "E1*\n(GPa)": Decimal("137.400"),
                    "E2*\n(GPa)": Decimal("58.226"),
                    "G12*\n(GPa)": Decimal("32.150"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("24.469"),
                    "K23*\n(GPa)": Decimal("39.398"),
                },
                {
                    "Vf": Decimal("0.72"),
                    "E1*\n(GPa)": Decimal("136.800"),
                    "E2*\n(GPa)": Decimal("59.385"),
                    "G12*\n(GPa)": Decimal("32.532"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("24.900"),
                    "K23*\n(GPa)": Decimal("40.425"),
                },
                {
                    "Vf": Decimal("0.73"),
                    "E1*\n(GPa)": Decimal("136.200"),
                    "E2*\n(GPa)": Decimal("60.582"),
                    "G12*\n(GPa)": Decimal("32.921"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("25.344"),
                    "K23*\n(GPa)": Decimal("41.496"),
                },
                {
                    "Vf": Decimal("0.74"),
                    "E1*\n(GPa)": Decimal("135.600"),
                    "E2*\n(GPa)": Decimal("61.821"),
                    "G12*\n(GPa)": Decimal("33.317"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("25.803"),
                    "K23*\n(GPa)": Decimal("42.614"),
                },
                {
                    "Vf": Decimal("0.75"),
                    "E1*\n(GPa)": Decimal("135.000"),
                    "E2*\n(GPa)": Decimal("63.101"),
                    "G12*\n(GPa)": Decimal("33.719"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("26.276"),
                    "K23*\n(GPa)": Decimal("43.781"),
                },
                {
                    "Vf": Decimal("0.76"),
                    "E1*\n(GPa)": Decimal("134.400"),
                    "E2*\n(GPa)": Decimal("64.426"),
                    "G12*\n(GPa)": Decimal("34.127"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("26.765"),
                    "K23*\n(GPa)": Decimal("45.001"),
                },
                {
                    "Vf": Decimal("0.77"),
                    "E1*\n(GPa)": Decimal("133.800"),
                    "E2*\n(GPa)": Decimal("65.798"),
                    "G12*\n(GPa)": Decimal("34.543"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("27.271"),
                    "K23*\n(GPa)": Decimal("46.278"),
                },
                {
                    "Vf": Decimal("0.78"),
                    "E1*\n(GPa)": Decimal("133.200"),
                    "E2*\n(GPa)": Decimal("67.218"),
                    "G12*\n(GPa)": Decimal("34.966"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("27.793"),
                    "K23*\n(GPa)": Decimal("47.615"),
                },
                {
                    "Vf": Decimal("0.79"),
                    "E1*\n(GPa)": Decimal("132.600"),
                    "E2*\n(GPa)": Decimal("68.692"),
                    "G12*\n(GPa)": Decimal("35.396"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("28.334"),
                    "K23*\n(GPa)": Decimal("49.018"),
                },
                {
                    "Vf": Decimal("0.8"),
                    "E1*\n(GPa)": Decimal("132.000"),
                    "E2*\n(GPa)": Decimal("70.220"),
                    "G12*\n(GPa)": Decimal("35.833"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("28.894"),
                    "K23*\n(GPa)": Decimal("50.490"),
                },
                {
                    "Vf": Decimal("0.81"),
                    "E1*\n(GPa)": Decimal("131.400"),
                    "E2*\n(GPa)": Decimal("71.807"),
                    "G12*\n(GPa)": Decimal("36.278"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("29.474"),
                    "K23*\n(GPa)": Decimal("52.038"),
                },
                {
                    "Vf": Decimal("0.82"),
                    "E1*\n(GPa)": Decimal("130.800"),
                    "E2*\n(GPa)": Decimal("73.454"),
                    "G12*\n(GPa)": Decimal("36.731"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("30.075"),
                    "K23*\n(GPa)": Decimal("53.667"),
                },
                {
                    "Vf": Decimal("0.83"),
                    "E1*\n(GPa)": Decimal("130.200"),
                    "E2*\n(GPa)": Decimal("75.168"),
                    "G12*\n(GPa)": Decimal("37.192"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("30.699"),
                    "K23*\n(GPa)": Decimal("55.384"),
                },
                {
                    "Vf": Decimal("0.84"),
                    "E1*\n(GPa)": Decimal("129.600"),
                    "E2*\n(GPa)": Decimal("76.953"),
                    "G12*\n(GPa)": Decimal("37.661"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("31.347"),
                    "K23*\n(GPa)": Decimal("57.197"),
                },
                {
                    "Vf": Decimal("0.85"),
                    "E1*\n(GPa)": Decimal("129.000"),
                    "E2*\n(GPa)": Decimal("78.808"),
                    "G12*\n(GPa)": Decimal("38.139"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("32.019"),
                    "K23*\n(GPa)": Decimal("59.112"),
                },
                {
                    "Vf": Decimal("0.86"),
                    "E1*\n(GPa)": Decimal("128.400"),
                    "E2*\n(GPa)": Decimal("80.743"),
                    "G12*\n(GPa)": Decimal("38.626"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("32.718"),
                    "K23*\n(GPa)": Decimal("61.140"),
                },
                {
                    "Vf": Decimal("0.87"),
                    "E1*\n(GPa)": Decimal("127.800"),
                    "E2*\n(GPa)": Decimal("82.761"),
                    "G12*\n(GPa)": Decimal("39.122"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("33.445"),
                    "K23*\n(GPa)": Decimal("63.291"),
                },
                {
                    "Vf": Decimal("0.88"),
                    "E1*\n(GPa)": Decimal("127.200"),
                    "E2*\n(GPa)": Decimal("84.867"),
                    "G12*\n(GPa)": Decimal("39.626"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("34.202"),
                    "K23*\n(GPa)": Decimal("65.575"),
                },
                {
                    "Vf": Decimal("0.89"),
                    "E1*\n(GPa)": Decimal("126.600"),
                    "E2*\n(GPa)": Decimal("87.069"),
                    "G12*\n(GPa)": Decimal("40.141"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("34.991"),
                    "K23*\n(GPa)": Decimal("68.007"),
                },
                {
                    "Vf": Decimal("0.9"),
                    "E1*\n(GPa)": Decimal("126.000"),
                    "E2*\n(GPa)": Decimal("89.374"),
                    "G12*\n(GPa)": Decimal("40.665"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("35.814"),
                    "K23*\n(GPa)": Decimal("70.601"),
                },
                {
                    "Vf": Decimal("0.91"),
                    "E1*\n(GPa)": Decimal("125.400"),
                    "E2*\n(GPa)": Decimal("91.786"),
                    "G12*\n(GPa)": Decimal("41.199"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("36.673"),
                    "K23*\n(GPa)": Decimal("73.372"),
                },
                {
                    "Vf": Decimal("0.92"),
                    "E1*\n(GPa)": Decimal("124.800"),
                    "E2*\n(GPa)": Decimal("94.314"),
                    "G12*\n(GPa)": Decimal("41.744"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("37.570"),
                    "K23*\n(GPa)": Decimal("76.342"),
                },
                {
                    "Vf": Decimal("0.93"),
                    "E1*\n(GPa)": Decimal("124.200"),
                    "E2*\n(GPa)": Decimal("96.969"),
                    "G12*\n(GPa)": Decimal("42.299"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("38.509"),
                    "K23*\n(GPa)": Decimal("79.530"),
                },
                {
                    "Vf": Decimal("0.94"),
                    "E1*\n(GPa)": Decimal("123.600"),
                    "E2*\n(GPa)": Decimal("99.757"),
                    "G12*\n(GPa)": Decimal("42.865"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("39.491"),
                    "K23*\n(GPa)": Decimal("82.963"),
                },
                {
                    "Vf": Decimal("0.95"),
                    "E1*\n(GPa)": Decimal("123.000"),
                    "E2*\n(GPa)": Decimal("102.692"),
                    "G12*\n(GPa)": Decimal("43.443"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("40.521"),
                    "K23*\n(GPa)": Decimal("86.670"),
                },
                {
                    "Vf": Decimal("0.96"),
                    "E1*\n(GPa)": Decimal("122.400"),
                    "E2*\n(GPa)": Decimal("105.782"),
                    "G12*\n(GPa)": Decimal("44.032"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("41.601"),
                    "K23*\n(GPa)": Decimal("90.684"),
                },
                {
                    "Vf": Decimal("0.97"),
                    "E1*\n(GPa)": Decimal("121.800"),
                    "E2*\n(GPa)": Decimal("109.044"),
                    "G12*\n(GPa)": Decimal("44.633"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("42.736"),
                    "K23*\n(GPa)": Decimal("95.047"),
                },
                {
                    "Vf": Decimal("0.98"),
                    "E1*\n(GPa)": Decimal("121.200"),
                    "E2*\n(GPa)": Decimal("112.489"),
                    "G12*\n(GPa)": Decimal("45.246"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("43.929"),
                    "K23*\n(GPa)": Decimal("99.805"),
                },
                {
                    "Vf": Decimal("0.99"),
                    "E1*\n(GPa)": Decimal("120.600"),
                    "E2*\n(GPa)": Decimal("116.135"),
                    "G12*\n(GPa)": Decimal("45.873"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("45.186"),
                    "K23*\n(GPa)": Decimal("105.014"),
                },
                {
                    "Vf": Decimal("1"),
                    "E1*\n(GPa)": Decimal("120.000"),
                    "E2*\n(GPa)": Decimal("120.001"),
                    "G12*\n(GPa)": Decimal("46.512"),
                    "v12*": Decimal("0.2900"),
                    "G23*\n(GPa)": Decimal("46.512"),
                    "K23*\n(GPa)": Decimal("110.742"),
                },
            ],
            "Fiberglass-Graphite_eff_moduli.csv",
        )

    def test_get_effective_elastic_moduli_and_filename_output_with_invalid_inputs(
            self, fiberglass, none_arg
    ):
        """
        Test output of ``_get_effective_elastic_moduli_and_filename`` helper function
        with invalid arguments that raise TypeError
        """
        with pytest.raises(TypeError):
            _get_effective_elastic_moduli_and_filename()  # Argument is None
        with pytest.raises(TypeError):
            _get_effective_elastic_moduli_and_filename(none_arg)  # Argument is None
        with pytest.raises(TypeError):
            _get_effective_elastic_moduli_and_filename(
                fiberglass
            )  # Argument is not HT object

    @pytest.fixture
    def properties_list1(self):
        """
        Provide arguments for list that contains constituent's elastic moduli
        """
        return [
            {
                "Constituent": "Fiberglass",
                "Young's\nModulus,\nE (GPa)": Decimal("120.000"),
                "Poisson's\nRatio,\nv": Decimal("0.290"),
                "Shear\nModulus,\nG (GPa)": Decimal("46.512"),
                "Plane-strain\nBulk Modulus,\nK (GPa)": Decimal("110.742"),
            },
            {
                "Constituent": "Epoxy",
                "Young's\nModulus,\nE (GPa)": Decimal("2.800"),
                "Poisson's\nRatio,\nv": Decimal("0.300"),
                "Shear\nModulus,\nG (GPa)": Decimal("1.077"),
                "Plane-strain\nBulk Modulus,\nK (GPa)": Decimal("2.692"),
            },
        ]

    def test_save_csv_file_output_with_valid_list_1(self, properties_list1):
        """
        Test output of ``_save_csv_file`` helper function to save phases' elastic moduli
        with valid arguments where first argument is a valid list containing two dicts
        of elastic moduli from fiber and matrix of the same type. Here, dummy folder and
        filename is used.
        """
        return_filename = _save_csv_file(properties_list1, "trial", "trial1.csv")
        # Validate return value as the filename
        assert return_filename == "trial1.csv"
        folder_path = "./trial"
        file_path = os.path.join(folder_path, "trial1.csv")
        # Check the existence of the file and folder
        assert os.path.isfile(file_path) == True

    @pytest.fixture
    def properties_list2(self):
        """
        Provide arguments for a tuple that contains constituent elastic moduli
        """
        return [
            {
                "Constituent": "Carbon",
                "Axial\nYoung's\nModulus,\nE1 (GPa)": Decimal("250.000"),
                "Transverse\nYoung's\nModulus,\nE2 (GPa)": Decimal("25.000"),
                "Axial\nShear\nModulus,\nG12 (GPa)": Decimal("20.000"),
                "Transverse\nShear\nModulus,\nG23 (GPa)": Decimal("10.000"),
                "Major\nPoisson's\nRatio,\nv12": Decimal("0.280"),
                "Plane-strain\nBulk\nModulus,\nK23 (GPa)": Decimal("17.023"),
            }
        ]

    def test_save_csv_file_output_with_valid_list_2(self, properties_list2):
        """
        Test output of ``_save_csv_file`` helper function with valid arguments where the
        first is a valid list of only 1 dict of constituent elastic moduli and here,
        dummy folder with dummy filename
        """
        return_filename = _save_csv_file(properties_list2, "trial", "trial2.csv")
        # Validate return value as the filename
        assert return_filename == "trial2.csv"
        folder_path = "./trial"
        file_path = os.path.join(folder_path, "trial2.csv")
        # Check the existence of the file and folder
        assert os.path.isfile(file_path) == True

    def test_save_csv_file_output_with_invalid_inputs(
            self, fiberglass, composite1, none_arg
    ):
        """
        Test output of ``_save_csv_file`` helper function with invalid arguments that
        raise TypeError
        """
        with pytest.raises(TypeError):
            _get_effective_elastic_moduli_and_filename()  # No argument
        with pytest.raises(TypeError):
            _get_effective_elastic_moduli_and_filename(
                none_arg, "csv", "properties.csv"
            )  # First argument is not HT object
        with pytest.raises(TypeError):
            _get_effective_elastic_moduli_and_filename(
                fiberglass, "csv", "properties.csv"
            )  # First argument is not HT object
        with pytest.raises(TypeError):
            _get_effective_elastic_moduli_and_filename(
                fiberglass, none_arg, "properties.csv"
            )  # Second argument is None
        with pytest.raises(TypeError):
            _get_effective_elastic_moduli_and_filename(
                fiberglass, 2, "properties.csv"
            )  # Second argument is not str
        with pytest.raises(TypeError):
            _get_effective_elastic_moduli_and_filename(
                composite1, "csv", none_arg
            )  # Third argument is None
        with pytest.raises(TypeError):
            _get_effective_elastic_moduli_and_filename(
                composite1, "csv", 2
            )  # Second argument is not str

    def test_is_confirmed_output(self):
        """
        Test output of ``_is_confirmed`` helper function with valid arguments that
        follows from previous unit tests: `test_save_csv_file_output_with_valid_list_1`
        and also, `test_save_csv_file_output_with_valid_list_2`
        """
        # Confirm files are present resulting from previous unit test
        assert _is_confirmed("trial", "trial1.csv") == True
        assert _is_confirmed("trial", "trial2.csv") == True
        # Remove file trial1.csv
        folder_path = "./trial"
        file_path1 = os.path.join(folder_path, "trial1.csv")
        os.remove(file_path1)
        # Confirm trial1.csv is no longer present
        assert os.path.isfile(file_path1) == False

    def test_is_confirmed_output_with_invalid_inputs(self, none_arg):
        """
        Test output of ``_is_confirmed`` helper function with invalid arguments that
        raise TypeError
        """
        with pytest.raises(TypeError):
            _is_confirmed()  # No argument
        with pytest.raises(TypeError):
            _is_confirmed(none_arg, "properties.csv")  # First argument is None
        with pytest.raises(TypeError):
            _is_confirmed(2, "properties.csv")  # First argument is not str
        with pytest.raises(TypeError):
            _is_confirmed(
                "csv",
            )  # Second argument is None
        with pytest.raises(TypeError):
            _is_confirmed("csv", none_arg)  # Second argument is None
        with pytest.raises(TypeError):
            _is_confirmed("csv", 2)  # Second argument is not str

    def test_get_confirmation_notices_output(self):
        """
        Test output of ``_get_confirmation_notices`` with valid arguments that follows
        from previous unit tests: `test_save_csv_file_output_with_valid_list_1`,
        `test_save_csv_file_output_with_valid_list_2`, and `test_is_confirmed_output`
        """
        # For saved file
        assert _get_confirmation_notices(True, "trial2.csv") == (
            "========================= trial2.csv file saved! ========================="
        )
        # For missing file as has been removed earlier in previous unit test
        assert _get_confirmation_notices(False, "trial1.csv") == (
            "========================= trial1.csv is missing! ========================="
        )
        # Remove additional file and whole directory - clean up
        folder_path = "./trial"
        file_path = os.path.join(folder_path, "trial2.csv")
        os.remove(file_path)
        os.rmdir("./trial")

    def test_get_confirmation_notices_output_with_invalid_inputs(self, none_arg):
        """
        Test output of ``_get_confirmation_notices`` helper function with invalid
        arguments that raise TypeError
        """
        with pytest.raises(TypeError):
            _get_confirmation_notices()  # no argument
        with pytest.raises(TypeError):
            _get_confirmation_notices(
                none_arg, "properties.csv"
            )  # first argument is None
        with pytest.raises(TypeError):
            _get_confirmation_notices(
                "4", "properties.csv"
            )  # first argument is not bool
        with pytest.raises(TypeError):
            _get_confirmation_notices("True", none_arg)  # second argument is None
        with pytest.raises(TypeError):
            _get_confirmation_notices("False", 2)  # second argument is not str

    def test_save_output_1(
            self, composite1, composite2, composite3, composite4, capsys
    ):
        """
        Test output of ``save`` major function with valid arguments, i.e 4 different UD
        composites having different types of constituent materials but save one at a
        time only
        """
        # 1) New folder creation with save(composite1) using default folder's name - "csv"
        # with 3 csv files saved in the folder
        save(composite1)
        captured = capsys.readouterr()
        assert captured.out == (
            "Folder ./csv created\n"
            + "============= Carbon-Epoxy_fiber_tra_moduli.csv file saved! ==============\n"
            + "============= Carbon-Epoxy_matrix_iso_moduli.csv file saved! =============\n"
            + "================ Carbon-Epoxy_eff_moduli.csv file saved! =================\n"
        )
        # Verify 3 files created
        folder_path = "./csv"
        file_path1 = os.path.join(folder_path, "Carbon-Epoxy_fiber_tra_moduli.csv")
        file_path2 = os.path.join(folder_path, "Carbon-Epoxy_matrix_iso_moduli.csv")
        file_path3 = os.path.join(folder_path, "Carbon-Epoxy_eff_moduli.csv")
        # Check the existence of the file and folder
        assert os.path.isfile(file_path1) == True
        assert os.path.isfile(file_path2) == True
        assert os.path.isfile(file_path3) == True

        # 2) No new folder creation with save(composite2) since default "csv" folder
        # exists already but only 2 csv files saved in that folder since both fiber and
        # matrix are same type
        save(composite2)
        captured = capsys.readouterr()
        assert captured.out == (
            "=========== Fiberglass-Epoxy_phases_iso_moduli.csv file saved! ===========\n"
            + "============== Fiberglass-Epoxy_eff_moduli.csv file saved! ===============\n"
        )
        # Verify 2 files created
        folder_path = "./csv"
        file_path4 = os.path.join(folder_path, "Fiberglass-Epoxy_phases_iso_moduli.csv")
        file_path5 = os.path.join(folder_path, "Fiberglass-Epoxy_eff_moduli.csv")
        # Check the existence of the file and folder
        assert os.path.isfile(file_path4) == True
        assert os.path.isfile(file_path5) == True

        # 3) New folder creation with save(composite3, folder="csv_2") using user-defined
        # folder's name using keyword parameter, folder="csv_2" with 2 csv files saved
        # in that folder
        save(composite3, folder="csv_2")
        captured = capsys.readouterr()
        assert captured.out == (
            "Folder ./csv_2 created\n"
            + "=========== Carbon-Graphite_phases_tra_moduli.csv file saved! ============\n"
            + "=============== Carbon-Graphite_eff_moduli.csv file saved! ===============\n"
        )
        # Verify 2 files created
        folder_path = "./csv_2"
        file_path6 = os.path.join(folder_path, "Carbon-Graphite_phases_tra_moduli.csv")
        file_path7 = os.path.join(folder_path, "Carbon-Graphite_eff_moduli.csv")
        # Check the existence of the file and folder
        assert os.path.isfile(file_path6) == True
        assert os.path.isfile(file_path7) == True

        # 4) No new folder creation with save(composite4, folder="csv_2") since "csv_2"
        # exists already and 3 csv files saved in that folder
        save(composite4, folder="csv_2")
        captured = capsys.readouterr()
        assert captured.out == (
            "========== Fiberglass-Graphite_fiber_iso_moduli.csv file saved! ==========\n"
            + "========= Fiberglass-Graphite_matrix_tra_moduli.csv file saved! ==========\n"
            + "============= Fiberglass-Graphite_eff_moduli.csv file saved! =============\n"
        )
        # Verify 3 files created
        folder_path = "./csv_2"
        file_path8 = os.path.join(
            folder_path, "Fiberglass-Graphite_fiber_iso_moduli.csv"
        )
        file_path9 = os.path.join(
            folder_path, "Fiberglass-Graphite_matrix_tra_moduli.csv"
        )
        file_path10 = os.path.join(folder_path, "Fiberglass-Graphite_eff_moduli.csv")
        # Check the existence of the file and folder
        assert os.path.isfile(file_path8) == True
        assert os.path.isfile(file_path9) == True
        assert os.path.isfile(file_path10) == True

        # Clean-up
        os.remove(file_path1)
        os.remove(file_path2)
        os.remove(file_path3)
        os.remove(file_path4)
        os.remove(file_path5)
        os.remove(file_path6)
        os.remove(file_path7)
        os.remove(file_path8)
        os.remove(file_path9)
        os.remove(file_path10)
        os.rmdir("./csv")
        os.rmdir("./csv_2")

    def test_save_output_2(
            self, composite1, composite2, composite3, composite4, capsys
    ):
        """
        Test output of ``save`` major function with valid arguments, i.e 4 different UD
        composites having different types of constituent materials but are saved
        altogether with a single ``save`` function
        """
        save(composite1, composite2, composite3, composite4)
        captured = capsys.readouterr()
        assert captured.out == (
            "Folder ./csv created\n"
            + "============= Carbon-Epoxy_fiber_tra_moduli.csv file saved! ==============\n"
            + "============= Carbon-Epoxy_matrix_iso_moduli.csv file saved! =============\n"
            + "================ Carbon-Epoxy_eff_moduli.csv file saved! =================\n"
            + "=========== Fiberglass-Epoxy_phases_iso_moduli.csv file saved! ===========\n"
            + "============== Fiberglass-Epoxy_eff_moduli.csv file saved! ===============\n"
            + "=========== Carbon-Graphite_phases_tra_moduli.csv file saved! ============\n"
            + "=============== Carbon-Graphite_eff_moduli.csv file saved! ===============\n"
            + "========== Fiberglass-Graphite_fiber_iso_moduli.csv file saved! ==========\n"
            + "========= Fiberglass-Graphite_matrix_tra_moduli.csv file saved! ==========\n"
            + "============= Fiberglass-Graphite_eff_moduli.csv file saved! =============\n"
        )

        # Verify all files are saved in "csv" folder
        folder_path = "./csv"
        file_path1 = os.path.join(folder_path, "Carbon-Epoxy_fiber_tra_moduli.csv")
        file_path2 = os.path.join(folder_path, "Carbon-Epoxy_matrix_iso_moduli.csv")
        file_path3 = os.path.join(folder_path, "Carbon-Epoxy_eff_moduli.csv")
        file_path4 = os.path.join(folder_path, "Fiberglass-Epoxy_phases_iso_moduli.csv")
        file_path5 = os.path.join(folder_path, "Fiberglass-Epoxy_eff_moduli.csv")
        file_path6 = os.path.join(folder_path, "Carbon-Graphite_phases_tra_moduli.csv")
        file_path7 = os.path.join(folder_path, "Carbon-Graphite_eff_moduli.csv")
        file_path8 = os.path.join(
            folder_path, "Fiberglass-Graphite_fiber_iso_moduli.csv"
        )
        file_path9 = os.path.join(
            folder_path, "Fiberglass-Graphite_matrix_tra_moduli.csv"
        )
        file_path10 = os.path.join(folder_path, "Fiberglass-Graphite_eff_moduli.csv")
        assert os.path.isfile(file_path1) == True
        assert os.path.isfile(file_path2) == True
        assert os.path.isfile(file_path3) == True
        assert os.path.isfile(file_path4) == True
        assert os.path.isfile(file_path5) == True
        assert os.path.isfile(file_path6) == True
        assert os.path.isfile(file_path7) == True
        assert os.path.isfile(file_path8) == True
        assert os.path.isfile(file_path9) == True
        assert os.path.isfile(file_path10) == True

        # Clean up
        os.remove(file_path1)
        os.remove(file_path2)
        os.remove(file_path3)
        os.remove(file_path4)
        os.remove(file_path5)
        os.remove(file_path6)
        os.remove(file_path7)
        os.remove(file_path8)
        os.remove(file_path9)
        os.remove(file_path10)
        os.rmdir("./csv")

    def test_save_output_with_invalid_inputs(self, carbon, composite1, none_arg):
        """
        Test output of ``save`` major function with invalid arguments that raise
        TypeError
        """
        with pytest.raises(TypeError):
            save()  # no argument
        with pytest.raises(TypeError):
            save(none_arg)  # argument is None
        with pytest.raises(TypeError):
            save(carbon)  # argument is not HT object
        with pytest.raises(TypeError):
            save(composite1, none_arg)  # one of the arguments is None
        with pytest.raises(TypeError):
            save(composite1, carbon)  # one of the arguments is not HT object


class Test_Plot:
    """
    Test suite for ``plot`` major function that plots information about UD
    composite's effective elastic moduli to png format files in a default name "png"
    folder, which can be redefined if user desired.

    This test suite contains all unit tests for every helper functions that make up the
    ``plot`` function. Once all helper functions are tested, and then ``plot`` major
    function is unit-tested as well.
    """

    @pytest.fixture
    def fiberglass(self):
        """
        Provide arguments on fiber isotropic material called fiberglass
        """
        # Isotropic class and its methods have been fully unit-tested and all passed as done above
        return Isotropic(name="Fiberglass", youngs_modulus=120, poissons_ratio=0.29)

    @pytest.fixture
    def carbon(self):
        """
        Provide arguments for transversely isotropic fiber called carbon
        """
        # Transtropic class and all its methods are assumed to have been fully unit-tested and all passed
        return Transtropic(
            name="Carbon",
            axial_youngs_modulus=250,
            transverse_youngs_modulus=25,
            axial_shear_modulus=20,
            transverse_shear_modulus=10,
            major_poissons_ratio=0.28,
        )

    @pytest.fixture
    def epoxy(self):
        """
        Provide arguments for isotropic matrix material called epoxy
        """
        return Isotropic(name="Epoxy", youngs_modulus=2.8, poissons_ratio=0.3)

    @pytest.fixture
    def graphite(self):
        """
        Provide arguments for transversely isotropic matrix material called graphite
        """
        return Transtropic(
            name="Graphite",
            axial_youngs_modulus=180,
            transverse_youngs_modulus=20,
            axial_shear_modulus=15,
            transverse_shear_modulus=10,
            major_poissons_ratio=0.29,
        )

    @pytest.fixture
    def composite1(self, carbon, epoxy):
        """
        Provide arguments for UD composite with carbon fiber as transversely isotropic
        material and epoxy matrix as isotropic material
        """
        # HT class and all its methods are assumed to have been fully unit-tested and all passed
        return HT(fiber=carbon, matrix=epoxy)

    @pytest.fixture
    def composite2(self, fiberglass, epoxy):
        """
        Provide arguments for UD composite with both fiberglass fiber and epoxy matrix
        as isotropic materials
        """
        return HT(fiber=fiberglass, matrix=epoxy)

    @pytest.fixture
    def composite3(self, carbon, graphite):
        """
        Provide arguments for UD composite with both carbon fiber and graphite matrix as
        transversely isotropic materials
        """
        return HT(fiber=carbon, matrix=graphite)

    @pytest.fixture
    def composite4(self, fiberglass, graphite):
        """
        Provide arguments for UD composite with fiberglass fiber as isotropic material
        and graphite matrix as transversely isotropic material
        """
        return HT(fiber=fiberglass, matrix=graphite)

    @pytest.fixture
    def none_arg(self):
        """
        Provide argument with None
        """
        return None

    def test_get_E1eff_data_for_plot_and_filename_output(self, composite1, composite2):
        """
        Test output of ``_get_E1eff_data_for_plot_and_filename`` with valid arguments,
        i.e. 2 different UD composites - composite1 and composite2
        """
        result1 = _get_E1eff_data_for_plot_and_filename(composite1)
        assert result1 == (
            "Carbon-Epoxy_E1eff.png",
            (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            (
                Decimal("2.800"),
                Decimal("5.272"),
                Decimal("7.744"),
                Decimal("10.216"),
                Decimal("12.688"),
                Decimal("15.160"),
                Decimal("17.632"),
                Decimal("20.104"),
                Decimal("22.576"),
                Decimal("25.048"),
                Decimal("27.520"),
                Decimal("29.992"),
                Decimal("32.464"),
                Decimal("34.936"),
                Decimal("37.408"),
                Decimal("39.880"),
                Decimal("42.352"),
                Decimal("44.824"),
                Decimal("47.296"),
                Decimal("49.768"),
                Decimal("52.240"),
                Decimal("54.712"),
                Decimal("57.184"),
                Decimal("59.656"),
                Decimal("62.128"),
                Decimal("64.600"),
                Decimal("67.072"),
                Decimal("69.544"),
                Decimal("72.016"),
                Decimal("74.488"),
                Decimal("76.960"),
                Decimal("79.432"),
                Decimal("81.904"),
                Decimal("84.376"),
                Decimal("86.848"),
                Decimal("89.320"),
                Decimal("91.792"),
                Decimal("94.264"),
                Decimal("96.736"),
                Decimal("99.208"),
                Decimal("101.680"),
                Decimal("104.152"),
                Decimal("106.624"),
                Decimal("109.096"),
                Decimal("111.568"),
                Decimal("114.040"),
                Decimal("116.512"),
                Decimal("118.984"),
                Decimal("121.456"),
                Decimal("123.928"),
                Decimal("126.400"),
                Decimal("128.872"),
                Decimal("131.344"),
                Decimal("133.816"),
                Decimal("136.288"),
                Decimal("138.760"),
                Decimal("141.232"),
                Decimal("143.704"),
                Decimal("146.176"),
                Decimal("148.648"),
                Decimal("151.120"),
                Decimal("153.592"),
                Decimal("156.064"),
                Decimal("158.536"),
                Decimal("161.008"),
                Decimal("163.480"),
                Decimal("165.952"),
                Decimal("168.424"),
                Decimal("170.896"),
                Decimal("173.368"),
                Decimal("175.840"),
                Decimal("178.312"),
                Decimal("180.784"),
                Decimal("183.256"),
                Decimal("185.728"),
                Decimal("188.200"),
                Decimal("190.672"),
                Decimal("193.144"),
                Decimal("195.616"),
                Decimal("198.088"),
                Decimal("200.560"),
                Decimal("203.032"),
                Decimal("205.504"),
                Decimal("207.976"),
                Decimal("210.448"),
                Decimal("212.920"),
                Decimal("215.392"),
                Decimal("217.864"),
                Decimal("220.336"),
                Decimal("222.808"),
                Decimal("225.280"),
                Decimal("227.752"),
                Decimal("230.224"),
                Decimal("232.696"),
                Decimal("235.168"),
                Decimal("237.640"),
                Decimal("240.112"),
                Decimal("242.584"),
                Decimal("245.056"),
                Decimal("247.528"),
                Decimal("250.000"),
            ),
            "Carbon-Epoxy",
            "Vf",
            "E1* (GPa)",
        )
        result2 = _get_E1eff_data_for_plot_and_filename(composite2)
        assert result2 == (
            "Fiberglass-Epoxy_E1eff.png",
            (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            (
                Decimal("2.800"),
                Decimal("3.972"),
                Decimal("5.144"),
                Decimal("6.316"),
                Decimal("7.488"),
                Decimal("8.660"),
                Decimal("9.832"),
                Decimal("11.004"),
                Decimal("12.176"),
                Decimal("13.348"),
                Decimal("14.520"),
                Decimal("15.692"),
                Decimal("16.864"),
                Decimal("18.036"),
                Decimal("19.208"),
                Decimal("20.380"),
                Decimal("21.552"),
                Decimal("22.724"),
                Decimal("23.896"),
                Decimal("25.068"),
                Decimal("26.240"),
                Decimal("27.412"),
                Decimal("28.584"),
                Decimal("29.756"),
                Decimal("30.928"),
                Decimal("32.100"),
                Decimal("33.272"),
                Decimal("34.444"),
                Decimal("35.616"),
                Decimal("36.788"),
                Decimal("37.960"),
                Decimal("39.132"),
                Decimal("40.304"),
                Decimal("41.476"),
                Decimal("42.648"),
                Decimal("43.820"),
                Decimal("44.992"),
                Decimal("46.164"),
                Decimal("47.336"),
                Decimal("48.508"),
                Decimal("49.680"),
                Decimal("50.852"),
                Decimal("52.024"),
                Decimal("53.196"),
                Decimal("54.368"),
                Decimal("55.540"),
                Decimal("56.712"),
                Decimal("57.884"),
                Decimal("59.056"),
                Decimal("60.228"),
                Decimal("61.400"),
                Decimal("62.572"),
                Decimal("63.744"),
                Decimal("64.916"),
                Decimal("66.088"),
                Decimal("67.260"),
                Decimal("68.432"),
                Decimal("69.604"),
                Decimal("70.776"),
                Decimal("71.948"),
                Decimal("73.120"),
                Decimal("74.292"),
                Decimal("75.464"),
                Decimal("76.636"),
                Decimal("77.808"),
                Decimal("78.980"),
                Decimal("80.152"),
                Decimal("81.324"),
                Decimal("82.496"),
                Decimal("83.668"),
                Decimal("84.840"),
                Decimal("86.012"),
                Decimal("87.184"),
                Decimal("88.356"),
                Decimal("89.528"),
                Decimal("90.700"),
                Decimal("91.872"),
                Decimal("93.044"),
                Decimal("94.216"),
                Decimal("95.388"),
                Decimal("96.560"),
                Decimal("97.732"),
                Decimal("98.904"),
                Decimal("100.076"),
                Decimal("101.248"),
                Decimal("102.420"),
                Decimal("103.592"),
                Decimal("104.764"),
                Decimal("105.936"),
                Decimal("107.108"),
                Decimal("108.280"),
                Decimal("109.452"),
                Decimal("110.624"),
                Decimal("111.796"),
                Decimal("112.968"),
                Decimal("114.140"),
                Decimal("115.312"),
                Decimal("116.484"),
                Decimal("117.656"),
                Decimal("118.828"),
                Decimal("120.000"),
            ),
            "Fiberglass-Epoxy",
            "Vf",
            "E1* (GPa)",
        )

    def test_get_E1eff_data_for_plot_and_filename_output_with_invalid_inputs(
            self, carbon, none_arg
    ):
        """
        Test output of ``_get_E1eff_data_for_plot_and_filename`` with invalid arguments
        that raise TypeError
        """
        with pytest.raises(TypeError):
            _get_E1eff_data_for_plot_and_filename()  # no argument
        with pytest.raises(TypeError):
            _get_E1eff_data_for_plot_and_filename(none_arg)  # argument is None
        with pytest.raises(TypeError):
            _get_E1eff_data_for_plot_and_filename(carbon)  # argument is not HT object

    def test_get_E2eff_data_for_plot_and_filename_output(self, composite3, composite4):
        """
        Test output of ``_get_E2eff_data_for_plot_and_filename`` with valid arguments,
        i.e. 2 different UD composites - composite3 and composite4
        """
        result1 = _get_E2eff_data_for_plot_and_filename(composite3)
        assert result1 == (
            "Carbon-Graphite_E2eff.png",
            (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            (
                Decimal("20.000"),
                Decimal("20.049"),
                Decimal("20.100"),
                Decimal("20.149"),
                Decimal("20.199"),
                Decimal("20.250"),
                Decimal("20.300"),
                Decimal("20.350"),
                Decimal("20.400"),
                Decimal("20.450"),
                Decimal("20.500"),
                Decimal("20.550"),
                Decimal("20.600"),
                Decimal("20.650"),
                Decimal("20.700"),
                Decimal("20.750"),
                Decimal("20.800"),
                Decimal("20.850"),
                Decimal("20.900"),
                Decimal("20.950"),
                Decimal("21.000"),
                Decimal("21.050"),
                Decimal("21.100"),
                Decimal("21.150"),
                Decimal("21.200"),
                Decimal("21.250"),
                Decimal("21.300"),
                Decimal("21.350"),
                Decimal("21.400"),
                Decimal("21.450"),
                Decimal("21.500"),
                Decimal("21.550"),
                Decimal("21.600"),
                Decimal("21.650"),
                Decimal("21.700"),
                Decimal("21.750"),
                Decimal("21.800"),
                Decimal("21.850"),
                Decimal("21.900"),
                Decimal("21.950"),
                Decimal("22.000"),
                Decimal("22.050"),
                Decimal("22.100"),
                Decimal("22.150"),
                Decimal("22.200"),
                Decimal("22.250"),
                Decimal("22.300"),
                Decimal("22.350"),
                Decimal("22.400"),
                Decimal("22.450"),
                Decimal("22.500"),
                Decimal("22.550"),
                Decimal("22.600"),
                Decimal("22.650"),
                Decimal("22.700"),
                Decimal("22.750"),
                Decimal("22.800"),
                Decimal("22.850"),
                Decimal("22.900"),
                Decimal("22.950"),
                Decimal("23.000"),
                Decimal("23.050"),
                Decimal("23.100"),
                Decimal("23.150"),
                Decimal("23.200"),
                Decimal("23.250"),
                Decimal("23.300"),
                Decimal("23.350"),
                Decimal("23.400"),
                Decimal("23.450"),
                Decimal("23.500"),
                Decimal("23.550"),
                Decimal("23.600"),
                Decimal("23.650"),
                Decimal("23.700"),
                Decimal("23.750"),
                Decimal("23.800"),
                Decimal("23.850"),
                Decimal("23.900"),
                Decimal("23.950"),
                Decimal("24.000"),
                Decimal("24.050"),
                Decimal("24.100"),
                Decimal("24.150"),
                Decimal("24.200"),
                Decimal("24.250"),
                Decimal("24.300"),
                Decimal("24.350"),
                Decimal("24.400"),
                Decimal("24.450"),
                Decimal("24.500"),
                Decimal("24.550"),
                Decimal("24.600"),
                Decimal("24.650"),
                Decimal("24.700"),
                Decimal("24.750"),
                Decimal("24.800"),
                Decimal("24.850"),
                Decimal("24.900"),
                Decimal("24.950"),
                Decimal("25.000"),
            ),
            "Carbon-Graphite",
            "Vf",
            "E2* (GPa)",
        )
        result2 = _get_E2eff_data_for_plot_and_filename(composite4)
        assert result2 == (
            "Fiberglass-Graphite_E2eff.png",
            (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            (
                Decimal("20.000"),
                Decimal("20.261"),
                Decimal("20.526"),
                Decimal("20.793"),
                Decimal("21.066"),
                Decimal("21.342"),
                Decimal("21.622"),
                Decimal("21.907"),
                Decimal("22.196"),
                Decimal("22.488"),
                Decimal("22.786"),
                Decimal("23.088"),
                Decimal("23.395"),
                Decimal("23.706"),
                Decimal("24.023"),
                Decimal("24.344"),
                Decimal("24.672"),
                Decimal("25.004"),
                Decimal("25.341"),
                Decimal("25.684"),
                Decimal("26.035"),
                Decimal("26.389"),
                Decimal("26.751"),
                Decimal("27.117"),
                Decimal("27.492"),
                Decimal("27.872"),
                Decimal("28.260"),
                Decimal("28.655"),
                Decimal("29.055"),
                Decimal("29.466"),
                Decimal("29.882"),
                Decimal("30.307"),
                Decimal("30.741"),
                Decimal("31.181"),
                Decimal("31.632"),
                Decimal("32.091"),
                Decimal("32.559"),
                Decimal("33.037"),
                Decimal("33.524"),
                Decimal("34.022"),
                Decimal("34.530"),
                Decimal("35.048"),
                Decimal("35.578"),
                Decimal("36.119"),
                Decimal("36.673"),
                Decimal("37.238"),
                Decimal("37.818"),
                Decimal("38.409"),
                Decimal("39.014"),
                Decimal("39.633"),
                Decimal("40.268"),
                Decimal("40.917"),
                Decimal("41.581"),
                Decimal("42.262"),
                Decimal("42.961"),
                Decimal("43.678"),
                Decimal("44.411"),
                Decimal("45.165"),
                Decimal("45.938"),
                Decimal("46.732"),
                Decimal("47.546"),
                Decimal("48.384"),
                Decimal("49.244"),
                Decimal("50.130"),
                Decimal("51.041"),
                Decimal("51.978"),
                Decimal("52.942"),
                Decimal("53.936"),
                Decimal("54.959"),
                Decimal("56.015"),
                Decimal("57.102"),
                Decimal("58.226"),
                Decimal("59.385"),
                Decimal("60.582"),
                Decimal("61.821"),
                Decimal("63.101"),
                Decimal("64.426"),
                Decimal("65.798"),
                Decimal("67.218"),
                Decimal("68.692"),
                Decimal("70.220"),
                Decimal("71.807"),
                Decimal("73.454"),
                Decimal("75.168"),
                Decimal("76.953"),
                Decimal("78.808"),
                Decimal("80.743"),
                Decimal("82.761"),
                Decimal("84.867"),
                Decimal("87.069"),
                Decimal("89.374"),
                Decimal("91.786"),
                Decimal("94.314"),
                Decimal("96.969"),
                Decimal("99.757"),
                Decimal("102.692"),
                Decimal("105.782"),
                Decimal("109.044"),
                Decimal("112.489"),
                Decimal("116.135"),
                Decimal("120.001"),
            ),
            "Fiberglass-Graphite",
            "Vf",
            "E2* (GPa)",
        )

    def test_get_E2eff_data_for_plot_and_filename_output_with_invalid_inputs(
            self, fiberglass, none_arg
    ):
        """
        Test output of ``_get_E2eff_data_for_plot_and_filename`` with invalid arguments
        that raise TypeError
        """
        with pytest.raises(TypeError):
            _get_E2eff_data_for_plot_and_filename()  # no argument
        with pytest.raises(TypeError):
            _get_E2eff_data_for_plot_and_filename(none_arg)  # argument is None
        with pytest.raises(TypeError):
            _get_E2eff_data_for_plot_and_filename(
                fiberglass
            )  # argument is not HT object

    def test_get_G12eff_data_for_plot_and_filename_output(self, composite1, composite2):
        """
        Test output of ``_get_G12eff_data_for_plot_and_filename`` with valid arguments,
        i.e. 2 different UD composites - composite1 and composite2 having different
        types of constituent materials
        """
        result1 = _get_G12eff_data_for_plot_and_filename(composite1)
        assert result1 == (
            "Carbon-Epoxy_G12eff.png",
            (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            (
                Decimal("1.077"),
                Decimal("1.097"),
                Decimal("1.116"),
                Decimal("1.137"),
                Decimal("1.157"),
                Decimal("1.178"),
                Decimal("1.200"),
                Decimal("1.221"),
                Decimal("1.244"),
                Decimal("1.266"),
                Decimal("1.289"),
                Decimal("1.313"),
                Decimal("1.337"),
                Decimal("1.362"),
                Decimal("1.387"),
                Decimal("1.412"),
                Decimal("1.438"),
                Decimal("1.465"),
                Decimal("1.492"),
                Decimal("1.520"),
                Decimal("1.548"),
                Decimal("1.577"),
                Decimal("1.607"),
                Decimal("1.638"),
                Decimal("1.669"),
                Decimal("1.700"),
                Decimal("1.733"),
                Decimal("1.766"),
                Decimal("1.800"),
                Decimal("1.835"),
                Decimal("1.871"),
                Decimal("1.908"),
                Decimal("1.945"),
                Decimal("1.984"),
                Decimal("2.023"),
                Decimal("2.064"),
                Decimal("2.106"),
                Decimal("2.148"),
                Decimal("2.192"),
                Decimal("2.238"),
                Decimal("2.284"),
                Decimal("2.332"),
                Decimal("2.381"),
                Decimal("2.431"),
                Decimal("2.484"),
                Decimal("2.537"),
                Decimal("2.592"),
                Decimal("2.649"),
                Decimal("2.708"),
                Decimal("2.769"),
                Decimal("2.832"),
                Decimal("2.896"),
                Decimal("2.963"),
                Decimal("3.032"),
                Decimal("3.104"),
                Decimal("3.178"),
                Decimal("3.255"),
                Decimal("3.335"),
                Decimal("3.417"),
                Decimal("3.503"),
                Decimal("3.592"),
                Decimal("3.685"),
                Decimal("3.781"),
                Decimal("3.882"),
                Decimal("3.986"),
                Decimal("4.096"),
                Decimal("4.210"),
                Decimal("4.329"),
                Decimal("4.453"),
                Decimal("4.584"),
                Decimal("4.721"),
                Decimal("4.864"),
                Decimal("5.015"),
                Decimal("5.174"),
                Decimal("5.341"),
                Decimal("5.517"),
                Decimal("5.704"),
                Decimal("5.901"),
                Decimal("6.110"),
                Decimal("6.332"),
                Decimal("6.568"),
                Decimal("6.819"),
                Decimal("7.088"),
                Decimal("7.376"),
                Decimal("7.685"),
                Decimal("8.017"),
                Decimal("8.375"),
                Decimal("8.763"),
                Decimal("9.183"),
                Decimal("9.642"),
                Decimal("10.143"),
                Decimal("10.694"),
                Decimal("11.301"),
                Decimal("11.974"),
                Decimal("12.725"),
                Decimal("13.567"),
                Decimal("14.519"),
                Decimal("15.604"),
                Decimal("16.850"),
                Decimal("18.298"),
                Decimal("20.000"),
            ),
            "Carbon-Epoxy",
            "Vf",
            "G12* (GPa)",
        )
        result2 = _get_G12eff_data_for_plot_and_filename(composite2)
        assert result2 == (
            "Fiberglass-Epoxy_G12eff.png",
            (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            (
                Decimal("1.077"),
                Decimal("1.098"),
                Decimal("1.119"),
                Decimal("1.141"),
                Decimal("1.163"),
                Decimal("1.185"),
                Decimal("1.208"),
                Decimal("1.231"),
                Decimal("1.255"),
                Decimal("1.279"),
                Decimal("1.304"),
                Decimal("1.330"),
                Decimal("1.356"),
                Decimal("1.382"),
                Decimal("1.409"),
                Decimal("1.437"),
                Decimal("1.465"),
                Decimal("1.494"),
                Decimal("1.524"),
                Decimal("1.554"),
                Decimal("1.585"),
                Decimal("1.617"),
                Decimal("1.650"),
                Decimal("1.683"),
                Decimal("1.717"),
                Decimal("1.752"),
                Decimal("1.788"),
                Decimal("1.825"),
                Decimal("1.863"),
                Decimal("1.902"),
                Decimal("1.942"),
                Decimal("1.983"),
                Decimal("2.025"),
                Decimal("2.068"),
                Decimal("2.112"),
                Decimal("2.158"),
                Decimal("2.205"),
                Decimal("2.254"),
                Decimal("2.303"),
                Decimal("2.355"),
                Decimal("2.408"),
                Decimal("2.463"),
                Decimal("2.519"),
                Decimal("2.577"),
                Decimal("2.637"),
                Decimal("2.700"),
                Decimal("2.764"),
                Decimal("2.830"),
                Decimal("2.899"),
                Decimal("2.971"),
                Decimal("3.044"),
                Decimal("3.121"),
                Decimal("3.201"),
                Decimal("3.283"),
                Decimal("3.369"),
                Decimal("3.459"),
                Decimal("3.552"),
                Decimal("3.649"),
                Decimal("3.750"),
                Decimal("3.855"),
                Decimal("3.966"),
                Decimal("4.081"),
                Decimal("4.202"),
                Decimal("4.328"),
                Decimal("4.461"),
                Decimal("4.600"),
                Decimal("4.747"),
                Decimal("4.901"),
                Decimal("5.064"),
                Decimal("5.235"),
                Decimal("5.417"),
                Decimal("5.610"),
                Decimal("5.814"),
                Decimal("6.031"),
                Decimal("6.262"),
                Decimal("6.509"),
                Decimal("6.773"),
                Decimal("7.056"),
                Decimal("7.360"),
                Decimal("7.688"),
                Decimal("8.042"),
                Decimal("8.426"),
                Decimal("8.844"),
                Decimal("9.300"),
                Decimal("9.801"),
                Decimal("10.352"),
                Decimal("10.962"),
                Decimal("11.640"),
                Decimal("12.400"),
                Decimal("13.256"),
                Decimal("14.228"),
                Decimal("15.342"),
                Decimal("16.631"),
                Decimal("18.139"),
                Decimal("19.928"),
                Decimal("22.084"),
                Decimal("24.734"),
                Decimal("28.069"),
                Decimal("32.392"),
                Decimal("38.222"),
                Decimal("46.512"),
            ),
            "Fiberglass-Epoxy",
            "Vf",
            "G12* (GPa)",
        )

    def test_get_G12eff_data_for_plot_and_filename_output_with_invalid_inputs(
            self, epoxy, none_arg
    ):
        """
        Test output of ``_get_G12eff_data_for_plot_and_filename`` with invalid arguments
        that raise TypeError
        """
        with pytest.raises(TypeError):
            _get_G12eff_data_for_plot_and_filename()  # no argument
        with pytest.raises(TypeError):
            _get_G12eff_data_for_plot_and_filename(none_arg)  # argument is None
        with pytest.raises(TypeError):
            _get_G12eff_data_for_plot_and_filename(epoxy)  # argument is not HT object

    def test_get_v12eff_data_for_plot_and_filename_output(self, composite3, composite4):
        """
        Test output of ``_get_v12eff_data_for_plot_and_filename`` with valid arguments,
        i.e. 2 different UD composites - composite3 and composite4 having different
        types of constituent materials
        """
        result1 = _get_v12eff_data_for_plot_and_filename(composite3)
        assert result1 == (
            "Carbon-Graphite_v12eff.png",
            (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            (
                Decimal("0.2900"),
                Decimal("0.2899"),
                Decimal("0.2898"),
                Decimal("0.2897"),
                Decimal("0.2896"),
                Decimal("0.2895"),
                Decimal("0.2894"),
                Decimal("0.2893"),
                Decimal("0.2892"),
                Decimal("0.2891"),
                Decimal("0.2890"),
                Decimal("0.2889"),
                Decimal("0.2888"),
                Decimal("0.2887"),
                Decimal("0.2886"),
                Decimal("0.2885"),
                Decimal("0.2884"),
                Decimal("0.2883"),
                Decimal("0.2882"),
                Decimal("0.2881"),
                Decimal("0.2880"),
                Decimal("0.2879"),
                Decimal("0.2878"),
                Decimal("0.2877"),
                Decimal("0.2876"),
                Decimal("0.2875"),
                Decimal("0.2874"),
                Decimal("0.2873"),
                Decimal("0.2872"),
                Decimal("0.2871"),
                Decimal("0.2870"),
                Decimal("0.2869"),
                Decimal("0.2868"),
                Decimal("0.2867"),
                Decimal("0.2866"),
                Decimal("0.2865"),
                Decimal("0.2864"),
                Decimal("0.2863"),
                Decimal("0.2862"),
                Decimal("0.2861"),
                Decimal("0.2860"),
                Decimal("0.2859"),
                Decimal("0.2858"),
                Decimal("0.2857"),
                Decimal("0.2856"),
                Decimal("0.2855"),
                Decimal("0.2854"),
                Decimal("0.2853"),
                Decimal("0.2852"),
                Decimal("0.2851"),
                Decimal("0.2850"),
                Decimal("0.2849"),
                Decimal("0.2848"),
                Decimal("0.2847"),
                Decimal("0.2846"),
                Decimal("0.2845"),
                Decimal("0.2844"),
                Decimal("0.2843"),
                Decimal("0.2842"),
                Decimal("0.2841"),
                Decimal("0.2840"),
                Decimal("0.2839"),
                Decimal("0.2838"),
                Decimal("0.2837"),
                Decimal("0.2836"),
                Decimal("0.2835"),
                Decimal("0.2834"),
                Decimal("0.2833"),
                Decimal("0.2832"),
                Decimal("0.2831"),
                Decimal("0.2830"),
                Decimal("0.2829"),
                Decimal("0.2828"),
                Decimal("0.2827"),
                Decimal("0.2826"),
                Decimal("0.2825"),
                Decimal("0.2824"),
                Decimal("0.2823"),
                Decimal("0.2822"),
                Decimal("0.2821"),
                Decimal("0.2820"),
                Decimal("0.2819"),
                Decimal("0.2818"),
                Decimal("0.2817"),
                Decimal("0.2816"),
                Decimal("0.2815"),
                Decimal("0.2814"),
                Decimal("0.2813"),
                Decimal("0.2812"),
                Decimal("0.2811"),
                Decimal("0.2810"),
                Decimal("0.2809"),
                Decimal("0.2808"),
                Decimal("0.2807"),
                Decimal("0.2806"),
                Decimal("0.2805"),
                Decimal("0.2804"),
                Decimal("0.2803"),
                Decimal("0.2802"),
                Decimal("0.2801"),
                Decimal("0.2800"),
            ),
            "Carbon-Graphite",
            "Vf",
            "v12*",
        )
        result2 = _get_v12eff_data_for_plot_and_filename(composite4)
        assert result2 == (
            "Fiberglass-Graphite_v12eff.png",
            (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            (
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
                Decimal("0.2900"),
            ),
            "Fiberglass-Graphite",
            "Vf",
            "v12*",
        )

    def test_get_v12eff_data_for_plot_and_filename_output_with_invalid_inputs(
            self, graphite, none_arg
    ):
        """
        Test output of ``_get_v12eff_data_for_plot_and_filename`` with invalid arguments
        that raise TypeError
        """
        with pytest.raises(TypeError):
            _get_v12eff_data_for_plot_and_filename()  # no argument
        with pytest.raises(TypeError):
            _get_v12eff_data_for_plot_and_filename(none_arg)  # argument is None
        with pytest.raises(TypeError):
            _get_v12eff_data_for_plot_and_filename(
                graphite
            )  # argument is not HT object

    def test_get_G23eff_data_for_plot_and_filename_output(self, composite1, composite2):
        """
        Test output of ``_get_G23eff_data_for_plot_and_filename`` with valid arguments,
        i.e. 2 different UD composites - composite1 and composite2 having different
        types of constituent materials
        """
        result1 = _get_G23eff_data_for_plot_and_filename(composite1)
        assert result1 == (
            "Carbon-Epoxy_G23eff.png",
            (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            (
                Decimal("1.077"),
                Decimal("1.091"),
                Decimal("1.106"),
                Decimal("1.120"),
                Decimal("1.135"),
                Decimal("1.151"),
                Decimal("1.166"),
                Decimal("1.182"),
                Decimal("1.198"),
                Decimal("1.214"),
                Decimal("1.231"),
                Decimal("1.248"),
                Decimal("1.265"),
                Decimal("1.283"),
                Decimal("1.301"),
                Decimal("1.319"),
                Decimal("1.338"),
                Decimal("1.357"),
                Decimal("1.376"),
                Decimal("1.396"),
                Decimal("1.416"),
                Decimal("1.437"),
                Decimal("1.458"),
                Decimal("1.479"),
                Decimal("1.501"),
                Decimal("1.524"),
                Decimal("1.546"),
                Decimal("1.570"),
                Decimal("1.594"),
                Decimal("1.618"),
                Decimal("1.643"),
                Decimal("1.669"),
                Decimal("1.695"),
                Decimal("1.722"),
                Decimal("1.749"),
                Decimal("1.777"),
                Decimal("1.806"),
                Decimal("1.835"),
                Decimal("1.865"),
                Decimal("1.896"),
                Decimal("1.928"),
                Decimal("1.960"),
                Decimal("1.993"),
                Decimal("2.028"),
                Decimal("2.063"),
                Decimal("2.099"),
                Decimal("2.136"),
                Decimal("2.174"),
                Decimal("2.213"),
                Decimal("2.253"),
                Decimal("2.295"),
                Decimal("2.338"),
                Decimal("2.382"),
                Decimal("2.427"),
                Decimal("2.474"),
                Decimal("2.522"),
                Decimal("2.571"),
                Decimal("2.623"),
                Decimal("2.676"),
                Decimal("2.731"),
                Decimal("2.787"),
                Decimal("2.846"),
                Decimal("2.906"),
                Decimal("2.969"),
                Decimal("3.034"),
                Decimal("3.102"),
                Decimal("3.172"),
                Decimal("3.245"),
                Decimal("3.321"),
                Decimal("3.399"),
                Decimal("3.481"),
                Decimal("3.567"),
                Decimal("3.656"),
                Decimal("3.749"),
                Decimal("3.846"),
                Decimal("3.947"),
                Decimal("4.054"),
                Decimal("4.165"),
                Decimal("4.282"),
                Decimal("4.404"),
                Decimal("4.533"),
                Decimal("4.669"),
                Decimal("4.813"),
                Decimal("4.964"),
                Decimal("5.124"),
                Decimal("5.293"),
                Decimal("5.473"),
                Decimal("5.664"),
                Decimal("5.867"),
                Decimal("6.085"),
                Decimal("6.317"),
                Decimal("6.566"),
                Decimal("6.833"),
                Decimal("7.122"),
                Decimal("7.433"),
                Decimal("7.771"),
                Decimal("8.139"),
                Decimal("8.540"),
                Decimal("8.980"),
                Decimal("9.464"),
                Decimal("10.000"),
            ),
            "Carbon-Epoxy",
            "Vf",
            "G23* (GPa)",
        )
        result2 = _get_G23eff_data_for_plot_and_filename(composite2)
        assert result2 == (
            "Fiberglass-Epoxy_G23eff.png",
            (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            (
                Decimal("1.077"),
                Decimal("1.093"),
                Decimal("1.110"),
                Decimal("1.127"),
                Decimal("1.144"),
                Decimal("1.162"),
                Decimal("1.180"),
                Decimal("1.198"),
                Decimal("1.217"),
                Decimal("1.236"),
                Decimal("1.256"),
                Decimal("1.276"),
                Decimal("1.296"),
                Decimal("1.317"),
                Decimal("1.339"),
                Decimal("1.360"),
                Decimal("1.383"),
                Decimal("1.406"),
                Decimal("1.429"),
                Decimal("1.453"),
                Decimal("1.477"),
                Decimal("1.502"),
                Decimal("1.528"),
                Decimal("1.555"),
                Decimal("1.582"),
                Decimal("1.609"),
                Decimal("1.638"),
                Decimal("1.667"),
                Decimal("1.697"),
                Decimal("1.727"),
                Decimal("1.759"),
                Decimal("1.791"),
                Decimal("1.825"),
                Decimal("1.859"),
                Decimal("1.894"),
                Decimal("1.931"),
                Decimal("1.968"),
                Decimal("2.006"),
                Decimal("2.046"),
                Decimal("2.087"),
                Decimal("2.129"),
                Decimal("2.173"),
                Decimal("2.218"),
                Decimal("2.264"),
                Decimal("2.312"),
                Decimal("2.362"),
                Decimal("2.413"),
                Decimal("2.466"),
                Decimal("2.521"),
                Decimal("2.578"),
                Decimal("2.637"),
                Decimal("2.699"),
                Decimal("2.762"),
                Decimal("2.829"),
                Decimal("2.898"),
                Decimal("2.970"),
                Decimal("3.044"),
                Decimal("3.122"),
                Decimal("3.204"),
                Decimal("3.289"),
                Decimal("3.378"),
                Decimal("3.471"),
                Decimal("3.569"),
                Decimal("3.671"),
                Decimal("3.779"),
                Decimal("3.892"),
                Decimal("4.011"),
                Decimal("4.136"),
                Decimal("4.269"),
                Decimal("4.409"),
                Decimal("4.558"),
                Decimal("4.716"),
                Decimal("4.884"),
                Decimal("5.062"),
                Decimal("5.253"),
                Decimal("5.457"),
                Decimal("5.676"),
                Decimal("5.911"),
                Decimal("6.164"),
                Decimal("6.438"),
                Decimal("6.735"),
                Decimal("7.058"),
                Decimal("7.411"),
                Decimal("7.798"),
                Decimal("8.225"),
                Decimal("8.697"),
                Decimal("9.223"),
                Decimal("9.811"),
                Decimal("10.475"),
                Decimal("11.229"),
                Decimal("12.093"),
                Decimal("13.093"),
                Decimal("14.265"),
                Decimal("15.655"),
                Decimal("17.333"),
                Decimal("19.397"),
                Decimal("21.998"),
                Decimal("25.377"),
                Decimal("29.945"),
                Decimal("36.461"),
                Decimal("46.512"),
            ),
            "Fiberglass-Epoxy",
            "Vf",
            "G23* (GPa)",
        )

    def test_get_G23eff_data_for_plot_and_filename_output_with_invalid_inputs(
            self, fiberglass, none_arg
    ):
        """
        Test output of ``_get_G23eff_data_for_plot_and_filename`` with invalid arguments
        that raise TypeError
        """
        with pytest.raises(TypeError):
            _get_G23eff_data_for_plot_and_filename()  # no argument
        with pytest.raises(TypeError):
            _get_G23eff_data_for_plot_and_filename(none_arg)  # argument is None
        with pytest.raises(TypeError):
            _get_G23eff_data_for_plot_and_filename(
                fiberglass
            )  # argument is not HT object

    def test_get_K23eff_data_for_plot_and_filename_output(self, composite3, composite4):
        """
        Test output of ``_get_K23eff_data_for_plot_and_filename`` with valid arguments,
        i.e. 2 different UD composites - composite3 and composite4
        """
        result1 = _get_K23eff_data_for_plot_and_filename(composite3)
        assert result1 == (
            "Carbon-Graphite_K23eff.png",
            (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            (
                Decimal("10.190"),
                Decimal("10.241"),
                Decimal("10.293"),
                Decimal("10.344"),
                Decimal("10.396"),
                Decimal("10.449"),
                Decimal("10.501"),
                Decimal("10.554"),
                Decimal("10.607"),
                Decimal("10.660"),
                Decimal("10.714"),
                Decimal("10.768"),
                Decimal("10.822"),
                Decimal("10.876"),
                Decimal("10.931"),
                Decimal("10.986"),
                Decimal("11.041"),
                Decimal("11.097"),
                Decimal("11.153"),
                Decimal("11.209"),
                Decimal("11.265"),
                Decimal("11.322"),
                Decimal("11.379"),
                Decimal("11.437"),
                Decimal("11.494"),
                Decimal("11.552"),
                Decimal("11.611"),
                Decimal("11.669"),
                Decimal("11.728"),
                Decimal("11.788"),
                Decimal("11.847"),
                Decimal("11.907"),
                Decimal("11.967"),
                Decimal("12.028"),
                Decimal("12.089"),
                Decimal("12.150"),
                Decimal("12.212"),
                Decimal("12.274"),
                Decimal("12.336"),
                Decimal("12.399"),
                Decimal("12.462"),
                Decimal("12.525"),
                Decimal("12.589"),
                Decimal("12.653"),
                Decimal("12.717"),
                Decimal("12.782"),
                Decimal("12.848"),
                Decimal("12.913"),
                Decimal("12.979"),
                Decimal("13.045"),
                Decimal("13.112"),
                Decimal("13.179"),
                Decimal("13.247"),
                Decimal("13.314"),
                Decimal("13.383"),
                Decimal("13.451"),
                Decimal("13.521"),
                Decimal("13.590"),
                Decimal("13.660"),
                Decimal("13.730"),
                Decimal("13.801"),
                Decimal("13.872"),
                Decimal("13.944"),
                Decimal("14.016"),
                Decimal("14.088"),
                Decimal("14.161"),
                Decimal("14.234"),
                Decimal("14.308"),
                Decimal("14.382"),
                Decimal("14.457"),
                Decimal("14.532"),
                Decimal("14.608"),
                Decimal("14.684"),
                Decimal("14.760"),
                Decimal("14.837"),
                Decimal("14.915"),
                Decimal("14.993"),
                Decimal("15.071"),
                Decimal("15.150"),
                Decimal("15.230"),
                Decimal("15.310"),
                Decimal("15.390"),
                Decimal("15.471"),
                Decimal("15.553"),
                Decimal("15.635"),
                Decimal("15.717"),
                Decimal("15.801"),
                Decimal("15.884"),
                Decimal("15.968"),
                Decimal("16.053"),
                Decimal("16.138"),
                Decimal("16.224"),
                Decimal("16.311"),
                Decimal("16.398"),
                Decimal("16.485"),
                Decimal("16.573"),
                Decimal("16.662"),
                Decimal("16.751"),
                Decimal("16.841"),
                Decimal("16.932"),
                Decimal("17.023"),
            ),
            "Carbon-Graphite",
            "Vf",
            "K23* (GPa)",
        )
        result2 = _get_K23eff_data_for_plot_and_filename(composite4)
        assert result2 == (
            "Fiberglass-Graphite_K23eff.png",
            (
                Decimal("0"),
                Decimal("0.01"),
                Decimal("0.02"),
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("0.05"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
                Decimal("0.11"),
                Decimal("0.12"),
                Decimal("0.13"),
                Decimal("0.14"),
                Decimal("0.15"),
                Decimal("0.16"),
                Decimal("0.17"),
                Decimal("0.18"),
                Decimal("0.19"),
                Decimal("0.2"),
                Decimal("0.21"),
                Decimal("0.22"),
                Decimal("0.23"),
                Decimal("0.24"),
                Decimal("0.25"),
                Decimal("0.26"),
                Decimal("0.27"),
                Decimal("0.28"),
                Decimal("0.29"),
                Decimal("0.3"),
                Decimal("0.31"),
                Decimal("0.32"),
                Decimal("0.33"),
                Decimal("0.34"),
                Decimal("0.35"),
                Decimal("0.36"),
                Decimal("0.37"),
                Decimal("0.38"),
                Decimal("0.39"),
                Decimal("0.4"),
                Decimal("0.41"),
                Decimal("0.42"),
                Decimal("0.43"),
                Decimal("0.44"),
                Decimal("0.45"),
                Decimal("0.46"),
                Decimal("0.47"),
                Decimal("0.48"),
                Decimal("0.49"),
                Decimal("0.5"),
                Decimal("0.51"),
                Decimal("0.52"),
                Decimal("0.53"),
                Decimal("0.54"),
                Decimal("0.55"),
                Decimal("0.56"),
                Decimal("0.57"),
                Decimal("0.58"),
                Decimal("0.59"),
                Decimal("0.6"),
                Decimal("0.61"),
                Decimal("0.62"),
                Decimal("0.63"),
                Decimal("0.64"),
                Decimal("0.65"),
                Decimal("0.66"),
                Decimal("0.67"),
                Decimal("0.68"),
                Decimal("0.69"),
                Decimal("0.7"),
                Decimal("0.71"),
                Decimal("0.72"),
                Decimal("0.73"),
                Decimal("0.74"),
                Decimal("0.75"),
                Decimal("0.76"),
                Decimal("0.77"),
                Decimal("0.78"),
                Decimal("0.79"),
                Decimal("0.8"),
                Decimal("0.81"),
                Decimal("0.82"),
                Decimal("0.83"),
                Decimal("0.84"),
                Decimal("0.85"),
                Decimal("0.86"),
                Decimal("0.87"),
                Decimal("0.88"),
                Decimal("0.89"),
                Decimal("0.9"),
                Decimal("0.91"),
                Decimal("0.92"),
                Decimal("0.93"),
                Decimal("0.94"),
                Decimal("0.95"),
                Decimal("0.96"),
                Decimal("0.97"),
                Decimal("0.98"),
                Decimal("0.99"),
                Decimal("1"),
            ),
            (
                Decimal("10.190"),
                Decimal("10.360"),
                Decimal("10.532"),
                Decimal("10.707"),
                Decimal("10.886"),
                Decimal("11.067"),
                Decimal("11.252"),
                Decimal("11.440"),
                Decimal("11.631"),
                Decimal("11.826"),
                Decimal("12.024"),
                Decimal("12.226"),
                Decimal("12.432"),
                Decimal("12.641"),
                Decimal("12.855"),
                Decimal("13.072"),
                Decimal("13.294"),
                Decimal("13.520"),
                Decimal("13.750"),
                Decimal("13.985"),
                Decimal("14.225"),
                Decimal("14.469"),
                Decimal("14.719"),
                Decimal("14.973"),
                Decimal("15.233"),
                Decimal("15.499"),
                Decimal("15.770"),
                Decimal("16.047"),
                Decimal("16.329"),
                Decimal("16.619"),
                Decimal("16.914"),
                Decimal("17.216"),
                Decimal("17.525"),
                Decimal("17.841"),
                Decimal("18.165"),
                Decimal("18.496"),
                Decimal("18.835"),
                Decimal("19.182"),
                Decimal("19.537"),
                Decimal("19.902"),
                Decimal("20.275"),
                Decimal("20.658"),
                Decimal("21.051"),
                Decimal("21.453"),
                Decimal("21.867"),
                Decimal("22.291"),
                Decimal("22.727"),
                Decimal("23.175"),
                Decimal("23.635"),
                Decimal("24.108"),
                Decimal("24.595"),
                Decimal("25.096"),
                Decimal("25.611"),
                Decimal("26.142"),
                Decimal("26.689"),
                Decimal("27.253"),
                Decimal("27.834"),
                Decimal("28.434"),
                Decimal("29.053"),
                Decimal("29.693"),
                Decimal("30.353"),
                Decimal("31.036"),
                Decimal("31.743"),
                Decimal("32.474"),
                Decimal("33.232"),
                Decimal("34.017"),
                Decimal("34.831"),
                Decimal("35.675"),
                Decimal("36.552"),
                Decimal("37.464"),
                Decimal("38.411"),
                Decimal("39.398"),
                Decimal("40.425"),
                Decimal("41.496"),
                Decimal("42.614"),
                Decimal("43.781"),
                Decimal("45.001"),
                Decimal("46.278"),
                Decimal("47.615"),
                Decimal("49.018"),
                Decimal("50.490"),
                Decimal("52.038"),
                Decimal("53.667"),
                Decimal("55.384"),
                Decimal("57.197"),
                Decimal("59.112"),
                Decimal("61.140"),
                Decimal("63.291"),
                Decimal("65.575"),
                Decimal("68.007"),
                Decimal("70.601"),
                Decimal("73.372"),
                Decimal("76.342"),
                Decimal("79.530"),
                Decimal("82.963"),
                Decimal("86.670"),
                Decimal("90.684"),
                Decimal("95.047"),
                Decimal("99.805"),
                Decimal("105.014"),
                Decimal("110.742"),
            ),
            "Fiberglass-Graphite",
            "Vf",
            "K23* (GPa)",
        )

    def test_get_K23eff_data_for_plot_and_filename_output_with_invalid_inputs(
            self, carbon, none_arg
    ):
        """
        Test output of ``_get_K23eff_data_for_plot_and_filename`` with invalid arguments
        that raise TypeError
        """
        with pytest.raises(TypeError):
            _get_K23eff_data_for_plot_and_filename()  # no argument
        with pytest.raises(TypeError):
            _get_K23eff_data_for_plot_and_filename(none_arg)  # argument is None
        with pytest.raises(TypeError):
            _get_K23eff_data_for_plot_and_filename(carbon)  # argument is not HT object

    @pytest.fixture
    def data_E1eff_dummy(self):
        """
        Dummy E1eff data for test_plot_and_save_Valid
        """
        return (
            "composite_E1eff.png",  # filename
            (  # fiber volume fraction
                0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1,
            ),
            (  # E1eff
                0,
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
                1000,
            ),
            "composite",  # composite name for legend
            "Vf",  # x-axis label
            "E1* (GPa)",  # y-axis label
        )

    def test_plot_and_save_output_1(self, data_E1eff_dummy):
        """
        Test output of ``_plot_and_save`` helper function with valid arguments where the
        first is `data_E1eff_dummy` and second is folder's name - "png_trial"
        """
        return_filename = _plot_and_save(data_E1eff_dummy, "png_trial")
        # Validate return value as the filename
        assert return_filename == "composite_E1eff.png"
        folder_path = "./png_trial"
        file_path = os.path.join(folder_path, "composite_E1eff.png")
        # Check the existence of the file and folder
        assert os.path.isfile(file_path) == True

    @pytest.fixture
    def data_G12eff_dummy(self):
        """
        Dummy G12eff data for test_plot_and_save_Valid
        """
        return (
            "composite_G12eff.png",  # filename
            (  # fiber volume fraction
                0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1,
            ),
            (  # E1eff
                0,
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
                1000,
            ),
            "composite",  # composite name for legend
            "Vf",  # x-axis label
            "G12* (GPa)",  # y-axis label
        )

    def test_plot_and_save_output_2(self, data_G12eff_dummy):
        """
        Test output of ``_plot_and_save`` helper function with valid arguments where the
        first is `data_G12eff_dummy` and second is folder's name - "png_trial"
        """
        return_filename = _plot_and_save(data_G12eff_dummy, "png_trial")
        # Validate return value as the filename
        assert return_filename == "composite_G12eff.png"
        folder_path = "./png_trial"
        file_path = os.path.join(folder_path, "composite_G12eff.png")
        # Check the existence of the file and folder
        assert os.path.isfile(file_path) == True

    @pytest.fixture
    def invalid_data_dummy1(self):
        """
        Invalid Dummy G12eff data 1 where filename is not str
        """
        return (
            ["composite_G12eff.png"],  # invalid filename
            (  # fiber volume fraction
                0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1,
            ),
            (  # E1eff
                0,
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
                1000,
            ),
            "composite",  # composite name for legend
            "Vf",  # x-axis label
            "G12* (GPa)",  # y-axis label
        )

    @pytest.fixture
    def invalid_data_dummy2(self):
        """
        Invalid Dummy G12eff data 2 where filename is not png file
        """
        return (
            "composite_G12eff.csv",  # invalid file extension
            (  # fiber volume fraction
                0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1,
            ),
            (  # E1eff
                0,
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
                1000,
            ),
            "composite",  # composite name for legend
            "Vf",  # x-axis label
            "G12* (GPa)",  # y-axis label
        )

    @pytest.fixture
    def invalid_data_dummy3(self):
        """
        Invalid Dummy G12eff data 3 where fiber volume is not given in tuple
        """
        return (
            "composite_G12eff.png",  # filename
            [  # fiber volume fraction not in tuple - invalid
                0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1,
            ],
            (  # E1eff
                0,
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
                1000,
            ),
            "composite",  # composite name for legend
            "Vf",  # x-axis label
            "G12* (GPa)",  # y-axis label
        )

    @pytest.fixture
    def invalid_data_dummy4(self):
        """
        Invalid Dummy G12eff data 4 where effective property not given in tuple
        """
        return (
            "composite_G12eff.png",  # filename
            (  # fiber volume fraction
                0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1,
            ),
            [  # E1eff not in tuple - invalid
                0,
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
                1000,
            ],
            "composite",  # composite name for legend
            "Vf",  # x-axis label
            "G12* (GPa)",  # y-axis label
        )

    @pytest.fixture
    def invalid_data_dummy5(self):
        """
        Invalid Dummy G12eff data 4 where tuple of fiber volume fraction and tuple of
        effective property are not of the same size
        """
        return (
            "composite_G12eff.png",  # filename
            (  # fiber volume fraction
                0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1,
            ),
            (  # E1eff not in tuple - invalid
                0,
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
            ),
            "composite",  # composite name for legend
            "Vf",  # x-axis label
            "G12* (GPa)",  # y-axis label
        )

    @pytest.fixture
    def invalid_data_dummy6(self):
        """
        Invalid Dummy G12eff data 1 where composite name for legend is not str object
        """
        return (
            "composite_G12eff.png",  # filename
            (  # fiber volume fraction
                0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1,
            ),
            (  # E1eff
                0,
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
                1000,
            ),
            5,  # composite name for legend is not str object - invalid
            "Vf",  # x-axis label
            "G12* (GPa)",  # y-axis label
        )

    @pytest.fixture
    def invalid_data_dummy7(self):
        """
        Invalid Dummy G12eff data 1 where x-axis label is not str object
        """
        return (
            "composite_G12eff.png",  # filename
            (  # fiber volume fraction
                0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1,
            ),
            (  # E1eff
                0,
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
                1000,
            ),
            "composite",  # composite name for legend
            10,  # x-axis label is not a str object - invalid
            "G12* (GPa)",  # y-axis label
        )

    @pytest.fixture
    def invalid_data_dummy8(self):
        """
        Invalid Dummy G12eff data 1 where y-axis label is not str object
        """
        return (
            "composite_G12eff.png",  # filename
            (  # fiber volume fraction
                0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1,
            ),
            (  # E1eff
                0,
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
                1000,
            ),
            "composite",  # composite name for legend
            "Vf",  # x-axis label
            15,  # y-axis label is not str object - invalid
        )

    @pytest.fixture
    def invalid_data_dummy9(self):
        """
        Invalid Dummy G12eff data 1 where x-axis is label is not "Vf"
        """
        return (
            "composite_G12eff.png",  # filename
            (  # fiber volume fraction
                0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1,
            ),
            (  # E1eff
                0,
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
                1000,
            ),
            "composite",  # composite name for legend
            "vf",  # x-axis label is not 'Vf' - invalid
            "G12* (GPa)",  # y-axis label
        )

    @pytest.fixture
    def invalid_data_dummy10(self):
        """
        Invalid Dummy G12eff data 1 where y-axis label is not one of the label of
        effective elastic property - 'E1* (GPa)', 'E2* (GPa)', 'G12* (GPa)', 'v12*',
        'G23* (GPa)', 'K23* (GPa)',
        """
        return (
            "composite_G12eff.png",  # filename
            (  # fiber volume fraction
                0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1,
            ),
            (  # E1eff
                0,
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
                1000,
            ),
            "composite",  # composite name for legend
            "Vf",  # x-axis label
            "G13*",  # y-axis label is not the correct label - invalid
        )

    def test_plot_and_save_output_with_invalid_inputs(
        self,
        data_E1eff_dummy,
        none_arg,
        invalid_data_dummy1,
        invalid_data_dummy2,
        invalid_data_dummy3,
        invalid_data_dummy4,
        invalid_data_dummy5,
        invalid_data_dummy6,
        invalid_data_dummy7,
        invalid_data_dummy8,
        invalid_data_dummy9,
        invalid_data_dummy10,
    ):
        """
        Test output of ``_plot_and_save`` helper function with invalid arguments that
        raises TypeError and ValuError
        """
        with pytest.raises(TypeError):
            _plot_and_save()  # No argument
        with pytest.raises(TypeError):
            _plot_and_save(none_arg, "png_trial")  # first argument is None
        with pytest.raises(TypeError):
            _plot_and_save(
                "dataE1eff", "png_trial"
            )  # first argument is not tuple object
        with pytest.raises(TypeError):
            _plot_and_save(data_E1eff_dummy, none_arg)  # second argument is not none
        with pytest.raises(TypeError):
            _plot_and_save(data_E1eff_dummy, 2)  # second argument is str
        with pytest.raises(TypeError):
            _plot_and_save(
                invalid_data_dummy1, "trial_png"
            )  # first argument tuple contains invalid filename
        with pytest.raises(ValueError):
            _plot_and_save(
                invalid_data_dummy2, "trial_png"
            )  # first argument tuple contains invalid filename
        with pytest.raises(TypeError):
            _plot_and_save(
                invalid_data_dummy3, "trial_png"
            )  # first argument tuple contains invalid fiber volume fractin
        with pytest.raises(TypeError):
            _plot_and_save(
                invalid_data_dummy4, "trial_png"
            )  # first argument tuple contains invalid effective modulus
        with pytest.raises(ValueError):
            _plot_and_save(
                invalid_data_dummy5, "trial_png"
            )  # first argument tuple contains invalid size of fiber volume fraction and effective moduli
        with pytest.raises(TypeError):
            _plot_and_save(
                invalid_data_dummy6, "trial_png"
            )  # first argument tuple contains invalid legend
        with pytest.raises(TypeError):
            _plot_and_save(
                invalid_data_dummy7, "trial_png"
            )  # first argument tuple contains invalid x-axis label
        with pytest.raises(TypeError):
            _plot_and_save(
                invalid_data_dummy8, "trial_png"
            )  # first argument tuple contains invalid y-axis label
        with pytest.raises(ValueError):
            _plot_and_save(
                invalid_data_dummy9, "trial_png"
            )  # first argument tuple contains invalid x-axis label
        with pytest.raises(ValueError):
            _plot_and_save(
                invalid_data_dummy10, "trial_png"
            )  # first argument tuple contains invalid y-axis label

    def test_is_confirmed_output(self):
        """
        Test output of ``_is_confirmed`` helper function with valid arguments, which
        follows from previous unit tests of `test_plot_and_save_output_1` and
        `test_plot_and_save_output_2`
        """
        # Confirm files are present resulting from previous unit test
        assert _is_confirmed("png_trial", "composite_E1eff.png") == True
        assert _is_confirmed("png_trial", "composite_G12eff.png") == True
        # Remove file composite_E1eff.png
        folder_path = "./png_trial"
        file_path1 = os.path.join(folder_path, "composite_E1eff.png")
        os.remove(file_path1)
        # Confirm composite_E1eff.png is no longer present
        assert os.path.isfile(file_path1) == False
        # Remove additional file and whole directory - clean up
        folder_path = "./png_trial"
        file_path = os.path.join(folder_path, "composite_G12eff.png")
        os.remove(file_path)
        os.rmdir("./png_trial")

    def test_is_confirmed_output_with_invalid_inputs(self, none_arg):
        """
        Test output of ``_is_confirmed`` helper function with valid arguments that raise
        TypeError
        """
        with pytest.raises(TypeError):
            _is_confirmed()  # No argument
        with pytest.raises(TypeError):
            _is_confirmed(none_arg, "composite_E1eff.png")  # First argument is None
        with pytest.raises(TypeError):
            _is_confirmed(2, "composite_E1eff.png")  # First argument is not str
        with pytest.raises(TypeError):
            _is_confirmed("png", none_arg)  # Second argument is None
        with pytest.raises(TypeError):
            _is_confirmed("png", ["composite_E1eff.png"])  # Second argument is not str

    def test_get_confirmation_notices_output(self):
        """
        Test output of ``_get_confirmation_notices`` helper function with valid
        arguments, which follows from previous unit tests of `test_plot_and_save_output_1`,
        `test_plot_and_save_output_2` and `test_is_confirmed_output`
        """
        # For saved file
        assert _get_confirmation_notices(True, "trial1.png") == (
            "========================= trial1.png file saved! ========================="
        )
        # For missing file as has been removed earlier in previous unit test
        assert _get_confirmation_notices(False, "trial2.png") == (
            "========================= trial2.png is missing! ========================="
        )

    def test_get_confirmation_notices_output_with_invalid_inputs(self, none_arg):
        """
        Test ``_get_confirmation_notices`` helper function with valid arguments that
        raise TypeError
        """
        with pytest.raises(TypeError):
            _get_confirmation_notices()  # no argument
        with pytest.raises(TypeError):
            _get_confirmation_notices(
                none_arg, "comp_E1eff.png"
            )  # first argument is None
        with pytest.raises(TypeError):
            _get_confirmation_notices(
                "4", "comp_E1eff.png"
            )  # first argument is not bool
        with pytest.raises(TypeError):
            _get_confirmation_notices("True", none_arg)  # second argument is None
        with pytest.raises(TypeError):
            _get_confirmation_notices("False", 2)  # second argument is not str

    def test_plot_output_1(
            self, composite1, composite2, composite3, composite4, capsys
    ):
        """
        Test ``plot`` major function with valid arguments, i.e 4 different UD composites
        having different constituent materials but are saved one at a time
        """
        # 1) New folder creation with plot(composite1) using default folder's name - "png"
        # with 6 png files saved in the folder
        plot(composite1)
        captured = capsys.readouterr()
        assert captured.out == (
            "Folder ./png created\n"
            + "=================== Carbon-Epoxy_E1eff.png file saved! ===================\n"
            + "=================== Carbon-Epoxy_E2eff.png file saved! ===================\n"
            + "================== Carbon-Epoxy_G12eff.png file saved! ===================\n"
            + "================== Carbon-Epoxy_G23eff.png file saved! ===================\n"
            + "================== Carbon-Epoxy_K23eff.png file saved! ===================\n"
            + "================== Carbon-Epoxy_v12eff.png file saved! ===================\n"
        )
        # Verify 6 files created
        folder_path = "./png"
        file_path1 = os.path.join(folder_path, "Carbon-Epoxy_E1eff.png")
        file_path2 = os.path.join(folder_path, "Carbon-Epoxy_E2eff.png")
        file_path3 = os.path.join(folder_path, "Carbon-Epoxy_G12eff.png")
        file_path4 = os.path.join(folder_path, "Carbon-Epoxy_G23eff.png")
        file_path5 = os.path.join(folder_path, "Carbon-Epoxy_K23eff.png")
        file_path6 = os.path.join(folder_path, "Carbon-Epoxy_v12eff.png")
        # Check the existence of the file and folder
        assert os.path.isfile(file_path1) == True
        assert os.path.isfile(file_path2) == True
        assert os.path.isfile(file_path3) == True
        assert os.path.isfile(file_path4) == True
        assert os.path.isfile(file_path5) == True
        assert os.path.isfile(file_path6) == True

        # 2) No new folder creation with plot(composite2) since default "png" folder
        # exists already but still 6 png files are saved in that folder
        plot(composite2)
        captured = capsys.readouterr()
        assert captured.out == (
            "================= Fiberglass-Epoxy_E1eff.png file saved! =================\n"
            + "================= Fiberglass-Epoxy_E2eff.png file saved! =================\n"
            + "================ Fiberglass-Epoxy_G12eff.png file saved! =================\n"
            + "================ Fiberglass-Epoxy_G23eff.png file saved! =================\n"
            + "================ Fiberglass-Epoxy_K23eff.png file saved! =================\n"
            + "================ Fiberglass-Epoxy_v12eff.png file saved! =================\n"
        )
        # Verify 6 files created
        folder_path = "./png"
        file_path7 = os.path.join(folder_path, "Fiberglass-Epoxy_E1eff.png")
        file_path8 = os.path.join(folder_path, "Fiberglass-Epoxy_E2eff.png")
        file_path9 = os.path.join(folder_path, "Fiberglass-Epoxy_G12eff.png")
        file_path10 = os.path.join(folder_path, "Fiberglass-Epoxy_G23eff.png")
        file_path11 = os.path.join(folder_path, "Fiberglass-Epoxy_K23eff.png")
        file_path12 = os.path.join(folder_path, "Fiberglass-Epoxy_v12eff.png")
        # Check the existence of the file and folder
        assert os.path.isfile(file_path7) == True
        assert os.path.isfile(file_path8) == True
        assert os.path.isfile(file_path9) == True
        assert os.path.isfile(file_path10) == True
        assert os.path.isfile(file_path11) == True
        assert os.path.isfile(file_path12) == True

        # 3) New folder creation with plot(composite3, folder="png_2") using user-defined
        # folder's name using keyword parameter, folder="png_2" with 6 png files saved
        # in that folder
        plot(composite3, folder="png_2")
        captured = capsys.readouterr()
        assert captured.out == (
            "Folder ./png_2 created\n"
            + "================= Carbon-Graphite_E1eff.png file saved! ==================\n"
            + "================= Carbon-Graphite_E2eff.png file saved! ==================\n"
            + "================= Carbon-Graphite_G12eff.png file saved! =================\n"
            + "================= Carbon-Graphite_G23eff.png file saved! =================\n"
            + "================= Carbon-Graphite_K23eff.png file saved! =================\n"
            + "================= Carbon-Graphite_v12eff.png file saved! =================\n"
        )
        # Verify 6 files created
        folder_path = "./png_2"
        file_path13 = os.path.join(folder_path, "Carbon-Graphite_E1eff.png")
        file_path14 = os.path.join(folder_path, "Carbon-Graphite_E2eff.png")
        file_path15 = os.path.join(folder_path, "Carbon-Graphite_G12eff.png")
        file_path16 = os.path.join(folder_path, "Carbon-Graphite_G23eff.png")
        file_path17 = os.path.join(folder_path, "Carbon-Graphite_K23eff.png")
        file_path18 = os.path.join(folder_path, "Carbon-Graphite_v12eff.png")
        # Check the existence of the file and folder
        assert os.path.isfile(file_path13) == True
        assert os.path.isfile(file_path14) == True
        assert os.path.isfile(file_path15) == True
        assert os.path.isfile(file_path16) == True
        assert os.path.isfile(file_path17) == True
        assert os.path.isfile(file_path18) == True

        # 4) No new folder creation with plot(composite4, folder="png_2") since "png_2"
        # exists already and 6 png files saved in that folder
        plot(composite4, folder="png_2")
        captured = capsys.readouterr()
        assert captured.out == (
            "=============== Fiberglass-Graphite_E1eff.png file saved! ================\n"
            + "=============== Fiberglass-Graphite_E2eff.png file saved! ================\n"
            + "=============== Fiberglass-Graphite_G12eff.png file saved! ===============\n"
            + "=============== Fiberglass-Graphite_G23eff.png file saved! ===============\n"
            + "=============== Fiberglass-Graphite_K23eff.png file saved! ===============\n"
            + "=============== Fiberglass-Graphite_v12eff.png file saved! ===============\n"
        )
        # Verify 6 files created
        folder_path = "./png_2"
        file_path19 = os.path.join(folder_path, "Fiberglass-Graphite_E1eff.png")
        file_path20 = os.path.join(folder_path, "Fiberglass-Graphite_E2eff.png")
        file_path21 = os.path.join(folder_path, "Fiberglass-Graphite_G12eff.png")
        file_path22 = os.path.join(folder_path, "Fiberglass-Graphite_G23eff.png")
        file_path23 = os.path.join(folder_path, "Fiberglass-Graphite_K23eff.png")
        file_path24 = os.path.join(folder_path, "Fiberglass-Graphite_v12eff.png")
        # Check the existence of the file and folder
        assert os.path.isfile(file_path19) == True
        assert os.path.isfile(file_path20) == True
        assert os.path.isfile(file_path21) == True
        assert os.path.isfile(file_path22) == True
        assert os.path.isfile(file_path23) == True
        assert os.path.isfile(file_path24) == True

        # Clean-up
        os.remove(file_path1)
        os.remove(file_path2)
        os.remove(file_path3)
        os.remove(file_path4)
        os.remove(file_path5)
        os.remove(file_path6)
        os.remove(file_path7)
        os.remove(file_path8)
        os.remove(file_path9)
        os.remove(file_path10)
        os.remove(file_path11)
        os.remove(file_path12)
        os.remove(file_path13)
        os.remove(file_path14)
        os.remove(file_path15)
        os.remove(file_path16)
        os.remove(file_path17)
        os.remove(file_path18)
        os.remove(file_path19)
        os.remove(file_path20)
        os.remove(file_path21)
        os.remove(file_path22)
        os.remove(file_path23)
        os.remove(file_path24)
        os.rmdir("./png")
        os.rmdir("./png_2")

    def test_plot_output_2(
            self, composite1, composite2, composite3, composite4, capsys
    ):
        """
        Test ``plot`` major function with valid arguments, i.e 4 different UD composites
        having different types of constituent materials but altogether saved in a single
        ``plot`` function
        """
        plot(composite1, composite2, composite3, composite4)
        captured = capsys.readouterr()
        assert captured.out == (
            "Folder ./png created\n"
            + "=================== Carbon-Epoxy_E1eff.png file saved! ===================\n"
            + "=================== Carbon-Epoxy_E2eff.png file saved! ===================\n"
            + "================== Carbon-Epoxy_G12eff.png file saved! ===================\n"
            + "================== Carbon-Epoxy_G23eff.png file saved! ===================\n"
            + "================== Carbon-Epoxy_K23eff.png file saved! ===================\n"
            + "================== Carbon-Epoxy_v12eff.png file saved! ===================\n"
            + "================= Fiberglass-Epoxy_E1eff.png file saved! =================\n"
            + "================= Fiberglass-Epoxy_E2eff.png file saved! =================\n"
            + "================ Fiberglass-Epoxy_G12eff.png file saved! =================\n"
            + "================ Fiberglass-Epoxy_G23eff.png file saved! =================\n"
            + "================ Fiberglass-Epoxy_K23eff.png file saved! =================\n"
            + "================ Fiberglass-Epoxy_v12eff.png file saved! =================\n"
            + "================= Carbon-Graphite_E1eff.png file saved! ==================\n"
            + "================= Carbon-Graphite_E2eff.png file saved! ==================\n"
            + "================= Carbon-Graphite_G12eff.png file saved! =================\n"
            + "================= Carbon-Graphite_G23eff.png file saved! =================\n"
            + "================= Carbon-Graphite_K23eff.png file saved! =================\n"
            + "================= Carbon-Graphite_v12eff.png file saved! =================\n"
            + "=============== Fiberglass-Graphite_E1eff.png file saved! ================\n"
            + "=============== Fiberglass-Graphite_E2eff.png file saved! ================\n"
            + "=============== Fiberglass-Graphite_G12eff.png file saved! ===============\n"
            + "=============== Fiberglass-Graphite_G23eff.png file saved! ===============\n"
            + "=============== Fiberglass-Graphite_K23eff.png file saved! ===============\n"
            + "=============== Fiberglass-Graphite_v12eff.png file saved! ===============\n"
        )

        # Verify all files are saved in "csv" folder
        folder_path = "./png"
        file_path1 = os.path.join(folder_path, "Carbon-Epoxy_E1eff.png")
        file_path2 = os.path.join(folder_path, "Carbon-Epoxy_E2eff.png")
        file_path3 = os.path.join(folder_path, "Carbon-Epoxy_G12eff.png")
        file_path4 = os.path.join(folder_path, "Carbon-Epoxy_G23eff.png")
        file_path5 = os.path.join(folder_path, "Carbon-Epoxy_K23eff.png")
        file_path6 = os.path.join(folder_path, "Carbon-Epoxy_v12eff.png")
        file_path7 = os.path.join(folder_path, "Fiberglass-Epoxy_E1eff.png")
        file_path8 = os.path.join(folder_path, "Fiberglass-Epoxy_E2eff.png")
        file_path9 = os.path.join(folder_path, "Fiberglass-Epoxy_G12eff.png")
        file_path10 = os.path.join(folder_path, "Fiberglass-Epoxy_G23eff.png")
        file_path11 = os.path.join(folder_path, "Fiberglass-Epoxy_K23eff.png")
        file_path12 = os.path.join(folder_path, "Fiberglass-Epoxy_v12eff.png")
        file_path13 = os.path.join(folder_path, "Carbon-Graphite_E1eff.png")
        file_path14 = os.path.join(folder_path, "Carbon-Graphite_E2eff.png")
        file_path15 = os.path.join(folder_path, "Carbon-Graphite_G12eff.png")
        file_path16 = os.path.join(folder_path, "Carbon-Graphite_G23eff.png")
        file_path17 = os.path.join(folder_path, "Carbon-Graphite_K23eff.png")
        file_path18 = os.path.join(folder_path, "Carbon-Graphite_v12eff.png")
        file_path19 = os.path.join(folder_path, "Fiberglass-Graphite_E1eff.png")
        file_path20 = os.path.join(folder_path, "Fiberglass-Graphite_E2eff.png")
        file_path21 = os.path.join(folder_path, "Fiberglass-Graphite_G12eff.png")
        file_path22 = os.path.join(folder_path, "Fiberglass-Graphite_G23eff.png")
        file_path23 = os.path.join(folder_path, "Fiberglass-Graphite_K23eff.png")
        file_path24 = os.path.join(folder_path, "Fiberglass-Graphite_v12eff.png")
        assert os.path.isfile(file_path1) == True
        assert os.path.isfile(file_path2) == True
        assert os.path.isfile(file_path3) == True
        assert os.path.isfile(file_path4) == True
        assert os.path.isfile(file_path5) == True
        assert os.path.isfile(file_path6) == True
        assert os.path.isfile(file_path7) == True
        assert os.path.isfile(file_path8) == True
        assert os.path.isfile(file_path9) == True
        assert os.path.isfile(file_path10) == True
        assert os.path.isfile(file_path11) == True
        assert os.path.isfile(file_path12) == True
        assert os.path.isfile(file_path13) == True
        assert os.path.isfile(file_path14) == True
        assert os.path.isfile(file_path15) == True
        assert os.path.isfile(file_path16) == True
        assert os.path.isfile(file_path17) == True
        assert os.path.isfile(file_path18) == True
        assert os.path.isfile(file_path19) == True
        assert os.path.isfile(file_path20) == True
        assert os.path.isfile(file_path21) == True
        assert os.path.isfile(file_path22) == True
        assert os.path.isfile(file_path23) == True
        assert os.path.isfile(file_path24) == True

        # Clean up
        os.remove(file_path1)
        os.remove(file_path2)
        os.remove(file_path3)
        os.remove(file_path4)
        os.remove(file_path5)
        os.remove(file_path6)
        os.remove(file_path7)
        os.remove(file_path8)
        os.remove(file_path9)
        os.remove(file_path10)
        os.remove(file_path11)
        os.remove(file_path12)
        os.remove(file_path13)
        os.remove(file_path14)
        os.remove(file_path15)
        os.remove(file_path16)
        os.remove(file_path17)
        os.remove(file_path18)
        os.remove(file_path19)
        os.remove(file_path20)
        os.remove(file_path21)
        os.remove(file_path22)
        os.remove(file_path23)
        os.remove(file_path24)
        os.rmdir("./png")

    def test_plot_output_with_invalid_inputs(self, carbon, composite1, none_arg):
        """
        Test output of ``save`` major function with invalid arguments
        """
        with pytest.raises(TypeError):
            plot()  # no argument
        with pytest.raises(TypeError):
            plot(none_arg)  # argument is None
        with pytest.raises(TypeError):
            plot(carbon)  # argument is not HT object
        with pytest.raises(TypeError):
            plot(composite1, none_arg)  # one of the arguments is None
        with pytest.raises(TypeError):
            plot(composite1, carbon)  # one of the arguments is not HT object
