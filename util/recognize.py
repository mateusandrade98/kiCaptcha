import tensorflow as tf #importação do tensorflow para construção de redes neurais
from tensorflow.examples.tutorials.mnist import input_data #importação de um exemplo de reconhecimento de números do proprio tensorflow

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True) #leitura do database de números para treinamento

n_train = mnist.train.num_examples #números para treinamento
n_validation = mnist.validation.num_examples #números para validação do treinamento
n_test = mnist.test.num_examples #números para os testes de treinamento

n_input = 784 #quantidade de entradas
n_hidden1 = 512 #layer1 oculta
n_hidden2 = 256 #layer2 oculta
n_hidden3 = 128 #layer3 oculta
n_output = 10 #saída
