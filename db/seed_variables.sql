INSERT OR IGNORE INTO variables
(code, name, curve, source_id, frequency_raw, frequency_used, stress_orientation, transformation_notes, confidence, phase, is_critical)
VALUES
('E1', 'VIX', 'E', NULL, 'daily', 'monthly', 'higher_is_stress', 'monthly average, monthly max, z-score, percentile stress', 'A', 'phase_1', 1),
('E2', 'TED spread', 'E', NULL, 'daily', 'monthly', 'higher_is_stress', 'monthly average, monthly max, z-score, percentile stress', 'A', 'phase_1', 1),
('E3', 'S&P 500 or MSCI World drawdown', 'E', NULL, 'daily/monthly', 'monthly', 'drawdown_is_stress', 'drawdown, z-score, percentile stress', 'A', 'phase_1', 0),
('E4', 'Real GDP US + Euro Area', 'E', NULL, 'quarterly', 'monthly_aligned', 'lower_growth_is_stress', 'quarterly value aligned to months, z-score, percentile stress', 'B', 'phase_1', 0),
('E5', 'Unemployment US + Euro Area', 'E', NULL, 'monthly', 'monthly', 'higher_is_stress', 'z-score, percentile stress', 'A', 'phase_1', 0),
('E6', 'Inflation US + Euro Area', 'E', NULL, 'monthly', 'monthly', 'extreme_deviation_is_stress', 'absolute deviation from target/regime, z-score, percentile stress', 'B', 'phase_1', 0),

('D1', 'ECB CISS', 'D', NULL, 'daily/weekly', 'monthly', 'higher_is_stress', 'monthly average, monthly max, z-score, percentile stress', 'A', 'phase_1', 1),
('D2', 'Euro area sovereign spreads versus Germany', 'D', NULL, 'daily/monthly', 'monthly', 'higher_is_stress', 'spread average and max, z-score, percentile stress', 'B', 'phase_1', 0),
('D3', 'Public intervention intensity', 'D', NULL, 'event', 'monthly', 'higher_is_stress', 'manual event score for TARP, QE, bailouts, EFSF, ESM, OMT', 'B', 'phase_2', 1),

('S1', 'Euro area youth unemployment', 'S', NULL, 'monthly', 'monthly', 'higher_is_stress', 'z-score, percentile stress', 'B', 'phase_3', 0),
('S2', 'Anti-austerity protests', 'S', NULL, 'event/monthly', 'monthly', 'higher_is_stress', 'manual or ACLED-style event count and intensity score', 'C', 'phase_3', 0),

('L1', 'Brent or WTI oil price', 'L', NULL, 'daily', 'monthly', 'extreme_move_is_stress', 'monthly average, monthly change, absolute shock percentile', 'A', 'phase_1', 0),
('L2', 'World trade volume', 'L', NULL, 'monthly/quarterly', 'monthly', 'contraction_is_stress', 'growth contraction, z-score, percentile stress', 'B', 'phase_1', 0),

('I1', 'Financial crisis / euro crisis media volume', 'I', NULL, 'daily', 'monthly', 'higher_is_stress', 'GDELT DOC query volume, z-score, percentile stress', 'C', 'phase_4', 0),
('I2', 'Media tone / crisis narrative negativity', 'I', NULL, 'daily', 'monthly', 'negative_tone_is_stress', 'GDELT tone or equivalent, z-score, percentile stress', 'C', 'phase_4', 0);
