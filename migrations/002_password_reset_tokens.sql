-- Migração 002: tabela para armazenar tokens de redefinição de senha.
--
-- Motivo: os tokens ficavam em um dicionário Python em memória, o que causava
-- dois problemas:
--   1. Tokens perdidos ao reiniciar o servidor ou com múltiplos workers.
--   2. Acúmulo ilimitado de tokens expirados sem limpeza automática.
--
-- Com esta tabela:
--   - Os tokens sobrevivem a reinicializações do processo.
--   - O evento MySQL apaga automaticamente os registros expirados a cada hora.
--   - Um único token ativo por usuário é garantido pela constraint UNIQUE em usuario_id.

USE anime_mania;

CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id          BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT,
    usuario_id  BIGINT UNSIGNED  NOT NULL,
    token       VARCHAR(128)     NOT NULL,
    expira_em   DATETIME         NOT NULL,
    criado_em   TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    -- Garante que cada token seja único na tabela.
    UNIQUE KEY uq_prt_token (token),
    -- Garante que cada usuário tenha no máximo um token ativo por vez.
    -- Ao solicitar um novo link, o INSERT ON DUPLICATE KEY UPDATE sobrescreve o anterior.
    UNIQUE KEY uq_prt_usuario (usuario_id),
    CONSTRAINT fk_prt_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Evento agendado que remove tokens expirados a cada hora.
-- Evita que a tabela cresça infinitamente com registros velhos.
-- Requer que o MySQL Event Scheduler esteja ativo (padrão na maioria das instalações).
CREATE EVENT IF NOT EXISTS evt_limpar_tokens_expirados
    ON SCHEDULE EVERY 1 HOUR
    DO
        DELETE FROM password_reset_tokens WHERE expira_em < NOW();
