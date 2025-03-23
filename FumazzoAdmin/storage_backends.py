import os
from django.core.files.storage import Storage
from supabase import create_client, Client

class SupabaseStorage(Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY"),
        )
        self.bucket_name = os.getenv("SUPABASE_BUCKET")

    def _save(self, name, content):
        bucket = self.supabase.storage.from_(self.bucket_name)
        content.seek(0) 
        response = bucket.upload(name, content.read())  
        if response.get("error"):
            raise Exception(f"Erro ao enviar arquivo para Supabase: {response['error']}")
        return name

    def url(self, name):
        return f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/{self.bucket_name}/{name}"
