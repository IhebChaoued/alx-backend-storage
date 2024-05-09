-- index idx_name_first_score: name column and score column
CREATE INDEX idx_name_first_score ON names (name(1)), score);
