# RETURN SERIAL ID RETURNING id;
query_catalog = {
    "write": {
        "CREATE_BATTLE": """
                                          INSERT INTO ckb.battles (battle_name, 
                                                                   battle_description, 
                                                                   tournament_id, 
                                                                   github_repo, 
                                                                   creator,
                                                                   end_date,
                                                                   registration_deadline,
                                                                   min_group_size,
                                                                   max_group_size,
                                                                   manual_scoring)
                                          VALUES ('_BATTLE_NAME_', 
                                                  '_BATTLE_DESC_', 
                                                  _TOURNAMENT_ID_, 
                                                  '_BATTLE_REPO_', 
                                                  '_BATTLE_CREATOR_',
                                                  '_END_DATE_',
                                                  '_REGISTRATION_DEADLINE_',
                                                  _MIN_GROUP_SIZE_,
                                                  _MAX_GROUP_SIZE_,
                                                  _MANUAL_SCORING_)
                                          RETURNING bid;
                                          """,
        "END_TOURNAMENT": """
                                            UPDATE ckb.tournaments
                                            SET end_date = NOW()
                                            WHERE tid = _TOURNAMENT_ID_;

                                            """,
        "CREATE_TOURNAMENT": """
                                                 INSERT INTO ckb.tournaments (tournament_name, creator,description,subscription_deadline)
                                                 VALUES ('_TOURNAMENT_NAME_', '_CREATOR_','_DESCRIPTION_','_SUBSCRIPTION_DEADLINE_')
                                                 RETURNING tid;
                                                 """,
        "CREATE_BADGE": """
                            INSERT INTO ckb.badge (badge_name, badge_description, tournament_id, rank, num_battles)
                            VALUES 
                            ('_BADGE_NAME_', '_BADGE_DESC_', _TOURNAMENT_ID_, _RANK_, _NUM_BATTLES_)
                            """,
        "AWARD_BADGE": """
                            INSERT INTO ckb.badgeholders (bid, uid)
                            VALUES 
                            (_BADGE_ID_, _USER_ID_)
                            """,
        "REGISTER_NOTIFICATION": """
                                   INSERT INTO ckb.message_board (uid, notification_type, tournament_id, notification_text, battle_id)
                                   VALUES
                                   (_USER_ID_, '_NOTIFICATION_TYPE_', _TOURNAMENT_ID_, '_NOTIFICATION_TEXT_', _BATTLE_ID_)
                                   """,
       "MARK_NOTIFICATION_AS_SENT":       """
                                          UPDATE ckb.message_board
                                          SET is_sent = TRUE, 
                                          sent_date = CURRENT_DATE
                                          WHERE nid = _NOTIFICATION_ID_;

                                          """,
       "JOIN_GROUP": """
                     INSERT INTO ckb.groups (group_name, bid, uid)
                     VALUES ('_GROUP_NAME_', _BATTLE_ID_, _USER_ID_);

                     """,
       "SUBSCRIBE_TO_TOURNAMENT":  """
                                   INSERT INTO ckb.subscriptions (uid, tid)  
                                   VALUES ( _USER_ID_,_TOURNAMENT_ID_);
                                   """,
       "ASSIGN_MANUAL_SCORE":      """
                                   UPDATE ckb.submissions
                                   SET submission_score = _SCORE_ 
                                   WHERE smid = _SUBMISSION_ID_;
                                   """,
       "ASSIGN_AUTOMATIC_SCORE":      """
                            INSERT INTO ckb.submissions (bid, gid,score)
                            VALUES ( _BATTLE_ID_,_GROUP_ID_,_SCORE_);
                            """,
       "MARK_SUBMISSION_AS_SENT":  """
                                   UPDATE ckb.submissions
                                   SET notification_registered = TRUE
                                   WHERE smid = _SUBMISSION_ID_;
                                   """,
       "ADD_USER":   """
                     INSERT INTO ckb.users (uid, create_date, user_email, user_name, password, is_educator, github_user_name)  
                     VALUES (_uid_, _create_date_, '_user_email_', '_user_name_', '_password_', _is_educator_, '_github_')
                     """
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
                                                 SELECT tournament_name,creator, description, subscription_deadline FROM ckb.tournaments t
                                                 WHERE t.tid = _TOURNAMENT_ID_
                                                 """,
                                                 
       "GET_UPCOMING_TOURNAMENTS": """          SELECT tournament_name, subscription_deadline, description, tid FROM ckb.tournaments
                                                 WHERE subscription_deadline >= NOW()::DATE
                                                                                           
                                                 """,
       "GET_ONGOING_TOURNAMENTS": """           SELECT tournament_name, description, tid FROM ckb.tournaments
                                                 WHERE subscription_deadline < NOW()::DATE
                                                 AND end_date IS NULL                                           
                                                 """,

       "GET_RELATED_BATTLES_ONGOING": """
                                          SELECT b.bid,
                                                 b.battle_name,
                                                 CASE WHEN b.end_date < NOW()::DATE
                                                 THEN 'Ended'
                                                 ELSE 'Ongoing'
                                                 END
                                                 as battle_status,
                                                 b.min_group_size,
                                                 b.max_group_size,
                                                 b.end_date
                                                 
                                                 FROM ckb.battles b
                                                 INNER JOIN 
                                                 ckb.tournaments t
                                                 ON b.tournament_id = t.tid
                                                 
                                                 
                                                 WHERE t.tid = _TOURNAMENT_ID_
                                                 AND registration_deadline < NOW()::DATE
                                                 
                                                 ORDER BY b.end_date desc
                                                 
                                                 """,
                                                 
       "GET_RELATED_BATTLES_UPCOMING": """
                                                 SELECT b.bid,
                                                 b.battle_name,
                                                 b.registration_deadline,
                                                 b.min_group_size,
                                                 b.max_group_size
                                                 
                                                 
                                                 FROM ckb.battles b
                                                 INNER JOIN 
                                                 ckb.tournaments t
                                                 ON b.tournament_id = t.tid
                                                 
                                                 
                                                 WHERE t.tid = _TOURNAMENT_ID_
                                                 AND registration_deadline >= NOW()::DATE
                                                 
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
                            submission_score,
                            group_repository
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
        "GET_BADGE_ACHIEVERS": """
                                   WITH RankedSubmissions AS (
                                   SELECT 
                                          s.submission_score, 
                                          g.uid, 
                                          s.battle_id,
                                          b.tournament_id,
                                          RANK() OVER (PARTITION BY s.battle_id ORDER BY s.submission_score DESC) as rank
                                   FROM ckb.submissions s
                                   JOIN ckb.groups g ON s.gid = g.gid
                                   JOIN ckb.battles b ON s.battle_id = b.bid
                                   WHERE b.tournament_id = _TOURNAMENT_ID_
                                   ),
                                   TopUsers AS (
                                   SELECT 
                                          uid, 
                                          COUNT(*) AS top_finishes
                                   FROM RankedSubmissions
                                   WHERE rank <= _RANK_
                                   GROUP BY uid
                                   )
                                   SELECT 
                                   u.uid, 
                                   u.user_name, 
                                   top_finishes
                                   FROM TopUsers tu
                                   JOIN ckb.users u ON tu.uid = u.uid
                                   WHERE top_finishes > _NUM_BATTLES_;
                                   """,
        "GET_BADGE_LOGIC": """
                                   SELECT tournament_id, rank, num_battles 
                                   FROM ckb.badge
                                   WHERE bid = _BADGE_ID_
                                   """,
        "GET_USER_TOURNAMENTS": """
                                   SELECT 
                                   t.tid,
                                   tournament_name from 
                                   ckb.tournaments t
                                   INNER JOIN ckb.subscriptions s
                                   ON t.tid = s.tid
                                   WHERE s.uid = _USER_ID_
                                   """,
       
       "GET_USER_ONGOING_TOURNAMENTS": """
                                   SELECT 
                                   t.tid,
                                   tournament_name,
                                   description
                                   from 
                                   ckb.tournaments t
                                   INNER JOIN ckb.subscriptions s
                                   ON t.tid = s.tid
                                   WHERE s.uid = _USER_ID_
                                   AND t.subscription_deadline < NOW()::DATE
                                   AND t.end_date IS NULL
                                   """,
      
       "GET_USER_UPCOMING_TOURNAMENTS": """
                                   SELECT 
                                   t.tid
                                   tournament_name,
                                   subscription_deadline ,
                                   description
                                   from 
                                   ckb.tournaments t
                                   INNER JOIN ckb.subscriptions s
                                   ON t.tid = s.tid
                                   WHERE s.uid = _USER_ID_
                                   AND subscription_deadline >= NOW()::DATE
                                   AND end_date IS NULL
                                   """,
       
        "GET_USER_BATTLES": """
                                   select battle_name,group_name,b.end_date 
                                   FROM ckb.groups g
                                   INNER JOIN ckb.battles b 
                                   ON b.bid = g.bid 
                                   WHERE g.uid = _USER_ID_
                                   """,
        
        "GET_USER_ONGOING_BATTLES": """
                                   select b.bid, battle_name, group_name, b.end_date, b.github_repo
                                   FROM ckb.groups g
                                   INNER JOIN ckb.battles b 
                                   ON b.bid = g.bid 
                                   WHERE g.uid = _USER_ID_
                                   AND b.registration_deadline < NOW()::DATE
                                   AND (b.end_date IS NULL OR b.end_date > NOW()::DATE)
                                   """,  
                                                             
        "GET_USER_UPCOMING_BATTLES": """
                                   select b.bid, battle_name, registration_deadline, group_name, b.end_date
                                   FROM ckb.groups g
                                   INNER JOIN ckb.battles b 
                                   ON b.bid = g.bid 
                                   WHERE g.uid = _USER_ID_
                                   AND b.registration_deadline >= NOW()::DATE
                                   AND b.end_date IS NULL
                                   """,                              
                                   
        "GET_USER_BADGES": """
                                   select badge_name,tournament_name,badge_achieved 
                                   FROM ckb.badge b
                                   INNER JOIN ckb.badgeholders bh 
                                   ON b.bid = bh.bid 
                                   INNER JOIN ckb.tournaments t
                                   ON t.tid = b.tournament_id
                                   WHERE bh.uid = _USER_ID_
                                   """,
       "GET_BADGE_NAME":    """
                            SELECT badge_name FROM ckb.badge WHERE bid = _BADGE_ID_
                            """,
       "GET_TOURNAMENT_NAME_FROM_BADGE_ID":      """
                                                 SELECT tournament_id,tournament_name FROM ckb.badge b
                                                 INNER JOIN ckb.tournaments t
                                                 ON b.tournament_id = t.tid
                                                 WHERE bid = _BADGE_ID_ 
                                                 """,
       "GET_USER_NAME_FROM_UID":                 """
                                                 SELECT user_name FROM ckb.users u
                                                 WHERE uid = _USER_ID_
                                                 """,
       "CHECK_MESSAGEBOARD":       """
                                   SELECT u.user_email , m.*FROM ckb.message_board m
                                   inner join ckb.users u
                                   ON u.uid = m.uid
                                   WHERE is_sent = false
                                   """,
       "GET_ALL_BADGES":    """
                            SELECT * FROM ckb.badge b
                            INNER JOIN ckb.tournaments t
                            ON b.tournament_id = t.tid
                            WHERE t.end_date is NULL
                            """,
       "GET_BATTLE_TOURNAMENT":    """
                                   SELECT tournament_id 
                                   """,
       "GET_CURRENT_BADGE_HOLDERS":       """
                                          SELECT * FROM ckb.badgeholders
                                          WHERE bid = _BADGE_ID_
                                          """,
       "GET_TOURNAMENT_NAME":      """
                                   SELECT tournament_name FROM ckb.tournaments t
                                   WHERE tid = _TOURNAMENT_ID_
                                   """,

       "GET_UNASSIGNED_SUBSCRIBERS":    """
              SELECT u.uid,u.user_name FROM 
              ckb.battles b 
              INNER JOIN ckb.tournaments t
              ON b.tournament_id = t.tid
              INNER JOIN ckb.subscriptions s
              ON s.tid = t.tid
              INNER JOIN ckb.users u
              ON s.uid = u.uid

              WHERE 
              b.bid = _BATTLE_ID_
              AND
              u.uid NOT IN 
              (SELECT g.uid FROM 
              ckb.battles b 
              INNER JOIN ckb.tournaments t
              ON b.tournament_id = t.tid
              INNER JOIN ckb.groups g
              ON g.bid = b.bid
              WHERE b.bid = _BATTLE_ID_)
              """,
       "GET_NEW_SUBMISSIONS":    """SELECT * FROM ckb.submissions WHERE notification_registered = false;""",
       "GET_USERS_FROM_GID":    """
              SELECT * FROM ckb.groups g
              INNER JOIN ckb.battles b 
              on g.bid = b.bid
              INNER JOIN ckb.users u
              ON g.uid = u.uid
              INNER JOIN ckb.tournaments t
              ON t.tid = b.tournament_id

              WHERE g.gid = _GROUP_ID_
              """,
       "GET_EDUCATOR_BATTLES":     """
                                   SELECT 
                                   b.bid,
                                   battle_name ,
                                   registration_deadline,
                                   b.end_date,
                                   battle_description,
                                   github_repo,
                                   min_group_size,
                                   max_group_size,
                                   user_name as creator,
                                   tournament_name
                                   FROM 
                                   ckb.battles b
                                   INNER JOIN
                                   ckb.tournaments t 
                                   ON b.tournament_id = t.tid

                                   INNER JOIN
                                   ckb.users u 
                                   ON b.creator = u.uid

                                   WHERE b.creator = _USER_ID_
                                   """,
                                   
       "GET_ONGOING_EDUCATOR_BATTLES":     """
                                   SELECT 
                                   b.bid,
                                   battle_name ,
                                   registration_deadline,
                                   b.end_date,
                                   battle_description,
                                   github_repo,
                                   min_group_size,
                                   max_group_size,
                                   user_name as creator,
                                   tournament_name
                                   FROM 
                                   ckb.battles b
                                   INNER JOIN
                                   ckb.tournaments t 
                                   ON b.tournament_id = t.tid

                                   INNER JOIN
                                   ckb.users u 
                                   ON b.creator = u.uid

                                   WHERE b.creator = _USER_ID_
                                   AND b.registration_deadline < NOW()::DATE
                                   AND (b.end_date > NOW()::DATE OR b.end_date IS NULL)
                                   """,
       "GET_UPCOMING_EDUCATOR_BATTLES":     """
                                   SELECT 
                                   b.bid,
                                   battle_name ,
                                   registration_deadline,
                                   b.end_date,
                                   battle_description,
                                   github_repo,
                                   min_group_size,
                                   max_group_size,
                                   user_name as creator,
                                   tournament_name
                                   FROM 
                                   ckb.battles b
                                   INNER JOIN
                                   ckb.tournaments t 
                                   ON b.tournament_id = t.tid

                                   INNER JOIN
                                   ckb.users u 
                                   ON b.creator = u.uid

                                   WHERE b.creator = _USER_ID_
                                   AND b.registration_deadline >= NOW()::DATE
                                   
                                   """,
                                   
       "GET_EDUCATOR_TOURNAMENTS":     """
                                   SELECT  t.creator, t.tid, tournament_name, subscription_deadline, description, u.user_name as creator_name,COUNT(b.bid) AS number_of_battles
                                   FROM ckb.tournaments t
                                   INNER JOIN ckb.users u 
                                   on t.creator = uid
                                   LEFT JOIN 
                                   ckb.battles b ON t.tid = b.tournament_id
                                   WHERE t.creator = _USER_ID_
                                   GROUP BY 
                                   t.creator, t.tid, t.tournament_name, t.subscription_deadline, t.description, u.user_name
                                   """,
       "GET_ONGOING_EDUCATOR_TOURNAMENTS":     """
                                   SELECT 
                                   t.tid,
                                   tournament_name,
                                   description,
				       count(distinct b.bid) as num_battles,
                                   u.user_name as creator_name
                                   FROM ckb.tournaments t
                                   INNER JOIN ckb.users u 
                                   on creator = uid
                                   INNER JOIN ckb.battles b
                                   on b.tournament_id = t.tid
                                   WHERE t.creator = _USER_ID_
                                   AND t.subscription_deadline < NOW()::DATE
                                   AND t.end_date IS NULL 
								   
                                   GROUP BY 
                                   t.tid,tournament_name,
                                   description,
                                   u.user_name; 
                                   """,
       "GET_UPCOMING_EDUCATOR_TOURNAMENTS":     """
                                   SELECT 
                                   t.tid,
                                   tournament_name,
                                   subscription_deadline,
                                   description,
				       count(distinct b.bid) as num_battles,
                                   u.user_name as creator_name
                                   FROM ckb.tournaments t
                                   INNER JOIN ckb.users u 
                                   on creator = uid
                                   INNER JOIN ckb.battles b
                                   on b.tournament_id = t.tid
                                   WHERE t.creator = _USER_ID_
                                   AND t.subscription_deadline >= NOW()::DATE
                                   
								   
                                   GROUP BY 
                                   t.tid,tournament_name,
                                   subscription_deadline,
                                   description,
                                   u.user_name; 
                                   """,
       
       "GET_GROUPS": """
                     select g.group_name,string_agg(user_name,' - ') as Members from ckb.groups g
                     INNER JOIN
                     ckb.users u 
                     ON u.uid = g.uid
                     WHERE bid = _BATTLE_ID_
                     GROUP BY g.group_name
                     """,

       "GET_PARTICIPANTS":  """
                            SELECT uid from ckb.groups where bid = _BATTLE_ID_
                            """,
       "IS_USER_SUBSCRIBED":       """
                                   SELECT * from ckb.subscriptions
                                   WHERE uid = _USER_ID_
                                   AND tid = _TOURNAMENT_ID_
                                   """,

       "GET_SUBMISSION":    """
                            
                            """,
       "GET_CREDENTIALS": """
                            SELECT user_email, uid, user_name, password, is_educator
                            FROM ckb.users;
                     """,
       "GET_MAX_ID": """
                     SELECT MAX(uid) AS highest_uid
                     FROM ckb.users;
                     """,
       "GET_ID": """
                     SELECT uid FROM ckb.users u
                     WHERE user_name = '_USER_NAME_'
                     """,
       "GET_STUDENTS": """
                     SELECT user_name, uid FROM ckb.users u
                     WHERE is_educator is FALSE
                     """,
       "GET_SUBMISSION_FOR_SCORING": """
                                   WITH RankedSubmissions AS (
                                   SELECT 
                                          s.*, g.group_name, b.battle_name, b.creator, b.github_repo,
                                          RANK() OVER (PARTITION BY s.battle_id, s.gid ORDER BY s.submission_score DESC) as rank
                                   FROM 
                                          ckb.submissions s
                                   INNER JOIN 
                                          ckb.groups g ON s.gid = g.gid
                                   INNER JOIN 
                                          ckb.battles b ON s.battle_id = b.bid
                                   INNER JOIN 
                                          ckb.users u ON b.creator = u.uid
                                   WHERE 
                                          u.uid = _EDUCATOR_ID_
                                          AND b.end_date < NOW()::DATE
                                   )
                                   SELECT 
                                   gid, battle_id, submission_datetime, submission_score, 
                                   group_name, battle_name, creator, smid, github_repo
                                   FROM 
                                   RankedSubmissions
                                   WHERE 
                                   rank = 1;

                                   """

    },
}
