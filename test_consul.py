import urllib.request
import urllib.error
import time

try:
    start = time.time()
    req = urllib.request.Request("http://127.0.0.1:18501/v1/kv/test", data=b"test", method="PUT")
    
    # Bypass proxy
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)
    
    with opener.open(req) as f:
        print(f"Got: {f.read()}, took {time.time() - start:.3f}s")
except Exception as e:
    print(f"Error: {e}")
