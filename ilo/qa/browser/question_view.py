from five import grok
from plone.directives import dexterity, form
from ilo.qa.content.question import IQuestion
from Products.CMFCore.utils import getToolByName
from HTMLParser import HTMLParser
from plone import api

grok.templatedir('templates')

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


class Index(dexterity.DisplayForm):
    grok.context(IQuestion)
    grok.require('zope2.View')
    grok.template('question_view')
    grok.name('view')

    @property
    def catalog(self):
    	return getToolByName(self.context, 'portal_catalog')

    def contents(self):
    	context = self.context
    	catalog = self.catalog
    	path = '/'.join(context.getPhysicalPath())
    	brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.qa.answer',review_state='internally_published',sort_on='Date',sort_order='reverse')
    	return brains
    
    def strip_tags(self, html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()
    
    # def show_add_answer(self, ):
    #     context = self.context
    #     # import pdb; pdb.set_trace()
    #     return context.portal_membership.getAuthenticatedMember().has_role('Site Administrator', 'Manager') or context.portal_membership.getAuthenticatedMember().has_role('Editor', 'Reviewer')
    # 

    def show_add_answer(self):
        current = api.user.get_current()
        roles = api.user.get_roles(username=str(current))
        return any((True for x in roles if x in ['Reviewer', 'Administrator', 'Manager','Site Administrator'] ))
