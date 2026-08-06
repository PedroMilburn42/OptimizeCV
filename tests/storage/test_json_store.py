import json

from rolesherpa.storage.json_store import JsonStore


def test_load_returns_default_when_file_is_missing(tmp_path):
    store = JsonStore(tmp_path / "seen_jobs.json", default={"seen": {}})
    assert store.load() == {"seen": {}}


def test_load_default_is_not_a_shared_mutable_reference(tmp_path):
    default = {"seen": {}}
    store = JsonStore(tmp_path / "seen_jobs.json", default=default)
    first = store.load()
    first["seen"]["x"] = 1
    assert store.load() == {"seen": {}}


def test_save_then_load_round_trips(tmp_path):
    path = tmp_path / "seen_jobs.json"
    store = JsonStore(path)
    data = {"seen": {"job-1": {"title": "Data Engineer", "status": "new"}}}

    store.save(data)

    assert store.load() == data
    assert json.loads(path.read_text()) == data


def test_save_creates_parent_directories(tmp_path):
    path = tmp_path / "nested" / "dir" / "seen_jobs.json"
    store = JsonStore(path)

    store.save({"seen": {}})

    assert path.exists()


def test_default_without_argument_is_empty_dict(tmp_path):
    store = JsonStore(tmp_path / "missing.json")
    assert store.load() == {}
