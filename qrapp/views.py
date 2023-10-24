from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .models import QRCode
import qrcode
from io import BytesIO
from django.core.files import File
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def generate_qr(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        qr_code = QRCode(url=url)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_code.qr_code.save(f"qrcode_{qr_code.id}.png", File(buffer), save=False)
        qr_code.save()

        return HttpResponseRedirect(reverse('qrcode_display', args=[qr_code.id]))

    return render(request, 'index.html')

def qrcode_display(request, qrcode_id):
    qr_code = QRCode.objects.get(id=qrcode_id)
    return render(request, 'qrcode_display.html', {'qr_code': qr_code})
