CREATE DATABASE IF NOT EXISTS anime_mania
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE anime_mania;

CREATE TABLE IF NOT EXISTS usuarios (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    email VARCHAR(254) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    papel ENUM('usuario', 'admin') NOT NULL DEFAULT 'usuario',
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id),
    UNIQUE KEY uq_usuarios_email (email),
    KEY idx_usuarios_papel_ativo (papel, ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS categorias (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome VARCHAR(80) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_categorias_nome (nome),
    UNIQUE KEY uq_categorias_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS publicacoes (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    categoria_id BIGINT UNSIGNED NOT NULL,
    autor_id BIGINT UNSIGNED NULL,
    titulo VARCHAR(200) NOT NULL,
    slug VARCHAR(191) NOT NULL,
    resumo VARCHAR(500) NOT NULL,
    conteudo MEDIUMTEXT NOT NULL,
    imagem_capa VARCHAR(500) NULL,
    status ENUM('rascunho', 'publicada') NOT NULL DEFAULT 'rascunho',
    publicado_em DATETIME NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_publicacoes_slug (slug),
    KEY idx_publicacoes_categoria (categoria_id),
    KEY idx_publicacoes_autor (autor_id),
    KEY idx_publicacoes_status_data (status, publicado_em),
    CONSTRAINT fk_publicacoes_categoria
        FOREIGN KEY (categoria_id) REFERENCES categorias (id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_publicacoes_autor
        FOREIGN KEY (autor_id) REFERENCES usuarios (id)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
