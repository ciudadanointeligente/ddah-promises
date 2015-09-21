# -*- coding: utf-8 -*-
from django.test import TestCase
from promises.csv_loader import HeaderReader, PromiseCreator, match_with
from promises.models import Promise, Category, VerificationDocument
from popolo.models import Identifier


class CSVLoaderTestCaseBase(TestCase):
    def setUp(self):
        self.headers = ['id',
                        'category',
                        'promess',
                        'description',
                        'quality',
                        'fulfillment',
                        'ponderator',
                        'verification_doc_name_1',
                        'verification_doc_link_1',
                        'information_source_name_1',
                        'information_source_link_1',
                        'tag',
                        'tag']
        self.row = ['1',  # Identifier
                    'Probidad y fortalecimiento de Municipios',  # category
                    'Plan gradual de capacitación y profesionalización del personal y seleccionar profesionales en unidades clave con asesoría de la ADP.',  # promise
                    '',  # description
                    '7,0',  # quality
                    '10',  # fulfillment
                    '0.040',  # ponderator
                    '',  # verification_doc_name_1
                    '',  # verification_doc_link_1
                    '',  # information_source_name_1
                    '',  # information_source_link_1
                    '',  # tag
                    '',  # tag
                    ]


class HeaderReaderTestCase(CSVLoaderTestCaseBase):
    def test_instanciate_header_reader(self):
        '''I can instanciate a header reader'''
        reader = HeaderReader(headers=self.headers)
        self.assertTrue(hasattr(reader, 'instructions'))
        self.assertIsInstance(reader.instructions, dict)
        key, instruction = reader.what_to_do_with_column(0)
        self.assertEquals(key, 'create_promise_kwarg')
        self.assertEquals(instruction, 'identifier')
        #  Create category
        key, instruction = reader.what_to_do_with_column(1)
        self.assertEquals(key, 'create_promise_kwarg')
        self.assertEquals(instruction, 'category')
        #  Create category
        key, instruction = reader.what_to_do_with_column(2)
        self.assertEquals(key, 'create_promise_kwarg')
        self.assertEquals(instruction, 'promess')
        #  Description
        key, instruction = reader.what_to_do_with_column(3)
        self.assertEquals(key, 'create_promise_kwarg')
        self.assertEquals(instruction, 'description')
        #  Quality
        key, instruction = reader.what_to_do_with_column(5)
        self.assertEquals(key, 'create_promise_kwarg')
        self.assertEquals(instruction, 'fulfillment')
        #  Fulfillment
        key, instruction = reader.what_to_do_with_column(6)
        self.assertEquals(key, 'create_promise_kwarg')
        self.assertEquals(instruction, 'ponderator')
        # Verification doc
        key, instruction = reader.what_to_do_with_column(7)
        self.assertEquals(key, 'create_verification_doc_kwarg')

        self.assertEquals(instruction['match_with'], 'verification_doc_link_1')
        self.assertEquals(instruction['use_other_as'], 'url')
        self.assertEquals(instruction['use_this_as'], 'name')

    def test_match_with_method(self):
        key = 'verification_doc_1'
        result = match_with('verification_doc_link_', key)
        self.assertEquals(result, 'verification_doc_link_1')


class PromiseCreatorTestCase(CSVLoaderTestCaseBase):
    def test_create_category(self):
        creator = PromiseCreator()
        category = creator.get_category(self.row[1])

        self.assertIsInstance(category, Category)
        self.assertEquals(category.name, self.row[1])

        self.assertIsInstance(creator.category, Category)
        self.assertEquals(creator.category.name, self.row[1])

    def test_create_promise(self):
        creator = PromiseCreator()
        creator.get_category(self.row[1])
        promise = creator.get_promise(self.row[2])
        self.assertIsInstance(promise, Promise)
        self.assertEquals(promise.name, self.row[2])
        self.assertEquals(promise, creator.promise)
        self.assertEquals(promise.category, creator.category)

        # Without category
        creator = PromiseCreator()
        promise = creator.get_promise(self.row[2])
        self.assertIsNone(promise.category)

        # With description
        creator = PromiseCreator()
        promise = creator.get_promise(self.row[2], description=u"la fiera es la mejor")
        self.assertEquals(promise.description, u"la fiera es la mejor")

        # With category and description
        creator = PromiseCreator()
        creator.get_category(self.row[1])
        promise = creator.get_promise(self.row[2], description=u"la fiera es la mejor")
        self.assertEquals(promise.category, creator.category)
        self.assertEquals(promise.description, u"la fiera es la mejor")

        # working with kwargs
        creator = PromiseCreator()
        promise = creator.get_promise(self.row[2],
                                      description=u"la fiera es la mejor",
                                      quality=self.row[4],
                                      fulfillment=self.row[5],
                                      ponderator=self.row[6],
                                      identifier=self.row[0])
        promise = Promise.objects.get(id=promise.id)
        self.assertEquals(promise.ponderator, 0.04)
        self.assertEquals(promise.fulfillment.percentage, 10)
        self.assertTrue(promise.identifiers.filter(identifier=self.row[0]))

    def test_get_promise_by_identifier_not_by_name(self):
        p = Promise.objects.create(name="This is a promise")
        i = Identifier.objects.create(identifier="i1")
        p.identifiers.add(i)

        creator = PromiseCreator()
        promise = creator.get_promise("the new version of the promise",
                                      identifier="i1")

        self.assertEquals(p, promise)

    def test_create_verification_document(self):
        creator = PromiseCreator()
        promise = creator.get_promise("the new version of the promise",
                                      identifier="i1")
        verification_doc = creator.get_verification_doc(name="the_name",
                                                        url='http://ciudadanoi.org')
        self.assertIsInstance(verification_doc, VerificationDocument)
        self.assertEquals(verification_doc.promise, promise)

    def test_create_a_tag(self):
        creator = PromiseCreator()
        creator.get_promise("the new version of the promise")
        creator.add_tag("perro")
        self.assertTrue(creator.promise.tags.all())

