import sys
import base64

decode =  sys.argv[1].decode("hex")
print decode
print base64.b64encode(decode)
