# -*- coding: utf-8 -*-
from promises.models import Promise, Category, VerificationDocument
from popolo.models import Identifier
import re


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

    def add_tag(self, tag):
        self.promise.tags.add(tag)


def match_with(first_part, key):
    pattern = re.compile('_(?P<id>\d+)$')
    return first_part + str(pattern.search(key).group('id'))


HEADER_TYPES = {'id': {'what': 'promise_kwarg', 'as': 'identifier'},
                'category': {'what': 'promise_kwarg'},
                'promess': {'what': 'promise_kwarg'},
                'description': {'what': 'promise_kwarg'},
                'quality': {'what': 'promise_kwarg'},
                'fulfillment': {'what': 'promise_kwarg'},
                'ponderator': {'what': 'promise_kwarg'},
                'verification_doc_name_(?P<id>\d+)': {'what': 'create_verification_doc',
                                                      'match': 'verification_doc_link_',
                                                      'use_this_as': 'name',
                                                      'use_other_as': 'url'
                                                      },
                'verification_doc_link_(?P<id>\d+)': {'what': 'promise_kwarg'},
                'information_source_name_(?P<id>\d+)': {'what': 'promise_kwarg'},
                'information_source_link_(?P<id>\d+)': {'what': 'promise_kwarg'},
                'tag': {'what': 'promise_kwarg'},
}


class HeaderReader():
    def __init__(self, headers=None):
        self.headers = headers
        self.instructions = {}

    def what_to_do_with_column(self, column_number):
        for key in HEADER_TYPES.keys():
            pattern = re.compile(key)
            if pattern.search(self.headers[column_number]):
                instruction_alias = self.headers[column_number]
                instruction = instruction_alias
                raw_instructions = HEADER_TYPES[key]
                if 'as' in raw_instructions.keys():
                    instruction = raw_instructions['as']
                if 'match' in raw_instructions.keys():
                    raw_instructions['match_with'] = match_with(raw_instructions['match'], instruction_alias)
                    instruction = raw_instructions
                return HEADER_TYPES[key]['what'], instruction

