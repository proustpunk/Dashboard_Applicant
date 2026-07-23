import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Candidates from "./pages/Candidates";
import CandidateDetail from "./pages/CandidateDetail";

function App() {

  return (
    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={
            <Navigate to="/login" />
          }
        />

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/candidates"
          element={<Candidates />}
        />

        <Route
    path="/candidates/:id"
    element={<CandidateDetail />}
/>

      </Routes>

    </BrowserRouter>
  )
}

export default App;