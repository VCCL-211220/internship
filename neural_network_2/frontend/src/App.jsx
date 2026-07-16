import { useState } from "react";
import ReactECharts from "echarts-for-react";
import "./App.css";

const rawApiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

const API_BASE_URL = rawApiUrl.startsWith("http")
  ? rawApiUrl
  : `https://${rawApiUrl}`;

function App() {
  const [preview, setPreview] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const imageToPixels = (file) => {
    return new Promise((resolve, reject) => {
      const image = new Image();
      const imageUrl = URL.createObjectURL(file);

      image.onload = () => {
        const canvas = document.createElement("canvas");
        canvas.width = 28;
        canvas.height = 28;

        const ctx = canvas.getContext("2d");

        // 设置白色背景
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, 28, 28);

        // 把上传的图片压缩成 28×28
        ctx.drawImage(image, 0, 0, 28, 28);

        const imageData = ctx.getImageData(0, 0, 28, 28);
        const data = imageData.data;

        const pixels = [];

        for (let i = 0; i < data.length; i += 4) {
          const r = data[i];
          const g = data[i + 1];
          const b = data[i + 2];

          // 把彩色图片转成灰度值
          const gray = 0.299 * r + 0.587 * g + 0.114 * b;

          // 把白底黑字转换成 MNIST 更接近的黑底白字
          const inverted = 255 - gray;

          pixels.push(Math.round(inverted));
        }

        URL.revokeObjectURL(imageUrl);
        resolve(pixels);
      };

      image.onerror = () => {
        reject(new Error("图片读取失败"));
      };

      image.src = imageUrl;
    });
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    setPreview(URL.createObjectURL(file));
    setResult(null);
    setLoading(true);

    try {
      const pixels = await imageToPixels(file);

      const response = await fetch(`${API_BASE_URL}/api/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          pixels: pixels
        })
      });

      const data = await response.json();

      if (data.success) {
        setResult(data);
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.log(error);
      alert("识别失败，请检查后端是否正在运行");
    } finally {
      setLoading(false);
    }
  };

  const option = {
    title: {
      text: "0-9 数字识别分数",
      left: "center"
    },
    tooltip: {},
    xAxis: {
      type: "category",
      data: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    },
    yAxis: {
      type: "value",
      min: 0,
      max: 1
    },
    series: [
      {
        name: "识别分数",
        type: "bar",
        data: result ? result.scores : []
      }
    ]
  };

  return (
    <div className="page">
      <div className="card">
        <p className="description">上传手写数字图片</p>

        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
        />

        {preview && (
          <div className="preview-box">
            <p>上传图片预览：</p>
            <img src={preview} alt="preview" className="preview-image" />
          </div>
        )}

        {loading && <p className="loading">正在识别中...</p>}

        {result && (
          <div className="result-box">
            <h2>预测结果：{result.label}</h2>

            <ReactECharts
              option={option}
              style={{ height: "400px", width: "100%" }}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;