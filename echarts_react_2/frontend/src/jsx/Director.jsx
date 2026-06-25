import { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";

function Director() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/movies/top-directors")
      .then((response) => response.json())
      .then((result) => {
        setData(result);
      })
      .catch((error) => {
        console.log("请求导演数据失败：", error);
      });
  }, []);

  const option = {
    title: {
      text: "豆瓣电影 Top100 导演作品数量 Top10"
    },
    tooltip: {},
    xAxis: {
      type: "value"
    },
    yAxis: {
      type: "category",
      data: data.map((item) => item.director)
    },
    series: [
      {
        name: "电影数量",
        type: "bar",
        data: data.map((item) => item.count)
      }
    ],
    grid: {
        left: "30%",
        right: "8%",
        top: "18%",
        bottom: "8%"
      }
  };

  return <ReactECharts option={option} style={{ height: "500px" }} />;
}

export default Director;