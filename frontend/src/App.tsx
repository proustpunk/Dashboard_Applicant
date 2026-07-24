import {

    BrowserRouter,

    Routes,

    Route,

    Navigate

} from "react-router-dom";


import Login from "./pages/Login";

import Candidates from "./pages/Candidates";

import CandidateDetail from "./pages/CandidateDetail";

import ProtectedRoute from "./components/ProtectedRoute";





export default function App(){



    return (


        <BrowserRouter>


            <Routes>



                <Route

                    path="/"

                    element={

                        <Navigate

                            to="/login"

                            replace

                        />

                    }

                />





                <Route

                    path="/login"

                    element={<Login />}

                />







                <Route

                    path="/candidates"

                    element={

                        <ProtectedRoute>


                            <Candidates />


                        </ProtectedRoute>


                    }

                />







                <Route

                    path="/candidates/:id"

                    element={


                        <ProtectedRoute>


                            <CandidateDetail />


                        </ProtectedRoute>


                    }

                />





            </Routes>


        </BrowserRouter>


    )

}