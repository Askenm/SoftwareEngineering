
# RETURN SERIAL ID RETURNING id;
query_catalog = {'write':{"CREATE_BATTLE":
                                          """
                                          INSERT INTO ckb.battles (battle_name, battle_description, tournament_id, github_repo, creator,end_date)
                                          VALUES (_BATTLE_NAME_, _BATTLE_DESC_, 1, _BATTLE_REPO_, _BATTLE_CREATOR_,_END_DATE_)
                                          RETURNING bid;
                                          """},
                 'read':{"GET_BATTLE_RANKINGS":
                                              """SELECT 
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
                            "GET_BATTLE_PAGE_INFO":
                                                 """
                                                 SELECT * FROM ckb.battles b
                                                 WHERE b.bid = _BATTLE_ID_
                                                 """}}