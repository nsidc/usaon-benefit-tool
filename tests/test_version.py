from usaon_vta_survey.constants.version import VERSION


def test_version_matches(client):
    actual = client.get('/login', follow_redirects=True).text
    expected = VERSION
    assert expected in actual
