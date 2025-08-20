from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

def gerar_pergunta(tipo_calculo):
    intervalo = range(1, 11)
    num1 = random.choice(intervalo)
    num2 = random.choice(intervalo)

    if tipo_calculo == 'multiplicacao':
        resposta = num1 * num2
        operador = '*'
    elif tipo_calculo == 'adicao':
        resposta = num1 + num2
        operador = '+'
    elif tipo_calculo == 'subtracao':
        resposta = num1 - num2
        operador = '-'
    elif tipo_calculo == 'divisao':
        num2 = random.choice(intervalo[1:])
        resposta = num1 // num2
        num1 = resposta * num2
        operador = '/'
    else:
        return None

    return {"num1": num1, "num2": num2, "operador": operador, "resposta": resposta}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz/<tipo>', methods=['GET', 'POST'])
def quiz(tipo):
    if request.method == 'POST':
        acertos = int(request.form['acertos'])
        total = int(request.form['total'])
        resposta_certa = int(request.form['resposta_certa'])
        resposta_usuario = int(request.form['resposta_usuario'])

        if resposta_usuario == resposta_certa:
            acertos += 1

        total += 1

        if total >= 5:
            return redirect(url_for('resultado', acertos=acertos, total=total))

        pergunta = gerar_pergunta(tipo)
        return render_template('quiz.html', tipo=tipo, pergunta=pergunta, acertos=acertos, total=total)

    pergunta = gerar_pergunta(tipo)
    return render_template('quiz.html', tipo=tipo, pergunta=pergunta, acertos=0, total=0)

@app.route('/resultado')
def resultado():
    acertos = request.args.get('acertos')
    total = request.args.get('total')
    return render_template('resultado.html', acertos=acertos, total=total)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
