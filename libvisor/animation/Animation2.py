'''
Created on 28 de ene. de 2016

@author: IHC
'''

class AnimationData(object):
    '''
    Conveniently holds frame information for animations and provides
    a method to retrieve frames based on a dateTime object to know
    the time (frame) to request and a timedelta to know how much
    deviation from that time is accepted when looking for the nearest
    frame to that provided dateTime. 
    
    This object is used in AnimationLayer objects as the animationData
    attribute. 
    '''


    def __init__(self, animationName, framesDict):
        """
        :param    animationName:  An identifier for this animation.
        :type     animationName:  [str]
        
        :param    framesDict:    A dictionary in which the key identifies what
                                 time is it's layer value showing.
        :type     framesDict:    dict(TimeStamp : MapToShow)
        """
        self.animationName = animationName
        self.frameData = framesDict
            
            
    def getName(self):
        return self.animationName
        
        
    def getFrameByTime(self, time, tolerance = None):
        """
        :param    time:    The time we want data about.
        :type     time:    datetime
        
        :param    tolerance: The max deviation from that time we want data from,
                             or none for "exact value" (inclusive)
        :type     tolerance: datetime.timedelta
        
        """
        if tolerance is None:
            #print(self.animationName+"Exact frame for "+str(time)+" found.")
            frame = self.frameData[time]
        else:
            try:
                frame = self.frameData[time]
                #print(self.animationName+" 2 -Exact frame for "+str(time)+" found.")
            except KeyError:
                #print(self.animationName+"Exact frame for "+str(time)+" not found. Evaluating deltas")
                possibleFrame = min(self.frameData.keys(), key = lambda date : abs(date - time))
                #print("POSSIBLE FRAME: "+str(possibleFrame))
                #print("DEVIATION: "+str(abs(possibleFrame - time))+" from a tolerance of: "+str(tolerance))
                if abs(possibleFrame - time) <= tolerance:
                    frame = self.frameData[possibleFrame]
                    #print("returning frame: "+str(frame.name()))
                else:
                    #print("frame does not fit delta")
                    raise KeyError
            
        return frame 
        
        