-- schema.sql
-- Ce script crée la table de référence pour toutes les tables hebdomadaires.
-- Exécutez ce code une seule fois directement dans votre base de données.

CREATE TABLE IF NOT EXISTS portfolio_template (
    ticker VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255),
    shares DECIMAL(18, 4),
    price DECIMAL(18, 4),
    purchase_price DECIMAL(18, 4),
    holding_value DECIMAL(18, 4),
    holding_gain_change_pct DECIMAL(10, 2),
    six_month_return_pct DECIMAL(10, 2),
    ytd_return_pct DECIMAL(10, 2),
    one_year_return_pct DECIMAL(10, 2),
    portfolio_pct DECIMAL(10, 2),
    industry VARCHAR(255),
    p_e_ratio VARCHAR(20), -- Modifié pour accepter des valeurs non numériques
    currency VARCHAR(3),
    holding_value_cad DECIMAL(18, 4),
    highest_price_target DECIMAL(18, 4),
    lowest_price_target DECIMAL(18, 4)
);