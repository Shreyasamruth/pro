import { useEffect, useState } from "react";
import axios from "axios";

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const userId = 1; // Replace with actual user ID from authentication
  const token = localStorage.getItem("token");

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const response = await axios.post("http://127.0.0.1:5000/send_appointments_reminder", 
          { patient_id: userId, appointment_id: 1 },  // Replace appointment_id dynamically
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setNotifications([response.data.message]);
      } catch (error) {
        console.error("Error fetching notifications:", error);
      }
    };

    fetchNotifications();
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold">Notifications</h2>
      {notifications.length === 0 ? (
        <p className="mt-4 text-gray-500">No notifications available.</p>
      ) : (
        <ul className="mt-4">
          {notifications.map((notif, index) => (
            <li key={index} className="p-4 bg-yellow-100 shadow-md rounded-md mb-3">
              {notif}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Notifications;
