# Native Messaging Protocol (v1)

## Request
```json
{
  "version": 1,
  "action": "open_url_in_profile",
  "requestId": "uuid",
  "url": "https://example.com",
  "profileDirectory": "Profile 1",
  "closeOriginalTabRequested": false
}
```

### Field rules
- `version`: must be `1`
- `action`: must be `open_url_in_profile`
- `requestId`: required string (max 128)
- `url`: required URL with `http` or `https` scheme
- `profileDirectory`: required string (1..128)
- `closeOriginalTabRequested`: optional boolean

## Response
```json
{
  "ok": true,
  "requestId": "uuid",
  "errorCode": null,
  "message": "Launched",
  "launchedCommandSummary": "chrome --profile-directory=Profile 1 --new-window https://example.com"
}
```

## Error codes
- `INVALID_REQUEST`
- `INVALID_URL`
- `INVALID_PROFILE`
- `CHROME_NOT_FOUND`
- `LAUNCH_FAILED`
