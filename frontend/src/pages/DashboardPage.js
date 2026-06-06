import React from 'react';
import { useAuth } from '../context/AuthContext';

const DashboardPage = () => {
  const { user, logout, loading } = useAuth();

  if (loading) {
    return <div>Loading user...</div>;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-gray-600">Welcome back, {user?.name || 'reader'}.</p>
        </div>
        <button
          onClick={logout}
          className="bg-red-600 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-3">Your Profile</h2>
          <p className="text-gray-700">Email: {user?.email}</p>
          <p className="text-gray-700">Role: {user?.role}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-3">Next Steps</h2>
          <ul className="list-disc list-inside text-gray-700">
            <li>Create a book listing</li>
            <li>Search books by location</li>
            <li>Request a book safely</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
