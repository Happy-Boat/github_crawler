import sqlite3

def generate_standalone_html():
    # 连接到数据库
    conn = sqlite3.connect('stars.db')
    cursor = conn.cursor()

    # 执行 SQL 查询
    cursor.execute('SELECT * FROM stars')
    stars = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    # 关闭数据库连接
    conn.close()

    # 生成 HTML 表格的头部
    table_header = "<tr>"
    for col in columns:
        table_header += f"<th class=\"py-2 px-4 border-b\">{col}</th>"
    table_header += "</tr>"

    # 生成 HTML 表格的内容
    table_content = ""
    for row in stars:
        table_content += "<tr>"
        for cell in row:
            table_content += f"<td class=\"py-2 px-4 border-b\">{cell}</td>"
        table_content += "</tr>"

    # 生成完整的 HTML 内容
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stars Database</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 p-8">
    <h1 class="text-3xl font-bold mb-4">Stars Database</h1>
    <table class="min-w-full bg-white border border-gray-300">
        <thead>
            {table_header}
        </thead>
        <tbody>
            {table_content}
        </tbody>
    </table>
</body>
</html>
    """

    return html_template

# 示例用法
if __name__ == "__main__":
    # 生成 HTML 内容
    html_content = generate_standalone_html()

    # 保存到文件
    with open("standalone_star.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("独立 HTML 文件已生成: standalone_star.html")