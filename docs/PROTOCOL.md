# 客户端请求接口清单（CallGS）

> 由 `work/probe/scan_protocol.js` 从运行时 dump 的 Lua 5.4 字节码自动生成。
> 覆盖范围 = 当前 `work/_dump/` 里已 dump 的模块，不是全量。

共 **484** 个字面量接口 + **0** 个符号形式。

## BagRogue (24)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `BagRogue_AwardRefresh` | tbTalent | PROTO_G_BagRogue_AwardRefresh<br>PROTO_L__G_BagRogue_AwardRefresh |
| `BagRogue_CheckNewMapNode` | — | PROTO_G_BagRogue_CheckMapNode<br>PROTO_L__G_BagRogue_CheckMapNode |
| `BagRogue_CheckOpenAct` | — | PROTO_G_BagRogue_CheckOpenAct/_ENV<br>PROTO_L__G_BagRogue_CheckOpenAct/_ENV |
| `BagRogue_DoCraftItem` | nUniqueIdA, nUniqueIdB | PROTO_G_BagRogue_DoCraftItem<br>PROTO_L__G_BagRogue_DoCraftItem |
| `BagRogue_EnterLevel` | nID, tbLog | PROTO_G_BagRogue_EnterLevel<br>PROTO_L__G_BagRogue_EnterLevel |
| `BagRogue_EquipBag` | tbList, tbTalent | PROTO_G_BagRogue_DoEquipBag<br>PROTO_L__G_BagRogue_DoEquipBag |
| `BagRogue_ExFightLog` | BagRogueLevel | PROTO_G_BagRogue_LevelSettlement<br>PROTO_L__G_BagRogue_LevelSettlement |
| `BagRogue_FirstEnter` | — | PROTO_G_BagRogue_SetFirstEnter<br>PROTO_L__G_BagRogue_SetFirstEnter |
| `BagRogue_GetQuestAward` | tbIdList | PROTO_G_BagRogue_GetQuestAward<br>PROTO_L__G_BagRogue_GetQuestAward |
| `BagRogue_LevelMoppingUp` | nID, tbTalent | PROTO_G_BagRogue_LevelMoppingUp<br>PROTO_L__G_BagRogue_LevelMoppingUp |
| `BagRogue_LevelSelectAward` | nSelectIdx, tbTalent | PROTO_G_BagRogue_SelectLevelAward<br>PROTO_L__G_BagRogue_SelectLevelAward |
| `BagRogue_NodeFinish` | — | PROTO_G_BagRogue_NodeFinish<br>PROTO_L__G_BagRogue_NodeFinish |
| `BagRogue_NodeWalk` | nNodeId | PROTO_G_BagRogue_NodeWalk<br>PROTO_L__G_BagRogue_NodeWalk |
| `BagRogue_ReforgeItem` | nUniqueId, tbAffixIdx | PROTO_G_BagRogue_DoReforgeItem<br>PROTO_L__G_BagRogue_DoReforgeItem |
| `BagRogue_RefreshStore` | — | PROTO_G_BagRogue_StoreRefresh<br>PROTO_L__G_BagRogue_StoreRefresh |
| `BagRogue_RemoveExternStorageItem` | nUniqueId | PROTO_G_BagRogue_RemoveExternStorageItem<br>PROTO_L__G_BagRogue_RemoveExternStorageItem |
| `BagRogue_SaveItemToExternStorage` | nNodeId, nUniqueId | PROTO_G_BagRogue_SaveItemToExternStorage<br>PROTO_L__G_BagRogue_SaveItemToExternStorage |
| `BagRogue_SaveTrialCard` | tbTrial | PROTO_G_BagRogue_SaveTrialCard<br>PROTO_L__G_BagRogue_SaveTrialCard |
| `BagRogue_SelectAdventure` | nSelectIdx | PROTO_G_BagRogue_SelectAdventure/_ENV<br>PROTO_L__G_BagRogue_SelectAdventure/_ENV |
| `BagRogue_SelectCraftItem` | nIndex | PROTO_G_BagRogue_SelectCraftItem<br>PROTO_L__G_BagRogue_SelectCraftItem |
| `BagRogue_SelectExternStorageItem` | tbUniqueId | PROTO_G_BagRogue_SelectExternStorageItem<br>PROTO_L__G_BagRogue_SelectExternStorageItem |
| `BagRogue_SellItem` | nUniqueId | PROTO_G_BagRogue_SellItem<br>PROTO_L__G_BagRogue_SellItem |
| `BagRogue_StoreBuyItem` | nSelectIdx | PROTO_G_BagRogue_StoreBuyItem/_ENV<br>PROTO_L__G_BagRogue_StoreBuyItem/_ENV |
| `BagRogue_UpgradeItem` | nUniqueA, nUniqueB | PROTO_G_BagRogue_DoUpgradeItem<br>PROTO_L__G_BagRogue_DoUpgradeItem |

## Rogue3D (23)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Rogue3D_CheckOpenAct` | — | PROTO_G_Rogue3DLogic_Req_CheckOpenAct<br>PROTO_L__G_Rogue3DLogic_Req_CheckOpenAct |
| `Rogue3D_EnterLevel` | nDiffId, nTeamID, tbBuffList, tbLog, tbTeam | PROTO_G_Rogue3DLogic_Req_EnterLevel<br>PROTO_L__G_Rogue3DLogic_Req_EnterLevel |
| `Rogue3D_EnterSeasonLevel` | nDiffId, nTeamID, tbBuffList, tbLog, tbTeam | PROTO_G_Rogue3DLogic_Req_EnterSeasonLevel<br>PROTO_L__G_Rogue3DLogic_Req_EnterSeasonLevel |
| `Rogue3D_GetLevelAward` | tbIdList | PROTO_G_Rogue3DLogic_Req_GetLevelAward<br>PROTO_L__G_Rogue3DLogic_Req_GetLevelAward |
| `Rogue3D_GetQuestAward` | tbIdList | PROTO_G_Rogue3DLogic_Req_GetQuestAward<br>PROTO_L__G_Rogue3DLogic_Req_GetQuestAward |
| `Rogue3D_GetSeasonLotteryAward` | nIndex, nTimes | PROTO_G_Rogue3DLogic_Req_Gacha<br>PROTO_L__G_Rogue3DLogic_Req_Gacha |
| `Rogue3D_GetSeasonQuestAward` | tbIdList | PROTO_G_Rogue3DLogic_Req_GetSeasonQuestAward<br>PROTO_L__G_Rogue3DLogic_Req_GetSeasonQuestAward |
| `Rogue3D_LevelReset` | nDiffId, tbMember | PROTO_G_Rogue3DLogic_Req_LevelReset<br>PROTO_L__G_Rogue3DLogic_Req_LevelReset |
| `Rogue3D_MonsterRikiAward` | — | PROTO_G_Rogue3DLogic_ReqMonsterRikiAward<br>PROTO_L__G_Rogue3DLogic_ReqMonsterRikiAward |
| `Rogue3D_RecoverJourneySan` | — | PROTO_G_Rogue3DLogic_Req_RecoverJourneySan<br>PROTO_L__G_Rogue3DLogic_Req_RecoverJourneySan |
| `Rogue3D_RestrictTech` | nRestrict, nTechId | PROTO_G_Rogue3DLogic_Req_RestrictTech<br>PROTO_L__G_Rogue3DLogic_Req_RestrictTech |
| `Rogue3D_RoomSettlement` | nNodeId, tbKill, tbMonster | PROTO_G_Rogue3DLogic_Req_SendAchievementData<br>PROTO_L__G_Rogue3DLogic_Req_SendAchievementData |
| `Rogue3D_SaveFightData` | tbData | PROTO_G_Rogue3DSave_Reset<br>PROTO_G_Rogue3DSave_SaveReal |
| `Rogue3D_SaveSeasonFightData` | — | PROTO_G_Rogue3DSave_SaveReal<br>PROTO_L__G_Rogue3DSave_SaveReal |
| `Rogue3D_SeasonLevelReset` | nDiffId, tbMember | PROTO_G_Rogue3DLogic_Req_SeasonLevelReset<br>PROTO_L__G_Rogue3DLogic_Req_SeasonLevelReset |
| `Rogue3D_SeasonRoomSettlement` | nNodeId, tbKill, tbMonster | PROTO_G_Rogue3DLogic_Req_SendAchievementData<br>PROTO_G_Rogue3DLogic_Req_SendSeasonAchievementData |
| `Rogue3D_SelectDiff` | nDiffId | PROTO_G_Rogue3DLogic_Req_SelectDiff<br>PROTO_L__G_Rogue3DLogic_Req_SelectDiff |
| `Rogue3D_SelectMode` | nModeID | PROTO_G_Rogue3DLogic_Req_SelectMode<br>PROTO_L__G_Rogue3DLogic_Req_SelectMode |
| `Rogue3D_SelectSeasonTalent` | nTalentId | PROTO_G_Rogue3DLogic_Req_SelectSeasonTalent<br>PROTO_L__G_Rogue3DLogic_Req_SelectSeasonTalent |
| `Rogue3D_SelectTalent` | nTalentId | PROTO_G_Rogue3DLogic_Req_SelectTalent<br>PROTO_L__G_Rogue3DLogic_Req_SelectTalent |
| `Rogue3D_UnlockJourneyLine` | nLineID, nPeriodID | PROTO_G_Rogue3DAdventure_Req_UnlockJourneyLine<br>PROTO_L__G_Rogue3DAdventure_Req_UnlockJourneyLine |
| `Rogue3D_UpgradeTech` | nTechId | PROTO_G_Rogue3DLogic_Req_UpgradTech<br>PROTO_L__G_Rogue3DLogic_Req_UpgradTech |
| `Rogue3D_VisitJourneyNode` | nNodeID, nPeriodID | PROTO_G_Rogue3DAdventure_Req_VisitJourneyNode<br>PROTO_L__G_Rogue3DAdventure_Req_VisitJourneyNode |

## DarkZone (14)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DarkZone_CheckOpenAct` | — | PROTO_G_DarkZone_CheckOpenAct/_ENV<br>PROTO_L__G_DarkZone_CheckOpenAct/_ENV |
| `DarkZone_CompleteMission` | nChallengeId, nId, nMiniLevelId, nNpcId | PROTO_L_package_loaded_Challenge_DarkZone_ExploreMission_ReqCompleteMission<br>PROTO_L__G_ExploreMission_ReqCompleteMission |
| `DarkZone_EndExplore` | nLevelID | PROTO_G_DarkZone_EndExplore<br>PROTO_L__G_DarkZone_EndExplore |
| `DarkZone_EnterLevel` | nLevelID, tbLog | PROTO_G_DarkZone_Req_EnterLevel<br>PROTO_L__G_DarkZone_Req_EnterLevel |
| `DarkZone_EnterMiniLevel` | nLevelID | PROTO_G_DarkZone_Req_EnterMiniLevel<br>PROTO_L__G_DarkZone_Req_EnterMiniLevel |
| `DarkZone_ExchangeData` | nLevelID | PROTO_G_DarkZone_Exchange<br>PROTO_L__G_DarkZone_Exchange |
| `DarkZone_ExchangeKey` | nLevelID, nNum | PROTO_G_DarkZone_ExchangeKey<br>PROTO_L__G_DarkZone_ExchangeKey |
| `DarkZone_GetGainReward` | dataId, nGainId, nLevelID | PROTO_G_DarkZone_GetGainReward<br>PROTO_L__G_DarkZone_GetGainReward |
| `DarkZone_GetLevelAward` | tbIdList | PROTO_G_DarkZone_DoGetAward<br>PROTO_L__G_DarkZone_DoGetAward |
| `DarkZone_GetMissionAward` | nId | PROTO_L_package_loaded_Challenge_DarkZone_ExploreMission_ReqMissionAward<br>PROTO_L__G_ExploreMission_ReqMissionAward |
| `DarkZone_LeaveLevel` | tbLog | PROTO_G_DarkZone_Req_LeaveLevel<br>PROTO_L__G_DarkZone_Req_LeaveLevel |
| `DarkZone_RefreshMission` | — | PROTO_L_package_loaded_Challenge_DarkZone_ExploreMission_ReqRefreshEntrust<br>PROTO_L__G_ExploreMission_ReqRefreshEntrust |
| `DarkZone_SaveFightData` | bRS, nLevelID, nSaveType, tbData | PROTO_G_DarkZone_SaveFightData<br>PROTO_L__G_DarkZone_SaveFightData |
| `DarkZone_TrackingMission` | bClose, nId | PROTO_L_package_loaded_Challenge_DarkZone_ExploreMission_ReqTrackingMission<br>PROTO_L__G_ExploreMission_ReqTrackingMission |

## StarWish (13)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `StarWish_AutoCompleteStoryQuest` | nID | PROTO_G_StarWishLogic_AutoCompleteStoryQuest<br>PROTO_L__G_StarWishLogic_AutoCompleteStoryQuest |
| `StarWish_CheckOpenAct` | — | PROTO_G_StarWishLogic_CheckOpenAct/_ENV<br>PROTO_L__G_StarWishLogic_CheckOpenAct/_ENV |
| `StarWish_CleanSubIDCompleted` | nID | PROTO_G_StarWishLogic_CleanSubIDCompleted<br>PROTO_L__G_StarWishLogic_CleanSubIDCompleted |
| `StarWish_CompleteShareAchievement` | — | PROTO_G_StarWishLogic_CompleteShareAchievement<br>PROTO_L__G_StarWishLogic_CompleteShareAchievement |
| `StarWish_GetAllCompleteAward` | — | PROTO_G_StarWishLogic_GetAllCompleteAward<br>PROTO_L__G_StarWishLogic_GetAllCompleteAward |
| `StarWish_GetRepeatQuestAward` | tbTaskID | PROTO_G_StarWishLogic_GetRepeatQuestAward<br>PROTO_L__G_StarWishLogic_GetRepeatQuestAward |
| `StarWish_GetRepeatQuestExtraAward` | nPos | PROTO_G_StarWishLogic_GetRepeatQuestExtraAward<br>PROTO_L__G_StarWishLogic_GetRepeatQuestExtraAward |
| `StarWish_GetScoreAward` | — | PROTO_G_StarWishLogic_GetScoreAward<br>PROTO_L__G_StarWishLogic_GetScoreAward |
| `StarWish_GetStoryPageAward` | nID | PROTO_G_StarWishLogic_GetStoryPageAward<br>PROTO_L__G_StarWishLogic_GetStoryPageAward |
| `StarWish_GetStoryQuestAward` | tbID | PROTO_G_StarWishLogic_GetStoryQuestAward<br>PROTO_L__G_StarWishLogic_GetStoryQuestAward |
| `StarWish_LotteryJigsaw` | nTimes | PROTO_G_StarWishLogic_LotteryJigsaw<br>PROTO_L__G_StarWishLogic_LotteryJigsaw |
| `StarWish_SetStoryQuestCompleted` | Value, bShowPop, nID | PROTO_G_StarWishLogic_SetStoryQuestCompleted<br>PROTO_L__G_StarWishLogic_SetStoryQuestCompleted |
| `StarWish_SetSubIDCompleted` | bShowPop, nID, nPos, v | PROTO_G_StarWishLogic_SetSubIDCompleted<br>PROTO_L__G_StarWishLogic_SetSubIDCompleted |

## DreamCard (12)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DreamCard_CheckOpen` | — | PROTO_G_DreamCard_CheckOpen<br>PROTO_L__G_DreamCard_CheckOpen |
| `DreamCard_CleanData` | — | PROTO_G_DreamCard_CleanData<br>PROTO_L__G_DreamCard_CleanData |
| `DreamCard_EndlessLevelSettlement` | nID, nType, tbLog, tbUpScore | PROTO_G_DreamCard_EndlessLevelSettlement<br>PROTO_L__G_DreamCard_EndlessLevelSettlement |
| `DreamCard_EnterLevel` | nDiff, nID, nRoleId, nType | PROTO_G_DreamCard_EnterLevel<br>PROTO_L__G_DreamCard_EnterLevel |
| `DreamCard_LevelOut` | nDiff, nID, nSeed, nType, tbLog | PROTO_G_DreamCard_LevelOut<br>PROTO_L__G_DreamCard_LevelOut |
| `DreamCard_QuickGetReward` | tbIdList | PROTO_G_DreamCard_DoGetMission<br>PROTO_L__G_DreamCard_DoGetMission |
| `DreamCard_QuickGetScoreReward` | nId, tbIdList | PROTO_G_DreamCard_DoGetScoreMission<br>PROTO_L__G_DreamCard_DoGetScoreMission |
| `DreamCard_QuickGetStarReward` | tbIdList | PROTO_G_DreamCard_DoGetStarMission<br>PROTO_L__G_DreamCard_DoGetStarMission |
| `DreamCard_ResetTalent` | nID, nTab | PROTO_G_DreamCard_ResetTalent<br>PROTO_L__G_DreamCard_ResetTalent |
| `DreamCard_UnlockTalent` | nID | PROTO_G_DreamCard_UnlockTalent<br>PROTO_L__G_DreamCard_UnlockTalent |
| `DreamCard_UpdateData` | — | PROTO_G_DreamCard_ChackAddData<br>PROTO_G_DreamCard_UpdateData |
| `DreamCard_UpdateData3` | — | PROTO_G_DreamCard_UpdateData3<br>PROTO_L__G_DreamCard_UpdateData3 |

## FarmWarLogic (12)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `FarmWarLogic_ActiveGrowNode` | nId, nSkillId | PROTO_G_FarmWarActivity_Req_ActiveGrowNode<br>PROTO_L__G_FarmWarActivity_Req_ActiveGrowNode |
| `FarmWarLogic_ActiveLimitGrowNode` | nId, nSkillId | PROTO_G_FarmWarActivity_Req_ActiveLimitGrowNode<br>PROTO_L__G_FarmWarActivity_Req_ActiveLimitGrowNode |
| `FarmWarLogic_CheckActOpen` | — | PROTO_G_FarmWarActivity_Req_CheckActOpen<br>PROTO_L__G_FarmWarActivity_Req_CheckActOpen |
| `FarmWarLogic_EnterLevel` | nID, nTeamID, tbLog | PROTO_G_FarmWarActivity_Req_EnterLevel<br>PROTO_L__G_FarmWarActivity_Req_EnterLevel |
| `FarmWarLogic_GetQuestAward` | tbIdList | PROTO_G_FarmWarActivity_Req_GetQuestAward<br>PROTO_L__G_FarmWarActivity_Req_GetQuestAward |
| `FarmWarLogic_LevelFail` | B, F, K, P, U, nID, tbLog | PROTO_G_FarmWarActivity_Req_LevelFail<br>PROTO_L__G_FarmWarActivity_Req_LevelFail |
| `FarmWarLogic_ResetGrow` | nId, nType | PROTO_G_FarmWarActivity_Req_ResetGrow<br>PROTO_L__G_FarmWarActivity_Req_ResetGrow |
| `FarmWarLogic_ResetGrowNode` | nId, nSkillId | PROTO_G_FarmWarActivity_Req_ResetGrowNode<br>PROTO_L__G_FarmWarActivity_Req_ResetGrowNode |
| `FarmWarLogic_ResetLimitGrow` | nId | PROTO_G_FarmWarActivity_Req_ResetLimitGrow<br>PROTO_L__G_FarmWarActivity_Req_ResetLimitGrow |
| `FarmWarLogic_ResetLimitGrowNode` | nId, nSkillId | PROTO_G_FarmWarActivity_Req_ResetLimitGrowNode<br>PROTO_L__G_FarmWarActivity_Req_ResetLimitGrowNode |
| `FarmWarLogic_SwitchLimitGrowNode` | — | PROTO_G_FarmWarActivity_Req_SwitchLimitGrowNode<br>PROTO_L__G_FarmWarActivity_Req_SwitchLimitGrowNode |
| `FarmWarLogic_UpdateFormation` | nLevelId, tbTeam | PROTO_G_FarmWarActivity_Req_UpdateFormation<br>PROTO_L__G_FarmWarActivity_Req_UpdateFormation |

## (无前缀) (11)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ChangeMainScene` | bClearRandom, nId | PROTO_G_PreviewMain_Req_ChangeMainScene<br>PROTO_L__G_PreviewMain_Req_ChangeMainScene |
| `DownloadMultMediaLog` | tbLog | PROTO_G_Mail_DownloadMultiMediaLog<br>PROTO_G_ShareLogic_SendLog |
| `EnterGirlRoom` | nCardId, nSkinId | PROTO_G_PreviewSkin_Req_EnterGirlRoom<br>PROTO_L__G_PreviewSkin_Req_EnterGirlRoom |
| `ExtendFightDynamicLog` | tbLog | PROTO_G_BagRogue_LevelSettlement<br>PROTO_G_BossLogic_Req_LevelFail |
| `ExtendFightLog` | tbLog | PROTO_G_BagRogue_LevelSettlement<br>PROTO_G_BossLogic_Req_LevelFail |
| `FavMailLog` | tbLog | PROTO_G_FightLevel_WriteSequenceLog<br>PROTO_L__G_FightLevel_WriteSequenceLog |
| `GirlRoomLog` | sLog | PROTO_G_PreviewSkin_ReportLog<br>PROTO_L__G_PreviewSkin_ReportLog |
| `LanguageChange` | nType, sEx, sLan | PROTO_G_Localization_NotifyLanSetting<br>PROTO_L__G_Localization_NotifyLanSetting |
| `RecordConfession` | nIdx | PROTO_G_PreviewSkin_Req_RecordConfession<br>PROTO_L__G_PreviewSkin_Req_RecordConfession |
| `ReqEntranceGreenLevel` | — | PROTO_G_PreviewSkin_ReqEntranceGreenLevel<br>PROTO_L__G_PreviewSkin_ReqEntranceGreenLevel |
| `SettingChange` | — | PROTO_G_PlayerSetting_Save<br>PROTO_L__G_PlayerSetting_Save |

## DonoDuel (11)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DonoDuel_ChangeFormation` | bNotRefresh, nType, tbFormation | PROTO_G_DonoDuel_DoChangeFightFormation<br>PROTO_G_DonoDuel_DoChangeFormation |
| `DonoDuel_ClientCheck` | — | PROTO_G_DonoDuel_DoCheckOpen<br>PROTO_L__G_DonoDuel_DoCheckOpen |
| `DonoDuel_LockSkill` | bLock, nLockSkillPos, nUniqueId | PROTO_G_DonoDuel_DoLockSkill<br>PROTO_L__G_DonoDuel_DoLockSkill |
| `DonoDuel_Recycle` | tbRecycle | PROTO_G_DonoDuel_DoRecycle<br>PROTO_L__G_DonoDuel_DoRecycle |
| `DonoDuel_SetLock` | bLock, nUniqueId | PROTO_G_DonoDuel_DoLockAndUnlock<br>PROTO_L__G_DonoDuel_DoLockAndUnlock |
| `DonoDuel_StudySkillTree` | nSkillId | PROTO_G_DonoDuel_DoStudySkillTree<br>PROTO_L__G_DonoDuel_DoStudySkillTree |
| `DonoDuel_UpgradeAttr` | nPos, nUniqueId | PROTO_G_DonoDuel_DoUpgradeAttr<br>PROTO_L__G_DonoDuel_DoUpgradeAttr |
| `DonoDuel_UpgradeLeaderSkill` | nSkillId | PROTO_G_DonoDuel_DoUpgradeLeaderSkill<br>PROTO_L__G_DonoDuel_DoUpgradeLeaderSkill |
| `DonoDuel_UpgradeQuality` | nUniqueId | PROTO_G_DonoDuel_DoUpgradeQuality<br>PROTO_L__G_DonoDuel_DoUpgradeQuality |
| `DonoDuel_UpgradeSkill` | bResetAll, nPos, nSkillId, nUniqueId, tbGiveUpSkill | PROTO_G_DonoDuel_DoUpgradeSkill<br>PROTO_L__G_DonoDuel_DoUpgradeSkill |
| `DonoDuel_UpgradeStar` | nSourStar, nUniqueId, tbMaterial | PROTO_G_DonoDuel_DoUpgradeStar<br>PROTO_L__G_DonoDuel_DoUpgradeStar |

## RogueLogic (11)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RogueLogic_ChangeFormation` | tbFormation | PROTO_L_package_loaded_DLC_Rogue_Rogue_SetRogueLineup<br>PROTO_L__G_RogueLogic_SetRogueLineup |
| `RogueLogic_ClientMoveNext` | nID | PROTO_L_package_loaded_DLC_Rogue_Rogue_MoveNext<br>PROTO_L__G_RogueLogic_MoveNext |
| `RogueLogic_EnterRogue` | — | PROTO_L_package_loaded_DLC_Rogue_Rogue_EnterRogue<br>PROTO_L__G_RogueLogic_EnterRogue |
| `RogueLogic_FetchDailyBuff` | — | PROTO_L_package_loaded_DLC_Rogue_Rogue_FetchDailyBuff<br>PROTO_L__G_RogueLogic_FetchDailyBuff |
| `RogueLogic_FinishNode` | — | PROTO_L_package_loaded_DLC_Rogue_Rogue_FinishNode<br>PROTO_L__G_RogueLogic_FinishNode |
| `RogueLogic_QuickGetReward` | tbIdList | PROTO_L_package_loaded_DLC_Rogue_Rogue_QuickGetReward<br>PROTO_L__G_RogueLogic_QuickGetReward |
| `RogueLogic_RefreshShopGoods` | nNodeID | PROTO_L_package_loaded_DLC_Rogue_Rogue_RefreshShopGoods<br>PROTO_L__G_RogueLogic_RefreshShopGoods |
| `RogueLogic_ResetRogue` | — | PROTO_L_package_loaded_DLC_Rogue_Rogue_ResetRogue<br>PROTO_L__G_RogueLogic_ResetRogue |
| `RogueLogic_ReviveRole` | — | PROTO_L_package_loaded_DLC_Rogue_Rogue_ReviveRole<br>PROTO_L__G_RogueLogic_ReviveRole |
| `RogueLogic_ShowOpenStory` | — | PROTO_L_Launch_Classes_RogueLogic_OnSettlement<br>PROTO_L_package_loaded_Launch_Classes_RogueLogic_OnSettlement |
| `RogueLogic_VisitShop` | nNodeID | PROTO_L_package_loaded_DLC_Rogue_Rogue_VisitShop<br>PROTO_L__G_RogueLogic_VisitShop |

## Weapon (11)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Weapon_Break` | Id | PROTO_L_package_loaded_Item_Weapon_Req_Break<br>PROTO_L__G_Weapon_Req_Break |
| `Weapon_Evolution` | Id, nItemId | PROTO_L_package_loaded_Item_Weapon_Req_Evolution<br>PROTO_L__G_Weapon_Req_Evolution |
| `Weapon_Exchange` | CardIdA, CardIdB | PROTO_L_package_loaded_Item_Weapon_Req_Exchange<br>PROTO_L__G_Weapon_Req_Exchange |
| `Weapon_GetUpgradePartUnlock` | gdpl, nWeaponId, weapon | PROTO_L_package_loaded_Item_Weapon_Req_GetUpgradePartUnlock<br>PROTO_L__G_Weapon_Req_GetUpgradePartUnlock |
| `Weapon_OneKeyToMax` | Id, tbBreakUpgradeMat | PROTO_L_package_loaded_Item_Weapon_Req_OneKeyToMax<br>PROTO_L__G_Weapon_Req_OneKeyToMax |
| `Weapon_Replace` | CardId, Id | PROTO_L_package_loaded_Item_Weapon_Req_Replace<br>PROTO_L__G_Weapon_Req_Replace |
| `Weapon_ReplacePart` | Id, PartId, Type | PROTO_L_package_loaded_Item_Weapon_Req_ReplacePart<br>PROTO_L__G_Weapon_Req_ReplacePart |
| `Weapon_SetAssignShowDefaultPart` | Id, nFlag, nType | PROTO_L_package_loaded_Item_Weapon_Req_SetAssignShowDefaultPart<br>PROTO_L__G_Weapon_Req_SetAssignShowDefaultPart |
| `Weapon_SetDefaultAudio` | Id, nFlag | PROTO_L_package_loaded_Item_Weapon_Req_SetDefaultAudio<br>PROTO_L__G_Weapon_Req_SetDefaultAudio |
| `Weapon_ShowDefaultPart` | Id, nFlag | PROTO_L_package_loaded_Item_Weapon_Req_SetShowDefaultPart<br>PROTO_L__G_Weapon_Req_SetShowDefaultPart |
| `Weapon_Upgrade` | Id, tbMat | PROTO_L_package_loaded_Item_Weapon_Req_Upgrade<br>PROTO_L__G_Weapon_Req_Upgrade |

## Activity (9)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Activity_BirthdayMail_Gain` | — | PROTO_G_BirthdayMail_RequestMail<br>PROTO_L__G_BirthdayMail_RequestMail |
| `Activity_Flag` | nId, nType | PROTO_L_Activity_Activity_Quest_Flag<br>PROTO_L__G_Activity_Quest_Flag |
| `Activity_GetAward` | — | PROTO_L_Activity_Activity_Quest_GetAward<br>PROTO_L__G_Activity_Quest_GetAward |
| `Activity_GetRoleFestivalLevelReward` | nId, nMessageNum | PROTO_L_package_loaded_Activity_RoleFestivalMessage_GetLevelReward<br>PROTO_L__G_RoleFestivalMessage_GetLevelReward |
| `Activity_MarkTip` | nGId, nSubId | PROTO_L_package_loaded_Activity_Sign_Req_MarkActivityTip<br>PROTO_L__G_Sign_Req_MarkActivityTip |
| `Activity_QuickQuestAward` | nId, tbIdList | PROTO_L_Activity_Activity_Quick_QuestAward<br>PROTO_L__G_Activity_Quick_QuestAward |
| `Activity_Refresh` | nId | PROTO_L_Activity_Activity_Quest_Refresh<br>PROTO_L__G_Activity_Quest_Refresh |
| `Activity_ReSign` | nId, nType | PROTO_L_package_loaded_Activity_Sign_DoResign<br>PROTO_L__G_Sign_DoResign |
| `Activity_SetRoleFestivalMessageBeRead` | nGirlId | PROTO_L_package_loaded_Activity_RoleFestivalMessage_SetMessageReadState<br>PROTO_L__G_RoleFestivalMessage_SetMessageReadState |

## AlienDefense (9)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `AlienDefense_CheckOpenAct` | — | PROTO_G_AlienDefense_CheckOpenAct/_ENV<br>PROTO_L__G_AlienDefense_CheckOpenAct/_ENV |
| `AlienDefense_EnterLevel` | nID, tbLog | PROTO_G_AlienDefense_EnterLevel<br>PROTO_L__G_AlienDefense_EnterLevel |
| `AlienDefense_GetQuestAward` | tbIdList | PROTO_G_AlienDefense_GetQuestAward<br>PROTO_L__G_AlienDefense_GetQuestAward |
| `AlienDefense_GetScoreAward` | nIdx | PROTO_G_AlienDefense_GetScoreAward<br>PROTO_L__G_AlienDefense_GetScoreAward |
| `AlienDefense_LevelFail` | tbLog | PROTO_G_AlienDefense_LevelFail<br>PROTO_L__G_AlienDefense_LevelFail |
| `AlienDefense_SaveFightGirl` | nGirlId | PROTO_G_AlienDefense_SaveFightGirl<br>PROTO_L__G_AlienDefense_SaveFightGirl |
| `AlienDefense_SaveFightPal` | tbPalIdx | PROTO_G_AlienDefense_SaveFightPal<br>PROTO_L__G_AlienDefense_SaveFightPal |
| `AlienDefense_SetPalFlag` | — | PROTO_G_AlienDefense_SetPalFlag<br>PROTO_L__G_AlienDefense_SetPalFlag |
| `AlienDefense_UpgradeSkill` | nPalIdx, nSkillIdx | PROTO_G_AlienDefense_UpgradeSkill<br>PROTO_L__G_AlienDefense_UpgradeSkill |

## PartyLogic (9)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `PartyLogic_CheckFirstSign` | nId, nTeach | PROTO_G_PartyLogic_CheckFirstSign<br>PROTO_L__G_PartyLogic_CheckFirstSign |
| `PartyLogic_SetFightCard` | nId | PROTO_G_PartyLogic_SetFightCard<br>PROTO_L__G_PartyLogic_SetFightCard |
| `PartyLogic_SetFirstSign` | nId | PROTO_G_PartyLogic_SetFirstSign<br>PROTO_L__G_PartyLogic_SetFirstSign |
| `PartyLogic_SetMatchId` | nId | PROTO_G_PartyLogic_SetMatchId<br>PROTO_L__G_PartyLogic_SetMatchId |
| `PartyLogic_SetMatchMode` | nSingle | PROTO_G_PartyLogic_SetMatchMode<br>PROTO_L__G_PartyLogic_SetMatchMode |
| `PartyLogic_SetRandomMapId` | nId, nSetData, nSingle, tbMapId | PROTO_G_PartyLogic_SetRandomMapId<br>PROTO_L__G_PartyLogic_SetRandomMapId |
| `PartyLogic_SetSkillID` | nId1, nId2 | PROTO_G_PartyLogic_SetFightSkill<br>PROTO_L__G_PartyLogic_SetFightSkill |
| `PartyLogic_SetTitle` | nId | PROTO_G_PartyLogic_SetTitle<br>PROTO_L__G_PartyLogic_SetTitle |
| `PartyLogic_SetTitleShow` | nType | PROTO_G_PartyLogic_SetTitleShow<br>PROTO_L__G_PartyLogic_SetTitleShow |

## SupporterCard (9)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `SupporterCard_Break` | Id, tbMaterials | PROTO_L_Item_Logistics_Req_BreakLogistics |
| `SupporterCard_Equip` | BEqId, EqId, EqSlot, Model, bForce, beEqId | PROTO_L_Item_Logistics_Req_Equip<br>PROTO_L_Item_Logistics_Req_EquipChange |
| `SupporterCard_FixedResetInitialAffix` | FixedId, Id, Index | PROTO_L_Item_Logistics_Req_ResetInitialAffix |
| `SupporterCard_ReceiveFixedItem` | — | PROTO_L_Item_Logistics_Req_ReceiveFixedItem |
| `SupporterCard_ResetAffix` | Id | PROTO_L_Item_Logistics_Req_ResetAffix |
| `SupporterCard_ResetInitialAffix` | FixedId, Id, Index | PROTO_L_Item_Logistics_Req_ResetInitialAffix |
| `SupporterCard_SelectAffix` | Id, SelectNew | PROTO_L_Item_Logistics_Req_SelectAffix |
| `SupporterCard_SelectInitialAffix` | Id, Index, SelectNew | PROTO_L_Item_Logistics_Req_SelectInitialAffix |
| `SupporterCard_Upgrade` | Id, tbMaterials | PROTO_L_Item_Logistics_Req_UpLogistics |

## VirCapture (9)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `VirCapture_ChangeBagRedFlag` | bFlag | PROTO_G_VirCapture_DoChangeBagRedFlag<br>PROTO_L__G_VirCapture_DoChangeBagRedFlag |
| `VirCapture_ChangeFormation` | nId, nUnloadId | PROTO_G_VirCapture_DoChangeFormation<br>PROTO_L__G_VirCapture_DoChangeFormation |
| `VirCapture_CheckOpenAct` | — | PROTO_G_VirCapture_CheckOpenAct/_ENV<br>PROTO_L__G_VirCapture_CheckOpenAct/_ENV |
| `VirCapture_GachaMonster` | bTen | PROTO_G_VirCapture_DoGachaMonster<br>PROTO_L__G_VirCapture_DoGachaMonster |
| `VirCapture_GetLevelAward` | nId, tbIdList | PROTO_G_VirCapture_DoGetLevelAward<br>PROTO_L__G_VirCapture_DoGetLevelAward |
| `VirCapture_GetRikiAward` | nId, tbIdList | PROTO_G_VirCapture_DoGetRikiAward<br>PROTO_L__G_VirCapture_DoGetRikiAward |
| `VirCapture_SetLock` | MonsterId, bLock | PROTO_G_VirCapture_DoLockAndUnlock<br>PROTO_L__G_VirCapture_DoLockAndUnlock |
| `VirCapture_SwitchDayNight` | nMapId | PROTO_G_VirCapture_DoSwitchDayNight<br>PROTO_L__G_VirCapture_DoSwitchDayNight |
| `VirCapture_UpgradeLevel` | nId, nSkillId | PROTO_G_VirCapture_DoUpgradeLevel<br>PROTO_L__G_VirCapture_DoUpgradeLevel |

## GirlCard (8)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GirlCard_ProLevelPromote` | nID | PROTO_L_package_loaded_UMG_Role_RoleCard_ProLevelPromote<br>PROTO_L__G_RoleCard_ProLevelPromote |
| `GirlCard_ReceiveProLevelAward` | nID, nProLevel | PROTO_L_package_loaded_UMG_Role_RoleCard_ReceiveProLevelAward<br>PROTO_L__G_RoleCard_ReceiveProLevelAward |
| `GirlCard_SetRoleLeave` | nValue, tbID | PROTO_L_package_loaded_UMG_Role_RoleCard_SetAllRoleLeave<br>PROTO_L_package_loaded_UMG_Role_RoleCard_SetRoleLeave |
| `GirlCard_SetRoleLikeFlag` | nCardID, nFlag | PROTO_L_package_loaded_UMG_Role_RoleCard_Req_SetRoleLikeFlag<br>PROTO_L__G_RoleCard_Req_SetRoleLikeFlag |
| `GirlCard_UnLockCharacter` | d, g, l, p | PROTO_L_package_loaded_UMG_Role_RoleCard_Req_UnLockPlayer<br>PROTO_L__G_RoleCard_Req_UnLockPlayer |
| `GirlCard_UpByBreak` | nBreakLv, pId, tbMaterials | PROTO_L_package_loaded_Item_RoleBreak_Req_ByBreak<br>PROTO_L__G_RBreak_Req_ByBreak |
| `GirlCard_UpBySpecialBreak` | nCardId | PROTO_L_package_loaded_Item_RoleBreak_Req_BySpecialBreak<br>PROTO_L__G_RBreak_Req_BySpecialBreak |
| `GirlCard_UpdateLevel` | Id, tbMaterials | PROTO_L_package_loaded_UMG_Role_RoleCard_Req_LevelUp<br>PROTO_L__G_RoleCard_Req_LevelUp |

## RichManLoveLogic (8)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RichManLoveLogic_CheckOpenAct` | — | PROTO_G_RichManLoveLogic_CheckOpenAct<br>PROTO_L__G_RichManLoveLogic_CheckOpenAct |
| `RichManLoveLogic_EnterMap` | bContinue, nId, nMapId | PROTO_G_RichManLoveLogic_EnterMap<br>PROTO_L__G_RichManLoveLogic_EnterMap |
| `RichManLoveLogic_EnterMapLog` | nMapId, nSeed, tbLog | PROTO_G_RichManLoveLogic_EnterMapLog<br>PROTO_L__G_RichManLoveLogic_EnterMapLog |
| `RichManLoveLogic_LikeEnd` | nId | PROTO_G_RichManLoveLogic_LikeEnd<br>PROTO_L__G_RichManLoveLogic_LikeEnd |
| `RichManLoveLogic_MapSettlement` | activityId, activityType, mapId, nSeed, tbLevelNum | PROTO_G_RichManLoveLogic_MapSettlement<br>PROTO_L__G_RichManLoveLogic_MapSettlement |
| `RichManLoveLogic_QuickGetReward` | tbIdList | PROTO_G_RichmanLogic_DoGetMission<br>PROTO_L__G_RichmanLogic_DoGetMission |
| `RichManLoveLogic_SettlementUnlockEnd` | nId, nMapId, tbLog | PROTO_G_RichManLoveLogic_SettlementUnlockEnd<br>PROTO_L__G_RichManLoveLogic_SettlementUnlockEnd |
| `RichManLoveLogic_UseDice` | — | PROTO_G_RichManLoveLogic_UseDice<br>PROTO_L__G_RichManLoveLogic_UseDice |

## BossLogic (7)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `BossLogic_EnterLevel` | nDifficulty, nID, nTeamID, tbEntrie, tbLog | PROTO_G_BossLogic_Req_EnterLevel<br>PROTO_L__G_BossLogic_Req_EnterLevel |
| `BossLogic_GetOpenID` | — | PROTO_G_BossLogic_GetOpenID/_ENV<br>PROTO_L__G_BossLogic_GetOpenID/_ENV |
| `BossLogic_GetReward` | Mileage | PROTO_G_BossLogic_GetReward<br>PROTO_L__G_BossLogic_GetReward |
| `BossLogic_LevelFail` | nID, tbLog | PROTO_G_BossLogic_Req_LevelFail<br>PROTO_L__G_BossLogic_Req_LevelFail |
| `BossLogic_OneClicReward` | — | PROTO_G_BossLogic_OneClicReward<br>PROTO_L__G_BossLogic_OneClicReward |
| `BossLogic_Record` | bRecord, nID, nSeed, nTime | PROTO_G_BossLogic_Record<br>PROTO_L__G_BossLogic_Record |
| `BossLogic_Reset` | nID | PROTO_G_BossLogic_Reset<br>PROTO_L__G_BossLogic_Reset |

## Chapter (7)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Chapter_DealLevelSettlement` | — | PROTO_G_Reconnect_Send_SettleInfo<br>PROTO_G_Reconnect_Tick_SettleInfo |
| `Chapter_EnterLevel` | bFree, nID, nMultiple, nTeamID, tbLog | PROTO_G_Chapter_Req_EnterLevel<br>PROTO_L__G_Chapter_Req_EnterLevel |
| `Chapter_GetStarAward` | bMain, nChapterID, nDifficult, nIndex | PROTO_G_Chapter_Req_GetStarAward<br>PROTO_L__G_Chapter_Req_GetStarAward |
| `Chapter_LevelFail` | nID, tbLog | PROTO_G_Chapter_Req_LevelFail<br>PROTO_L__G_Chapter_Req_LevelFail |
| `Chapter_NewPrologueEnterLevel` | bFree, nID, nMultiple, nTeamID, tbLog | PROTO_G_Chapter_Req_NewPrologue_EnterLevel<br>PROTO_L__G_Chapter_Req_NewPrologue_EnterLevel |
| `Chapter_NewPrologueSettlement` | bWaitServer, nID, nSeed, nTime, tbLog | PROTO_G_Chapter_Req_NewPrologueSettlement<br>PROTO_L__G_Chapter_Req_NewPrologueSettlement |
| `Chapter_SyncGuideLevelPassData` | tbData | PROTO_G_Chapter_SyncGuideLevelPassData<br>PROTO_L__G_Chapter_SyncGuideLevelPassData |

## JigsawPuzzle (7)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `JigsawPuzzle_EnterLog` | nEnterType, nId | PROTO_G_JigsawPuzzle_EnterLog<br>PROTO_L__G_JigsawPuzzle_EnterLog |
| `JigsawPuzzle_GetGirl` | nId | PROTO_G_JigsawPuzzle_GetGirl<br>PROTO_L__G_JigsawPuzzle_GetGirl |
| `JigsawPuzzle_GetPiece` | nActivityId, nId, nNum, nStage | PROTO_G_JigsawPuzzle_GetPiece<br>PROTO_L__G_JigsawPuzzle_GetPiece |
| `JigsawPuzzle_GetReward` | nActId, nId | PROTO_G_JigsawPuzzle_GetMissionReward<br>PROTO_L__G_JigsawPuzzle_GetMissionReward |
| `JigsawPuzzle_PutPiece` | nActId, nId | PROTO_G_JigsawPuzzle_PutPiece<br>PROTO_L__G_JigsawPuzzle_PutPiece |
| `JigsawPuzzle_SetActive` | nId | PROTO_G_JigsawPuzzle_SetActive<br>PROTO_L__G_JigsawPuzzle_SetActive |
| `JigsawPuzzle_UseHelp` | nActId, nId | PROTO_G_JigsawPuzzle_UseHelp<br>PROTO_L__G_JigsawPuzzle_UseHelp |

## ClimbTowerLogic (6)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ClimbTowerLogic_CheckCycleLevel` | — | PROTO_G_ClimbTowerLogic_CheckCycleLevel/_ENV<br>PROTO_L__G_ClimbTowerLogic_CheckCycleLevel/_ENV |
| `ClimbTowerLogic_GetReward` | nGroup, nLayer, nType | PROTO_G_ClimbTowerLogic_GetReward<br>PROTO_L__G_ClimbTowerLogic_GetReward |
| `ClimbTowerLogic_OneClicReward` | nGroup, nType | PROTO_G_ClimbTowerLogic_OneClicReward<br>PROTO_L__G_ClimbTowerLogic_OneClicReward |
| `ClimbTowerLogic_RecordChallenged` | nID | PROTO_G_ClimbTowerLogic_RecordChallenged<br>PROTO_L__G_ClimbTowerLogic_RecordChallenged |
| `ClimbTowerLogic_RecordProgres` | nArea, nID, nStar, nTeamEnergy, tbRoleHP | PROTO_G_ClimbTowerLogic_RecordProgres<br>PROTO_L__G_ClimbTowerLogic_RecordProgres |
| `ClimbTowerLogic_SetLevelDiff` | nDiff | PROTO_G_ClimbTowerLogic_SetLevelDiff<br>PROTO_L__G_ClimbTowerLogic_SetLevelDiff |

## Daily (6)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Daily_EnterLevel` | nChapterID, nID, nLevelID, nMultiple, nTeamID, tbLog | PROTO_G_Daily_Req_EnterLevel<br>PROTO_L__G_Daily_Req_EnterLevel |
| `Daily_GetActivityInfo` | — | PROTO_G_Daily_Req_GetActivityInfo<br>PROTO_L__G_Daily_Req_GetActivityInfo |
| `Daily_GetGuaranteeReward` | Suit, Type, bDlc | PROTO_G_Daily_GetGuaranteeReward<br>PROTO_L__G_Daily_GetGuaranteeReward |
| `Daily_LevelFail` | nID, tbLog | PROTO_G_Daily_Req_LevelFail<br>PROTO_L__G_Daily_Req_LevelFail |
| `Daily_LevelMoppingUp` | nChapterID, nID, nLevelID, nMultiple, nTeamID | PROTO_G_Daily_Req_LevelMopup<br>PROTO_L__G_Daily_Req_LevelMopup |
| `Daily_SetSelectSuit` | Suit, Type, bDlc | PROTO_G_Daily_SetSelectSuit<br>PROTO_L__G_Daily_SetSelectSuit |

## ElementLogic (6)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ElementLogic_BuyGoods` | nGoodsID | PROTO_G_ElementLogic_Req_BuyGoods<br>PROTO_L__G_ElementLogic_Req_BuyGoods |
| `ElementLogic_CheckOpenAct` | — | PROTO_G_ElementLogic_CheckOpenAct<br>PROTO_L__G_ElementLogic_CheckOpenAct |
| `ElementLogic_EnterLevel` | nID, nMultiple, nTeamID, tbLog | PROTO_G_ElementLogic_Req_EnterLevel<br>PROTO_L__G_ElementLogic_Req_EnterLevel |
| `ElementLogic_Harvest` | — | PROTO_G_ElementLogic_Req_Sweep<br>PROTO_L__G_ElementLogic_Req_Sweep |
| `ElementLogic_LevelFail` | nID, tbLog | PROTO_G_ElementLogic_Req_LevelFail<br>PROTO_L__G_ElementLogic_Req_LevelFail |
| `ElementLogic_LotteryDraw` | — | PROTO_G_ElementLogic_Req_Gacha<br>PROTO_L__G_ElementLogic_Req_Gacha |

## FishingServer (6)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `FishingServer_BeginFishing` | nNodeID, nSelectBait | PROTO_G_FishingLogic_BeginFishing<br>PROTO_L__G_FishingLogic_BeginFishing |
| `FishingServer_ConvertFood` | nFoodID, nNum | PROTO_G_FishingLogic_GetCookAward<br>PROTO_L__G_FishingLogic_GetCookAward |
| `FishingServer_EndFishing` | nState | PROTO_G_FishingLogic_EndFishing<br>PROTO_L__G_FishingLogic_EndFishing |
| `FishingServer_GetCollectAward` | nId, tbIdList | PROTO_G_FishingLogic_GetCollectAward<br>PROTO_L__G_FishingLogic_GetCollectAward |
| `FishingServer_GetLevelAward` | nLevel | PROTO_G_FishingLogic_GetLevelAward<br>PROTO_L__G_FishingLogic_GetLevelAward |
| `FishingServer_ReadFishRecord` | nFishID | PROTO_G_FishingLogic_ReadFishRecord<br>PROTO_L__G_FishingLogic_ReadFishRecord |

## Item (6)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Item_CleanRed` | — | PROTO_L_UMG_Bag_umg_bag_UpdateTabRedDot |
| `Item_Expiration` | tbItems | PROTO_G_Item_Expiration/_ENV<br>PROTO_L__G_Item_Expiration/_ENV |
| `Item_OpenBox` | Count, Id | PROTO_L_UMG_Bag_umg_bag_OnInit/_ENV |
| `Item_Recycle` | tbItems | PROTO_L_UMG_Bag_umg_bag_SetSellPanel/self/_ENV |
| `Item_SetLock` | ItemId, Lock | PROTO_L_UMG_Bag_umg_bag_UpdateInfo/_ENV |
| `Item_SetReadFlag` | ItemId, bReaded | PROTO_L_package_loaded_UMG_Main_umg_main_CheckBagRed<br>PROTO_L_UMG_Main_umg_main_CheckBagRed |

## PlayerSetting (6)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `PlayerSetting_ChangeAccountShowCard` | nIndex, nItemID | PROTO_G_PlayerSetting_Req_ChangeAccountShowCard<br>PROTO_L__G_PlayerSetting_Req_ChangeAccountShowCard |
| `PlayerSetting_ChangeAccountShowSkin` | nIndex, nItemID | PROTO_G_PlayerSetting_Req_ChangeAccountShowSkin<br>PROTO_L__G_PlayerSetting_Req_ChangeAccountShowSkin |
| `PlayerSetting_ChangeShowCard` | nID | PROTO_G_PlayerSetting_Req_ChangeRole<br>PROTO_L__G_PlayerSetting_Req_ChangeRole |
| `PlayerSetting_GetPlayTime` | — | PROTO_G_HealthTip_Req_PlayTime<br>PROTO_L__G_HealthTip_Req_PlayTime |
| `PlayerSetting_ReportPlayTime` | nTime | PROTO_G_HealthTip_SavePlayTime<br>PROTO_L__G_HealthTip_SavePlayTime |
| `PlayerSetting_SetShowBadge` | tbBadge | PROTO_G_PlayerSetting_Req_ChangeAccountShowBadge<br>PROTO_L__G_PlayerSetting_Req_ChangeAccountShowBadge |

## BattlePassLogic (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `BattlePassLogic_BuyLevel` | nLevel | PROTO_G_BattlePass_DoBuyLevel<br>PROTO_L__G_BattlePass_DoBuyLevel |
| `BattlePassLogic_ClientRefresh` | — | PROTO_G_BattlePass_DoRefresh<br>PROTO_L__G_BattlePass_DoRefresh |
| `BattlePassLogic_FirstOpen` | — | PROTO_G_BattlePass_DoFirstOpen<br>PROTO_L__G_BattlePass_DoFirstOpen |
| `BattlePassLogic_GetPassAward` | — | PROTO_G_BattlePass_DoGetAward<br>PROTO_L__G_BattlePass_DoGetAward |
| `BattlePassLogic_QuickGetReward` | tbIdList | PROTO_G_BattlePass_DoGetMission<br>PROTO_L__G_BattlePass_DoGetMission |

## BossPvpLogic (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `BossPvpLogic_EnterLevel` | nDifficulty, nID, nLevelID, nTeamID, tbEntrie, tbLog | PROTO_G_BossPvpLogic_Req_EnterLevel<br>PROTO_L__G_BossPvpLogic_Req_EnterLevel |
| `BossPvpLogic_GetOpenID` | — | PROTO_G_BossPvpLogic_GetOpenID/_ENV<br>PROTO_L__G_BossPvpLogic_GetOpenID/_ENV |
| `BossPvpLogic_GetReward` | tbTaskID | PROTO_G_BossPvpLogic_GetReward<br>PROTO_L__G_BossPvpLogic_GetReward |
| `BossPvpLogic_LevelMopup` | nDiff, nID | PROTO_G_BossPvpLogic_Req_LevelMopup<br>PROTO_L__G_BossPvpLogic_Req_LevelMopup |
| `BossPvpLogic_Record` | ResidueTime, bRecord, nDiff, nID, nSeed, nTime | PROTO_G_BossPvpLogic_Record<br>PROTO_L__G_BossPvpLogic_Record |

## DefendLogic (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DefendLogic_CheckOpenAct` | — | PROTO_G_DefendLogic_CheckOpenAct/_ENV<br>PROTO_G_DefendLogic_GetOpenConf |
| `DefendLogic_EnterLevel` | nDiff, nID, nTeamID, tbLog | PROTO_G_DefendLogic_Req_EnterLevel<br>PROTO_L__G_DefendLogic_Req_EnterLevel |
| `DefendLogic_GetLevelAward` | tbIdList | PROTO_G_DefendLogic_Req_GetLevelAward<br>PROTO_L__G_DefendLogic_Req_GetLevelAward |
| `DefendLogic_GetReward` | bAll, nDiff, nID, nIdx, nTargetId | PROTO_G_DefendLogic_GetReward<br>PROTO_G_DefendLogic_GetRewardAll |
| `DefendLogic_SelectDiff` | nDiffId | PROTO_G_DefendLogic_Req_SelectDiff<br>PROTO_L__G_DefendLogic_Req_SelectDiff |

## Gacha (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Gacha_GetOpenTime` | — | PROTO_G_Gacha_PullOpenTime<br>PROTO_L__G_Gacha_PullOpenTime |
| `Gacha_Launch` | bPickUp, nId, nTime | PROTO_G_Gacha_Req_Launch<br>PROTO_L__G_Gacha_Req_Launch |
| `Gacha_PickUp` | nId, nPickUp | PROTO_G_Gacha_Req_PickUp<br>PROTO_L__G_Gacha_Req_PickUp |
| `Gacha_TogglePickUp` | nId | PROTO_G_Gacha_Req_TogglePickUp<br>PROTO_L__G_Gacha_Req_TogglePickUp |
| `Gacha_UpSelect` | gdpl, nId | PROTO_G_Gacha_Req_UpSelect<br>PROTO_L__G_Gacha_Req_UpSelect |

## GirlSkin (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GirlSkin_Change` | CardId, Id | PROTO_L_Item_Fashion_ChangeSkinReq<br>PROTO_L_package_loaded_Item_Fashion_ChangeSkinReq |
| `GirlSkin_ChangeSkinType` | nSkinId, nType | PROTO_L_Item_Fashion_Req_ChangeSkinType<br>PROTO_L_package_loaded_Item_Fashion_Req_ChangeSkinType |
| `GirlSkin_ChangeSkinType2` | nSkinId, nType | PROTO_L_Item_Fashion_Req_ChangeSkinType2<br>PROTO_L_package_loaded_Item_Fashion_Req_ChangeSkinType2 |
| `GirlSkin_RandomChange` | tbCardId, tbId | PROTO_L_Item_Fashion_RandomChangeSkinReq<br>PROTO_L_package_loaded_Item_Fashion_RandomChangeSkinReq |
| `GirlSkin_ResetRandomChange` | — | PROTO_L_Item_Fashion_ResetRandomChangeSkinReq<br>PROTO_L_package_loaded_Item_Fashion_ResetRandomChangeSkinReq |

## LimitedTime (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `LimitedTime_CheckLimitedItemRecycle` | — | PROTO_G_LimitedRole_CheckLimitedItemRecycle<br>PROTO_L__G_LimitedRole_CheckLimitedItemRecycle |
| `LimitedTime_CheckLimitedItemUpdate` | — | PROTO_G_LimitedRole_CheckLimitedItemUpdate<br>PROTO_L__G_LimitedRole_CheckLimitedItemUpdate |
| `LimitedTime_CheckLimitedRoleGet` | — | PROTO_G_LimitedRole_CheckLimitedRoleGet<br>PROTO_L__G_LimitedRole_CheckLimitedRoleGet |
| `LimitedTime_CheckLimitedSupportGet` | — | PROTO_G_LimitedRole_CheckLimitedSupportGet<br>PROTO_L__G_LimitedRole_CheckLimitedSupportGet |
| `LimitedTime_CheckLimitedWeaponGet` | — | PROTO_G_LimitedRole_CheckLimitedWeaponGet<br>PROTO_L__G_LimitedRole_CheckLimitedWeaponGet |

## Online (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Online_ClientLog` | AREnter, ARQuit, GiftboxSuggest, LevelPerformance, ShieldEmoji | PROTO_G_Chat_SetLockEmoji<br>PROTO_G_GiftboxSuggest_RecordLog |
| `Online_CostVigour` | bOpen | PROTO_G_Online_VigourSwitch<br>PROTO_L__G_Online_VigourSwitch |
| `Online_FirstPop` | nId | PROTO_G_Online_CheckNoPopInfo<br>PROTO_G_Online_CheckPopInfo |
| `Online_RecordPartySpectateLog` | tbLog | PROTO_G_Online_SendPartySpectateLog<br>PROTO_L__G_Online_SendPartySpectateLog |
| `Online_WeeklyAward` | — | PROTO_G_Online_GetAllWeeklyAward<br>PROTO_L__G_Online_GetAllWeeklyAward |

## Repression (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Repression_ChangeFormation` | nID, tbFormation | PROTO_G_Repression_Chapter_GetLineup<br>PROTO_G_Repression_Chapter_SetLineup |
| `Repression_Chapter_EnterLevel` | nID, nMultiple, nTeamID, tbLog | PROTO_G_Repression_Chapter_Req_EnterLevel<br>PROTO_L__G_Repression_Chapter_Req_EnterLevel |
| `Repression_Chapter_FirstEnter` | — | PROTO_G_Repression_Chapter_IsFirstEnter<br>PROTO_L__G_Repression_Chapter_IsFirstEnter |
| `Repression_Chapter_LevelFail` | nID, tbLog | PROTO_G_Repression_Chapter_Req_LevelFail<br>PROTO_L__G_Repression_Chapter_Req_LevelFail |
| `Repression_Chapter_STAR_AWARD` | — | PROTO_G_Repression_Chapter_Req_GetStarAward<br>PROTO_L__G_Repression_Chapter_Req_GetStarAward |

## RichmanLogic (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RichmanLogic_CheckOpenAct` | — | PROTO_G_RichmanLogic_CheckOpenAct<br>PROTO_L__G_RichmanLogic_CheckOpenAct |
| `RichmanLogic_EnterMap` | bContinue, nId, nMapId, tbLog | PROTO_G_RichmanLogic_EnterMap<br>PROTO_L__G_RichmanLogic_EnterMap |
| `RichmanLogic_MapSettlement` | activityId, activityType, mapId, nRank, nSeed, tbLevelNum, tbLog | PROTO_G_RichmanLogic_MapSettlement<br>PROTO_L__G_RichmanLogic_MapSettlement |
| `RichmanLogic_ReceiveVoteveReward` | nId | PROTO_G_RichmanLogic_ReceiveVoteveReward<br>PROTO_L__G_RichmanLogic_ReceiveVoteveReward |
| `RichmanLogic_VoteGirl` | nId, nNum, nTotalNum | PROTO_G_RichmanLogic_VoteGirl<br>PROTO_L__G_RichmanLogic_VoteGirl |

## SeasonBoss (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `SeasonBoss_CheckOpen` | ForceEnter | PROTO_G_SeasonBossLogic_CheckOpen<br>PROTO_L__G_SeasonBossLogic_CheckOpen |
| `SeasonBoss_EnterLevel` | nDifficulty, nID, nTeamID, nZoneID, tbEntrie, tbLog | PROTO_G_SeasonBossLogic_Req_EnterLevel<br>PROTO_L__G_SeasonBossLogic_Req_EnterLevel |
| `SeasonBoss_GetReward` | tbTaskID | PROTO_G_SeasonBossLogic_GetReward<br>PROTO_L__G_SeasonBossLogic_GetReward |
| `SeasonBoss_LevelFail` | ResidueTime, nDamage, nDiff, nID, nReason, nSeed, nTime, nZoneID, tbLog | PROTO_G_SeasonBossLogic_Req_LevelFail<br>PROTO_L__G_SeasonBossLogic_Req_LevelFail |
| `SeasonBoss_Record` | ResidueTime, bRecord, nDamage, nDiff, nID, nSeed, nTime, nZoneID | PROTO_G_SeasonBossLogic_Record<br>PROTO_L__G_SeasonBossLogic_Record |

## VirCaptureLevel (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `VirCaptureLevel_ChangeFlag` | bClean, nLevelID, nRegionId, nSeed | PROTO_G_VirCapture_ChangeFlag<br>PROTO_L__G_VirCapture_ChangeFlag |
| `VirCaptureLevel_EnterLevel` | nLevelID, nTeamID, tbLog | PROTO_G_VirCapture_Req_EnterLevel<br>PROTO_L__G_VirCapture_Req_EnterLevel |
| `VirCaptureLevel_SaveCapture` | nLevelID, nRegionId, nSeed | PROTO_G_VirCapture_DoSaveCaptureMonster<br>PROTO_L__G_VirCapture_DoSaveCaptureMonster |
| `VirCaptureLevel_SaveFightData` | nLevelID, nRegionId, nSeed | PROTO_G_VirCapture_DoSaveMonsterFightData<br>PROTO_L__G_VirCapture_DoSaveMonsterFightData |
| `VirCaptureLevel_SavePos` | nLevelID, nPosX, nPosY, nPosZ, nSeed, nToward, tbKill, tbMonster | PROTO_G_VirCapture_SavePos<br>PROTO_L__G_VirCapture_SavePos |

## VirCaptureTask (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `VirCaptureTask_DoCheckCostTask` | nMapId | PROTO_G_VirCaptureTask_ReqGetCostTask<br>PROTO_L__G_VirCaptureTask_ReqGetCostTask |
| `VirCaptureTask_DoGiveUp` | nMapId, nMissionId | PROTO_G_VirCaptureTask_ReqGiveUpMission<br>PROTO_L__G_VirCaptureTask_ReqGiveUpMission |
| `VirCaptureTask_DoRandom` | nMapId | PROTO_G_VirCaptureTask_ReqGetRandomMission<br>PROTO_L__G_VirCaptureTask_ReqGetRandomMission |
| `VirCaptureTask_DoSomething` | — | PROTO_G_VirCaptureTask_ReqDoSomething<br>PROTO_L__G_VirCaptureTask_ReqDoSomething |
| `VirCaptureTask_GetReward` | nId | PROTO_G_VirCaptureTask_ReqGetReward<br>PROTO_L__G_VirCaptureTask_ReqGetReward |

## DLC (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DLC_Chapter_EnterLevel` | bFree, nChapterID, nID, nMultiple, nTeamID, tbLog | PROTO_G_DLC_Chapter_Req_EnterLevel<br>PROTO_L__G_DLC_Chapter_Req_EnterLevel |
| `DLC_Chapter_LevelFail` | nID, tbLog | PROTO_G_DLC_Chapter_Req_LevelFail<br>PROTO_L__G_DLC_Chapter_Req_LevelFail |
| `DLC_Chapter_Mopup` | nChapterID, nID, nMultiple, nTeamID, tbLog | PROTO_G_DLC_Chapter_Req_Moppingup<br>PROTO_L__G_DLC_Chapter_Req_Moppingup |
| `DLC_Chapter_STAR_AWARD` | — | PROTO_G_DLC_Chapter_Req_GetStarAward<br>PROTO_L__G_DLC_Chapter_Req_GetStarAward |

## DonoDuelTask (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DonoDuelTask_Accept` | nId | PROTO_G_DonoDuelTask_ReqAccept<br>PROTO_L__G_DonoDuelTask_ReqAccept |
| `DonoDuelTask_DoSomething` | — | PROTO_G_DonoDuelTask_ReqDoSomething<br>PROTO_L__G_DonoDuelTask_ReqDoSomething |
| `DonoDuelTask_GetReward` | nId | PROTO_G_DonoDuelTask_DoReqGetReward<br>PROTO_L__G_DonoDuelTask_DoReqGetReward |
| `DonoDuelTask_QuickGetReward` | tbIdList | PROTO_G_DonoDuelTask_QuickGetReward<br>PROTO_L__G_DonoDuelTask_QuickGetReward |

## GirlRush (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GirlRush_EnterLevel` | — | PROTO_G_GirlRush_Req_EnterLevel<br>PROTO_L__G_GirlRush_Req_EnterLevel |
| `GirlRush_GetAward` | — | PROTO_G_GirlRush_Req_GetAward<br>PROTO_L__G_GirlRush_Req_GetAward |
| `GirlRush_LevelFail` | — | PROTO_G_GirlRush_Req_LevelFail<br>PROTO_L__G_GirlRush_Req_LevelFail |
| `GirlRush_SaveData` | — | PROTO_G_GirlRush_Req_SaveData<br>PROTO_L__G_GirlRush_Req_SaveData |

## GirlSpine (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GirlSpine_ChildNodeReset` | pId | PROTO_L_package_loaded_Item_Spine_Req_ChildNodeReset<br>PROTO_L__G_Spine_Req_ChildNodeReset |
| `GirlSpine_ChildUnLock` | pId, tbInfo, tbMasterList, tbMat | PROTO_L_package_loaded_Item_Spine_Req_ChildNode<br>PROTO_L__G_Spine_Req_ChildNode |
| `GirlSpine_MasterUnlock` | NodeId, pId | PROTO_L_package_loaded_Item_Spine_Req_MasterNode<br>PROTO_L__G_Spine_Req_MasterNode |
| `GirlSpine_UnlockNodeOneKey` | nIdx, pId, tbMasterList, tbOneKey | PROTO_L_package_loaded_Item_Spine_Req_OneKey<br>PROTO_L__G_Spine_Req_OneKey |

## OnlineActivity (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineActivity_QuestAward` | nId, tbIdList | PROTO_G_OnlineActivity_GetAllQuestAward<br>PROTO_L__G_OnlineActivity_GetAllQuestAward |
| `OnlineActivity_Request` | — | PROTO_G_Online_CheckOpenList<br>PROTO_L__G_Online_CheckOpenList |
| `OnlineActivity_SetOnlineTrial` | nId, nTrialId | PROTO_G_Online_SyncOnlineTrial<br>PROTO_L__G_Online_SyncOnlineTrial |
| `OnlineActivity_SetProfession` | nId, nProf | PROTO_G_Online_SyncOnlineSetProf<br>PROTO_L__G_Online_SyncOnlineSetProf |

## OnlineAssaultOps (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineAssaultOps_ChangeFormation` | nFormationId, nOnlineId | PROTO_G_OnlineAssaultOps_ReqChangeFormation<br>PROTO_L__G_OnlineAssaultOps_ReqChangeFormation |
| `OnlineAssaultOps_Equip` | bUnEquip, nChipId, nFormationId, nOnlineId, nPos | PROTO_G_OnlineAssaultOps_ReqEquipChip<br>PROTO_L__G_OnlineAssaultOps_ReqEquipChip |
| `OnlineAssaultOps_QuestAward` | nOnlineId, tbIdList | PROTO_G_OnlineAssaultOps_GetAllQuestAward<br>PROTO_L__G_OnlineAssaultOps_GetAllQuestAward |
| `OnlineAssaultOps_SystemEquip` | nFormationId, nOnlineId, nSysModIndx, tbEquipList | PROTO_G_OnlineAssaultOps_ReqSystemEquipChip<br>PROTO_L__G_OnlineAssaultOps_ReqSystemEquipChip |

## OnlineBoss (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineBoss_CheckOpenAct` | — | PROTO_G_OnlineBoss_CheckOpenAct/_ENV<br>PROTO_L__G_OnlineBoss_CheckOpenAct/_ENV |
| `OnlineBoss_DamageAward` | tbIdList | PROTO_G_OnlineBoss_Req_DamageAward<br>PROTO_L__G_OnlineBoss_Req_DamageAward |
| `OnlineBoss_EnterLevel` | nID, nTeamID, tbLog | PROTO_G_OnlineBoss_Req_EnterLevel<br>PROTO_L__G_OnlineBoss_Req_EnterLevel |
| `OnlineBoss_LevelFail` | nID, tbLog | PROTO_G_OnlineBoss_Req_LevelFail<br>PROTO_L__G_OnlineBoss_Req_LevelFail |

## OnlineSea (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineSea_BuyMod` | nModId, nOnlineId | PROTO_G_OnlineSea_ReqBuyMod<br>PROTO_L__G_OnlineSea_ReqBuyMod |
| `OnlineSea_Equip` | bFormation, nFormationId, nOnlineId, nSysModIndx, tbEquipList | PROTO_G_OnlineSea_ReqEquip<br>PROTO_L__G_OnlineSea_ReqEquip |
| `OnlineSea_SetAutoBuy` | bAutoBuy, nFormationId, nOnlineId | PROTO_G_OnlineSea_ReqSetAutoBuy<br>PROTO_L__G_OnlineSea_ReqSetAutoBuy |
| `OnlineSea_UseFormation` | bUse, nFormationId, nOnlineId, nSysModIndx | PROTO_G_OnlineSea_ReqUseFormation<br>PROTO_L__G_OnlineSea_ReqUseFormation |

## ShopLogic (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ShopLogic_BuyGoods` | nBuyMode, nCount, nGoodsId | PROTO_G_ShopLogic_BuyGoods<br>PROTO_L__G_ShopLogic_BuyGoods |
| `ShopLogic_GetGoodsList` | nShopId | PROTO_G_ShopLogic_GetGoodsList<br>PROTO_L__G_ShopLogic_GetGoodsList |
| `ShopLogic_GetOpenTime` | — | PROTO_G_ShopLogic_GetOpenTime<br>PROTO_L__G_ShopLogic_GetOpenTime |
| `ShopLogic_UpdateShop` | nShopId | PROTO_G_ShopLogic_UpdateShop<br>PROTO_G_ShopLogic_UpdateShop/_ENV |

## VirCaptureBuild (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `VirCaptureBuild_AssignWorker` | nId, nStaffId, nStaffState | PROTO_G_VirCaptureBuild_ReqAssignWorker<br>PROTO_L__G_VirCaptureBuild_ReqAssignWorker |
| `VirCaptureBuild_OperateBuilding` | nMapId | PROTO_G_VirCaptureBuild_ReqOperateBuilding<br>PROTO_L__G_VirCaptureBuild_ReqOperateBuilding |
| `VirCaptureBuild_UpgradeAttribute` | nAttrIndx, nId | PROTO_G_VirCaptureBuild_ReqUpgradeAttribute<br>PROTO_L__G_VirCaptureBuild_ReqUpgradeAttribute |
| `VirCaptureBuild_UpgradeBuild` | nId | PROTO_G_VirCaptureBuild_ReqUpgradeBuild<br>PROTO_L__G_VirCaptureBuild_ReqUpgradeBuild |

## Achievement (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Achievement_GetReward` | nId | PROTO_G_Achievement_GetExtraReward<br>PROTO_G_Achievement_GetReward |
| `Achievement_OnAddSomeOne` | nType, tbParam | PROTO_G_AchievementExtend_CheckBindingSeasun/_ENV<br>PROTO_G_AchievementExtend_CheckLevelPass |
| `Achievement_QuickGetReward` | nType, tbIdList, tbPointList | PROTO_G_Achievement_QuickGetReward<br>PROTO_L__G_Achievement_QuickGetReward |

## chess.apply (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `chess.apply_get_reward` | ShowTip, activityId, activityType, rewardIndex | PROTO_G_ChessData_SetReward<br>PROTO_L__G_ChessData_SetReward |
| `chess.apply_map_complete` | QuitGame, activityId, activityType, mapId | PROTO_G_ChessData_SetMapComplete<br>PROTO_L__G_ChessData_SetMapComplete |
| `chess.apply_on_map_save` | activityId, activityType, moduleName, tbMapId | PROTO_G_ChessData_C2S_OnMapSave<br>PROTO_L__G_ChessData_C2S_OnMapSave |

## ChessLogic (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ChessLogic_ChangeFormation` | tbFormation | PROTO_G_ChessLogic_SetLineup<br>PROTO_L__G_ChessLogic_SetLineup |
| `ChessLogic_CheckOpenAct` | — | PROTO_G_ChessLogic_CheckOpenAct/_ENV<br>PROTO_L__G_ChessLogic_CheckOpenAct/_ENV |
| `ChessLogic_EnterMap` | nId, nMapId | PROTO_G_ChessLogic_EnterMap<br>PROTO_L__G_ChessLogic_EnterMap |

## DecryptLogic (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DecryptLogic_CleanSubIDCompleted` | nID | PROTO_G_DecryptLogic_CleanSubIDCompleted<br>PROTO_L__G_DecryptLogic_CleanSubIDCompleted |
| `DecryptLogic_SetCompleted` | Value, nID | PROTO_G_DecryptLogic_SetCompleted<br>PROTO_L__G_DecryptLogic_SetCompleted |
| `DecryptLogic_SetSubIDCompleted` | nID, nPos, v | PROTO_G_DecryptLogic_SetSubIDCompleted<br>PROTO_L__G_DecryptLogic_SetSubIDCompleted |

## DonoDuelRogue (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DonoDuelRogue_EnterLevel` | nID, nTeamID, tbLog | PROTO_G_DonoDuelRogue_Req_EnterLevel<br>PROTO_L__G_DonoDuelRogue_Req_EnterLevel |
| `DonoDuelRogue_MiniGameSettlement` | nRoomId, nSeed | PROTO_G_DonoDuelRogue_Req_MiniGameAward<br>PROTO_L__G_DonoDuelRogue_Req_MiniGameAward |
| `DonoDuelRogue_SelectBondTag` | nBondTag | PROTO_G_DonoDuelRogue_Req_SelectBondTag<br>PROTO_L__G_DonoDuelRogue_Req_SelectBondTag |

## GuideLogic (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GuideLogic_GMSetBeginner` | — | PROTO_G_GuideLogic_SkipAllGuide<br>PROTO_L__G_GuideLogic_SkipAllGuide |
| `GuideLogic_SetBeginner` | nType | PROTO_G_GuideLogic_SetBeginner<br>PROTO_L__G_GuideLogic_SetBeginner |
| `GuideLogic_WriteGuideLog` | logstr | PROTO_G_GuideLogic_ChackGuideLog<br>PROTO_L__G_GuideLogic_ChackGuideLog |

## IBLogic (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `IBLogic_BuyGoods` | nCount, nGoodsId, nIndex, nType, tbSelectItem1, tbSelectItem2 | PROTO_G_IBLogic_DoBuyProduct<br>PROTO_L__G_IBLogic_DoBuyProduct |
| `IBLogic_GoodsRedDot` | tbList | PROTO_G_IBLogic_SetSkinRedDot<br>PROTO_L__G_IBLogic_SetSkinRedDot |
| `IBLogic_ShoppingCart` | — | PROTO_G_IBLogic_DoBuyProductList<br>PROTO_L__G_IBLogic_DoBuyProductList |

## OnlineAssaultOpsBattlePass (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineAssaultOpsBattlePass_ChangeBP` | nId | PROTO_G_OnlineAssaultOpsBattlePass_ChangeActivityBP<br>PROTO_L__G_OnlineAssaultOpsBattlePass_ChangeActivityBP |
| `OnlineAssaultOpsBattlePass_ClientRefresh` | — | PROTO_G_OnlineAssaultOpsBattlePass_DoRefresh<br>PROTO_L__G_OnlineAssaultOpsBattlePass_DoRefresh |
| `OnlineAssaultOpsBattlePass_LevelAward` | nId, tbIdList | PROTO_G_OnlineAssaultOpsBattlePass_GetAllLevelAward<br>PROTO_L__G_OnlineAssaultOpsBattlePass_GetAllLevelAward |

## OnlineBattlePass (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineBattlePass_ClientRefresh` | — | PROTO_G_OnlineBattlePass_DoRefresh<br>PROTO_L__G_OnlineBattlePass_DoRefresh |
| `OnlineBattlePass_LevelAward` | nId, tbIdList | PROTO_G_OnlineBattlePass_GetAllLevelAward<br>PROTO_L__G_OnlineBattlePass_GetAllLevelAward |
| `OnlineBattlePass_QuestAward` | nId, tbIdList | PROTO_G_OnlineBattlePass_GetAllQuestAward<br>PROTO_L__G_OnlineBattlePass_GetAllQuestAward |

## OnlineCombineBattlePass (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineCombineBattlePass_ClientRefresh` | — | PROTO_G_OnlineCombineBattlePass_DoRefresh<br>PROTO_L__G_OnlineCombineBattlePass_DoRefresh |
| `OnlineCombineBattlePass_LevelAward` | nId, tbIdList | PROTO_G_OnlineCombineBattlePass_GetAllLevelAward<br>PROTO_L__G_OnlineCombineBattlePass_GetAllLevelAward |
| `OnlineCombineBattlePass_QuestAward` | nId, tbIdList | PROTO_G_OnlineCombineBattlePass_GetAllQuestAward<br>PROTO_L__G_OnlineCombineBattlePass_GetAllQuestAward |

## OnlineSpeedScore (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineSpeedScore_ChangeFormation` | nFormationId, nOnlineId | PROTO_G_OnlineSpeedScore_ReqChangeFormation<br>PROTO_L__G_OnlineSpeedScore_ReqChangeFormation |
| `OnlineSpeedScore_Equip` | bUnEquip, nBuffId, nFormationId, nOnlineId, nPos | PROTO_G_OnlineSpeedScore_ReqEquipBuff<br>PROTO_L__G_OnlineSpeedScore_ReqEquipBuff |
| `OnlineSpeedScore_QuickEquip` | bAllUnEquip, nFormationId, nOnlineId, tbEquipList | PROTO_G_OnlineSpeedScore_ReqQuickEquipBuff<br>PROTO_L__G_OnlineSpeedScore_ReqQuickEquipBuff |

## RandomShowGirl (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RandomShowGirl_Set` | tbForm, tbItemId | PROTO_G_RandomShowGirl_SetRandomGirl<br>PROTO_L__G_RandomShowGirl_SetRandomGirl |
| `RandomShowGirl_SetGirlSkinInLevel` | — | PROTO_G_RandomShowGirl_SetRandomGirlSkinInLevel<br>PROTO_L__G_RandomShowGirl_SetRandomGirlSkinInLevel |
| `RandomShowGirl_SetMainBg` | b3D, tbId | PROTO_G_RandomShowGirl_SetRandomMainBg/_ENV<br>PROTO_L__G_RandomShowGirl_SetRandomMainBg/_ENV |

## Rogue3DScoreModel (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Rogue3DScoreModel_BuyBuff` | nBuffId | PROTO_L_package_loaded_Dlc_Rogue3D_Rogue3DScoreModel_Req_BuyBuff<br>PROTO_L__G_Rogue3DScoreModel_Req_BuyBuff |
| `Rogue3DScoreModel_LevelScoreAward` | nLevelId, tbIdList | PROTO_L_package_loaded_Dlc_Rogue3D_Rogue3DScoreModel_Req_LevelScoreAward<br>PROTO_L__G_Rogue3DScoreModel_Req_LevelScoreAward |
| `Rogue3DScoreModel_SaveBuffPlan` | nIndex, tbCommonBuff, tbPlayerBuff | PROTO_L_package_loaded_Dlc_Rogue3D_Rogue3DScoreModel_Req_SaveBuffPlan<br>PROTO_L__G_Rogue3DScoreModel_Req_SaveBuffPlan |

## Rogue3DUav (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Rogue3DUav_ChangeCore` | — | PROTO_G_Rogue3DUav_ReqChangeCore<br>PROTO_L__G_Rogue3DUav_ReqChangeCore |
| `Rogue3DUav_Equip` | — | PROTO_G_Rogue3DUav_ReqEquip<br>PROTO_L__G_Rogue3DUav_ReqEquip |
| `Rogue3DUav_Merge` | — | PROTO_G_Rogue3DUav_ReqMerge<br>PROTO_L__G_Rogue3DUav_ReqMerge |

## Role (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Role_EnterLevel` | nID, nMultiple, nTeamID, tbLog | PROTO_G_Role_Req_EnterLevel<br>PROTO_L__G_Role_Req_EnterLevel |
| `Role_LevelFail` | nID, tbLog | PROTO_G_Role_Req_LevelFail<br>PROTO_L__G_Role_Req_LevelFail |
| `Role_LevelMoppingUp` | nID, nMultiple, nRoleID | PROTO_G_Role_Req_LevelMopup<br>PROTO_L__G_Role_Req_LevelMopup |

## Seven (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Seven_day_getAchievementAward` | achievementId, actId, index | PROTO_L_Activity_SevenDay_GetAcheveimentAward<br>PROTO_L_package_loaded_Activity_SevenDay_GetAcheveimentAward |
| `Seven_day_getAllRewardCanGet` | — | PROTO_L_Activity_SevenDay_GetAllRewardCanGet<br>PROTO_L_package_loaded_Activity_SevenDay_GetAllRewardCanGet |
| `Seven_day_getIndexAward` | actId, index | PROTO_L_Activity_SevenDay_GetIndexAward<br>PROTO_L_package_loaded_Activity_SevenDay_GetIndexAward |

## VirCaptureTower (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `VirCaptureTower_EnterLevel` | nID, nTeamID, tbLog | PROTO_G_VirCaptureTower_Req_EnterLevel<br>PROTO_L__G_VirCaptureTower_Req_EnterLevel |
| `VirCaptureTower_GetStarAward` | nChapterId, nDifficult, nIndex | PROTO_G_VirCaptureTower_Req_GetStarAward<br>PROTO_L__G_VirCaptureTower_Req_GetStarAward |
| `VirCaptureTower_LevelFail` | nID, tbLog | PROTO_G_VirCaptureTower_Req_LevelFail<br>PROTO_L__G_VirCaptureTower_Req_LevelFail |

## AchievementDLC (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `AchievementDLC_GetReward` | nId | PROTO_G_AchievementDLC_GetReward<br>PROTO_L__G_AchievementDLC_GetReward |
| `AchievementDLC_QuickGetReward` | tbIdList | PROTO_G_AchievementDLC_QuickGetReward<br>PROTO_L__G_AchievementDLC_QuickGetReward |

## AchievementExtend (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `AchievementExtend_RefreshPopFlag` | tbList | PROTO_G_AchievementExtend_SetRefreshPopFlag<br>PROTO_L__G_AchievementExtend_SetRefreshPopFlag |
| `AchievementExtend_WeeklyRedDot` | tbList | PROTO_G_AchievementExtend_SetWeeklyRedDot<br>PROTO_L__G_AchievementExtend_SetWeeklyRedDot |

## AchievementVirCapture (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `AchievementVirCapture_GetReward` | nId | PROTO_G_AchievementVirCapture_GetReward<br>PROTO_L__G_AchievementVirCapture_GetReward |
| `AchievementVirCapture_QuickGetReward` | tbIdList | PROTO_G_AchievementVirCapture_QuickGetReward<br>PROTO_L__G_AchievementVirCapture_QuickGetReward |

## Chat (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Chat_BlockSettings` | — | PROTO_G_Chat_BlockSettings<br>PROTO_L__G_Chat_BlockSettings |
| `Chat_Report` | Channel, Content, Name, Pid, Reason, Type | PROTO_L_UMG_Common_Widgets_uw_common_chat_item2_Construct/self/_ENV |

## Chess (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Chess_EnterLevel` | activityId, activityType, fightId, moduleName, nTeamID, tbLog | PROTO_G_ChessClient_Req_EnterLevel<br>PROTO_L__G_ChessClient_Req_EnterLevel |
| `Chess_LevelFail` | activityId, activityType, fightId, moduleName, tbLog | PROTO_G_ChessClient_Req_LevelFail<br>PROTO_L__G_ChessClient_Req_LevelFail |

## ClimbTower (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ClimbTower_Award` | — | PROTO_G_ClimbTower_GetAward<br>PROTO_L__G_ClimbTower_GetAward |
| `ClimbTower_EnterLevel` | — | PROTO_G_ClimbTower_EnterLevel<br>PROTO_L__G_ClimbTower_EnterLevel |

## DonoDuelArena (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DonoDuelArena_EnterLevel` | nID, nTeamID, tbLog | PROTO_G_DonoDuelArena_Req_EnterLevel<br>PROTO_L__G_DonoDuelArena_Req_EnterLevel |
| `DonoDuelArena_LevelFail` | nID, tbKill, tbLog | PROTO_G_DonoDuelArena_Req_LevelFail<br>PROTO_L__G_DonoDuelArena_Req_LevelFail |

## FunTimed (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `FunTimed_EnterLevel` | nID, nSession, nTeamID, tbLog | PROTO_G_FunTimed_EnterLevel<br>PROTO_L__G_FunTimed_EnterLevel |
| `FunTimed_LevelExit` | nID, tbLog | PROTO_G_FunTimed_ExitLevel<br>PROTO_L__G_FunTimed_ExitLevel |

## GachaTry (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GachaTry_EnterLevel` | nActId, nGirlIdx, nLevelID, tbLog | PROTO_L_package_loaded_Activity_GachaTry_Req_EnterLevel<br>PROTO_L__G_GachaTry_Req_EnterLevel |
| `GachaTry_LevelFail` | nActId, nGirlIdx, nLevelID, tbLog | PROTO_L_package_loaded_Activity_GachaTry_Req_LevelFail<br>PROTO_L__G_GachaTry_Req_LevelFail |

## ItemConsole (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ItemConsole_Decomposition` | gdpl, nNum | PROTO_G_ItemConsole_Req_Decomposition<br>PROTO_L__G_ItemConsole_Req_Decomposition |
| `ItemConsole_Synthesis` | gdpl, nNum | PROTO_G_ItemConsole_Req_Synthesis<br>PROTO_L__G_ItemConsole_Req_Synthesis |

## OnlineForbidzone (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineForbidzone_Equip` | nId | PROTO_G_OnlineForbidzone_ReqEquip<br>PROTO_L__G_OnlineForbidzone_ReqEquip |
| `OnlineForbidzone_LevelUp` | nId, nOldLevel, nSelectLevel | PROTO_G_OnlineForbidzone_ReqLevelUp<br>PROTO_L__G_OnlineForbidzone_ReqLevelUp |

## OnlineTraining (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineTraining_EnterLevel` | nID, nOnlineId, nTeamID, tbLog | PROTO_G_OnlineTraining_Req_EnterLevel<br>PROTO_L__G_OnlineTraining_Req_EnterLevel |
| `OnlineTraining_LevelFail` | nID, tbLog | PROTO_G_OnlineTraining_Req_LevelFail<br>PROTO_L__G_OnlineTraining_Req_LevelFail |

## PlayerCharge (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `PlayerCharge_GetAward` | — | PROTO_G_PlayerCharge_GetChargeAward<br>PROTO_L__G_PlayerCharge_GetChargeAward |
| `PlayerCharge_Switch` | — | PROTO_G_PlayerCharge_SetSwitch<br>PROTO_L__G_PlayerCharge_SetSwitch |

## PSCamera (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `PSCamera_SetEnterLog` | — | PROTO_L_PhotoStudio_Base_PSMgr_SetEnterLog<br>PROTO_L__G_PSMgr_SetEnterLog |
| `PSCamera_SetLog` | Detail, MapId | PROTO_L_PhotoStudio_Base_PSMgr_SetLog<br>PROTO_L__G_PSMgr_SetLog |

## RikiLogic (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RikiLogic_AddExploreRiki` | — | PROTO_G_FragmentStory_Show<br>PROTO_L__G_FragmentStory_Show |
| `RikiLogic_AddSouvenirRiki` | — | PROTO_G_Mail_CheckSouvenir<br>PROTO_L__G_Mail_CheckSouvenir |

## Rouge3D (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Rouge3D_ConvertJourneyKey` | nNodeID, nNum, nTargetCashID, tbFromCashID | PROTO_G_Rogue3DAdventure_Req_ShopSwap<br>PROTO_L__G_Rogue3DAdventure_Req_ShopSwap |
| `Rouge3D_ExchangeJourneyKey` | nNodeID, nNum, nTargetCashID | PROTO_G_Rogue3DAdventure_Req_ExchangeKey<br>PROTO_L__G_Rogue3DAdventure_Req_ExchangeKey |

## TowerEventChapter (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `TowerEventChapter_EnterLevel` | nID, nTeamID, tbLog | PROTO_G_TowerEventChapter_Req_EnterLevel<br>PROTO_L__G_TowerEventChapter_Req_EnterLevel |
| `TowerEventChapter_LevelFail` | nID, tbLog | PROTO_G_TowerEventChapter_Req_LevelFail<br>PROTO_L__G_TowerEventChapter_Req_LevelFail |

## TowerLevel (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `TowerLevel_EnterLevel` | nID, nTeamID, tbLog | PROTO_G_TowerLevel_Req_EnterLevel<br>PROTO_L__G_TowerLevel_Req_EnterLevel |
| `TowerLevel_LevelFail` | bClear, nID, nSeed, nTowerID, tbLog | PROTO_G_TowerLevel_Req_LevelFail<br>PROTO_L__G_TowerLevel_Req_LevelFail |

## VigourSupply (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `VigourSupply_CheckRefresh` | — | PROTO_L_Activity_VigourSupply_CheckRefresh<br>PROTO_L__G_VigourSupply_CheckRefresh |
| `VigourSupply_ReceiveVigour` | nId | PROTO_L_Activity_VigourSupply_ReceiveVigour<br>PROTO_L__G_VigourSupply_ReceiveVigour |

## VirCaptureStaff (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `VirCaptureStaff_Recruit` | nStaffId | PROTO_G_VirCaptureBuild_ReqRecruit<br>PROTO_L__G_VirCaptureBuild_ReqRecruit |
| `VirCaptureStaff_Upgrade` | nMapId, nStaffId | PROTO_G_VirCaptureBuild_ReqUpgrade<br>PROTO_L__G_VirCaptureBuild_ReqUpgrade |

## VirCaptureTrial (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `VirCaptureTrial_EnterLevel` | nID, nTeamID, tbLog | PROTO_G_VirCaptureTrial_Req_EnterLevel<br>PROTO_L__G_VirCaptureTrial_Req_EnterLevel |
| `VirCaptureTrial_LevelFail` | nID, tbLog | PROTO_G_VirCaptureTrial_Req_LevelFail<br>PROTO_L__G_VirCaptureTrial_Req_LevelFail |

## WorldBossLogic (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `WorldBossLogic_CheckOpen` | — | PROTO_G_WorldBossLogic_CheckOpen<br>PROTO_L__G_WorldBossLogic_CheckOpen |
| `WorldBossLogic_GetReward` | tbTaskID | PROTO_G_WorldBossLogic_GetReward<br>PROTO_L__G_WorldBossLogic_GetReward |

## AchievementPoint (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `AchievementPoint_GetReward` | nGroup, nIndex | PROTO_G_AchievementPoint_GetReward<br>PROTO_L__G_AchievementPoint_GetReward |

## ActivityFace (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ActivityFace_Update` | bFlag, nId, nType | PROTO_L_package_loaded_Activity_Activityface_SetPopFlag<br>PROTO_L_package_loaded_Activity_Activityface_SetPopNum |

## Adjust (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Adjust_Record` | nType | PROTO_G_Adjust_DoRecordInfo<br>PROTO_L__G_Adjust_DoRecordInfo |

## CallmeLogic (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `CallmeLogic_RecordLog` | tbLog | PROTO_G_CallmeLogic_SendLog<br>PROTO_L__G_CallmeLogic_SendLog |

## Cash (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Cash_Exchange` | nCost, nExhcangTarget, nExhcangeCash | PROTO_G_CashExchange_Exchange<br>PROTO_L__G_CashExchange_Exchange |

## chess.client (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `chess.client_operation_log` | — | PROTO_G_ChessClient_WriteOperationLog<br>PROTO_L__G_ChessClient_WriteOperationLog |

## DLCLogic (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DLCLogic_CheckOpenAct` | — | PROTO_L_package_loaded_DLC_DLC_Logic_CheckOpenAct<br>PROTO_L__G_DLC_Logic_CheckOpenAct |

## GacheTry (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GacheTry_GetAlreadyPassedAward` | nActId | PROTO_L_package_loaded_Activity_GachaTry_Req_GetAlreadyPassedAward<br>PROTO_L__G_GachaTry_Req_GetAlreadyPassedAward |

## GirlSkinParts (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GirlSkinParts_Update` | nSkinId, tbPartsID | PROTO_L_Item_Fashion_Req_GirlSkinParts_Update<br>PROTO_L_package_loaded_Item_Fashion_Req_GirlSkinParts_Update |

## GirlWeaponSkin (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GirlWeaponSkin_Change` | nCardId, nSkinId | PROTO_G_WeaponSkin_Req_Change<br>PROTO_L__G_WeaponSkin_Req_Change |

## Handbook (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Handbook_GetAward` | nIndex | PROTO_L_package_loaded_Challenge_DarkZone_Handbook_DoAward<br>PROTO_L__G_HandbookLogic_DoAward |

## House (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `House_Request` | — | PROTO_G_HouseMessageHandle_HouseMessageSender<br>PROTO_L__G_HouseMessageHandle_HouseMessageSender |

## HouseThrow (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `HouseThrow_ClearData` | — | PROTO_L_package_loaded_House_HouseMiniGame_HouseThrow_HouseThrowSeverMessage_ClearData<br>PROTO_L__G_HouseThrowSeverMessage_ClearData |

## Launch (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Launch_OnCloseLoadingLog` | nLevelID, nSpendTime, nType | PROTO_G_Launch_OnCloseLoading<br>PROTO_L__G_Launch_OnCloseLoading |

## Lineup (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Lineup_Update` | index, member1, member2, member3, name | PROTO_G_VirCapture_InitFormation<br>PROTO_L_package_loaded_Formation_Formation_Req_UpdateLineup |

## Lineups (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Lineups_Update` | — | PROTO_L_package_loaded_Formation_Formation_Req_UpdateLineups<br>PROTO_L__G_Formation_Req_UpdateLineups |

## Logistics (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Logistics_Evolution` | — | PROTO_L_Item_Logistics_Req_Evolution |

## OnlineTowerRush (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineTowerRush_Equip` | nId, nOnlineId | PROTO_G_OnlineTowerRush_ReqEquip<br>PROTO_L__G_OnlineTowerRush_ReqEquip |

## PlayerReturn (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `PlayerReturn_GetReward` | bQuick, missionId, nId, nType | PROTO_G_PlayerReturn_GetFirstReward<br>PROTO_G_PlayerReturn_GetMissionReward |

## Questionnaire (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Questionnaire_Finish` | nId, nSecret, nTime | PROTO_G_Questionnaire_OnClientFinish<br>PROTO_G_Questionnaire_OnFinishQuestID |

## Record (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Record_RTL` | online, rtl | PROTO_G_DataPost_OnGetRTL<br>PROTO_L__G_DataPost_OnGetRTL |

## Report (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Report_UserInform` | nPid, nReason, sName, sSign | PROTO_G_Report_UserInfo<br>PROTO_L__G_Report_UserInfo |

## ReservationReward (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ReservationReward_Gain` | — | PROTO_L_package_loaded_UMG_Main_umg_main_OnOpen<br>PROTO_L_UMG_Main_umg_main_OnOpen |

## RoleCard (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RoleCard_SetSupporterTeamIndex` | Id, Index | PROTO_L_package_loaded_UMG_Role_RoleCard_SetSupporterTeamIndex<br>PROTO_L__G_RoleCard_SetSupporterTeamIndex |

## SupportCard (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `SupportCard_Refine` | — | PROTO_L_package_loaded_Item_Refine_Req_Refine<br>PROTO_L__G_Refine_Req_Refine |

## SupporterSkill (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `SupporterSkill_Evolut` | Id, MatID | PROTO_L_Item_Logistics_Req_Evolut |

## TargetShoot (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `TargetShoot_C2SMsg` | — | PROTO_G_TargetShootMsgHandle_TargetShootMsgSender<br>PROTO_L__G_TargetShootMsgHandle_TargetShootMsgSender |

## TowerEventLogic (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `TowerEventLogic_GetReward` | nChapterID, nGroup | PROTO_G_TowerEvent_GetReward<br>PROTO_L__G_TowerEvent_GetReward |

## ZoneTime (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ZoneTime_ReqTime` | — | PROTO_G_ZoneTime_ReqTime<br>PROTO_L__G_ZoneTime_ReqTime |

