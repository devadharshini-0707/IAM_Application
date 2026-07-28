import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    createUser,
    getCurrentUser,
} from "../services/user";

function CreateUser() {
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");

    const [organizationId, setOrganizationId] =
        useState("");

    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadCurrentUser();
    }, []);

    const loadCurrentUser = async () => {
        try {
            const currentUser =
                await getCurrentUser();

            setOrganizationId(
                currentUser.primary_organization_id
            );
        } catch (err) {
            console.error(err);
            alert("Failed to load current user.");
        }
    };

    const handleSubmit = async (
        e: React.FormEvent
    ) => {
        e.preventDefault();

        try {
            setLoading(true);

            await createUser({
                username,
                email,
                primary_organization_id:
                    organizationId,
            });

            alert("User created successfully.");

            navigate("/users");
        } catch (err: any) {
            console.error(err);

            alert(
                err?.response?.data?.detail ??
                    "Failed to create user."
            );
        } finally {
            setLoading(false);
        }
    };

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
            <h1>Invite User</h1>

            <form onSubmit={handleSubmit}>
                <div
                    style={{
                        marginBottom: 20,
                    }}
                >
                    <label>Username</label>

                    <br />

                    <input
                        value={username}
                        onChange={(e) =>
                            setUsername(
                                e.target.value
                            )
                        }
                        style={{
                            width: "100%",
                            padding: 10,
                            marginTop: 5,
                        }}
                        required
                    />
                </div>

                <div
                    style={{
                        marginBottom: 20,
                    }}
                >
                    <label>Email</label>

                    <br />

                    <input
                        type="email"
                        value={email}
                        onChange={(e) =>
                            setEmail(
                                e.target.value
                            )
                        }
                        style={{
                            width: "100%",
                            padding: 10,
                            marginTop: 5,
                        }}
                        required
                    />
                </div>

                <div
                    style={{
                        marginBottom: 20,
                    }}
                >
                    <label>Organization</label>

                    <br />

                    <input
                        value={organizationId}
                        disabled
                        style={{
                            width: "100%",
                            padding: 10,
                            marginTop: 5,
                            background: "#f3f4f6",
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
                        disabled={loading}
                    >
                        {loading
                            ? "Creating..."
                            : "Create User"}
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

export default CreateUser;