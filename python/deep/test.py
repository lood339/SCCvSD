import scipy.io as sio
import numpy as np

data = sio.loadmat('../../data/features/testset_feature.mat')

#sio.savemat('database_camera_feature.mat', {'cameras': cameras,
#                                            'features':features})

#print('{}'.format(data['edge_distances'].keys()))
d1 = data['edge_distances']
d2 = data['edge_map']
d3 = data['features']



print('{} {} {}'.format(d1.shape, d2.shape, d3.shape))
#cameras = data['cameras']
#features = data['features']
#print(data.keys())
#print('{} {}'.format(cameras.shape, features.shape))