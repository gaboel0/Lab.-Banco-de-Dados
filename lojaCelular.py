import mysql.connector


def cria_estrutura(sql, conexao, tabela):
    try:
        conexao.execute(sql)
        print("Tabela", tabela, "criada com sucesso")
    except mysql.connector.Error as err:
        print("Erro ao criar tabela:", tabela)
        print("Mensagem de erro:", err)
        exit()


try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="loja_celulares"
    )
    cursor = conexao.cursor()
except mysql.connector.Error as err:
    print("Erro ao conectar com o banco de dados")
    print("Mensagem de erro:", err)
    exit()


# cria_estrutura("CREATE TABLE IF NOT EXISTS empresas (id INT NOT NULL AUTO_INCREMENT, nome VARCHAR(50), PRIMARY KEY (id))", cursor, "empresas")

# cria_estrutura("CREATE TABLE produtos (id INT NOT NULL AUTO_INCREMENT, nome VARCHAR(50) NOT NULL, valor DECIMAL(10,2) NOT NULL, PRIMARY KEY (id))", cursor, "produtos")

# cria_estrutura("CREATE TABLE servicos (id INT NOT NULL AUTO_INCREMENT, nome VARCHAR(50) NOT NULL, valor DECIMAL(10,2) NOT NULL, PRIMARY KEY (id))", cursor, "servicos")

# cria_estrutura("CREATE TABLE vendas (id INT NOT NULL AUTO_INCREMENT, data_pedido DATE, valor DECIMAL(10,2) NOT NULL, id_produto INT, PRIMARY KEY (id), FOREIGN KEY (id_produto) REFERENCES produtos(id))", cursor, "vendas")

# cria_estrutura("CREATE TABLE itens_venda (id INT NOT NULL AUTO_INCREMENT, venda_id INT NOT NULL, produto_id INT, servico_id INT, quantidade INT, preco_unitario_produto FLOAT, preco_unitario_servico FLOAT, preco_total FLOAT, PRIMARY KEY (id), FOREIGN KEY (venda_id) REFERENCES vendas(id), FOREIGN KEY (produto_id) REFERENCES produtos(id), FOREIGN KEY (servico_id) REFERENCES servicos(id))", cursor, "itens_venda")


def cadastrarEmpresa():
    nome = input("Digite o nome da empresa: ")
    cursor = conexao.cursor()
    sql = "INSERT INTO empresas (nome) VALUES (%s)"
    valores = (nome,)
    cursor.execute(sql, valores)
    conexao.commit()


def listarEmpresa():
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM empresas ORDER BY id")
    empresas = cursor.fetchall()
    if not empresas:
        print("Não existem empresas cadastradas")
    else:
        for empresa in empresas:
            print(" ")
            print(f"ID: {empresa[0]}, Nome: {empresa[1]},")
            print(" ")


def cadastrarProduto():
    produtoNome = input("Digite o nome do produto: ")

    print("Escolha qual empresa deseja vincular o produto: ")
    listarEmpresa()

    empresa_id = input("ID da empresa escolhida: ")
    cursor = conexao.cursor()
    sql = "SELECT id FROM empresas WHERE id = %s"
    valores = (empresa_id,)
    cursor.execute(sql, valores)

    empresa = cursor.fetchone()

    if empresa is None:
        print("ID inválido")
    else:
        cursor = conexao.cursor()
        sql = "INSERT INTO produtos (nome, valor, empresas_id) VALUES (%s, %s, %s)"
        valor = float(input("Digite o valor do produto: "))
        valores = (produtoNome, valor, empresa_id)
        cursor.execute(sql, valores)
        conexao.commit()
        print("Produto cadastrado com sucesso")


def listarProdutos():
    cursor = conexao.cursor()
    cursor.execute("SELECT produtos.id, produtos.nome, produtos.valor, empresas.nome FROM produtos INNER JOIN empresas ON produtos.empresa_id = empresas.id ORDER BY id ")
    produtos = cursor.fetchall()
    if not produtos:
        print("Não existem produtos cadastrados")
    else:
        for produto in produtos:
            print(" ")
            print(f"ID: {produto[0]}, Nome: {produto[1]}, Valor: {produto[2]}, Nome Empresa: {produto[3]}")
            print(" ")

def vender():
    produto_id = input("Digite o ID do produto a ser vendido: ")
    cursor = conexao.cursor()
    sql = "SELECT * FROM produtos WHERE id = %s"
    valores = (produto_id,)
    cursor.execute(sql, valores)
    produto = cursor.fetchone()

    if produto is None:
        print("Produto não encontrado")
    else:
        quantidade = int(input("Digite a quantidade vendida: "))
        preco_unitario = produto[2]  
        preco_total = quantidade * preco_unitario

        cursor = conexao.cursor()
        sql = "INSERT INTO vendas (data_pedido, valor, id_produto) VALUES (CURDATE(), %s, %s)"
        valores = (preco_total, produto_id)
        cursor.execute(sql, valores)
        conexao.commit()

        venda_id = cursor.lastrowid

        cursor = conexao.cursor()
        sql = "INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario_produto, preco_total) VALUES (%s, %s, %s, %s, %s)"
        valores = (venda_id, produto_id, quantidade, preco_unitario, preco_total)
        cursor.execute(sql, valores)
        conexao.commit()

        print("Venda registrada com sucesso!")


def listarVendas():
    cursor = conexao.cursor()
    cursor.execute("SELECT vendas.id, vendas.data_pedido, vendas.valor, produtos.nome FROM vendas INNER JOIN produtos ON vendas.id_produto = produtos.id ORDER BY id")
    vendas = cursor.fetchall()
    if not vendas:
        print("Não existem vendas registradas")
    else:
        for venda in vendas:
            print(" ")
            print(f"ID: {venda[0]}, Data Pedido: {venda[1]}, Valor: {venda[2]}, Produto: {venda[3]}")
            print(" ")


while True:
    print("\nEscolha uma opção")
    print("1 - Cadastrar empresa...")
    print("2 - Cadastrar produto...")
    print("3 - Listar empresas...")
    print("4 - Listar produtos...")
    print("5 - Vender. . . ")
    print("6 - Listar vendas. . .")
    print("0 - Sair")

    opcao = int(input("Insira sua opção: "))

    if opcao == 1:
        cadastrarEmpresa()
    elif opcao == 3:
        listarEmpresa()
    elif opcao == 2:
        cadastrarProduto()
    elif opcao == 4:
        listarProdutos()
    elif opcao == 5:
        vender()
    elif opcao == 6:
        listarVendas()
    elif opcao == 0:
        break
    else:
        print("Opção inválida")
