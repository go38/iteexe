# ===========================================================================
# eXe 
# Copyright 2004-2005, University of Auckland
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# ===========================================================================

"""
A Wikipedia Idevice is one built from a Wikipedia article.
"""

import re
from exe.engine.beautifulsoup import BeautifulSoup
from exe.engine.idevice       import Idevice
from exe.engine.field         import TextAreaField

import urllib
class eXeURLopener(urllib.FancyURLopener):
    """
    Set a distinctive User-Agent, so Wikipedia.org knows we're not spammers
    """
    version = "eXe/exe@auckland.ac.nz"
urllib._urlopener = eXeURLopener()

import logging
import gettext
_ = gettext.gettext
log = logging.getLogger(__name__)

# ===========================================================================
class WikipediaIdevice(Idevice):
    """
    A Wikipedia Idevice is one built from a Wikipedia article.
    """
    Site = 'http://en.wikipedia.org/'
    def __init__(self):
        Idevice.__init__(self, _(u"Wikipedia Article"), 
                         _(u"University of Auckland"), 
                         _(u"""The Wikipedia iDevice takes a copy of an
article from en.wikipedia.org, including copying the associated images."""), 
                         u"", u"")
        self.articleName = u""
        self.article = TextAreaField(_(u"Article"))
        self.article.idevice = self
        self.images = {}
 

    def getResources(self):
        """
        Return the resource files used by this iDevice
        """
        resources = Idevice.getResources(self)
        for image in self.images:
            resources.append(image)
        return resources


    def loadArticle(self, name):
        """
        Load the article from Wikipedia
        """
        self.articleName = name

        name = urllib.quote(name.replace(" ", "_"))
        net  = urllib.urlopen(WikipediaIdevice.Site+'wiki/'+name)
        page = net.read()
        #open("test.html","w").write(page)
        net.close()
        #page = open("test.html").read()

        soup = BeautifulSoup(unicode(page, "iso-8859-1"))
        content = soup.first('div', {'id': "content"})

        if not content:
            print "no content"

        # clear out any old images
        for image in self.images:
            self.parentNode.package.deleteResource(image)
        self.images = {}

        # download the images
        for imageTag in content.fetch('img'):
            imageSrc  = unicode(imageTag['src'])
            imageName = self.id + u"_" + imageSrc.split('/')[-1]
            if imageName not in self.images:
                if not imageSrc.startswith("http://"):
                    imageSrc = WikipediaIdevice.Site + imageSrc
                imageDest = self.parentNode.package.resourceDir/imageName
                urllib.urlretrieve(imageSrc, imageDest)
                self.images[imageName] = True

            imageTag['src'] = (u"/" + self.parentNode.package.name + 
                               u"/resources/" + imageName)
                
        self.article.content = self.reformatArticle(unicode(content))


    def reformatArticle(self, content):
        """
        Changes links, etc
        """
        content = re.sub(r'href="/wiki/', 
                         r'href="'+WikipediaIdevice.Site+'wiki/', content)
        content = re.sub(r'<div class="editsection".*?</div>', '', content)
        #TODO Find a way to remove scripts without removing newlines
        content = content.replace("\n", "")
        content = re.sub(r'<script.*?</script>', '', content)
        return content


    def delete(self):
        """
        Delete the fields when this iDevice is deleted
        """
        for image in self.images:
            self.parentNode.package.deleteResource(image)
        self.images = {}
        Idevice.delete(self)

        

        
# ===========================================================================

if __name__ == "__main__":
    idev = WikipediaIdevice()
    idev.loadArticle("Mozilla Firefox")
#    print "<html><body>"
#    print idev.article.content
#    print "</body></html>"

