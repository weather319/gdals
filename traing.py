from bp_neuralnetwork import NeuralNetwork 
from load_training_data import load_data
import numpy as np




if __name__ == '__main__':
    data_path = 'C:/zhut11/python/data/'
    excel_path = 'C:/zhut11/python/gdals/TH.xlsx'
    WaterQualiteId_lists = ['叶绿素a']

    train_data = []
    train_labels = []

    test_data = []
    test_labels = []

    x_array,y_array = load_data(excel_path,WaterQualiteId_lists,data_path,save_excel = True)
    num = len(y_array)
    print ('一共有[{}]条数据'.format(num))

    train_data = np.array(x_array[:90])
    train_labels = np.array(y_array[:90])
    print ('训练数据90条')
    test_data = np.array(x_array[91:num])
    test_labels = np.array(y_array[91:num])
    print ('测试数据{}条'.format(num-91))

    layers = [7,5,1]
    print ('设定的神经网络模型层数为{}'.format(layers))
    nn = NeuralNetwork(layers=layers)

    nn.fit(train_data,train_labels)
    nn.test(test_data,test_labels,5)

