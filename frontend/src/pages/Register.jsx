import { useState } from "react";
import api from "../services/api";

function Register() {

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const register = async () => {

        console.log("Register button clicked");

        try {

            const response = await api.post(
                "/register",
                {
                    name,
                    email,
                    password
                }
            );

            console.log(response);

            alert("Registration Successful");

            setName("");
            setEmail("");
            setPassword("");

        } catch (error) {

            console.log(error);

            if (error.response) {
                alert("Backend Error: " + JSON.stringify(error.response.data));
            } else {
                alert("Cannot connect to backend");
            }
        }
    };

    return (
        <div>

            <h1>Register</h1>

            <input
                type="text"
                placeholder="Name"
                value={name}
                onChange={(e) =>
                    setName(e.target.value)
                }
            />

            <br />
            <br />

            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) =>
                    setEmail(e.target.value)
                }
            />

            <br />
            <br />

            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) =>
                    setPassword(e.target.value)
                }
            />

            <br />
            <br />

            <button onClick={register}>
                Register
            </button>

        </div>
    );
}

export default Register;