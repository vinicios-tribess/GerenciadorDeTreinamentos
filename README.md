# Gerenciador De Treinamentos

Como compilar e executar?
---
A compilação é feita através do PyInstaller.  
Caso sua máquina não tenha o PyInstaller, primeiro é necessário fazer a instalação do mesmo. Esse processo ocorre através do __pip__, seguindo os passos abaixo:

- Passo 1:  
Em uma máquina com Python 3 instalado, abra o terminal e digite o comando abaixo, pressione enter e aguarde a instalação:  
```
pip install pyinstaller
```
- Passo 2:  
Ainda dentro do terminal, navegue até a pasta onde se encontram os arquivos **Gerenciador.py** e **functions.py**, e então execute o seguinte comando:
```
pyinstaller --onefile Gerenciador.py
```
- Passo 3:  
Após encerrar o processo, feche o terminal e abra pelo explorador de arquivos a pasta onde onde se encontrava o arquivo compilado.
Você deve encontrar uma pasta chamada *dist*. Abra ela e procure pelo executável ___Gerenciador.exe___.

- Passo 4:  
Execute o programa. Você deverá ver uma tela semelhante a que está abaixo. Se isso acontecer, significa que ocorreu tudo certo e o programa já está rodando.  

```
Bem-vindo ao Gerenciador de Treinamentos Versão 5.0!
Digite o número de pessoas que participarão do evento:
->
```
Funcionamento do Programa
---
**Cadastros**   

O programa inicia com uma mensagem de boas-vindas.    

Logo após essa mensagem, ele pede para que seja informado o número de pessoas que farão parte do evento. Digite o número e pressione ___Enter___.    
    
Desse momento em diante, basta apenas ir informando ao programa as informações que ele for pedindo, quando forem solicitadas, e pressionando ___Enter___ para confirmar.   
 
Caso alguma informação for incorreta ou incoerente, o programa avisará e pedirá que você corrija ela. A parte de cadastro encerra quando você chegar no Menu de Consultas     
    
**Menu de Consultas**    
    
O Menu de Consultas tem a seguinte aparência:    
```
Tudo pronto! Os dados estão salvos e já podem ser utilizados.
Digite a opção do que você deseja fazer agora:
1 - Consultar pessoa pelo nome.
2 - Consultar sala pelo nome.
3 - Consultar espaço de café pelo nome.
4 - Sair (encerrar o programa).

Sua opção:
->
```
Para selecionar uma opção, digite o número dela logo abaixo do campo __"Sua opção:"__.    
    
Dentro de cada menu, informe ao programa as informações que ele pedir, e ele retornará a consulta ao banco de dados de acordo com os parâmetros informados.    
    
Após encerrar uma consulta, lhe será dada a opção de fazer uma nova consulta ou retornar ao Menu de Consultas.    

Para encerrar o programa, feche-o ou escolha a opção 4 dentro do Menu de Consultas.    

Observações Importantes
---    
* Caso o programa seja encerrado após chegar ao Menu de Consultas, os dados ficam salvos para utilização posterior (consultas posteriores).
* Caso o programa seja encerrado antes de chegar ao Menu de Consultas, os dados que foram cadastrados ficarão salvos, mas de maneira inacessível ao programa dentro do arquivo **BancoDeDados.db**.    
Se o programa for iniciado novamente, eles serão apagados para realizar uma nova etapa de cadastro.
* O programa não diferencia letras minúsculas de maiúsculas, mas diferencia letras com acento das sem acento.