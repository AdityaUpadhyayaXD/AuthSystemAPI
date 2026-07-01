import { useEffect } from "react";
import api from "./api/axios";

function App() {

  useEffect(() => {

    api.get("/")
      .then((res) => {
        console.log(res.data);
      })
      .catch((err) => {
        console.log(err);
      });

  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900">
      <h1 className="text-white text-5xl font-bold">
        Authentication System
      </h1>
    </div>
  );
}

export default App;