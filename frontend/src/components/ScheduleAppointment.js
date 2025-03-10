import { useState } from "react";
import axios from "axios";

const ScheduleAppointment = () => {
  const [appointment, setAppointment] = useState({ patient_id: "", doctor_id: "", appointment_time: "" });

  const handleSubmit = async () => {
    try {
      await axios.post("http://127.0.0.1:5000/schedule_appointment", appointment, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });
      alert("Appointment Scheduled!");
    } catch (error) {
      alert("Error scheduling appointment!");
    }
  };

  return (
    <div className="p-8">
      <h2 className="text-xl font-semibold">Schedule Appointment</h2>
      <input className="w-full mt-2 p-2 border" type="number" placeholder="Patient ID" onChange={(e) => setAppointment({ ...appointment, patient_id: e.target.value })} />
      <input className="w-full mt-2 p-2 border" type="number" placeholder="Doctor ID" onChange={(e) => setAppointment({ ...appointment, doctor_id: e.target.value })} />
      <input className="w-full mt-2 p-2 border" type="datetime-local" onChange={(e) => setAppointment({ ...appointment, appointment_time: e.target.value })} />
      <button className="w-full bg-blue-500 text-white p-2 mt-4" onClick={handleSubmit}>Schedule</button>
    </div>
  );
};

export default ScheduleAppointment;
