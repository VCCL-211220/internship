import { useState } from "react";
import { Card, Form, Input, Button, message } from "antd";

function Register({ goLogin }) {
  const [loading, setLoading] = useState(false);

  const handleRegister = (values) => {
    setLoading(true);

    fetch("http://127.0.0.1:5000/api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(values),
    })
      .then((response) => response.json())
      .then((result) => {
        if (result.success) {
          message.success(result.message);

          if (goLogin) {
            goLogin();
          }
        } else {
          message.error(result.message);
        }
      })
      .catch((error) => {
        console.log("注册请求失败：", error);
        message.error("注册请求失败");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div className="auth-page">
      <Card title="注册账号" className="auth-card">
        <Form layout="vertical" onFinish={handleRegister}>
          <Form.Item
            label="用户名"
            name="username"
            rules={[{ required: true, message: "请输入用户名" }]}
          >
            <Input placeholder="请输入用户名" />
          </Form.Item>

          <Form.Item label="邮箱" name="email">
            <Input placeholder="请输入邮箱，可选" />
          </Form.Item>

          <Form.Item
            label="密码"
            name="password"
            rules={[{ required: true, message: "请输入密码" }]}
          >
            <Input.Password placeholder="请输入密码" />
          </Form.Item>

          <Button type="primary" htmlType="submit" loading={loading} block>
            注册
          </Button>

          <Button type="link" onClick={goLogin} block>
            已有账号？去登录
          </Button>
        </Form>
      </Card>
    </div>
  );
}

export default Register;