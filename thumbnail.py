from PIL import Image
from PIL import _imaging
import boto3  
import os  
import re  
import subprocess

s3 = boto3.client('s3')  

max_width = 256
max_height = 256
image_format = "jpg"
acl = "public-read"
output_dir = "/tmp/thumbnails"
output_bucket = "ameade-thumbnail-images"

def handler(event, context):  
  bucket = event['bucket']
  key = event['object']

  try:
    meta = metadata(bucket, key)
    # skip if image is already processed
    if 'image-processed' in meta and meta['image-processed'] == 'true':
      raise Exception('Already processed image')

    tmp = tmp_path(key)
    s3.download_file(Bucket=bucket, Key=key, Filename=tmp)

    # resize
    resized = resized_path(key)
    resize(tmp, resized)

    # upload resized image
    upload(resized, bucket, key)

    return  

  except Exception as e:  
      print(e)  
      

def tmp_path(key):
  filename = os.path.basename(key)  
  return u'/tmp/' + filename 

def resized_path(key):
  filename = os.path.basename(key)  
  return '/tmp/{}.{}'.format(filename, image_format)

def resize(src, dest):
  # pil image processing
  img = Image.open(src, 'r')  
  img.thumbnail((max_width, max_height), Image.ANTIALIAS)  
  print('format: ' + img.format)
  if img.format == 'PNG' and image_format == 'jpg':
    img = img.convert('RGB')
  print('image resized')
  return img.save(dest)
  
def metadata(bucket, key):
  return s3.head_object(Bucket=bucket, Key=key)['Metadata']

def download(bucket, key, dest):
  return s3.download_file(Bucket=bucket, Key=key, Filename=dest)  

def upload(src, bucket, dest):
  return s3.upload_file(Filename=src, Bucket=dest_bucket(bucket), Key=dest, ExtraArgs=extra_args())

def dest_bucket(bucket):
  return bucket if not output_bucket else output_bucket

def extra_args():
  return {'ContentType': content_type(), 'Metadata': {'image-processed': 'true'}, 'ACL': acl}

def content_type():
  if image_format in ['jpg', 'jpeg']:
    return 'image/jpeg'
  elif image_format == 'png':
    return 'image/png'
  else:
    return 'application/octet-stream'

def filename(key):
  filename = os.path.basename(key)  
  name, ext = os.path.splitext(filename)
  return name


if __name__ == "__main__":
    event = {
      "bucket": "ameade-original-images",
      "object": "flower.png",
    }
    handler(event, None)
