# -*- coding: utf-8 -*-
from promises.models import Promise, Category, VerificationDocument, InformationSource
from popolo.models import Identifier


class PromiseCreator():
    def __init__(self):
        self.category = None

    def get_category(self, category_name):
        self.category, created = Category.objects.get_or_create(name=category_name)
        return self.category

    def filter_promise_kwargs(self, kwargs):
        for key in kwargs.keys():
            if key in ['fulfillment', 'ponderator', 'quality']:
                value = kwargs[key]
                value = value.replace('%','')
                value = value.replace(',','.')
                try:
                    value = float(value)
                except ValueError:
                    value = 0.0
                    print 'Problem parsing ', key, kwargs[key]
                kwargs[key] = value
        return kwargs

    def create_promise(self, promise_name=None, **kwargs):
        kwargs = self.filter_promise_kwargs(kwargs)
        if promise_name is None and 'name' in kwargs.keys():
            promise_name = kwargs['name']
        search_key = {
            'name': promise_name
        }
        if 'identifier' in kwargs:
            search_key = {
                'identifiers__identifier': kwargs['identifier']
            }
        if 'category' in kwargs:
            self.get_category(kwargs['category'])
            del kwargs['category']
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

    def create_verification_doc(self, name, url):
        verification_doc, created = VerificationDocument.objects.get_or_create(display_name=name)
        verification_doc.url = url
        verification_doc.promise = self.promise
        verification_doc.save()
        return verification_doc

    def create_information_source(self, name, url):
        information_source, created = InformationSource.objects.get_or_create(promise=self.promise, display_name=name)
        information_source.url = url
        information_source.save()
        return information_source

    def create_tag(self, tag):
        self.promise.tags.add(tag)
