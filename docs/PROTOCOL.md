# 客户端请求接口清单（CallGS）

> 由 `work/probe/scan_protocol.js` 从运行时 dump 的 Lua 5.4 字节码自动生成。
> 覆盖范围 = 当前 `work/_dump/` 里已 dump 的模块，不是全量。

共 **430** 个字面量接口 + **49** 个符号形式。

## BagRogue (24)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `BagRogue_AwardRefresh` | tbTalent | PROTO_L__G_BagRogue_AwardRefresh |
| `BagRogue_CheckNewMapNode` | — | PROTO_L__G_BagRogue_CheckMapNode |
| `BagRogue_CheckOpenAct` | — | PROTO_L__G_BagRogue_CheckOpenAct/_ENV |
| `BagRogue_DoCraftItem` | nUniqueIdA, nUniqueIdB | PROTO_L__G_BagRogue_DoCraftItem |
| `BagRogue_EnterLevel` | nID, tbLog | PROTO_L__G_BagRogue_EnterLevel |
| `BagRogue_EquipBag` | tbList, tbTalent | PROTO_L__G_BagRogue_DoEquipBag |
| `BagRogue_ExFightLog` | BagRogueLevel | PROTO_L__G_BagRogue_LevelSettlement |
| `BagRogue_FirstEnter` | — | PROTO_L__G_BagRogue_SetFirstEnter |
| `BagRogue_GetQuestAward` | tbIdList | PROTO_L__G_BagRogue_GetQuestAward |
| `BagRogue_LevelMoppingUp` | nID, tbTalent | PROTO_L__G_BagRogue_LevelMoppingUp |
| `BagRogue_LevelSelectAward` | nSelectIdx, tbTalent | PROTO_L__G_BagRogue_SelectLevelAward |
| `BagRogue_NodeFinish` | — | PROTO_L__G_BagRogue_NodeFinish |
| `BagRogue_NodeWalk` | nNodeId | PROTO_L__G_BagRogue_NodeWalk |
| `BagRogue_ReforgeItem` | nUniqueId, tbAffixIdx | PROTO_L__G_BagRogue_DoReforgeItem |
| `BagRogue_RefreshStore` | — | PROTO_L__G_BagRogue_StoreRefresh |
| `BagRogue_RemoveExternStorageItem` | nUniqueId | PROTO_L__G_BagRogue_RemoveExternStorageItem |
| `BagRogue_SaveItemToExternStorage` | nNodeId, nUniqueId | PROTO_L__G_BagRogue_SaveItemToExternStorage |
| `BagRogue_SaveTrialCard` | tbTrial | PROTO_L__G_BagRogue_SaveTrialCard |
| `BagRogue_SelectAdventure` | nSelectIdx | PROTO_L__G_BagRogue_SelectAdventure/_ENV |
| `BagRogue_SelectCraftItem` | nIndex | PROTO_L__G_BagRogue_SelectCraftItem |
| `BagRogue_SelectExternStorageItem` | tbUniqueId | PROTO_L__G_BagRogue_SelectExternStorageItem |
| `BagRogue_SellItem` | nUniqueId | PROTO_L__G_BagRogue_SellItem |
| `BagRogue_StoreBuyItem` | nSelectIdx | PROTO_L__G_BagRogue_StoreBuyItem/_ENV |
| `BagRogue_UpgradeItem` | nUniqueA, nUniqueB | PROTO_L__G_BagRogue_DoUpgradeItem |

## Rogue3D (23)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Rogue3D_CheckOpenAct` | — | PROTO_L__G_Rogue3DLogic_Req_CheckOpenAct<br>_G_Rogue3DLogic__Req_CheckOpenAct |
| `Rogue3D_EnterLevel` | nDiffId, nTeamID, tbBuffList, tbLog, tbTeam | PROTO_L__G_Rogue3DLogic_Req_EnterLevel<br>_G_Rogue3DLogic__Req_EnterLevel |
| `Rogue3D_EnterSeasonLevel` | nDiffId, nTeamID, tbBuffList, tbLog, tbTeam | PROTO_L__G_Rogue3DLogic_Req_EnterSeasonLevel<br>_G_Rogue3DLogic__Req_EnterSeasonLevel |
| `Rogue3D_GetLevelAward` | tbIdList | PROTO_L__G_Rogue3DLogic_Req_GetLevelAward<br>_G_Rogue3DLogic__Req_GetLevelAward |
| `Rogue3D_GetQuestAward` | tbIdList | PROTO_L__G_Rogue3DLogic_Req_GetQuestAward<br>_G_Rogue3DLogic__Req_GetQuestAward |
| `Rogue3D_GetSeasonLotteryAward` | nIndex, nTimes | PROTO_L__G_Rogue3DLogic_Req_Gacha<br>_G_Rogue3DLogic__Req_Gacha |
| `Rogue3D_GetSeasonQuestAward` | tbIdList | PROTO_L__G_Rogue3DLogic_Req_GetSeasonQuestAward<br>_G_Rogue3DLogic__Req_GetSeasonQuestAward |
| `Rogue3D_LevelReset` | nDiffId, tbMember | PROTO_L__G_Rogue3DLogic_Req_LevelReset<br>_G_Rogue3DLogic__Req_LevelReset |
| `Rogue3D_MonsterRikiAward` | — | PROTO_L__G_Rogue3DLogic_ReqMonsterRikiAward<br>_G_Rogue3DLogic__ReqMonsterRikiAward |
| `Rogue3D_RecoverJourneySan` | — | PROTO_L__G_Rogue3DLogic_Req_RecoverJourneySan<br>_G_Rogue3DLogic__Req_RecoverJourneySan |
| `Rogue3D_RestrictTech` | nRestrict, nTechId | PROTO_L__G_Rogue3DLogic_Req_RestrictTech<br>_G_Rogue3DLogic__Req_RestrictTech |
| `Rogue3D_RoomSettlement` | nNodeId, tbKill, tbMonster | PROTO_L__G_Rogue3DLogic_Req_SendAchievementData<br>_G_Rogue3DLogic__Req_SendAchievementData |
| `Rogue3D_SaveFightData` | tbData | PROTO_L__G_Rogue3DSave_Reset<br>PROTO_L__G_Rogue3DSave_SaveReal |
| `Rogue3D_SaveSeasonFightData` | — | PROTO_L__G_Rogue3DSave_SaveReal |
| `Rogue3D_SeasonLevelReset` | nDiffId, tbMember | PROTO_L__G_Rogue3DLogic_Req_SeasonLevelReset<br>_G_Rogue3DLogic__Req_SeasonLevelReset |
| `Rogue3D_SeasonRoomSettlement` | nNodeId, tbKill, tbMonster | PROTO_L__G_Rogue3DLogic_Req_SendAchievementData<br>PROTO_L__G_Rogue3DLogic_Req_SendSeasonAchievementData |
| `Rogue3D_SelectDiff` | nDiffId | PROTO_L__G_Rogue3DLogic_Req_SelectDiff<br>_G_Rogue3DLogic__Req_SelectDiff |
| `Rogue3D_SelectMode` | nModeID | PROTO_L__G_Rogue3DLogic_Req_SelectMode<br>_G_Rogue3DLogic__Req_SelectMode |
| `Rogue3D_SelectSeasonTalent` | nTalentId | PROTO_L__G_Rogue3DLogic_Req_SelectSeasonTalent<br>_G_Rogue3DLogic__Req_SelectSeasonTalent |
| `Rogue3D_SelectTalent` | nTalentId | PROTO_L__G_Rogue3DLogic_Req_SelectTalent<br>_G_Rogue3DLogic__Req_SelectTalent |
| `Rogue3D_UnlockJourneyLine` | nLineID, nPeriodID | PROTO_L__G_Rogue3DAdventure_Req_UnlockJourneyLine |
| `Rogue3D_UpgradeTech` | nTechId | PROTO_L__G_Rogue3DLogic_Req_UpgradTech<br>_G_Rogue3DLogic__Req_UpgradTech |
| `Rogue3D_VisitJourneyNode` | nNodeID, nPeriodID | PROTO_L__G_Rogue3DAdventure_Req_VisitJourneyNode |

## DarkZone (14)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DarkZone_CheckOpenAct` | — | PROTO_L__G_DarkZone_CheckOpenAct/_ENV |
| `DarkZone_CompleteMission` | nChallengeId, nId, nMiniLevelId, nNpcId | PROTO_L__G_ExploreMission_ReqCompleteMission |
| `DarkZone_EndExplore` | nLevelID | PROTO_L__G_DarkZone_EndExplore |
| `DarkZone_EnterLevel` | nLevelID, tbLog | PROTO_L__G_DarkZone_Req_EnterLevel |
| `DarkZone_EnterMiniLevel` | nLevelID | PROTO_L__G_DarkZone_Req_EnterMiniLevel |
| `DarkZone_ExchangeData` | nLevelID | PROTO_L__G_DarkZone_Exchange |
| `DarkZone_ExchangeKey` | nLevelID, nNum | PROTO_L__G_DarkZone_ExchangeKey |
| `DarkZone_GetGainReward` | dataId, nGainId, nLevelID | PROTO_L__G_DarkZone_GetGainReward |
| `DarkZone_GetLevelAward` | tbIdList | PROTO_L__G_DarkZone_DoGetAward |
| `DarkZone_GetMissionAward` | nId | PROTO_L__G_ExploreMission_ReqMissionAward |
| `DarkZone_LeaveLevel` | tbLog | PROTO_L__G_DarkZone_Req_LeaveLevel |
| `DarkZone_RefreshMission` | — | PROTO_L__G_ExploreMission_ReqRefreshEntrust |
| `DarkZone_SaveFightData` | bRS, nLevelID, nSaveType, tbData | PROTO_L__G_DarkZone_SaveFightData |
| `DarkZone_TrackingMission` | bClose, nId | PROTO_L__G_ExploreMission_ReqTrackingMission |

## StarWish (13)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `StarWish_AutoCompleteStoryQuest` | nID | PROTO_L__G_StarWishLogic_AutoCompleteStoryQuest<br>_G_StarWishLogic__AutoCompleteStoryQuest |
| `StarWish_CheckOpenAct` | — | PROTO_L__G_StarWishLogic_CheckOpenAct/_ENV<br>_G_StarWishLogic__CheckOpenAct/_ENV |
| `StarWish_CleanSubIDCompleted` | nID | PROTO_L__G_StarWishLogic_CleanSubIDCompleted<br>_G_StarWishLogic__CleanSubIDCompleted |
| `StarWish_CompleteShareAchievement` | — | PROTO_L__G_StarWishLogic_CompleteShareAchievement<br>_G_StarWishLogic__CompleteShareAchievement |
| `StarWish_GetAllCompleteAward` | — | PROTO_L__G_StarWishLogic_GetAllCompleteAward<br>_G_StarWishLogic__GetAllCompleteAward |
| `StarWish_GetRepeatQuestAward` | tbTaskID | PROTO_L__G_StarWishLogic_GetRepeatQuestAward<br>_G_StarWishLogic__GetRepeatQuestAward |
| `StarWish_GetRepeatQuestExtraAward` | nPos | PROTO_L__G_StarWishLogic_GetRepeatQuestExtraAward<br>_G_StarWishLogic__GetRepeatQuestExtraAward |
| `StarWish_GetScoreAward` | — | PROTO_L__G_StarWishLogic_GetScoreAward<br>_G_StarWishLogic__GetScoreAward |
| `StarWish_GetStoryPageAward` | nID | PROTO_L__G_StarWishLogic_GetStoryPageAward<br>_G_StarWishLogic__GetStoryPageAward |
| `StarWish_GetStoryQuestAward` | tbID | PROTO_L__G_StarWishLogic_GetStoryQuestAward<br>_G_StarWishLogic__GetStoryQuestAward |
| `StarWish_LotteryJigsaw` | nTimes | PROTO_L__G_StarWishLogic_LotteryJigsaw<br>_G_StarWishLogic__LotteryJigsaw |
| `StarWish_SetStoryQuestCompleted` | Value, bShowPop, nID | PROTO_L__G_StarWishLogic_SetStoryQuestCompleted<br>_G_StarWishLogic__SetStoryQuestCompleted |
| `StarWish_SetSubIDCompleted` | bShowPop, nID, nPos, v | PROTO_L__G_StarWishLogic_SetSubIDCompleted<br>_G_StarWishLogic__SetSubIDCompleted |

## DreamCard (12)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DreamCard_CheckOpen` | — | PROTO_L__G_DreamCard_CheckOpen |
| `DreamCard_CleanData` | — | PROTO_L__G_DreamCard_CleanData |
| `DreamCard_EndlessLevelSettlement` | nID, nType, tbLog, tbUpScore | PROTO_L__G_DreamCard_EndlessLevelSettlement |
| `DreamCard_EnterLevel` | nDiff, nID, nRoleId, nType | PROTO_L__G_DreamCard_EnterLevel |
| `DreamCard_LevelOut` | nDiff, nID, nSeed, nType, tbLog | PROTO_L__G_DreamCard_LevelOut |
| `DreamCard_QuickGetReward` | tbIdList | PROTO_L__G_DreamCard_DoGetMission |
| `DreamCard_QuickGetScoreReward` | nId, tbIdList | PROTO_L__G_DreamCard_DoGetScoreMission |
| `DreamCard_QuickGetStarReward` | tbIdList | PROTO_L__G_DreamCard_DoGetStarMission |
| `DreamCard_ResetTalent` | nID, nTab | PROTO_L__G_DreamCard_ResetTalent |
| `DreamCard_UnlockTalent` | nID | PROTO_L__G_DreamCard_UnlockTalent |
| `DreamCard_UpdateData` | — | PROTO_L__G_DreamCard_ChackAddData<br>PROTO_L__G_DreamCard_UpdateData |
| `DreamCard_UpdateData3` | — | PROTO_L__G_DreamCard_UpdateData3 |

## (无前缀) (11)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ChangeMainScene` | bClearRandom, nId | PROTO_L__G_PreviewMain_Req_ChangeMainScene |
| `DownloadMultMediaLog` | tbLog | PROTO_L__G_Mail_DownloadMultiMediaLog<br>PROTO_L__G_ShareLogic_SendLog |
| `EnterGirlRoom` | nCardId, nSkinId | PROTO_L__G_PreviewSkin_Req_EnterGirlRoom |
| `ExtendFightDynamicLog` | tbLog | PROTO_L__G_BagRogue_LevelSettlement<br>PROTO_L__G_BossLogic_Req_LevelFail |
| `ExtendFightLog` | tbLog | PROTO_L__G_BagRogue_LevelSettlement<br>PROTO_L__G_BossLogic_Req_LevelFail |
| `FavMailLog` | tbLog | PROTO_L__G_FightLevel_WriteSequenceLog |
| `GirlRoomLog` | sLog | PROTO_L__G_PreviewSkin_ReportLog |
| `LanguageChange` | nType, sEx, sLan | PROTO_L__G_Localization_NotifyLanSetting |
| `RecordConfession` | nIdx | PROTO_L__G_PreviewSkin_Req_RecordConfession |
| `ReqEntranceGreenLevel` | — | PROTO_L__G_PreviewSkin_ReqEntranceGreenLevel |
| `SettingChange` | — | PROTO_L__G_PlayerSetting_Save |

## DonoDuel (11)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DonoDuel_ChangeFormation` | bNotRefresh, nType, tbFormation | PROTO_L__G_DonoDuel_DoChangeFightFormation<br>PROTO_L__G_DonoDuel_DoChangeFormation |
| `DonoDuel_ClientCheck` | — | PROTO_L__G_DonoDuel_DoCheckOpen |
| `DonoDuel_LockSkill` | bLock, nLockSkillPos, nUniqueId | PROTO_L__G_DonoDuel_DoLockSkill |
| `DonoDuel_Recycle` | tbRecycle | PROTO_L__G_DonoDuel_DoRecycle |
| `DonoDuel_SetLock` | bLock, nUniqueId | PROTO_L__G_DonoDuel_DoLockAndUnlock |
| `DonoDuel_StudySkillTree` | nSkillId | PROTO_L__G_DonoDuel_DoStudySkillTree |
| `DonoDuel_UpgradeAttr` | nPos, nUniqueId | PROTO_L__G_DonoDuel_DoUpgradeAttr |
| `DonoDuel_UpgradeLeaderSkill` | nSkillId | PROTO_L__G_DonoDuel_DoUpgradeLeaderSkill |
| `DonoDuel_UpgradeQuality` | nUniqueId | PROTO_L__G_DonoDuel_DoUpgradeQuality |
| `DonoDuel_UpgradeSkill` | bResetAll, nPos, nSkillId, nUniqueId, tbGiveUpSkill | PROTO_L__G_DonoDuel_DoUpgradeSkill |
| `DonoDuel_UpgradeStar` | nSourStar, nUniqueId, tbMaterial | PROTO_L__G_DonoDuel_DoUpgradeStar |

## RogueLogic (11)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RogueLogic_ChangeFormation` | tbFormation | PROTO_L__G_RogueLogic_SetRogueLineup<br>_G_RogueLogic__SetRogueLineup |
| `RogueLogic_ClientMoveNext` | nID | PROTO_L__G_RogueLogic_MoveNext<br>_G_RogueLogic__MoveNext |
| `RogueLogic_EnterRogue` | — | PROTO_L__G_RogueLogic_EnterRogue<br>_G_RogueLogic__EnterRogue |
| `RogueLogic_FetchDailyBuff` | — | PROTO_L__G_RogueLogic_FetchDailyBuff<br>_G_RogueLogic__FetchDailyBuff |
| `RogueLogic_FinishNode` | — | PROTO_L__G_RogueLogic_FinishNode<br>_G_RogueLogic__FinishNode |
| `RogueLogic_QuickGetReward` | tbIdList | PROTO_L__G_RogueLogic_QuickGetReward<br>_G_RogueLogic__QuickGetReward |
| `RogueLogic_RefreshShopGoods` | nNodeID | PROTO_L__G_RogueLogic_RefreshShopGoods<br>_G_RogueLogic__RefreshShopGoods |
| `RogueLogic_ResetRogue` | — | PROTO_L__G_RogueLogic_ResetRogue<br>_G_RogueLogic__ResetRogue |
| `RogueLogic_ReviveRole` | — | PROTO_L__G_RogueLogic_ReviveRole<br>_G_RogueLogic__ReviveRole |
| `RogueLogic_ShowOpenStory` | — | PROTO_L_Launch_Classes_RogueLogic_OnSettlement |
| `RogueLogic_VisitShop` | nNodeID | PROTO_L__G_RogueLogic_VisitShop<br>_G_RogueLogic__VisitShop |

## Weapon (11)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Weapon_Break` | Id | PROTO_L__G_Weapon_Req_Break |
| `Weapon_Evolution` | Id, nItemId | PROTO_L__G_Weapon_Req_Evolution |
| `Weapon_Exchange` | CardIdA, CardIdB | PROTO_L__G_Weapon_Req_Exchange |
| `Weapon_GetUpgradePartUnlock` | gdpl, nWeaponId, weapon | PROTO_L__G_Weapon_Req_GetUpgradePartUnlock |
| `Weapon_OneKeyToMax` | Id, tbBreakUpgradeMat | PROTO_L__G_Weapon_Req_OneKeyToMax |
| `Weapon_Replace` | CardId, Id | PROTO_L__G_Weapon_Req_Replace |
| `Weapon_ReplacePart` | Id, PartId, Type | PROTO_L__G_Weapon_Req_ReplacePart |
| `Weapon_SetAssignShowDefaultPart` | Id, nFlag, nType | PROTO_L__G_Weapon_Req_SetAssignShowDefaultPart |
| `Weapon_SetDefaultAudio` | Id, nFlag | PROTO_L__G_Weapon_Req_SetDefaultAudio |
| `Weapon_ShowDefaultPart` | Id, nFlag | PROTO_L__G_Weapon_Req_SetShowDefaultPart |
| `Weapon_Upgrade` | Id, tbMat | PROTO_L__G_Weapon_Req_Upgrade |

## FarmWarLogic (10)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `FarmWarLogic_ActiveGrowNode` | nId, nSkillId | PROTO_L__G_FarmWarActivity_Req_ActiveGrowNode |
| `FarmWarLogic_ActiveLimitGrowNode` | nId, nSkillId | PROTO_L__G_FarmWarActivity_Req_ActiveLimitGrowNode |
| `FarmWarLogic_CheckActOpen` | — | PROTO_L__G_FarmWarActivity_Req_CheckActOpen |
| `FarmWarLogic_GetQuestAward` | tbIdList | PROTO_L__G_FarmWarActivity_Req_GetQuestAward |
| `FarmWarLogic_ResetGrow` | nId, nType | PROTO_L__G_FarmWarActivity_Req_ResetGrow |
| `FarmWarLogic_ResetGrowNode` | nId, nSkillId | PROTO_L__G_FarmWarActivity_Req_ResetGrowNode |
| `FarmWarLogic_ResetLimitGrow` | nId | PROTO_L__G_FarmWarActivity_Req_ResetLimitGrow |
| `FarmWarLogic_ResetLimitGrowNode` | nId, nSkillId | PROTO_L__G_FarmWarActivity_Req_ResetLimitGrowNode |
| `FarmWarLogic_SwitchLimitGrowNode` | — | PROTO_L__G_FarmWarActivity_Req_SwitchLimitGrowNode |
| `FarmWarLogic_UpdateFormation` | nLevelId, tbTeam | PROTO_L__G_FarmWarActivity_Req_UpdateFormation |

## Activity (9)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Activity_BirthdayMail_Gain` | — | PROTO_L__G_BirthdayMail_RequestMail |
| `Activity_Flag` | nId, nType | PROTO_L__G_Activity_Quest_Flag |
| `Activity_GetAward` | — | PROTO_L__G_Activity_Quest_GetAward |
| `Activity_GetRoleFestivalLevelReward` | nId, nMessageNum | PROTO_L__G_RoleFestivalMessage_GetLevelReward |
| `Activity_MarkTip` | nGId, nSubId | PROTO_L__G_Sign_Req_MarkActivityTip |
| `Activity_QuickQuestAward` | nId, tbIdList | PROTO_L__G_Activity_Quick_QuestAward |
| `Activity_Refresh` | nId | PROTO_L__G_Activity_Quest_Refresh |
| `Activity_ReSign` | nId, nType | PROTO_L__G_Sign_DoResign |
| `Activity_SetRoleFestivalMessageBeRead` | nGirlId | PROTO_L__G_RoleFestivalMessage_SetMessageReadState |

## AlienDefense (9)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `AlienDefense_CheckOpenAct` | — | PROTO_L__G_AlienDefense_CheckOpenAct/_ENV |
| `AlienDefense_EnterLevel` | nID, tbLog | PROTO_L__G_AlienDefense_EnterLevel |
| `AlienDefense_GetQuestAward` | tbIdList | PROTO_L__G_AlienDefense_GetQuestAward |
| `AlienDefense_GetScoreAward` | nIdx | PROTO_L__G_AlienDefense_GetScoreAward |
| `AlienDefense_LevelFail` | tbLog | PROTO_L__G_AlienDefense_LevelFail |
| `AlienDefense_SaveFightGirl` | nGirlId | PROTO_L__G_AlienDefense_SaveFightGirl |
| `AlienDefense_SaveFightPal` | tbPalIdx | PROTO_L__G_AlienDefense_SaveFightPal |
| `AlienDefense_SetPalFlag` | — | PROTO_L__G_AlienDefense_SetPalFlag |
| `AlienDefense_UpgradeSkill` | nPalIdx, nSkillIdx | PROTO_L__G_AlienDefense_UpgradeSkill |

## PartyLogic (9)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `PartyLogic_CheckFirstSign` | nId, nTeach | PROTO_L__G_PartyLogic_CheckFirstSign<br>_G_PartyLogic__CheckFirstSign |
| `PartyLogic_SetFightCard` | nId | PROTO_L__G_PartyLogic_SetFightCard<br>_G_PartyLogic__SetFightCard |
| `PartyLogic_SetFirstSign` | nId | PROTO_L__G_PartyLogic_SetFirstSign<br>_G_PartyLogic__SetFirstSign |
| `PartyLogic_SetMatchId` | nId | PROTO_L__G_PartyLogic_SetMatchId<br>_G_PartyLogic__SetMatchId |
| `PartyLogic_SetMatchMode` | nSingle | PROTO_L__G_PartyLogic_SetMatchMode<br>_G_PartyLogic__SetMatchMode |
| `PartyLogic_SetRandomMapId` | nId, nSetData, nSingle, tbMapId | PROTO_L__G_PartyLogic_SetRandomMapId<br>_G_PartyLogic__SetRandomMapId |
| `PartyLogic_SetSkillID` | nId1, nId2 | PROTO_L__G_PartyLogic_SetFightSkill<br>_G_PartyLogic__SetFightSkill |
| `PartyLogic_SetTitle` | nId | PROTO_L__G_PartyLogic_SetTitle<br>_G_PartyLogic__SetTitle |
| `PartyLogic_SetTitleShow` | nType | PROTO_L__G_PartyLogic_SetTitleShow<br>_G_PartyLogic__SetTitleShow |

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
| `VirCapture_ChangeBagRedFlag` | bFlag | PROTO_L__G_VirCapture_DoChangeBagRedFlag |
| `VirCapture_ChangeFormation` | nId, nUnloadId | PROTO_L__G_VirCapture_DoChangeFormation |
| `VirCapture_CheckOpenAct` | — | PROTO_L__G_VirCapture_CheckOpenAct/_ENV |
| `VirCapture_GachaMonster` | bTen | PROTO_L__G_VirCapture_DoGachaMonster |
| `VirCapture_GetLevelAward` | nId, tbIdList | PROTO_L__G_VirCapture_DoGetLevelAward |
| `VirCapture_GetRikiAward` | nId, tbIdList | PROTO_L__G_VirCapture_DoGetRikiAward |
| `VirCapture_SetLock` | MonsterId, bLock | PROTO_L__G_VirCapture_DoLockAndUnlock |
| `VirCapture_SwitchDayNight` | nMapId | PROTO_L__G_VirCapture_DoSwitchDayNight |
| `VirCapture_UpgradeLevel` | nId, nSkillId | PROTO_L__G_VirCapture_DoUpgradeLevel |

## GirlCard (8)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GirlCard_ProLevelPromote` | nID | PROTO_L__G_RoleCard_ProLevelPromote |
| `GirlCard_ReceiveProLevelAward` | nID, nProLevel | PROTO_L__G_RoleCard_ReceiveProLevelAward |
| `GirlCard_SetRoleLeave` | nValue, tbID | PROTO_L__G_RoleCard_SetAllRoleLeave<br>PROTO_L__G_RoleCard_SetRoleLeave |
| `GirlCard_SetRoleLikeFlag` | nCardID, nFlag | PROTO_L__G_RoleCard_Req_SetRoleLikeFlag |
| `GirlCard_UnLockCharacter` | d, g, l, p | PROTO_L__G_RoleCard_Req_UnLockPlayer |
| `GirlCard_UpByBreak` | nBreakLv, pId, tbMaterials | PROTO_L__G_RBreak_Req_ByBreak |
| `GirlCard_UpBySpecialBreak` | nCardId | PROTO_L__G_RBreak_Req_BySpecialBreak |
| `GirlCard_UpdateLevel` | Id, tbMaterials | PROTO_L__G_RoleCard_Req_LevelUp |

## RichManLoveLogic (8)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RichManLoveLogic_CheckOpenAct` | — | PROTO_L__G_RichManLoveLogic_CheckOpenAct<br>_G_RichManLoveLogic__CheckOpenAct |
| `RichManLoveLogic_EnterMap` | bContinue, nId, nMapId | PROTO_L__G_RichManLoveLogic_EnterMap<br>_G_RichManLoveLogic__EnterMap |
| `RichManLoveLogic_EnterMapLog` | nMapId, nSeed, tbLog | PROTO_L__G_RichManLoveLogic_EnterMapLog<br>_G_RichManLoveLogic__EnterMapLog |
| `RichManLoveLogic_LikeEnd` | nId | PROTO_L__G_RichManLoveLogic_LikeEnd<br>_G_RichManLoveLogic__LikeEnd |
| `RichManLoveLogic_MapSettlement` | activityId, activityType, mapId, nSeed, tbLevelNum | PROTO_L__G_RichManLoveLogic_MapSettlement<br>_G_RichManLoveLogic__MapSettlement |
| `RichManLoveLogic_QuickGetReward` | tbIdList | PROTO_L__G_RichmanLogic_DoGetMission<br>_G_RichmanLogic__DoGetMission |
| `RichManLoveLogic_SettlementUnlockEnd` | nId, nMapId, tbLog | PROTO_L__G_RichManLoveLogic_SettlementUnlockEnd<br>_G_RichManLoveLogic__SettlementUnlockEnd |
| `RichManLoveLogic_UseDice` | — | PROTO_L__G_RichManLoveLogic_UseDice<br>_G_RichManLoveLogic__UseDice |

## BossLogic (7)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `BossLogic_EnterLevel` | nDifficulty, nID, nTeamID, tbEntrie, tbLog | PROTO_L__G_BossLogic_Req_EnterLevel<br>_G_BossLogic__Req_EnterLevel |
| `BossLogic_GetOpenID` | — | PROTO_L__G_BossLogic_GetOpenID/_ENV<br>_G_BossLogic__GetOpenID/_ENV |
| `BossLogic_GetReward` | Mileage | PROTO_L__G_BossLogic_GetReward<br>_G_BossLogic__GetReward |
| `BossLogic_LevelFail` | nID, tbLog | PROTO_L__G_BossLogic_Req_LevelFail<br>_G_BossLogic__Req_LevelFail |
| `BossLogic_OneClicReward` | — | PROTO_L__G_BossLogic_OneClicReward<br>_G_BossLogic__OneClicReward |
| `BossLogic_Record` | bRecord, nID, nSeed, nTime | PROTO_L__G_BossLogic_Record<br>_G_BossLogic__Record |
| `BossLogic_Reset` | nID | PROTO_L__G_BossLogic_Reset<br>_G_BossLogic__Reset |

## JigsawPuzzle (7)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `JigsawPuzzle_EnterLog` | nEnterType, nId | PROTO_L__G_JigsawPuzzle_EnterLog |
| `JigsawPuzzle_GetGirl` | nId | PROTO_L__G_JigsawPuzzle_GetGirl |
| `JigsawPuzzle_GetPiece` | nActivityId, nId, nNum, nStage | PROTO_L__G_JigsawPuzzle_GetPiece |
| `JigsawPuzzle_GetReward` | nActId, nId | PROTO_L__G_JigsawPuzzle_GetMissionReward |
| `JigsawPuzzle_PutPiece` | nActId, nId | PROTO_L__G_JigsawPuzzle_PutPiece |
| `JigsawPuzzle_SetActive` | nId | PROTO_L__G_JigsawPuzzle_SetActive |
| `JigsawPuzzle_UseHelp` | nActId, nId | PROTO_L__G_JigsawPuzzle_UseHelp |

## ClimbTowerLogic (6)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ClimbTowerLogic_CheckCycleLevel` | — | PROTO_L__G_ClimbTowerLogic_CheckCycleLevel/_ENV<br>_G_ClimbTowerLogic__CheckCycleLevel/_ENV |
| `ClimbTowerLogic_GetReward` | nGroup, nLayer, nType | PROTO_L__G_ClimbTowerLogic_GetReward<br>_G_ClimbTowerLogic__GetReward |
| `ClimbTowerLogic_OneClicReward` | nGroup, nType | PROTO_L__G_ClimbTowerLogic_OneClicReward<br>_G_ClimbTowerLogic__OneClicReward |
| `ClimbTowerLogic_RecordChallenged` | nID | PROTO_L__G_ClimbTowerLogic_RecordChallenged<br>_G_ClimbTowerLogic__RecordChallenged |
| `ClimbTowerLogic_RecordProgres` | nArea, nID, nStar, nTeamEnergy, tbRoleHP | PROTO_L__G_ClimbTowerLogic_RecordProgres<br>_G_ClimbTowerLogic__RecordProgres |
| `ClimbTowerLogic_SetLevelDiff` | nDiff | PROTO_L__G_ClimbTowerLogic_SetLevelDiff<br>_G_ClimbTowerLogic__SetLevelDiff |

## FishingServer (6)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `FishingServer_BeginFishing` | nNodeID, nSelectBait | PROTO_L__G_FishingLogic_BeginFishing<br>_G_FishingLogic__BeginFishing |
| `FishingServer_ConvertFood` | nFoodID, nNum | PROTO_L__G_FishingLogic_GetCookAward<br>_G_FishingLogic__GetCookAward |
| `FishingServer_EndFishing` | nState | PROTO_L__G_FishingLogic_EndFishing<br>_G_FishingLogic__EndFishing |
| `FishingServer_GetCollectAward` | nId, tbIdList | PROTO_L__G_FishingLogic_GetCollectAward<br>_G_FishingLogic__GetCollectAward |
| `FishingServer_GetLevelAward` | nLevel | PROTO_L__G_FishingLogic_GetLevelAward<br>_G_FishingLogic__GetLevelAward |
| `FishingServer_ReadFishRecord` | nFishID | PROTO_L__G_FishingLogic_ReadFishRecord<br>_G_FishingLogic__ReadFishRecord |

## PlayerSetting (6)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `PlayerSetting_ChangeAccountShowCard` | nIndex, nItemID | PROTO_L__G_PlayerSetting_Req_ChangeAccountShowCard |
| `PlayerSetting_ChangeAccountShowSkin` | nIndex, nItemID | PROTO_L__G_PlayerSetting_Req_ChangeAccountShowSkin |
| `PlayerSetting_ChangeShowCard` | nID | PROTO_L__G_PlayerSetting_Req_ChangeRole |
| `PlayerSetting_GetPlayTime` | — | PROTO_L__G_HealthTip_Req_PlayTime |
| `PlayerSetting_ReportPlayTime` | nTime | PROTO_L__G_HealthTip_SavePlayTime |
| `PlayerSetting_SetShowBadge` | tbBadge | PROTO_L__G_PlayerSetting_Req_ChangeAccountShowBadge |

## BattlePassLogic (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `BattlePassLogic_BuyLevel` | nLevel | PROTO_L__G_BattlePass_DoBuyLevel |
| `BattlePassLogic_ClientRefresh` | — | PROTO_L__G_BattlePass_DoRefresh |
| `BattlePassLogic_FirstOpen` | — | PROTO_L__G_BattlePass_DoFirstOpen |
| `BattlePassLogic_GetPassAward` | — | PROTO_L__G_BattlePass_DoGetAward |
| `BattlePassLogic_QuickGetReward` | tbIdList | PROTO_L__G_BattlePass_DoGetMission |

## BossPvpLogic (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `BossPvpLogic_EnterLevel` | nDifficulty, nID, nLevelID, nTeamID, tbEntrie, tbLog | PROTO_L__G_BossPvpLogic_Req_EnterLevel<br>_G_BossPvpLogic__Req_EnterLevel |
| `BossPvpLogic_GetOpenID` | — | PROTO_L__G_BossPvpLogic_GetOpenID/_ENV<br>_G_BossPvpLogic__GetOpenID/_ENV |
| `BossPvpLogic_GetReward` | tbTaskID | PROTO_L__G_BossPvpLogic_GetReward<br>_G_BossPvpLogic__GetReward |
| `BossPvpLogic_LevelMopup` | nDiff, nID | PROTO_L__G_BossPvpLogic_Req_LevelMopup<br>_G_BossPvpLogic__Req_LevelMopup |
| `BossPvpLogic_Record` | ResidueTime, bRecord, nDiff, nID, nSeed, nTime | PROTO_L__G_BossPvpLogic_Record<br>_G_BossPvpLogic__Record |

## DefendLogic (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DefendLogic_CheckOpenAct` | — | PROTO_L__G_DefendLogic_CheckOpenAct/_ENV<br>PROTO_L__G_DefendLogic_GetOpenConf |
| `DefendLogic_EnterLevel` | nDiff, nID, nTeamID, tbLog | PROTO_L__G_DefendLogic_Req_EnterLevel<br>_G_DefendLogic__Req_EnterLevel |
| `DefendLogic_GetLevelAward` | tbIdList | PROTO_L__G_DefendLogic_Req_GetLevelAward<br>_G_DefendLogic__Req_GetLevelAward |
| `DefendLogic_GetReward` | bAll, nDiff, nID, nIdx, nTargetId | PROTO_L__G_DefendLogic_GetReward<br>PROTO_L__G_DefendLogic_GetRewardAll |
| `DefendLogic_SelectDiff` | nDiffId | PROTO_L__G_DefendLogic_Req_SelectDiff<br>_G_DefendLogic__Req_SelectDiff |

## Gacha (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Gacha_GetOpenTime` | — | PROTO_L__G_Gacha_PullOpenTime |
| `Gacha_Launch` | bPickUp, nId, nTime | PROTO_L__G_Gacha_Req_Launch |
| `Gacha_PickUp` | nId, nPickUp | PROTO_L__G_Gacha_Req_PickUp |
| `Gacha_TogglePickUp` | nId | PROTO_L__G_Gacha_Req_TogglePickUp |
| `Gacha_UpSelect` | gdpl, nId | PROTO_L__G_Gacha_Req_UpSelect |

## GirlSkin (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GirlSkin_Change` | CardId, Id | PROTO_L_Item_Fashion_ChangeSkinReq |
| `GirlSkin_ChangeSkinType` | nSkinId, nType | PROTO_L_Item_Fashion_Req_ChangeSkinType |
| `GirlSkin_ChangeSkinType2` | nSkinId, nType | PROTO_L_Item_Fashion_Req_ChangeSkinType2 |
| `GirlSkin_RandomChange` | tbCardId, tbId | PROTO_L_Item_Fashion_RandomChangeSkinReq |
| `GirlSkin_ResetRandomChange` | — | PROTO_L_Item_Fashion_ResetRandomChangeSkinReq |

## LimitedTime (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `LimitedTime_CheckLimitedItemRecycle` | — | PROTO_L__G_LimitedRole_CheckLimitedItemRecycle |
| `LimitedTime_CheckLimitedItemUpdate` | — | PROTO_L__G_LimitedRole_CheckLimitedItemUpdate |
| `LimitedTime_CheckLimitedRoleGet` | — | PROTO_L__G_LimitedRole_CheckLimitedRoleGet |
| `LimitedTime_CheckLimitedSupportGet` | — | PROTO_L__G_LimitedRole_CheckLimitedSupportGet |
| `LimitedTime_CheckLimitedWeaponGet` | — | PROTO_L__G_LimitedRole_CheckLimitedWeaponGet |

## Online (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Online_ClientLog` | AREnter, ARQuit, GiftboxSuggest, LevelPerformance, ShieldEmoji | PROTO_L__G_ArLogic_RecordEnterLog<br>PROTO_L__G_ArLogic_RecordQuitLog |
| `Online_CostVigour` | bOpen | PROTO_L__G_Online_VigourSwitch |
| `Online_FirstPop` | nId | PROTO_L__G_Online_CheckNoPopInfo<br>PROTO_L__G_Online_CheckPopInfo |
| `Online_RecordPartySpectateLog` | tbLog | PROTO_L__G_Online_SendPartySpectateLog |
| `Online_WeeklyAward` | — | PROTO_L__G_Online_GetAllWeeklyAward |

## RichmanLogic (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RichmanLogic_CheckOpenAct` | — | PROTO_L__G_RichmanLogic_CheckOpenAct<br>_G_RichmanLogic__CheckOpenAct |
| `RichmanLogic_EnterMap` | bContinue, nId, nMapId, tbLog | PROTO_L__G_RichmanLogic_EnterMap<br>_G_RichmanLogic__EnterMap |
| `RichmanLogic_MapSettlement` | activityId, activityType, mapId, nRank, nSeed, tbLevelNum, tbLog | PROTO_L__G_RichmanLogic_MapSettlement<br>_G_RichmanLogic__MapSettlement |
| `RichmanLogic_ReceiveVoteveReward` | nId | PROTO_L__G_RichmanLogic_ReceiveVoteveReward<br>_G_RichmanLogic__ReceiveVoteveReward |
| `RichmanLogic_VoteGirl` | nId, nNum, nTotalNum | PROTO_L__G_RichmanLogic_VoteGirl<br>_G_RichmanLogic__VoteGirl |

## SeasonBoss (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `SeasonBoss_CheckOpen` | ForceEnter | PROTO_L__G_SeasonBossLogic_CheckOpen<br>_G_SeasonBossLogic__CheckOpen |
| `SeasonBoss_EnterLevel` | nDifficulty, nID, nTeamID, nZoneID, tbEntrie, tbLog | PROTO_L__G_SeasonBossLogic_Req_EnterLevel<br>_G_SeasonBossLogic__Req_EnterLevel |
| `SeasonBoss_GetReward` | tbTaskID | PROTO_L__G_SeasonBossLogic_GetReward<br>_G_SeasonBossLogic__GetReward |
| `SeasonBoss_LevelFail` | ResidueTime, nDamage, nDiff, nID, nReason, nSeed, nTime, nZoneID, tbLog | PROTO_L__G_SeasonBossLogic_Req_LevelFail<br>_G_SeasonBossLogic__Req_LevelFail |
| `SeasonBoss_Record` | ResidueTime, bRecord, nDamage, nDiff, nID, nSeed, nTime, nZoneID | PROTO_L__G_SeasonBossLogic_Record<br>_G_SeasonBossLogic__Record |

## VirCaptureTask (5)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `VirCaptureTask_DoCheckCostTask` | nMapId | PROTO_L__G_VirCaptureTask_ReqGetCostTask |
| `VirCaptureTask_DoGiveUp` | nMapId, nMissionId | PROTO_L__G_VirCaptureTask_ReqGiveUpMission |
| `VirCaptureTask_DoRandom` | nMapId | PROTO_L__G_VirCaptureTask_ReqGetRandomMission |
| `VirCaptureTask_DoSomething` | — | PROTO_L__G_VirCaptureTask_ReqDoSomething |
| `VirCaptureTask_GetReward` | nId | PROTO_L__G_VirCaptureTask_ReqGetReward |

## DonoDuelTask (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DonoDuelTask_Accept` | nId | PROTO_L__G_DonoDuelTask_ReqAccept |
| `DonoDuelTask_DoSomething` | — | PROTO_L__G_DonoDuelTask_ReqDoSomething |
| `DonoDuelTask_GetReward` | nId | PROTO_L__G_DonoDuelTask_DoReqGetReward |
| `DonoDuelTask_QuickGetReward` | tbIdList | PROTO_L__G_DonoDuelTask_QuickGetReward |

## GirlSpine (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GirlSpine_ChildNodeReset` | pId | PROTO_L__G_Spine_Req_ChildNodeReset |
| `GirlSpine_ChildUnLock` | pId, tbInfo, tbMasterList, tbMat | PROTO_L__G_Spine_Req_ChildNode |
| `GirlSpine_MasterUnlock` | NodeId, pId | PROTO_L__G_Spine_Req_MasterNode |
| `GirlSpine_UnlockNodeOneKey` | nIdx, pId, tbMasterList, tbOneKey | PROTO_L__G_Spine_Req_OneKey |

## OnlineActivity (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineActivity_QuestAward` | nId, tbIdList | PROTO_L__G_OnlineActivity_GetAllQuestAward |
| `OnlineActivity_Request` | — | PROTO_L__G_Online_CheckOpenList |
| `OnlineActivity_SetOnlineTrial` | nId, nTrialId | PROTO_L__G_Online_SyncOnlineTrial |
| `OnlineActivity_SetProfession` | nId, nProf | PROTO_L__G_Online_SyncOnlineSetProf |

## OnlineAssaultOps (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineAssaultOps_ChangeFormation` | nFormationId, nOnlineId | PROTO_L__G_OnlineAssaultOps_ReqChangeFormation |
| `OnlineAssaultOps_Equip` | bUnEquip, nChipId, nFormationId, nOnlineId, nPos | PROTO_L__G_OnlineAssaultOps_ReqEquipChip |
| `OnlineAssaultOps_QuestAward` | nOnlineId, tbIdList | PROTO_L__G_OnlineAssaultOps_GetAllQuestAward |
| `OnlineAssaultOps_SystemEquip` | nFormationId, nOnlineId, nSysModIndx, tbEquipList | PROTO_L__G_OnlineAssaultOps_ReqSystemEquipChip |

## OnlineSea (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineSea_BuyMod` | nModId, nOnlineId | PROTO_L__G_OnlineSea_ReqBuyMod |
| `OnlineSea_Equip` | bFormation, nFormationId, nOnlineId, nSysModIndx, tbEquipList | PROTO_L__G_OnlineSea_ReqEquip |
| `OnlineSea_SetAutoBuy` | bAutoBuy, nFormationId, nOnlineId | PROTO_L__G_OnlineSea_ReqSetAutoBuy |
| `OnlineSea_UseFormation` | bUse, nFormationId, nOnlineId, nSysModIndx | PROTO_L__G_OnlineSea_ReqUseFormation |

## ShopLogic (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ShopLogic_BuyGoods` | nBuyMode, nCount, nGoodsId | PROTO_L__G_ShopLogic_BuyGoods<br>_G_ShopLogic__BuyGoods |
| `ShopLogic_GetGoodsList` | nShopId | PROTO_L__G_ShopLogic_GetGoodsList<br>_G_ShopLogic__GetGoodsList |
| `ShopLogic_GetOpenTime` | — | PROTO_L__G_ShopLogic_GetOpenTime<br>_G_ShopLogic__GetOpenTime |
| `ShopLogic_UpdateShop` | nShopId | PROTO_L__G_ShopLogic_UpdateShop<br>PROTO_L__G_ShopLogic_UpdateShop/_ENV |

## VirCaptureBuild (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `VirCaptureBuild_AssignWorker` | nId, nStaffId, nStaffState | PROTO_L__G_VirCaptureBuild_ReqAssignWorker |
| `VirCaptureBuild_OperateBuilding` | nMapId | PROTO_L__G_VirCaptureBuild_ReqOperateBuilding |
| `VirCaptureBuild_UpgradeAttribute` | nAttrIndx, nId | PROTO_L__G_VirCaptureBuild_ReqUpgradeAttribute |
| `VirCaptureBuild_UpgradeBuild` | nId | PROTO_L__G_VirCaptureBuild_ReqUpgradeBuild |

## VirCaptureLevel (4)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `VirCaptureLevel_ChangeFlag` | bClean, nLevelID, nRegionId, nSeed | PROTO_L__G_VirCapture_ChangeFlag |
| `VirCaptureLevel_SaveCapture` | nLevelID, nRegionId, nSeed | PROTO_L__G_VirCapture_DoSaveCaptureMonster |
| `VirCaptureLevel_SaveFightData` | nLevelID, nRegionId, nSeed | PROTO_L__G_VirCapture_DoSaveMonsterFightData |
| `VirCaptureLevel_SavePos` | nLevelID, nPosX, nPosY, nPosZ, nSeed, nToward, tbKill, tbMonster | PROTO_L__G_VirCapture_SavePos |

## Achievement (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Achievement_GetReward` | nId | PROTO_L__G_Achievement_GetExtraReward<br>PROTO_L__G_Achievement_GetReward |
| `Achievement_OnAddSomeOne` | nType, tbParam | PROTO_L__G_AchievementExtend_CheckBindingSeasun/_ENV<br>PROTO_L__G_AchievementExtend_CheckLevelPass |
| `Achievement_QuickGetReward` | nType, tbIdList, tbPointList | PROTO_L__G_Achievement_QuickGetReward |

## chess.apply (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `chess.apply_get_reward` | ShowTip, activityId, activityType, rewardIndex | PROTO_L__G_ChessData_SetReward |
| `chess.apply_map_complete` | QuitGame, activityId, activityType, mapId | PROTO_L__G_ChessData_SetMapComplete |
| `chess.apply_on_map_save` | activityId, activityType, moduleName, tbMapId | PROTO_L__G_ChessData_C2S_OnMapSave |

## ChessLogic (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ChessLogic_ChangeFormation` | tbFormation | PROTO_L__G_ChessLogic_SetLineup<br>_G_ChessLogic__SetLineup |
| `ChessLogic_CheckOpenAct` | — | PROTO_L__G_ChessLogic_CheckOpenAct/_ENV<br>_G_ChessLogic__CheckOpenAct/_ENV |
| `ChessLogic_EnterMap` | nId, nMapId | PROTO_L__G_ChessLogic_EnterMap<br>_G_ChessLogic__EnterMap |

## DecryptLogic (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DecryptLogic_CleanSubIDCompleted` | nID | PROTO_L__G_DecryptLogic_CleanSubIDCompleted<br>_G_DecryptLogic__CleanSubIDCompleted |
| `DecryptLogic_SetCompleted` | Value, nID | PROTO_L__G_DecryptLogic_SetCompleted<br>_G_DecryptLogic__SetCompleted |
| `DecryptLogic_SetSubIDCompleted` | nID, nPos, v | PROTO_L__G_DecryptLogic_SetSubIDCompleted<br>_G_DecryptLogic__SetSubIDCompleted |

## GuideLogic (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GuideLogic_GMSetBeginner` | — | PROTO_L__G_GuideLogic_SkipAllGuide<br>_G_GuideLogic__SkipAllGuide |
| `GuideLogic_SetBeginner` | nType | PROTO_L__G_GuideLogic_SetBeginner<br>_G_GuideLogic__SetBeginner |
| `GuideLogic_WriteGuideLog` | logstr | PROTO_L__G_GuideLogic_ChackGuideLog<br>_G_GuideLogic__ChackGuideLog |

## IBLogic (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `IBLogic_BuyGoods` | nCount, nGoodsId, nIndex, nType, tbSelectItem1, tbSelectItem2 | PROTO_L__G_IBLogic_DoBuyProduct<br>_G_IBLogic__DoBuyProduct |
| `IBLogic_GoodsRedDot` | tbList | PROTO_L__G_IBLogic_SetSkinRedDot<br>_G_IBLogic__SetSkinRedDot |
| `IBLogic_ShoppingCart` | — | PROTO_L__G_IBLogic_DoBuyProductList<br>_G_IBLogic__DoBuyProductList |

## OnlineAssaultOpsBattlePass (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineAssaultOpsBattlePass_ChangeBP` | nId | PROTO_L__G_OnlineAssaultOpsBattlePass_ChangeActivityBP |
| `OnlineAssaultOpsBattlePass_ClientRefresh` | — | PROTO_L__G_OnlineAssaultOpsBattlePass_DoRefresh |
| `OnlineAssaultOpsBattlePass_LevelAward` | nId, tbIdList | PROTO_L__G_OnlineAssaultOpsBattlePass_GetAllLevelAward |

## OnlineBattlePass (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineBattlePass_ClientRefresh` | — | PROTO_L__G_OnlineBattlePass_DoRefresh |
| `OnlineBattlePass_LevelAward` | nId, tbIdList | PROTO_L__G_OnlineBattlePass_GetAllLevelAward |
| `OnlineBattlePass_QuestAward` | nId, tbIdList | PROTO_L__G_OnlineBattlePass_GetAllQuestAward |

## OnlineCombineBattlePass (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineCombineBattlePass_ClientRefresh` | — | PROTO_L__G_OnlineCombineBattlePass_DoRefresh |
| `OnlineCombineBattlePass_LevelAward` | nId, tbIdList | PROTO_L__G_OnlineCombineBattlePass_GetAllLevelAward |
| `OnlineCombineBattlePass_QuestAward` | nId, tbIdList | PROTO_L__G_OnlineCombineBattlePass_GetAllQuestAward |

## OnlineSpeedScore (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineSpeedScore_ChangeFormation` | nFormationId, nOnlineId | PROTO_L__G_OnlineSpeedScore_ReqChangeFormation |
| `OnlineSpeedScore_Equip` | bUnEquip, nBuffId, nFormationId, nOnlineId, nPos | PROTO_L__G_OnlineSpeedScore_ReqEquipBuff |
| `OnlineSpeedScore_QuickEquip` | bAllUnEquip, nFormationId, nOnlineId, tbEquipList | PROTO_L__G_OnlineSpeedScore_ReqQuickEquipBuff |

## RandomShowGirl (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RandomShowGirl_Set` | tbForm, tbItemId | PROTO_L__G_RandomShowGirl_SetRandomGirl |
| `RandomShowGirl_SetGirlSkinInLevel` | — | PROTO_L__G_RandomShowGirl_SetRandomGirlSkinInLevel |
| `RandomShowGirl_SetMainBg` | b3D, tbId | PROTO_L__G_RandomShowGirl_SetRandomMainBg/_ENV |

## Rogue3DScoreModel (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Rogue3DScoreModel_BuyBuff` | nBuffId | PROTO_L__G_Rogue3DScoreModel_Req_BuyBuff |
| `Rogue3DScoreModel_LevelScoreAward` | nLevelId, tbIdList | PROTO_L__G_Rogue3DScoreModel_Req_LevelScoreAward |
| `Rogue3DScoreModel_SaveBuffPlan` | nIndex, tbCommonBuff, tbPlayerBuff | PROTO_L__G_Rogue3DScoreModel_Req_SaveBuffPlan |

## Rogue3DUav (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Rogue3DUav_ChangeCore` | — | PROTO_L__G_Rogue3DUav_ReqChangeCore |
| `Rogue3DUav_Equip` | — | PROTO_L__G_Rogue3DUav_ReqEquip |
| `Rogue3DUav_Merge` | — | PROTO_L__G_Rogue3DUav_ReqMerge |

## Seven (3)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Seven_day_getAchievementAward` | achievementId, actId, index | PROTO_L_Activity_SevenDay_GetAcheveimentAward |
| `Seven_day_getAllRewardCanGet` | — | PROTO_L_Activity_SevenDay_GetAllRewardCanGet |
| `Seven_day_getIndexAward` | actId, index | PROTO_L_Activity_SevenDay_GetIndexAward |

## AchievementDLC (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `AchievementDLC_GetReward` | nId | PROTO_L__G_AchievementDLC_GetReward |
| `AchievementDLC_QuickGetReward` | tbIdList | PROTO_L__G_AchievementDLC_QuickGetReward |

## AchievementExtend (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `AchievementExtend_RefreshPopFlag` | tbList | PROTO_L__G_AchievementExtend_SetRefreshPopFlag |
| `AchievementExtend_WeeklyRedDot` | tbList | PROTO_L__G_AchievementExtend_SetWeeklyRedDot |

## AchievementVirCapture (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `AchievementVirCapture_GetReward` | nId | PROTO_L__G_AchievementVirCapture_GetReward |
| `AchievementVirCapture_QuickGetReward` | tbIdList | PROTO_L__G_AchievementVirCapture_QuickGetReward |

## Chess (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Chess_EnterLevel` | activityId, activityType, fightId, moduleName, nTeamID, tbLog | PROTO_L__G_ChessClient_Req_EnterLevel |
| `Chess_LevelFail` | activityId, activityType, fightId, moduleName, tbLog | PROTO_L__G_ChessClient_Req_LevelFail |

## ClimbTower (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ClimbTower_Award` | — | PROTO_L__G_ClimbTower_GetAward |
| `ClimbTower_EnterLevel` | — | PROTO_L__G_ClimbTower_EnterLevel |

## FunTimed (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `FunTimed_EnterLevel` | nID, nSession, nTeamID, tbLog | PROTO_L__G_FunTimed_EnterLevel |
| `FunTimed_LevelExit` | nID, tbLog | PROTO_L__G_FunTimed_ExitLevel |

## GachaTry (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GachaTry_EnterLevel` | nActId, nGirlIdx, nLevelID, tbLog | PROTO_L__G_GachaTry_Req_EnterLevel |
| `GachaTry_LevelFail` | nActId, nGirlIdx, nLevelID, tbLog | PROTO_L__G_GachaTry_Req_LevelFail |

## Item (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Item_Expiration` | tbItems | PROTO_L__G_Item_Expiration/_ENV |
| `Item_SetReadFlag` | ItemId, bReaded | PROTO_L_UMG_Main_umg_main_CheckBagRed |

## ItemConsole (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ItemConsole_Decomposition` | gdpl, nNum | PROTO_L__G_ItemConsole_Req_Decomposition |
| `ItemConsole_Synthesis` | gdpl, nNum | PROTO_L__G_ItemConsole_Req_Synthesis |

## OnlineForbidzone (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineForbidzone_Equip` | nId | PROTO_L__G_OnlineForbidzone_ReqEquip |
| `OnlineForbidzone_LevelUp` | nId, nOldLevel, nSelectLevel | PROTO_L__G_OnlineForbidzone_ReqLevelUp |

## PlayerCharge (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `PlayerCharge_GetAward` | — | PROTO_L__G_PlayerCharge_GetChargeAward |
| `PlayerCharge_Switch` | — | PROTO_L__G_PlayerCharge_SetSwitch |

## PSCamera (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `PSCamera_SetEnterLog` | — | PROTO_L__G_PSMgr_SetEnterLog |
| `PSCamera_SetLog` | Detail, MapId | PROTO_L__G_PSMgr_SetLog |

## RikiLogic (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RikiLogic_AddExploreRiki` | — | PROTO_L__G_FragmentStory_Show |
| `RikiLogic_AddSouvenirRiki` | — | PROTO_L__G_Mail_CheckSouvenir |

## Rouge3D (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Rouge3D_ConvertJourneyKey` | nNodeID, nNum, nTargetCashID, tbFromCashID | PROTO_L__G_Rogue3DAdventure_Req_ShopSwap |
| `Rouge3D_ExchangeJourneyKey` | nNodeID, nNum, nTargetCashID | PROTO_L__G_Rogue3DAdventure_Req_ExchangeKey |

## TowerLevel (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `TowerLevel_EnterLevel` | nID, nTeamID, tbLog | PROTO_L__G_TowerLevel_Req_EnterLevel |
| `TowerLevel_LevelFail` | bClear, nID, nSeed, nTowerID, tbLog | PROTO_L__G_TowerLevel_Req_LevelFail |

## VigourSupply (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `VigourSupply_CheckRefresh` | — | PROTO_L__G_VigourSupply_CheckRefresh |
| `VigourSupply_ReceiveVigour` | nId | PROTO_L__G_VigourSupply_ReceiveVigour |

## VirCaptureStaff (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `VirCaptureStaff_Recruit` | nStaffId | PROTO_L__G_VirCaptureBuild_ReqRecruit |
| `VirCaptureStaff_Upgrade` | nMapId, nStaffId | PROTO_L__G_VirCaptureBuild_ReqUpgrade |

## WorldBossLogic (2)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `WorldBossLogic_CheckOpen` | — | PROTO_L__G_WorldBossLogic_CheckOpen<br>_G_WorldBossLogic__CheckOpen |
| `WorldBossLogic_GetReward` | tbTaskID | PROTO_L__G_WorldBossLogic_GetReward<br>_G_WorldBossLogic__GetReward |

## AchievementPoint (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `AchievementPoint_GetReward` | nGroup, nIndex | PROTO_L__G_AchievementPoint_GetReward |

## ActivityFace (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ActivityFace_Update` | bFlag, nId, nType | PROTO_L__G_Activityface_SetPopFlag<br>PROTO_L__G_Activityface_SetPopNum |

## Adjust (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Adjust_Record` | nType | PROTO_L__G_Adjust_DoRecordInfo |

## CallmeLogic (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `CallmeLogic_RecordLog` | tbLog | PROTO_L__G_CallmeLogic_SendLog<br>_G_CallmeLogic__SendLog |

## Cash (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Cash_Exchange` | nCost, nExhcangTarget, nExhcangeCash | PROTO_L__G_CashExchange_Exchange |

## Chapter (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Chapter_SyncGuideLevelPassData` | tbData | PROTO_L__G_Chapter_SyncGuideLevelPassData |

## Chat (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Chat_BlockSettings` | — | PROTO_L__G_Chat_BlockSettings |

## chess.client (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `chess.client_operation_log` | — | PROTO_L__G_ChessClient_WriteOperationLog |

## Daily (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Daily_LevelMoppingUp` | nChapterID, nID, nLevelID, nMultiple, nTeamID | PROTO_L__G_Daily_Req_LevelMopup |

## DLCLogic (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `DLCLogic_CheckOpenAct` | — | PROTO_L__G_DLC_Logic_CheckOpenAct<br>_G_DLC_Logic__CheckOpenAct |

## ElementLogic (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ElementLogic_CheckOpenAct` | — | PROTO_L__G_ElementLogic_CheckOpenAct<br>_G_ElementLogic__CheckOpenAct |

## GacheTry (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GacheTry_GetAlreadyPassedAward` | nActId | PROTO_L__G_GachaTry_Req_GetAlreadyPassedAward |

## GirlRush (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GirlRush_GetAward` | — | PROTO_L__G_GirlRush_Req_GetAward |

## GirlSkinParts (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GirlSkinParts_Update` | nSkinId, tbPartsID | PROTO_L_Item_Fashion_Req_GirlSkinParts_Update |

## GirlWeaponSkin (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `GirlWeaponSkin_Change` | nCardId, nSkinId | PROTO_L__G_WeaponSkin_Req_Change |

## Handbook (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Handbook_GetAward` | nIndex | PROTO_L__G_HandbookLogic_DoAward<br>_G_HandbookLogic__DoAward |

## House (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `House_Request` | — | PROTO_L__G_HouseMessageHandle_HouseMessageSender |

## HouseThrow (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `HouseThrow_ClearData` | — | PROTO_L__G_HouseThrowSeverMessage_ClearData |

## Launch (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Launch_OnCloseLoadingLog` | nLevelID, nSpendTime, nType | PROTO_L__G_Launch_OnCloseLoading |

## Lineup (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Lineup_Update` | index, member1, member2, member3, name | PROTO_L__G_Formation_Req_UpdateLineup<br>PROTO_L__G_VirCapture_InitFormation |

## Lineups (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Lineups_Update` | — | PROTO_L__G_Formation_Req_UpdateLineups |

## Logistics (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Logistics_Evolution` | — | PROTO_L_Item_Logistics_Req_Evolution |

## OnlineBoss (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineBoss_CheckOpenAct` | — | PROTO_L__G_OnlineBoss_CheckOpenAct/_ENV |

## OnlineTowerRush (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `OnlineTowerRush_Equip` | nId, nOnlineId | PROTO_L__G_OnlineTowerRush_ReqEquip<br>_G_OnlineTowerRush__ReqEquip |

## PlayerReturn (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `PlayerReturn_GetReward` | bQuick, missionId, nId, nType | PROTO_L__G_PlayerReturn_GetFirstReward<br>PROTO_L__G_PlayerReturn_GetMissionReward |

## Questionnaire (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Questionnaire_Finish` | nId, nSecret, nTime | PROTO_L__G_Questionnaire_OnClientFinish<br>PROTO_L__G_Questionnaire_OnFinishQuestID |

## Record (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Record_RTL` | online, rtl | PROTO_L__G_DataPost_OnGetRTL |

## Report (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Report_UserInform` | nPid, nReason, sName, sSign | PROTO_L__G_Report_UserInfo |

## Repression (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `Repression_ChangeFormation` | nID, tbFormation | PROTO_L__G_Repression_Chapter_GetLineup<br>PROTO_L__G_Repression_Chapter_SetLineup |

## ReservationReward (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ReservationReward_Gain` | — | PROTO_L_UMG_Main_umg_main_OnOpen |

## RoleCard (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `RoleCard_SetSupporterTeamIndex` | Id, Index | PROTO_L__G_RoleCard_SetSupporterTeamIndex |

## SupportCard (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `SupportCard_Refine` | — | PROTO_L__G_Refine_Req_Refine |

## SupporterSkill (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `SupporterSkill_Evolut` | Id, MatID | PROTO_L_Item_Logistics_Req_Evolut |

## TargetShoot (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `TargetShoot_C2SMsg` | — | PROTO_L__G_TargetShootMsgHandle_TargetShootMsgSender |

## TowerEventLogic (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `TowerEventLogic_GetReward` | nChapterID, nGroup | PROTO_L__G_TowerEvent_GetReward |

## VirCaptureTower (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `VirCaptureTower_GetStarAward` | nChapterId, nDifficult, nIndex | PROTO_L__G_VirCaptureTower_Req_GetStarAward |

## ZoneTime (1)

| 接口 | 参数 | 调用方 |
|---|---|---|
| `ZoneTime_ReqTime` | — | PROTO_L__G_ZoneTime_ReqTime<br>_G_ZoneTime__ReqTime |

## 符号形式 (49)

接口名不是字符串常量，而是模块表字段（如 `Chapter.REQ_ENTER_LEVEL`）。
要拿到字面值需要在运行时把对应模块表的字符串字段 dump 出来。

| 符号 | 参数 | 调用方 |
|---|---|---|
| `Chapter.REQ_ENTER_LEVEL` | bFree, nID, nMultiple, nTeamID, tbLog | PROTO_L__G_Chapter_Req_EnterLevel |
| `Chapter.REQ_GET_STAR_AWARDC` | bMain, nChapterID, nDifficult, nIndex | PROTO_L__G_Chapter_Req_GetStarAward |
| `Chapter.REQ_LEVEL_FAIL` | nID, tbLog | PROTO_L__G_Chapter_Req_LevelFail |
| `Chapter.REQ_NEWPROLOGUE_ENTER_LEVEL` | bFree, nID, nMultiple, nTeamID, tbLog | PROTO_L__G_Chapter_Req_NewPrologue_EnterLevel |
| `Chapter.REQ_NEWPROLOGUE_SETTLEMENT` | bWaitServer, nID, nSeed, nTime, tbLog | PROTO_L__G_Chapter_Req_NewPrologueSettlement |
| `Daily.REQ_ENTER_LEVEL` | nChapterID, nID, nLevelID, nMultiple, nTeamID, tbLog | PROTO_L__G_Daily_Req_EnterLevel |
| `Daily.REQ_GET_ACTIVITY_INFO` | — | PROTO_L__G_Daily_Req_GetActivityInfo |
| `Daily.REQ_Get_Guarantee_Reward` | Suit, Type, bDlc | PROTO_L__G_Daily_GetGuaranteeReward |
| `Daily.REQ_LEVEL_FAIL` | nID, tbLog | PROTO_L__G_Daily_Req_LevelFail |
| `Daily.REQ_Set_Select_Suit` | Suit, Type, bDlc | PROTO_L__G_Daily_SetSelectSuit |
| `DLC_Chapter.REQ_ENTER_LEVEL` | bFree, nChapterID, nID, nMultiple, nTeamID, tbLog | PROTO_L__G_DLC_Chapter_Req_EnterLevel |
| `DLC_Chapter.REQ_GET_STAR_AWARDC` | — | PROTO_L__G_DLC_Chapter_Req_GetStarAward |
| `DLC_Chapter.REQ_LEVEL_FAIL` | nID, tbLog | PROTO_L__G_DLC_Chapter_Req_LevelFail |
| `DLC_Chapter.REQ_MOPPINGUP` | nChapterID, nID, nMultiple, nTeamID, tbLog | PROTO_L__G_DLC_Chapter_Req_Moppingup |
| `DonoDuelArena.REQ_ENTER_LEVEL` | nID, nTeamID, tbLog | PROTO_L__G_DonoDuelArena_Req_EnterLevel |
| `DonoDuelArena.REQ_LEVEL_FAIL` | nID, tbKill, tbLog | PROTO_L__G_DonoDuelArena_Req_LevelFail |
| `DonoDuelRogue.REQ_ENTER_LEVEL` | nID, nTeamID, tbLog | PROTO_L__G_DonoDuelRogue_Req_EnterLevel |
| `DonoDuelRogue.REQ_MINIGAME_SETTLEMENT` | nRoomId, nSeed | PROTO_L__G_DonoDuelRogue_Req_MiniGameAward |
| `DonoDuelRogue.REQ_SELECT_BONDTAG` | nBondTag | PROTO_L__G_DonoDuelRogue_Req_SelectBondTag |
| `ElementLogic.REQ_BUYGOODS` | nGoodsID | PROTO_L__G_ElementLogic_Req_BuyGoods |
| `ElementLogic.REQ_ENTER_LEVEL` | nID, nMultiple, nTeamID, tbLog | PROTO_L__G_ElementLogic_Req_EnterLevel |
| `ElementLogic.REQ_GACHA` | — | PROTO_L__G_ElementLogic_Req_Gacha |
| `ElementLogic.REQ_LEVEL_FAIL` | nID, tbLog | PROTO_L__G_ElementLogic_Req_LevelFail |
| `ElementLogic.REQ_SWEEP` | — | PROTO_L__G_ElementLogic_Req_Sweep |
| `FarmWarActivity.REQ_ENTER_LEVEL` | nID, nTeamID, tbLog | PROTO_L__G_FarmWarActivity_Req_EnterLevel |
| `FarmWarActivity.REQ_LEVEL_FAIL` | B, F, K, P, U, nID, tbLog | PROTO_L__G_FarmWarActivity_Req_LevelFail |
| `GirlRush.REQ_ENTER_LEVEL` | — | PROTO_L__G_GirlRush_Req_EnterLevel |
| `GirlRush.REQ_LEVEL_FAIL` | — | PROTO_L__G_GirlRush_Req_LevelFail |
| `GirlRush.REQ_SAVE_DATA` | — | PROTO_L__G_GirlRush_Req_SaveData |
| `OnlineBoss.REQ_DAMAGE_AWARD` | tbIdList | PROTO_L__G_OnlineBoss_Req_DamageAward |
| `OnlineBoss.REQ_ENTER_LEVEL` | nID, nTeamID, tbLog | PROTO_L__G_OnlineBoss_Req_EnterLevel |
| `OnlineBoss.REQ_LEVEL_FAIL` | nID, tbLog | PROTO_L__G_OnlineBoss_Req_LevelFail |
| `OnlineTraining.REQ_ENTER_LEVEL` | nID, nOnlineId, nTeamID, tbLog | PROTO_L__G_OnlineTraining_Req_EnterLevel |
| `OnlineTraining.REQ_LEVEL_FAIL` | nID, tbLog | PROTO_L__G_OnlineTraining_Req_LevelFail |
| `Reconnect.REQ_DealLevelSettlement` | — | PROTO_L__G_Reconnect_Send_SettleInfo |
| `Repression_Chapter.REQ_ENTER_LEVEL` | nID, nMultiple, nTeamID, tbLog | PROTO_L__G_Repression_Chapter_Req_EnterLevel |
| `Repression_Chapter.REQ_FirstEnter` | — | PROTO_L__G_Repression_Chapter_IsFirstEnter |
| `Repression_Chapter.REQ_GET_STAR_AWARDC` | — | PROTO_L__G_Repression_Chapter_Req_GetStarAward |
| `Repression_Chapter.REQ_LEVEL_FAIL` | nID, tbLog | PROTO_L__G_Repression_Chapter_Req_LevelFail |
| `Role.REQ_ENTER_LEVEL` | nID, nMultiple, nTeamID, tbLog | PROTO_L__G_Role_Req_EnterLevel |
| `Role.REQ_LEVEL_FAIL` | nID, tbLog | PROTO_L__G_Role_Req_LevelFail |
| `Role.REQ_LEVEL_MOPUP` | nID, nMultiple, nRoleID | PROTO_L__G_Role_Req_LevelMopup |
| `TowerEventChapter.REQ_ENTER_LEVEL` | nID, nTeamID, tbLog | PROTO_L__G_TowerEventChapter_Req_EnterLevel |
| `TowerEventChapter.REQ_LEVEL_FAIL` | nID, tbLog | PROTO_L__G_TowerEventChapter_Req_LevelFail |
| `VirCapture.REQ_ENTER_LEVEL` | nLevelID, nTeamID, tbLog | PROTO_L__G_VirCapture_Req_EnterLevel |
| `VirCaptureTower.REQ_ENTER_LEVEL` | nID, nTeamID, tbLog | PROTO_L__G_VirCaptureTower_Req_EnterLevel |
| `VirCaptureTower.REQ_LEVEL_FAIL` | nID, tbLog | PROTO_L__G_VirCaptureTower_Req_LevelFail |
| `VirCaptureTrial.REQ_ENTER_LEVEL` | nID, nTeamID, tbLog | PROTO_L__G_VirCaptureTrial_Req_EnterLevel |
| `VirCaptureTrial.REQ_LEVEL_FAIL` | nID, tbLog | PROTO_L__G_VirCaptureTrial_Req_LevelFail |

