import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    getUsers,
    disableUser,
    enableUser,
    deleteUser,
} from "../services/user";

function Users() {
    const navigate = useNavigate();

    const [users, setUsers] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    const [search, setSearch] = useState("");

    const [page, setPage] = useState(1);
    const pageSize = 10;

    const [totalPages, setTotalPages] = useState(1);

    useEffect(() => {
        loadUsers();
    }, [page]);

    const loadUsers = async (
        keyword: string = search
    ) => {
        try {
            setLoading(true);

            const data = await getUsers(
                page,
                pageSize,
                keyword
            );

            setUsers(data.items);
            setTotalPages(data.total_pages);
        } catch (err) {
            console.error(err);
            alert("Failed to load users.");
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async () => {
        setPage(1);
        await loadUsers(search);
    };

    const handleDisableEnable = async (
        user: any
    ) => {
        try {
            if (user.status === "active") {
                await disableUser(user.user_id);
                alert("User disabled successfully.");
            } else {
                await enableUser(user.user_id);
                alert("User enabled successfully.");
            }

            loadUsers();
        } catch (err) {
            console.error(err);
            alert("Operation failed.");
        }
    };

    const handleDelete = async (
        user: any
    ) => {
        const confirmed = window.confirm(
            `Delete user "${user.username}"?`
        );

        if (!confirmed) {
            return;
        }

        try {
            await deleteUser(user.user_id);

            alert("User deleted successfully.");

            loadUsers();
        } catch (err) {
            console.error(err);
            alert("Delete failed.");
        }
    };

    if (loading) {
        return (
            <div style={{ padding: 30 }}>
                <h2>Loading users...</h2>
            </div>
        );
    }

    return (
        <div style={{ padding: 30 }}>
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: 20,
                }}
            >
                <h1>Users</h1>

                <button
                    onClick={() =>
                        navigate("/users/create")
                    }
                    style={{
                        padding: "10px 18px",
                        background: "#2563eb",
                        color: "white",
                        border: "none",
                        borderRadius: 8,
                        cursor: "pointer",
                        fontWeight: "bold",
                    }}
                >
                    + Invite User
                </button>
            </div>

            <div
                style={{
                    display: "flex",
                    gap: 10,
                    marginBottom: 20,
                }}
            >
                <input
                    type="text"
                    placeholder="Search username or email..."
                    value={search}
                    onChange={(e) =>
                        setSearch(e.target.value)
                    }
                    style={{
                        flex: 1,
                        padding: 10,
                    }}
                />

                <button
                    onClick={handleSearch}
                >
                    Search
                </button>
            </div>

            <table
                style={{
                    width: "100%",
                    borderCollapse: "collapse",
                    border: "1px solid #ddd",
                }}
            >
                <thead>
                    <tr
                        style={{
                            background: "#f3f4f6",
                        }}
                    >
                        <th style={{ padding: 12 }}>
                            Username
                        </th>

                        <th style={{ padding: 12 }}>
                            Email
                        </th>

                        <th style={{ padding: 12 }}>
                            Status
                        </th>

                        <th style={{ padding: 12 }}>
                            Actions
                        </th>
                    </tr>
                </thead>

                <tbody>
                    {users.length === 0 ? (
                        <tr>
                            <td
                                colSpan={4}
                                style={{
                                    textAlign: "center",
                                    padding: 20,
                                }}
                            >
                                No users found.
                            </td>
                        </tr>
                    ) : (
                        users.map((user) => (
                            <tr
                                key={user.user_id}
                            >
                                <td
                                    style={{
                                        padding: 12,
                                    }}
                                >
                                    {user.username}
                                </td>

                                <td
                                    style={{
                                        padding: 12,
                                    }}
                                >
                                    {user.email}
                                </td>

                                <td
                                    style={{
                                        padding: 12,
                                    }}
                                >
                                    {user.status}
                                </td>

                                <td
                                    style={{
                                        padding: 12,
                                        display: "flex",
                                        gap: 10,
                                    }}
                                >
                                    <button
                                        onClick={() =>
                                            navigate(
                                                `/users/edit/${user.user_id}`
                                            )
                                        }
                                    >
                                        Edit
                                    </button>

                                    <button
                                        onClick={() =>
                                            handleDisableEnable(
                                                user
                                            )
                                        }
                                    >
                                        {user.status ===
                                        "active"
                                            ? "Disable"
                                            : "Enable"}
                                    </button>

                                    <button
                                        onClick={() =>
                                            handleDelete(
                                                user
                                            )
                                        }
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>

            <div
                style={{
                    marginTop: 20,
                    display: "flex",
                    justifyContent:
                        "space-between",
                    alignItems: "center",
                }}
            >
                <button
                    disabled={page === 1}
                    onClick={() =>
                        setPage(page - 1)
                    }
                >
                    Previous
                </button>

                <span>
                    Page {page} of {totalPages}
                </span>

                <button
                    disabled={
                        page >= totalPages
                    }
                    onClick={() =>
                        setPage(page + 1)
                    }
                >
                    Next
                </button>
            </div>

            <div
                style={{
                    marginTop: 20,
                }}
            >
                <button
                    onClick={() =>
                        navigate("/dashboard")
                    }
                    style={{
                        padding: "10px 18px",
                        border: "none",
                        borderRadius: 8,
                        background: "#6b7280",
                        color: "white",
                        cursor: "pointer",
                    }}
                >
                    ← Back to Dashboard
                </button>
            </div>
        </div>
    );
}

export default Users;