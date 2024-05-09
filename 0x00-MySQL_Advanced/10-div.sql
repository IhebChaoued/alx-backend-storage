-- Create function SafeDiv
DELIMITER //

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT
BEGIN
    DECLARE result FLOAT;
    
    IF b = 0 THEN
        RETURN 0;
    ELSE
        SET result = a / b;
        RETURN result;
    END IF;
END //

DELIMITER ;
