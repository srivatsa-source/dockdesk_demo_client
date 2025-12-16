def reset_password(email_address):
    """
    Initiates the password reset process.
    """
    if not email_address or "@" not in email_address:
        raise ValueError("Invalid email provided.")
    
    print(f"Sending reset link to {email_address}...")
    return True
