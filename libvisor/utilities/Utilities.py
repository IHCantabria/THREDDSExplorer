"""
Created on 8 de ene. de 2016

@author: IHC
"""

import re
import sys

def combineURLS(urlA, urlB,contentBetween=""):
        """This method is designed to concatenate an urlB which may be
        either relative to a 'middle' element of urlA, relative to the urlA
        final element, or a complete URL in an "intelligent" way.

        Will check, section by section of the URL (elements separated by '/')
        if the URL's have matching elements. If they do, a new URL will be
        returned which (hopefully) properly manages any "subfolder" which is
        repeated between both url's. Otherwise, it'll will only concatenate
        both.
        As an example, take the urlA: http://www.google.es/things/yourthings/
        and the urlB:                 yourthings/thing1.html.
        If we perform a direct concatenation, we would end up with an (in our
        example) invalid URL:
            http://www.google.es/things/yourthings/yourthings/thing1.html.

        If we perform a check by element, we will be able to eliminate the
        redundant elements informed in both URL's and construct the correct
        one. This is useful in environments in which you can not be sure if
        a given URL is relative to other, is relative but contains part
        of other, or is a full URL itself.

        As another joy, if you have two urls...
            http://www.url.com/elements/stored/thing1.xml
        and you pass it a whatever url...
            /stored/thing2.xml...
        this method will return...
            http://www.url.com/elements/stored/thing2.xml

        discarding any potential not interesting parts of the url. Including
        any file referenced at the end of the urlA (any thing.ext stuff).

        Use with care. A lot of.

        :param contentBetween: If you wish to insert another element
                                between both URL's (other than a slash)
                                put it here.
        :type contentBetween:  String
        """
        #This check here saves hassle later on...
        if contentBetween is None:
            contentBetween = ''
        if urlB is None:
            urlB = ''
        if urlA is None:
            urlA = ''

        #We will remove any potential file references from urlA:
        #We will assume it has to be removed for good.
        #
        #Workaround for IH Cantabria THREDDS structure.
        hasFilePattern = re.compile(r'[\w][/][\w]+[.][\w]{1,4}') #To avoid accidentally throwing away .com or www. stuff...
        fileCheck = hasFilePattern.findall(urlA)
        if fileCheck is not None and len(fileCheck) > 0:
            matchFilename = (fileCheck[-1])[2:] #We take only the last occurence, hopefully a /file.wha thing, and ignore its first two letters ('x/')
            urlA = urlA.replace(matchFilename, '')



        #This will split the URL into..
        #HTTP:    //    www.example.com/dfsdf/aas/...
        protocol = urlA.split('//')
        #We take the last element (URL part) and split it again.
        firstElements = (protocol[len(protocol)-1].rstrip('/')).split('/')


        secondElements = (urlB.lstrip('/')).split('/')
        #print(firstElements)
        #print(secondElements)
        iteration = 0
        for elementA in firstElements[::-1]: #We check from the end, reverse order
            if secondElements[0].lower() == elementA.lower():
                #print iteration
                #print("MATCH: "+secondElements[iteration] + "-" + elementA)

                #After the match, we append the
                #first elements and all the "B" elements
                #we have and construct a new URL.
                returnURL = protocol[0]+'//'
                for element in firstElements[0:(len(firstElements)-1)-iteration]:
                    returnURL+=element+'/'

                #We add the "content between" sent as parameter.
                contentBetween = contentBetween.strip("/") #Yeah, we also check this one.. just in case..
                returnURL=returnURL.rstrip('/')+contentBetween+'/'
                returnURL+=urlB.lstrip('/')
                #print("CONSTRUCTED URL --- "+returnURL)
                return returnURL
            iteration+=1

        #If no matching could be done above, we return a simple concatenation,
        #making sure only one slash is between both segments.
        contentBetween = contentBetween.strip("/") #Yeah, we also check this one.. just in case..

        #With this we sill make sure there will -only- be a single slash
        #between URL components.
        if contentBetween is not None and len(contentBetween) != 0:
            returnURL = urlA.rstrip('/')+'/'+contentBetween+'/'+urlB.lstrip('/')
        else:
            returnURL = urlA.rstrip('/')+'/'+urlB.lstrip('/')

        #print "A:"+urlA
        #print "B:"+urlB
        #print "MIX:"+returnURL
        return returnURL

def is_linux():
    """Returns True if we are running on a Linux system. False otherwise."""

    return sys.platform.startswith('linux')

