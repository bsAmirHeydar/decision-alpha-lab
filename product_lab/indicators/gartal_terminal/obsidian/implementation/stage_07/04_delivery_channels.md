# 04 — Delivery Channels

Supported channels:

```text
Popup Alert()
Sound PlaySound()
Push SendNotification()
Email SendMail()
Log-only test mode
```

## Log-only mode

`InpAlertLogOnly=true` is used for safe validation. It lets the trader test the state machine without popup/sound spam.

## Cooldown

`InpAlertCooldownSeconds` prevents multiple distinct events from firing too rapidly in the same timer pass. Duplicate keys are still blocked independently.
