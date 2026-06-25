import { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";

function Genre() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/movies/genre-count")
      .then((response) => response.json())
      .then((result) => {
        setData(result);
      })
      .catch((error) => {
        console.log("请求类型数据失败：", error);
      });
  }, []);

  const option = {
    title: {
      text: "豆瓣电影 Top100 类型分布"
    },
    tooltip: {
      trigger: "item"
    },
    series: [
      {
        name: "电影类型",
        type: "pie",
        radius: "60%",
        data: data.map((item) => ({
          name: item.genre,
          value: item.count
        }))
      }
    ]
  };

  return <ReactECharts option={option} style={{ height: "500px" }} />;
}

export default Genre;