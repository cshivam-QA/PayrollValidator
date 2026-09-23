from file_matcher import get_matching_files


def test_unreadable_xml_is_skipped_with_clear_warning(tmp_path, capsys):
    cb_folder = tmp_path / "cb"
    ac_folder = tmp_path / "ac"
    cb_folder.mkdir()
    ac_folder.mkdir()

    good_file = cb_folder / "good.xml"
    good_file.write_text(
        '<ROOT concept="C" location="00050" date="20260101" '
        'search="PAYROLL_EXPORT" created="x"><H0/></ROOT>'
    )

    corrupt_file = cb_folder / "corrupt.xml"
    corrupt_file.write_text("<ROOT><UNCLOSED></ROOT>")

    cb_files, ac_files = get_matching_files(str(cb_folder), str(ac_folder))

    captured = capsys.readouterr()

    # The corrupt file must still be safely skipped (not raise, not match).
    assert "00050_20260101" in cb_files
    assert len(cb_files) == 1

    # But now a clear warning naming the file and the reason must be printed.
    assert "corrupt.xml" in captured.out
    assert "WARNING" in captured.out
