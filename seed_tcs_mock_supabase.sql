-- =====================================================================
-- FILE: seed_tcs_mock_supabase.sql
-- PURPOSE: Self-healing & idempotent SQL script to seed 'TCS NQT Style Mock'
--          on Supabase PostgreSQL.
-- BEHAVIOR ON RERUN:
--   - If 'TCS NQT Style Mock' does not exist, it creates the test, 3 sections,
--     and all 30 verified questions (45 mins total, 15 mins per section).
--   - If 'TCS NQT Style Mock' ALREADY exists and has 0 student attempts, it safely
--     purges any outdated sections and questions and re-inserts the clean,
--     mathematically verified question set. No duplicates, no orphan rows.
--   - If attempts exist, it does NOT modify questions at all to protect attempt
--     integrity, and instructs the administrator to edit via the admin panel.
-- USAGE INSTRUCTIONS:
--   1. Open the Supabase Dashboard -> SQL Editor.
--   2. Paste this entire file into the editor and click 'Run'.
-- =====================================================================

DO $$
DECLARE
    v_test_id INTEGER;
    v_attempt_count INTEGER := 0;
    v_sec_num_id INTEGER;
    v_sec_verb_id INTEGER;
    v_sec_reas_id INTEGER;
BEGIN
    -- 1. Check if 'TCS NQT Style Mock' Test exists
    SELECT id INTO v_test_id FROM mock_test WHERE title = 'TCS NQT Style Mock' AND company_name = 'TCS';
    
    IF v_test_id IS NULL THEN
        INSERT INTO mock_test (company_name, title, description, duration_minutes, is_active, allow_multiple_attempts, created_at)
        VALUES (
            'TCS',
            'TCS NQT Style Mock',
            'Simulated TCS NQT placement examination featuring 3 core sections: Numerical Ability, Verbal Ability, and Reasoning Ability. Zero negative marking, single-attempt rule, and proctoring discipline monitoring.',
            45,
            TRUE,
            FALSE,
            NOW()
        ) RETURNING id INTO v_test_id;
        RAISE NOTICE 'Created test: TCS NQT Style Mock with ID %', v_test_id;
    ELSE
        SELECT COUNT(*) INTO v_attempt_count FROM mock_attempt WHERE test_id = v_test_id;
        IF v_attempt_count = 0 THEN
            RAISE NOTICE 'Found existing TCS NQT Style Mock (ID %) with 0 attempts. Purging outdated questions and sections for clean update...', v_test_id;
            DELETE FROM mock_question WHERE section_id IN (SELECT id FROM mock_section WHERE test_id = v_test_id);
            DELETE FROM mock_section WHERE test_id = v_test_id;
        ELSE
            RAISE NOTICE 'TCS NQT Style Mock (ID %) has % attempt(s). Existing sections and questions were NOT modified to preserve attempt history. Please edit questions via the QuizCraft Admin Panel.', v_test_id, v_attempt_count;
            RETURN;
        END IF;
    END IF;

    -- Update test metadata
    UPDATE mock_test
    SET description = 'Simulated TCS NQT placement examination featuring 3 core sections: Numerical Ability, Verbal Ability, and Reasoning Ability. Zero negative marking, single-attempt rule, and proctoring discipline monitoring.',
        duration_minutes = 45,
        is_active = TRUE,
        allow_multiple_attempts = FALSE
    WHERE id = v_test_id;

    -- 2.1. Section: Numerical Ability
    SELECT id INTO v_sec_num_id FROM mock_section WHERE test_id = v_test_id AND name = 'Numerical Ability';
    IF v_sec_num_id IS NULL THEN
        INSERT INTO mock_section (test_id, name, "order", num_questions, section_minutes, created_at)
        VALUES (v_test_id, 'Numerical Ability', 1, 10, 15, NOW())
        RETURNING id INTO v_sec_num_id;
        RAISE NOTICE 'Created section: Numerical Ability with ID %', v_sec_num_id;
    ELSE
        UPDATE mock_section
        SET "order" = 1, num_questions = 10, section_minutes = 15
        WHERE id = v_sec_num_id;
        RAISE NOTICE 'Updated section: Numerical Ability (ID %)', v_sec_num_id;
    END IF;

    -- Numerical Ability Question 1
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_num_id, 'A retailer marks the price of an article 25% above its cost price of ₹4,000. If he sells it after offering a 12% discount on the marked price, what is his profit in rupees?', '₹360', '₹400', '₹440', '₹480', 2, 'Marked Price = ₹4,000 × 1.25 = ₹5,000. Selling Price = ₹5,000 × (1 - 0.12) = ₹5,000 × 0.88 = ₹4,400. Profit = Selling Price - Cost Price = ₹4,400 - ₹4,000 = ₹400.', 1, NOW());

    -- Numerical Ability Question 2
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_num_id, 'Pipe A can fill a tank in 12 hours, and Pipe B can fill it in 15 hours. A drainage Pipe C can empty the full tank in 20 hours. If all three pipes are opened simultaneously into an empty tank, how many hours will it take to fill the tank completely?', '8 hours', '10 hours', '12 hours', '15 hours', 2, 'In 1 hour, portion of the tank filled = (1/12) + (1/15) - (1/20) = (5 + 4 - 3)/60 = 6/60 = 1/10. Therefore, the time required to fill the tank completely = 1 / (1/10) = 10 hours.', 1, NOW());

    -- Numerical Ability Question 3
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_num_id, 'A train traveling at a constant speed of 72 km/h crosses a 280-meter long tunnel in 24 seconds. What is the length of the train in meters?', '180 m', '200 m', '220 m', '240 m', 2, 'Speed in m/s = 72 × (5/18) = 20 m/s. Total distance traveled in 24 seconds = 20 m/s × 24 s = 480 meters. Since Total distance = Train length + Tunnel length, Train length = 480 m - 280 m = 200 meters.', 1, NOW());

    -- Numerical Ability Question 4
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_num_id, 'A vessel contains 60 liters of a mixture of milk and water in the ratio 3 : 2. How many liters of water must be added to the mixture so that the ratio of milk to water becomes 1 : 1?', '8 liters', '10 liters', '12 liters', '15 liters', 3, 'Initial milk = 60 × (3 / 5) = 36 liters; initial water = 60 × (2 / 5) = 24 liters. To achieve a 1 : 1 ratio, the quantity of water must equal the quantity of milk (36 liters). Water to be added = 36 - 24 = 12 liters.', 1, NOW());

    -- Numerical Ability Question 5
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_num_id, 'A sum of ₹8,000 is invested at an annual interest rate of 10% compounded annually. What is the compound interest earned at the end of 2 years?', '₹1,600', '₹1,680', '₹1,720', '₹1,800', 2, 'Amount = P(1 + R/100)^T = 8000 × (1 + 10/100)^2 = 8000 × (1.10)^2 = 8000 × 1.21 = ₹9,680. Compound Interest = Amount - Principal = 9,680 - 8,000 = ₹1,680.', 1, NOW());

    -- Numerical Ability Question 6
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_num_id, 'The average age of a group of 6 colleagues is 35 years. When one member leaves and is replaced by a new colleague aged 28 years, the average age of the group becomes 33 years. What was the age of the colleague who left?', '36 years', '38 years', '40 years', '42 years', 3, 'Initial total age of the 6 colleagues = 6 × 35 = 210 years. New total age after replacement = 6 × 33 = 198 years. Let X be the age of the colleague who left. Then: 210 - X + 28 = 198 => 238 - X = 198 => X = 238 - 198 = 40 years.', 1, NOW());

    -- Numerical Ability Question 7
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_num_id, 'Find the least number which when divided by 12, 15, and 20 leaves a remainder of 7 in each case.', '57', '67', '77', '127', 2, 'The required least number is LCM(12, 15, 20) + Remainder. LCM(12, 15, 20) = 60. Therefore, the least number = 60 + 7 = 67.', 1, NOW());

    -- Numerical Ability Question 8
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_num_id, 'A box contains 5 red balls, 4 blue balls, and 3 green balls. If two balls are drawn at random one after another without replacement, what is the probability that both balls are blue?', '1/11', '1/12', '2/33', '3/22', 1, 'Total number of balls = 5 + 4 + 3 = 12. Probability of first ball being blue = 4 / 12 = 1 / 3. Remaining blue balls = 3; remaining total balls = 11. Probability of second ball being blue = 3 / 11. Combined probability = (4 / 12) × (3 / 11) = 12 / 132 = 1 / 11.', 1, NOW());

    -- Numerical Ability Question 9
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_num_id, 'In a right-angled triangle, the hypotenuse measures 25 cm and the base measures 24 cm. What is the area of the triangle in square centimeters?', '72 sq.cm', '84 sq.cm', '96 sq.cm', '168 sq.cm', 2, 'By Pythagoras theorem, Height = √(Hypotenuse² - Base²) = √(25² - 24²) = √(625 - 576) = √49 = 7 cm. Area = (1/2) × Base × Height = (1/2) × 24 cm × 7 cm = 12 × 7 = 84 sq.cm.', 1, NOW());

    -- Numerical Ability Question 10
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_num_id, 'If 2x + 3y = 23 and 3x + 2y = 27, what is the value of (x + y)?', '8', '9', '10', '11', 3, 'Adding the two equations directly: (2x + 3y) + (3x + 2y) = 23 + 27 => 5x + 5y = 50 => 5(x + y) = 50 => x + y = 10. (Alternatively, solving gives x = 7 and y = 3, so x + y = 10).', 1, NOW());

    -- 2.2. Section: Verbal Ability
    SELECT id INTO v_sec_verb_id FROM mock_section WHERE test_id = v_test_id AND name = 'Verbal Ability';
    IF v_sec_verb_id IS NULL THEN
        INSERT INTO mock_section (test_id, name, "order", num_questions, section_minutes, created_at)
        VALUES (v_test_id, 'Verbal Ability', 2, 10, 15, NOW())
        RETURNING id INTO v_sec_verb_id;
        RAISE NOTICE 'Created section: Verbal Ability with ID %', v_sec_verb_id;
    ELSE
        UPDATE mock_section
        SET "order" = 2, num_questions = 10, section_minutes = 15
        WHERE id = v_sec_verb_id;
        RAISE NOTICE 'Updated section: Verbal Ability (ID %)', v_sec_verb_id;
    END IF;

    -- Verbal Ability Question 1
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_verb_id, 'Choose the word most nearly SIMILAR in meaning (SYNONYM) to ''TRANSPARENT'' as used in the sentence: ''The auditor found that the company''''s financial records were completely transparent, leaving no room for suspicion.''', 'Ambiguous', 'Clear', 'Complex', 'Deceptive', 2, '''Transparent'' in this context means easily understood, clear, and free from deceit or concealment. ''Clear'' is the exact synonym.', 1, NOW());

    -- Verbal Ability Question 2
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_verb_id, 'Select the word OPPOSITE in meaning (ANTONYM) to ''FRUGAL'' as used in the sentence: ''Her frugal lifestyle allowed her to save a significant portion of her monthly salary.''', 'Thrifty', 'Extravagant', 'Economical', 'Prudent', 2, '''Frugal'' means careful and economical in spending resources. Its direct opposite is ''Extravagant'' (spending money wastefully or excessively).', 1, NOW());

    -- Verbal Ability Question 3
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_verb_id, 'Choose the grammatically correct sentence from the options below:', 'Neither the manager nor the employees was present at the safety briefing.', 'Neither the manager nor the employees were present at the safety briefing.', 'Neither the manager nor the employees is present at the safety briefing.', 'Neither the manager nor the employees has been present at the safety briefing.', 2, 'When two subjects are connected by ''neither... nor'', the verb must agree with the closer subject. Here, ''employees'' is plural, requiring the plural verb ''were''.', 1, NOW());

    -- Verbal Ability Question 4
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_verb_id, 'Identify the sentence that does NOT contain a misplaced or dangling modifier:', 'Walking through the park, the fallen leaves covered the path.', 'Having completed the project, the report was submitted by the analyst.', 'Having completed the project, the analyst submitted the report.', 'Running for the train, his wallet fell from his pocket.', 3, 'In option 3, the introductory participle phrase ''Having completed the project'' correctly modifies the agent who did the action (''the analyst''). In options 1, 2, and 4, the participle incorrectly modifies ''the leaves'', ''the report'', and ''his wallet''.', 1, NOW());

    -- Verbal Ability Question 5
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_verb_id, 'Select the appropriate preposition to complete the sentence: ''She is very fond ______ classical music.''', 'of', 'about', 'with', 'for', 1, 'The adjective ''fond'' is strictly followed by the preposition ''of'' (''to be fond of something''). ''About'', ''with'', and ''for'' are grammatically incorrect in this context.', 1, NOW());

    -- Verbal Ability Question 6
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_verb_id, 'What is the true meaning of the idiom ''to burn the midnight oil''?', 'To waste fuel or resources carelessly', 'To work or study late into the night', 'To cause accidental damage by negligence', 'To wake up earlier than usual', 2, '''To burn the midnight oil'' is an established English idiom meaning to stay up working or studying late into the night.', 1, NOW());

    -- Verbal Ability Question 7
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_verb_id, 'Read the sentence and find which part contains a grammatical error: ''Despite of (A) / all his preparations, (B) / he could not qualify (C) / for the final round. (D)''', 'Despite of (A)', 'all his preparations (B)', 'he could not qualify (C)', 'for the final round (D)', 1, '''Despite'' is a preposition that never takes ''of''. The correct phrase is either ''Despite all his preparations'' or ''In spite of all his preparations''.', 1, NOW());

    -- Verbal Ability Question 8
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_verb_id, 'Arrange the sentences into a coherent paragraph:
P: This real-time analysis helps prevent potential fraudulent transactions.
Q: Banks process millions of digital payment requests every second.
R: Advanced machine learning algorithms immediately scan each transaction for suspicious patterns.
S: These high transaction volumes demand automated security mechanisms.', 'Q-S-R-P', 'Q-P-S-R', 'S-Q-P-R', 'P-Q-S-R', 1, 'Q introduces the premise (millions of payments). S links the volume to need for automated security. R specifies the mechanism (machine learning algorithms scan transactions). P concludes with the outcome (preventing fraudulent transactions). The logical flow is Q-S-R-P.', 1, NOW());

    -- Verbal Ability Question 9
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_verb_id, 'Which option represents the correct passive transformation of: ''The committee approved the revised proposal yesterday.''', 'The revised proposal was approved by the committee yesterday.', 'The revised proposal has been approved by the committee yesterday.', 'The revised proposal had been approved by the committee yesterday.', 'The revised proposal is approved by the committee yesterday.', 1, 'The active sentence is in Simple Past (''approved''). The passive rule for Simple Past is ''was/were + past participle'' (''was approved'').', 1, NOW());

    -- Verbal Ability Question 10
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_verb_id, 'Read the passage: ''Renewable energy adoption has accelerated significantly over the past decade. However, the intermittent nature of solar and wind energy means that grid reliability still requires either substantial battery storage infrastructure or backup generation capacity.'' What can be directly inferred from the passage?', 'Solar and wind energy are unsuitable for modern power grids.', 'Renewable energy sources alone cannot guarantee uninterrupted grid power without energy storage or backup systems.', 'Battery storage systems are cheaper than conventional backup power plants.', 'Global energy demand has declined as a result of renewable energy adoption.', 2, 'The passage directly explains that due to intermittent generation, grid reliability cannot be maintained without storage or backup, directly supporting Option 2.', 1, NOW());

    -- 2.3. Section: Reasoning Ability
    SELECT id INTO v_sec_reas_id FROM mock_section WHERE test_id = v_test_id AND name = 'Reasoning Ability';
    IF v_sec_reas_id IS NULL THEN
        INSERT INTO mock_section (test_id, name, "order", num_questions, section_minutes, created_at)
        VALUES (v_test_id, 'Reasoning Ability', 3, 10, 15, NOW())
        RETURNING id INTO v_sec_reas_id;
        RAISE NOTICE 'Created section: Reasoning Ability with ID %', v_sec_reas_id;
    ELSE
        UPDATE mock_section
        SET "order" = 3, num_questions = 10, section_minutes = 15
        WHERE id = v_sec_reas_id;
        RAISE NOTICE 'Updated section: Reasoning Ability (ID %)', v_sec_reas_id;
    END IF;

    -- Reasoning Ability Question 1
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_reas_id, 'What is the next number in the geometric series: 7, 14, 28, 56, 112, ___?', '168', '196', '224', '248', 3, 'Each term is obtained by multiplying the preceding term by 2: 7×2=14, 14×2=28, 28×2=56, 56×2=112, 112×2=224.', 1, NOW());

    -- Reasoning Ability Question 2
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_reas_id, 'In a certain code language, if ''CLOUD'' is coded as ''DMPVE'', how will ''TIGER'' be coded in that same language?', 'UJHFS', 'VKIGT', 'UJGES', 'TIGFS', 1, 'Each letter is shifted forward by 1 position in the alphabet (+1 shift): T(+1)→U, I(+1)→J, G(+1)→H, E(+1)→F, R(+1)→S. Hence, ''TIGER'' becomes ''UJHFS''.', 1, NOW());

    -- Reasoning Ability Question 3
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_reas_id, 'Pointing to a photograph of a boy, Suresh said: ''He is the only son of my father''''s only son.'' How is the boy related to Suresh?', 'Brother', 'Son', 'Nephew', 'Uncle', 2, 'Suresh is a male speaker. ''My father''''s only son'' refers to Suresh himself. The statement therefore means: ''He is the only son of Suresh.'' Thus, the boy is Suresh''''s son.', 1, NOW());

    -- Reasoning Ability Question 4
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_reas_id, 'Ankit starts from point P and walks 20 meters North. He turns right and walks 15 meters, then turns right again and walks 20 meters. Finally, he turns left and walks 10 meters to reach point Q. In which direction and at what straight-line distance is point Q from point P?', '25 meters East', '25 meters West', '35 meters East', '15 meters North', 1, 'Vertical displacement = +20 m (North) - 20 m (South) = 0 m. Horizontal displacement = +15 m (East) + 10 m (East) = +25 meters East. Point Q is 25 meters due East of point P.', 1, NOW());

    -- Reasoning Ability Question 5
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_reas_id, 'Statements:
I. All roses are flowers.
II. All flowers are plants.
Conclusions:
1. All roses are plants.
2. Some plants are roses.
Which conclusion(s) logically follow?', 'Only conclusion 1 follows', 'Only conclusion 2 follows', 'Neither conclusion 1 nor 2 follows', 'Both conclusions 1 and 2 follow', 4, 'Roses ⊆ Flowers ⊆ Plants. Transitivity implies Roses ⊆ Plants, so Conclusion 1 definitely follows. Since the set of roses is non-empty, Plants ∩ Roses is non-empty, so Conclusion 2 (''Some plants are roses'') also definitely follows. Hence, both follow.', 1, NOW());

    -- Reasoning Ability Question 6
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_reas_id, 'In a row of 40 students facing North, Priya is 15th from the left end. What is Priya''''s position from the right end of the row?', '24th', '25th', '26th', '27th', 3, 'Position from Right = Total Students - Position from Left + 1 = 40 - 15 + 1 = 26th.', 1, NOW());

    -- Reasoning Ability Question 7
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_reas_id, 'Select the pair that expresses a relationship most similar to that expressed in the original pair:
AUTHOR : BOOK :: ?', 'DOCTOR : MEDICINE', 'COMPOSER : SYMPHONY', 'ACTOR : THEATER', 'TEACHER : CLASSROOM', 2, 'An author creates a book (Creator : Intellectual Creation). Similarly, a composer creates a symphony. A doctor does not create medicine, an actor performs in a theater, and a teacher teaches in a classroom.', 1, NOW());

    -- Reasoning Ability Question 8
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_reas_id, 'Four letter-clusters are given below. Three are alike in a certain manner and one is different. Select the odd one out:', 'CEG', 'KMO', 'PRT', 'UWZ', 4, 'In CEG (C+2=E, E+2=G), KMO (K+2=M, M+2=O), and PRT (P+2=R, R+2=T), the consecutive letters have an alphabet difference of +2. In UWZ, U+2=W, but W+3=Z. Therefore, UWZ is the odd one out.', 1, NOW());

    -- Reasoning Ability Question 9
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_reas_id, 'At 4:20, what is the acute angle between the hour hand and the minute hand of an analog clock?', '0°', '10°', '15°', '20°', 2, 'Hour hand angle from 12:00 = 4 × 30° + 20 × 0.5° = 120° + 10° = 130°. Minute hand angle from 12:00 = 20 × 6° = 120°. The angle between them = |130° - 120°| = 10°.', 1, NOW());

    -- Reasoning Ability Question 10
    INSERT INTO mock_question (section_id, text, option1, option2, option3, option4, correct_option, explanation, marks, created_at)
    VALUES (v_sec_reas_id, 'Five friends—A, B, C, D, and E—are seated in a row facing North.
1. C sits in the exact middle of the row.
2. A sits immediately to the left of C.
3. B sits at the extreme right end.
4. E sits immediately to the left of B.
Who is sitting at the extreme left end of the row?', 'A', 'B', 'D', 'E', 3, 'Row positions 1 to 5 from left to right: Condition 1 places C at position 3. Condition 2 places A at position 2 (immediate left of C). Condition 3 places B at position 5 (extreme right). Condition 4 places E at position 4 (immediate left of B). The only remaining person D must sit at position 1 (extreme left end).', 1, NOW());

    RAISE NOTICE 'Successfully seeded all 30 questions for TCS NQT Style Mock.';
END $$;