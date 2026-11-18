# Devolutiva formativa — Atividade 01 da SA

**Estudante:** Franciele  
**Turma:** Rio Negrinho — Tarde  
**Unidade Curricular:** Programação de Aplicativos  
**Projeto escolhido:** Escola — Portal do Aluno  
**Código analisado:** `codigo/app.py`  
**Referência:** Situação de Aprendizagem nº 1 — *Da Ideia ao Código*

## O que você já conseguiu desenvolver

Franciele, parabéns pelo desenvolvimento do seu projeto! Você criou um Portal do Aluno que permite consultar notas, médias, faltas e horários escolares. Seu trabalho demonstra uma boa compreensão da organização de programas em Python e da aplicação de conceitos de programação orientada a objetos.

Pontos positivos identificados:

- Utilizou **programação orientada a objetos**, criando as classes `Aluno` e `PortalAluno` para separar informações escolares e funcionalidades do sistema.
- Organizou o programa em **métodos com responsabilidades específicas**, como `calcular_media()`, `menu_notas()`, `menu_faltas()`, `exibir_horario()` e `exibir_media_geral()`.
- Aplicou **listas e dicionários** para armazenar notas, faltas e horários de diferentes disciplinas.
- Implementou corretamente o cálculo da média aritmética, utilizando `sum()` e `len()`.
- Utilizou **estruturas de repetição e condicionais** para construir menus interativos.
- Incluiu tratamento de entradas inválidas com `try/except ValueError`, evitando erros quando o usuário digita letras em opções numéricas.
- Criou um fluxo principal com `if __name__ == "__main__":`, permitindo iniciar o programa diretamente.
- Organizou os dados de demonstração e as funcionalidades de maneira compreensível.

## O que precisa ser corrigido

### 1. Melhorar o sistema de autenticação

Atualmente, o programa utiliza uma senha fixa, definida como `SENHA_PADRAO = "1234"`.

Além disso, qualquer pessoa que informe essa senha pode digitar um nome e acessar os mesmos dados escolares, pois o nome informado substitui `self.aluno.nome`.

**Por que isso é importante?**

Em um sistema escolar real, cada estudante deve acessar somente suas próprias informações. Uma senha compartilhada não permite identificar corretamente o usuário.

**Como melhorar:**

- Criar usuários fictícios para os testes.
- Associar cada usuário às suas próprias notas, faltas e horários.
- Validar a identidade antes de permitir o acesso às informações.

Para a Atividade 01, a senha fixa pode ser compreendida como uma simplificação do protótipo. Entretanto, essa limitação deve ser corrigida antes de utilizar o sistema com dados reais.

### 2. Corrigir o comportamento da média quando não existem notas

No método `calcular_media()`, quando uma disciplina não possui notas cadastradas, o programa retorna `0.0`.

Essa solução evita um erro de divisão por zero, o que é positivo. Porém, pode causar uma interpretação incorreta: uma disciplina sem avaliações não significa necessariamente que o aluno recebeu nota zero.

**Como melhorar:**

Diferenciar as situações:

- Disciplina com notas: calcular a média normalmente.
- Disciplina sem notas: apresentar a mensagem "Ainda não há notas cadastradas".

Esse ajuste melhora a precisão das informações exibidas.

## Oportunidades de melhoria

### 3. Tornar a limpeza da tela compatível com outros sistemas

O programa utiliza `os.system("cls")` em diferentes métodos.

Esse comando funciona normalmente no terminal do Windows, mas pode não funcionar como esperado em Linux ou macOS.

**Como melhorar:**

Criar uma função reutilizável para limpar a tela:

```python
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")
```

Depois, substituir as chamadas repetidas de `os.system("cls")` por `limpar_tela()`.

Isso evita repetição e facilita a manutenção do código.

### 4. Melhorar a experiência de navegação

O uso de `time.sleep()` entre as opções do menu cria uma apresentação gradual, mas também obriga o usuário a esperar sempre que retorna ao menu principal.

**Como melhorar:**

- Reduzir ou remover os atrasos entre as opções.
- Manter mensagens de confirmação somente quando necessário.
- Permitir uma navegação mais rápida entre as funcionalidades.

A interface deve priorizar a clareza e a facilidade de utilização.

### 5. Aprimorar a documentação do código

O programa apresenta nomes de métodos claros e alguns comentários explicativos, mas ainda pode melhorar sua documentação.

No método `obter_materias()`, por exemplo, existe um comentário depois do `return`. Embora isso não cause um erro de execução, dificulta a organização da explicação.

**Como melhorar:**

- Colocar comentários antes do trecho que será explicado.
- Adicionar docstrings aos métodos mais importantes.
- Explicar regras de negócio e comportamentos menos evidentes.
- Evitar comentários que apenas repitam o que o código já demonstra.

Uma boa documentação permite que outro programador compreenda a aplicação sem depender de explicações presenciais.

### 6. Planejar a evolução dos dados escolares

Atualmente, as informações de notas, faltas e horários são definidas diretamente no código.

Isso é adequado para demonstrar as funcionalidades iniciais, mas limita a utilização do sistema por diferentes estudantes.

**Próximo passo:**

Nas próximas etapas, organizar os dados para permitir futuramente:

- Cadastro de estudantes.
- Consulta individual de notas e faltas.
- Atualização de informações.
- Armazenamento em banco de dados.

Essas funcionalidades representam possíveis evoluções do projeto e não precisam ser consideradas entregas já concluídas na Atividade 01.

## Testes recomendados

Antes de avançar para a próxima versão, verifique estes cenários:

1. Acesso com a senha definida para o protótipo.
2. Tentativa de acesso com senha incorreta.
3. Digitação de letras em uma opção numérica do menu.
4. Consulta de notas e cálculo da média de uma disciplina.
5. Consulta de faltas e cálculo do total geral.
6. Exibição do quadro de horários.
7. Consulta de uma disciplina sem notas cadastradas.

Registre quais testes funcionaram e quais situações precisam de correção.

## Prioridades para a próxima versão

1. **Melhorar o controle de acesso, associando cada usuário aos seus próprios dados.**
2. **Diferenciar disciplinas sem notas de disciplinas com média zero.**
3. **Centralizar a limpeza da tela em uma função reutilizável.**
4. **Reduzir atrasos desnecessários na navegação.**
5. **Adicionar documentação aos métodos e registrar os testes realizados.**

## Mensagem final

Franciele, seu projeto apresenta uma estrutura organizada e demonstra que você compreendeu conceitos importantes de programação, especialmente **classes, objetos, métodos, listas, dicionários e estruturas de controle**.

A separação entre as classes `Aluno` e `PortalAluno` é um bom exemplo de como organizar responsabilidades em uma aplicação.

Continue aprimorando o sistema e buscando soluções que tornem o código mais seguro, reutilizável e fácil de manter. Você já possui uma base consistente para desenvolver as próximas funcionalidades do Portal do Aluno.

**Parabéns pelo trabalho e continue evoluindo seu projeto!**
