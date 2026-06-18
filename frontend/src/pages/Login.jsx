import { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

function Login() {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const login = async () => {

        try {

            const response = await api.post(
                "/login",
                {
                    email,
                    password
                }
            );

            localStorage.setItem(
                "token",
                response.data.access_token
            );

            alert("Login Successful");

            navigate("/dashboard");

        } catch {

            alert("Login Failed");
        }
    };

    return (
        <div>

            <h1>Login</h1>

            <input
                placeholder="Email"
                onChange={(e) =>
                    setEmail(e.target.value)
                }
            />

            <br />

            <input
                type="password"
                placeholder="Password"
                onChange={(e) =>
                    setPassword(e.target.value)
                }
            />

            <br />

            <button onClick={login}>
                Login
            </button>

        </div>
    );
}

export default Login;