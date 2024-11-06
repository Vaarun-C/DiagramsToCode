import axios from 'axios';

const axiosInstance = axios.create({
  validateStatus: function (status) {
    return status >= 200 && status < 400;
  },
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

export default axiosInstance;
