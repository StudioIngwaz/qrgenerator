from django.db import models
from django.core.files import File
import qrcode
from io import BytesIO

class QRCode(models.Model):
    url = models.URLField()
    qr_code = models.ImageField(upload_to='qrcodes/', default='path/to/default_qr_code.png')


    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        self.qr_code.save(f"qrcode_{self.id}.png", File(buffer), save=False)
        super().save(*args, **kwargs)
