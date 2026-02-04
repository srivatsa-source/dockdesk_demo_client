def reset_password(user_email):
    """
    Initiates the password reset process.
    """
    if not user_email:
        raise ValueError("Email is required")
    
    print(f"Password reset initiated for {user_email}")
    return {"status": "success", "message": "Reset link sent"}
