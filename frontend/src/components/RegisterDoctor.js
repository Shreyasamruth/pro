import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const RegisterDoctor = () => {
  const [formData, setFormData] = useState({ name: "", specialty: "" });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://127.0.0.1:5000/register_doctor", formData);
      alert("Doctor registered successfully!");
      navigate("/");
    } catch (error) {
      alert("Registration failed!");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-8 shadow-md rounded-md w-96">
        <h2 className="text-xl font-semibold text-center">Register as Doctor</h2>
        <form onSubmit={handleSubmit}>
          <input className="w-full mt-2 p-2 border" type="text" placeholder="Full Name" onChange={(e) => setFormData({ ...formData, name: e.target.value })} />
          <input className="w-full mt-2 p-2 border" type="text" placeholder="Specialty" onChange={(e) => setFormData({ ...formData, specialty: e.target.value })} />
          <button className="w-full bg-green-500 text-white p-2 mt-4" type="submit">Register</button>
        </form>
      </div>
    </div>
  );
};

export default RegisterDoctor;
