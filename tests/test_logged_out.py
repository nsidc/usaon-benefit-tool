def test_logged_out(client):
    actual = client.get('/').location
    expected = '/login?next=%2F'
    assert actual == expected
