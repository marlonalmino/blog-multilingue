from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from media.models import MediaAsset
import hashlib
from PIL import Image
import io


class MediaUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"detail": "missing_file"}, status=status.HTTP_400_BAD_REQUEST)
        fs = FileSystemStorage(location=str(settings.MEDIA_ROOT))
        saved_name = fs.save(f"uploads/{file.name}", file)
        full_path = settings.MEDIA_ROOT / saved_name
        with open(full_path, "rb") as f:
            checksum = hashlib.sha256(f.read()).hexdigest()
        width = None
        height = None
        mime = file.content_type or ""
        try:
            with Image.open(full_path) as img:
                width, height = img.size
        except Exception:
            pass
        asset, created = MediaAsset.objects.get_or_create(
            checksum=checksum,
            defaults={
                "storage_provider": "local",
                "path": saved_name.replace("\\", "/"),
                "mime_type": mime,
                "width": width,
                "height": height,
                "size_bytes": full_path.stat().st_size,
            },
        )
        return Response({"id": asset.id, "path": asset.path}, status=status.HTTP_201_CREATED)
