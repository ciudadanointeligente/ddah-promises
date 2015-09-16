# -*- coding: utf-8 -*-
from django.test import TestCase
from promises.csv_loader import HeaderReader, PromiseFactory


class HeaderReaderTestCase(TestCase):
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
                        'information_source_name_1',
                        'tag',
                        'tag']
        self.row = ['1',
                    'Probidad y fortalecimiento de Municipios',
                    'Plan gradual de capacitación y profesionalización del \
                    personal y seleccionar profesionales en unidades clave \
                    con asesoría de la ADP.',
                    '',
                    '0,0',
                    '0%',
                    '0,040%',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ]

    def test_promise_factory(self):
        self.fail()

    def test_instanciate_header_reader(self):
        '''I can instanciate a header reader'''
        reader = HeaderReader(columns=self.columns)
        self.assertTrue(reader)


