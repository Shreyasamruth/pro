import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Login = () => {
  const [userType, setUserType] = useState("patient");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/login", {
        user_type: userType,
        username,
        password,
      });

      localStorage.setItem("token", response.data.access_token);
      navigate("/dashboard");
    } catch (error) {
      alert("Invalid Credentials!");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-8 shadow-md rounded-md w-96">
        <h2 className="text-xl font-semibold text-center">Login</h2>
        <select className="w-full mt-2 p-2 border" onChange={(e) => setUserType(e.target.value)}>
          <option value="patient">Patient</option>
          <option value="doctor">Doctor</option>
        </select>
        <input className="w-full mt-2 p-2 border" type="text" placeholder="Email" onChange={(e) => setUsername(e.target.value)} />
        <input className="w-full mt-2 p-2 border" type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
        <button className="w-full bg-blue-500 text-white p-2 mt-4" onClick={handleLogin}>Login</button>
      </div>
    </div>
  );
};

export default Login;
