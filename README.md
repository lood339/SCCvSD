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


Preprocessing:
cd python/hog
python generate_test_feature_hog.py
python generate_database_hog.py

Put two generated .mat files to ./data/features

A demo script in testing phase: python/demo.py

Example 1: use deep feature
python demo.py --feature-type 'deep' --query-index 0

Example 2: use HoG feature
python demo.py --feature-type 'HoG' --query-index 0



To do:
1. train siamese network and extract feature. 
2. Accuracy of HoG feature is lower than 
   the matlab implementation (using vlfeat) 

