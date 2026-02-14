import host


def test_validate_ok():
  response = host._validate_request({
      'version': 1,
      'action': 'open_url_in_profile',
      'requestId': 'id-1',
      'url': 'https://example.com',
      'profileDirectory': 'Profile 1'
  })
  assert response['ok'] is True


def test_invalid_scheme():
  response = host._validate_request({
      'version': 1,
      'action': 'open_url_in_profile',
      'requestId': 'id-1',
      'url': 'chrome://settings',
      'profileDirectory': 'Profile 1'
  })
  assert response['ok'] is False
  assert response['errorCode'] == host.ERROR_INVALID_URL


def test_invalid_profile():
  response = host._validate_request({
      'version': 1,
      'action': 'open_url_in_profile',
      'requestId': 'id-1',
      'url': 'https://example.com',
      'profileDirectory': ''
  })
  assert response['ok'] is False
  assert response['errorCode'] == host.ERROR_INVALID_PROFILE
