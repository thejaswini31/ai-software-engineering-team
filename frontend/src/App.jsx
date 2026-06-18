import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import UploadPdf from "./pages/UploadPdf";
import Chat from "./pages/Chat";

function App() {

  return (

    <BrowserRouter>

      <Routes>
        <Route
          path="/register"
          element={<Register />}
        />

        <Route
          path="/"
          element={<Login />}
        />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/upload"
          element={<UploadPdf />}
        />

        <Route
          path="/chat"
          element={<Chat />}
        />

      </Routes>

    </BrowserRouter>

  );
}

export default App;