import { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";

function Rating() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/movies/top-rating")
      .then((response) => response.json())
      .then((result) => {
        setData(result);
      })
      .catch((error) => {
        console.log("请求评分数据失败：", error);
      });
  }, []);

  const option = {
    title: {
      text: "豆瓣电影评分 Top10"
    },
    tooltip: {},
    xAxis: {
      type: "category",
      data: data.map((item) => item.title),
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: "value",
      min: 9
    },
    series: [
      {
        name: "评分",
        type: "bar",
        data: data.map((item) => item.rating)
      }
    ]
  };

  return <ReactECharts option={option} style={{ height: "500px" }} />;
}

export default Rating;