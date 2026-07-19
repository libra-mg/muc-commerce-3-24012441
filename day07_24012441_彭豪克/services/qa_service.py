from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"
    #  4-1：补充“流失率”“偏好品类”“生命周期风险”和“订单”四类问答。
    # 每个回答都必须引用data目录中已经计算的指标，不得编造数值。
    # 1.流失率
    if any(word in normalized for word in ["流失率", "流失比例", "流失多少"]):
        churn_rate = metrics["流失率"]
        churn_count = int(metrics["流失人数"])
        return f"总体流失率为 {churn_rate:.1%}，共 {churn_count:,} 名用户流失。"
    # 2.偏好品类
    if any(word in normalized for word in ["哪个品类", "偏好品类", "最多用户", "最受欢迎"]):
        cat_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
        cat_df.columns = cat_df.columns.str.strip()
        max_row = cat_df.loc[cat_df["用户数"].idxmax()]
        category_col = "PreferedOrderCat" if "PreferedOrderCat" in cat_df.columns else "偏好品类"
        return f"用户数最多的偏好品类是「{max_row[category_col]}」，共有{int(max_row['用户数']):,}名用户。"
    # 3.生命周期风险
    if any(word in normalized for word in ["生命周期", "哪个阶段", "风险最高", "流失最高"]):
        seg_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")
        max_row = seg_df.loc[seg_df["流失率"].idxmax()]
        stage = max_row["TenureGroup"]
        rate = max_row["流失率"]
        count = int(max_row["用户数"])
        return f"流失率最高的生命周期阶段是 {stage} ，流失率为 {rate:.1%}，该阶段共有 {count:,} 名用户。"
    # 4.订单
    if any(word in normalized for word in ["平均订单", "订单数", "多少订单"]):
        avg = metrics["平均订单数"]
        median = metrics["订单数中位数"]
        return f"平均订单数为 {avg:.2f} 单/人，中位数为 {median:.0f} 单/人。"

    return (
        "抱歉，我目前只能回答关于用户数、流失率、偏好品类、生命周期风险和订单情况的问题。"
        "请换一种更具体的问法。"
    )
