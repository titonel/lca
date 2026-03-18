import sqlite3
import os

# Nomes dos arquivos de banco de dados
DB_NEW = 'db.sqlite3'
DB_HIPERTENSAO = 'old-hipertensao.sqlite3'
DB_MAREVAN = 'old-marevan.sqlite3'


def get_connection(db_file):
    if not os.path.exists(db_file):
        raise FileNotFoundError(f"O banco de dados {db_file} não foi encontrado no diretório atual.")
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn


def copy_table_mapped(cursor_src, cursor_dest, table_src, table_dest, user_map, user_fk_cols):
    """
    Copia dados da tabela de origem para a tabela de destino, mantendo os IDs originais,
    mas substituindo os IDs de chaves estrangeiras (FK) de usuários de acordo com o mapeamento.
    """
    # Identificar quais colunas existem no banco de destino para a tabela
    cursor_dest.execute(f"PRAGMA table_info({table_dest})")
    dest_cols = [row['name'] for row in cursor_dest.fetchall()]

    # Buscar os dados de origem
    try:
        cursor_src.execute(f"SELECT * FROM {table_src}")
        rows = cursor_src.fetchall()
    except sqlite3.OperationalError:
        print(f"  [Aviso] Tabela {table_src} não encontrada no banco de origem. Ignorando...")
        return

    if not rows:
        print(f"  [Info] Nenhum dado encontrado na tabela {table_src}.")
        return

    src_cols = rows[0].keys()

    # Cruza colunas de origem com as colunas existentes no destino
    common_cols = [c for c in src_cols if c in dest_cols]
    if not common_cols:
        return

    placeholders = ', '.join(['?'] * len(common_cols))
    insert_sql = f"INSERT INTO {table_dest} ({', '.join(common_cols)}) VALUES ({placeholders})"

    count = 0
    for row in rows:
        values = []
        for col in common_cols:
            val = row[col]
            # Se for uma coluna referenciando a tabela de usuários, aplicar o mapeamento do ID
            if col in user_fk_cols and val is not None:
                val = user_map.get(val, val)
            values.append(val)

        try:
            cursor_dest.execute(insert_sql, values)
            count += 1
        except sqlite3.IntegrityError as e:
            print(f"  [Erro] Falha ao inserir na tabela {table_dest} (ID={row['id']}): {e}")

    print(f"  [Sucesso] {count} registros copiados para {table_dest}.")


def migrate_users(cursor_src, cursor_dest, user_map):
    """
    Migra a tabela de usuários unificando pela coluna 'username'.
    Salva o dicionário de equivalência: ID do banco antigo -> ID no banco novo.
    """
    cursor_dest.execute("PRAGMA table_info(core_usuario)")
    dest_cols = [row['name'] for row in cursor_dest.fetchall() if row['name'] != 'id']

    cursor_src.execute("SELECT * FROM core_usuario")
    count = 0

    for row in cursor_src.fetchall():
        username = row['username']

        # Verifica se este usuário já foi cadastrado no banco novo
        cursor_dest.execute("SELECT id FROM core_usuario WHERE username = ?", (username,))
        existing = cursor_dest.fetchone()

        if existing:
            # O usuário já existe (foi importado de outro banco ou já estava no destino)
            user_map[row['id']] = existing['id']
        else:
            # Inserir o novo usuário
            values = []
            cols_to_insert = []

            for col in dest_cols:
                if col in row.keys():
                    values.append(row[col])
                    cols_to_insert.append(col)
                else:
                    # Tratar colunas novas do db.sqlite3 (ex: is_administrador)
                    if col in ['is_administrador', 'is_navegador']:
                        values.append(0)  # Padrão para False (0)
                        cols_to_insert.append(col)

            placeholders = ', '.join(['?'] * len(cols_to_insert))
            sql = f"INSERT INTO core_usuario ({', '.join(cols_to_insert)}) VALUES ({placeholders})"
            cursor_dest.execute(sql, values)

            # Guardar o novo ID gerado para uso posterior nas foreign keys
            user_map[row['id']] = cursor_dest.lastrowid
            count += 1

    print(f"  [Sucesso] {count} novos usuários integrados.")


def main():
    print("Iniciando processo de migração de banco de dados...")

    # Abrindo conexões
    conn_new = get_connection(DB_NEW)
    conn_hip = get_connection(DB_HIPERTENSAO)
    conn_mar = get_connection(DB_MAREVAN)

    # Desabilitar checagem de integridade FK temporariamente no banco de destino para facilitar inserções
    conn_new.execute("PRAGMA foreign_keys = OFF;")

    cursor_new = conn_new.cursor()

    # 1. Unificando Usuários
    print("\n--- Migrando Usuários (Hipertensão) ---")
    user_map_hip = {}  # Mapeamento ID_Antigo -> ID_Novo
    migrate_users(conn_hip.cursor(), cursor_new, user_map_hip)

    print("\n--- Migrando Usuários (Anticoagulação/Marevan) ---")
    user_map_mar = {}  # Mapeamento ID_Antigo -> ID_Novo
    migrate_users(conn_mar.cursor(), cursor_new, user_map_mar)

    # 2. Migrando Módulo de Hipertensão
    print("\n--- Migrando Dados Clínicos (Hipertensão) ---")
    tabelas_hipertensao = [
        # (tabela_origem, tabela_destino, [colunas_foreign_key_usuarios])
        ('core_paciente', 'hipertensao_paciente', []),
        ('core_medicamento', 'hipertensao_medicamento', []),
        ('core_triagemhipertensao', 'hipertensao_triagemhipertensao', ['profissional_id']),
        ('core_atendimentomedico', 'hipertensao_atendimentomedico', ['medico_id']),
        ('core_prescricaomedica', 'hipertensao_prescricaomedica', []),
        ('core_itemprescricao', 'hipertensao_itemprescricao', []),
        ('core_afericao', 'hipertensao_afericao', ['usuario_id']),
        ('core_afericao_medicamentos', 'hipertensao_afericao_medicamentos', []),
        ('core_atendimentomultidisciplinar', 'hipertensao_atendimentomultidisciplinar', ['profissional_id']),
        ('core_avaliacaoprevent', 'hipertensao_avaliacaoprevent', [])
    ]

    for tb_origem, tb_destino, fks in tabelas_hipertensao:
        copy_table_mapped(conn_hip.cursor(), cursor_new, tb_origem, tb_destino, user_map_hip, fks)

    # 3. Migrando Módulo de Anticoagulação (Marevan)
    print("\n--- Migrando Dados Clínicos (Anticoagulação) ---")
    tabelas_marevan = [
        # (tabela_origem, tabela_destino, [colunas_foreign_key_usuarios])
        ('core_paciente', 'anticoagulacao_paciente', []),
        ('core_medicao', 'anticoagulacao_medicao', ['usuario_id'])
    ]

    for tb_origem, tb_destino, fks in tabelas_marevan:
        copy_table_mapped(conn_mar.cursor(), cursor_new, tb_origem, tb_destino, user_map_mar, fks)

    # Salvar e reativar constraints
    print("\nLimpando e consolidando alterações...")
    conn_new.commit()
    conn_new.execute("PRAGMA foreign_keys = ON;")

    # Fechar conexões
    conn_new.close()
    conn_hip.close()
    conn_mar.close()
    print("Migração concluída com sucesso!")


if __name__ == '__main__':
    main()