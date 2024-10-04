import os
import subprocess
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.conf import settings
from .models import Presento
import uuid
import logging
from django.http import JsonResponse
import threading
import sys
import locale
from django.http import Http404

logger=logging.getLogger(__name__)

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        pptx_file = request.FILES['file']
        # Generate a process ID
        process_id = uuid.uuid4().hex
        print(process_id)
        #Create folder name: ID
        pross_dir=os.path.join(settings.MEDIA_ROOT,process_id)
        os.makedirs(pross_dir)
        #define file path
        file_name,_=os.path.splitext(pptx_file.name)
        file_folder = os.path.join(pross_dir, file_name)
        os.makedirs(file_folder, exist_ok=True)
        file_path=os.path.join(file_folder,pptx_file.name)
        # Save file into file path
        with open(file_path,'wb+')as f:
            for chunk in pptx_file.chunks():
                f.write(chunk)
        presentation = Presento(title=pptx_file.name, pptx_file=file_path, process_id=process_id)
        presentation.save()
        # Call the run_python_script function
        
        # Return the response
        return render(request, 'upload_file.html', {'process_id': process_id})
    else:
        return render(request, 'upload_file.html')

def run_python_script(request, process_id):
    # Construct the path to the script
    os.environ["LANG"] = "en_US.UTF-8"
    os.environ["LC_ALL"] = "en_US.UTF-8"
    os.environ["PYTHONIOENCODING"] = "utf-8"
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    script_path = os.path.join(settings.BASE_DIR, 'scripts', 'tts_v2.py')
    # Ensure that the path is properly quoted
    script_path_escaped = f'"{script_path}"' 
    # Construct the command to run the script
    command = f"python {script_path_escaped} {process_id}"
    logger.info(f"Running command: {command}")  # Log command
    
    try:
        # Run the command and capture output
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        
        # Log the script's output and errors
        logger.info(f"Script output: {result.stdout}")
        logger.info(f"Script error: {result.stderr}")
        presentation = Presento.objects.get(process_id=process_id)
        presentation.status = 'completed'
        presentation.save()
        # Return a JSON response indicating success
        return JsonResponse({'status': 'success', 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        # Log the error and return a JSON response indicating failure
        logger.error(f"Script error: {e.stderr}")
        return JsonResponse({'status': 'error', 'output': e.stderr})
   
def check_status(request, process_id):

    logger.info(f"Checking status for process_id: {process_id}")
    response = run_python_script(request, process_id)
    try:
        # Retrieve the presentation object based on process_id
        presentation = Presento.objects.get(process_id=process_id)
        
        # Get the current status from the presentation object
        status = presentation.status
        
        logger.info(f"Presentation status: {status}")

        if status == 'completed':
            return JsonResponse({'status': 'completed', 'presentation_id': presentation.id})
        else:
            return JsonResponse({'status': 'pending'})
    except Presento.DoesNotExist:
        logger.error(f"Presentation with process_id {process_id} does not exist.")
        return JsonResponse({'status': 'error'}, status=404)
    
def download_file(request, pk):
    presentation = get_object_or_404(Presento, pk=pk)
    if not presentation:
        return redirect('home')
        
    # Extract the process_id from the presentation object
    process_id = str(presentation.process_id).replace('-','')
    # Construct the folder path for this process ID
    folder_path = os.path.join(settings.MEDIA_ROOT, process_id)   
    # List to hold the paths of MP4 files
    mp4_paths = []   
    # Check if the directory exists
    if os.path.exists(folder_path):
        # Iterate through files in the directory
        for folder in os.listdir(folder_path):
            # Check if the file is an MP4 file
            output_path=os.path.join(folder_path,folder,"output")
            for file_name in os.listdir(output_path):
                if file_name.endswith(".mp4"):
                    file_path=os.path.join(folder_path,folder,'output',f'{file_name}')
            print(file_path)
            mp4_paths.append(file_path)  
    else:
        raise FileNotFoundError(f"Directory {folder_path} does not exist.")
    
    mp4_file_urls = [os.path.join(settings.MEDIA_URL, process_id, os.path.relpath(file, folder_path)) for file in mp4_paths]  
    print(mp4_file_urls)
    return render(request, 'download_file.html', {'presentation': presentation, 'mp4_file_urls': mp4_file_urls})

def home(request):
    #file = Presento.objects.all()  # Fetch all presentations
    return render(request, 'home.html')#, {'presentations': file})