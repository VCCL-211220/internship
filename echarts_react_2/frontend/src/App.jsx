import { useState } from "react";
import Login from "./jsx/Login";
import Register from "./jsx/Register";
import Dashboard from "./jsx/Dashboard";
import "./App.css";
import "antd/dist/reset.css";

function App() {
  const [user, setUser] = useState(null);
  const [page, setPage] = useState("login");

  const handleLogin = (userInfo) => {
    setUser(userInfo);
  };

  const handleLogout = () => {
    setUser(null);
    setPage("login");
  };

  if (user === null) {
    if (page === "login") {
      return (
        <Login
          onLogin={handleLogin}
          goRegister={() => setPage("register")}
        />
      );
    }

    return <Register goLogin={() => setPage("login")} />;
  }

  return <Dashboard onLogout={handleLogout} />;
}

export default App;