import axios from 'axios';
import { useNavigate } from 'react-router-dom';
 
const axiosInstance = axios.create();
 
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const navigate = useNavigate();
   
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');
      try {
        const res = await axiosInstance.post('http://localhost:8500/customers/refresh/', { refresh: refreshToken });
        const { access_token } = res.data;
     
        localStorage.setItem('access_token', access_token);
        axiosInstance.defaults.headers.common['Authorization'] = `Token ${access_token}`;
 
        return axiosInstance(originalRequest);
      } catch (err) {
        console.error('Refresh token failed', err);
 
     
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
 
       
        const currentUrl = window.location.pathname;
 
        navigate(currentUrl, { replace: true });
      }
    }
 
    return Promise.reject(error);
  }
);
 
export default axiosInstance;