"""torsion_analyzer views"""
import os
from io import StringIO
from wsgiref.util import FileWrapper
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TorsionAnalysis
from .tasks import calculate_torsion_analysis

ALLOWED_EXTENSIONS = ['.sdf']


@csrf_exempt
def torsion_analysis_perform(request):
    """Start a torsion analysis for a given set of molecules either as a string or a file"""
    if not request.method == 'POST':
        return JsonResponse({'error': 'request is not POST'}, status=400)

    if 'molFile' in request.FILES:
        mol_file = request.FILES['molFile']
        _basename, file_type = os.path.splitext(mol_file.name)
        if file_type not in ALLOWED_EXTENSIONS:
            error_string = 'invalid file extension is not {}'.format(' ,'.join(ALLOWED_EXTENSIONS))
            return JsonResponse({'error': error_string}, status=400)

        mol_string = mol_file.read().decode('ascii')
        torsion_analysis = TorsionAnalysis(mol_string=mol_string, file_type=file_type)
        torsion_analysis.save()
        calculate_torsion_analysis.delay(torsion_analysis.id)
        return JsonResponse(torsion_analysis.dict(detail=True), status=200)

    if 'molString' in request.POST and 'fileType' in request.POST:
        torsion_analysis = TorsionAnalysis(
            mol_string=request.POST['molString'],
            file_type=request.POST['fileType']
        )
        torsion_analysis.save()
        calculate_torsion_analysis.delay(torsion_analysis.id)
        return JsonResponse(torsion_analysis.dict(detail=True), status=200)

    return JsonResponse(
        {'error': 'Either molFile or molString and fileType are required'},
        status=400
    )


@csrf_exempt
def torsion_analysis_detail(request, torsion_analysis_id):
    """Retrieve a torsion analysis from the database"""
    try:
        torsion_analysis = TorsionAnalysis.objects.get(id=torsion_analysis_id)
    except TorsionAnalysis.DoesNotExist:
        return JsonResponse({'error': 'model not found'}, status=404)
    return JsonResponse(torsion_analysis.dict(detail=True), status=200)


@csrf_exempt
def torsion_analysis_download(request, torsion_analysis_id):
    """Retrieve the raw TSV of a torsion analysis"""
    try:
        torsion_analysis = TorsionAnalysis.objects.get(id=torsion_analysis_id)
    except TorsionAnalysis.DoesNotExist:
        return JsonResponse({'error': 'model not found'}, status=404)
    torsion_file = StringIO(torsion_analysis.result_string)
    torsion_file_name = 'torsion_analysis_{}.tsv'.format(torsion_analysis_id)
    response = HttpResponse(FileWrapper(torsion_file), content_type='application/tsv')
    response['Content-Disposition'] = 'attachment; filename=' + torsion_file_name
    return response
