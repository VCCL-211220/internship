import { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";

function Actor() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/movies/top-actors")
      .then((response) => response.json())
      .then((result) => {
        setData(result);
      })
      .catch((error) => {
        console.log("请求演员数据失败：", error);
      });
  }, []);

  const option = {
    title: {
      text: "豆瓣电影 Top100 演员参演次数 Top10"
    },
    tooltip: {},
    xAxis: {
      type: "value"
    },
    yAxis: {
      type: "category",
      data: data.map((item) => item.actor)
    },
    series: [
      {
        name: "参演电影数量",
        type: "bar",
        data: data.map((item) => item.count)
      }
    ]
  };

  return <ReactECharts option={option} style={{ height: "500px" }} />;
}

export default Actor;