from torchvision import datasets, transforms

from model_ops.lenet import LeNet
from model_ops.resnet import *
from model_ops.vgg import *

def build_model(model_name, num_classes):
    # build network
    if model_name == "LeNet":
        return LeNet()
    elif model_name == "ResNet18":
        return ResNet18(num_classes)
    elif model_name == "ResNet34":
        return ResNet34()
    elif model_name == "ResNet50":
        return ResNet50()
    elif model_name == "VGG11":
        return vgg11_bn(num_classes)

def prepare_data(args):
    # load training and test set here:
    if args.dataset == "MNIST":
        training_set = datasets.MNIST('./mnist_data', train=True, download=True,
                   transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))]))
        train_loader = torch.utils.data.DataLoader(training_set, batch_size=args.batch_size, shuffle=True)
        test_loader = torch.utils.data.DataLoader(
            datasets.MNIST('./mnist_data', train=False, transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ])), batch_size=args.test_batch_size, shuffle=True)
    elif args.dataset == "Cifar10":
        normalize = transforms.Normalize(mean=[x/255.0 for x in [125.3, 123.0, 113.9]],
                                std=[x/255.0 for x in [63.0, 62.1, 66.7]])
        transform_train = transforms.Compose([
            transforms.ToTensor(),
            transforms.Lambda(lambda x: F.pad(
                                Variable(x.unsqueeze(0), requires_grad=False),
                                (4,4,4,4),mode='reflect').data.squeeze()),
            transforms.ToPILImage(),
            transforms.RandomCrop(32),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            normalize,
            ])
        # data prep for test set
        transform_test = transforms.Compose([
            transforms.ToTensor(),
            normalize])
        # load training and test set here:
        training_set = datasets.CIFAR10(root='./cifar10_data', train=True,
                                                download=True, transform=transform_train)
        train_loader = torch.utils.data.DataLoader(training_set, batch_size=args.batch_size,
                                                  shuffle=True)
        testset = datasets.CIFAR10(root='./cifar10_data', train=False,
                                               download=True, transform=transform_test)
        test_loader = torch.utils.data.DataLoader(testset, batch_size=args.test_batch_size,
                                                 shuffle=False)
    elif args.dataset == 'Cifar100':
        normalize = transforms.Normalize(mean=[x/255.0 for x in [125.3, 123.0, 113.9]],
                                std=[x/255.0 for x in [63.0, 62.1, 66.7]])
        transform_train = transforms.Compose([
            transforms.ToTensor(),
            transforms.Lambda(lambda x: F.pad(
                                Variable(x.unsqueeze(0), requires_grad=False),
                                (4,4,4,4),mode='reflect').data.squeeze()),
            transforms.ToPILImage(),
            transforms.RandomCrop(32),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            normalize,
            ])
        # data prep for test set
        transform_test = transforms.Compose([
            transforms.ToTensor(),
            normalize])
        # load training and test set here:
        training_set = datasets.CIFAR100(root='./cifar100_data', train=True,
                                                download=True, transform=transform_train)
        train_loader = torch.utils.data.DataLoader(training_set, batch_size=args.batch_size,
                                                  shuffle=True)
        testset = datasets.CIFAR100(root='./cifar100_data', train=False,
                                               download=True, transform=transform_test)
        test_loader = torch.utils.data.DataLoader(testset, batch_size=args.test_batch_size,
                                                 shuffle=False)
    # SVHN dataset
    elif args.dataset == 'SVHN':
        training_set = datasets.SVHN('./svhn_data', split='train', transform=transforms.Compose([
                                 transforms.RandomCrop(32, padding=4),
                                 transforms.RandomHorizontalFlip(),
                                 transforms.ToTensor(),
                                 transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
                             ]))
        train_loader = torch.utils.data.DataLoader(training_set, batch_size=128,
                                                  shuffle=True)
        transform_test = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
            ])
        testset = datasets.SVHN(root='./svhn_data', split='test',
                                               download=True, transform=transform_test)
        test_loader = torch.utils.data.DataLoader(testset, batch_size=args.test_batch_size,
                                                 shuffle=False)
    return train_loader, test_loader