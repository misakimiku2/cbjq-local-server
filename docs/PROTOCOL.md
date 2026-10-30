# 客户端请求接口清单（CallGS）

> 由 `work/probe/scan_protocol.js` 从运行时 dump 的 Lua 5.4 字节码自动生成。
> 覆盖范围 = 当前 `work/_dump/` 里已 dump 的模块，不是全量。

共 **127** 个接口。

## Rogue3D (19)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Rogue3D_CheckOpenAct` | — | _G_Rogue3DLogic__Req_CheckOpenAct |
| `Rogue3D_EnterLevel` | nDiffId, nTeamID, tbBuffList, tbLog, tbTeam | _G_Rogue3DLogic__Req_EnterLevel |
| `Rogue3D_EnterSeasonLevel` | nDiffId, nTeamID, tbBuffList, tbLog, tbTeam | _G_Rogue3DLogic__Req_EnterSeasonLevel |
| `Rogue3D_GetLevelAward` | tbIdList | _G_Rogue3DLogic__Req_GetLevelAward |
| `Rogue3D_GetQuestAward` | tbIdList | _G_Rogue3DLogic__Req_GetQuestAward |
| `Rogue3D_GetSeasonLotteryAward` | nIndex, nTimes | _G_Rogue3DLogic__Req_Gacha |
| `Rogue3D_GetSeasonQuestAward` | tbIdList | _G_Rogue3DLogic__Req_GetSeasonQuestAward |
| `Rogue3D_LevelReset` | nDiffId, tbMember | _G_Rogue3DLogic__Req_LevelReset |
| `Rogue3D_MonsterRikiAward` | — | _G_Rogue3DLogic__ReqMonsterRikiAward |
| `Rogue3D_RecoverJourneySan` | — | _G_Rogue3DLogic__Req_RecoverJourneySan |
| `Rogue3D_RestrictTech` | nRestrict, nTechId | _G_Rogue3DLogic__Req_RestrictTech |
| `Rogue3D_RoomSettlement` | nNodeId, tbKill, tbMonster | _G_Rogue3DLogic__Req_SendAchievementData |
| `Rogue3D_SeasonLevelReset` | nDiffId, tbMember | _G_Rogue3DLogic__Req_SeasonLevelReset |
| `Rogue3D_SeasonRoomSettlement` | nNodeId, tbKill, tbMonster | _G_Rogue3DLogic__Req_SendAchievementData<br>_G_Rogue3DLogic__Req_SendSeasonAchievementData |
| `Rogue3D_SelectDiff` | nDiffId | _G_Rogue3DLogic__Req_SelectDiff |
| `Rogue3D_SelectMode` | nModeID | _G_Rogue3DLogic__Req_SelectMode |
| `Rogue3D_SelectSeasonTalent` | nTalentId | _G_Rogue3DLogic__Req_SelectSeasonTalent |
| `Rogue3D_SelectTalent` | nTalentId | _G_Rogue3DLogic__Req_SelectTalent |
| `Rogue3D_UpgradeTech` | nTechId | _G_Rogue3DLogic__Req_UpgradTech |

## StarWish (13)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `StarWish_AutoCompleteStoryQuest` | nID | _G_StarWishLogic__AutoCompleteStoryQuest |
| `StarWish_CheckOpenAct` | — | _G_StarWishLogic__CheckOpenAct/_ENV |
| `StarWish_CleanSubIDCompleted` | nID | _G_StarWishLogic__CleanSubIDCompleted |
| `StarWish_CompleteShareAchievement` | — | _G_StarWishLogic__CompleteShareAchievement |
| `StarWish_GetAllCompleteAward` | — | _G_StarWishLogic__GetAllCompleteAward |
| `StarWish_GetRepeatQuestAward` | tbTaskID | _G_StarWishLogic__GetRepeatQuestAward |
| `StarWish_GetRepeatQuestExtraAward` | nPos | _G_StarWishLogic__GetRepeatQuestExtraAward |
| `StarWish_GetScoreAward` | — | _G_StarWishLogic__GetScoreAward |
| `StarWish_GetStoryPageAward` | nID | _G_StarWishLogic__GetStoryPageAward |
| `StarWish_GetStoryQuestAward` | tbID | _G_StarWishLogic__GetStoryQuestAward |
| `StarWish_LotteryJigsaw` | nTimes | _G_StarWishLogic__LotteryJigsaw |
| `StarWish_SetStoryQuestCompleted` | Value, bShowPop, nID | _G_StarWishLogic__SetStoryQuestCompleted |
| `StarWish_SetSubIDCompleted` | bShowPop, nID, nPos, v | _G_StarWishLogic__SetSubIDCompleted |

## RogueLogic (10)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RogueLogic_ChangeFormation` | tbFormation | _G_RogueLogic__SetRogueLineup |
| `RogueLogic_ClientMoveNext` | nID | _G_RogueLogic__MoveNext |
| `RogueLogic_EnterRogue` | — | _G_RogueLogic__EnterRogue |
| `RogueLogic_FetchDailyBuff` | — | _G_RogueLogic__FetchDailyBuff |
| `RogueLogic_FinishNode` | — | _G_RogueLogic__FinishNode |
| `RogueLogic_QuickGetReward` | tbIdList | _G_RogueLogic__QuickGetReward |
| `RogueLogic_RefreshShopGoods` | nNodeID | _G_RogueLogic__RefreshShopGoods |
| `RogueLogic_ResetRogue` | — | _G_RogueLogic__ResetRogue |
| `RogueLogic_ReviveRole` | — | _G_RogueLogic__ReviveRole |
| `RogueLogic_VisitShop` | nNodeID | _G_RogueLogic__VisitShop |

## PartyLogic (9)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `PartyLogic_CheckFirstSign` | nId, nTeach | _G_PartyLogic__CheckFirstSign |
| `PartyLogic_SetFightCard` | nId | _G_PartyLogic__SetFightCard |
| `PartyLogic_SetFirstSign` | nId | _G_PartyLogic__SetFirstSign |
| `PartyLogic_SetMatchId` | nId | _G_PartyLogic__SetMatchId |
| `PartyLogic_SetMatchMode` | nSingle | _G_PartyLogic__SetMatchMode |
| `PartyLogic_SetRandomMapId` | — | _G_PartyLogic__SetRandomMapId |
| `PartyLogic_SetSkillID` | nId1, nId2 | _G_PartyLogic__SetFightSkill |
| `PartyLogic_SetTitle` | nId | _G_PartyLogic__SetTitle |
| `PartyLogic_SetTitleShow` | nType | _G_PartyLogic__SetTitleShow |

## RichManLoveLogic (8)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RichManLoveLogic_CheckOpenAct` | — | _G_RichManLoveLogic__CheckOpenAct |
| `RichManLoveLogic_EnterMap` | bContinue, nId, nMapId | _G_RichManLoveLogic__EnterMap |
| `RichManLoveLogic_EnterMapLog` | nMapId, nSeed, tbLog | _G_RichManLoveLogic__EnterMapLog |
| `RichManLoveLogic_LikeEnd` | nId | _G_RichManLoveLogic__LikeEnd |
| `RichManLoveLogic_MapSettlement` | activityId, activityType, mapId, nSeed, tbLevelNum | _G_RichManLoveLogic__MapSettlement |
| `RichManLoveLogic_QuickGetReward` | tbIdList | _G_RichmanLogic__DoGetMission |
| `RichManLoveLogic_SettlementUnlockEnd` | nId, nMapId, tbLog | _G_RichManLoveLogic__SettlementUnlockEnd |
| `RichManLoveLogic_UseDice` | — | _G_RichManLoveLogic__UseDice |

## BossLogic (7)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `BossLogic_EnterLevel` | nDifficulty, nID, nTeamID, tbEntrie, tbLog | _G_BossLogic__Req_EnterLevel |
| `BossLogic_GetOpenID` | — | _G_BossLogic__GetOpenID/_ENV |
| `BossLogic_GetReward` | Mileage | _G_BossLogic__GetReward |
| `BossLogic_LevelFail` | nID, tbLog | _G_BossLogic__Req_LevelFail |
| `BossLogic_OneClicReward` | — | _G_BossLogic__OneClicReward |
| `BossLogic_Record` | bRecord, nID, nSeed, nTime | _G_BossLogic__Record |
| `BossLogic_Reset` | nID | _G_BossLogic__Reset |

## ClimbTowerLogic (6)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ClimbTowerLogic_CheckCycleLevel` | — | _G_ClimbTowerLogic__CheckCycleLevel/_ENV |
| `ClimbTowerLogic_GetReward` | nGroup, nLayer, nType | _G_ClimbTowerLogic__GetReward |
| `ClimbTowerLogic_OneClicReward` | nGroup, nType | _G_ClimbTowerLogic__OneClicReward |
| `ClimbTowerLogic_RecordChallenged` | nID | _G_ClimbTowerLogic__RecordChallenged |
| `ClimbTowerLogic_RecordProgres` | nArea, nID, nStar, nTeamEnergy, tbRoleHP | _G_ClimbTowerLogic__RecordProgres |
| `ClimbTowerLogic_SetLevelDiff` | nDiff | _G_ClimbTowerLogic__SetLevelDiff |

## FishingServer (6)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `FishingServer_BeginFishing` | nNodeID, nSelectBait | _G_FishingLogic__BeginFishing |
| `FishingServer_ConvertFood` | nFoodID, nNum | _G_FishingLogic__GetCookAward |
| `FishingServer_EndFishing` | nState | _G_FishingLogic__EndFishing |
| `FishingServer_GetCollectAward` | nId, tbIdList | _G_FishingLogic__GetCollectAward |
| `FishingServer_GetLevelAward` | nLevel | _G_FishingLogic__GetLevelAward |
| `FishingServer_ReadFishRecord` | nFishID | _G_FishingLogic__ReadFishRecord |

## BossPvpLogic (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `BossPvpLogic_EnterLevel` | nDifficulty, nID, nLevelID, nTeamID, tbEntrie, tbLog | _G_BossPvpLogic__Req_EnterLevel |
| `BossPvpLogic_GetOpenID` | — | _G_BossPvpLogic__GetOpenID/_ENV |
| `BossPvpLogic_GetReward` | tbTaskID | _G_BossPvpLogic__GetReward |
| `BossPvpLogic_LevelMopup` | — | _G_BossPvpLogic__Req_LevelMopup |
| `BossPvpLogic_Record` | ResidueTime, bRecord, nDiff, nID, nSeed, nTime | _G_BossPvpLogic__Record |

## DefendLogic (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DefendLogic_CheckOpenAct` | — | _G_DefendLogic__CheckOpenAct/_ENV<br>_G_DefendLogic__GetOpenConf |
| `DefendLogic_EnterLevel` | nDiff, nID, nTeamID, tbLog | _G_DefendLogic__Req_EnterLevel |
| `DefendLogic_GetLevelAward` | tbIdList | _G_DefendLogic__Req_GetLevelAward |
| `DefendLogic_GetReward` | bAll, nDiff, nID, nIdx, nTargetId | _G_DefendLogic__GetReward<br>_G_DefendLogic__GetRewardAll |
| `DefendLogic_SelectDiff` | nDiffId | _G_DefendLogic__Req_SelectDiff |

## RichmanLogic (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RichmanLogic_CheckOpenAct` | — | _G_RichmanLogic__CheckOpenAct |
| `RichmanLogic_EnterMap` | bContinue, nId, nMapId, tbLog | _G_RichmanLogic__EnterMap |
| `RichmanLogic_MapSettlement` | activityId, activityType, mapId, nRank, nSeed, tbLevelNum, tbLog | _G_RichmanLogic__MapSettlement |
| `RichmanLogic_ReceiveVoteveReward` | nId | _G_RichmanLogic__ReceiveVoteveReward |
| `RichmanLogic_VoteGirl` | nId, nNum, nTotalNum | _G_RichmanLogic__VoteGirl |

## SeasonBoss (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `SeasonBoss_CheckOpen` | ForceEnter | _G_SeasonBossLogic__CheckOpen |
| `SeasonBoss_EnterLevel` | nDifficulty, nID, nTeamID, nZoneID, tbEntrie, tbLog | _G_SeasonBossLogic__Req_EnterLevel |
| `SeasonBoss_GetReward` | tbTaskID | _G_SeasonBossLogic__GetReward |
| `SeasonBoss_LevelFail` | ResidueTime, nDamage, nDiff, nID, nReason, nSeed, nTime, nZoneID, tbLog | _G_SeasonBossLogic__Req_LevelFail |
| `SeasonBoss_Record` | ResidueTime, bRecord, nDamage, nDiff, nID, nSeed, nTime, nZoneID | _G_SeasonBossLogic__Record |

## ShopLogic (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ShopLogic_BuyGoods` | nBuyMode, nCount, nGoodsId | _G_ShopLogic__BuyGoods |
| `ShopLogic_GetGoodsList` | nShopId | _G_ShopLogic__GetGoodsList |
| `ShopLogic_GetOpenTime` | — | _G_ShopLogic__GetOpenTime |
| `ShopLogic_UpdateShop` | nShopId | _G_ShopLogic__UpdateShop<br>_G_ShopLogic__UpdateShop/_ENV |

## ChessLogic (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ChessLogic_ChangeFormation` | tbFormation | _G_ChessLogic__SetLineup |
| `ChessLogic_CheckOpenAct` | — | _G_ChessLogic__CheckOpenAct/_ENV |
| `ChessLogic_EnterMap` | nId, nMapId | _G_ChessLogic__EnterMap |

## DecryptLogic (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DecryptLogic_CleanSubIDCompleted` | nID | _G_DecryptLogic__CleanSubIDCompleted |
| `DecryptLogic_SetCompleted` | Value, nID | _G_DecryptLogic__SetCompleted |
| `DecryptLogic_SetSubIDCompleted` | nID, nPos, v | _G_DecryptLogic__SetSubIDCompleted |

## (无前缀) (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DownloadMultMediaLog` | — | _G_ShareLogic__SendLog |
| `ExtendFightDynamicLog` | tbLog | _G_BossLogic__Req_LevelFail<br>_G_BossLogic__Req_LevelSettlement |
| `ExtendFightLog` | tbLog | _G_BossLogic__Req_LevelFail<br>_G_BossLogic__Req_LevelSettlement |

## GuideLogic (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GuideLogic_GMSetBeginner` | — | _G_GuideLogic__SkipAllGuide |
| `GuideLogic_SetBeginner` | nType | _G_GuideLogic__SetBeginner |
| `GuideLogic_WriteGuideLog` | logstr | _G_GuideLogic__ChackGuideLog |

## IBLogic (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `IBLogic_BuyGoods` | nCount, nGoodsId, nIndex, nType, tbSelectItem1, tbSelectItem2 | _G_IBLogic__DoBuyProduct |
| `IBLogic_GoodsRedDot` | tbList | _G_IBLogic__SetSkinRedDot |
| `IBLogic_ShoppingCart` | — | _G_IBLogic__DoBuyProductList |

## WorldBossLogic (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `WorldBossLogic_CheckOpen` | — | _G_WorldBossLogic__CheckOpen |
| `WorldBossLogic_GetReward` | tbTaskID | _G_WorldBossLogic__GetReward |

## Achievement (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Achievement_OnAddSomeOne` | nType | _G_InteractAnimLogic__PlayAnim |

## CallmeLogic (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `CallmeLogic_RecordLog` | tbLog | _G_CallmeLogic__SendLog |

## DLCLogic (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DLCLogic_CheckOpenAct` | — | _G_DLC_Logic__CheckOpenAct |

## ElementLogic (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ElementLogic_CheckOpenAct` | — | _G_ElementLogic__CheckOpenAct |

## Handbook (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Handbook_GetAward` | nIndex | _G_HandbookLogic__DoAward |

## Online (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Online_ClientLog` | AREnter, ARQuit | _G_ArLogic__RecordEnterLog<br>_G_ArLogic__RecordQuitLog |

## OnlineTowerRush (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineTowerRush_Equip` | nId, nOnlineId | _G_OnlineTowerRush__ReqEquip |

## ZoneTime (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ZoneTime_ReqTime` | — | _G_ZoneTime__ReqTime |

