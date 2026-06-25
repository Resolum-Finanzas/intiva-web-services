"""Cloudinary SDK configuration — shared infrastructure.

This module is the single place where the Cloudinary SDK is initialised with
credentials read from environment variables.  Any bounded context that needs
to interact with Cloudinary imports from here instead of calling
``cloudinary_storage.config()`` on its own, guaranteeing a single source of truth for
credentials.

Environment variables required:

- ``CLOUDINARY_CLOUD_NAME``
- ``CLOUDINARY_API_KEY``
- ``CLOUDINARY_API_SECRET``
"""

import os
import cloudinary

cloudinary.config(
    cloud_name=os.environ["CLOUDINARY_CLOUD_NAME"],
    api_key=os.environ["CLOUDINARY_API_KEY"],
    api_secret=os.environ["CLOUDINARY_API_SECRET"],
    secure=True,
)