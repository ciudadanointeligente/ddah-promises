# -*- coding: utf-8 -*-
from django.test import TestCase
from promises.csv_loader import HeaderReader, PromiseCreator
from promises.models import Promise, Category, VerificationDocument
from popolo.models import Identifier
from unittest import skip


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
        self.assertTrue(reader)


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

    @skip("Promises don't yet have tags")
    def test_create_a_tag(self):
        creator = PromiseCreator()
        creator.get_promise("the new version of the promise")

