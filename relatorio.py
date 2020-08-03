from ResumeStock import Wallet
import numpy as np

ticks = ['WEGE3.SA','PETR4.SA','B3SA3.SA','ITSA4.SA','RAPT4.SA','BTOW3.SA','VVAR3.SA','PRIO3.SA','OIBR3.SA','COGN3.SA','ANIM3.SA']
strHTML = '<h1>Relatório Dianna</h1>'
strHTML = strHTML + 'Relatório Dianna gerado para a carteira com as seguintes ações:'
for tick in ticks:
    acao = Wallet([tick])
    strHTML = strHTML + '<br><h3> {} </h3>'.format(tick)
    media = round(acao.mean(mode=1)*100,2)
    strHTML = strHTML + 'Média de retorno encontrada para a ação: {}%  <br>'.format(media)
    variacao = round(acao.walletVariance()*100,2)
    strHTML = strHTML + 'Variação da ação: {}% <br>'.format(variacao)
    volatilidade = round(acao.walletVolatility()*100,2)
    strHTML = strHTML + 'Volatilidade da ação: {}% <br>'.format(volatilidade)
    beta = round(acao.beta(),2)
    strHTML = strHTML + 'Beta da ação: {} <br>'.format(beta)
    esperado = round(acao.expReturn()*100,2)
    strHTML = strHTML + 'Retorno esperado, considerando 2.25% de juros livre e 8% de prêmio de mercado : {}% <br>'.format(esperado)
    sharpe = round(acao.sharpe(),2)
    strHTML = strHTML + 'Numero Sharpe: {} <br><br><br>'.format(sharpe)

strHTML = strHTML + 'Resumo da carteira: <br> Foi utilizada a teoria moderna de portifólios para definir quais as melhores combinações de peso para a carteira: <br>'
carteira = Wallet(ticks)
border = carteira.border()
melhores =list(np.array(border.sort_values(['Volatility','Return']).iloc[0:5]))
cont = 1
for tentativa in melhores:
    strHTML = strHTML + '<br>Iteração {} <br>'.format(cont)
    cont += 1
    pesos = list(tentativa[2])
    strHTML = strHTML + '<table style="border:1px solid black">'
    for x in range(len(pesos)):
        strHTML = strHTML + '<tr style="border:1px solid black"><th style="font-weight:bold;border:1px solid black">{}</th><th style="border:1px solid black">{}%</th></tr>'.format(ticks[x],round(pesos[x]*100,2))
    strHTML = strHTML + '</table>'
    retorno = round(tentativa[0]*100,2)
    volatilidade = round(tentativa[1]*100,2)
    carteira.weights = pesos
    variacao = round(carteira.walletVariance()*100,2)
    strHTML = strHTML + 'Média de retorno encontrada para a carteira: {}% <br>'.format(retorno)
    strHTML = strHTML + 'Variação da carteira: {}% <br>'.format(variacao)
    strHTML = strHTML + 'Volatilidade da carteira: {}% <br>'.format(volatilidade)
    beta = round(carteira.beta(),2)
    strHTML = strHTML + 'Beta da carteira: {} <br>'.format(beta)
    esperado = round(carteira.expReturn()*100,2)
    strHTML = strHTML + 'Retorno esperado: {}% <br>'.format(esperado)
    sharpe = round(carteira.sharpe(),2)
    strHTML = strHTML + 'Número de Sharpe da carteira: {} <br>'.format(sharpe)
    riscoDiv = round(carteira.divRisc()*100,2)
    strHTML = strHTML + 'Risco diversificável: {}% <br>'.format(riscoDiv)
    nonRiscoDiv = round(carteira.nonDivRisc()*100,2)
    strHTML = strHTML + 'Risco não Diversificado: {}% <br>'.format(nonRiscoDiv)
    resultados = (carteira.MonteCarlo())
    monte = list(resultados[-1])
    count = 0
    esp = 0
    pos = 0
    S0 = carteira.historic.iloc[-1].sum()
    for x in range(len(monte)):
        valor_final = monte[x]
        valor_meio = list(resultados[int(len(resultados)/2)])[x]
        m1 = ((valor_meio/S0)-1)*100
        m2 = ((valor_final/valor_meio)-1)*100
        media_anual = (m1+m2)/2
        #print("{} - {} - {} - {}".format(S0,valor_meio,valor_final,media_anual))
        if media_anual >= retorno - 5:
            count += 1
        if media_anual >= esperado:
            esp += 1
        if media_anual > 0:
            pos += 1
    
    strHTML = strHTML + 'Foram feitas 1000 simulações de Monte Carlo com a carteira, e em {}% das simulações a carteira apresentou um lucro próximo da média em 2 anos. <br>'.format(round(count/10,2))
    strHTML = strHTML + 'Das simulações {}% ficaram acima do retorno esperado <br>'.format(round(esp/10,2))
    strHTML = strHTML + 'Das simulações {}% ficaram com um lucro positivo <br>'.format(round(pos/10,2))
    #print(count)
with open('relatorio.html', "w") as arquivo:
            arquivo.write(strHTML)
    
    
    
    


        