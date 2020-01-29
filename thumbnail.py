from PIL import Image
from PIL import _imaging
import os  

max_width = 256
max_height = 256
image_format = "jpg"
output_dir = "/tmp/thumbnails"
output_bucket = "ameade-thumbnail-images"

def handler(event, context):  
  bucket = event['bucket']
  key = event['object']

  try:
    #tmp = "/tmp/" + key
    tmp = key
    download(bucket, key, tmp)

    # resize
    resized = resized_path(key)
    resize(tmp, resized)

    # upload resized image
    upload(resized, output_bucket, key)

    return  

  except Exception as e:  
      print(e)  
      
def resized_path(key):
  name = get_filename(os.path.basename(key))
  return '/tmp/{}.{}'.format(name, image_format)

def resize(src, dest):
  # pil image processing
  img = Image.open(src, 'r')  
  img.thumbnail((max_width, max_height), Image.ANTIALIAS)  
  print('format: ' + img.format)
  if img.format == 'PNG' and image_format == 'jpg':
    img = img.convert('RGB')
  print('image resized')
  return img.save(dest)

def download(source_bucket, source_object_key, tmp):
  """ Download the specified object to the tmp location """
  # TODO
  pass

def upload(src, dest_bucket, dest_object):
  """ Upload the specified src file to the specific object"""
  # TODO
  pass

def get_filename(key):
  filename = os.path.basename(key)  
  name, ext = os.path.splitext(filename)
  return name


if __name__ == "__main__":
    event = {
      "bucket": "ameade-original-images",
      "object": "flower.png",
    }
    handler(event, None)
