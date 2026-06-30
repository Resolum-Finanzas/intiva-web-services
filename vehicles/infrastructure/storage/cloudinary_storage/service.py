import cloudinary
import cloudinary.uploader

import vehicles.infrastructure.storage.cloudinary_storage.config  # noqa: F401


class CloudinaryCarPhotoService:
    """Uploads car photos to Cloudinary and returns managed URLs."""

    UPLOAD_FOLDER = "vehicles/cars"

    @staticmethod
    def upload(image_data: bytes, public_id: str) -> str:
        """Upload raw image bytes to Cloudinary.

        Args:
            image_data (bytes): Raw image bytes to upload.
            public_id (str): Slugified identifier used as the Cloudinary
                public ID within ``UPLOAD_FOLDER``.

        Returns:
            str: The ``secure_url`` of the uploaded image.
        """
        result = cloudinary.uploader.upload(
            image_data,
            public_id=public_id,
            folder=CloudinaryCarPhotoService.UPLOAD_FOLDER,
            overwrite=True,
            resource_type="image",
        )
        return result["secure_url"]