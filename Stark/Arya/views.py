from django.shortcuts import render,HttpResponse

from django.utils.encoding import smart_str
from Stark import settings
import os
from django.http import FileResponse

# Create your views here.




def file_download(request):

    file_path = request.GET.get('file_path')
    if file_path:
        file_center_dir = settings.SALT_CONFIG_FILES_DIR
        file_path = "%s%s" %(file_center_dir,file_path)
        print('file path:',file_path)
        filename = file_path.split('/')[-1]


        response = FileResponse(open(file_path, 'rb'))
        #response = HttpResponse(content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        response['X-Sendfile'] = smart_str(file_path)
        #response['Content-Length'] = os.stat(file_path).st_size
        # It's usually a good idea to set the 'Content-Length' header too.
        # You can also set any other required headers: Cache-Control, etc.

        return response

    else:
        raise  KeyError
