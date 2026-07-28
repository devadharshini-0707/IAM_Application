import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import api from "../services/api";
import { updateUser } from "../services/user";

function EditUser() {
    const navigate = useNavigate();
    const { userId } = useParams();

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");

    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        loadUser();
    }, []);

    const loadUser = async () => {
        try {
            const response = await api.get(
                `/users/${userId}`
            );

            setUsername(response.data.username);
            setEmail(response.data.email);
        } catch (err) {
            console.error(err);
            alert("Failed to load user.");
            navigate("/users");
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (
        e: React.FormEvent
    ) => {
        e.preventDefault();

        try {
            setSaving(true);

            await updateUser(userId!, {
                username,
                email,
            });

            alert("User updated successfully.");

            navigate("/users");
        } catch (err: any) {
            console.error(err);

            alert(
                err?.response?.data?.detail ??
                "Failed to update user."
            );
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div style={{ padding: 40 }}>
                <h2>Loading...</h2>
            </div>
        );
    }

    return (
        <div
            style={{
                maxWidth: 600,
                margin: "40px auto",
                padding: 30,
                border: "1px solid #ddd",
                borderRadius: 10,
            }}
        >
            <h1>Edit User</h1>

            <form onSubmit={handleSubmit}>
                <div
                    style={{
                        marginBottom: 20,
                    }}
                >
                    <label>Username</label>

                    <input
                        value={username}
                        onChange={(e) =>
                            setUsername(e.target.value)
                        }
                        style={{
                            width: "100%",
                            padding: 10,
                            marginTop: 5,
                        }}
                    />
                </div>

                <div
                    style={{
                        marginBottom: 20,
                    }}
                >
                    <label>Email</label>

                    <input
                        type="email"
                        value={email}
                        onChange={(e) =>
                            setEmail(e.target.value)
                        }
                        style={{
                            width: "100%",
                            padding: 10,
                            marginTop: 5,
                        }}
                    />
                </div>

                <div
                    style={{
                        display: "flex",
                        gap: 10,
                    }}
                >
                    <button
                        type="submit"
                        disabled={saving}
                    >
                        {saving
                            ? "Saving..."
                            : "Save Changes"}
                    </button>

                    <button
                        type="button"
                        onClick={() =>
                            navigate("/users")
                        }
                    >
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    );
}

export default EditUser;