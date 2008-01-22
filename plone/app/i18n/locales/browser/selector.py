from zope.interface import implements
from zope.viewlet.interfaces import IViewlet

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile


class LanguageSelector(BrowserView):
    """Language selector.

      >>> ls = LanguageSelector(None, dict(), None, None)
      >>> ls
      <plone.app.i18n.locales.browser.selector.LanguageSelector object at ...>

      >>> ls.update()
      >>> ls.available()
      False
      >>> ls.languages()
      []
      >>> ls.showFlags()
      False

      >>> class Tool(object):
      ...     use_cookie_negotiation = True
      ...
      ...     def showFlags(self):
      ...         return True
      ...
      ...     def getAvailableLanguageInformation(self):
      ...         return dict(en={'selected' : True}, de={'selected' : False})

      >>> ls.tool = Tool()
      >>> ls.available()
      True
      >>> ls.languages()
      [{'code': 'en', 'selected': True}]
      >>> ls.showFlags()
      True

      >>> class Dummy(object):
      ...     def getPortalObject(self):
      ...         return self
      ...
      ...     def absolute_url(self):
      ...         return 'absolute url'

      >>> context = Dummy()
      >>> context.portal_url = Dummy()
      >>> ls = LanguageSelector(context, dict(), None, None)
      >>> ls.portal_url
      'absolute url'
    """
    implements(IViewlet)

    render = ZopeTwoPageTemplateFile('languageselector.pt')

    def __init__(self, context, request, view, manager):
        super(LanguageSelector, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.tool = getToolByName(context, 'portal_languages', None)
        portal_tool = getToolByName(context, 'portal_url', None)
        self.portal_url = None
        if portal_tool is not None:
            self.portal_url = portal_tool.getPortalObject().absolute_url()

    def update(self):
        pass

    def available(self):
        if self.tool is not None and self.tool.use_cookie_negotiation:
            return True
        return False

    def languages(self):
        """Returns list of languages."""
        if self.tool is None:
            return []

        def merge(lang, info):
            info["code"]=lang
            return info

        return [merge(lang, info) for (lang,info) in
                    self.tool.getAvailableLanguageInformation().items()
                    if info["selected"]]

    def showFlags(self):
        """Do we use flags?."""
        if self.tool is not None:
            return self.tool.showFlags()
        return False
