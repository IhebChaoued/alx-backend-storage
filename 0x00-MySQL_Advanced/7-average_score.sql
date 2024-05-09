-- Create stored procedure ComputeAverageScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE v_avg_score DECIMAL(10, 2);
    
    SELECT AVG(score) INTO v_avg_score
    FROM corrections
    WHERE user_id = p_user_id;
    
    UPDATE users
    SET average_score = v_avg_score
    WHERE id = p_user_id;
END //

DELIMITER ;
