# Authentication Service

## Password Reset
To initiate a password reset flow, the internal API requires the user's `email_address`.
This parameter must be provided (cannot be empty) and is validated to ensure it contains the "@" symbol. 

If either condition is not met, a `ValueError` is raised with the specific message: "Invalid email provided."

Upon successful validation, the system initiates the process of sending a reset link to the provided email address and returns `True`.

## Features
- Email validation with @ symbol check
- Clear error messages
- Boolean return value for success