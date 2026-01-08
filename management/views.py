import zipfile
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from portal.models import Post, StudentResult, Department

@login_required
def teacher_dashboard(request):
    return render(request, 'management/dashboard.html')

@login_required
def create_post(request):
    if request.method == 'POST':
        Post.objects.create(
            author=request.user,
            post_type=request.POST.get('post_type'),
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            promotion=request.POST.get('promotion'),
            image=request.FILES.get('image'),
            video=request.FILES.get('video'),
            document_pdf=request.FILES.get('document_pdf')
        )
        return redirect('home')
    return render(request, 'management/create_post.html')

@login_required
def bulk_upload_results(request):
    if request.method == 'POST' and request.FILES.get('zip_file'):
        zip_file = request.FILES['zip_file']
        promotion = request.POST.get('promotion')
        name_mapping = {}
        with zipfile.ZipFile(zip_file, 'r') as archive:
            for f_name in archive.namelist():
                if f_name.endswith(('.xlsx', '.csv')):
                    with archive.open(f_name) as f:
                        df = pd.read_excel(f) if f_name.endswith('.xlsx') else pd.read_csv(f)
                        name_mapping = dict(zip(df['matricule'].astype(str), df['nom']))
            for f_name in archive.namelist():
                if f_name.endswith('.pdf'):
                    mat = f_name.split('/')[-1].replace('.pdf', '')
                    content = archive.read(f_name)
                    res, _ = StudentResult.objects.update_or_create(
                        student_id=mat, 
                        defaults={'author': request.user, 'student_name': name_mapping.get(mat, f"Étudiant {mat}"), 'promotion': promotion}
                    )
                    res.result_pdf.save(f"{mat}.pdf", ContentFile(content))
        return redirect('results')
    return render(request, 'management/bulk_upload.html')