from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
    segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"
    #  4-1：补充“流失率”“偏好品类”“生命周期风险”和“订单”四类问答。
    # 每个回答都必须引用data目录中已经计算的指标，不得编造数值。
    # 流失率
    if any(word in normalized for word in ["流失率", "总体流失"]):
        return f"总体流失率为 {metrics['流失率']:.1%}。"
    # 偏好品类
    if any(word in normalized for word in ["偏好品类", "最多人", "最受欢迎"]):
        top_idx = category_df["用户数"].idxmax()
        top_cat = category_df.loc[top_idx, "PreferedOrderCat"]
        top_count = int(category_df.loc[top_idx, "用户数"])
        return f"偏好品类中，'{top_cat}' 的用户最多，共有 {top_count} 人。"
    # 生命周期风险
    if any(word in normalized for word in ["生命周期", "阶段", "风险最高"]):
        max_idx = segment_df["流失率"].idxmax()
        seg = segment_df.loc[max_idx, "TenureGroup"]
        rate = segment_df.loc[max_idx, "流失率"]
        return f"生命周期阶段 '{seg}' 的流失率最高，为 {rate:.1%}。"
    # 订单
    if any(word in normalized for word in ["订单", "平均订单"]):
        return f"平均订单数为 {metrics['平均订单数']:.2f} 笔/人。"
    
    return (
         "非常抱歉，我暂时只能回答关于总用户数、总体流失率、偏好品类、生命周期风险和平均订单数的问题。"
        "请换一种更具体的问法。"
    )
