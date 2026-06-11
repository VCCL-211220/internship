import { useState } from "react";
import "./App.css";

function App() {
  const [messageInput, setMessageInput] = useState("");
  const [bodyInput, setBodyInput] = useState("");
  const [paramInput, setParamInput] = useState("");

  const [getResult, setGetResult] = useState("");
  const [postResult, setPostResult] = useState("");

  const handleGetClick = async () => {
    const response = await fetch(`/get_message?message=${messageInput}`);
    const data = await response.text();

    setGetResult(data);
  };

  const handlePostClick = async () => {
    const response = await fetch(`/post_message?param=${paramInput}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        body: bodyInput,
      }),
    });

    const data = await response.text();

    setPostResult(data);
  };

  return (
    <div className="App">

      <div>
        <h2>GET</h2>

        <input
          type="text"
          value={messageInput}
          onChange={(event) => setMessageInput(event.target.value)}
          placeholder="请输入参数"
        />

        <button onClick={handleGetClick}>确认</button>

        <p>后端返回：{getResult}</p>
      </div>

      <div>
        <h2>POST</h2>

        <input
          type="text"
          value={bodyInput}
          onChange={(event) => setBodyInput(event.target.value)}
          placeholder="请输入body参数"
        />

        <input
          type="text"
          value={paramInput}
          onChange={(event) => setParamInput(event.target.value)}
          placeholder="请输入param参数"
        />

        <button onClick={handlePostClick}>确认</button>

        <p>后端返回：{postResult}</p>
      </div>
    </div>
  );
}

export default App;