
import qi
import argparse
import threading
from naoqi import ALProxy





def main(IP, PORT):

    print "Connecting to", IP, "with port", PORT
    motion = ALProxy("ALMotion", IP, PORT)
    posture = ALProxy("ALRobotPosture", IP, PORT)
    tracker = ALProxy("ALTracker", IP, PORT)
    awareness = ALProxy("ALBasicAwareness", IP, PORT)
    memory = ALProxy("ALMemory", IP, PORT)
    speech = ALProxy("ALTextToSpeech", IP, PORT)
    
    # First, wake up.
    motion.wakeUp()

    fractionMaxSpeed = 0.8
    # Go to posture stand
    posture.goToPosture("StandInit", fractionMaxSpeed)
    

    awareness.pauseAwareness()


    # Add target to track.
    targetName = "RedBall"
    ballSize = 0.13
    diameterOfBall = ballSize
    tracker.unregisterAllTargets()
    tracker.registerTarget(targetName, diameterOfBall)

    trackingRedBall = False

    # set mode
    mode = "Move"
    tracker.setMode(mode)

    # Then, start tracker.
    tracker.track(targetName)

    

    print "ALTracker successfully started, now show a red ball to robot!"
    print "Use Ctrl+c to stop this script."

    def tracking():
        import time
        try:
            while True:
                time.sleep(0.1)
                print tracker.getTargetPosition()
                print tracker.isTargetLost()
                if tracker.isTargetLost():
                    lookingForTheBall()
        except KeyboardInterrupt:
            print
            print "Interrupted by user"
            print "Stopping..."

        # Stop tracker, go to posture Sit.
        tracker.stopTracker()
        tracker.unregisterAllTargets()

        awareness.resumeAwareness()
        posture.goToPosture("Sit", fractionMaxSpeed)
        motion.rest()
        print "ALTracker stopped."

    def lookingForTheBall():
        import math
        theta = math.pi / 2
        motion.moveTo(0, 0, theta)

    tracking()
    #t1 = threading.Thread(target=tracking)
    #t2 = threading.Thread(target=lookingForTheBall)

    #t1.start()
    #t2.start()



if __name__ == "__main__" :
    main("192.168.162.139",9559)
