import { useEffect, useState } from "react";
import axios from "axios";

const Dashboard = () => {
  const [appointments, setAppointments] = useState([]);
  const userId = 1; // Replace with actual user ID from authentication
  const token = localStorage.getItem("token");

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/get_appointments?patient_id=${userId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setAppointments(response.data);
      } catch (error) {
        console.error("Error fetching appointments:", error);
      }
    };

    fetchAppointments();
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold">Your Appointments</h2>
      {appointments.length === 0 ? (
        <p className="mt-4 text-gray-500">No appointments scheduled.</p>
      ) : (
        <ul className="mt-4">
          {appointments.map((appt, index) => (
            <li key={index} className="p-4 bg-white shadow-md rounded-md mb-3">
              <p><strong>Doctor:</strong> {appt.doctor}</p>
              <p><strong>Specialty:</strong> {appt.specialty}</p>
              <p><strong>Date & Time:</strong> {appt.appointment_time}</p>
              <p><strong>Status:</strong> {appt.status}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Dashboard;
