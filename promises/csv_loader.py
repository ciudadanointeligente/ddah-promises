# -*- coding: utf-8 -*-
from promises.models import Promise, Category
from popolo.models import Identifier


class PromiseCreator():
    def __init__(self):
        self.category = None

    def get_category(self, category_name):
        self.category, created = Category.objects.get_or_create(name=category_name)
        return self.category

    def get_promise(self, promise_name, **kwargs):
        self.promise, created = Promise.objects.get_or_create(name=promise_name)
        for key, value in kwargs.items():
            if key == 'fulfillment':
                self.promise.fulfillment.percentage = value
                self.promise.fulfillment.save()
                continue
            if key == 'identifier':
                i = Identifier(identifier=value)
                self.promise.identifiers.add(i)
                continue
            setattr(self.promise, key, value)
        self.promise.category = self.category
        self.promise.save()
        return self.promise


class HeaderReader():
    def __init__(self, headers=None):
        self.headers = headers
