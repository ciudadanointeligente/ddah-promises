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
                        'tag',
                        'verification_doc_name_2',
                        'verification_doc_link_2',
                        ]
        self.row = ['1',  # Identifier
                    'Probidad y fortalecimiento de Municipios',  # category
                    'Plan gradual de capacitación y profesionalización del personal y seleccionar profesionales en unidades clave con asesoría de la ADP.',  # promise
                    '',  # description
                    '7,0',  # quality
                    '10',  # fulfillment
                    '0.040',  # ponderator
                    'vf_name',  # verification_doc_name_1
                    'http://verification.doc',  # verification_doc_link_1
                    'is_name',  # information_source_name_1
                    'http://information.source',  # information_source_link_1
                    '',  # tag
                    '',  # tag
                    'vf_name2',  # verification_doc_name_2
                    'http://verification.doc2',  # verification_doc_link_2
                    ]


class HeaderReaderTestCase(CSVLoaderTestCaseBase):
    def test_instanciate_header_reader(self):
        '''I can instanciate a header reader'''
        reader = HeaderReader(headers=self.headers)
        self.assertTrue(hasattr(reader, 'instructions'))
        self.assertIsInstance(reader.instructions, dict)
        key, instruction = reader.what_to_do_with_column(0)
        self.assertEquals(key, 'promise_kwarg')
        self.assertEquals(instruction, 'identifier')
        #  Create category
        key, instruction = reader.what_to_do_with_column(1)
        self.assertEquals(key, 'promise_kwarg')
        self.assertEquals(instruction, 'category')
        #  Create category
        key, instruction = reader.what_to_do_with_column(2)
        self.assertEquals(key, 'promise_kwarg')
        self.assertEquals(instruction, 'name')
        #  Description
        key, instruction = reader.what_to_do_with_column(3)
        self.assertEquals(key, 'promise_kwarg')
        self.assertEquals(instruction, 'description')
        #  Quality
        key, instruction = reader.what_to_do_with_column(5)
        self.assertEquals(key, 'promise_kwarg')
        self.assertEquals(instruction, 'fulfillment')
        #  Fulfillment
        key, instruction = reader.what_to_do_with_column(6)
        self.assertEquals(key, 'promise_kwarg')
        self.assertEquals(instruction, 'ponderator')
        # Verification doc
        key, instruction = reader.what_to_do_with_column(7)
        self.assertEquals(key, 'verification_doc_kwarg')

        self.assertIsNone(reader.what_to_do_with_column(8))

        self.assertEquals(instruction['match_with'], 'verification_doc_link_1')
        self.assertEquals(instruction['use_other_as'], 'url')
        self.assertEquals(instruction['use_this_as'], 'name')
        # Verification doc 2
        key, instruction = reader.what_to_do_with_column(13)
        self.assertEquals(key, 'verification_doc_kwarg')

        self.assertIsNone(reader.what_to_do_with_column(14))

        self.assertEquals(instruction['match_with'], 'verification_doc_link_2')
        self.assertEquals(instruction['use_other_as'], 'url')
        # Information source
        key, instruction = reader.what_to_do_with_column(9)
        self.assertEquals(key, 'information_source_kwarg')

        self.assertEquals(instruction['match_with'], 'information_source_link_1')
        self.assertEquals(instruction['use_other_as'], 'url')
        self.assertEquals(instruction['use_this_as'], 'name')
        #  Tags
        key, instruction = reader.what_to_do_with_column(11)
        self.assertEquals(key, 'create_tag_arg')
        self.assertEquals(instruction, 'tag')

    def test_get_what_columns_to_read_to_get_promise_creation_kwargs(self):
        reader = HeaderReader(headers=self.headers)

        columns = reader.promise_kwarg

        self.assertEquals(columns[0],'identifier')
        self.assertIn(7, reader.verification_doc_kwarg.keys())

    def test_get_creation_kwargs(self):
        reader = HeaderReader(headers=self.headers)
        kwargs = reader.get_promise_kwargs(self.row)
        self.assertEquals(kwargs['identifier'], '1')
        self.assertEquals(kwargs['category'], 'Probidad y fortalecimiento de Municipios')
        self.assertEquals(kwargs['name'],'Plan gradual de capacitación y profesionalización del personal y seleccionar profesionales en unidades clave con asesoría de la ADP.') # description
        self.assertEquals(kwargs['quality'], '7,0')  # quality
        self.assertEquals(kwargs['fulfillment'], '10')  # fulfillment
        self.assertEquals(kwargs['ponderator'], '0.040')  # ponderator

        kwargs = reader.get_information_source_kwargs(self.row)
        self.assertEquals(kwargs[9]['name'], 'is_name')  # information_source_name_1
        self.assertEquals(kwargs[9]['url'], 'http://information.source')  # information_source_link_1

        kwargs = reader.get_verification_doc_kwargs(self.row)
        self.assertEquals(2, len(kwargs))
        first_kwargs = kwargs[7]
        self.assertEquals(first_kwargs['name'], 'vf_name')  # verification_doc_name_1
        self.assertEquals(first_kwargs['url'], 'http://verification.doc')  # verification_doc_link_1
        second_kwargs = kwargs[13]
        self.assertEquals(second_kwargs['name'], 'vf_name2')  # verification_doc_name_1
        self.assertEquals(second_kwargs['url'], 'http://verification.doc2')  # verification_doc_link_1

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
        promise = creator.create_promise(self.row[2])
        self.assertIsInstance(promise, Promise)
        self.assertEquals(promise.name, self.row[2])
        self.assertEquals(promise, creator.promise)
        self.assertEquals(promise.category, creator.category)

        # Without category
        creator = PromiseCreator()
        promise = creator.create_promise(self.row[2])
        self.assertIsNone(promise.category)

        # With description
        creator = PromiseCreator()
        promise = creator.create_promise(self.row[2], description=u"la fiera es la mejor")
        self.assertEquals(promise.description, u"la fiera es la mejor")

        # With category and description
        creator = PromiseCreator()
        creator.get_category(self.row[1])
        promise = creator.create_promise(self.row[2], description=u"la fiera es la mejor")
        self.assertEquals(promise.category, creator.category)
        self.assertEquals(promise.description, u"la fiera es la mejor")

        # working with kwargs
        creator = PromiseCreator()
        promise = creator.create_promise(self.row[2],
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
        promise = creator.create_promise("the new version of the promise",
                                         identifier="i1")

        self.assertEquals(p, promise)

    def test_create_verification_document(self):
        creator = PromiseCreator()
        promise = creator.create_promise("the new version of the promise",
                                         identifier="i1")
        verification_doc = creator.create_verification_doc(name="the_name",
                                                        url='http://ciudadanoi.org')
        self.assertIsInstance(verification_doc, VerificationDocument)
        self.assertEquals(verification_doc.promise, promise)

    def test_create_a_tag(self):
        creator = PromiseCreator()
        creator.create_promise("the new version of the promise")
        creator.create_tag("perro")
        self.assertTrue(creator.promise.tags.all())

