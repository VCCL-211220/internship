import { useState } from "react";
import { Menu, Button } from "antd";

import Rating from "./Rating";
import Year from "./Year";
import Country from "./Country";
import Director from "./Director";
import Genre from "./Genre";
import Actor from "./Actor";

function Dashboard({ onLogout }) {
  const [currentChart, setCurrentChart] = useState("rating");

  return (
    <div className="page">
      <Button className="logout-button" onClick={onLogout}>
        退出登录
      </Button>

      <h1 className="page-title">豆瓣电影数据可视化</h1>

      <div className="menu-wrapper">
        <Menu
          className="chart-menu"
          mode="horizontal"
          selectedKeys={[currentChart]}
          onClick={(e) => setCurrentChart(e.key)}
          items={[
            { key: "rating", label: "评分 Top10" },
            { key: "year", label: "年份分布" },
            { key: "country", label: "国家/地区分布" },
            { key: "director", label: "导演 Top10" },
            { key: "genre", label: "类型分布" },
            { key: "actor", label: "演员 Top10" },
          ]}
        />
      </div>

      <div className="chart-card">
        {currentChart === "rating" && <Rating />}
        {currentChart === "year" && <Year />}
        {currentChart === "country" && <Country />}
        {currentChart === "director" && <Director />}
        {currentChart === "genre" && <Genre />}
        {currentChart === "actor" && <Actor />}
      </div>
    </div>
  );
}

export default Dashboard;