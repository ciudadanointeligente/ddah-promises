# -*- coding: utf-8 -*-
from promises.models import Promise, Category, VerificationDocument
from popolo.models import Identifier


class PromiseCreator():
    def __init__(self):
        self.category = None

    def get_category(self, category_name):
        self.category, created = Category.objects.get_or_create(name=category_name)
        return self.category

    def get_promise(self, promise_name, **kwargs):
        search_key = {
            'name': promise_name
        }
        if 'identifier' in kwargs:
            search_key = {
                'identifiers__identifier': kwargs['identifier']
            }
        self.promise, created = Promise.objects.get_or_create(**search_key)
        for key, value in kwargs.items():
            if key == 'fulfillment':
                self.promise.fulfillment.percentage = value
                self.promise.fulfillment.save()
                continue
            if key == 'identifier' and created:
                i = Identifier(identifier=value)
                self.promise.identifiers.add(i)
                continue
            setattr(self.promise, key, value)
        self.promise.category = self.category
        self.promise.save()
        return self.promise

    def get_verification_doc(self, name, url):
        verification_doc, created = VerificationDocument.objects.get_or_create(display_name=name)
        verification_doc.url = url
        verification_doc.promise = self.promise
        verification_doc.save()
        return verification_doc


class HeaderReader():
    def __init__(self, headers=None):
        self.headers = headers
