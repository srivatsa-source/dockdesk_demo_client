# Authentication Service

## Password Reset
To initiate a password reset flow, the internal API requires the user's `email_address`.
This parameter must be a non-empty string and must contain the "@" symbol for basic validation checks to pass.
This email address is then used to send the reset link directly to the user's primary contact method.