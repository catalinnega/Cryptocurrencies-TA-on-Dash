from ochlv.ochlv_obj import StreamOCHLV
import time

stop_streaming = False

def ochlv_fn():
    stream_ochlv_obj = StreamOCHLV();
    while stop_streaming == False:
        stream_ochlv_obj.update()
        time.sleep(5)
