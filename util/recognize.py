import tensorflow as tf #importação do tensorflow para construção de redes neurais.
import numpy as np #importação da biblioteca de criação de conjuntos multidimensionais.
from tensorflow.examples.tutorials.mnist import input_data #importação de um exemplo de reconhecimento de números do proprio tensorflow.

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True) #leitura do database de números para treinamento.

n_train = mnist.train.num_examples #números para treinamento.
n_validation = mnist.validation.num_examples #números para validação do treinamento.
n_test = mnist.test.num_examples #números para os testes de treinamento.

n_input = 784 #quantidade de entradas.
n_hidden1 = 512 #layer1 oculta.
n_hidden2 = 256 #layer2 oculta.
n_hidden3 = 128 #layer3 oculta.
n_output = 10 #saída.

learning_rate = 1e-4 #taxa de aprendizado.
n_iterations = 1000 #quantidade de interação.
batch_size = 128 #tamanho do lote.
dropout = 0.5 #tamanho do drop 50%.

X = tf.placeholder("float", [None, n_input]) #criando uma virtual variável X(entrada).
Y = tf.placeholder("float", [None, n_output]) #criando uma virtual variável Y(saída).

#redes neurais
#X(entrada) -> (Layer1Hidden -> Layer2Hidden -> Layer3Hidden)(processamento) -> Y(saída).

keep_prob = tf.placeholder(tf.float32) #taxa de desistência do treinamento, baseado no dropout.

weights = {
    'w1': tf.Variable(tf.truncated_normal([n_input, n_hidden1], stddev=0.1)),
    'w2': tf.Variable(tf.truncated_normal([n_hidden1, n_hidden2], stddev=0.1)),
    'w3': tf.Variable(tf.truncated_normal([n_hidden2, n_hidden3], stddev=0.1)),
    'out': tf.Variable(tf.truncated_normal([n_hidden3, n_output], stddev=0.1)),
} #conjunto de desenvolvimento da estrutura neural.

biases = {
    'b1': tf.Variable(tf.constant(0.1, shape=[n_hidden1])),
    'b2': tf.Variable(tf.constant(0.1, shape=[n_hidden2])),
    'b3': tf.Variable(tf.constant(0.1, shape=[n_hidden3])),
    'out': tf.Variable(tf.constant(0.1, shape=[n_output]))
}#conjunto de criação das variavéis da estrutura neural.

layer_1 = tf.add(tf.matmul(X, weights['w1']), biases['b1']) #Layer1.
layer_2 = tf.add(tf.matmul(layer_1, weights['w2']), biases['b2']) #Layer2.
layer_3 = tf.add(tf.matmul(layer_2, weights['w3']), biases['b3']) #Layer3.
layer_drop = tf.nn.dropout(layer_3, keep_prob) #LayerDrop.
output_layer = tf.matmul(layer_3, weights['out']) + biases['out'] #LayerOut.

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=output_layer)) #probabilidade de acerto com o output_layer.
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)#tempo de otimização de processamento neural.

correct_pred = tf.equal(tf.argmax(output_layer, 1), tf.argmax(Y, 1)) #retorna os resultados parecidos.
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32)) #taxa de precisão.

def initRecognize(img):
    init = tf.global_variables_initializer() #inicializa as variavéis virtuais.
    sess = tf.Session() #cria uma sessão.
    sess.run(init) #carrega a sessão.

    for i in range(n_iterations): #cria um range de interações.
        batch_x, batch_y = mnist.train.next_batch(batch_size) #treina o neurônio com o lote, e retorna o lote x e y.
        sess.run(train_step,feed_dict={X:batch_x,Y:batch_y,keep_prob:dropout}) #carrega o retorno do treinamento e executa.

        if i%100==0: #caso o interação for divisível de 100 entra na condição.
            minibatch_loss, minibatch_accuracy = sess.run([cross_entropy, accuracy], feed_dict={X: batch_x, Y: batch_y, keep_prob:1.0}) #carrega e retorna a parca e a precissão do treino.
            print("Iteração", str(i), "\t| Perda =", str(minibatch_loss), "\t| Precisão =", str(minibatch_accuracy))#mostra o resultado da condição.

    prediction = sess.run(tf.argmax(output_layer,1), feed_dict={X: [img]}) #executa o reconhecimento da imagem, e retorna uma previsão de qual seria o número.
    print("Previsão do número: ", np.squeeze(prediction))
