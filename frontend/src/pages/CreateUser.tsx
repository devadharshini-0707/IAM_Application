import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createUser } from "../services/user";

function CreateUser() {
    const navigate = useNavigate();

    const [form, setForm] = useState({
        username: "",
        email: "",
        primary_organization_id: "",
    });

    const [loading, setLoading] = useState(false);

    const handleChange = (
        e: React.ChangeEvent<HTMLInputElement>
    ) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (
        e: React.FormEvent
    ) => {
        e.preventDefault();

        try {
            setLoading(true);

            const response = await createUser(form);

            console.log("SUCCESS:", response);

            alert("User created successfully.");

            navigate("/users");
        } catch (err: any) {
            console.error("========== CREATE USER ERROR ==========");
            console.error(err);

            console.log("Status:", err.response?.status);
            console.log("Response:", err.response?.data);

            const error = err.response?.data;

            if (typeof error?.detail === "string") {
                alert(error.detail);
            } else if (Array.isArray(error?.detail)) {
                alert(
                    error.detail
                        .map((item: any) => {
                            return `${item.loc.join(" -> ")} : ${item.msg}`;
                        })
                        .join("\n")
                );
            } else {
                alert(JSON.stringify(error, null, 2));
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            style={{
                maxWidth: "600px",
                margin: "50px auto",
                fontFamily: "Arial",
            }}
        >
            <h1>Create User</h1>

            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: 20 }}>
                    <label>Username</label>
                    <input
                        type="text"
                        name="username"
                        value={form.username}
                        onChange={handleChange}
                        required
                        style={{
                            width: "100%",
                            padding: 10,
                            marginTop: 5,
                        }}
                    />
                </div>

                <div style={{ marginBottom: 20 }}>
                    <label>Email</label>
                    <input
                        type="email"
                        name="email"
                        value={form.email}
                        onChange={handleChange}
                        required
                        style={{
                            width: "100%",
                            padding: 10,
                            marginTop: 5,
                        }}
                    />
                </div>

                <div style={{ marginBottom: 20 }}>
                    <label>Primary Organization ID</label>
                    <input
                        type="text"
                        name="primary_organization_id"
                        value={form.primary_organization_id}
                        onChange={handleChange}
                        required
                        style={{
                            width: "100%",
                            padding: 10,
                            marginTop: 5,
                        }}
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    style={{
                        padding: "12px 24px",
                        background: "#2563eb",
                        color: "white",
                        border: "none",
                        borderRadius: "6px",
                        cursor: "pointer",
                    }}
                >
                    {loading ? "Creating..." : "Create User"}
                </button>
            </form>
        </div>
    );
}

export default CreateUser;