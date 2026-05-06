def send_verification_email(email: str, token: str):
    print(f"\nVerify your email:")
    print(f"http://localhost:8000/auth/verify?token={token}\n")