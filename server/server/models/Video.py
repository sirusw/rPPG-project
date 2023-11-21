from django.db import models

class Video(models.Model):
    # FilePathField will store the file path of the video, you can also use FileField if you want Django to handle file storage
    video_file = models.FileField(upload_to='../media/videos')
    
    # Metadata
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    frame_rate = models.FloatField()
    length = models.FloatField()
    
    # Additional fields
    created_at = models.DateTimeField(auto_now_add=True)