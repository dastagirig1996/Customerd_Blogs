import React, { useState, useEffect } from 'react';
import axiosInstance from '../../utils/axiosConfig';
import { useParams ,useNavigate} from 'react-router-dom';
import './Customer.css';
import LogoutButton from '../logout/Logout';
 
const CustomerList = () => {
  const { id } = useParams();
  const [customers, setCustomers] = useState([]);
  const [error, setError] = useState('');
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [loading, setLoading] = useState(false);
 
  const navigate = useNavigate()
  const fetchCustomers = async () => {
    setLoading(true);
    const token = localStorage.getItem('access_token');
    try {
      const response = await axiosInstance.get('http:localhost:8500/customers/customer/', {
        headers: { Authorization: `Token ${token}` },
      });
      setCustomers(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch customer data.');
      // navigate("/login")
    }
    setLoading(false);
  };
 
 
  const fetchCustomerById = async (customerId) => {
    setLoading(true);
    const token = localStorage.getItem('access_token');
    try {
      const response = await axiosInstance.get(`http://35.200.248.136:9500/customers/customer/${customerId}/`, {
        headers: { Authorization: `Token ${token}` },
      });
      setSelectedCustomer(response.data);
      setError('');
    } catch (err) {
      if (err.response && err.response.status === 404) {
        setError('Customer ID does not exist.');
      } else {
        // navigate("/login")
        setError('Failed to fetch customer details.');
      }
      setSelectedCustomer(null);
    }
    setLoading(false);
  };
 
 
  useEffect(() => {
    fetchCustomers();
  }, []);
 
 
  useEffect(() => {
    if (id) {
      fetchCustomerById(id);
    }
  }, [id]);
 
  return (
    <div className="customer-container">
      <h2>Customer Management</h2>
 
      {error && <p className="error">{error}</p>}
 
      {loading && <p>Loading...</p>}
 
      {!selectedCustomer && (
        <ul className="customer-list">
          {customers.map((customer) => (
            <li key={customer.id} onClick={() => fetchCustomerById(customer.id)}>
              {customer.id} - {customer.first_name} {customer.last_name}
            </li>
          ))}
        </ul>
      )}
 
      {selectedCustomer && (
        <div className="customer-details">
          <h3>Customer Details</h3>
          <p><strong>ID:</strong> {selectedCustomer.id}</p>
          <p><strong>First Name:</strong> {selectedCustomer.first_name}</p>
          <p><strong>Last Name:</strong> {selectedCustomer.last_name}</p>
          <p><strong>Date of Birth:</strong> {selectedCustomer.date_of_birth}</p>
          <p><strong>Phone Number:</strong> {selectedCustomer.phone_number}</p>
 
          <button onClick={() => setSelectedCustomer(null)}>Back to List</button>
        </div>
      )}
 
      <LogoutButton />
    </div>
  );
};
 
export default CustomerList;
 