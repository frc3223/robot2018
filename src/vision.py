from cscore import CameraServer

def main():
    cs = CameraServer.getInstance()
    camera = cs.startAutomaticCapture()
    camera.setResolution(320,240)
