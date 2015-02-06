from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class TaskView(BrowserView):

    template = ViewPageTemplateFile('task.pt')

    def __call__(self):
        return self.template()
