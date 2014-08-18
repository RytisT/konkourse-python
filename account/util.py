import StringIO
import os
from PIL import Image
import urllib2 as urllib
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


def createImage(image, dimensions):
    name = image.name
    image = Image.open(settings.MEDIA_ROOT + image.name)
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")

    # define file output dimensions (ex 60x60)
    x = dimensions[0]
    y = dimensions[1]

    # get orginal image ratio
    img_ratio = float(image.size[0]) / image.size[1]

    # resize but constrain proportions?
    if x == 0.0:
        x = y * img_ratio
    elif y == 0.0:
        y = x / img_ratio

    # output file ratio
    resize_ratio = float(x) / y
    x = int(x)
    y = int(y)

    # get output with and height to do the first crop
    if(img_ratio > resize_ratio):
        output_width = x * image.size[1] / y
        output_height = image.size[1]
        originX = image.size[0] / 2 - output_width / 2
        originY = 0
    else:
        output_width = image.size[0]
        output_height = y * image.size[0] / x
        originX = 0
        originY = image.size[1] / 2 - output_height / 2

    # crop
    cropBox = (originX, originY, originX + output_width, originY + output_height)
    image = image.crop(cropBox)

    # resize (doing a thumb)
    image.thumbnail([x, y], Image.ANTIALIAS)
    # re-initialize imageFile and set a hash (unique filename)
    imagefile = StringIO.StringIO()
    image.save(imagefile, 'png')
    imagefile.seek(0)
    suf = SimpleUploadedFile(os.path.split(name)[-1],
                             imagefile.read(), content_type='image/png')
    return suf
