# ===========================================================================
# eXe 
# Copyright 2004-2006, University of Auckland
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
An iDevice built up from simple fields.
"""

from exe.engine.idevice import Idevice
# For backward compatibility Jelly expects to find a Field class
from exe.engine.field   import Field, TextField, TextAreaField, FeedbackField
import logging
log = logging.getLogger(__name__)


# ===========================================================================
class GenericIdevice(Idevice):
    """
    A generic Idevice is one built up from simple fields... as such it
    can have a multitude of different forms all of which are just simple
    XHTML fields.
    """
    persistenceVersion = 8
    
    def __init__(self, title, class_, author, purpose, tip):
        """
        Initialize 
        """
        if class_ in ("objectives", "activity", "reading", "preknowledge"):
            icon = class_
        else:
            icon = None
        Idevice.__init__(self, title, author, purpose, tip, icon)
        self.class_  = class_
        self.icon    = icon
        self.fields  = []
        self.nextFieldId = 0
        self.systemResources += ["common.js", "libot_drag.js"]


    def clone(self):
        """
        Clone a Generic iDevice just like this one
        """
        miniMe = Idevice.clone(self)
        for field in miniMe.fields:
            field.idevice = miniMe
        return miniMe


    def addField(self, field):
        """
        Add a new field to this iDevice.  Fields are indexed by their id.
        """
        if field.idevice:
            log.error(u"Field already belonging to %s added to %s" %
                      (field.idevice.title, self.title))
        field.idevice = self
        self.fields.append(field)
        
    def getUniqueFieldId(self):
        """
        Returns a unique id (within this idevice) for a field
        """
        self.calcNextFieldId()
        result = self.nextFieldId
        self.nextFieldId += 1
        return result
        
    def calcNextFieldId(self):
        """
        Returns a nextFieldId for a field
        """
        if self.nextFieldId == 0:
            maxId = 0
            for field in self.fields:
                if field.id > maxId:
                    maxId = field.id
                    self.nextFieldId = maxId 

    def __iter__(self):
        return iter(self.fields)

 
    def upgradeToVersion1(self):
        """
        Upgrades the node from version 0 (eXe version 0.4) to 1.
        Adds icon
        """
        log.debug("Upgrading iDevice")
        if self.class_ in ("objectives", "activity", "reading", "preknowledge"):
            self.icon = self.class_
        else:
            self.icon = "generic"


    def upgradeToVersion2(self):
        """
        Upgrades the node from version 1 (not released) to 2
        Use new Field classes
        """
        oldFields   = self.fields
        self.fields = []
        for oldField in oldFields:
            if oldField.fieldType == "Text":
                self.addField(TextField(oldField.__dict__['name'],
                                        oldField.instruction,
                                        oldField.content))
            elif oldField.fieldType == "TextArea":
                self.addField(TextAreaField(oldField.__dict__['name'],
                                            oldField.instruction,
                                            oldField.content))
            else:
                log.error(u"Unknown field type in upgrade "+oldField.fieldType)


    def upgradeToVersion3(self):
        """
        Upgrades the node from 2 (v0.5) to 3 (v0.6).
        Old packages will loose their icons, but they will load.
        """
        log.debug(u"Upgrading iDevice")
        self.emphasis = Idevice.SomeEmphasis


    def upgradeToVersion4(self):
        """
        Upgrades v0.6 to v0.7.
        """
        self.lastIdevice = False


    def upgradeToVersion5(self):
        """
        Upgrades exe to v0.10
        """
        self._upgradeIdeviceToVersion1()


    def upgradeToVersion6(self):
        """
        Upgrades to v0.12
        """
        self._upgradeIdeviceToVersion2()

        for field in self.fields:
            field._upgradeFieldToVersion2()

        self.systemResources += ["common.js", "libot_drag.js"]

    def upgradeToVersion7(self):
        """
        Upgrades to v0.13
        """
        # Upgrade old style reading activity's feedback field
        if self.class_ == 'reading':
            # Upgrade the feedback field
            for i, field in enumerate(self.fields):
                if isinstance(field, TextAreaField) and \
                   field.name in (_(u'Feedback'), u'Feedback'):
                    newField = FeedbackField(field.name, field.instruc)
                    Field.nextId -= 1
                    newField._id = field._id
                    newField.feedback = field.content
                    newField.idevice = self
                    self.fields[i] = newField
            # Upgrade the title
            if self.title == _(u'Reading Activity 0.11'):
                # If created in non-english, upgrade in non-english
                self.title = _(u'Reading Activity')
            if self.title == u'Reading Activity 0.11':
                # If created in english, upgrade in english
                self.title = u'Reading Activity'
                
    def upgradeToVersion8(self):
        """
        Upgrades to v0.20
        """
        self.nextFieldId = 0

        


# ===========================================================================
