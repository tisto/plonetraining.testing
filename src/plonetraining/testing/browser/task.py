from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


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
