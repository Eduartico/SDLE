// src/views/List.js

import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ApiService from '../services/ApiService';

const List = () => {
  const { listId } = useParams();
  const [list, setList] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchList = async () => {
      try {
        const response = await ApiService.getListById(listId);
        setList(response.data.list);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching list:', error);
        setError('An error occurred while fetching the list.');
        setLoading(false);
      }
    };

    fetchList();
  }, [listId]);

  const handleQuantityChange = (itemId, newQuantity) => {
    setList((prevList) => {
      const updatedItems = prevList.items.map((item) => {
        if (item.id === itemId) {
          return { ...item, boughtQuantity: newQuantity };
        }
        return item;
      });

      return { ...prevList, items: updatedItems };
    });
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p style={{ color: 'red' }}>{error}</p>;
  }

  return (
    <div>
      <h2>List Name: {list.name}</h2>

      <ul>
        {list.items.map((item) => (
          <li key={item.id}>
            <div>
              <strong>{item.name}</strong>
              <label>
                <input
                  type="checkbox"
                  checked={item.boughtQuantity === item.quantity}
                  onChange={() => handleQuantityChange(item.id, item.quantity)}
                />
                Bought
              </label>

              {item.quantity > 1 && (
                <label>
                  Quantity:
                  <select
                    value={item.boughtQuantity}
                    onChange={(e) => handleQuantityChange(item.id, parseInt(e.target.value, 10))}
                  >
                    {[...Array(item.quantity).keys()].map((num) => (
                      <option key={num + 1} value={num + 1}>
                        {num + 1}
                      </option>
                    ))}
                  </select>
                </label>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default List;
