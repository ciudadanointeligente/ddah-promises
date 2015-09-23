# -*- coding: utf-8 -*-
from promises.models import Promise, Category, VerificationDocument, InformationSource
from popolo.models import Identifier


class PromiseCreator():
    def __init__(self,
                 category_qs=Category.objects.all(),
                 promise_qs=Promise.objects.all(),
                 verification_doc_qs = VerificationDocument.objects.all(),
                 information_source_qs = InformationSource.objects.all(),
                 **kwargs):
        self.category = None
        self.kwargs = kwargs
        self.category_qs = category_qs
        self.promise_qs = promise_qs
        self.verification_doc_qs = verification_doc_qs
        self.information_source_qs = information_source_qs
        self.warnings = []

    def get_category(self, category_name):
        self.category, created = self.category_qs.get_or_create(name=category_name)
        return self.category

    def filter_promise_kwargs(self, kwargs):
        kwargs.update(self.kwargs)
        for key in kwargs.keys():
            if key in ['fulfillment', 'ponderator', 'quality']:
                value = kwargs[key]
                value = value.replace('%','')
                value = value.replace(',','.')
                try:
                    value = float(value)
                except ValueError:
                    value = 0.0
                    self.warnings.append('Problem parsing %s at %s with value %s' % (key, kwargs['name'], kwargs[key]))
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
        self.promise, created = self.promise_qs.get_or_create(**search_key)
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
        verification_doc, created = self.verification_doc_qs.get_or_create(display_name=name)
        verification_doc.url = url
        verification_doc.promise = self.promise
        verification_doc.save()
        return verification_doc

    def create_information_source(self, name, url):
        information_source, created = self.information_source_qs.get_or_create(promise=self.promise, display_name=name)
        information_source.url = url
        information_source.save()
        return information_source

    def create_tag(self, tag):
        self.promise.tags.add(tag)
