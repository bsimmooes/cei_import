# cei-b3-import
## Script to generate the stocks' descriptions to use in "Declaração de Imposto de Renda Pessoa Física (DIRPF)" through CEI's reports. Help to fill the "Fica de Bens e Direitos".
 
[BR]
Declaração de Imposto de Renda Pessoa Física (DIRPF) é basicamente uma obrigação anual do Brasil que cruza as informações referente, "origem das rendas X bens e direitos X impostos pago no ano calendário", a qual realiza uma espécie de ajuste entre os impostos pagos e os devidos, resultando em um "valor real justo", conforme as normas tributárias do governo.

Dentre todas as fichas que são preenchidas no sistema anualmente pelo contribuinte, temos uma ficha de Bens e Direitos, que devemos incluir nossas posições de custódia de ações no último dia do respectivo ano calendário.

O próprio contribuinte tem a obrigação de realizar o acompanhamento, organização, controle de preço médio de suas ações, como o cálculo dos impostos devidos nas alienações. (Que não é o intuito do projeto ressalta-las, ao menos até agora).

No processo de preenchimento da Ficha de Bens e Direitos, temos um campo que devemos fazer uma breve discriminação com as informações das ações e CNPJ da Empresa.

É comum, que os informes de rendimentos fornecidos pelas instituições financeiras com as posições em custódia, não fornecem essa discriminação para inserir na Declaração, apenas quantidade e valor total atualizado (preço de mercado).

Logo, é necessário realizar a digitação de todas as discriminações conforme um "padrão" para todos os ativos da carteira. Por ser uma tarefa repetitiva e por muitas vezes, informações como CNPJ e Razão Social estarem incompletas ou abreviadas, o contribuinte acaba "gastando" um tempo maior nessa etapa. E devemos prestar bastante atenção para entregar ao fisco as informações de forma clara, objetiva e correta.

### Pensando nisso, por experiência própria, estou compartilhando esse repositório com um script que desenvolvi, com intuito de facilitar o preenchimento da Ficha de Bens e Direitos, em específico para os ativos em custódia do Portal do CEI, da B3.

Basicamente:
1) Recebe um arquivo gerado no Portal do CEI.
2) O script realiza, Data Cleaning + Web Scraping no arquivo e gera um "historico_irpf_12-2020.csv" com as informações necessáraias.
3) Com o "historico_irpf_12-2020.csv", "Ctrl+C e Ctrl+V" no programa da DIRPF, nos campos devidos.

Ressalvas:
1) Os arquivos de exemplo do repositório, foram editados, substituindo dados cadastrais, quantidade e valores das ações.
2) A coluna "SALDO" do "historico_irpf_12-2020.csv", refere-se ao valor total atualizado (preço de mercado), que o Portal do CEI gerou no arquivo. O saldo na Ficha de Bens e Direitos, deve ser preenchida com o saldo total a partir do preço médio dos custos de aquisição, sem nenhuma atualização, valorização ou desvalorização.
3) O preenchimento, organização, conferência da DIRPF são de responsabilidade do contribuinte.
4) Aceito "issues" do github, para aperfeiçoamento e correções. Tenho nível intermediário em Python, logo usei esse contexto para praticar a linguagem.
