# RETURN SERIAL ID RETURNING id;
query_catalog = {
    "write": {
        "CREATE_BATTLE": """
                                          INSERT INTO ckb.battles (battle_name, battle_description, tournament_id, github_repo, creator,end_date)
                                          VALUES ('_BATTLE_NAME_', '_BATTLE_DESC_', 1, '_BATTLE_REPO_', '_BATTLE_CREATOR_','_END_DATE_')
                                          RETURNING bid;
                                          """,
        "END_TOURNAMENT": """
                                            UPDATE ckb.tournaments
                                            SET end_date = NOW()
                                            WHERE tid = _TOURNAMENT_ID_;

                                            """,
        "CREATE_TOURNAMENT": """
                                                 INSERT INTO ckb.tournaments (tournament_name, creator)
                                                 VALUES ('_TOURNAMENT_NAME_', '_CREATOR_')
                                                 RETURNING tid;
                                                 """,
    },
    "read": {
        "GET_BATTLE_RANKINGS": """SELECT 
                                                 g.group_name,
                                                 MAX(submission_score) as score, 
                                                 COUNT(DISTINCT smid) as num_submissions 
                                                 FROM ckb.battles b
                                                 INNER JOIN ckb.groups g
                                                 ON b.bid = g.bid
                                                 INNER JOIN ckb.submissions s
                                                 ON s.gid = g.gid

                                                 WHERE b.bid = _BATTLE_ID_

                                                 GROUP BY g.group_name
                                                 ORDER BY score desc
                                                 """,
        "GET_BATTLE_PAGE_INFO": """
                                                 SELECT * FROM ckb.battles b
                                                 WHERE b.bid = _BATTLE_ID_
                                                 """,
        "BATTLE_NAME_VACANT": """
                                                 SELECT count(*) AS count FROM ckb.battles 
                                                 WHERE battle_name = '_BATTLE_NAME_'
                                                 """,
        "TOURNAMENT_NAME_VACANT": """
                                                 SELECT count(*) AS count FROM ckb.tournaments 
                                                 WHERE tournament_name = '_TOURNAMENT_NAME_'
                                                 """,
        "GET_TOURNAMENT_RANKINGS": """SELECT 
                                                 u.user_name,
                                                 BattleQuery.score,
                                                 COUNT(distinct BattleQuery.bid) as num_battles

                                                 FROM ckb.tournaments t
                                                 INNER JOIN 
                                                 (SELECT b.bid,
                                                               g.uid,
                                                 MAX(submission_score) as score
                                                 FROM ckb.battles b
                                                 INNER JOIN ckb.groups g
                                                 ON b.bid = g.bid
                                                 INNER JOIN ckb.submissions s
                                                 ON s.gid = g.gid

                                                 GROUP BY b.bid,g.uid
                                                 ) as BattleQuery

                                                 ON t.tid = BattleQuery.bid
                                                 INNER JOIN ckb.users u
                                                 on u.uid = BattleQuery.uid

                                                 WHERE t.tid = _TOURNAMENT_ID_ 

                                                 GROUP BY u.user_name,BattleQuery.score
                                                 ORDER BY BattleQuery.score desc
                                                 """,
        "GET_TOURNAMENT_PAGE_INFO": """
                                                 SELECT tournament_name FROM ckb.tournaments t
                                                 WHERE t.tid = _TOURNAMENT_ID_
                                                 """,
        "GET_RELATED_BATTLES": """
                                                 SELECT b.battle_name,
                                                 CASE WHEN b.end_date < NOW()::DATE
                                                 THEN 'Ended'
                                                 ELSE 'Ongoing'
                                                 END
                                                 as battle_status,
                                                 b.create_date,
                                                 b.end_date
                                                 FROM ckb.battles b
                                                 INNER JOIN 
                                                 ckb.tournaments t
                                                 ON b.tournament_id = t.tid
                                                 
                                                 
                                                 WHERE t.tid = _TOURNAMENT_ID_
                                                 
                                                 ORDER BY b.end_date desc
                                                 
                                                 """,
        "IS_EDUCATOR": """
                            SELECT is_educator FROM ckb.users WHERE uid = _USER_ID_
                            """,
        "GET_USER_GROUP": """
                            SELECT DISTINCT u.uid,g.gid,group_name 
                            FROM ckb.users u
                            INNER JOIN ckb.groups g
                            ON g.uid = u.uid
                            INNER JOIN ckb.battles b
                            ON g.bid = b.bid
                            WHERE u.uid = _USER_ID_
                            AND
                            b.bid = _BATTLE_ID_
                            """,
        "GET_SUBMISSIONS": """
                            SELECT DISTINCT
                            smid,
                            s.gid,
                            group_name,
                            submission_datetime,
                            submission_score
                            FROM
                            ckb.submissions s
                            INNER JOIN ckb.groups g
                            ON s.gid = g.gid

                            WHERE _CONDITIONAL_
                            """,
        "GET_TOURNAMENT_BADGES": """
                                   SELECT badge_name,badge_description
                                   FROM ckb.badge b
                                   WHERE tournament_id = _TOURNAMENT_ID_
                                   """,
    },
}
