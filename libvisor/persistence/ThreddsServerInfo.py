'''
Created on 4 de ene. de 2016

@author: IHC
'''

class ThreddsServerInfoObject(object):
    '''
    Simple object to store the most basic information required
    to access a thredds server.
    
    TODO: Improve input validators isValidName() and isValidURL()
    '''


    def __init__(self, serverName, serverURL):
        '''
        Constructor.
        
        :param serverName     An user readable server name, i.e. 'My Thredds Server'
        :type serverName      String
        
        :param serverBaseURL     The URL or IP where the server is located,
                                 i.e. : http://www.mythreddsstuff.com/thredds/, 
                                        http://192.168.1.10:5000/thredds
        :type serverBaseURL      String
        '''
        self.serverName = serverName
        self.serverURL = serverURL
        
        
    def getName(self):
        return self.serverName
    
    def getURL(self):
        return self.serverURL
    

def isValidName(name):
    """
    TODO: Fix!
    Validates if the same conforms to certain basic characteristics
    (e.g. length > 0, not null, doesn't contain '/' to avoid messing
    with Settings objects)
    """
    if name is None:
        return False
    else:
        return len(name) > 0 and len (name) < 30 and '/' not in name


def isValidURL(url):
    """
    TODO: Fix!
    Validates if the same conforms to certain basic characteristics
    (e.g. length limits, not null)
    """
    if url is None:
        return False
    else:
        return len(url) > 3 and len (url) < 100
