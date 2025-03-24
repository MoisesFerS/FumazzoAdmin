from django.core.files.storage import Storage
from supabase import create_client, Client

class SupabaseStorage(Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.supabase: Client = create_client(
            'https://vezutwhcnhzoysmbvbhy.supabase.co',
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZlenV0d2hjbmh6b3lzbWJ2Ymh5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjU2MjYyNiwiZXhwIjoyMDU4MTM4NjI2fQ.y3acg9XUICMVgrb7tut_M2yOslY0pjbZAYFUQiJeHg8',
        )
        self.bucket_name = 'media-files'

    def _save(self, name, content):
        bucket = self.supabase.storage.from_(self.bucket_name)
        
        file_content = content.read()  # Lê o conteúdo do arquivo
        
        # Fazendo o upload do arquivo
        response = bucket.upload(name, file_content)
        
        # Verifica se houve erro na resposta do Supabase
        if hasattr(response, 'error') and response.error:
            raise Exception(f"Erro ao enviar arquivo para Supabase: {response.error}")
        
        # Se não houver erro, o upload foi bem-sucedido
        return name

    def url(self, name):
        # URL para acessar o arquivo armazenado no Supabase
        return f"https://vezutwhcnhzoysmbvbhy.supabase.co/storage/v1/object/public/{self.bucket_name}/{name}"
    
    def exists(self, name):
        """
        Verifica se o arquivo existe no armazenamento do Supabase.
        """
        bucket = self.supabase.storage.from_(self.bucket_name)
        
        try:
            # Tenta baixar o arquivo (se ele não existir, um erro será gerado)
            bucket.download(name)
            return True  # O arquivo existe
        except Exception:
            return False  # O arquivo não existe
