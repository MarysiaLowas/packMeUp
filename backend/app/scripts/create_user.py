#!/usr/bin/env python3
import argparse
import asyncio
from typing import Optional
from uuid import UUID

from fastapi_sqlalchemy import AsyncDBSessionMiddleware  # type: ignore
from fastapi_sqlalchemy import async_db as db  # type: ignore
from passlib.context import CryptContext  # type: ignore

from app import settings  # an object to provide global access to a database session
from app.main import app
from app.models import User

dupa = AsyncDBSessionMiddleware(app, db_url=settings.POSTGRES_URL)

# Use the same password hashing as in UserService
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


async def create_user(
    email: str,
    password: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    is_admin: bool = False,
    user_id: Optional[UUID] = None,
) -> User:
    """Create a new user in the database.

    Args:
        email: User's email address
        password: Plain text password (will be hashed)
        first_name: Optional first name
        last_name: Optional last name
        is_admin: Whether the user should be an admin (default: False)
        user_id: Optional UUID for the user (default: None, will be auto-generated)

    Returns:
        The created User object
    """
    try:
        async with db():
            # Hash the password using bcrypt
            hashed_password = hash_password(password)

            # Create user object
            user = User(
                id=user_id,
                email=email,
                hashed_password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                is_admin=is_admin,
            )

            # Add to session and commit
            db.session.add(user)
            await db.session.commit()
            await db.session.refresh(user)

            print(f"Successfully created user: {email}")
            return user

    except Exception as e:
        print(f"Error creating user: {str(e)}")
        raise


def main():
    """Handle command line arguments and create a user."""
    parser = argparse.ArgumentParser(description="Create a new user in the database")

    # Required arguments
    parser.add_argument("--email", required=True, help="User's email address")
    parser.add_argument("--password", required=True, help="User's password")

    # Optional arguments
    parser.add_argument("--first-name", help="User's first name")
    parser.add_argument("--last-name", help="User's last name")
    parser.add_argument("--admin", action="store_true", help="Make the user an admin")
    parser.add_argument("--id", type=UUID, help="Specific UUID for the user")

    args = parser.parse_args()

    # Run the async function
    asyncio.run(
        create_user(
            email=args.email,
            password=args.password,
            first_name=args.first_name,
            last_name=args.last_name,
            is_admin=args.admin,
            user_id=args.id,
        )
    )


if __name__ == "__main__":
    main()
