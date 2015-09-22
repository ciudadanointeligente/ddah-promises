# -*- coding: utf-8 -*-
from promises.models import Promise, Category, VerificationDocument
from popolo.models import Identifier
import re
import copy
import types


class PromiseCreator():
    def __init__(self):
        self.category = None

    def get_category(self, category_name):
        self.category, created = Category.objects.get_or_create(name=category_name)
        return self.category

    def create_promise(self, promise_name, **kwargs):
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

    def create_verification_doc(self, name, url):
        verification_doc, created = VerificationDocument.objects.get_or_create(display_name=name)
        verification_doc.url = url
        verification_doc.promise = self.promise
        verification_doc.save()
        return verification_doc

    def create_tag(self, tag):
        self.promise.tags.add(tag)


def match_with(first_part, key):
    pattern = re.compile('_(?P<id>\d+)$')
    return first_part + str(pattern.search(key).group('id'))


HEADER_TYPES = {'id': {'what': 'promise_kwarg', 'as': 'identifier'},
                'category': {'what': 'promise_kwarg'},
                'promess': {'what': 'promise_kwarg', 'as': 'name'},
                'description': {'what': 'promise_kwarg'},
                'quality': {'what': 'promise_kwarg'},
                'fulfillment': {'what': 'promise_kwarg'},
                'ponderator': {'what': 'promise_kwarg'},
                'verification_doc_name_(?P<id>\d+)': {'what': 'verification_doc_kwarg',
                                                      'match': 'verification_doc_link_',
                                                      'use_this_as': 'name',
                                                      'use_other_as': 'url'
                                                      },
                'information_source_name_(?P<id>\d+)': {'what': 'information_source_kwarg',
                                                      'match': 'information_source_link_',
                                                      'use_this_as': 'name',
                                                      'use_other_as': 'url'
                                                      },
                'tag': {'what': 'create_tag_arg'},
}


class HeaderReader():
    def __init__(self, headers=None):
        self.headers = headers
        self.instructions = {}

        for column_number in range(len(self.headers)):
            key_and_instruction = self.what_to_do_with_column(column_number)
            if key_and_instruction is None:
                continue
            key, instruction = key_and_instruction
            if key not in self.instructions.keys():
                self.instructions[key] = {}
                setattr(self, key, self.instructions[key])
                def make_get_kwargs(k):
                    def f(self, row):
                        return self.get_kwargs_for(getattr(self, k), row)
                    return f
                setattr(self, "get_" + key + "s", types.MethodType(make_get_kwargs(key), self))
            self.instructions[key][column_number] = instruction

    def get_kwargs_for(self, dictionary, row):
        kwargs = {}
        for key in dictionary.keys():
            instruction = dictionary[key]
            if isinstance(dictionary[key], dict):
                kwargs[key] = {}
                kwargs[key][instruction['use_this_as']] = row[key]
                other_index = self.headers.index(instruction['match_with'])
                kwargs[key][instruction['use_other_as']] = row[other_index]
            else:
                kwargs[dictionary[key]] = row[key]
        return kwargs

    def what_to_do_with_column(self, column_number):
        for key in HEADER_TYPES.keys():
            pattern = re.compile(key)
            if pattern.search(self.headers[column_number]):
                instruction_alias = self.headers[column_number]
                instruction = instruction_alias
                raw_instructions = copy.copy(HEADER_TYPES[key])
                if 'as' in raw_instructions.keys():
                    instruction = raw_instructions['as']
                if 'match' in raw_instructions.keys():
                    the_match =  match_with(raw_instructions['match'], instruction_alias)
                    raw_instructions['match_with'] = the_match
                    instruction = raw_instructions
                return HEADER_TYPES[key]['what'], instruction

