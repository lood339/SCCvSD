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

If no GPU:  
conda install pytorch-cpu torchvision-cpu -c pytorch    


**Pre-processing:** 
1. Generate HoG feature (optional)  
`cd python/hog`
`python generate_test_feature_hog.py`  
`python generate_database_hog.py`  

Put two generated .mat files to ./data/features

2. train a network to generate deep feature (optional)   
Here, we use 10K cameras for an example.   
`cd python/deep`   
`python generate_train_data.py`  
Put the generated .mat file to ./data  
`bash network_train.sh`  
It generates a 'network.pth' file.  
`bash network_test.sh`    
It generates a .mat file which has 'features' and 'cameras'.  


**A demo script in testing phase:**  
python/demo.py  
python/demo_uot.py   # contributed by jiangwei221     
Example 1: use deep feature  
`python demo.py --feature-type 'deep' --query-index 0 ` 
It uses pre-trained-deep-features.

Example 2: use HoG feature  
`python demo.py --feature-type 'HoG' --query-index 0`

Example 3: run all testing example of UoT dataset  
`python demo_uot.py --feature-type 'deep'`    

You wil get the result:  
mean IoU for refined homogrpahy 0.948    
median IoU for refined homogrpahy 0.964  
Slightly better than the result in the paper.       

To do:  
1. Refine train siamese network and extract deep feature. 
2. Accuracy of HoG feature is lower than 
   the matlab implementation (using vlfeat)
 

