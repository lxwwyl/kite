#!/bin/python
import unittest
import numpy as num
import matplotlib.pyplot as plt

from kite import Scene
from . import common

benchmark = common.Benchmark()
common.setLogLevel('DEBUG')


class TestCovariance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        file = common.get_test_data('myanmar_alos_dsc_ionocorr.mat')
        cls.sc = Scene.import_data(file)

    def test_covariance(self):
        cov = self.sc.covariance
        cov.epsilon = .02
        cov.subsampling = 24

        d = []
        d.append(('Full', cov._calcCovarianceMatrix(method='full',
                 nthreads=0)))
        d.append(('Focal', cov._calcCovarianceMatrix(method='focal')))

        for _, c1 in d:
            for _, c2 in d:
                num.testing.assert_allclose(c1, c2,
                                            rtol=200, atol=2e3, verbose=True)

    def test_synthetic_noise(self):
        self.sc.covariance.syntheticNoise()
        self.sc.covariance.variance

    @benchmark
    def test_covariance_parallel(self):
        cov = self.sc.covariance
        cov._calcCovarianceMatrix(method='full', nthreads=0)

    @benchmark
    def _test_covariance_single_thread(self):
        cov = self.sc.covariance
        cov._calcCovarianceMatrix(method='full', nthreads=1)

    @benchmark
    def test_covariance_focal(self):
        cov = self.sc.covariance
        cov._calcCovarianceMatrix(method='focal')

    @unittest.skip('Skip!')
    def _test_covariance_visual(self):
        cov = self.sc.covariance
        cov.epsilon = .02
        cov.subsampling = 10
        # l = self.sc.quadtree.leaves[0]
        d = []
        d.append(('Full', cov._calcCovarianceMatrix(method='full',
                 nthreads=0)))
        d.append(('Focal', cov._calcCovarianceMatrix(method='focal')))

        fig, _ = plt.subplots(1, len(d))
        for i, (title, mat) in enumerate(d):
            print '%s Max %f' % (title, num.nanmax(mat)), mat.shape
            fig.axes[i].imshow(mat)
            fig.axes[i].set_title(title)
        plt.show()


if __name__ == '__main__':
    unittest.main(exit=False)
    print benchmark
