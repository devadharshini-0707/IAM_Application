import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
    getUsers,
    deleteUser,
    disableUser,
    enableUser,
} from "../services/user";

function Users() {
    const navigate = useNavigate();

    const [users, setUsers] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    const loadUsers = async () => {
        try {
            const data = await getUsers();
            setUsers(data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadUsers();
    }, []);

    const handleDelete = async (id: string) => {
        if (!window.confirm("Are you sure you want to delete this user?")) {
            return;
        }

        try {
            await deleteUser(id);
            loadUsers();
        } catch (error) {
            console.error(error);
        }
    };

    const handleDisable = async (id: string) => {
        try {
            await disableUser(id);
            loadUsers();
        } catch (error) {
            console.error(error);
        }
    };

    const handleEnable = async (id: string) => {
        try {
            await enableUser(id);
            loadUsers();
        } catch (error) {
            console.error(error);
        }
    };

    if (loading) {
        return (
            <div
                style={{
                    padding: 40,
                    fontFamily: "Arial",
                }}
            >
                <h2>Loading Users...</h2>
            </div>
        );
    }

    return (
        <div
            style={{
                padding: 40,
                fontFamily: "Arial",
            }}
        >
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: 30,
                }}
            >
                <div>
                    <h1>User Management</h1>
                    <p>Manage all users in your organization.</p>
                </div>

                <button
                    onClick={() => navigate("/users/create")}
                    style={{
                        padding: "10px 18px",
                        background: "#2563eb",
                        color: "white",
                        border: "none",
                        borderRadius: 8,
                        cursor: "pointer",
                    }}
                >
                    + Create User
                </button>
            </div>

            <table
                style={{
                    width: "100%",
                    borderCollapse: "collapse",
                }}
            >
                <thead>
                    <tr
                        style={{
                            background: "#f3f4f6",
                        }}
                    >
                        <th
                            style={{
                                padding: 12,
                                textAlign: "left",
                            }}
                        >
                            Username
                        </th>

                        <th>Email</th>

                        <th>Status</th>

                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>
                    {users.map((user) => (
                        <tr
                            key={user.user_id}
                            style={{
                                borderBottom: "1px solid #ddd",
                            }}
                        >
                            <td
                                style={{
                                    padding: 12,
                                }}
                            >
                                {user.username}
                            </td>

                            <td>{user.email}</td>

                            <td>
                                <span
                                    style={{
                                        fontWeight: "bold",
                                        color:
                                            user.status === "active"
                                                ? "green"
                                                : user.status === "disabled"
                                                ? "orange"
                                                : "red",
                                    }}
                                >
                                    {user.status}
                                </span>
                            </td>

                            <td>
                                <button
                                    onClick={() =>
                                        navigate(
                                            `/users/edit/${user.user_id}`
                                        )
                                    }
                                    disabled={user.status === "deleted"}
                                    style={{
                                        marginRight: 8,
                                    }}
                                >
                                    Edit
                                </button>

                                {user.status === "active" && (
                                    <button
                                        onClick={() =>
                                            handleDisable(user.user_id)
                                        }
                                        style={{
                                            marginRight: 8,
                                        }}
                                    >
                                        Disable
                                    </button>
                                )}

                                {user.status === "disabled" && (
                                    <button
                                        onClick={() =>
                                            handleEnable(user.user_id)
                                        }
                                        style={{
                                            marginRight: 8,
                                        }}
                                    >
                                        Enable
                                    </button>
                                )}

                                {user.status !== "deleted" && (
                                    <button
                                        onClick={() =>
                                            handleDelete(user.user_id)
                                        }
                                    >
                                        Delete
                                    </button>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Users;