from cscore import CameraServer

def main():
    cs = CameraServer.getInstance()
    camera = cs.startAutomaticCapture(dev = 0)
    camera2 = cs.startAutomaticCapture(dev = 1)
    camera.setResolution(320,240)

    cs.waitForever()


