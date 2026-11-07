
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <winsock2.h>
#include <mysql.h>

void transformar_maiusculo(char *str) {
    while (*str) {
        *str = toupper((unsigned char)*str);
        str++;
    }
}

int main() {
    MYSQL *conexao = mysql_init(NULL);
    if (conexao == NULL) {
        fprintf(stderr, "Erro ao inicializar o MySQL: %s\n", mysql_error(conexao));
        return 1;
    }
    if (mysql_real_connect(conexao, "localhost", "root", "sua_senha_aqui", "integracao_estagio", 0, NULL, 0) == NULL) {
        fprintf(stderr, "Erro ao conectar no banco: %s\n", mysql_error(conexao));
        mysql_close(conexao);
        return 1;
    }
    printf("v Conexao com o MySQL realizada com sucesso!\n");
    int id_bruto = 42;
    char nome_bruto[] = "joao silva";
    char email_bruto[] = "JOAO@EMAIL.COM";
    char cidade_bruta[] = "Brasilia";
    printf("v Dados brutos extraidos da origem.\n");
    transformar_maiusculo(nome_bruto);
    for(int i = 0; email_bruto[i]; i++){
        email_bruto[i] = tolower((unsigned char)email_bruto[i]);
    }
    printf("v Fase de Transformacao concluida (Dados padronizados).\n");
    char query[500];
    sprintf(query, "INSERT INTO tb_usuarios_tratados (id, nome, email, cidade, data_importacao) VALUES (%d, '%s', '%s', '%s', NOW()) ON DUPLICATE KEY UPDATE nome='%s', email='%s', cidade='%s', data_importacao=NOW();", id_bruto, nome_bruto, email_bruto, cidade_bruta, nome_bruto, email_bruto, cidade_bruta);
    if (mysql_query(conexao, query)) {
        fprintf(stderr, "x Erro ao carregar os dados no MySQL: %s\n", mysql_error(conexao));
    } else {
        printf("v Dados carregados com sucesso no MySQL (Carga Idempotente)!\n");
    }
    mysql_close(conexao);
    printf("=== Pipeline C Finalizado ===\n");
    return 0;
}
