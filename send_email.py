import smtplib
import base64
import os

# 发件人邮箱和授权码
sender_email = "18043063568@163.com"
sender_password = "HAqL4nFAyp77784q"  # 替换为你的 163 邮箱授权码

# 收件人邮箱
receiver_email = "2400013094@stu.pku.edu.cn"

# 邮件主题
subject = "包含 HTML 文件附件的邮件"

# 邮件正文
body = "这封邮件包含 standalone_follow_graph.html 和 standalone_star.html 两个附件。"

# 边界字符串，用于分隔邮件各部分
boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"

print("开始构建邮件内容...")

# 构建邮件头部
message = f"From: {sender_email}\n"
message += f"To: {receiver_email}\n"
message += f"Subject: =?utf-8?B?{base64.b64encode(subject.encode('utf-8')).decode('utf-8')}?=\n"
message += f"MIME-Version: 1.0\n"
message += f"Content-Type: multipart/mixed; boundary={boundary}\n\n"

# 添加邮件正文
message += f"--{boundary}\n"
message += "Content-Type: text/plain; charset=utf-8\n"
message += "Content-Transfer-Encoding: 7bit\n\n"
message += f"{body}\n\n"

# 处理 standalone_follow_graph.html 附件
if os.path.exists('standalone_follow_graph.html'):
    print("找到 standalone_follow_graph.html 文件，开始处理...")
    with open('standalone_follow_graph.html', 'rb') as file:
        file_content = file.read()
    encoded_content = base64.b64encode(file_content).decode('utf-8')
    message += f"--{boundary}\n"
    message += "Content-Type: text/html; name=standalone_follow_graph.html\n"
    message += "Content-Disposition: attachment; filename=standalone_follow_graph.html\n"
    message += "Content-Transfer-Encoding: base64\n\n"
    message += f"{encoded_content}\n\n"
    print("standalone_follow_graph.html 文件处理完成。")
else:
    print("未找到 standalone_follow_graph.html 文件。")

# 结束边界
message += f"--{boundary}--"

print("邮件内容构建完成。")

# 打印邮件内容（可选，内容可能很长）
# print("即将发送的邮件内容：")
# print(message)

print("尝试连接到 163 邮箱的 SMTP 服务器...")
try:
    server = smtplib.SMTP_SSL("smtp.163.com", 465)
    print("成功连接到 SMTP 服务器，开始登录...")
    server.login(sender_email, sender_password)
    print("登录成功，开始发送邮件...")

    # 发送邮件
    server.sendmail(sender_email, receiver_email, message.encode('utf-8'))
    print("邮件发送成功！")
except smtplib.SMTPException as e:
    print(f"SMTP 错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
finally:
    if 'server' in locals():
        try:
            server.quit()
            print("SMTP 连接已关闭。")
        except smtplib.SMTPServerDisconnected:
            print("SMTP 服务器已断开连接。")
