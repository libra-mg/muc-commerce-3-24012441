from pathlib import Path

import pandas as pd


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def load_dashboard_data(base_dir: Path, selected_category: str = "全部") -> dict:
    data_dir = base_dir / "data"
    metrics_df = _read_csv(data_dir / "overall_metrics.csv")
    category_df = _read_csv(data_dir / "category_analysis.csv")
    segment_df = _read_csv(data_dir / "segment_analysis.csv")

    metric_map = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    # TODO 2-1：在已有两张指标卡基础上，增加“总体流失率”和“平均订单数”。
    metrics = [
        {"label": "总用户数", "value": f"{int(metric_map['用户数']):,}", "note": "人"},
        {"label": "流失用户", "value": f"{int(metric_map['流失人数']):,}", "note": "人"},
        {"label": "总体流失率", "value": f"{metric_map['流失率']:.1%}", "note": ""},
        {"label": "平均订单数", "value": f"{metric_map['平均订单数']:.2f}", "note": "单/人"},
    ]

    categories = ["全部", *category_df["PreferedOrderCat"].tolist()]
    table_df = category_df.copy()
    # TODO 3-1：选择具体品类后筛选table_df。
    # 提示：教师参考项目中使用布尔条件筛选。
    if selected_category != "全部":
        table_df = table_df[table_df["PreferedOrderCat"] == selected_category]

    table_df = table_df.rename(
        columns={
            "PreferedOrderCat": "偏好品类",
            "用户数": "用户数",
            "流失率": "流失率",
            "平均订单数": "平均订单数",
        }
    )[["偏好品类", "用户数", "流失率", "平均订单数"]]
    table_df["流失率"] = table_df["流失率"].map(lambda value: f"{value:.1%}")
    table_df["平均订单数"] = table_df["平均订单数"].map(lambda value: f"{value:.2f}")

    # TODO 2-2：找出流失率最高的生命周期阶段，并生成一句数据观察。
    max_idx = segment_df["流失率"].idxmax()
    highest_segment = segment_df.loc[max_idx, "TenureGroup"]
    highest_rate = segment_df.loc[max_idx, "流失率"]
    insight = (
        f"生命周期阶段中，'{highest_segment}' 的流失率最高，达到 {highest_rate:.1%}，"
        f"该阶段用户数为 {int(segment_df.loc[max_idx, '用户数'])} 人。"
    )

    return {
        "metrics": metrics,
        "categories": categories,
        "category_rows": table_df.to_dict("records"),
        "insight": insight,
    }


def get_segment_analysis(base_dir: Path):
    """读取生命周期分析数据，并返回记录和观察结论"""
    data_dir = base_dir / "data"
    segment_df = _read_csv(data_dir / "segment_analysis.csv")
    # 找出流失率最高的行
    max_idx = segment_df["流失率"].idxmax()
    highest_segment = segment_df.loc[max_idx, "TenureGroup"]
    highest_rate = segment_df.loc[max_idx, "流失率"]
    insight = (
        f"生命周期阶段中，'{highest_segment}' 的流失率最高，达到 {highest_rate:.1%}，"
        f"该阶段用户数为 {int(segment_df.loc[max_idx, '用户数'])} 人。"
    )
    records = segment_df.to_dict("records")
    return records, insight