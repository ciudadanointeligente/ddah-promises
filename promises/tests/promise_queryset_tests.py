from django.test import TestCase
import unittest
from django.utils.timezone import now
from ..models import Promise, Category
from ..queryset import PromiseSummary
from popolo.models import Person

nownow = now()


class PromiseQuerysetTestCase(TestCase):
    def setUp(self):
        self.person = Person.objects.create(name=u"A person")
        self.category = Category.objects.create(name="Education")

    def test_there_is_a_promise_summary_class(self):
        '''Instanciate a promise summary class'''
        summary = PromiseSummary()

        self.assertTrue(hasattr(summary, 'accomplished'))
        self.assertTrue(hasattr(summary, 'in_progress'))
        self.assertTrue(hasattr(summary, 'no_progress'))
        self.assertTrue(hasattr(summary, 'total_progress'))
        self.assertEquals(summary.accomplished, 0)
        self.assertEquals(summary.in_progress, 0)
        self.assertEquals(summary.no_progress, 0)
        self.assertEquals(summary.total_progress, 0)

    def test_instanciate_with_data(self):
        summary = PromiseSummary(accomplished=1,
                                 in_progress=2,
                                 no_progress=3,
                                 total_progress=4
                                 )

        self.assertEquals(summary.accomplished, 1)
        self.assertEquals(summary.in_progress, 2)
        self.assertEquals(summary.no_progress, 3)
        self.assertEquals(summary.total_progress, 4)

    def test_promise_queryset_with_summary(self):
        '''A promise queryset has a summary'''
        # this promise has 0 fulfillment
        Promise.objects.create(name="this is a promise 1",
                               category=self.category,
                               person=self.person
                               )
        # promises half accomplished
        promise_2 = Promise.objects.create(name="this is a promise 2",
                                           category=self.category,
                                           person=self.person
                                           )
        promise_2.fulfillment.percentage = 50
        promise_2.fulfillment.save()
        promise_4 = Promise.objects.create(name="this is a promise 4",
                                           category=self.category,
                                           person=self.person
                                           )
        promise_4.fulfillment.percentage = 1
        promise_4.fulfillment.save()
        promise_5 = Promise.objects.create(name="this is a promise 5",
                                           category=self.category,
                                           person=self.person
                                           )
        promise_5.fulfillment.percentage = 99
        promise_5.fulfillment.save()
        # fully acoomplished promises
        promise_3 = Promise.objects.create(name="this is a promise 3",
                                           category=self.category,
                                           person=self.person
                                           )
        promise_3.fulfillment.percentage = 100
        promise_3.fulfillment.save()
        promise_6 = Promise.objects.create(name="this is a promise 6",
                                           category=self.category,
                                           person=self.person
                                           )
        promise_6.fulfillment.percentage = 100
        promise_6.fulfillment.save()

        queryset = Promise.objects.all()
        summary = queryset.summary()
        self.assertIsInstance(summary, PromiseSummary)
        self.assertEquals(summary.accomplished, 2)
        self.assertEquals(summary.in_progress, 3)
        self.assertEquals(summary.in_progress, 3)
        self.assertEquals(summary.no_progress, 1)
        self.assertEquals(summary.total, 6)
        self.assertEquals(summary.accomplished_percentage,
                          (float(1)/float(3))*100)
        self.assertEquals(summary.in_progress_percentage, float(50))
        self.assertEquals(summary.no_progress_percentage,
                          (float(1)/float(6))*100)
        expected_total_progress = (float(0 + 50 + 100 + 1 + 99 + 100)/float(6))
        self.assertAlmostEquals(summary.total_progress, expected_total_progress)
        for p in Promise.objects.all():
            p.ponderator = 0.16
            p.save()
        queryset = Promise.objects.all()
        summary = queryset.summary()

    def test_summary_with_empty_data(self):
        '''Summary calculates correctly the percentage even
        if there are no promises'''
        summary = PromiseSummary()
        self.assertEquals(summary.total, 0)
        self.assertEquals(summary.accomplished_percentage, float(0))
        self.assertEquals(summary.in_progress_percentage, float(0))
        self.assertEquals(summary.no_progress_percentage, float(0))
        self.assertEquals(summary.total_progress, float(0))

    def test_queryset_ordered(self):

        promise_1 = Promise.objects.create(name="this is a promise 1",
                                           category=self.category,
                                           person=self.person
                                           )
        # promises half accomplished
        promise_2 = Promise.objects.create(name="this is a promise 2",
                                           category=self.category,
                                           person=self.person
                                           )
        promise_2.fulfillment.percentage = 50
        promise_2.fulfillment.save()
        promise_4 = Promise.objects.create(name="this is a promise 4",
                                           category=self.category,
                                           person=self.person
                                           )
        promise_4.fulfillment.percentage = 1
        promise_4.fulfillment.save()
        promise_5 = Promise.objects.create(name="this is a promise 5",
                                           category=self.category,
                                           person=self.person
                                           )
        promise_5.fulfillment.percentage = 99
        promise_5.fulfillment.save()
        # fully acoomplished promises
        promise_3 = Promise.objects.create(name="this is a promise 3",
                                           category=self.category,
                                           person=self.person
                                           )
        promise_3.fulfillment.percentage = 100
        promise_3.fulfillment.save()

        promises = Promise.objects.all()
        self.assertEquals(promises[0], promise_3)
        self.assertEquals(promises[1], promise_5)
        self.assertEquals(promises[2], promise_2)
        self.assertEquals(promises[3], promise_4)
        self.assertEquals(promises[4], promise_1)

    def test_promises_queryset_with_index(self):
        '''Every promise has an index annotated
        promise  | ponderator | fulfilment | index
        -------------------------------------------
        promise2 |    0.3     |    50      |  15.0
        promise3 |    0.1     |   100      |  10.0
        promise5 |    0.1     |    99      |  9.9
        promise4 |    0.1     |     1      |  0.1
        promise1 |    0.1     |     0      |  0.0
        '''
        promise_1 = Promise.objects.create(name="this is a promise 1",
                                           category=self.category,
                                           ponderator=0.1
                                           )
        # promises half accomplished
        promise_2 = Promise.objects.create(name="this is a promise 2",
                                           category=self.category,
                                           ponderator=0.3
                                           )
        promise_2.fulfillment.percentage = 50
        promise_2.fulfillment.save()
        promise_4 = Promise.objects.create(name="this is a promise 4",
                                           category=self.category,
                                           ponderator=0.1
                                           )
        promise_4.fulfillment.percentage = 1
        promise_4.fulfillment.save()
        promise_5 = Promise.objects.create(name="this is a promise 5",
                                           category=self.category,
                                           ponderator=0.1
                                           )
        promise_5.fulfillment.percentage = 99
        promise_5.fulfillment.save()
        # fully acoomplished promises
        promise_3 = Promise.objects.create(name="this is a promise 3",
                                           category=self.category,
                                           ponderator=0.1
                                           )
        promise_3.fulfillment.percentage = 100
        promise_3.fulfillment.save()

        promises = Promise.objects.all()
        self.assertEquals(promises.get(id=promise_1.id).index, 0.0)
        self.assertEquals(promises.get(id=promise_2.id).index, 15.0)
        self.assertEquals(promises.get(id=promise_3.id).index, 10.0)
        self.assertEquals(promises.get(id=promise_4.id).index, 0.1)
        self.assertEquals(promises.get(id=promise_5.id).index, 9.9)
