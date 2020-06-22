import lief
from PIL import Image


def pe_to_img(namePe="ZoomInstaller.exe", img_format="RGB", ySize=64, xSize=64) :
  pe = lief.parse(namePe)
  section_text = [ x for x in list( pe.sections ) if "text" in x.name ]

  if len(section_text) < 1 :
    print("Cannot find .text")
    return []
  
  rets = "".join( [ chr(x) for x in section_text[0].content[:ySize*xSize]] )

  if img_format == "RGB" :
    rets = "".join( [ chr(x) for x in section_text[0].content[:ySize*xSize*3]] )

  output_img = Image.new(img_format, (ySize, xSize))
  output_img.frombytes(rets)
  output_img.save("img/output_{}.bmp".format(namePe))



pe_to_img()


