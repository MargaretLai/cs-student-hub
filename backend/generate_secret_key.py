#!/usr/bin/env python3
"""
Generate a secure SECRET_KEY for Django production deployment
Run this script to generate a new secret key for your .env.production file
"""

from django.core.management.utils import get_random_secret_key


def generate_secret_key():
    """Generate a new Django secret key"""
    secret_key = get_random_secret_key()
    print("=" * 60)
    print("🔐 NEW PRODUCTION SECRET KEY GENERATED")
    print("=" * 60)
    print(f"SECRET_KEY={secret_key}")
    print("=" * 60)
    print()
    print("📋 INSTRUCTIONS:")
    print("1. Copy the SECRET_KEY line above")
    print("2. Add it to your .env.production file")
    print("3. Keep this key secret and secure!")
    print("4. Never commit this key to version control")
    print()
    print("⚠️  SECURITY NOTE:")
    print("Generate a new key for each environment (staging, production)")
    print("=" * 60)

    return secret_key


if __name__ == "__main__":
    generate_secret_key()
