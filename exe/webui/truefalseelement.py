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
TrueFalseElement is responsible for a block of question. Used by TrueFalseBlock.
"""

import logging
from exe.webui import common

log = logging.getLogger(__name__)
# ===========================================================================
class TrueFalseElement(object):
    """
    TrueFalseElement is responsible for a block of question. 
    Used by TrueFalseBlock.
    """
    def __init__(self, index, idevice, question):
        """
        Initialize
        """
        self.index      = index
        self.id         = unicode(index) + "b" + idevice.id        
        self.idevice    = idevice
        self.question   = question
        self.questionId = "question"+ unicode(index) + "b" + idevice.id
        self.keyId      = "Key" + unicode(index) + "b" + idevice.id       
        self.feedbackId = "feedback" + unicode(index) + "b" + idevice.id 
        self.hintId     = "hint" + unicode(index) + "b" + idevice.id 
        

    def process(self, request):
        """
        Process arguments from the webserver.  Return any which apply to this 
        element.
        """
        log.debug("process " + repr(request.args))
        
        if self.questionId in request.args:
            self.question.question = request.args[self.questionId][0]
            
        if self.hintId in request.args:
            self.question.hint = request.args[self.hintId][0]
                        
        if self.keyId in request.args:
            if request.args[self.keyId][0] == "true":
                self.question.isCorrect = True 
                log.debug("question " + repr(self.question.isCorrect))
            else:
                self.question.isCorrect = False        
        
        if self.feedbackId in request.args:
            self.question.feedback = request.args[self.feedbackId][0]
            
        if "action" in request.args and request.args["action"][0] == self.id:
            self.idevice.questions.remove(self.question)


    def renderEdit(self):
        """
        Returns an XHTML string for editing this option element
        """
        question = self.question.question
        feedback = self.question.feedback
        hint     = self.question.hint
        
        question = question.replace("\r", "")
        question = question.replace("\n", "\\n")
        question = question.replace("'", "\\'")
        question = question.replace("\"", "\\\"")
        
        feedback = feedback.replace("\r", "")
        feedback = feedback.replace("\n", "\\n")
        feedback = feedback.replace("'", "\\'")
        feedback = feedback.replace('"', '\\"')
        
        hint = hint.replace("\r", "")
        hint = hint.replace("\n", "\\n")
        hint = hint.replace("'", "\\'")
        hint = hint.replace('"', '\\"')
        
        html = u"<tr><td>"
        html += common.richTextArea(self.questionId, question)
        html += u"</td><td>\n"
        html += common.option(self.keyId, self.question.isCorrect, "true") 
        #html += u"</td><td>\n"
        html += common.option(self.keyId, not self.question.isCorrect, "false")
        html += u"</td><td></td><td>\n"
        html += common.richTextArea(self.feedbackId, feedback)
        html += u"</td><td>\n"
        html += common.richTextArea(self.hintId, hint)
        html += u"</td><td>\n"
        html += common.submitImage(self.id, self.idevice.id, 
                                   "/images/stock-cancel.png",
                                   _("Delete option"))
        html += u"</td></tr>\n"
        return html
    
    def renderQuestionView(self):
        """
        Returns an XHTML string for viewing this question element
        """
        html  = self.renderQuestion()
        html += '<span style="background-image:url(\'panel-amusements.png\');">'
        html += '\n<a onmousedown="Javascript:updateCoords(event);'
        html += 'showMe(\'%s\', 350, 100);" ' % self.hintId
        html += 'style="cursor:help;align:center;vertical-align:middle;" '
        html += 'title="Hint" \n'
        html += 'href="javascript:void(0);">&nbsp;&nbsp;&nbsp;&nbsp;</a></span>'
        html += '<div id="'+self.hintId+'" '
        html += 'style="display:none; z-index:99;">'
        html += '<div style="float:right;" >'
        html += '<img alt="%s" ' % _('Close')
        html += 'src="stock-stop.png" title="%s"' % _('Close')
        html += " onmousedown=\"Javascript:hideMe();\"/></div>"
        html += '<div class="popupDivLabel">'
        html += _("Hint")
        html += '</div>\n'
        html += self.question.hint
        html += "</div>\n"
        
        return html
    
    def renderQuestionPreview(self):
        #TODO merge renderQuestionView and renderQuestionPreview
        """
        Returns an XHTML string for previewing this question element
        """
        html  = self.renderQuestion()
        html += " &nbsp;&nbsp;\n"
        html += common.elementInstruc(self.hintId, self.question.hint, 
                                      "panel-amusements.png", "Hint")
        return html

    def renderQuestion(self):
        """
        Returns an XHTML string for viewing and previewing this question element
        """
        log.debug("renderPreview called")
    
        html  = u"<br/><br/><b>" +unicode(self.index + 1) + ". " 
        html += self.question.question + "</b><br/><br/>"
        html += _("True") + " " 
        html += self.__option(0, 2, "true") + "\n"
        html += _("False") + " " 
        html += self.__option(1, 2, "false") + "\n"
       
        return html
    
    def __option(self, index, length, true):
        """Add a option input"""
        html  = u'<input type="radio" name="option%s" ' % self.id
        html += u'id="%s%s" ' % (true, self.id)
        html += u'onclick="getFeedback(%d,%d,\'%s\',\'truefalse\')"/>' % (
                index, length, self.id)
        return html
    
    def renderFeedbackView(self):
        """
        return xhtml string for display this option's feedback
        """
        feedbackStr1 = _(u"Correct!") + " " + self.question.feedback
        feedbackStr2 = _(u"Incorrect!") + " " + self.question.feedback
        if not self.question.isCorrect:
            feedbackStr1, feedbackStr2 = feedbackStr2, feedbackStr1 
            
        feedbackId1 = "0" + "b" + self.id
        feedbackId2 = "1" + "b" + self.id
        html  = u'<div id="s%s" style="color: rgb(0, 51, 204);' % feedbackId1
        html += u'display: none;">' 
        html += feedbackStr1 + '</div>\n'
        html += u'<div id="s%s" style="color: rgb(0, 51, 204);' % feedbackId2
        html += u'display: none;">' 
        html += feedbackStr2 + '</div>\n'
        
        return html
        
    
# ===========================================================================
