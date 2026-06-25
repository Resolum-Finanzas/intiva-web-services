import cloudinary
import cloudinary.uploader

from vehicles.infrastructure.storage.cloudinary_storage import config  # noqa: F401


class CloudinaryCarPhotoService:

    UPLOAD_FOLDER = "vehicles/cars"

    @staticmethod
    def upload(image_data: bytes, public_id: str) -> str:
        result = cloudinary.uploader.upload(
            image_data,
            public_id=public_id,
            folder=CloudinaryCarPhotoService.UPLOAD_FOLDER,
            overwrite=True,
            resource_type="image",
        )
        return result["secure_url"]
    