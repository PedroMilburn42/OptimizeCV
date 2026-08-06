from rolesherpa.domain.dedup import canonical_key, filter_new, is_likely_duplicate, normalize_company_name
from rolesherpa.domain.models import JobPosting


def _posting(**overrides):
    defaults = dict(
        id="1",
        title="Data Engineer",
        company="Acme S.A.",
        url="https://example.com/jobs/1",
        source="linkedin",
        description="Build data pipelines with Python and SQL.",
    )
    defaults.update(overrides)
    return JobPosting(**defaults)


def test_normalize_strips_sa_suffix():
    assert normalize_company_name("Acme S.A.") == normalize_company_name("ACME S.A")


def test_normalize_strips_srl_suffix():
    assert normalize_company_name("Acme S.R.L.") == "acme"


def test_normalize_strips_sas_suffix_without_leftover_s():
    assert normalize_company_name("Acme S.A.S.") == "acme"


def test_normalize_strips_ltda_suffix():
    assert normalize_company_name("Acme Ltda.") == "acme"


def test_normalize_strips_parentheticals():
    assert normalize_company_name("Acme (Uruguay)") == "acme"


def test_normalize_strips_everything_after_comma():
    assert normalize_company_name("Acme, sucursal Uruguay") == "acme"


def test_normalize_strips_accents():
    assert normalize_company_name("Compañía Ñandú S.A.") == normalize_company_name("Compania Nandu SA")


def test_canonical_key_ignores_tracking_params():
    a = canonical_key("https://x.com/job/1?utm_source=a")
    b = canonical_key("https://x.com/job/1?utm_source=b")
    assert a == b


def test_canonical_key_differs_for_different_paths():
    a = canonical_key("https://x.com/job/1")
    b = canonical_key("https://x.com/job/2")
    assert a != b


def test_canonical_key_is_case_insensitive():
    a = canonical_key("https://X.com/Job/1")
    b = canonical_key("https://x.com/job/1")
    assert a == b


def test_same_url_is_a_duplicate_regardless_of_other_fields():
    a = _posting(id="1", url="https://x.com/job/1?utm=a", title="Data Engineer")
    b = _posting(id="2", url="https://x.com/job/1?utm=b", title="Something Else Entirely")
    assert is_likely_duplicate(a, b) is True


def test_cross_posted_role_is_detected_via_fuzzy_match():
    a = _posting(
        url="https://linkedin.com/jobs/1",
        company="Acme S.A.",
        title="Senior Data Engineer",
        description="Build and maintain data pipelines using Python, SQL, and Airflow.",
    )
    b = _posting(
        url="https://computrabajo.com/jobs/2",
        company="ACME SA",
        title="Senior Data Engineer",
        description="Build and maintain data pipelines using Python, SQL and Airflow.",
    )
    assert is_likely_duplicate(a, b) is True


def test_different_roles_at_same_company_are_not_merged():
    a = _posting(
        url="https://linkedin.com/jobs/1",
        company="Acme S.A.",
        title="Data Engineer",
        description="Build data pipelines with Python and SQL.",
    )
    b = _posting(
        url="https://computrabajo.com/jobs/2",
        company="Acme S.A.",
        title="Office Receptionist",
        description="Greet visitors and manage the front desk.",
    )
    assert is_likely_duplicate(a, b) is False


def test_different_companies_are_not_merged_even_with_similar_titles():
    a = _posting(url="https://linkedin.com/jobs/1", company="Acme S.A.", title="Data Engineer")
    b = _posting(url="https://computrabajo.com/jobs/2", company="Globex S.A.", title="Data Engineer")
    assert is_likely_duplicate(a, b) is False


def test_missing_description_on_either_side_prevents_a_false_positive():
    a = _posting(url="https://linkedin.com/jobs/1", company="Acme S.A.", title="Data Engineer", description=None)
    b = _posting(url="https://computrabajo.com/jobs/2", company="Acme S.A.", title="Data Engineer")
    assert is_likely_duplicate(a, b) is False


def test_filter_new_separates_new_from_duplicate_against_existing():
    existing = [_posting(id="existing-1", url="https://linkedin.com/jobs/1")]
    candidate_dup = _posting(id="new-1", url="https://linkedin.com/jobs/1?utm=x", title="Different Title")
    candidate_new = _posting(id="new-2", url="https://computrabajo.com/jobs/9", title="Backend Engineer")

    new, duplicates = filter_new([candidate_dup, candidate_new], existing)

    assert new == [candidate_new]
    assert len(duplicates) == 1
    assert duplicates[0][0] == candidate_dup
    assert duplicates[0][1] == existing[0]


def test_filter_new_deduplicates_within_the_candidate_batch_itself():
    a = _posting(id="a", url="https://linkedin.com/jobs/1", title="Data Engineer")
    b = _posting(id="b", url="https://linkedin.com/jobs/1?utm=tracking", title="Data Engineer")

    new, duplicates = filter_new([a, b], existing=[])

    assert new == [a]
    assert len(duplicates) == 1
    assert duplicates[0][0] == b


def test_filter_new_with_no_existing_and_no_internal_dupes_returns_all_as_new():
    a = _posting(id="a", url="https://linkedin.com/jobs/1", company="Acme S.A.", title="Data Engineer")
    b = _posting(id="b", url="https://computrabajo.com/jobs/2", company="Globex S.A.", title="Sales Manager")

    new, duplicates = filter_new([a, b], existing=[])

    assert new == [a, b]
    assert duplicates == []
