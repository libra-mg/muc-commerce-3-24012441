from functools import wraps
from pathlib import Path
import pandas as pd
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from services.data_service import load_dashboard_data
from services.qa_service import answer_question


BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config["SECRET_KEY"] = "day07-classroom-demo-key"


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            flash("请先登录后再访问数据看板。", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def index():
    return redirect(url_for("dashboard") if "username" in session else url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username == "student" and password == "day07":
            session["username"] = username
            flash("登录成功，欢迎进入电商用户分析系统。", "success")
            return redirect(url_for("dashboard"))
        flash("账号或密码错误。演示账号：student / day07", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("你已安全退出。", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    category = request.args.get("category", "全部")
    dashboard_data = load_dashboard_data(BASE_DIR, category)
    return render_template(
        "dashboard.html",
        username=session["username"],
        selected_category=category,
        **dashboard_data,
    )


@app.route("/assistant")
@login_required
def assistant():
    return render_template("assistant.html", username=session["username"])


@app.route("/api/ask", methods=["POST"])
@login_required
def ask():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()
    if not question:
        return jsonify({"ok": False, "answer": "请输入一个与项目数据有关的问题。"}), 400
    return jsonify({"ok": True, "answer": answer_question(BASE_DIR, question)})


# 拓展B：生命周期详情页
@app.template_filter('format_number')
def format_number(value):
    return f"{value:,}"

@app.route('/segments')
def segments():
    data_dir = Path('data')
    seg_df = pd.read_csv(data_dir / 'segment_analysis.csv', encoding='utf-8-sig')
    if '流失人数' not in seg_df.columns:
        seg_df['流失人数'] = (seg_df['用户数'] * seg_df['流失率']).round().astype(int)
    seg_df = seg_df.sort_values('流失率', ascending=False)
    max_row = seg_df.iloc[0]
    insight = (
        f"生命周期阶段 {max_row['TenureGroup']} 流失率最高，达到 {max_row['流失率']:.1%}，"
        f"该阶段共有 {int(max_row['用户数']):,} 名用户，流失人数 {max_row['流失人数']:,} 人。"
        " 需重点关注早期用户（0-12月）的留存策略。"
    )
    rows = seg_df.to_dict('records')
    return render_template('segments.html', rows=rows, insight=insight)


@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=False, port=5000)
