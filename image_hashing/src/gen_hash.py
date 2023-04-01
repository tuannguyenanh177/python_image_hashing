import os
from io import BytesIO
from PIL import Image
import imagehash
import json

def twos_complement(hexstr, bits):
        value = int(hexstr,16) #convert hexadecimal to integer

		#convert from unsigned number to signed number with "bits" bits
        if value & (1 << (bits-1)):
            value -= 1 << bits
        return value

def genHash():
  params = []
  for entry in os.scandir("./image_hashing/jpg"):
    with open(entry.path, "rb") as imageBinary:
      img = Image.open(imageBinary)
      imgHash = str(imagehash.dhash(img))
      hashInt = twos_complement(imgHash, 64) #convert from hexadecimal to 64 bit signed integer
      print(f"added image with hash {hashInt} {entry.name} to database")
      params.append({"hash": hashInt, "url": entry.name})
      imageBinary.close()
	

  with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(params, f, ensure_ascii=False, indent=2)
    f.close()


if __name__ == "__main__":
   genHash()


