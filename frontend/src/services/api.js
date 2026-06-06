import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',
  withCredentials: true,
});

// Auth Service
export const authService = {
  login: (idToken) => apiClient.post('/auth/login', { id_token: idToken }),
  logout: () => apiClient.post('/auth/logout'),
  getCurrentUser: () => apiClient.get('/auth/user'),
};

// Books Service
export const booksService = {
  createBook: (bookData) => apiClient.post('/books', bookData),
  getBook: (bookId) => apiClient.get(`/books/${bookId}`),
  updateBook: (bookId, bookData) => apiClient.put(`/books/${bookId}`, bookData),
  deleteBook: (bookId) => apiClient.delete(`/books/${bookId}`),
  searchBooks: (params) => apiClient.get('/books/search', { params }),
  requestBook: (bookId, requestData) => apiClient.post(`/books/${bookId}/request`, requestData),
};

// Centers Service
export const centersService = {
  getAllCenters: (params) => apiClient.get('/centers', { params }),
  getCenter: (centerId) => apiClient.get(`/centers/${centerId}`),
  confirmDropoff: (centerId, requestData) => apiClient.post(`/centers/${centerId}/dropoff-confirm`, requestData),
  confirmHandover: (centerId, requestData) => apiClient.post(`/centers/${centerId}/handover-confirm`, requestData),
};

// Admin Service
export const adminService = {
  getDashboard: () => apiClient.get('/admin/dashboard'),
  getAllUsers: () => apiClient.get('/admin/users'),
  moderateListing: (listingId, action) => apiClient.post(`/admin/listings/${listingId}/moderate`, { action }),
};

export default apiClient;
