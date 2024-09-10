import os
from minio import Minio
from minio.error import S3Error

class MinIOHelper:

    def __init__(self,endpoint:str,access_key:str, secret_key:str, bucket:str = None) -> None:
        """ 
        Connection setup to S3 Storage 
        
        :param endpoint: endpoint to S3 ( withot http\https)
        :param acces_key:
        :param secret_key:
        :param bucket : the name of the bucket 
        :param bucket_create : Creates a bucket if it is not present
        """
        self._endpoint = endpoint
        self._access_key = access_key
        self._secret_key= secret_key
        self._client = Minio(self._endpoint,self._access_key,self._secret_key)
        self._bucket_name = bucket
        
    def download_File(self,object_file:str, new_file_name:str=None):
        """ 
        download file from S3 Storage to local 
        
        :param object_file: path + file from S3
        :param new_file_name: path + file local

        """
        if(new_file_name==None):
            new_file_name = os.path.basename(object_file)
        self._client.fget_object(self._bucket_name,object_file,new_file_name)
    
    def upload_File(self,object_file:str,  file_path:str ):
        """
        upload file from local to S3-Storage

        :param object_file: path + file from S3
        :param new_file_name: path + file local  
        """
        if((object_file==None) or (not object_file)):
            object_file = os.path.basename(file_path)
        self._client.fput_object(self._bucket_name,object_file,file_path)

    def delete_File(self,object_file):
        """
        delete file from S3-Storage

        :param object_file: path + file from S3
        """
        self._client.remove_object(self._bucket_name,object_file,)
    
    def set_Bucket(self,new_bucket):
        """
        set the bucket 
        """
        self._bucket_name = new_bucket

    def print_all_buckets(self):
        """
        print all buckets 
        """
        bucket_names = []
        buckets = self._client.list_buckets()
        for bucket in buckets:
            bucket_names.append(bucket.name)
        return bucket_names
    
    def split_path(self, path):
        components = path.split("/")
        if "" in components:
            components.remove("")

        prefix = "/".join(components[:-1]) + "/"
        filename = components[-1]

        if(prefix == "/" or prefix == ""):
            prefix = None

        return (prefix, filename)
        
    def is_directory(self, uri:str, bucket_name:str = None):
        prefix, filename = self.split_path(uri)
        if bucket_name is None:
            bucket_name = self._bucket_name

        objects = self._client.list_objects(bucket_name, prefix=prefix)
        for obj in objects:
            if(obj.object_name == uri or obj.object_name == uri + "/"):
                if obj.is_dir:
                    return True
        return False
    
    def object_exists(self, uri:str, bucket_name:str = None):
        prefix, filename = self.split_path(uri)
        if bucket_name is None:
            bucket_name = self._bucket_name

        objects = self._client.list_objects(bucket_name, prefix=prefix)
        for obj in objects:
            if(obj.object_name == uri or obj.object_name == uri + "/"):
                return True
        return False

    def list_all_objects(self, bucket_name:str = None, recursive:bool = False, prefix:str = None):
        if bucket_name is None:
            bucket_name = self._bucket_name
        objects = self._client.list_objects(bucket_name, recursive=recursive, prefix = prefix)

        return objects
    
    def list_object_names(self, bucket_name:str = None, recursive:bool = False, prefix:str = None):
        object_names = []
        for obj in self.list_all_objects(bucket_name=bucket_name, recursive=recursive, prefix=prefix):
            object_names.append(obj.object_name) 
        return object_names
    
    def list_file_object_names(self, bucket_name:str = None, recursive:bool = False, prefix:str = None):
        dir_object_names = []
        for obj in self.list_all_objects(bucket_name=bucket_name, recursive=recursive, prefix=prefix):
            if obj.is_dir == False:
                dir_object_names.append(obj.object_name) 
        return dir_object_names
    
    def list_directory_object_names(self, bucket_name:str = None, recursive:bool = False, prefix:str = None):
        file_object_names = []
        for obj in self.list_all_objects(bucket_name=bucket_name, recursive=recursive, prefix=prefix):
            if obj.is_dir == True:
                file_object_names.append(obj.object_name) 
        return file_object_names
