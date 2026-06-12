# -*- coding: utf-8 -*-
import subprocess, pathlib, os, sys, time
BASE = r"C:\Users\aimsb\Downloads\26년 1학기 생명의과학세미나 기말고사"
html = os.path.join(BASE, "생명의과학세미나_기말_정리본(일타강사).html")
pdf  = os.path.join(BASE, "생명의과학세미나_기말_정리본(일타강사).pdf")
uri = pathlib.Path(html).as_uri()
edges = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
         r"C:\Program Files\Google\Chrome\Application\chrome.exe"]
edge = next((e for e in edges if os.path.exists(e)), None)
print("browser:", edge)
print("uri:", uri)
if os.path.exists(pdf):
    try: os.remove(pdf)
    except Exception: pass
cmd = [edge, "--headless", "--disable-gpu", "--no-pdf-header-footer",
       "--run-all-compositor-stages-before-draw", "--virtual-time-budget=20000",
       f"--print-to-pdf={pdf}", uri]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
print("returncode:", r.returncode)
if r.stderr: print("stderr(tail):", r.stderr[-500:])
time.sleep(0.5)
print("PDF exists:", os.path.exists(pdf), "size:", os.path.getsize(pdf) if os.path.exists(pdf) else 0)
