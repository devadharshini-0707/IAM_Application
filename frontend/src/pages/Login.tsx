import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "../services/auth";

function Login() {
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleLogin = async () => {
        setError("");

        if (!email || !password) {
            setError("Please enter both email and password.");
            return;
        }

        try {
            setLoading(true);

            const response = await login({
                email,
                password,
            });

            console.log("LOGIN RESPONSE:", response);

            if (!response.access_token) {
                setError("Backend did not return an access token.");
                return;
            }

            localStorage.setItem("access_token", response.access_token);

            console.log(
                "TOKEN SAVED:",
                localStorage.getItem("access_token")
            );

            alert("Login Successful!");

            navigate("/dashboard");
        } catch (err: any) {
            console.error(err);

            if (err.response?.data?.detail) {
                setError(err.response.data.detail);
            } else {
                setError("Invalid email or password.");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                minHeight: "100vh",
                background: "#f5f7fb",
            }}
        >
            <div
                style={{
                    width: "420px",
                    background: "white",
                    padding: "35px",
                    borderRadius: "12px",
                    boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
                    display: "flex",
                    flexDirection: "column",
                    gap: "15px",
                }}
            >
                <h1
                    style={{
                        textAlign: "center",
                    }}
                >
                    Login
                </h1>

                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    style={{
                        padding: "12px",
                        borderRadius: "8px",
                        border: "1px solid #ccc",
                    }}
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{
                        padding: "12px",
                        borderRadius: "8px",
                        border: "1px solid #ccc",
                    }}
                />

                {error && (
                    <div
                        style={{
                            color: "red",
                        }}
                    >
                        {error}
                    </div>
                )}

                <button
                    type="button"
                    onClick={handleLogin}
                    disabled={loading}
                    style={{
                        padding: "12px",
                        border: "none",
                        borderRadius: "8px",
                        background: "#2563eb",
                        color: "white",
                        cursor: "pointer",
                    }}
                >
                    {loading ? "Logging in..." : "Login"}
                </button>

                <div style={{ textAlign: "center" }}>
                    Don't have an account?{" "}
                    <Link to="/">Create Organization</Link>
                </div>
            </div>
        </div>
    );
}

export default Login;