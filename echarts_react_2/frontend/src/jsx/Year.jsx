import { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";

function Year() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/movies/year-count")
      .then((response) => response.json())
      .then((result) => {
        setData(result);
      })
      .catch((error) => {
        console.log("请求年份数据失败：", error);
      });
  }, []);

  const option = {
    title: {
      text: "豆瓣电影 Top100 年份分布"
    },
    tooltip: {},
    xAxis: {
      type: "category",
      data: data.map((item) => item.year),
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: "value"
    },
    series: [
      {
        name: "电影数量",
        type: "line",
        data: data.map((item) => item.count)
      }
    ]
  };

  return <ReactECharts option={option} style={{ height: "500px" }} />;
}

export default Year;