# 批量替换日期功能实现计划

## 需求概述

在编辑工单顶部增加批量替换功能，用于替换界面上所有控件中的日期部分，时间部分保持不变。

## 功能要求

1. **界面显示**（仅编辑模式下显示）
   - 原始日期选择器（仅选择年月日）
   - 替换日期选择器（仅选择年月日）
   - "批量替换"按钮

2. **替换逻辑**
   - 替换所有日期时间选择器中的日期部分，保持时间部分不变
   - 例如：2025-01-12 10:35:50 → 2026-01-12 10:35:50
   - 替换所有文本框中的日期部分
   - 例如："四川省成都市简阳市观音井路辅路2025-01-12 10:41:33" → "四川省成都市简阳市观音井路辅路2026-01-12 10:41:33"

3. **数据持久化**
   - 新增字段（originalDate、replaceDate）不保存到数据库

## 实现方案

### 修改文件

**frontend/src/views/WorkOrderForm.vue**

### 实现步骤

1. **添加批量替换 UI 组件**
   - 在 el-card 标题下方添加批量替换区域
   - 仅在编辑模式（isEditMode）下显示
   - 使用 el-date-picker 组件，type="date" 仅选择年月日
   - 添加"批量替换"按钮

2. **添加响应式变量**
   - originalDate：原始日期
   - replaceDate：替换日期

3. **实现批量替换函数 batchReplaceDates()**
   该函数需要处理：
   - **日期字段替换**：遍历 formData 中所有 Date 类型字段
     - 保持原有的时、分、秒
     - 替换年、月、日
   - **文本字段替换**：遍历 formData 中所有 String 类型字段
     - 使用正则表达式匹配日期格式（YYYY-MM-DD）
     - 替换匹配到的日期部分
   - **数组字段处理**：处理 operationRecords、products、settlementList、attachmentGroups、serviceRequirements 等数组中的嵌套字段

4. **需要处理的字段清单**
   - 基本信息：createdDate、appointmentStartTime、appointmentEndTime、completeTime、evaluationTime
   - 详情信息：expectedStartTime、expectedEndTime、outboundTime
   - 操作记录：operationRecords[].lastModifiedDate
   - 节点信息：completeFeedbackTime、createdFeedbackTime、inServiceFeedbackTime、sendOrdersFeedbackTime
   - 结算信息：settlementBuyTime、settlementInstallTime、settlementList[].fksj
   - 子信息阅读栏：serviceRequirements[].createdDate
   - 所有文本字段：contactName、contactPhone、signInLocation、annexName、serviceRequireTypeDesc、serviceRequireContent 等

## 风险考虑

1. **正则表达式匹配**：确保能正确匹配各种日期格式
2. **数组嵌套处理**：正确遍历和处理数组中的嵌套对象
3. **性能**：由于是前端操作，对于大量数据可能有性能影响，但通常可以接受
4. **数据安全**：替换操作是临时的，用户可选择保存或取消

## 验证计划

1. 验证仅在编辑模式下显示批量替换功能
2. 验证日期选择器仅显示年月日
3. 验证日期时间选择器中的日期替换正确
4. 验证文本框中的日期替换正确
5. 验证数组中的日期替换正确
6. 验证替换后的数据可以正常保存
