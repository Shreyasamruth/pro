import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import RegisterPatient from "./components/RegisterPatient";
import RegisterDoctor from "./components/RegisterDoctor";
import Dashboard from "./components/Dashboard";
import ScheduleAppointment from "./components/ScheduleAppointment";
import Notifications from "./components/Notifications";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register-patient" element={<RegisterPatient />} />
        <Route path="/register-doctor" element={<RegisterDoctor />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/schedule" element={<ScheduleAppointment />} />
        <Route path="/notifications" element={<Notifications />} />
      </Routes>
    </Router>
  );
}

export default App;
