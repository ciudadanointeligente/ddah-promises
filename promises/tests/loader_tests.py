# -*- coding: utf-8 -*-
from django.test import TestCase
from promises.csv_loader import HeaderReader, PromiseCreator, match_with, RowProcessor, CsvProcessor
from promises.models import Promise, Category, VerificationDocument, InformationSource
from popolo.models import Identifier
import types
from django.core.management import call_command
import os
import codecs
from django.utils import timezone
from datetime import timedelta


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

        self.rows = [self.headers, self.row]


class CSVCommandTestCase(CSVLoaderTestCaseBase):
    def setUp(self):
        super(CSVCommandTestCase, self).setUp()
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.csv_file = os.path.join(current_dir, 'fixtures', 'example_data.csv')

    def test_csv_processor(self):
        file_ = codecs.open(self.csv_file)
        processor = CsvProcessor(file_)
        processor.work()
        self.assertTrue(Promise.objects.all())
        self.assertTrue(Category.objects.all())
        self.assertTrue(VerificationDocument.objects.all())
        self.assertTrue(InformationSource.objects.all())
        self.assertTrue(processor.warnings)
        self.assertIn('Exigir que en ciertas unidades relevantes', processor.warnings[0])
        self.assertIn('Problem parsing ponderator', processor.warnings[0])
        # Using extra params
        file_ = codecs.open(self.csv_file)
        yesterday = timezone.now() - timedelta(days=1)
        processor = CsvProcessor(file_, date=yesterday)
        processor.work()
        promise = Promise.objects.first()
        self.assertEquals(promise.date.day, yesterday.day)


    def test_call_command(self):
        call_command('csv_promises_importer', self.csv_file)
        self.assertTrue(Promise.objects.all())
        self.assertTrue(Category.objects.all())
        self.assertTrue(VerificationDocument.objects.all())
        self.assertTrue(InformationSource.objects.all())


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

    def test_get_the_creation_order(self):
        reader = HeaderReader(headers=self.headers)
        order = reader.get_creation_instructions()
        self.assertEquals(order[0], {'creation_method': 'create_promise',
                                     'kwargs_getter': 'get_promise_kwargs',
                                     'multiple': False})
        self.assertEquals(order[1], {'creation_method': 'create_verification_doc',
                                     'kwargs_getter': 'get_verification_doc_kwargs',
                                     'multiple': True})
        self.assertEquals(order[2], {'creation_method': 'create_information_source',
                                     'kwargs_getter': 'get_information_source_kwargs',
                                     'multiple': True})

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

    def test_create_promise_and_category(self):
        creator = PromiseCreator()
        creator.create_promise(name=self.row[2], category=self.row[1])
        category = Category.objects.get()
        self.assertEquals(category.name, self.row[1])


    def test_create_information_source(self):
        creator = PromiseCreator()
        promise = creator.create_promise("the new version of the promise",
                                         identifier="i1")
        information_source = creator.create_information_source(name="the_name",
                                                               url='http://ciudadanoi.org')
        self.assertIsInstance(information_source, InformationSource)
        self.assertEquals(information_source.promise, promise)


    def test_promise_filter_kwargs(self):
        creator = PromiseCreator()
        kwargs = {'category': u'Probidad y fortalecimiento de Municipios',
                  'name': u'Plan gradual de capacitaci\xf3n y profesionalizaci\xf3n del pa de la ADP.',
                  'fulfillment': u'0%',
                  'ponderator': u'0,040%',
                  'identifier': u'1',
                  'quality': u'0,0',
                  'description': u''}

        new_kwargs = creator.filter_promise_kwargs(kwargs)
        self.assertEquals(new_kwargs['category'], kwargs['category'])
        self.assertEquals(new_kwargs['name'], kwargs['name'])
        self.assertEquals(new_kwargs['identifier'], kwargs['identifier'])
        self.assertEquals(new_kwargs['ponderator'], 0.04)
        self.assertEquals(new_kwargs['fulfillment'], 0)
        self.assertEquals(new_kwargs['quality'], 0.0)
        self.assertEquals(new_kwargs['description'], kwargs['description'])

    def test_create_promise(self):
        creator = PromiseCreator()
        creator.get_category(self.row[1])
        promise = creator.create_promise(self.row[2])
        self.assertIsInstance(promise, Promise)
        self.assertEquals(promise.name, self.row[2])
        self.assertEquals(promise, creator.promise)
        self.assertEquals(promise.category, creator.category)
        Promise.objects.all().delete()
        promise = creator.create_promise(name=self.row[2])
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

class FakeProcessor():
    def __init__(self):
        self.instructions = []
        self.warnings = []


    def __getattr__(self, name):
        dicti = {}
        dicti['name'] = name
        dicti['kwargs'] = None
        dicti['args'] = None
        dicti['called'] = False
        self.instructions.append(dicti)
        def make_method(n):
            def f(self, *args, **kwargs):
                counter = 0
                for i in self.instructions:
                    if i['name'] == n:
                        self.instructions[counter]['kwargs'] = kwargs
                        self.instructions[counter]['args'] = args
                        self.instructions[counter]['called'] = True
                    counter += 1
            return f
        the_method = types.MethodType(make_method(name), self)
        setattr(self, name, the_method)
        return the_method

        '''
        ### This
        p = FakeProcessor()
        p.create_promise(perrito="fiera")
        print p.instructions
        ### Will print
        {'create_promise': {'args': (), 'kwargs': {'perrito': 'fiera'}}}
        '''

class RowProcessorTestCase(CSVLoaderTestCaseBase):
    def test_given_a_row_it_processes_using_the_header_reader(self):
        processor = RowProcessor(self.rows)
        self.assertEquals(processor.header_reader.headers, self.headers)
        self.assertEquals(processor.rows[0], self.row)

    def test_fake_processor(self):
        p = FakeProcessor()
        p.create_promise(perrito="fiera")
        instructions = p.instructions
        self.assertEquals('create_promise', instructions[0]['name'])
        self.assertTrue(instructions[0]['called'])
        self.assertEquals({'perrito': 'fiera'}, instructions[0]['kwargs'])

    def test_the_order_in_which_the_creation_is_performed(self):
        processor = RowProcessor(self.rows, creator_class=FakeProcessor)
        processor.read_row(self.rows[1])
        i = processor.creator.instructions
        self.assertEquals(i[0]['name'], 'create_promise')
        self.assertTrue(i[0]['called'])
        self.assertEquals(i[1]['name'], 'create_verification_doc')
        self.assertTrue(i[1]['called'])
        self.assertEquals(i[2]['name'], 'create_information_source')
        self.assertTrue(i[2]['called'])

    def test_read_rows(self):
        processor = RowProcessor(self.rows, creator_class=FakeProcessor)
        processor.process()
        i = processor.creator.instructions
        self.assertEquals(i[0]['name'], 'create_promise')
        self.assertTrue(i[0]['called'])
        self.assertEquals(i[1]['name'], 'create_verification_doc')
        self.assertTrue(i[1]['called'])
        self.assertEquals(i[2]['name'], 'create_information_source')
        self.assertTrue(i[2]['called'])

    def test_original_creator(self):
        processor = RowProcessor(self.rows)
        processor.process()
        self.assertTrue(Promise.objects.all())
        self.assertTrue(VerificationDocument.objects.all())
        self.assertTrue(InformationSource.objects.all())


