#!/usr/bin/env python3
import json
import os
import shutil
import struct
import subprocess
import sys
from urllib.parse import urlparse

ERROR_INVALID_REQUEST = 'INVALID_REQUEST'
ERROR_INVALID_URL = 'INVALID_URL'
ERROR_INVALID_PROFILE = 'INVALID_PROFILE'
ERROR_CHROME_NOT_FOUND = 'CHROME_NOT_FOUND'
ERROR_LAUNCH_FAILED = 'LAUNCH_FAILED'


def _read_native_message():
  raw_length = sys.stdin.buffer.read(4)
  if len(raw_length) == 0:
    return None
  if len(raw_length) < 4:
    raise ValueError('Failed to read message length.')

  message_length = struct.unpack('<I', raw_length)[0]
  payload = sys.stdin.buffer.read(message_length)
  if len(payload) < message_length:
    raise ValueError('Failed to read full message payload.')
  return json.loads(payload.decode('utf-8'))


def _write_native_message(message):
  encoded = json.dumps(message).encode('utf-8')
  sys.stdout.buffer.write(struct.pack('<I', len(encoded)))
  sys.stdout.buffer.write(encoded)
  sys.stdout.buffer.flush()


def _invalid(error_code, message, request_id=None):
  return {
      'ok': False,
      'requestId': request_id,
      'errorCode': error_code,
      'message': message,
      'launchedCommandSummary': None,
  }


def _validate_request(data):
  if not isinstance(data, dict):
    return _invalid(ERROR_INVALID_REQUEST, 'Request must be a JSON object.')

  request_id = data.get('requestId')
  if not isinstance(request_id, str) or not request_id or len(request_id) > 128:
    return _invalid(ERROR_INVALID_REQUEST, 'Invalid requestId.', request_id)

  if data.get('version') != 1 or data.get('action') != 'open_url_in_profile':
    return _invalid(ERROR_INVALID_REQUEST, 'Unsupported version or action.', request_id)

  profile = data.get('profileDirectory')
  if not isinstance(profile, str) or not profile.strip() or len(profile.strip()) > 128:
    return _invalid(ERROR_INVALID_PROFILE, 'Invalid profileDirectory.', request_id)

  url = data.get('url')
  if not isinstance(url, str):
    return _invalid(ERROR_INVALID_URL, 'URL is required.', request_id)

  parsed = urlparse(url)
  if parsed.scheme not in ('http', 'https'):
    return _invalid(ERROR_INVALID_URL, 'Only http/https URLs are allowed.', request_id)

  return {
      'ok': True,
      'requestId': request_id,
      'profileDirectory': profile.strip(),
      'url': url,
  }


def _find_chrome_path():
  env_override = os.getenv('SEND_TO_PROFILE_CHROME_PATH')
  if env_override and os.path.exists(env_override):
    return env_override

  candidates = [
      os.path.expandvars(r'%ProgramFiles%\Google\Chrome\Application\chrome.exe'),
      os.path.expandvars(r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe'),
      os.path.expandvars(r'%LocalAppData%\Google\Chrome\Application\chrome.exe'),
  ]

  for path in candidates:
    if path and os.path.exists(path):
      return path

  return shutil.which('chrome')


def _launch_chrome(chrome_path, profile_directory, url):
  args = [chrome_path, f'--profile-directory={profile_directory}', '--new-window', url]
  subprocess.Popen(args)
  return ' '.join(args)


def main():
  try:
    request = _read_native_message()
    if request is None:
      return

    validated = _validate_request(request)
    if validated.get('ok') is not True:
      _write_native_message(validated)
      return

    chrome_path = _find_chrome_path()
    if not chrome_path:
      _write_native_message(_invalid(
          ERROR_CHROME_NOT_FOUND,
          'Chrome executable not found.',
          validated['requestId'],
      ))
      return

    try:
      summary = _launch_chrome(chrome_path, validated['profileDirectory'], validated['url'])
    except Exception as exc:
      _write_native_message(_invalid(
          ERROR_LAUNCH_FAILED,
          f'Failed to launch Chrome: {exc}',
          validated['requestId'],
      ))
      return

    _write_native_message({
        'ok': True,
        'requestId': validated['requestId'],
        'errorCode': None,
        'message': 'Launched',
        'launchedCommandSummary': summary,
    })
  except Exception as exc:
    _write_native_message(_invalid(ERROR_INVALID_REQUEST, f'Host error: {exc}'))


if __name__ == '__main__':
  main()
