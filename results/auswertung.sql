
SELECT
       (SELECT COUNT(*) FROM marks) as "total_marks",
       (SELECT COUNT(*) FROM marks WHERE was_correct = TRUE) as "total_marks_was_correct",
       (SELECT COUNT(*) FROM marks WHERE was_correct = FALSE) as "total_marks_was_incorrect",

       (SELECT COUNT(*) FROM marks WHERE ntbg = TRUE) as "total_marks_ntbg",
       (SELECT COUNT(*) FROM marks WHERE ntbg = TRUE AND was_correct = TRUE) as "total_marks_ntbg_correct",
       (SELECT COUNT(*) FROM marks WHERE ntbg = TRUE AND was_correct = FALSE) as "total_marks_ntbg_incorrect",

       (SELECT COUNT(*) FROM marks WHERE ntbg = FALSE) as "total_marks_not_ntbg",
       (SELECT COUNT(*) FROM marks WHERE ntbg = FALSE AND was_correct = TRUE) as "total_marks_not_ntbg_correct",
       (SELECT COUNT(*) FROM marks WHERE ntbg = FALSE AND was_correct = FALSE) as "total_marks_not_ntbg_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE) as "total_marks_without_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND was_correct = TRUE) as "total_marks_without_trivial_was_correct",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND was_correct = FALSE) as "total_marks_without_trivial_was_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND ntbg = TRUE) as "total_marks_without_trivial_ntbg",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND ntbg = TRUE AND was_correct = TRUE) as "total_marks_without_trivial_ntbg_correct",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND ntbg = TRUE AND was_correct = FALSE) as "total_marks_without_trivial_ntbg_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND ntbg = FALSE) as "total_marks_without_trivial_not_ntbg",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND ntbg = FALSE AND was_correct = TRUE) as "total_marks_without_trivial_not_ntbg_correct",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND ntbg = FALSE AND was_correct = FALSE) as "total_marks_without_trivial_not_ntbg_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE) as "total_marks_nouns",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND was_correct = TRUE) as "total_marks_nouns_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND was_correct = FALSE) as "total_marks_nouns_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE) as "total_marks_ntbg_nouns",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE AND was_correct = TRUE) as "total_marks_ntbg_nouns_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE AND was_correct = FALSE) as "total_marks_ntbg_nouns_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE) as "total_marks_not_ntbg_nouns",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE AND was_correct = TRUE) as "total_marks_not_ntbg_nouns_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE AND was_correct = FALSE) as "total_marks_not_ntbg_nouns_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND is_trivial = FALSE) as "total_marks_nouns_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND was_correct = TRUE AND is_trivial = FALSE) as "total_marks_nouns_correct_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND was_correct = FALSE AND is_trivial = FALSE) as "total_marks_nouns_incorrect_not_trivial",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE AND is_trivial = FALSE) as "total_marks_ntbg_nouns_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE AND was_correct = TRUE AND is_trivial = FALSE) as "total_marks_ntbg_nouns_correct_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE AND was_correct = FALSE AND is_trivial = FALSE) as "total_marks_ntbg_nouns_incorrect_not_trivial",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE AND is_trivial = FALSE) as "total_marks_not_ntbg_nouns_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE AND was_correct = TRUE AND is_trivial = FALSE) as "total_marks_not_ntbg_nouns_correct_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE AND was_correct = FALSE AND is_trivial = FALSE) as "total_marks_not_ntbg_nouns_incorrect_not_trivial",

       (SELECT COUNT(*) FROM marks WHERE is_noun = FALSE) as "total_marks_pronouns",
       (SELECT COUNT(*) FROM marks WHERE is_noun = FALSE AND was_correct = TRUE) as "total_marks_pronouns_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = FALSE AND was_correct = FALSE) as "total_marks_pronouns_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = FALSE AND ntbg = TRUE) as "total_marks_ntbg_pronouns",
       (SELECT COUNT(*) FROM marks WHERE is_noun = FALSE AND ntbg = TRUE AND was_correct = TRUE) as "total_marks_ntbg_pronouns_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = FALSE AND ntbg = TRUE AND was_correct = FALSE) as "total_marks_ntbg_pronouns_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = FALSE AND ntbg = FALSE) as "total_marks_not_ntbg_pronouns",
       (SELECT COUNT(*) FROM marks WHERE is_noun = FALSE AND ntbg = FALSE AND was_correct = TRUE) as "total_marks_not_ntbg_pronouns_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = FALSE AND ntbg = FALSE AND was_correct = FALSE) as "total_marks_not_ntbg_pronouns_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND is_singular = 'y') as "total_marks_nouns_singular",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND is_singular = 'y' AND was_correct = TRUE) as "total_marks_nouns_singular_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND is_singular = 'y' AND was_correct = FALSE) as "total_marks_nouns_singular_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE AND is_singular = 'y') as "total_marks_nouns_ntbg_singular",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE AND is_singular = 'y' AND was_correct = TRUE) as "total_marks_nouns_ntbg_singular_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE AND is_singular = 'y' AND was_correct = FALSE) as "total_marks_nouns_ntbg_singular_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE AND is_singular = 'y') as "total_marks_nouns_not_ntbg_singular",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE AND is_singular = 'y' AND was_correct = TRUE) as "total_marks_nouns_not_ntbg_singular_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE AND is_singular = 'y' AND was_correct = FALSE) as "total_marks_nouns_not_ntbg_singular_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND is_singular = '?') as "total_marks_nouns_?",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND is_singular = '?' AND was_correct = TRUE) as "total_marks_nouns_?_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND is_singular = '?' AND was_correct = FALSE) as "total_marks_nouns_?_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE AND is_singular = '?') as "total_marks_ntbg_nouns_?",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE AND is_singular = '?' AND was_correct = TRUE) as "total_marks_ntbg_nouns_?_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE AND is_singular = '?' AND was_correct = FALSE) as "total_marks_ntbg_nouns_?_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE AND is_singular = '?') as "total_marks_not_ntbg_nouns_?",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE AND is_singular = '?' AND was_correct = TRUE) as "total_marks_not_ntbg_nouns_?_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE AND is_singular = '?' AND was_correct = FALSE) as "total_marks_not_ntbg_nouns_?_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND is_singular = 'n') as "total_marks_nouns_plural",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND is_singular = 'n' AND was_correct = TRUE) as "total_marks_nouns_plural_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND is_singular = 'n' AND was_correct = FALSE) as "total_marks_nouns_plural_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE AND is_singular = 'n') as "total_marks_ntbg_nouns_plural",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE AND is_singular = 'n' AND was_correct = TRUE) as "total_marks_ntbg_nouns_plural_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = TRUE AND is_singular = 'n' AND was_correct = FALSE) as "total_marks_ntbg_nouns_plural_incorrect",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE AND is_singular = 'n') as "total_marks_not_ntbg_nouns_plural",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE AND is_singular = 'n' AND was_correct = TRUE) as "total_marks_not_ntbg_nouns_plural_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ntbg = FALSE AND is_singular = 'n' AND was_correct = FALSE) as "total_marks_not_ntbg_nouns_plural_incorrect",


       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND is_singular = 'y') as "total_marks_nouns_singular_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND is_singular = 'y' AND was_correct = TRUE) as "total_marks_nouns_singular_correct_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND is_singular = 'y' AND was_correct = FALSE) as "total_marks_nouns_singular_incorrect_not_trivial",

       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = TRUE AND is_singular = 'y') as "total_marks_nouns_ntbg_singular_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = TRUE AND is_singular = 'y' AND was_correct = TRUE) as "total_marks_nouns_ntbg_singular_correct_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = TRUE AND is_singular = 'y' AND was_correct = FALSE) as "total_marks_nouns_ntbg_singular_incorrect_not_trivial",

       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = FALSE AND is_singular = 'y') as "total_marks_nouns_not_ntbg_singular_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = FALSE AND is_singular = 'y' AND was_correct = TRUE) as "total_marks_nouns_not_ntbg_singular_correct_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = FALSE AND is_singular = 'y' AND was_correct = FALSE) as "total_marks_nouns_not_ntbg_singular_incorrect_not_trivial",

       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND is_singular = '?') as "total_marks_nouns_?_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND is_singular = '?' AND was_correct = TRUE) as "total_marks_nouns_?_correct_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND is_singular = '?' AND was_correct = FALSE) as "total_marks_nouns_?_incorrect_not_trivial",

       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = TRUE AND is_singular = '?') as "total_marks_ntbg_nouns_?_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = TRUE AND is_singular = '?' AND was_correct = TRUE) as "total_marks_ntbg_nouns_?_correct_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = TRUE AND is_singular = '?' AND was_correct = FALSE) as "total_marks_ntbg_nouns_?_incorrect_not_trivial",

       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = FALSE AND is_singular = '?') as "total_marks_not_ntbg_nouns_?_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = FALSE AND is_singular = '?' AND was_correct = TRUE) as "total_marks_not_ntbg_nouns_?_correct_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = FALSE AND is_singular = '?' AND was_correct = FALSE) as "total_marks_not_ntbg_nouns_?_incorrect_not_trivial",

       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND is_singular = 'n') as "total_marks_nouns_plural_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND is_singular = 'n' AND was_correct = TRUE) as "total_marks_nouns_plural_correct_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND is_singular = 'n' AND was_correct = FALSE) as "total_marks_nouns_plural_incorrect_not_trivial",

       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = TRUE AND is_singular = 'n') as "total_marks_ntbg_nouns_plural_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = TRUE AND is_singular = 'n' AND was_correct = TRUE) as "total_marks_ntbg_nouns_plural_correct_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = TRUE AND is_singular = 'n' AND was_correct = FALSE) as "total_marks_ntbg_nouns_plural_incorrect_not_trivial",

       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = FALSE AND is_singular = 'n') as "total_marks_not_ntbg_nouns_plural_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = FALSE AND is_singular = 'n' AND was_correct = TRUE) as "total_marks_not_ntbg_nouns_plural_correct_not_trivial",
       (SELECT COUNT(*) FROM marks WHERE is_trivial = FALSE AND is_noun = TRUE AND ntbg = FALSE AND is_singular = 'n' AND was_correct = FALSE) as "total_marks_not_ntbg_nouns_plural_incorrec_not_trivialt",

       (SELECT COUNT(*) FROM marks WHERE (ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE)) "need_to_be_corrected",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'B' WHERE ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'T' WHERE ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_partially_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'F' WHERE ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_incorrect",
       (SELECT COUNT(*) FROM marks WHERE (SELECT COUNT(*) FROM corrections WHERE uniq_id = uniqid) = 0 AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_not_marked",

       (SELECT COUNT(*) FROM marks WHERE is_noun = FALSE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_pronouns",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'B' WHERE is_noun = FALSE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_pronouns_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'T' WHERE is_noun = FALSE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_pronouns_partially_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'F' WHERE is_noun = FALSE AND((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_pronouns_incorrect",
       (SELECT COUNT(*) FROM marks WHERE is_noun = FALSE AND (SELECT COUNT(*) FROM corrections WHERE uniq_id = uniqid) = 0 AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_pronouns_not_marked",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'B' WHERE is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'T' WHERE is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_partially_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'F' WHERE is_noun = TRUE AND((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_incorrect",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND (SELECT COUNT(*) FROM corrections WHERE uniq_id = uniqid) = 0 AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_not_marked",

       (SELECT COUNT(*) FROM marks WHERE is_singular = 'n' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_plural",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'B' WHERE is_singular = 'n' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_correct_plural",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'T' WHERE is_singular = 'n' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_partially_correct_plural",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'F' WHERE is_singular = 'n' AND is_noun = TRUE AND((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_incorrect_plural",
       (SELECT COUNT(*) FROM marks WHERE is_singular = 'n' AND is_noun = TRUE AND (SELECT COUNT(*) FROM corrections WHERE uniq_id = uniqid) = 0 AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_not_marked_plural",

       (SELECT COUNT(*) FROM marks WHERE is_singular = '?' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_unknown",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'B' WHERE is_singular = '?' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_correct_unknown",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'T' WHERE is_singular = '?' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_partially_correct_unknown",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'F' WHERE is_singular = '?' AND is_noun = TRUE AND((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_incorrect_unknown",
       (SELECT COUNT(*) FROM marks WHERE is_singular = '?' AND is_noun = TRUE AND (SELECT COUNT(*) FROM corrections WHERE uniq_id = uniqid) = 0 AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_not_marked_unknown",

       (SELECT COUNT(*) FROM marks WHERE is_singular = 'y' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_sing",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'B' WHERE is_singular = 'y' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_correct_sing",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'T' WHERE is_singular = 'y' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_partially_correct_sing",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'F' WHERE is_singular = 'y' AND is_noun = TRUE AND((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_incorrect_sing",
       (SELECT COUNT(*) FROM marks WHERE is_singular = 'y' AND is_noun = TRUE AND (SELECT COUNT(*) FROM corrections WHERE uniq_id = uniqid) = 0 AND ((ntbg = TRUE AND was_correct = TRUE) OR (ntbg = FALSE AND was_correct = FALSE))) "need_to_be_corrected_nouns_not_marked_sing",

       (SELECT COUNT(*) FROM marks WHERE (ntbg = TRUE AND was_correct = TRUE)) "need_to_be_corrected_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'B' WHERE ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_correct_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'T' WHERE ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_partially_correct_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'F' WHERE ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_incorrect_only_correct",
       (SELECT COUNT(*) FROM marks WHERE (SELECT COUNT(*) FROM corrections WHERE uniq_id = uniqid) = 0 AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_not_marked_only_correct",

       (SELECT COUNT(*) FROM marks WHERE is_noun = FALSE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_pronouns_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'B' WHERE is_noun = FALSE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_pronouns_correct_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'T' WHERE is_noun = FALSE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_pronouns_partially_correct_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'F' WHERE is_noun = FALSE AND((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_pronouns_incorrect_only_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = FALSE AND (SELECT COUNT(*) FROM corrections WHERE uniq_id = uniqid) = 0 AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_pronouns_not_marked_only_correct",

       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'B' WHERE is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_correct_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'T' WHERE is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_partially_correct_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'F' WHERE is_noun = TRUE AND((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_incorrect_only_correct",
       (SELECT COUNT(*) FROM marks WHERE is_noun = TRUE AND (SELECT COUNT(*) FROM corrections WHERE uniq_id = uniqid) = 0 AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_not_marked_only_correct",

       (SELECT COUNT(*) FROM marks WHERE is_singular = 'n' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_plural_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'B' WHERE is_singular = 'n' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_correct_plural_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'T' WHERE is_singular = 'n' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_partially_correct_plural_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'F' WHERE is_singular = 'n' AND is_noun = TRUE AND((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_incorrect_plural_only_correct",
       (SELECT COUNT(*) FROM marks WHERE is_singular = 'n' AND is_noun = TRUE AND (SELECT COUNT(*) FROM corrections WHERE uniq_id = uniqid) = 0 AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_not_marked_plural_only_correct",

       (SELECT COUNT(*) FROM marks WHERE is_singular = '?' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_unknown_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'B' WHERE is_singular = '?' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_correct_unknown_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'T' WHERE is_singular = '?' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_partially_correct_unknown_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'F' WHERE is_singular = '?' AND is_noun = TRUE AND((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_incorrect_unknown_only_correct",
       (SELECT COUNT(*) FROM marks WHERE is_singular = '?' AND is_noun = TRUE AND (SELECT COUNT(*) FROM corrections WHERE uniq_id = uniqid) = 0 AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_not_marked_unknown_only_correct",

       (SELECT COUNT(*) FROM marks WHERE is_singular = 'y' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_sing_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'B' WHERE is_singular = 'y' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_correct_sing_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'T' WHERE is_singular = 'y' AND is_noun = TRUE AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_partially_correct_sing_only_correct",
       (SELECT COUNT(*) FROM marks INNER JOIN corrections ON uniq_id = uniqid AND result = 'F' WHERE is_singular = 'y' AND is_noun = TRUE AND((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_incorrect_sing_only_correct",
       (SELECT COUNT(*) FROM marks WHERE is_singular = 'y' AND is_noun = TRUE AND (SELECT COUNT(*) FROM corrections WHERE uniq_id = uniqid) = 0 AND ((ntbg = TRUE AND was_correct = TRUE))) "need_to_be_corrected_nouns_not_marked_sin_only_correct"
