python network_train.py \
--train-file '../../data/train_data_10k.mat' \
--cuda-id 0 \
--lr 0.01 \
--step-size 50 \
--num-epoch 100 \
--batch-size 2 \
--num-batch 4 \
--random-seed 0 \
--resume '' \
--save-name 'debug.pth'

#parser = argparse.ArgumentParser()
#parser.add_argument('--train-file', required=True, type=str, help='a .mat file')
#parser.add_argument('--cuda-id', required=True, type=int, default=0, help='CUDA ID 0, 1, 2, 3')
#parser.add_argument('--lr', required=True, type=float, help='learning rate')
#parser.add_argument('--step-size', required=True, type=int, help='learning rate drop step size')
#parser.add_argument('--num-epoch', required=True, type=int, help='epoch number')
#parser.add_argument('--batch-size', required=True, type=int)
#parser.add_argument('--num-batch', required=True, type=int, help='training sample number')
#parser.add_argument('--random-seed', required=True, type=int, help='random seed for generating train example')
#parser.add_argument('--resume', default='', type=str, help='path to the save checkpoint')
#parser.add_argument('--save-name', required=True, default='model.pth', type=str, help='model name .pth')