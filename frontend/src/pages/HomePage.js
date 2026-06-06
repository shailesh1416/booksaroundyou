import React from 'react';

const HomePage = () => {
  return (
    <div className="py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Share Books, Build Community
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Find books near you. Safe exchanges at local centers.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2">🔒 Safe Exchanges</h3>
          <p className="text-gray-600">
            Meet at verified local centers. No stranger danger, no phone numbers shared.
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2">📍 Find Locally</h3>
          <p className="text-gray-600">
            Discover books in your area. Filter by genre, language, and proximity.
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2">🚀 Easy Tracking</h3>
          <p className="text-gray-600">
            Track book requests, handovers, and return dates all in one dashboard.
          </p>
        </div>
      </div>

      <div className="mt-12 text-center">
        <p className="text-gray-600 text-sm">
          Feature development in progress. Features will be added soon.
        </p>
      </div>
    </div>
  );
};

export default HomePage;
