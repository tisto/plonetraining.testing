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
