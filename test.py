import pytz
import datetime
from win32com.propsys import propsys, pscon


path_to_image = "test.mp4"

properties = propsys.SHGetPropertyStoreFromParsingName(path_to_image)
datetime = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
datetime = str(datetime)

print(datetime)

termination = input("PRESS ANY KEY TO CONTINUE")