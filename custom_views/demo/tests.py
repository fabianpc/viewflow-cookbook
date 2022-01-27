from django.contrib.auth.models import User
from django.test import TestCase
from viewflow.models import Process

from demo.bloodtest.models import Patient


class Test(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.login(username='admin', password='password')

    def testFirstSampleFlow(self):
        self.client.post(
            '/workflow/bloodtest/bloodtest/first_sample/',
            {'0-patient_id': 'Patient-001',
             '0-age': '72',
             '0-sex': 'M',
             '0-weight': '92',
             '0-height': '198',
             'first_bood_sample_view-current_step': '0',
             '_viewflow_activation-started': '2000-01-01'}
        )
        self.client.post(
            '/workflow/bloodtest/bloodtest/first_sample/',
            {'1-taken_at': '2017-02-23 10:51:09',
             'first_bood_sample_view-current_step': '1',
             '_viewflow_activation-started': '2000-01-01'}
        )

        self.client.post(
            '/workflow/bloodtest/bloodtest/1/biochemical_analysis/2/assign/'
        )

        self.client.post(
            '/workflow/bloodtest/bloodtest/1/biochemical_analysis/2/',
            {'hemoglobin': '11',
             'lymphocytes': '6',
             '_viewflow_activation-started': '2000-01-01'}
        )

        self.client.post(
            '/workflow/bloodtest/bloodtest/1/hormone_tests/4/assign/'
        )

        self.client.post(
            '/workflow/bloodtest/bloodtest/1/hormone_tests/4/',
            {'acth': '1',
             'estradiol': '2',
             'free_t3': '3',
             'free_t4': '4',
             '_viewflow_activation-started': '2000-01-01'}
        )

        self.client.post(
            '/workflow/bloodtest/bloodtest/1/tumor_markers_test/5/assign/'
        )

        self.client.post(
            '/workflow/bloodtest/bloodtest/1/tumor_markers_test/5/',
            {'alpha_fetoprotein': '1',
             'beta_gonadotropin': '2',
             'ca19': '3',
             'cea': '4',
             'pap': '5',
             'pas': '6',
             '_viewflow_activation-started': '2000-01-01'}
        )

        process = Process.objects.get()

        self.assertEquals('DONE', process.status)
        self.assertEquals(7, process.task_set.count())

    def testSecondSampleFlow(self):
        patient = Patient.objects.create(
            patient_id='Patient-001',
            age=72,
            sex='M',
            weight=92,
            height=198,
        )

        self.client.post(
            '/workflow/bloodtest/bloodtest/second_sample/',
            {'taken_at': '2017-02-23 10:51:09',
             'patient': patient.pk,
             '_viewflow_activation-started': '2000-01-01'}
        )

        self.client.post(
            '/workflow/bloodtest/bloodtest/1/biochemical_analysis/2/assign/'
        )

        self.client.post(
            '/workflow/bloodtest/bloodtest/1/biochemical_analysis/2/',
            {'hemoglobin': '12',
             'lymphocytes': '5',
             '_viewflow_activation-started': '2000-01-01'}
        )

        process = Process.objects.get()

        self.assertEquals('DONE', process.status)
        self.assertEquals(5, process.task_set.count())
