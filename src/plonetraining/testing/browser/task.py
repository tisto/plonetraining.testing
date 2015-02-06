from zope.site.hooks import getSite
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import json


class TaskView(BrowserView):

    template = ViewPageTemplateFile('task.pt')

    def __call__(self):
        return self.template()


class TaskViewWithParams(BrowserView):

    template = ViewPageTemplateFile('task.pt')

    def __call__(self):
        self.term = self.request.get('term')
        return self.template()


class TaskViewWithBrowserLayer(BrowserView):

    template = ViewPageTemplateFile('task.pt')

    def __call__(self):
        return self.template()


class TaskViewJson(BrowserView):

    def __call__(self):
        self.request.response.setHeader(
            'Content-Type',
            'application/json; charset=utf-8'
        )
        result = {
            'title': self.context.title,
            'description': self.context.description,
        }
        return json.dumps(result, indent=2, sort_keys=True)


class TaskViewXml(BrowserView):

    def __call__(self):
        self.request.response.setHeader(
            'Content-Type',
            'application/xml; charset=utf-8'
        )
        from lxml import etree
        root = etree.Element('task')
        title = etree.Element('title')
        title.text = self.context.title
        root.append(title)
        description = etree.Element('description')
        description.text = self.context.description
        root.append(etree.Element('description'))
        return etree.tostring(root)


class TaskViewRedirect(BrowserView):

    def __call__(self):
        portal = getSite()
        return self.request.response.redirect(portal.absolute_url())
