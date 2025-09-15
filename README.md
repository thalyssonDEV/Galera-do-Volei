# Galera do Vôlei - Documentação

API para especificação do gerenciamento de partidas e jogadores de vôlei.

## Sumário de Recursos
- [Jogadores](#jogadores)
- [Partidas](#partidas)
- [Ações em Partidas](#ações-em-partidas)

---

## Jogadores

Recursos para gerenciar os jogadores do sistema.

### Criar um novo jogador

-   **Method:** `POST`
-   **URL:** `/jogadores`
-   **Corpo da Requisição:**
    ```json
    {
        "nome": "João da Silva",
        "email": "joao.silva@example.com",
        "data_nascimento": "1995-08-20",
        "sexo": "MASCULINO",
        "categoria": "AMADOR",
        "senha": "senha_123"
    }
    ```
-   **Resposta (Sucesso):**
    -   **Status:** `201 Created`
    -   **Body:**
        ```json
        {
            "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "nome": "João da Silva",
            "email": "joao.silva@example.com",
            "data_nascimento": "1995-08-20",
            "sexo": "MASCULINO",
            "categoria": "AMADOR"
        }
        ```
-   **Resposta (Falha):**
    -   **Status:** `422 Unprocessable Entity` (se os dados de entrada forem inválidos)

### Obter detalhes de um jogador

-   **Method:** `GET`
-   **URL:** `/jogadores/{jogador_id}`
-   **Parâmetros de Path:**
    -   `jogador_id` (uuid): ID único do jogador.
-   **Resposta (Sucesso):**
    -   **Status:** `200 OK`
    -   **Body:**
        ```json
        {
            "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "nome": "João da Silva",
            "email": "joao.silva@example.com",
            "data_nascimento": "1995-08-20",
            "sexo": "MASCULINO",
            "categoria": "AMADOR"
        }
        ```
-   **Resposta (Falha):**
    -   **Status:** `404 Not Found` (se o jogador não for encontrado)

---

## Partidas

Recursos para gerenciar as partidas.

### Agendar uma nova partida

-   **Method:** `POST`
-   **URL:** `/partidas`
-   **Corpo da Requisição:**
    ```json
    {
        "local_descricao": "Quadra de areia do Parque Central",
        "data_hora": "2025-10-15T20:00:00Z",
        "categoria": "INTERMEDIARIO",
        "tipo": "MISTA",
        "owner_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
    }
    ```
-   **Resposta (Sucesso):**
    -   **Status:** `201 Created`
    -   **Body:**
        ```json
        {
            "id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
            "owner_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "status": "EM_ADESAO",
            "local_descricao": "Quadra de areia do Parque Central",
            "data_hora": "2025-10-15T20:00:00Z",
            "categoria": "INTERMEDIARIO",
            "tipo": "MISTA",
            "jogadores_confirmados": [],
            "jogadores_pendentes": []
        }
        ```

### Listar partidas

-   **Method:** `GET`
-   **URL:** `/partidas`
-   **Parâmetros de Query:**
    -   `categoria` (opcional): Filtra por categoria (ex: `AMADOR`).
    -   `tipo` (opcional): Filtra por tipo (ex: `MISTA`).
    -   `status` (opcional): Filtra por status (ex: `EM_ADESAO`).
-   **Resposta (Sucesso):**
    -   **Status:** `200 OK`
    -   **Body:**
        ```json
        [
            {
                "id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
                "owner_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "status": "EM_ADESAO",
                "local_descricao": "Quadra de areia do Parque Central",
                "data_hora": "2025-10-15T20:00:00Z",
                "categoria": "INTERMEDIARIO",
                "tipo": "MISTA",
                "jogadores_confirmados": ["b2c3d4e5-f6a7-8901-2345-67890abcdef1"],
                "jogadores_pendentes": ["c3d4e5f6-a7b8-9012-3456-7890abcdef12"]
            }
        ]
        ```

### Obter detalhes de uma partida

-   **Method:** `GET`
-   **URL:** `/partidas/{partida_id}`
-   **Parâmetros de Path:**
    -   `partida_id` (uuid): ID único da partida.
-   **Resposta (Sucesso):**
    -   **Status:** `200 OK`
    -   **Body:**
        ```json
        {
            "id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
            "owner_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "status": "EM_ADESAO",
            "local_descricao": "Quadra de areia do Parque Central",
            "data_hora": "2025-10-15T20:00:00Z",
            "categoria": "INTERMEDIARIO",
            "tipo": "MISTA",
            "jogadores_confirmados": ["b2c3d4e5-f6a7-8901-2345-67890abcdef1"],
            "jogadores_pendentes": ["c3d4e5f6-a7b8-9012-3456-7890abcdef12"]
        }
        ```

---

## Ações em Partidas

Endpoints que representam ações e modificam o estado de uma partida.

### Solicitar adesão a uma partida

-   **Method:** `POST`
-   **URL:** `/partidas/{partida_id}/solicitar-adesao`
-   **Corpo da Requisição:**
    ```json
    {
        "jogador_id": "d4e5f6a7-b8c9-0123-4567-890abcdef123"
    }
    ```
-   **Resposta (Sucesso):**
    -   **Status:** `200 OK`
    -   **Body:**
        ```json
        {
            "message": "Operação registrada."
        }
        ```

### Aprovar jogador em uma partida

-   **Method:** `POST`
-   **URL:** `/partidas/{partida_id}/aprovar-jogador`
-   **Corpo da Requisição:**
    ```json
    {
        "owner_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "jogador_id_aprovar": "c3d4e5f6-a7b8-9012-3456-7890abcdef12"
    }
    ```
-   **Resposta (Sucesso):**
    -   **Status:** `200 OK`
    -   **Body:**
        ```json
        {
            "id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
            "owner_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "status": "EM_ADESAO",
            "local_descricao": "Quadra de areia do Parque Central",
            "data_hora": "2025-10-15T20:00:00Z",
            "categoria": "INTERMEDIARIO",
            "tipo": "MISTA",
            "jogadores_confirmados": ["b2c3d4e5-f6a7-8901-2345-67890abcdef1", "c3d4e5f6-a7b8-9012-3456-7890abcdef12"],
            "jogadores_pendentes": []
        }
        ```

### Fechar adesão de uma partida

-   **Method:** `POST`
-   **URL:** `/partidas/{partida_id}/fechar-adesao`
-   **Resposta (Sucesso):**
    -   **Status:** `200 OK`
    -   **Body:**
        ```json
        {
            "id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
            "owner_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "status": "COMPLETA",
            "local_descricao": "Quadra de areia do Parque Central",
            "data_hora": "2025-10-15T20:00:00Z",
            "categoria": "INTERMEDIARIO",
            "tipo": "MISTA",
            "jogadores_confirmados": ["b2c3d4e5-f6a7-8901-2345-67890abcdef1", "c3d4e5f6-a7b8-9012-3456-7890abcdef12"],
            "jogadores_pendentes": []
        }
        ```

### Finalizar uma partida

-   **Method:** `POST`
-   **URL:** `/partidas/{partida_id}/finalizar`
-   **Resposta (Sucesso):**
    -   **Status:** `200 OK`
    -   **Body:**
        ```json
        {
            "id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
            "owner_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "status": "REALIZADA",
            "local_descricao": "Quadra de areia do Parque Central",
            "data_hora": "2025-10-15T20:00:00Z",
            "categoria": "INTERMEDIARIO",
            "tipo": "MISTA",
            "jogadores_confirmados": ["b2c3d4e5-f6a7-8901-2345-67890abcdef1", "c3d4e5f6-a7b8-9012-3456-7890abcdef12"],
            "jogadores_pendentes": []
        }
        ```

### Cancelar uma partida

-   **Method:** `POST`
-   **URL:** `/partidas/{partida_id}/cancelar`
-   **Resposta (Sucesso):**
    -   **Status:** `200 OK`
    -   **Body:**
        ```json
        {
            "id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
            "owner_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "status": "CANCELADA",
            "local_descricao": "Quadra de areia do Parque Central",
            "data_hora": "2025-10-15T20:00:00Z",
            "categoria": "INTERMEDIARIO",
            "tipo": "MISTA",
            "jogadores_confirmados": ["b2c3d4e5-f6a7-8901-2345-67890abcdef1", "c3d4e5f6-a7b8-9012-3456-7890abcdef12"],
            "jogadores_pendentes": []
        }
        ```
