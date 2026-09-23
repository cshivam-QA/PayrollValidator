import pytest

from xml_loader import XMLLoader


def test_valid_xml_loads_as_before(tmp_path):
    xml_file = tmp_path / "valid.xml"
    xml_file.write_text(
        '<ROOT concept="C" location="00050" date="20260101" '
        'search="PAYROLL_EXPORT" created="x"><H0/></ROOT>'
    )

    loader = XMLLoader(str(xml_file))

    assert loader.get_root().tag == "ROOT"
    assert loader.get_root_info()["location"] == "00050"
    assert loader.get_root_info()["date"] == "20260101"


def test_corrupt_xml_raises_clear_error(tmp_path):
    xml_file = tmp_path / "corrupt.xml"
    xml_file.write_text("<ROOT><UNCLOSED></ROOT>")

    with pytest.raises(ValueError) as exc_info:
        XMLLoader(str(xml_file))

    assert str(xml_file) in str(exc_info.value)


def test_missing_xml_file_raises_clear_error(tmp_path):
    missing_file = tmp_path / "does_not_exist.xml"

    with pytest.raises(ValueError) as exc_info:
        XMLLoader(str(missing_file))

    assert str(missing_file) in str(exc_info.value)
