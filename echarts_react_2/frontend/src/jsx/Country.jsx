import { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";

function Country() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/movies/country-count")
      .then((response) => response.json())
      .then((result) => {
        setData(result);
      })
      .catch((error) => {
        console.log("请求国家数据失败：", error);
      });
  }, []);

  const option = {
    title: {
      text: "豆瓣电影 Top100 国家/地区分布"
    },
    tooltip: {},
    xAxis: {
      type: "category",
      data: data.map((item) => item.country),
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
        type: "bar",
        data: data.map((item) => item.count)
      }
    ]
  };

  return <ReactECharts option={option} style={{ height: "500px" }} />;
}

export default Country;