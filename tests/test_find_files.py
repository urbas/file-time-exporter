from file_time_exporter import find_files


def test_by_glob(tmp_path):
    (tmp_path / "foo.txt").touch()
    assert list(find_files.by_glob(tmp_path, "foo*")) == [tmp_path / "foo.txt"]
