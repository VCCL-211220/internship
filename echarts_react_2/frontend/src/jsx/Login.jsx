import { useState } from "react";
import { Card, Form, Input, Button, message } from "antd";

function Login({ onLogin, goRegister }) {
  const [loading, setLoading] = useState(false);

  const handleLogin = (values) => {
    setLoading(true);

    fetch("http://127.0.0.1:5000/api/login", {
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

          if (onLogin) {
            onLogin(result.user);
          }
        } else {
          message.error(result.message);
        }
      })
      .catch((error) => {
        console.log("登录请求失败：", error);
        message.error("登录请求失败");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div className="auth-page">
      <Card title="登录数据可视化平台" className="auth-card">
        <Form layout="vertical" onFinish={handleLogin}>
          <Form.Item
            label="用户名"
            name="username"
            rules={[{ required: true, message: "请输入用户名" }]}
          >
            <Input placeholder="请输入用户名" />
          </Form.Item>

          <Form.Item
            label="密码"
            name="password"
            rules={[{ required: true, message: "请输入密码" }]}
          >
            <Input.Password placeholder="请输入密码" />
          </Form.Item>

          <Button type="primary" htmlType="submit" loading={loading} block>
            登录
          </Button>

          <Button type="link" onClick={goRegister} block>
            没有账号？去注册
          </Button>
        </Form>
      </Card>
    </div>
  );
}

export default Login;