from PIL import Image


# open an image file (.bmp,.jpg,.png,.gif) you have in the working folder
def ResizeImage(ext_out,width,height,imageFile,path_out):
    try:
        im1 = Image.open(imageFile)
        im2 = im1.resize((width, height), Image.NEAREST)  # use nearest neighbour
        im2.save(path_out+ext_out)
        print("mensaje","El Proceso se completo correctamente..!!")
    except Exception as error:
        print("Error: ",error)

def ResizePerWidth(ext_out,imageFile_source,size_width,path_out):
    try:
        img = Image.open(imageFile_source)
        wpercent = (size_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((size_width, hsize), Image.ANTIALIAS)
        img.save(path_out+ext_out)
        print("mensaje", "El Proceso se completo correctamente..!!")
    except Exception as error:
        print("Error: ", error)

ResizeImage(".png",800,300,"e:\\Escritorio\\django.png","e:\\Escritorio\\salidas")
ResizePerWidth(".jpg","e:\\Escritorio\\django.png",200,"e:\\Escritorio\\salidas2")
