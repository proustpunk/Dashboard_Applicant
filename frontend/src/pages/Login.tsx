import { useState } from "react";
import api from "../api/axios";
import { useAuth } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom";


export default function Login(){

    const [email,setEmail] = useState("");
    const [password,setPassword] = useState("");

    const {login} = useAuth();

    const navigate = useNavigate();


    async function handleLogin(){

        try{

            const form = new URLSearchParams();

            form.append(
                "username",
                email
            );

            form.append(
                "password",
                password
            );


            const response = await api.post(
                "/auth/login",
                form,
                {
                    headers:{
                        "Content-Type":
                        "application/x-www-form-urlencoded"
                    }
                }
            );


            login(
                response.data.access_token
            );


            navigate("/candidates");


        }catch(error){

            console.log(error);

            alert(
                "Login failed"
            );
        }

    }


    return (

        <div>

            <h1>
                Login
            </h1>


            <input
                placeholder="email"
                value={email}
                onChange={
                    e=>setEmail(e.target.value)
                }
            />


            <input
                placeholder="password"
                type="password"
                value={password}
                onChange={
                    e=>setPassword(e.target.value)
                }
            />


            <button
                onClick={handleLogin}
            >
                Login
            </button>


        </div>

    )
}