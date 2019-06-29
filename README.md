# SCCvSD
Sports Camera Calibration via Synthetic Data

The original implemenation uses Matlab. This is a re-implementation.


The two-GAN code: https://github.com/lood339/pytorch-two-GAN

Link: https://arxiv.org/abs/1810.10658

Install required package via conda:

conda install -c anaconda numpy

conda install -c anaconda scipy

conda install -c conda-forge pyflann

conda install -c conda-forge opencv 


A demo script in testing phase: python/demo.py

To do:
1. sample pivot and positive camera pose pairs. 
2. train siamese network and extract feature. 
3. add '../data/features/testset_feature.mat'
