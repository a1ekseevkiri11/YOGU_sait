from django.views.generic import (
    ListView,
    View,
)


from django.shortcuts import (
    get_object_or_404,
)
from django.http import HttpResponse

from .models import (
    MotivationLetters,
)


class DownloadLetter(View):
    def get(self, request, letter_id):
        motivation_letter = get_object_or_404(MotivationLetters, id=letter_id)
        response = HttpResponse(motivation_letter.letter, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{motivation_letter.letter.name}"'
        return response