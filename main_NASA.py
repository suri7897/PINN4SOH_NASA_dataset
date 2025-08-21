from dataloader.dataloader import NASAdata
from Model.Model import PINN
import argparse
import os

def get_args():
    parser = argparse.ArgumentParser('Hyper Parameters for NASA dataset')
    parser.add_argument('--data', type=str, default='NASA', help='XJTU, HUST, MIT, TJU, NASA')
    parser.add_argument('--in_same_batch', type=bool, default=True)
    parser.add_argument('--train_batch', type=int, default=-1, choices=[-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    parser.add_argument('--test_batch', type=int, default=-1, choices=[-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    parser.add_argument('--batch', type=int, default=1, choices=list(range(1,10)))
    parser.add_argument('--batch_size', type=int, default=512)
    parser.add_argument('--normalization_method', type=str, default='min-max')

    # scheduler
    parser.add_argument('--epochs', type=int, default=200)
    parser.add_argument('--early_stop', type=int, default=30) # if model doesn't improve in recent early_stop iterations, then stop.
    parser.add_argument('--warmup_epochs', type=int, default=30)
    parser.add_argument('--warmup_lr', type=float, default=0.002)
    parser.add_argument('--lr', type=float, default=0.01)
    parser.add_argument('--final_lr', type=float, default=0.0002)
    parser.add_argument('--lr_F', type=float, default=0.001)

    # model
    parser.add_argument('--F_layers_num', type=int, default=3)
    parser.add_argument('--F_hidden_dim', type=int, default=60)

    # loss
    parser.add_argument('--alpha', type=float, default=0.7) # controls PDE constraint loss
    parser.add_argument('--beta', type=float, default=0.1) # controls ReLU loss

    parser.add_argument('--log_dir', type=str, default='logging.txt')
    parser.add_argument('--save_folder', type=str, default='results of reviewer/PINN/NASA results')

    return parser.parse_args()


def load_NASA_data(args, small_sample=None):
    root = 'data/NASA data'
    data = NASAdata(root=root, args=args)
    train_list, test_list = [], []

    if args.in_same_batch:
        batch_num = args.batch
        battery_ids = data.batchs[f'Batch_{batch_num}']
        
        dir_list = os.listdir(root)
        dataset_dir = None
        for d in dir_list:
            if all(f'{i:02d}' in d for i in battery_ids):
                dataset_dir = os.path.join(root, d)
                break
        assert dataset_dir is not None, f"Dataset directory for batch {batch_num} not found."

        for battery_id in battery_ids:
            filename = f'B{battery_id:04d}_charge_summary.csv'
            path = os.path.join(dataset_dir, filename)
            if battery_id % 10 in [5, 9]:
                test_list.append(path)
            else:
                train_list.append(path)

        if small_sample:
            train_list = train_list[:small_sample]

        train_loader = data.read_all(train_list)
        test_loader = data.read_all(test_list)

    else:
        train_loader = data.read_one_batch(args.train_batch)
        test_loader = data.read_one_batch(args.test_batch)

    return {
        'train': train_loader['train_2'],
        'valid': train_loader['valid_2'],
        'test': test_loader['test_3']
    }


def main():
    args = get_args()
    for batch in range(1, 10):
        setattr(args, 'in_same_batch', True)
        setattr(args, 'batch', batch)
        for e in range(10):
            save_folder = f'results of reviewer/PINN/NASA results/{batch}-{batch}/Experiment{e+1}'
            setattr(args, 'save_folder', save_folder)
            os.makedirs(save_folder, exist_ok=True)

            dataloader = load_NASA_data(args)
            pinn = PINN(args)
            pinn.Train(
                trainloader=dataloader['train'],
                validloader=dataloader['valid'],
                testloader=dataloader['test']
            )


if __name__ == '__main__':
    main()


