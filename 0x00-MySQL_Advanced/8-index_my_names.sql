-- Create index idx_name_first on the first letter of name column
CREATE INDEX idx_name_first ON names (LEFT(name, 1));
